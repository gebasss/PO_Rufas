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


# Terceiro intervalo (dia 60) de uma simulação real no NASEM (100 vacas, 1 ano, os mesmos preços e limites): as exigências médias do
# lote, a ração do SLSQP e o metano e o nitrogênio urinário do lote que o RuFaS grava (total do lote / vacas, no dia anterior).
REQUIREMENTS_NASEM = {
    "NEmaint_requirement": 12.598828056762212, "NEa_requirement": 0.0, "NEg_requirement": 0.7055866257710725,
    "NEpreg_requirement": 3.387441226539528, "NEl_requirement": 31.05055912676956, "MP_requirement": 2751.246603732121,
    "Ca_requirement": 66.84056194717414, "P_req": 63.195963443468685, "P_req_process": 38.266452721439094,
    "DMIest_requirement": 24.605916453605744, "avg_BW": 634.9297300425717,
}  # fmt: skip
RATION_NASEM = {"23": 0.10519, "44": 0.0, "50": 11.636345, "110": 20.245724, "138": 0.000432, "167": 0.0, "230": 0.0, "dry_matter_intake_total": 31.987691}


def simulacao_nasem(com_lote=True):
    dias = 61
    return SimulationResult(
        days=list(range(dias)),
        interval_days=[60],
        ration_kg_per_cow=[dict(RATION_NASEM)],
        requirements=[dict(REQUIREMENTS_NASEM)],
        cows_in_pen=[90],
        pen_animals=[90.0] * dias if com_lote else [],
        pen_methane_g=[90 * 708.58] * dias if com_lote else [],
        pen_urine_n_kg=[90 * 0.254557] * dias if com_lote else [],
    )


def test_nasem_usa_o_metano_e_o_nitrogenio_do_lote_e_o_lp_fica_perto_do_slsqp():
    out = compare_with_simulation(simulacao_nasem(), FEEDS, PRICES, LIMITS, "NASEM")
    row = out["intervals"][0]
    assert out["standard"] == "NASEM"
    for variant in ("lp_free", "lp_same"):
        assert row[variant]["verified"], row[variant]["violated"]
        assert row[variant]["cost"] <= row["slsqp"]["cost"] * 1.002  # nunca bem acima do SLSQP (CONCLUSOES_PREVIAS, 5)
    assert row["lp_same"]["dmi"] == pytest.approx(RATION_NASEM["dry_matter_intake_total"], rel=1e-6)


def test_nasem_sem_o_metano_do_lote_e_recusado_com_instrucao():
    with pytest.raises(ValueError, match="metano"):
        compare_with_simulation(simulacao_nasem(com_lote=False), FEEDS, PRICES, LIMITS, "NASEM")


def test_media_do_lote_vem_do_total_dividido_pelos_animais_do_dia_anterior():
    sim = SimulationResult(pen_animals=[10.0, 20.0, 20.0], pen_methane_g=[7000.0, 14000.0, 15000.0], pen_urine_n_kg=[2.0, 5.0, 6.0])
    assert sim.pen_averages(2) == (700.0, 0.25)  # dia 2 usa o dia 1 (formulada antes da atualização do dia)
    assert sim.pen_averages(0) == (700.0, 0.2)  # no dia 0, o dia 0
    assert SimulationResult().pen_averages(5) is None


def test_padrao_desconhecido_e_recusado():
    with pytest.raises(ValueError, match="Padrão"):
        compare_with_simulation(simulacao(), FEEDS, PRICES, LIMITS, "XYZ")


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
    assert steps == [(0, 2), (1, 2), (2, 2)]


def test_faixa_de_consumo_fixa_vale_no_lp_e_no_problema_original():
    cow = {"body_weight": 632.0, "mature_body_weight": 700, "parity": 2, "days_in_milk": 150, "housing": "Barn", "distance": 0,
           "milk_production": 35.0, "milk_fat": 3.7, "milk_true_protein": 3.1, "milk_lactose": 4.85}  # fmt: skip
    required = compute_requirements("NRC", "LAC_COW", cow, None, "LAC_COW")
    problem = optimize.build_problem("NRC", "LAC_COW", "LAC_COW", cow, FEEDS, PRICES, LIMITS, required, (29.0, 29.0))
    best, _ = optimize.search(problem, "rapida")
    assert best is not None
    assert float(best.x.sum()) == pytest.approx(29.0, rel=1e-6)


def test_mesmo_consumo_acima_do_teto_do_rufas_nao_reprova_a_racao_do_lp():
    """No mesmo consumo o consumo é do SLSQP (que chegou a passar do teto de +30% do RuFaS); só as demais restrições valem."""
    from dietopt.module.pen_lp import _solve

    teto = REQUIREMENTS["DMIest_requirement"] * 1.3
    out = _solve(REQUIREMENTS, FEEDS, PRICES, LIMITS, (teto + 0.2, teto + 0.2), None)
    assert out is not None
    assert out["verified"] is True
    assert "dmi_max" not in out["violated"]
