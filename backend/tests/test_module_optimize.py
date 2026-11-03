"""Dieta ótima (RF-30, fase 2): LP por escalares globais contra o SLSQP do RuFaS (LINEARIZACAO.md, 5.1b e 10)."""

import numpy as np
import pytest

from dietopt.module import optimize
from dietopt.module.evaluate import resolve_limits
from dietopt.module.optimize import Cancelled, optimize_diet
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
CONJUNTO_BASE = [50, 110, 44, 167, 138, 230, 23]  # LINEARIZACAO.md, 10.1


def problema(standard, category, animal, cow, ids=CONJUNTO_BASE):
    ids = sorted(ids)
    required = compute_requirements(standard, category, cow, None, animal)
    return optimize.build_problem(standard, category, animal, cow, ids, PRECOS, resolve_limits(standard, ids, None), required)


def test_desconto_de_ingestao_replica_o_do_rufas():
    rf = rufas()
    rng = np.random.default_rng(3)
    problem = problema("NRC", "LAC_COW", "LAC_COW", LACTACAO)
    for _ in range(25):
        x = rng.uniform(0.0, 12.0, len(problem.ids))
        point = optimize.scalars_of(problem, x)
        in_ration = [rf.feed_in_ration(float(a), fd) for a, fd in zip(x, problem.feeds)]
        esperado = rf.supply.calculate_nutrient_intake_discount(in_ration, problem.body_weight)
        assert optimize.intake_discount(point.tdn, point.dmi, problem.body_weight) == pytest.approx(esperado, abs=1e-12)


@pytest.mark.parametrize(
    "standard,category,animal,cow",
    [
        ("NRC", "LAC_COW", "LAC_COW", LACTACAO),
        ("NASEM", "LAC_COW", "LAC_COW", {**LACTACAO, **LOTE}),
        ("NRC", "CLOSE_UP", "DRY_COW", SECA),
        ("NASEM", "GROWING", "HEIFER_II", {**NOVILHA, **LOTE}),
    ],
)
def test_lp_nos_escalares_do_rufas_reproduz_o_custo_do_slsqp(standard, category, animal, cow):  # LINEARIZACAO.md, 10.3-1
    problem = problema(standard, category, animal, cow)
    run = optimize.run_rufas(problem, category, 1)[0]
    assert run["success"]
    solution = optimize.solve_point(problem, optimize.scalars_of(problem, run["x"]))
    assert solution is not None
    assert solution.cost == pytest.approx(run["cost"], rel=1e-6)


def test_ponto_fora_da_regiao_viavel_e_inviavel():
    problem = problema("NRC", "LAC_COW", "LAC_COW", LACTACAO)
    assert optimize.solve_point(problem, optimize.Point(dmi=33.0, tdn=40.0, conc=90.0)) is None


@pytest.mark.parametrize(
    "standard,category,animal,cow",
    [
        ("NRC", "LAC_COW", "LAC_COW", LACTACAO),
        ("NASEM", "LAC_COW", "LAC_COW", {**LACTACAO, **LOTE}),
        ("NRC", "CLOSE_UP", "DRY_COW", SECA),
        ("NASEM", "CLOSE_UP", "DRY_COW", {**SECA, **LOTE}),
        ("NRC", "GROWING", "HEIFER_II", NOVILHA),
        ("NASEM", "GROWING", "HEIFER_II", {**NOVILHA, **LOTE}),
    ],
)
def test_dieta_otima_e_viavel_nas_restricoes_originais_e_chega_perto_do_rufas(standard, category, animal, cow):
    result = optimize_diet(standard, category, cow, CONJUNTO_BASE, PRECOS, animal_type=animal, resolution="rapida", seeds=3)
    assert result["status"] == "ok"
    diet = result["diet"]
    assert diet["verified"], diet["evaluation"]["violated"]  # folgas das funções originais do RuFaS, nas exigências da otimização
    assert diet["cost"] == pytest.approx(sum(PRECOS[int(i)] * kg for i, kg in diet["amounts"].items()))
    assert sum(diet["amounts"].values()) == pytest.approx(diet["scalars"]["dmi"], rel=1e-6)
    rufas_ = result["rufas"]
    assert rufas_["n_runs"] == 3 and rufas_["n_success"] >= 1  # o SLSQP parte de um ponto aleatório e pode não convergir
    assert rufas_["lp_gap_pct"] < 0.5  # o LP, com a grade rápida, fica a menos de 0,5% do melhor do RuFaS (ou abaixo dele)


def test_caso_base_nrc_fica_a_0_1_por_cento_do_melhor_do_rufas():  # aceite da E7 (LINEARIZACAO.md, 10.2: 3,8373 contra 3,8342)
    result = optimize_diet("NRC", "LAC_COW", LACTACAO, CONJUNTO_BASE, PRECOS, resolution="normal", seeds=5)
    assert result["diet"]["verified"]
    assert result["diet"]["regime"] == "sem_desconto"  # o RuFaS explora a descontinuidade em TDN% = 60
    assert result["rufas"]["cost_min"] == pytest.approx(3.8342, abs=2e-4)
    assert result["rufas"]["lp_gap_pct"] < 0.1


def test_nasem_chega_ao_mesmo_custo_do_rufas():
    result = optimize_diet("NASEM", "LAC_COW", {**LACTACAO, **LOTE}, CONJUNTO_BASE, PRECOS, resolution="normal", seeds=3)
    assert abs(result["rufas"]["lp_gap_pct"]) < 0.01


