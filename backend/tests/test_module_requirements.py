"""Exigências da vaca pelas calculadoras do RuFaS (rodam isoladas, sem simulação) e a validação dos campos.

Os valores de referência foram obtidos com as próprias calculadoras do RuFaS v1.0.6 em 01/11/2026 (sondagem do FSD, B.3).
"""

import pytest

from dietopt.module.api import defaults_payload, requirements_payload
from dietopt.module.categories import constraints_for
from dietopt.module.fields import fields_for
from dietopt.module.requirements import compute_requirements
from dietopt.module.rufas import rufas as _rufas

LACTACAO = dict(
    body_weight=650, mature_body_weight=700, parity=2, days_in_milk=100, calving_interval=400,
    milk_production=40, milk_fat=3.7, milk_true_protein=3.1, milk_lactose=4.85,
    housing="Barn", distance=100, day_of_pregnancy=60, body_condition_score_5=3.0,
)  # fmt: skip
SECA = dict(
    body_weight=740, mature_body_weight=740, parity=2, day_of_pregnancy=250, calving_interval=400,
    housing="Barn", distance=100,
)  # fmt: skip
NOVILHA_II = dict(
    body_weight=450, mature_body_weight=700, day_of_pregnancy=100, parity=0, average_daily_gain_heifer=0.8,
    body_condition_score_5=3.0, days_born=500, housing="Barn", distance=100,
)  # fmt: skip


def values(result, *names):
    return {name: result.requirements[name] for name in names}


def close(expected):
    """Comparação com tolerância de 0,01 (as referências foram anotadas com 2 a 3 casas)."""
    return pytest.approx(expected, abs=0.01)


def test_vaca_em_lactacao_nrc_reproduz_a_calculadora_do_rufas():
    r = compute_requirements("NRC", "LAC_COW", LACTACAO)
    assert values(r, "maintenance_energy", "lactation_energy", "metabolizable_protein", "calcium", "phosphorus", "dry_matter") == close({
        "maintenance_energy": 10.299, "lactation_energy": 28.706, "metabolizable_protein": 2681.266,
        "calcium": 70.869, "phosphorus": 63.95, "dry_matter": 25.823,
    })  # fmt: skip
    assert not r.overridden and r.requirements == r.calculated


def test_vaca_em_lactacao_nasem_com_fdn_da_racao_anterior():
    r = compute_requirements("NASEM", "LAC_COW", {**LACTACAO, "ndf_percentage": 33})
    assert values(r, "maintenance_energy", "metabolizable_protein", "calcium", "phosphorus", "dry_matter") == close({
        "maintenance_energy": 12.862, "metabolizable_protein": 2334.29, "calcium": 63.845, "phosphorus": 61.64, "dry_matter": 24.735,
    })  # fmt: skip


def test_fdn_da_racao_anterior_vai_a_calculadora_como_fracao_como_faz_o_rufas():
    padrao = compute_requirements("NASEM", "CLOSE_UP", SECA)
    informada = compute_requirements("NASEM", "CLOSE_UP", {**SECA, "ndf_percentage": 45})
    assert padrao.inputs["ndf_percentage"] == pytest.approx(30)  # padrão do RuFaS (0,3), exibido em % da MS
    assert any("fração" in aviso for aviso in padrao.warnings)
    # O módulo envia 0,45 e não 45: com 45 a calculadora daria outro consumo estimado (a equação espera porcentagem).
    direto = _rufas().calculators["NASEM"].calculate_requirements(
        body_weight=740.0, mature_body_weight=740.0, day_of_pregnancy=250, body_condition_score_5=3.0, days_in_milk=None,
        average_daily_gain_heifer=None, animal_type=_rufas().animal_type.DRY_COW, parity=2, calving_interval=400,
        milk_fat=3.7, milk_true_protein=3.1, milk_lactose=4.85, milk_production=0.0, housing="Barn", distance=100.0,
        lactating=False, ndf_percentage=0.45, process_based_phosphorus_requirement=0.0,
    )  # fmt: skip
    assert informada.requirements["dry_matter"] == pytest.approx(direto.dry_matter)
    assert informada.requirements["dry_matter"] != pytest.approx(padrao.requirements["dry_matter"], abs=1e-6)


