"""Benchmark LP × SLSQP (``dietopt.benchmark``): desenho determinístico e estatística; sem rodar o RuFaS."""

import math

import numpy as np
import pytest

from dietopt import benchmark as bm


def test_casos_sao_fixos_e_cobrem_padrao_vaca_e_preco():
    a, b = bm.cases(), bm.cases()
    assert a == b  # determinístico
    assert len(a) == len(bm.STANDARDS) * len(bm.COWS) * (bm.PRICE_SETS + 1)
    assert len({c["id"] for c in a}) == len(a)
    assert all("enteric_methane" not in c["cow"] for c in a)  # metano e N urinário são calculados da dieta, nos dois padrões


def test_precos_sorteados_ficam_na_faixa_do_desenho_e_o_primeiro_conjunto_e_o_base():
    sets = bm.price_sets()
    assert sets[0] == bm.BASE_PRICES and len(sets) == bm.PRICE_SETS + 1
    low, high = bm.PRICE_FACTOR
    for prices in sets[1:]:
        for feed, price in prices.items():
            assert bm.BASE_PRICES[feed] * low * 0.999 <= price <= bm.BASE_PRICES[feed] * high * 1.001


def test_diferenca_relativa_tem_sinal_do_lp():
    assert bm.gap_pct(99.0, 100.0) == pytest.approx(-1.0)  # LP mais barato: negativa
    assert bm.gap_pct(101.0, 100.0) == pytest.approx(1.0)


def test_tost_reconhece_equivalencia_e_a_falta_dela():
    rng = np.random.default_rng(1)
    pequenas = rng.normal(0.0, 0.05, 40)  # média ~0, desvio 0,05%: dentro de ±0,5%
    grandes = rng.normal(1.0, 0.05, 40)  # média ~1%: fora da margem
    assert bm.tost(pequenas, 0.5)["equivalent"]
    assert not bm.tost(grandes, 0.5)["equivalent"]
    lo, hi = bm.bootstrap_ci(pequenas)
    assert -0.5 < lo < hi < 0.5


def test_tost_sem_variacao_nao_divide_por_zero():
    assert bm.tost([0.0, 0.0, 0.0], 0.5)["equivalent"]
    assert not bm.tost([1.0, 1.0, 1.0], 0.5)["equivalent"]


def test_bootstrap_e_reproduzivel():
    d = [0.01, -0.02, 0.0, 0.03, -0.01, 0.02]
    assert bm.bootstrap_ci(d) == bm.bootstrap_ci(d)


def test_wilcoxon_descarta_zeros_e_sem_nada_devolve_none():
    assert bm.wilcoxon_p([0.0, 0.0]) is None
    assert 0.0 <= bm.wilcoxon_p([0.1, -0.2, 0.3, 0.4, 0.5, -0.1]) <= 1.0


def test_describe_conta_ganhos_empates_e_perdas_com_o_empate_da_interface():
    d = bm.describe([-0.5, 0.05, -0.05, 0.3, 0.0, 0.2])
    assert (d["lp_cheaper"], d["tie"], d["lp_dearer"]) == (1, 3, 2)
    assert d["within_margin"] == 6 and d["n"] == 6
    assert bm.describe([])["n"] == 0


def _row(case_id, standard, cow, k, lp, others, lp_seconds=10.0):
    return {
        "id": case_id, "standard": standard, "cow_name": cow, "price_set": k, "status": "ok",
        "lp": {"cost": lp, "verified": True, "seconds": lp_seconds, "regime": "com_desconto"},
        "slsqp": [{"seed": s, "success": ok, "feasible": ok, "cost": c, "seconds": 0.2} for s, (c, ok) in enumerate(others)],
    }  # fmt: skip


def test_resumo_usa_so_execucoes_viaveis_e_conta_as_falhas():
    rows = [
        _row("a", "NRC", "alta", 0, 4.000, [(4.001, True), (4.002, True), (9.0, False)]),
        _row("b", "NRC", "alta", 1, 3.000, [(3.000, True), (3.100, True)]),
        {"id": "c", "standard": "NRC", "cow_name": "alta", "price_set": 2, "status": "infeasible"},
    ]
    g = bm.summarize(rows)["groups"]["NRC"]
    assert (g["cases"], g["ok"], g["infeasible"]) == (3, 2, 1)
    assert g["slsqp_runs"] == 5 and g["slsqp_failed"] == 1
    assert g["d_best"]["n"] == 2
    assert g["d_best"]["mean"] == pytest.approx((bm.gap_pct(4.000, 4.001) + 0.0) / 2)
    assert math.isclose(g["time_ratio"], 10.0 / 0.2)
    assert g["lp_verified"] == 2
