"""Dieta ótima de custo mínimo para uma vaca (RF-30, fase 2; LINEARIZACAO.md, 5.1b) e comparação com o SLSQP do RuFaS.

O problema do RuFaS é não linear só por causa de poucos escalares globais da dieta: o consumo (DMI), o TDN%, o % de
concentrado e, no NASEM, o amido total em kg. Fixados esses escalares como **parâmetros**, o problema vira um LP **exato**
(``linear.build_at``), com as igualdades lineares ``Σx = DMI``, ``Σ TDN_i·x_i = TDN%·DMI`` e ``Σ_conc x_i = (%conc/100)·DMI``.
A busca roda o LP numa grade desses escalares (dois regimes em TDN% = 60, onde o desconto de ingestão é descontínuo),
refina em torno do melhor ponto e verifica a solução com as funções originais do RuFaS.

As exigências são as da própria vaca (sem ração anterior), como o RuFaS faz na primeira formulação, e valem para todos os
pontos. As disjunções (energia total do NRC e teto de proteína) viram um LP por ramo.
"""

from __future__ import annotations

import itertools
import random
import time
from dataclasses import dataclass, field
from statistics import median
from typing import Any, Callable, Mapping, Sequence

import numpy as np
from scipy.optimize import linprog

from ..feeds import feed_library
from ..jobs import Cancelled
from ..standards import get_standard
from . import linear
from .categories import parse_animal_type, parse_category
from .evaluate import Diet, evaluate_diet, pen_inputs, resolve_limits
from .library import build_feeds
from .requirements import RequirementsResult, compute_requirements
from .rufas import rufas

REGIME_BREAK = 60.0  # TDN% em que o desconto de ingestão do NRC liga (descontínuo; LINEARIZACAO.md, 4.4)
BREAK_EPSILON = 1e-6  # o regime sem desconto vai até 60 − ε (o RuFaS usa ``TDN% < 60``)
TOLERANCE = 1e-9
RUFAS_TOLERANCE = 1e-5  # violação relativa que o SLSQP do RuFaS deixa passar (``ftol`` de 1e-6 e restrições de igualdade aproximadas)
MAX_SEEDS = 30
RESCUE_POINTS = 40  # pontos da grade de onde parte o resgate
MIN_GRID_HITS = 6  # abaixo disso a grade acertou pouco da região viável e o resgate entra
STARTS_PER_REGIME = 3  # melhores pontos da grade de cada regime que o refinamento parte
# Resolução da grade inicial: pontos por escalar (consumo, TDN% por regime, % de concentrado, amido) e orçamento de LPs do refinamento.
RESOLUTIONS: Mapping[str, tuple[int, int, int, int, int]] = {
    "rapida": (3, 4, 3, 2, 400),
    "normal": (5, 6, 5, 3, 1500),
    "fina": (7, 9, 7, 4, 3000),
}


# ----------------------------------------------------------------------------------------------------------------
# Escalares globais e LP por ponto
# ----------------------------------------------------------------------------------------------------------------
def intake_discount(tdn_percentage: float, dmi: float, body_weight: float) -> float:
    """Desconto de ingestão do NRC (``D``) dos escalares da dieta, como em ``calculate_nutrient_intake_discount`` do RuFaS."""
    total_tdn = tdn_percentage * dmi / 100
    if tdn_percentage < REGIME_BREAK or total_tdn < 0.035 * body_weight**0.75:
        return 1.0
    maintenance_intake = total_tdn / (0.035 * (body_weight * 0.96) ** 0.75)
    discount = (tdn_percentage - (0.18 * tdn_percentage - 10.3) * (maintenance_intake - 1)) / tdn_percentage
    return max(discount, rufas().constants.MINIMUM_TDN_DISCOUNT)


@dataclass(frozen=True)
class Point:
    """Escalares globais da dieta que ficam fixos num LP. ``starch`` (kg) só conta no NASEM."""

    dmi: float
    tdn: float
    conc: float
    starch: float = 0.0

    @property
    def regime(self) -> str:
        return "sem_desconto" if self.tdn < REGIME_BREAK else "com_desconto"