def test_vaca_seca_nrc_e_nasem():
    nrc = compute_requirements("NRC", "CLOSE_UP", SECA)
    assert nrc.animal_type == "DRY_COW"
    assert values(nrc, "maintenance_energy", "pregnancy_energy", "dry_matter") == close({
        "maintenance_energy": 10.656, "pregnancy_energy": 3.584, "dry_matter": 14.532,
    })  # fmt: skip
    nasem = compute_requirements("NASEM", "CLOSE_UP", {**SECA, "ndf_percentage": 33})
    assert values(nasem, "maintenance_energy", "pregnancy_energy", "phosphorus") == close({
        "maintenance_energy": 13.32, "pregnancy_energy": 3.713, "phosphorus": 19.369,
    })  # fmt: skip


def test_novilha_usa_ganho_diario_em_kg_e_nrc_pede_idade():
    nrc = compute_requirements(
        "NRC", "GROWING", {**NOVILHA_II, "tdn_percentage": 70, "net_energy_diet_concentration": 1.6, "previous_temperature": 20}
    )
    assert nrc.requirements["growth_energy"] == pytest.approx(3.18, abs=0.01)
    assert nrc.requirements["metabolizable_protein"] == pytest.approx(577, abs=1)
    nasem = compute_requirements("NASEM", "GROWING", {**NOVILHA_II, "ndf_percentage": 33})
    assert nasem.requirements["growth_energy"] == pytest.approx(4.15, abs=0.01)
    assert nasem.requirements["metabolizable_protein"] == pytest.approx(337.8, abs=0.1)


def test_ganho_diario_em_gramas_e_recusado():
    with pytest.raises(ValueError, match="Ganho médio diário"):
        compute_requirements("NASEM", "GROWING", {**NOVILHA_II, "average_daily_gain_heifer": 800})


def test_campo_obrigatorio_ausente_e_recusado_com_o_nome_do_campo():
    sem_peso = {k: v for k, v in LACTACAO.items() if k != "body_weight"}
    with pytest.raises(ValueError, match="Peso corporal é obrigatório"):
        compute_requirements("NRC", "LAC_COW", sem_peso)
    sem_idade = {k: v for k, v in NOVILHA_II.items() if k != "days_born"}
    with pytest.raises(ValueError, match="Idade é obrigatório"):  # o NRC usa a idade da novilha; o NASEM não
        compute_requirements("NRC", "GROWING", sem_idade)
    compute_requirements("NASEM", "GROWING", sem_idade)


def test_valores_invalidos_sao_recusados():
    for campo, valor in (("body_weight", 5000), ("parity", 1.5), ("housing", "Pasto"), ("milk_fat", "abc"), ("distance", True)):
        with pytest.raises(ValueError):
            compute_requirements("NRC", "LAC_COW", {**LACTACAO, campo: valor})
    with pytest.raises(ValueError, match="Campos desconhecidos"):
        compute_requirements("NRC", "LAC_COW", {**LACTACAO, "altura": 1})


def test_intervalo_entre_partos_vazio_nao_quebra_e_avisa_so_para_paridade_1_e_2():
    sem_intervalo = {k: v for k, v in LACTACAO.items() if k != "calving_interval"}
    r = compute_requirements("NRC", "LAC_COW", sem_intervalo)
    assert any("Intervalo entre partos" in aviso for aviso in r.warnings)
    assert r.requirements["growth_energy"] < compute_requirements("NRC", "LAC_COW", LACTACAO).requirements["growth_energy"]
    terceira = compute_requirements("NRC", "LAC_COW", {**sem_intervalo, "parity": 3})
    assert not any("Intervalo entre partos" in aviso for aviso in terceira.warnings)


