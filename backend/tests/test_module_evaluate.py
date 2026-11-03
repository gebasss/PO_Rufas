"""Avaliação de dietas: modelo linear contra as funções de restrição do próprio RuFaS (FSD, Anexo B.9).

As ofertas "originais" vêm de ``RationOptimizer`` (o mesmo código que o RuFaS usa ao formular a ração).
"""

import numpy as np
import pytest

from dietopt.feeds import feed_library
from dietopt.module import linear
from dietopt.module.categories import constraints_for
from dietopt.module.evaluate import MAX_DIETS, evaluate_diets, rank
from dietopt.module.library import build_feeds
from dietopt.module.requirements import compute_requirements
from dietopt.module.rufas import rufas

LACTACAO = dict(
    body_weight=650, mature_body_weight=700, parity=2, days_in_milk=100, calving_interval=400,
    milk_production=40, milk_fat=3.7, milk_true_protein=3.1, milk_lactose=4.85,
    housing="Barn", distance=100, day_of_pregnancy=60, body_condition_score_5=3.0,
)  # fmt: skip
SECA = dict(
    body_weight=740, mature_body_weight=740, parity=2, day_of_pregnancy=250, calving_interval=400,
    housing="Barn", distance=100,
)  # fmt: skip
NOVILHA = dict(
    body_weight=450, mature_body_weight=700, day_of_pregnancy=100, parity=0, average_daily_gain_heifer=0.8,
    body_condition_score_5=3.0, days_born=500, housing="Barn", distance=100,
)  # fmt: skip
LOTE = dict(enteric_methane=400, urinary_nitrogen=0.2)  # valores de teste (energia do NASEM)
PRECOS = {23: 1.10, 44: 0.28, 50: 0.09, 110: 0.12, 138: 0.25, 167: 0.55, 230: 0.10}
# Ração que o otimizador do RuFaS devolveu para o "Conjunto base" (NRC): TDN de 59,97%, no regime sem desconto (D = 1).
RACAO_RUFAS = {"name": "RuFaS", "amounts": {50: 11.87, 110: 19.42, 44: 0.63, 167: 0.63, 230: 0.6, 23: 0.03}}
# Ração com mais concentrado: TDN de 69,9%, no regime com desconto de ingestão (D < 1) no NRC.
RACAO_CONCENTRADO = {"name": "Concentrado", "amounts": {50: 9, 110: 10, 44: 8, 167: 3, 230: 0.2}}
RACAO_SILAGEM = {"name": "Só silagem", "amounts": {50: 15, 110: 15}}
# Pouca proteína degradável no rúmen: na PM, o ramo da PDR (e não o do TDN) é o menor.
RACAO_MILHO = {"name": "Milho e silagem", "amounts": {50: 15, 44: 14}}


def avaliar(standard, category, cow, diets, **kwargs):
    return evaluate_diets(standard, category, cow, diets, PRECOS, **kwargs)


def linhas(resultado, nome):
    dieta = next(d for d in resultado["diets"] if d["name"] == nome)
    return {c["id"]: c for c in dieta["constraints"]}


CASOS = [
    ("NRC", "LAC_COW", LACTACAO),
    ("NASEM", "LAC_COW", {**LACTACAO, **LOTE}),
    ("NRC", "CLOSE_UP", SECA),
    ("NASEM", "CLOSE_UP", {**SECA, **LOTE}),
    ("NRC", "GROWING", NOVILHA),
    ("NASEM", "GROWING", {**NOVILHA, **LOTE}),
]


@pytest.mark.parametrize("standard,category,cow", CASOS)
@pytest.mark.parametrize("dieta", [RACAO_RUFAS, RACAO_CONCENTRADO, RACAO_SILAGEM, RACAO_MILHO], ids=lambda d: d["name"])
def test_oferta_linear_no_ponto_e_igual_a_do_rufas(standard, category, cow, dieta):  # B.9-1
    resultado = avaliar(standard, category, cow, [dieta])
    for linha in resultado["diets"][0]["constraints"]:
        if linha["status"] == "indisponivel":
            continue
        assert linha["supply_linear"] == pytest.approx(linha["supply_nonlinear"], rel=1e-9, abs=1e-6), linha["id"]