@dataclass(frozen=True)
class Row:
    """Restrição ``a·x ≥ rhs`` (``ge``) ou ``a·x ≤ rhs`` (``le``)."""

    id: str
    a: np.ndarray
    sense: str
    rhs: float

    def holds(self, x: np.ndarray) -> bool:
        value, margin = float(self.a @ x), 1e-6 * max(1.0, abs(self.rhs))
        return value >= self.rhs - margin if self.sense == "ge" else value <= self.rhs + margin


@dataclass(frozen=True)
class Solution:
    point: Point
    x: np.ndarray
    cost: float
    energy_branch: str | None
    shadow_prices: dict[str, float]  # id da restrição (ou limit_ge_/limit_le_) -> variação do custo por unidade da exigência (ou do limite)


@dataclass(frozen=True)
class Problem:
    standard: str
    animal_type: str
    ids: list[int]
    feeds: list[Any]
    price: np.ndarray
    lower: np.ndarray
    upper: np.ndarray
    requirements: RequirementsResult
    body_weight: float
    pen: tuple[float, float] | None
    tdn: np.ndarray = field(repr=False)
    concentrate: np.ndarray = field(repr=False)
    starch: np.ndarray = field(repr=False)  # kg de amido por kg de MS

    @property
    def dims(self) -> tuple[str, ...]:
        return ("dmi", "tdn", "conc", "starch") if self.standard == "NASEM" else ("dmi", "tdn", "conc")

    def equalities(self, point: Point) -> tuple[np.ndarray, np.ndarray]:
        rows = [np.ones(len(self.ids)), self.tdn, self.concentrate]
        rhs = [point.dmi, point.tdn * point.dmi, point.conc / 100 * point.dmi]
        if self.standard == "NASEM":
            rows.append(self.starch)
            rhs.append(point.starch)
        return np.array(rows), np.array(rhs)

    def constraints_at(self, point: Point) -> list[linear.LinearConstraint]:
        reference = linear.Reference(
            point.dmi, intake_discount(point.tdn, point.dmi, self.body_weight), point.tdn, point.conc, point.starch
        )
        return linear.build_at(
            self.standard, self.animal_type, self.feeds, reference, self.requirements.nutrition_requirements, self.body_weight, self.pen
        )


def _split(constraints: Sequence[linear.LinearConstraint]) -> tuple[list[Row], list[Row], list[Row]]:
    """Linhas fixas, ramos da energia total (``max``) e ramos do teto de proteína (``min ≤``)."""
    fixed: list[Row] = []
    energy_branches: list[Row] = []
    protein_ceiling: list[Row] = []
    for c in constraints:
        if c.unavailable:
            raise ValueError(f"{c.label}: {c.unavailable}")
        if c.kind == "E":
            fixed.append(Row(c.id, c.homogeneous, c.sense, 0.0))
        elif c.combine == "single":
            fixed.append(Row(c.id, c.pieces[0].a, c.sense, c.requirement - c.pieces[0].c))
        elif c.combine == "min" and c.sense == "ge":  # min(a, b) ≥ r  ⇔  a ≥ r e b ≥ r (exato)
            fixed += [Row(c.id, p.a, "ge", c.requirement - p.c) for p in c.pieces]
        elif c.combine == "min":  # min(a, b) ≤ U  ⇔  a ≤ U ou b ≤ U
            protein_ceiling = [Row(c.id, p.a, "le", c.requirement - p.c) for p in c.pieces]
        elif c.combine == "max" and c.sense == "ge":  # max(a, b, c) ≥ r  ⇔  um dos três ≥ r
            energy_branches = [Row(c.id, p.a, "ge", c.requirement - p.c) for p in c.pieces]
        else:
            raise ValueError(f"Restrição sem tratamento no LP: {c.id}")
    return fixed, energy_branches, protein_ceiling


_BRANCH_NAMES = ("mantença", "crescimento", "lactação")  # ordem das partes de ``ne_total`` (``linear.build_at``)