def test_precos_sombra_tem_o_sinal_certo_e_preveem_a_variacao_do_custo():
    result = optimize_diet("NRC", "LAC_COW", LACTACAO, CONJUNTO_BASE, PRECOS, resolution="rapida", seeds=0)
    assert "rufas" not in result
    sombra = {s["id"]: s["value"] for s in result["shadow_prices"]}
    assert sombra["protein_min"] > 0  # exigir mais proteína custa mais
    assert all(v < 0 for k, v in sombra.items() if k.startswith("limit_le_") or k in ("ndf_max", "fat"))  # afrouxar um teto reduz o custo
    # Com os escalares fixos, o custo varia com a exigência na razão do preço-sombra (LP: valor ótimo é linear por partes).
    base = problema("NRC", "LAC_COW", "LAC_COW", LACTACAO)
    extra = 5.0
    required = compute_requirements("NRC", "LAC_COW", LACTACAO, {"metabolizable_protein": base.requirements.requirements["metabolizable_protein"] + extra}, "LAC_COW")
    maior = optimize.build_problem("NRC", "LAC_COW", "LAC_COW", LACTACAO, base.ids, PRECOS, resolve_limits("NRC", base.ids, None), required)
    ponto = optimize.Point(**{k: v for k, v in zip(("dmi", "tdn", "conc"), (result["diet"]["scalars"][c] for c in ("dmi", "tdn_percentage", "concentrate_percentage")))})
    antes, depois = optimize.solve_point(base, ponto), optimize.solve_point(maior, ponto)
    assert (depois.cost - antes.cost) / extra == pytest.approx(sombra["protein_min"], rel=0.05)


def test_alimentos_insuficientes_dao_status_inviavel_com_mensagem():
    result = optimize_diet("NRC", "LAC_COW", LACTACAO, [230], PRECOS, resolution="rapida", seeds=3)
    assert result["status"] == "infeasible" and "Nenhuma dieta" in result["message"]
    assert "diet" not in result and "rufas" not in result


def test_nasem_sem_metano_e_nitrogenio_e_recusado():
    with pytest.raises(ValueError, match="metano"):
        optimize_diet("NASEM", "LAC_COW", LACTACAO, CONJUNTO_BASE, PRECOS, resolution="rapida", seeds=0)


def test_cancelamento_interrompe_a_busca():
    with pytest.raises(Cancelled):
        optimize_diet("NRC", "LAC_COW", LACTACAO, CONJUNTO_BASE, PRECOS, resolution="rapida", seeds=0, should_stop=lambda: True)


def test_progresso_cresce_e_termina_no_total():
    passos = []
    optimize_diet("NRC", "CLOSE_UP", SECA, CONJUNTO_BASE, PRECOS, animal_type="DRY_COW", resolution="rapida", seeds=2, on_progress=lambda d, t: passos.append((d, t)))
    assert passos[-1][0] == passos[-1][1] and len({t for _, t in passos}) == 1
    assert all(0 <= d <= t for d, t in passos)


def test_limites_do_usuario_valem_e_a_dieta_os_respeita():
    limites = {110: [0.0, 5.0]}
    result = optimize_diet("NRC", "LAC_COW", LACTACAO, CONJUNTO_BASE, PRECOS, limits=limites, resolution="rapida", seeds=0)
    assert result["status"] == "ok" and result["diet"]["amounts"].get("110", result["diet"]["amounts"].get(110, 0)) <= 5.0 + 1e-9


@pytest.mark.parametrize(
    "kwargs,mensagem",
    [
        ({"resolution": "enorme"}, "Resolução"),
        ({"seeds": 31}, "sementes"),
        ({"seeds": -1}, "sementes"),
        ({"feed_ids": []}, "alimentos"),
        ({"feed_ids": [999999]}, "fora da biblioteca"),
        ({"prices": {}}, "preço"),
    ],
)
def test_entradas_invalidas_sao_recusadas(kwargs, mensagem):
    corpo = dict(standard="NRC", category="LAC_COW", cow=LACTACAO, feed_ids=CONJUNTO_BASE, prices=PRECOS, resolution="rapida", seeds=0)
    with pytest.raises(ValueError, match=mensagem):
        optimize_diet(**{**corpo, **kwargs})


def test_tolerancia_do_slsqp_aceita_violacao_minima_e_recusa_a_grande():
    def avaliacao(slack):
        return {"constraints": [{"slack": slack, "requirement": 45.0}, {"requirement": 1.0}]}  # a segunda é indisponível (sem folga)

    assert optimize._within(avaliacao(-2.8e-7), optimize.RUFAS_TOLERANCE)  # o SLSQP deixa passar violações dessa ordem
    assert not optimize._within(avaliacao(-0.5), optimize.RUFAS_TOLERANCE)
    assert not optimize._within(None, optimize.RUFAS_TOLERANCE)


def test_payload_da_rota_mapeia_o_corpo_e_usa_cinco_sementes_por_padrao():
    from dietopt.module.api import optimize_payload

    corpo = {"standard": "NRC", "category": "CLOSE_UP", "animal_type": "DRY_COW", "cow": SECA, "feed_ids": CONJUNTO_BASE, "prices": PRECOS, "resolution": "rapida"}
    resposta = optimize_payload(corpo, should_stop=None)
    assert resposta["status"] == "ok" and resposta["rufas"]["n_runs"] == 5
    assert optimize_payload({**corpo, "seeds": 0})["status"] == "ok"
