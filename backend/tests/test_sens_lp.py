"""Ração linear (LP) × ração do RuFaS em cada cenário da sensibilidade (FSD, A.15)."""

import pytest

from dietopt.jobs import Cancelled
from dietopt.module import sens_lp
from dietopt.module.pen_lp import compare_sample, sample_indices
from dietopt.rufas_adapter import Scenario
from dietopt.scenarios import Economics, Evaluation
from dietopt.sensitivity import Factor, plan_scenarios
from test_pen_lp import FEEDS, LIMITS, PRICES, simulacao

ARROZ = Factor("138", "Arroz", 0.10, 0.30)
MILHO = Factor("44", "Milho", 0.20, 0.40)
LEITE = Factor("milk_price", "Leite", 0.40, 0.60)
BASE = Scenario(name="base", feed_prices={138: 0.2, 44: 0.3}, lac_cow_feeds=[138, 44, 50])
ECONOMICS = Economics(milk_price=0.5)


def test_amostra_de_intervalos_igualmente_espacados():
    assert sample_indices(13, 4) == [0, 4, 8, 12]
    assert sample_indices(13, 1) == [0]
    assert sample_indices(3, 10) == [0, 1, 2]
    assert sample_indices(25, 4) == [0, 8, 16, 24]


def test_plano_compartilha_a_simulacao_quando_so_o_leite_muda():
    points, scenarios, index = plan_scenarios(BASE, [ARROZ, LEITE], "grid", 3)
    assert len(points) == 9 and len(scenarios) == 3  # 3 preços de arroz × 3 de leite, 1 simulação por preço de arroz
    assert sorted(index.values()) == [0, 1, 2]
    assert [s.feed_prices[138] for s in scenarios] == pytest.approx([0.10, 0.20, 0.30])
    assert scenarios[0].name == "base_s001"


def test_comparacao_curta_usa_so_o_mesmo_consumo_e_a_amostra_pedida():
    out = compare_sample(simulacao(3), FEEDS, PRICES, LIMITS, sample=1)
    assert out["intervals_sampled"] == 1 and out["intervals_used"] == 1
    assert out["verified"] is True
    assert out["lp_cost"] <= out["slsqp_cost"] * 1.002
    assert out["diff_pct"] == pytest.approx((out["lp_cost"] / out["slsqp_cost"] - 1) * 100)


class AvaliacaoFalsa:
    """Substitui ``evaluate``: a simulação do arroz a 0,30 falha; as outras trazem o resultado de ``simulacao()``."""

    def __call__(self, scenario, economics):
        if scenario.feed_prices[138] > 0.29:
            return Evaluation(scenario.name, False, 0.0, detail="No previous ration available")
        return Evaluation(scenario.name, True, 0.0, result=simulacao(1))


def comparacao_falsa(deltas):
    """Substitui ``compare_sample``: devolve diferenças canônicas, uma por chamada."""
    it = iter(deltas)

    def fake(simulation, feeds, prices, limits, sample, should_stop):
        diff = next(it)
        return {"intervals_sampled": sample, "intervals_used": sample, "slsqp_cost": 4.0, "lp_cost": 4.0 * (1 + diff / 100), "diff_pct": diff, "verified": True}

    return fake


def test_comparacao_por_cenario_agrupa_cenarios_que_dividem_a_simulacao(monkeypatch):
    monkeypatch.setattr(sens_lp, "evaluate", AvaliacaoFalsa())
    monkeypatch.setattr(sens_lp, "compare_sample", comparacao_falsa([0.0, -0.5]))
    out = sens_lp.compare_sensitivity(BASE, [ARROZ, LEITE], ECONOMICS, "grid", 3)
    assert [r["cenarios"] for r in out["rows"]] == [["S1", "S2", "S3"], ["S4", "S5", "S6"], ["S7", "S8", "S9"]]
    assert out["rows"][0]["precos"] == {"Arroz": 0.1}
    assert out["rows"][2]["erro"] == "No previous ration available"  # a simulação que falhou fica registrada e fora das médias
    assert out["summary"]["compared"] == 2 and out["summary"]["failed"] == 1 and out["summary"]["scenarios"] == 3


def test_resumo_conta_empates_e_extremos(monkeypatch):
    monkeypatch.setattr(sens_lp, "evaluate", lambda scenario, economics: Evaluation(scenario.name, True, 0.0, result=simulacao(1)))
    monkeypatch.setattr(sens_lp, "compare_sample", comparacao_falsa([-0.5, 0.02, 0.3]))
    summary = sens_lp.compare_sensitivity(BASE, [ARROZ], ECONOMICS, "grid", 3)["summary"]
    assert (summary["lp_cheaper"], summary["tie"], summary["lp_dearer"]) == (1, 1, 1)
    assert summary["min_diff_pct"] == pytest.approx(-0.5) and summary["max_diff_pct"] == pytest.approx(0.3)
    assert summary["mean_diff_pct"] == pytest.approx((-0.5 + 0.02 + 0.3) / 3)
    assert summary["all_verified"] is True


def test_resumo_sem_nenhuma_comparacao():
    assert sens_lp._summary([{"erro": "falhou"}, {"erro": "falhou"}]) == {"scenarios": 2, "compared": 0, "failed": 2}


def test_progresso_e_cancelamento(monkeypatch):
    monkeypatch.setattr(sens_lp, "evaluate", lambda scenario, economics: Evaluation(scenario.name, True, 0.0, result=simulacao(1)))
    monkeypatch.setattr(sens_lp, "compare_sample", comparacao_falsa([0.0, 0.0, 0.0]))
    passos = []
    sens_lp.compare_sensitivity(BASE, [ARROZ], ECONOMICS, "grid", 3, on_progress=lambda done, total: passos.append((done, total)))
    assert passos == [(0, 3), (1, 3), (2, 3), (3, 3)]
    with pytest.raises(Cancelled):
        sens_lp.compare_sensitivity(BASE, [ARROZ], ECONOMICS, "grid", 3, should_cancel=lambda: True)


def test_nasem_e_recusado():
    with pytest.raises(ValueError, match="NRC"):
        sens_lp.compare_sensitivity(Scenario(name="x", nutrient_standard="NASEM"), [ARROZ], ECONOMICS, "grid", 3)
