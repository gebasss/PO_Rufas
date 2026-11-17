"""Ração linear (LP) × ração do RuFaS (SLSQP) nas exigências de uma simulação (FSD, A.14)."""

import pytest

from dietopt.module import optimize
from dietopt.module.pen_lp import _interval_lengths, _summary, compare_with_simulation
from dietopt.module.requirements import compute_requirements
from dietopt.rufas_results import SimulationResult

FEEDS = [23, 44, 50, 110, 138, 167, 230]
PRICES = {23: 1.1, 44: 0.28, 50: 0.09, 110: 0.12, 138: 0.25, 167: 0.55, 230: 0.1}
LIMITS = {23: (0.0, 1.0), 44: (0.0, 100.0), 50: (0.0, 100.0), 110: (0.0, 100.0), 138: (0.0, 100.0), 167: (0.0, 100.0), 230: (0.0, 0.6)}

# Terceiro intervalo (dia 60) de uma simulação real (100 vacas, 1 ano, NRC, os preços e limites acima): exigências médias do lote e
# a ração que o SLSQP do RuFaS formulou para elas.
REQUIREMENTS = {
    "NEmaint_requirement": 10.097618820481992, "NEa_requirement": 0.01714395984485719, "NEg_requirement": 0.48978241919616117,
    "NEpreg_requirement": 0.0904672370114314, "NEl_requirement": 31.05055912676956, "MP_requirement": 2841.412000260867,
    "Ca_requirement": 71.94192741646144, "P_req": 65.04411543765406, "P_req_process": 38.896833125946955,
    "DMIest_requirement": 25.78039393163593, "avg_BW": 634.9297300425717,
}  # fmt: skip
RATION = {"23": 0.007112, "44": 0.129866, "50": 11.907126, "110": 18.621613, "138": 0.0, "167": 1.21891, "230": 0.6, "dry_matter_intake_total": 32.484627}


def simulacao(intervalos=1):
    return SimulationResult(
        days=list(range(60)),
        interval_days=[30 * i for i in range(intervalos)],
        ration_kg_per_cow=[dict(RATION) for _ in range(intervalos)],
        requirements=[dict(REQUIREMENTS) for _ in range(intervalos)],
        cows_in_pen=[80] * intervalos,
    )


def test_o_lp_nao_fica_mais_caro_que_o_slsqp_e_respeita_as_restricoes_originais_do_rufas():
    """Neste intervalo o SLSQP parou 0,7% acima do que o LP acha; em geral os dois empatam. O LP nunca fica mais caro que 0,2%."""
    out = compare_with_simulation(simulacao(), FEEDS, PRICES, LIMITS)
    row = out["intervals"][0]
    slsqp_cost = sum(v * PRICES[int(k)] for k, v in RATION.items() if k != "dry_matter_intake_total")
    assert row["slsqp"]["cost"] == pytest.approx(slsqp_cost)
    for variant in ("lp_free", "lp_same"):
        assert row[variant]["verified"], row[variant]["violated"]
        assert row[variant]["cost"] <= row["slsqp"]["cost"] * 1.002
        assert sum(row[variant]["amounts"].values()) == pytest.approx(row[variant]["dmi"])
    assert out["warnings"] == []


def test_a_variante_de_mesmo_consumo_usa_o_consumo_do_slsqp():
    row = compare_with_simulation(simulacao(), FEEDS, PRICES, LIMITS)["intervals"][0]
    assert row["lp_same"]["dmi"] == pytest.approx(RATION["dry_matter_intake_total"], rel=1e-6)
    assert row["lp_free"]["dmi"] >= row["lp_same"]["dmi"] - 1e-6  # o consumo livre pode usar a folga de +30% que o RuFaS permite


