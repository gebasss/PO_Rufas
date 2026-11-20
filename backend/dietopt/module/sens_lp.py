"""Ração linear (LP) × ração do RuFaS (SLSQP) em cada cenário de uma análise de sensibilidade (FSD, A.15).

Para cada simulação da análise (cada combinação de preços de alimentos), o LP é resolvido sobre as exigências que o RuFaS usou em
alguns intervalos da simulação (``pen_lp.compare_sample``: só o mesmo consumo, intervalos igualmente espaçados) e comparado com a
ração do SLSQP. As simulações vêm do cache (se faltar alguma, é simulada). Mostra se o empate medido na Vaca leiteira se mantém
quando os preços mudam.
"""

from __future__ import annotations

from typing import Any, Callable

from ..jobs import Cancelled
from ..rufas_adapter import Scenario
from ..scenarios import Economics, evaluate
from ..sensitivity import Factor, plan_scenarios
from .pen_lp import compare_sample

SAMPLE = 4  # intervalos por cenário
TIE_PCT = 0.1  # diferença (em %) abaixo da qual os dois custos contam como iguais


def compare_sensitivity(
    base: Scenario,
    factors: list[Factor],
    economics: Economics,
    method: str = "grid",
    n: int = 3,
    seed: int = 42,
    sample: int = SAMPLE,
    on_progress: Callable[[int, int], None] | None = None,
    should_cancel: Callable[[], bool] | None = None,
) -> dict[str, Any]:
    """Compara a ração do LP com a do SLSQP em cada simulação da análise; a lista de cenários é a mesma da sensibilidade."""
    standard = base.nutrient_standard
    points, scenarios, sim_index = plan_scenarios(base, factors, method, n, seed)
    feed_factors = [f for f in factors if not f.is_milk]
    labels_by_scenario: dict[int, list[str]] = {}
    for number, point in enumerate(points, start=1):
        key = tuple(round(v, 4) for v, f in zip(point, factors) if not f.is_milk)
        labels_by_scenario.setdefault(sim_index[key], []).append(f"S{number}")

    rows: list[dict[str, Any]] = []
    total = len(scenarios)
    if on_progress:
        on_progress(0, total)  # a barra já mostra o total antes da primeira simulação (sem "Na fila…")
    for index, scenario in enumerate(scenarios):
        if should_cancel and should_cancel():
            raise Cancelled()
        evaluation = evaluate(scenario, economics)
        row: dict[str, Any] = {
            "cenarios": labels_by_scenario[index],
            "precos": {f.label: round(scenario.feed_prices[int(f.key)], 4) for f in feed_factors},
        }
        if not evaluation.ok or evaluation.result is None:
            row["erro"] = evaluation.detail or "a simulação do RuFaS falhou"
        else:
            row |= compare_sample(
                evaluation.result, scenario.lac_cow_feeds or [], scenario.feed_prices, scenario.feed_limits, sample, should_cancel, standard
            )
        rows.append(row)
        if on_progress:
            on_progress(index + 1, total)
    return {"standard": standard, "sample": sample, "rows": rows, "summary": _summary(rows)}


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    done = [r for r in rows if r.get("intervals_used")]
    diffs = [r["diff_pct"] for r in done]
    if not diffs:
        return {"scenarios": len(rows), "compared": 0, "failed": sum("erro" in r for r in rows)}
    return {
        "scenarios": len(rows),
        "compared": len(done),
        "failed": sum("erro" in r for r in rows),
        "mean_diff_pct": sum(diffs) / len(diffs),
        "min_diff_pct": min(diffs),
        "max_diff_pct": max(diffs),
        "lp_cheaper": sum(d < -TIE_PCT for d in diffs),
        "tie": sum(abs(d) <= TIE_PCT for d in diffs),
        "lp_dearer": sum(d > TIE_PCT for d in diffs),
        "all_verified": all(r["verified"] for r in done),
        "tie_pct": TIE_PCT,
    }
