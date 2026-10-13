"""Leitura dos resultados de uma simulação do RuFaS (JSONs gerados pelos filtros de saída)."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

# Filtros (regex sobre "Classe.função.variável") que trazem só o que o otimizador precisa.
RESULT_FILTERS: dict[str, list[str]] = {
    "herd": [
        r".*report_herd_statistics_data\.(daily_milk_production|milking_cow_num|avg_days_in_milk"
        r"|herd_milk_fat_kg|herd_milk_protein_kg)",
    ],
    "lac_ration": [
        r".*report_ration_per_animal\.ration_per_animal_for_LAC_COW.*",
        r".*report_average_nutrient_requirements\.avg_rqmts_for_LAC_COW.*",
        r".*report_nutrient_amounts\.ration_nutrient_amount_for_LAC_COW.*",
    ],
    "purchases": [r".*FeedManager\.purchase_feed\.ration_interval_.*"],
    "lactation": [r".*LactationCurve\.__init__\.parity_\d_lactation_curve_parameter__[lmn]"],
}

DAILY_KEYS = {
    "daily_milk_production": "milk_kg",
    "milking_cow_num": "milking_cows",
    "avg_days_in_milk": "avg_dim",
    "herd_milk_fat_kg": "fat_kg",
    "herd_milk_protein_kg": "protein_kg",
}


def _series(entry: dict[str, Any]) -> list[tuple[int | None, Any]]:
    """Pares (dia da simulação, valor) de uma variável do pool."""
    values = entry.get("values", [])
    infos = entry.get("info_maps", [])
    pairs = []
    for index, value in enumerate(values):
        day = infos[index].get("simulation_day") if index < len(infos) and isinstance(infos[index], dict) else None
        pairs.append((index if day is None else day, value))
    return pairs


@dataclass
class SimulationResult:
    days: list[int] = field(default_factory=list)
    milk_kg: list[float] = field(default_factory=list)  # leite total do rebanho por dia
    milking_cows: list[float] = field(default_factory=list)
    avg_dim: list[float] = field(default_factory=list)
    fat_kg: list[float] = field(default_factory=list)
    protein_kg: list[float] = field(default_factory=list)
    # uma entrada por intervalo de formulação de ração
    interval_days: list[int] = field(default_factory=list)
    ration_kg_per_cow: list[dict[str, float]] = field(default_factory=list)  # feed id -> kg/vaca/dia (ou 'dry_matter_intake_total')
    requirements: list[dict[str, Any]] = field(default_factory=list)
    cows_in_pen: list[int] = field(default_factory=list)
    purchase_cost: dict[str, list[float]] = field(default_factory=dict)  # feed id -> custo por intervalo
    purchase_amount: dict[str, list[float]] = field(default_factory=dict)
    wood: dict[int, dict[str, float]] = field(default_factory=dict)  # paridade -> {l, m, n} da curva de Wood

    @property
    def total_milk_kg(self) -> float:
        return float(sum(self.milk_kg))

    @property
    def total_purchase_cost(self) -> float:
        return float(sum(sum(v) for v in self.purchase_cost.values()))


def parse_outputs(outputs: dict[str, Any]) -> SimulationResult:
    """Converte os JSONs lidos por ``RunResult.read_json_outputs`` em um ``SimulationResult``."""
    result = SimulationResult()
    pool: dict[str, Any] = {}
    for content in outputs.values():
        pool.update({k: v for k, v in content.items() if isinstance(v, dict)})

    daily: dict[str, dict[int, float]] = {}
    for key, entry in pool.items():
        short = key.rsplit(".", 1)[-1]
        if "report_herd_statistics_data" in key and short in DAILY_KEYS:
            daily[DAILY_KEYS[short]] = {int(day): float(value) for day, value in _series(entry) if day is not None}
    if daily:
        result.days = sorted(daily.get("milk_kg", {}))
        for name in DAILY_KEYS.values():
            setattr(result, name, [daily.get(name, {}).get(day, float("nan")) for day in result.days])

    for key, entry in pool.items():
        if re.search(r"ration_per_animal_for_LAC_COW", key):
            for day, value in _series(entry):
                result.interval_days.append(int(day) if day is not None else len(result.interval_days))
                result.ration_kg_per_cow.append({k: float(v) for k, v in value.items()})
            result.cows_in_pen = [info.get("number_animals_in_pen", 0) for info in entry.get("info_maps", [])]
        elif re.search(r"parity_(\d)_lactation_curve_parameter__([lmn])$", key):
            parity, letter = re.search(r"parity_(\d)_lactation_curve_parameter__([lmn])$", key).groups()  # type: ignore[union-attr]
            values = entry.get("values", [])
            if values:
                result.wood.setdefault(int(parity), {})[letter] = float(values[0])
        elif re.search(r"avg_rqmts_for_LAC_COW", key):
            result.requirements = [value for _, value in _series(entry)]
        elif re.search(r"purchase_feed\.ration_interval_(\d+)_(cost|amount_purchased)$", key):
            feed_id, kind = re.search(r"ration_interval_(\d+)_(cost|amount_purchased)$", key).groups()  # type: ignore[union-attr]
            target = result.purchase_cost if kind == "cost" else result.purchase_amount
            target[feed_id] = [float(v) for _, v in _series(entry)]
    return result


def load_result(folder: Path) -> SimulationResult:
    outputs = {}
    for path in sorted((folder / "json").glob("*.json")):
        with open(path, encoding="utf-8") as handle:
            outputs[path.name] = json.load(handle)
    return parse_outputs(outputs)


def result_to_dict(result: SimulationResult) -> dict[str, Any]:
    return asdict(result)


def result_from_dict(data: dict[str, Any]) -> SimulationResult:
    data = dict(data)
    data["wood"] = {int(parity): params for parity, params in data.get("wood", {}).items()}
    return SimulationResult(**data)
