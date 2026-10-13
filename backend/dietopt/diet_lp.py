"""Problema da dieta de custo mínimo (Pesquisa Operacional) resolvido por programação linear.

Modelo (o do quadro do professor, generalizado para N alimentos e M nutrientes):

    minimizar   sum_i  custo_i * x_i
    sujeito a   min_j <= sum_i q_ij * x_i <= max_j      para cada nutriente j
                0 <= x_i <= limite_i                     para cada alimento i

onde x_i é a quantidade (kg) do alimento i e q_ij a quantidade (kg) do nutriente j em 1 kg do alimento i.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import linprog


@dataclass(frozen=True)
class Food:
    name: str
    cost: float  # $/kg
    nutrients: dict[str, float]  # nutriente -> kg de nutriente por kg de alimento
    max_amount: float = float("inf")  # kg


@dataclass(frozen=True)
class NutrientBounds:
    minimum: float = 0.0
    maximum: float = float("inf")


@dataclass
class DietResult:
    feasible: bool
    status: str
    cost: float = float("nan")
    amounts: dict[str, float] = field(default_factory=dict)
    nutrient_totals: dict[str, float] = field(default_factory=dict)
    shadow_prices: dict[str, float] = field(default_factory=dict)  # variação do custo por kg extra do limite mínimo
    reduced_costs: dict[str, float] = field(default_factory=dict)


def solve_diet(foods: list[Food], bounds: dict[str, NutrientBounds]) -> DietResult:
    """Resolve o PL da dieta com HiGHS e devolve quantidades, custo e preços-sombra."""
    nutrients = list(bounds)
    cost = np.array([f.cost for f in foods], dtype=float)
    q = np.array([[f.nutrients.get(n, 0.0) for f in foods] for n in nutrients], dtype=float)

    a_ub, b_ub, ub_rows = [], [], []
    for j, name in enumerate(nutrients):
        b = bounds[name]
        if np.isfinite(b.maximum):
            a_ub.append(q[j])
            b_ub.append(b.maximum)
            ub_rows.append((name, "max"))
        if b.minimum > 0:
            a_ub.append(-q[j])
            b_ub.append(-b.minimum)
            ub_rows.append((name, "min"))

    result = linprog(
        cost,
        A_ub=np.array(a_ub) if a_ub else None,
        b_ub=np.array(b_ub) if b_ub else None,
        bounds=[(0.0, f.max_amount if np.isfinite(f.max_amount) else None) for f in foods],
        method="highs",
    )
    if not result.success:
        return DietResult(feasible=False, status=result.message)

    amounts = {f.name: float(x) for f, x in zip(foods, result.x)}
    totals = {n: float(q[j] @ result.x) for j, n in enumerate(nutrients)}
    shadow = {}
    for (name, kind), marginal in zip(ub_rows, result.ineqlin.marginals):
        # marginals é dCusto/dRHS; para a restrição de mínimo (-q x <= -min) o RHS é -min
        shadow[f"{name}_{kind}"] = float(-marginal) if kind == "min" else float(marginal)
    reduced = {f.name: float(r) for f, r in zip(foods, result.lower.marginals)}
    return DietResult(True, result.message, float(result.fun), amounts, totals, shadow, reduced)