def test_vetor_de_referencia_nrc_sem_desconto():  # B.9-7 (as rações da seção 5.3 não estão versionadas: usa-se a do Conjunto base)
    dieta = avaliar("NRC", "LAC_COW", LACTACAO, [RACAO_RUFAS])["diets"][0]
    assert dieta["intake"]["intake_discount"] == 1.0 and dieta["intake"]["tdn_percentage"] == pytest.approx(59.972, abs=1e-3)
    valores = {c["id"]: c["supply_nonlinear"] for c in dieta["constraints"]}
    esperado = {
        "calcium": 315.6117, "phosphorus": 66.2061, "ne_maintenance": 48.2193, "ne_growth": 28.9333,
        "ne_lactation": 47.9016, "ne_total": 48.2193, "protein_min": 2809.2527,
    }  # fmt: skip
    for chave, valor in esperado.items():
        assert valores[chave] == pytest.approx(valor, abs=1e-3), chave
    assert dieta["cost"] == pytest.approx(4.0146, abs=1e-4)


def test_desconto_de_ingestao_abaixo_de_1_acima_de_60_por_cento_de_tdn():
    dieta = avaliar("NRC", "LAC_COW", LACTACAO, [RACAO_CONCENTRADO])["diets"][0]
    assert dieta["intake"]["tdn_percentage"] == pytest.approx(69.92, abs=0.01)
    assert 0.6 <= dieta["intake"]["intake_discount"] < 1.0


def test_erro_fora_do_ponto_fica_em_ate_1_por_cento_na_racao_do_rufas():  # B.9-2 (±5%)
    for standard, cow in (("NRC", LACTACAO), ("NASEM", {**LACTACAO, **LOTE})):
        for linha in avaliar(standard, "LAC_COW", cow, [RACAO_RUFAS])["diets"][0]["constraints"]:
            if linha["status"] != "indisponivel":
                assert linha["error_pct"] <= 1.0, (standard, linha["id"], linha["error_pct"])


def test_erro_fora_do_ponto_cresce_com_o_desconto_de_ingestao_mas_fica_limitado():  # B.9-2, regime com D < 1
    por_regime = {}
    for dieta in (RACAO_RUFAS, RACAO_CONCENTRADO, RACAO_MILHO):
        linhas_ = avaliar("NRC", "LAC_COW", LACTACAO, [dieta])["diets"][0]["constraints"]
        por_regime[dieta["name"]] = {c["id"]: c["error_pct"] for c in linhas_}
    assert max(por_regime["RuFaS"][i] for i in ("ne_maintenance", "ne_lactation")) == pytest.approx(0.0, abs=1e-9)  # D = 1: exato
    for nome in ("Concentrado", "Milho e silagem"):
        erros = por_regime[nome]
        assert 1.0 < erros["ne_maintenance"] < 5.0 and erros["protein_min"] < 1.0, nome


def _modelo(standard, category_animal, cow, ids, x):
    """Restrições linearizadas e configuração do RuFaS para um vetor de quantidades arbitrário."""
    rf = rufas()
    category, animal = category_animal
    nutricao = compute_requirements(standard, category, cow, None, animal).nutrition_requirements
    feeds = build_feeds(standard, ids, {i: 0.3 for i in ids}, {i: (0.0, 100.0) for i in ids})
    pen = (400.0, 0.2) if standard == "NASEM" else None
    config = rf.ration_config(
        nutrient_standard=rf.standard[standard], animal_requirements=nutricao, pen_available_feeds=feeds,
        initial_dry_matter_requirement=nutricao.dry_matter, initial_protein_requirement=nutricao.metabolizable_protein,
        pen_average_body_weight=float(cow["body_weight"]), pen_average_enteric_methane=pen and pen[0],
        pen_average_urine_nitrogen=pen and pen[1],
    )  # fmt: skip
    return linear.build(standard, animal, feeds, np.asarray(x, float), nutricao, float(cow["body_weight"]), pen), config