def _solve_lp(problem: Problem, point: Point, rows: Sequence[Row], branch: str | None, fix_scalars: bool = True) -> Solution | None:
    sign = np.array([-1.0 if r.sense == "ge" else 1.0 for r in rows])
    a_ub = np.array([s * r.a for s, r in zip(sign, rows)])
    b_ub = np.array([s * r.rhs for s, r in zip(sign, rows)])
    a_eq, b_eq = problem.equalities(point) if fix_scalars else (None, None)
    result = linprog(
        problem.price, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=list(zip(problem.lower, problem.upper)),
        method="highs", options={"primal_feasibility_tolerance": 1e-9, "dual_feasibility_tolerance": 1e-9},
    )  # fmt: skip
    if result.status != 0:
        return None
    prices: dict[str, float] = {}
    for row, s, marginal in zip(rows, sign, result.ineqlin.marginals):
        value = -marginal if row.sense == "ge" else marginal  # d(custo)/d(exigência)
        if abs(value) > TOLERANCE:
            prices[row.id] = prices.get(row.id, 0.0) + float(value)
    for feed_id, low, high in zip(problem.ids, result.lower.marginals, result.upper.marginals):
        if abs(low) > TOLERANCE:
            prices[f"limit_ge_{feed_id}"] = float(low)
        if abs(high) > TOLERANCE:
            prices[f"limit_le_{feed_id}"] = float(high)
    return Solution(point, np.maximum(result.x, 0.0), float(result.fun), branch, prices)


def solve_point(problem: Problem, point: Point, fix_scalars: bool = True) -> Solution | None:
    """Menor custo com os escalares fixos em ``point`` (um LP por ramo das disjunções), ou ``None`` se inviável.

    Com ``fix_scalars=False`` só os coeficientes ficam congelados em ``point`` e as quantidades são livres: é o LP da
    programação linear sucessiva, que indica para onde os escalares querem ir (a solução não é viável no problema original).
    """
    fixed, energy_branches, protein_ceiling = _split(problem.constraints_at(point))
    best: Solution | None = None
    for index, branch in enumerate(energy_branches or [None]):
        rows = [*fixed, *([branch] if branch else [])]
        name = _BRANCH_NAMES[index] if branch and len(energy_branches) == len(_BRANCH_NAMES) else None
        solution = _solve_lp(problem, point, rows, name, fix_scalars)
        if solution and protein_ceiling and not any(r.holds(solution.x) for r in protein_ceiling):
            tries = (_solve_lp(problem, point, [*rows, r], name, fix_scalars) for r in protein_ceiling)
            solution = min((s for s in tries if s), key=lambda s: s.cost, default=None)
        if solution and (best is None or solution.cost < best.cost):
            best = solution
    return best


# ----------------------------------------------------------------------------------------------------------------
# Busca: grade por regime e refinamento local
# ----------------------------------------------------------------------------------------------------------------
def _relaxed_rows(problem: Problem) -> list[Row]:
    """Restrições que não dependem dos escalares (classes L e E): delimitam onde cada escalar pode variar."""
    point = Point(problem.requirements.requirements["dry_matter"], 65.0, 30.0, 4.0)
    rows, _, _ = _split(c for c in problem.constraints_at(point) if c.kind in ("L", "E"))
    return rows


def _scalar_range(problem: Problem, rows: Sequence[Row], dmi: float, direction: np.ndarray) -> tuple[float, float] | None:
    """Menor e maior valor de ``direction·x`` com o consumo em ``dmi`` e as restrições L e E."""
    sign = np.array([-1.0 if r.sense == "ge" else 1.0 for r in rows])
    a_ub = np.array([s * r.a for s, r in zip(sign, rows)])
    b_ub = np.array([s * r.rhs for s, r in zip(sign, rows)])
    bounds = list(zip(problem.lower, problem.upper))
    values = []
    for factor in (1.0, -1.0):
        result = linprog(factor * direction, A_ub=a_ub, b_ub=b_ub, A_eq=[np.ones(len(problem.ids))], b_eq=[dmi], bounds=bounds, method="highs")
        if result.status != 0:
            return None
        values.append(factor * result.fun)
    return values[0], values[1]


