"""Cenários: executa o RuFaS, calcula custo da dieta, receita do leite e margem sobre o custo de alimentação."""

from __future__ import annotations

import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .rufas_adapter import RUNS_DIR, RunResult, Scenario, run_scenario
from .rufas_results import RESULT_FILTERS, SimulationResult, load_result, result_from_dict, result_to_dict

# Preços ilustrativos em US$/kg de matéria seca. São valores de partida para a demonstração e devem ser
# substituídos pelos do usuário (por exemplo, indicadores do CEPEA convertidos).
DEFAULT_PRICES: dict[int, float] = {
    23: 1.10,  # farinha de sangue
    44: 0.28,  # milho grão moído seco
    50: 0.09,  # silagem de milho imatura
    51: 0.10,  # silagem de milho meio maturação
    95: 0.18,  # feno de gramínea-leguminosa maduro
    104: 0.11,  # silagem de gramínea-leguminosa
    110: 0.12,  # silagem de leguminosa
    138: 0.25,  # farelo de arroz
    164: 0.60,  # farelo de soja expeller
    166: 0.50,  # farelo de soja 44% PB
    167: 0.55,  # farelo de soja 48% PB
    169: 0.62,  # soja grão
    230: 0.10,  # carbonato de cálcio
    194: 0.30,  # trigo laminado
    8: 0.30,  # cevada laminada
    24: 0.22,  # grãos de cervejaria secos
    58: 0.35,  # caroço de algodão
    193: 0.20,  # farelo de trigo
    1: 0.20,  # farinha de alfafa
}
DEFAULT_MILK_PRICE = 0.45  # US$/kg de leite


@dataclass
class Economics:
    milk_price: float = DEFAULT_MILK_PRICE
    prices: dict[int, float] = field(default_factory=lambda: dict(DEFAULT_PRICES))


@dataclass
class Evaluation:
    name: str
    ok: bool
    seconds: float
    milk_kg: float = float("nan")
    milk_revenue: float = float("nan")
    feed_cost: float = float("nan")  # custo de compra de alimentos de todo o rebanho no período
    lac_cost_per_cow_day: float = float("nan")  # custo da ração das vacas em lactação (US$/vaca/dia)
    margin: float = float("nan")
    ration: dict[str, float] = field(default_factory=dict)  # kg MS/vaca/dia, média dos intervalos
    reduction: float = 0.0  # redução média de leite imposta pelo RuFaS por falta de alimento
    result: SimulationResult | None = None
    detail: str = ""

    def as_row(self) -> dict[str, Any]:
        return {
            "cenario": self.name,
            "ok": self.ok,
            "leite_kg": round(self.milk_kg),
            "receita": round(self.milk_revenue, 2),
            "custo_alimentacao": round(self.feed_cost, 2),
            "custo_vaca_dia": round(self.lac_cost_per_cow_day, 3),
            "margem": round(self.margin, 2),
            "segundos": round(self.seconds, 1),
        }


def with_defaults(scenario: Scenario, economics: Economics) -> Scenario:
    """Garante filtros de saída e preços para todos os alimentos usados pelo cenário."""
    scenario.filters = scenario.filters or RESULT_FILTERS
    prices = dict(economics.prices)
    prices.update(scenario.feed_prices)
    scenario.feed_prices = prices
    return scenario


CACHE_DIR = RUNS_DIR / "_cache"


def cache_key(scenario: Scenario) -> str:
    """Identifica a simulação pelos parâmetros que alteram o RuFaS (não pelo nome)."""
    content = asdict(scenario)
    content.pop("name")
    content.pop("filters")
    return hashlib.sha1(json.dumps(content, sort_keys=True, default=str).encode()).hexdigest()[:16]


def simulate(scenario: Scenario) -> tuple[bool, float, SimulationResult | None, str]:
    """Roda (ou recupera do cache) a simulação. Devolve (ok, segundos, resultado, detalhe)."""
    path = CACHE_DIR / f"{cache_key(scenario)}.json"
    if path.exists():
        with open(path, encoding="utf-8") as handle:
            return True, 0.0, result_from_dict(json.load(handle)), "cache"
    run: RunResult = run_scenario(scenario)
    if not run.ok:
        return False, run.seconds, None, run.stdout_tail[-400:]
    result = load_result(Path(RUNS_DIR) / scenario.name)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(result_to_dict(result), handle)
    return True, run.seconds, result, ""


def evaluate(scenario: Scenario, economics: Economics | None = None) -> Evaluation:
    economics = economics or Economics()
    scenario = with_defaults(scenario, economics)
    ok, seconds, result, detail = simulate(scenario)
    if not ok or result is None:
        return Evaluation(scenario.name, False, seconds, detail=detail)
    prices = scenario.feed_prices

    ration_totals: dict[str, float] = {}
    cost_rate = []
    for ration in result.ration_kg_per_cow:
        rate = 0.0
        for feed_id, kg in ration.items():
            if feed_id == "dry_matter_intake_total":
                continue
            ration_totals[feed_id] = ration_totals.get(feed_id, 0.0) + kg / len(result.ration_kg_per_cow)
            rate += kg * prices.get(int(feed_id), 0.0)
        cost_rate.append(rate)
    reductions = [r.get("avg_milk_production_reduction_pen", 0.0) for r in result.requirements]

    milk_revenue = result.total_milk_kg * economics.milk_price
    feed_cost = sum(
        sum(amounts) * prices.get(int(feed_id), 0.0) for feed_id, amounts in result.purchase_amount.items()
    )
    # custo informado pelo próprio RuFaS (quando disponível) é usado como conferência
    return Evaluation(
        name=scenario.name,
        ok=True,
        seconds=seconds,
        milk_kg=result.total_milk_kg,
        milk_revenue=milk_revenue,
        feed_cost=feed_cost,
        lac_cost_per_cow_day=sum(cost_rate) / max(len(cost_rate), 1),
        margin=milk_revenue - feed_cost,
        ration=ration_totals,
        reduction=sum(reductions) / max(len(reductions), 1),
        result=result,
    )


def evaluate_many(
    scenarios: list[Scenario], economics: Economics | None = None, workers: int = 2
) -> list[Evaluation]:
    """Roda vários cenários, até ``workers`` simulações ao mesmo tempo (cada uma usa ~1,2 GB de RAM)."""
    economics = economics or Economics()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda sc: evaluate(sc, economics), scenarios))