def test_razoes_de_fibra_e_gordura_tem_forma_linear_exata():  # B.9-3
    ids = [50, 110, 44, 167, 138, 230, 23]
    rng = np.random.default_rng(7)
    referencia = rng.uniform(1, 8, len(ids))
    modelo, config = _modelo("NRC", ("LAC_COW", "LAC_COW"), LACTACAO, ids, referencia)
    originais = {spec.id: spec.rufas_name for spec in constraints_for("NRC", "LAC_COW")}
    for _ in range(40):
        x = rng.uniform(0.0, 12.0, len(ids))
        for restricao in (c for c in modelo if c.kind == "E"):
            folga_original = float(getattr(rufas().optimizer, originais[restricao.id])(x, config))
            folga_linear = float(restricao.homogeneous @ x) * (1 if restricao.sense == "ge" else -1)
            assert (folga_linear >= 0) == (folga_original >= 0), restricao.id


def test_proteina_min_tem_duas_partes_e_a_menor_vale_no_ponto():  # B.9-4
    ids = [50, 110, 44, 167, 138, 230, 23]
    x = np.array([11.87, 19.42, 0.63, 0.63, 0.0, 0.6, 0.03])
    modelo, config = _modelo("NRC", ("LAC_COW", "LAC_COW"), LACTACAO, ids, x)
    proteina = next(c for c in modelo if c.id == "protein_min")
    assert len(proteina.pieces) == 2 and proteina.combine == "min"
    partes = [p.at(x) for p in proteina.pieces]
    folga = float(rufas().optimizer.protein_constraint_lower(x, config))
    assert min(partes) == pytest.approx(folga + proteina.requirement, rel=1e-9)
    assert max(partes) > min(partes)


def test_novilha_e_vaca_seca_nrc_nao_tem_energia_de_lactacao_nem_total():  # B.9-5
    for categoria, cow in (("CLOSE_UP", SECA), ("GROWING", NOVILHA)):
        ids = {c["id"] for c in avaliar("NRC", categoria, cow, [RACAO_RUFAS])["diets"][0]["constraints"]}
        assert not {"ne_total", "ne_lactation"} & ids and {"ne_maintenance", "ne_growth"} <= ids
    ids = {c["id"] for c in avaliar("NRC", "LAC_COW", LACTACAO, [RACAO_RUFAS])["diets"][0]["constraints"]}
    assert {"ne_total", "ne_lactation"} <= ids


def test_ordenacao_da_menos_para_a_mais_recomendada():  # B.9-6
    dietas = [
        {"name": "viável cara", "feasible": True, "cost": 5.0, "violation": 0.0},
        {"name": "inviável pouco", "feasible": False, "cost": 1.0, "violation": 0.05},
        {"name": "viável barata", "feasible": True, "cost": 3.0, "violation": 0.0},
        {"name": "inviável muito", "feasible": False, "cost": 2.0, "violation": 0.4},
    ]
    ordem, melhor = rank(dietas)
    assert ordem == ["inviável muito", "inviável pouco", "viável cara", "viável barata"]
    assert melhor == "viável barata"
    assert rank([dietas[1]]) == (["inviável pouco"], None)


def test_avaliacao_ordena_dietas_reais_e_marca_a_melhor_entre_as_informadas():
    boa = {"name": "Equilibrada", "amounts": {50: 5.5, 110: 5.5, 44: 11, 167: 4, 138: 1.6, 230: 0.25, 23: 0.2}}
    resultado = avaliar("NRC", "LAC_COW", LACTACAO, [RACAO_SILAGEM, boa, RACAO_RUFAS])
    assert resultado["ranking"][0] in {"Só silagem", "RuFaS"} and len(resultado["ranking"]) == 3
    por_nome = {d["name"]: d for d in resultado["diets"]}
    assert not por_nome["Só silagem"]["feasible"] and "phosphorus" in por_nome["Só silagem"]["violated"]
    if resultado["best"]:
        assert por_nome[resultado["best"]]["feasible"]


