"""Análise de sensibilidade: gera cenários S1..SN, roda o RuFaS e monta a tabela do quadro do professor.

Cada fator é o preço de um alimento (exige nova simulação) ou o preço do leite (só muda a receita, então é
recalculado sem rodar o RuFaS de novo). A tabela final tem uma linha por cenário com as colunas dos fatores
(``Arroz``, ``Milho``, ...) e o resultado (``Res`` = margem sobre o custo de alimentação).
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, replace
from typing import Any, Callable

import numpy as np
from scipy.stats import spearmanr

from .jobs import Cancelled
from .rufas_adapter import Scenario
from .scenarios import Economics, Evaluation, evaluate_many

MILK_PRICE = "milk_price"

# Limites do tamanho da análise: a grade cresce como n^k e cada simulação do RuFaS leva de 20 a 60 segundos e ~1,2 GB
# de memória. Sem teto, 8 fatores com 12 níveis seriam 430 milhões de cenários montados de uma vez na memória.
MIN_LEVELS = 2
MAX_LEVELS = 12  # níveis por fator na grade
MAX_SAMPLES = 100  # amostras do hipercubo latino
MAX_SIMULATIONS = 100  # simulações do RuFaS por análise (com o teto de níveis, também limita os cenários a 1.728)


def sensitivity_limits() -> dict[str, int]:
    """Limites do tamanho da análise, para a interface."""
    return {
        "min_levels": MIN_LEVELS,
        "max_levels": MAX_LEVELS,
        "max_samples": MAX_SAMPLES,
        "max_simulations": MAX_SIMULATIONS,
    }


def plan_size(n_feed_factors: int, n_factors: int, method: str, n: int) -> tuple[int, int]:
    """(cenários, simulações do RuFaS) de uma análise. O preço do leite só recalcula a receita, sem simulação nova."""
    if n_factors == 0:
        return 0, 0
    if method == "grid":
        return n**n_factors, n**n_feed_factors
    return n, (n if n_feed_factors else 1)


def check_plan(factors: list["Factor"], method: str, n: int) -> tuple[int, int]:
    """Valida o método, os níveis e o tamanho da análise; devolve (cenários, simulações) ou levanta ``ValueError``."""
    if method not in ("grid", "latin"):
        raise ValueError(f"Método desconhecido: {method}")
    if not factors:
        raise ValueError("Marque ao menos um fator.")
    if len({f.label for f in factors}) < len(factors) or len({f.key for f in factors}) < len(factors):
        raise ValueError("Há fatores repetidos: cada fator só pode entrar uma vez.")
    top = MAX_LEVELS if method == "grid" else MAX_SAMPLES
    if not MIN_LEVELS <= n <= top:
        raise ValueError(f"Use de {MIN_LEVELS} a {top} {'níveis' if method == 'grid' else 'amostras'} (recebido: {n}).")
    scenarios, simulations = plan_size(sum(not f.is_milk for f in factors), len(factors), method, n)
    if simulations > MAX_SIMULATIONS:
        raise ValueError(
            f"A análise exigiria {simulations} simulações do RuFaS; o limite é {MAX_SIMULATIONS}. Reduza os níveis ou os fatores."
        )
    return scenarios, simulations


@dataclass
class Factor:
    """Um fator da análise: ``key`` é o id do alimento (preço) ou ``"milk_price"``."""

    key: str
    label: str
    low: float
    high: float

    @property
    def is_milk(self) -> bool:
        return self.key == MILK_PRICE


def sample_points(factors: list[Factor], method: str, n: int, seed: int = 42) -> list[list[float]]:
    """Pontos no espaço dos fatores. ``grid``: n níveis por fator; ``latin``: n amostras por hipercubo latino."""
    if method == "grid":
        levels = [np.linspace(f.low, f.high, max(n, 2)) for f in factors]
        return [list(map(float, point)) for point in itertools.product(*levels)]
    if method == "latin":
        rng = np.random.default_rng(seed)
        unit = np.empty((n, len(factors)))
        for j in range(len(factors)):
            unit[:, j] = (rng.permutation(n) + rng.random(n)) / n
        lows = np.array([f.low for f in factors])
        highs = np.array([f.high for f in factors])
        return (lows + unit * (highs - lows)).tolist()
    raise ValueError(f"Método desconhecido: {method}")


def run_sensitivity(
    base: Scenario,
    factors: list[Factor],
    base_economics: Economics,
    method: str = "grid",
    n: int = 3,
    workers: int = 2,
    seed: int = 42,
    on_progress: Callable[[int, int], None] | None = None,
    should_cancel: Callable[[], bool] | None = None,
) -> dict[str, Any]:
    """Roda a análise e devolve ``{"columns", "rows", "effects"}``. Levanta ``Cancelled`` se ``should_cancel()`` for verdadeiro."""
    check_plan(factors, method, n)
    points = sample_points(factors, method, n, seed)

    # Cenários que exigem simulação: combinações únicas dos preços de alimentos.
    feed_factors = [f for f in factors if not f.is_milk]
    sim_index: dict[tuple[float, ...], int] = {}
    scenarios: list[Scenario] = []
    for point in points:
        feed_values = tuple(round(v, 4) for v, f in zip(point, factors) if not f.is_milk)
        if feed_values not in sim_index:
            prices = dict(base.feed_prices)
            for factor, value in zip(feed_factors, feed_values):
                prices[int(factor.key)] = value
            sim_index[feed_values] = len(scenarios)
            scenarios.append(replace(base, name=f"{base.name}_s{len(scenarios) + 1:03d}", feed_prices=prices))

    done = 0
    total = len(scenarios)
    evaluations: list[Evaluation] = []
    for start in range(0, total, workers):
        if should_cancel and should_cancel():
            raise Cancelled()
        batch = scenarios[start : start + workers]
        evaluations.extend(evaluate_many(batch, base_economics, workers=workers))
        done += len(batch)
        if on_progress:
            on_progress(done, total)

    rows: list[dict[str, Any]] = []
    for index, point in enumerate(points, start=1):
        feed_values = tuple(round(v, 4) for v, f in zip(point, factors) if not f.is_milk)
        evaluation = evaluations[sim_index[feed_values]]
        milk_price = base_economics.milk_price
        for value, factor in zip(point, factors):
            if factor.is_milk:
                milk_price = value
        row: dict[str, Any] = {"cenario": f"S{index}"}
        for value, factor in zip(point, factors):
            row[factor.label] = round(value, 4)
        if evaluation.ok:
            revenue = evaluation.milk_kg * milk_price
            row.update(
                {
                    "leite_kg": round(evaluation.milk_kg),
                    "receita": round(revenue, 2),
                    "custo_alimentacao": round(evaluation.feed_cost, 2),
                    "custo_vaca_dia": round(evaluation.lac_cost_per_cow_day, 3),
                    "reducao_leite": round(evaluation.reduction, 3),
                    "Res": round(revenue - evaluation.feed_cost, 2),
                    "ration": {k: round(v, 3) for k, v in evaluation.ration.items() if v > 1e-3},
                }
            )
        else:
            row.update({"Res": None, "erro": evaluation.detail})
        rows.append(row)

    return {
        "columns": [f.label for f in factors] + ["Res"],
        "rows": rows,
        "effects": rank_effects(factors, rows),
    }


def rank_effects(factors: list[Factor], rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Efeito de cada fator sobre o resultado (margem), de duas formas que se completam.

    - ``spearman``: correlação de postos, de -1 a +1. Diz a **direção** e a consistência (subir o fator sempre baixa a
      margem?), não o tamanho: um fator que muda a margem em 0,1% pode ter -1.
    - ``swing`` (US$) e ``swing_pct`` (% da margem média): quanto a margem muda quando o fator vai do mínimo ao máximo
      da faixa (declive da reta de mínimos quadrados vezes a amplitude do fator). Na grade, os níveis são balanceados e
      o declive isola o efeito de cada fator; no hipercubo latino é uma estimativa.
    """
    valid = [r for r in rows if r.get("Res") is not None]
    effects = []
    for factor in factors:
        xs = [r[factor.label] for r in valid]
        ys = [r["Res"] for r in valid]
        effect: dict[str, Any] = {"fator": factor.label, "spearman": None, "swing": None, "swing_pct": None}
        if len(valid) >= 2 and len(set(xs)) >= 2:
            slope = float(np.polyfit(xs, ys, 1)[0])
            swing = slope * (max(xs) - min(xs))
            mean = float(np.mean(ys))
            effect["swing"] = round(swing, 2)
            effect["swing_pct"] = round(100 * swing / abs(mean), 2) if mean else None
        if len(valid) >= 3 and len(set(xs)) >= 2 and len(set(ys)) >= 2:
            effect["spearman"] = round(float(spearmanr(xs, ys).statistic), 3)
        effects.append(effect)
    return effects