def _linspace(low: float, high: float, count: int) -> list[float]:
    return [low] if count <= 1 or high - low < TOLERANCE else [float(v) for v in np.linspace(low, high, count)]


@dataclass(frozen=True)
class Box:
    """Faixa de cada escalar (consumo, TDN%, % de concentrado, amido) onde a busca procura."""

    low: tuple[float, ...]
    high: tuple[float, ...]


def _grid(problem: Problem, sizes: tuple[int, int, int, int, int]) -> tuple[list[Point], Box | None]:
    n_dmi, n_tdn, n_conc, n_starch, _ = sizes
    requirement = problem.requirements.requirements["dry_matter"]
    constraint = (1 - rufas().constants.DMI_CONSTRAINT_FRACTION, 1 + rufas().constants.DMI_CONSTRAINT_FRACTION)
    rows = _relaxed_rows(problem)
    points: list[Point] = []
    lows = np.full(4, np.inf)
    highs = np.full(4, -np.inf)
    for dmi in _linspace(requirement * constraint[0], requirement * constraint[1], n_dmi):
        ranges = [_scalar_range(problem, rows, dmi, v) for v in (problem.tdn, problem.concentrate, problem.starch)]
        if any(r is None for r in ranges):
            continue
        (tdn_lo, tdn_hi), (conc_lo, conc_hi), (starch_lo, starch_hi) = ranges
        tdn_lo, tdn_hi, conc_lo, conc_hi = tdn_lo / dmi, tdn_hi / dmi, conc_lo / dmi * 100, conc_hi / dmi * 100
        tdn_values: list[float] = []
        if tdn_lo < REGIME_BREAK:
            tdn_values += _linspace(tdn_lo, min(tdn_hi, REGIME_BREAK - BREAK_EPSILON), n_tdn)
        if tdn_hi >= REGIME_BREAK:
            tdn_values += _linspace(max(tdn_lo, REGIME_BREAK), tdn_hi, n_tdn)
        starch_values = _linspace(starch_lo, starch_hi, n_starch) if problem.standard == "NASEM" else [0.0]
        for tdn, conc, starch in itertools.product(tdn_values, _linspace(conc_lo, conc_hi, n_conc), starch_values):
            points.append(Point(dmi, tdn, conc, starch))
        lows = np.minimum(lows, [dmi, tdn_lo, conc_lo, starch_lo])
        highs = np.maximum(highs, [dmi, tdn_hi, conc_hi, starch_hi])
    if not points:
        return [], None
    return points, Box(tuple(lows), tuple(highs))


def _clip(point: Point, box: Box, regime: str, nasem: bool) -> Point:
    low, high = list(box.low), list(box.high)
    if regime == "sem_desconto":
        high[1] = min(high[1], REGIME_BREAK - BREAK_EPSILON)
    else:
        low[1] = max(low[1], REGIME_BREAK)
    values = [min(max(v, lo), hi) for v, lo, hi in zip((point.dmi, point.tdn, point.conc, point.starch), low, high)]
    return Point(*values[:3], values[3] if nasem else 0.0)


def _refine(
    start: Solution,
    box: Box,
    steps: np.ndarray,
    problem: Problem,
    solve: Callable[[Point], Solution | None],
    budget: int,
) -> Solution:
    """Busca local por padrões: testa os vizinhos (±passo em cada escalar, combinados) e reduz o passo quando nenhum melhora."""
    best = start
    regime = start.point.regime
    active = [i for i, name in enumerate(("dmi", "tdn", "conc", "starch")) if name in problem.dims]
    spent = 0
    for _ in range(8):
        improved = True
        while improved and spent < budget:
            improved = False
            base = best.point
            found: Solution | None = None
            for moves in itertools.product((-1, 0, 1), repeat=len(active)):
                if not any(moves) or spent >= budget:
                    continue
                values = [base.dmi, base.tdn, base.conc, base.starch]
                for index, move in zip(active, moves):
                    values[index] += move * steps[index]
                candidate = _clip(Point(*values), box, regime, problem.standard == "NASEM")
                if candidate == base:
                    continue
                spent += 1
                solution = solve(candidate)
                if solution and solution.cost < (found or best).cost - 1e-12:
                    found = solution
            if found:
                best, improved = found, True
        steps = steps / 2
        if spent >= budget:
            break
    return best