def test_campo_ignorado_pelo_padrao_gera_aviso():
    r = compute_requirements("NRC", "LAC_COW", LACTACAO)
    assert any("Escore de condição corporal" in aviso and "ignora" in aviso for aviso in r.warnings)


def test_sobrescrita_substitui_so_a_exigencia_informada():
    r = compute_requirements("NRC", "LAC_COW", LACTACAO, {"calcium": 80})
    assert r.requirements["calcium"] == 80 and r.calculated["calcium"] == pytest.approx(70.869, abs=1e-3)
    assert r.requirements["phosphorus"] == r.calculated["phosphorus"] and r.overridden == ["calcium"]
    with pytest.raises(ValueError, match="desconhecidas"):
        compute_requirements("NRC", "LAC_COW", LACTACAO, {"sodio": 1})
    with pytest.raises(ValueError, match="maior ou igual a zero"):
        compute_requirements("NRC", "LAC_COW", LACTACAO, {"calcium": -1})


def test_tipo_de_animal_precisa_pertencer_a_categoria():
    assert compute_requirements("NASEM", "CLOSE_UP", {**NOVILHA_II, "days_in_milk": None}, animal_type="HEIFER_III").animal_type == "HEIFER_III"
    with pytest.raises(ValueError, match="não pertence"):
        compute_requirements("NASEM", "LAC_COW", LACTACAO, animal_type="DRY_COW")
    with pytest.raises(ValueError, match="Categoria desconhecida"):
        compute_requirements("NASEM", "CALF", LACTACAO)


def test_campos_por_padrao_e_tipo_de_animal():
    def required(standard, animal):
        return {f["key"] for f in fields_for(standard, animal) if f["required"]}

    assert "body_condition_score_5" in required("NASEM", "LAC_COW")
    assert "body_condition_score_5" not in {f["key"] for f in fields_for("NRC", "LAC_COW")}
    assert {"days_born", "body_condition_score_5", "average_daily_gain_heifer"} <= required("NRC", "HEIFER_II")
    assert "days_born" not in {f["key"] for f in fields_for("NASEM", "HEIFER_II")}
    assert "day_of_pregnancy" in required("NRC", "DRY_COW") and "milk_production" not in required("NRC", "DRY_COW")


def test_restricoes_por_padrao_e_categoria():
    def ids(standard, animal):
        return {c.id for c in constraints_for(standard, animal)}

    assert {"ne_total", "ne_lactation"} <= ids("NRC", "LAC_COW")
    assert not {"ne_total", "ne_lactation"} & ids("NRC", "DRY_COW")  # FSD B.9, critério 5
    assert not {"ne_total", "ne_lactation"} & ids("NRC", "HEIFER_II")
    assert ids("NASEM", "LAC_COW") == ids("NASEM", "HEIFER_II") and "ne_nasem" in ids("NASEM", "LAC_COW")
    assert "ne_maintenance" not in ids("NASEM", "LAC_COW")


def test_corpos_das_rotas_do_modulo():
    defaults = defaults_payload(None, "CLOSE_UP")
    assert defaults["standard"] == "NASEM" and defaults["animal_type"] == "DRY_COW"
    assert defaults["animal_types"] == ["DRY_COW", "HEIFER_III"]
    assert defaults["diet_defaults"]["tdn_percentage"] == pytest.approx(70)
    assert {c["id"] for c in defaults["constraints"]} >= {"calcium", "protein_min", "ne_nasem"}
    assert next(f for f in defaults["fields"] if f["key"] == "day_of_pregnancy")["required"]

    body = requirements_payload({"category": "LAC_COW", "cow": LACTACAO, "requirements_override": {"calcium": 80}})
    assert body["standard"] == "NASEM" and body["requirements"]["calcium"] == 80 and body["overridden"] == ["calcium"]