def test_economia_do_rebanho_pesa_pelas_vacas_e_pelos_dias():
    intervals = [
        {"day": 0, "days": 30, "cows": 80, "slsqp": {"cost": 4.0, "dmi": 28.0, "amounts": {"50": 20.0}},
         "lp_free": {"cost": 3.5, "dmi": 33.0, "amounts": {"50": 30.0}, "verified": True},
         "lp_same": {"cost": 3.8, "dmi": 28.0, "amounts": {"50": 25.0}, "verified": True}},
        {"day": 30, "days": 10, "cows": 60, "slsqp": {"cost": 5.0, "dmi": 28.0, "amounts": {"50": 20.0}},
         "lp_free": {"cost": 4.0, "dmi": 33.0, "amounts": {"50": 30.0}, "verified": True},
         "lp_same": {"cost": 4.5, "dmi": 28.0, "amounts": {"50": 25.0}, "verified": False}},
    ]  # fmt: skip
    summary = _summary(intervals, [50])
    assert summary["days"] == 40
    assert summary["slsqp_cost_per_cow_day"] == pytest.approx((4.0 * 30 + 5.0 * 10) / 40)
    assert summary["lp_free"]["herd_saving"] == pytest.approx(0.5 * 80 * 30 + 1.0 * 60 * 10)
    assert summary["lp_same"]["herd_saving"] == pytest.approx(0.2 * 80 * 30 + 0.5 * 60 * 10)
    assert summary["lp_free"]["saving_pct"] == pytest.approx((4.25 - 3.625) / 4.25 * 100)
    assert summary["lp_free"]["all_verified"] is True
    assert summary["lp_same"]["all_verified"] is False
    assert summary["lp_free"]["mean_amounts"]["50"] == pytest.approx(30.0)


def test_intervalos_sem_lp_viavel_ficam_fora_da_media():
    intervals = [
        {"day": 0, "days": 30, "cows": 80, "slsqp": {"cost": 4.0, "dmi": 28.0, "amounts": {}}, "lp_free": None, "lp_same": None},
    ]
    assert _summary(intervals, [50]) == {"intervals_used": 0}


def test_duracao_dos_intervalos_vai_ate_o_fim_da_simulacao():
    assert _interval_lengths([0, 30, 60], 75) == [30, 30, 15]


def test_nasem_e_recusado():
    with pytest.raises(ValueError, match="NRC"):
        compare_with_simulation(simulacao(), FEEDS, PRICES, LIMITS, "NASEM")


def test_alimento_sem_preco_e_recusado():
    with pytest.raises(ValueError, match="preço"):
        compare_with_simulation(simulacao(), FEEDS, {k: v for k, v in PRICES.items() if k != 44}, LIMITS)


def test_simulacao_sem_exigencias_e_recusada():
    with pytest.raises(ValueError, match="exigências"):
        compare_with_simulation(SimulationResult(), FEEDS, PRICES, LIMITS)


def test_cancelamento_interrompe_a_comparacao():
    with pytest.raises(optimize.Cancelled):
        compare_with_simulation(simulacao(), FEEDS, PRICES, LIMITS, should_stop=lambda: True)


def test_progresso_conta_duas_resolucoes_por_intervalo():
    steps = []
    compare_with_simulation(simulacao(), FEEDS, PRICES, LIMITS, on_progress=lambda done, total: steps.append((done, total)))
    assert steps == [(1, 2), (2, 2)]


def test_faixa_de_consumo_fixa_vale_no_lp_e_no_problema_original():
    cow = {"body_weight": 632.0, "mature_body_weight": 700, "parity": 2, "days_in_milk": 150, "housing": "Barn", "distance": 0,
           "milk_production": 35.0, "milk_fat": 3.7, "milk_true_protein": 3.1, "milk_lactose": 4.85}  # fmt: skip
    required = compute_requirements("NRC", "LAC_COW", cow, None, "LAC_COW")
    problem = optimize.build_problem("NRC", "LAC_COW", "LAC_COW", cow, FEEDS, PRICES, LIMITS, required, (29.0, 29.0))
    best, _ = optimize.search(problem, "rapida")
    assert best is not None
    assert float(best.x.sum()) == pytest.approx(29.0, rel=1e-6)