def scalars_of(problem: Problem, x: np.ndarray) -> Point:
    """Escalares globais de uma dieta."""
    dmi = float(x.sum())
    return Point(dmi, float(problem.tdn @ x / dmi), float(problem.concentrate @ x / dmi * 100), float(problem.starch @ x))


def _descend(
    start: Solution,
    box: Box,
    problem: Problem,
    solve: Callable[[Point], Solution | None],
    should_stop: Callable[[], bool] | None,
) -> Solution:
    """Descida guiada pelo LP: o LP com as quantidades livres (coeficientes congelados no ponto) aponta o destino dos
    escalares; testa passos de comprimentos decrescentes nessa direção, cada um resolvido como LP exato."""
    best = start
    regime = start.point.regime
    nasem = problem.standard == "NASEM"
    for _ in range(40):
        if should_stop and should_stop():
            raise Cancelled
        free = solve_point(problem, best.point, fix_scalars=False)
        if free is None:
            break
        target = scalars_of(problem, free.x)
        base = (best.point.dmi, best.point.tdn, best.point.conc, best.point.starch)
        found: Solution | None = None
        for fraction in (1.0, 0.5, 0.25, 0.1, 0.03):
            moved = Point(*(b + fraction * (t - b) for b, t in zip(base, (target.dmi, target.tdn, target.conc, target.starch))))
            candidate = _clip(moved, box, regime, nasem)
            if candidate == best.point:
                continue
            solution = solve(candidate)
            if solution and solution.cost < (found or best).cost - 1e-12:
                found = solution
        if not found:
            break
        best = found
    return best


