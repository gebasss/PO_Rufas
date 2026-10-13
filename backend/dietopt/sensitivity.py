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

from .rufas_adapter import Scenario
from .scenarios import Economics, Evaluation, evaluate_many

MILK_PRICE = "milk_price"


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
) -> dict[str, Any]:
    """Roda a análise e devolve ``{"columns", "rows", "effects"}``."""
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
    """Correlação de Spearman entre cada fator e o resultado (margem). Indica a direção e a força do efeito."""
    valid = [r for r in rows if r.get("Res") is not None]
    effects = []
    for factor in factors:
        xs = [r[factor.label] for r in valid]
        ys = [r["Res"] for r in valid]
        if len(valid) < 3 or len(set(xs)) < 2 or len(set(ys)) < 2:
            effects.append({"fator": factor.label, "spearman": None})
            continue
        rho = spearmanr(xs, ys).statistic
        effects.append({"fator": factor.label, "spearman": round(float(rho), 3)})
    return effects