def test_nasem_replica_amido_em_kg_e_avisa():  # B.9-8
    resultado = avaliar("NASEM", "LAC_COW", {**LACTACAO, **LOTE}, [RACAO_CONCENTRADO])
    biblioteca = feed_library("NASEM")
    em_kg = sum(kg * biblioteca[i].starch / 100 for i, kg in RACAO_CONCENTRADO["amounts"].items())
    assert resultado["diets"][0]["intake"]["total_starch_kg"] == pytest.approx(em_kg)
    assert any("amido total entra em kg" in aviso for aviso in resultado["warnings"])


def test_nasem_sem_metano_e_nitrogenio_deixa_a_energia_indisponivel():
    resultado = avaliar("NASEM", "LAC_COW", LACTACAO, [RACAO_RUFAS])
    dieta = resultado["diets"][0]
    energia = next(c for c in dieta["constraints"] if c["id"] == "ne_nasem")
    assert energia["status"] == "indisponivel" and dieta["incomplete"] and "metano" in energia["note"]
    with pytest.raises(ValueError, match="os dois"):
        avaliar("NASEM", "LAC_COW", {**LACTACAO, "enteric_methane": 400}, [RACAO_RUFAS])


def test_exigencias_da_dieta_vem_da_propria_dieta_e_sobrescritas_valem():
    base = avaliar("NRC", "LAC_COW", LACTACAO, [RACAO_RUFAS])
    assert "phosphorus" in linhas(base, "RuFaS")
    sobrescrito = avaliar("NRC", "LAC_COW", LACTACAO, [RACAO_RUFAS], overrides={"calcium": 500})
    assert linhas(sobrescrito, "RuFaS")["calcium"]["requirement"] == 500
    assert linhas(sobrescrito, "RuFaS")["calcium"]["status"] == "violada"
    assert sobrescrito["diets"][0]["requirements"]["calcium"] == 500


def test_limites_por_alimento_valem_como_restricoes():
    resultado = avaliar("NRC", "LAC_COW", LACTACAO, [RACAO_RUFAS], limits={"50": [12.0, 20.0]})
    linhas_ = linhas(resultado, "RuFaS")
    assert linhas_["limit_ge_50"]["status"] == "violada" and "limit_ge_50" in resultado["diets"][0]["violated"]
    assert linhas_["limit_le_230"]["status"] == "no_limite"  # teto padrão de mineral: 0,6 kg


def test_entradas_invalidas_sao_recusadas_e_alimento_ausente_e_removido_com_aviso():
    with pytest.raises(ValueError, match="preço"):
        evaluate_diets("NRC", "LAC_COW", LACTACAO, [RACAO_RUFAS], {44: 0.3})
    with pytest.raises(ValueError, match="Informe ao menos uma dieta"):
        avaliar("NRC", "LAC_COW", LACTACAO, [])
    with pytest.raises(ValueError, match="No máximo"):
        avaliar("NRC", "LAC_COW", LACTACAO, [{"name": str(i), "amounts": {50: 1}} for i in range(MAX_DIETS + 1)])
    with pytest.raises(ValueError, match="repetido"):
        avaliar("NRC", "LAC_COW", LACTACAO, [RACAO_RUFAS, RACAO_RUFAS])
    with pytest.raises(ValueError, match="maior ou igual a zero"):
        avaliar("NRC", "LAC_COW", LACTACAO, [{"name": "x", "amounts": {50: -1}}])
    com_166 = {"name": "x", "amounts": {50: 10, 110: 10, 166: 1}}  # farelo de soja 44%: só no NRC
    nasem = avaliar("NASEM", "LAC_COW", {**LACTACAO, **LOTE}, [com_166])
    assert any("166" in aviso and "NASEM" in aviso for aviso in nasem["warnings"])
    assert not any(c["id"].endswith("_166") for c in nasem["diets"][0]["constraints"])