def _rescue(
    problem: Problem, grid: Sequence[Point], solve: Callable[[Point], Solution | None], should_stop: Callable[[], bool] | None
) -> list[Solution]:
    """Pontos viáveis quando a grade quase não acerta a região viável (fina em alguns casos): ponto fixo dos escalares.

    A partir de pontos da grade, o LP com as quantidades livres indica os escalares da dieta que ele quer; resolve-se o LP
    exato nesses escalares e repete-se até achar um ponto viável (ou desistir)."""
    found: list[Solution] = []
    for point in grid[:: max(1, len(grid) // RESCUE_POINTS)]:
        current = point
        for _ in range(8):
            if should_stop and should_stop():
                raise Cancelled
            free = solve_point(problem, current, fix_scalars=False)
            if free is None:
                break
            current = scalars_of(problem, free.x)
            exact = solve(current)
            if exact:
                found.append(exact)
                break
    return found


@dataclass
class SearchStats:
    points: int = 0
    feasible: int = 0
    seconds: float = 0.0
    total: int = 0  # passos previstos da busca (grade e refinamento), para a barra de progresso


def search(
    problem: Problem,
    resolution: str,
    on_progress: Callable[[int, int], None] | None = None,
    should_stop: Callable[[], bool] | None = None,
) -> tuple[Solution | None, SearchStats]:
    """Melhor LP da grade de escalares, refinado em torno do melhor ponto de cada regime."""
    sizes = RESOLUTIONS[resolution]
    started = time.perf_counter()
    stats = SearchStats()
    cache: dict[Point, Solution | None] = {}
    grid, box = _grid(problem, sizes)
    total = stats.total = len(grid) + sizes[4] // 2  # o refinamento termina por convergência, bem antes do orçamento
    if on_progress:
        on_progress(0, total)

    def solve(point: Point) -> Solution | None:
        if should_stop and should_stop():
            raise Cancelled
        if point not in cache:
            cache[point] = solve_point(problem, point)
            stats.points += 1
            stats.feasible += cache[point] is not None
            if on_progress:
                on_progress(min(stats.points, total - 1), total)
        return cache[point]

    solutions = [s for s in (solve(p) for p in grid) if s]
    if grid and len(solutions) < MIN_GRID_HITS:
        solutions += _rescue(problem, grid, solve, should_stop)
    best: Solution | None = None
    if solutions and box:
        steps = np.array([(hi - lo) / max(n - 1, 1) for lo, hi, n in zip(box.low, box.high, (sizes[0], 2 * sizes[1], sizes[2], sizes[3]))])
        steps = np.maximum(steps, 1e-3)
        for regime in ("sem_desconto", "com_desconto"):
            starts = sorted((s for s in solutions if s.point.regime == regime), key=lambda s: s.cost)[:STARTS_PER_REGIME]
            for start in starts:
                # Dois caminhos a partir de cada ponto da grade: só a busca por padrões e a descida pelo LP (seguida da busca),
                # porque a função de custo dos escalares não é convexa e cada caminho pode parar num mínimo local diferente.
                paths = (
                    _refine(start, box, steps, problem, solve, sizes[4]),
                    _refine(_descend(start, box, problem, solve, should_stop), box, steps, problem, solve, sizes[4]),
                )
                for refined in paths:
                    best = refined if best is None or refined.cost < best.cost else best
    elif solutions:
        best = min(solutions, key=lambda s: s.cost)
    stats.seconds = time.perf_counter() - started
    if on_progress:
        on_progress(total, total)
    return best, stats


# ----------------------------------------------------------------------------------------------------------------
# Entrada, verificação e comparação com o RuFaS
# ----------------------------------------------------------------------------------------------------------------
def build_problem(
    standard: str,
    category: str,
    animal_type: str,
    cow: Mapping[str, Any],
    ids: Sequence[int],
    prices: Mapping[int, float],
    limits: Mapping[int, tuple[float, float]],
    required: RequirementsResult,
) -> Problem:
    feeds = build_feeds(standard, list(ids), prices, limits)
    pen = pen_inputs(standard, cow)
    if standard == "NASEM" and pen is None:
        raise ValueError("Informe o metano entérico e o nitrogênio urinário do lote: sem eles a energia do NASEM não é calculada.")
    return Problem(
        standard=standard,
        animal_type=animal_type,
        ids=list(ids),
        feeds=feeds,
        price=np.array([prices[i] for i in ids], dtype=float),
        lower=np.array([limits[i][0] for i in ids], dtype=float),
        upper=np.array([limits[i][1] for i in ids], dtype=float),
        requirements=required,
        body_weight=float(cow["body_weight"]),
        pen=pen,
        tdn=np.array([fd.TDN for fd in feeds], dtype=float),
        concentrate=np.array([1.0 if fd.feed_type is rufas().feed_component_type.CONC else 0.0 for fd in feeds]),
        starch=np.array([fd.starch * 0.01 for fd in feeds], dtype=float),
    )


def _amounts(problem: Problem, x: np.ndarray) -> dict[int, float]:
    return {i: float(v) for i, v in zip(problem.ids, x) if v > TOLERANCE}


def _check(
    problem: Problem, category: str, cow: Mapping[str, Any], name: str, amounts: Mapping[int, float],
    prices: Mapping[int, float], limits: Mapping[int, tuple[float, float]],
) -> dict[str, Any]:  # fmt: skip
    """Avaliação da dieta com as exigências da otimização e as funções originais do RuFaS."""
    return evaluate_diet(
        problem.standard, category, problem.animal_type, cow, None, Diet(name, dict(amounts)), prices, limits, problem.pen,
        fixed=problem.requirements,
    )  # fmt: skip


def run_rufas(problem: Problem, category: str, seeds: int, on_each: Callable[[int], None] | None = None) -> list[dict[str, Any]]:
    """Roda o ``RationOptimizer`` (SLSQP) do RuFaS, que parte de um ponto aleatório, com ``seeds`` sementes."""
    rf = rufas()
    nutrition = problem.requirements.nutrition_requirements
    combination = rf.animal_combination[category]
    out = []
    for seed in range(seeds):
        random.seed(seed)
        started = time.perf_counter()
        attempt, _ = rf.optimizer().attempt_optimization(
            nutrient_standard=rf.standard[problem.standard],
            pen_average_body_weight=problem.body_weight,
            pen_average_enteric_methane=problem.pen[0] if problem.pen else None,
            pen_average_urine_nitrogen=problem.pen[1] if problem.pen else None,
            requirements=nutrition,
            initial_dry_matter_requirement=nutrition.dry_matter,
            initial_protein_requirement=nutrition.metabolizable_protein,
            pen_available_feeds=problem.feeds,
            animal_combination=combination,
        )  # fmt: skip
        out.append(
            {
                "seed": seed,
                "success": bool(attempt.success),
                "cost": float(attempt.fun),
                "x": np.maximum(np.asarray(attempt.x, dtype=float), 0.0),
                "iterations": int(attempt.nit),
                "seconds": time.perf_counter() - started,
            }
        )
        if on_each:
            on_each(seed + 1)
    return out


def _within(check: Mapping[str, Any] | None, tolerance: float) -> bool:
    """Nenhuma restrição violada além de ``tolerance`` (relativa à exigência, ou absoluta se a exigência é pequena)."""
    if check is None:
        return False
    return all(max(0.0, -row["slack"]) / max(abs(row["requirement"]), 1.0) <= tolerance for row in check["constraints"] if "slack" in row)


def _comparison(
    problem: Problem, category: str, cow: Mapping[str, Any], runs: list[dict[str, Any]], optimum: Solution,
    prices: Mapping[int, float], limits: Mapping[int, tuple[float, float]],
) -> dict[str, Any]:  # fmt: skip
    results = []
    for run in runs:
        amounts = _amounts(problem, run["x"])
        check = _check(problem, category, cow, f"RuFaS (semente {run['seed']})", amounts, prices, limits) if amounts else None
        results.append(
            {
                "seed": run["seed"],
                "success": run["success"],
                "cost": run["cost"],
                "amounts": amounts,
                "iterations": run["iterations"],
                "seconds": run["seconds"],
                "feasible": _within(check, RUFAS_TOLERANCE),
                "violated": check["violated"] if check else [],
            }
        )
    good = [r for r in results if r["success"] and r["feasible"]]
    costs = [r["cost"] for r in good]
    best = min(good, key=lambda r: r["cost"], default=None)
    return {
        "runs": results,
        "n_runs": len(results),
        "n_success": len(good),
        "cost_min": min(costs, default=None),
        "cost_median": median(costs) if costs else None,
        "cost_max": max(costs, default=None),
        "best_seed": best["seed"] if best else None,
        # Variação do custo do LP em relação ao melhor do RuFaS, em %: negativa = o LP é mais barato.
        "lp_gap_pct": (optimum.cost - best["cost"]) / best["cost"] * 100 if best else None,
    }


def optimize_diet(
    standard: str | None,
    category: str | None,
    cow: Mapping[str, Any],
    feed_ids: Sequence[Any],
    prices: Mapping[Any, Any],
    overrides: Mapping[str, Any] | None = None,
    limits: Mapping[Any, Any] | None = None,
    animal_type: str | None = None,
    resolution: str = "normal",
    seeds: int = 5,
    on_progress: Callable[[int, int], None] | None = None,
    should_stop: Callable[[], bool] | None = None,
) -> dict[str, Any]:
    """Dieta de custo mínimo para a vaca, entre os alimentos dados, e comparação com o SLSQP do RuFaS."""
    nutrient_standard = get_standard(standard).code
    category_ = parse_category(category)
    animal = parse_animal_type(category_, animal_type)
    if resolution not in RESOLUTIONS:
        raise ValueError(f"Resolução desconhecida: {resolution!r} (use {', '.join(RESOLUTIONS)})")
    if isinstance(seeds, bool) or not isinstance(seeds, int) or not 0 <= seeds <= MAX_SEEDS:
        raise ValueError(f"O número de sementes do RuFaS deve ser um inteiro de 0 a {MAX_SEEDS}")
    if not isinstance(feed_ids, Sequence) or isinstance(feed_ids, (str, bytes)) or not feed_ids:
        raise ValueError("Informe os alimentos que a dieta pode usar")
    ids = sorted({int(i) for i in feed_ids})
    library = feed_library(nutrient_standard)
    absent = [i for i in ids if i not in library]
    if absent:
        raise ValueError(f"Alimentos fora da biblioteca {nutrient_standard}: {absent}")
    price_map = {int(k): float(v) for k, v in (prices or {}).items()}
    missing = [i for i in ids if i not in price_map]
    if missing:
        raise ValueError(f"Informe o preço (US$/kg MS) dos alimentos: {missing}")
    if any(price_map[i] < 0 for i in ids):
        raise ValueError("Os preços devem ser maiores ou iguais a zero")
    limit_map = resolve_limits(nutrient_standard, ids, limits)

    required = compute_requirements(nutrient_standard, category_.value, cow, overrides, animal)
    problem = build_problem(nutrient_standard, category_.value, animal, cow, ids, price_map, limit_map, required)
    # O progresso inclui as sementes do RuFaS, que vêm depois da busca.
    best, stats = search(
        problem, resolution, (lambda done, total: on_progress(done, total + seeds)) if on_progress else None, should_stop
    )

    result: dict[str, Any] = {
        "standard": nutrient_standard,
        "category": category_.value,
        "animal_type": animal,
        "requirements": required.requirements,
        "feed_ids": ids,
        "resolution": resolution,
        "search": {"points": stats.points, "feasible_points": stats.feasible, "seconds": stats.seconds},
        "warnings": list(required.warnings),
    }
    if best is None:
        return {
            **result,
            "status": "infeasible",
            "message": (
                "Nenhuma dieta com os alimentos escolhidos atende às restrições (consumo, cálcio, fósforo, fibra, gordura, "
                "energia e proteína). Inclua alimentos ou amplie os limites."
            ),
        }

    amounts = _amounts(problem, best.x)
    check = _check(problem, category_.value, cow, "Dieta ótima", amounts, price_map, limit_map)
    labels = {c["id"]: c["label"] for c in check["constraints"]}

    def label_of(key: str) -> str:
        if key.startswith("limit_"):  # limite de um alimento que ficou fora da dieta não tem linha na avaliação
            return f"Limite {'mínimo' if key.startswith('limit_ge_') else 'máximo'} do alimento {key.rsplit('_', 1)[-1]}"
        return labels.get(key, key)

    result |= {
        "status": "ok",
        "diet": {
            "amounts": amounts,
            "cost": best.cost,
            "cost_per_kg": best.cost / float(best.x.sum()),
            "scalars": {"dmi": best.point.dmi, "tdn_percentage": best.point.tdn, "concentrate_percentage": best.point.conc},
            "regime": best.point.regime,
            "energy_branch": best.energy_branch,
            "verified": check["feasible"],
            "evaluation": check,
        },
        "shadow_prices": [
            {"id": key, "label": label_of(key), "value": value} for key, value in sorted(best.shadow_prices.items())
        ],
    }
    if nutrient_standard == "NASEM":
        result["diet"]["scalars"]["total_starch_kg"] = best.point.starch
    if not check["feasible"]:
        result["warnings"].append(
            "A dieta ótima do LP viola alguma restrição original do RuFaS por uma diferença numérica: " + ", ".join(check["violated"]) + "."
        )
    if seeds:

        def tick(count: int) -> None:
            if should_stop and should_stop():
                raise Cancelled
            if on_progress:
                on_progress(stats.total + count, stats.total + seeds)

        runs = run_rufas(problem, category_.value, seeds, tick)
        result["rufas"] = _comparison(problem, category_.value, cow, runs, best, price_map, limit_map)
    return result

