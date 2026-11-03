"""Alimentos do RuFaS (objetos ``NRCFeed`` ou ``NASEMFeed``) montados a partir da biblioteca de cada padrão.

O RuFaS faz a mesma conversão ao ler a biblioteca (``FeedManager``): categorias e unidades viram enumerações e o resto é
numérico. Aqui o preço e os limites de inclusão vêm do pedido, não do arquivo.
"""

from __future__ import annotations

import csv
import dataclasses
import typing
from functools import cache
from typing import Any, Mapping

from ..standards import get_standard
from .rufas import rufas

_PER_FEED = {"amount_available", "on_farm_cost", "purchase_cost", "buffer", "limit", "lower_limit"}
_BUFFER = 0.15  # reserva padrão de compra do RuFaS (não afeta o cálculo das exigências nem das ofertas)


@cache
def _rows(standard: str) -> dict[int, dict[str, str]]:
    with open(get_standard(standard).library_path, encoding="utf-8-sig", newline="") as handle:
        return {int(float(row["rufas_id"])): row for row in csv.DictReader(handle) if row["rufas_id"]}


def _convert(name: str, hint: Any, raw: str) -> Any:
    rf = rufas()
    if name == "Fd_Category":
        return rf.feed_categorization(raw)
    if name == "feed_type":
        return rf.feed_component_type(raw)
    if name == "units":
        return rf.units(raw)
    if hint is bool:
        return str(raw).strip().upper() == "TRUE"
    if hint is int:
        return int(float(raw))
    if hint is str:
        return raw
    try:
        return float(raw)
    except (TypeError, ValueError):
        return 0.0  # campo vazio na biblioteca


def build_feed(standard: str, feed_id: int, price: float, limits: tuple[float, float]) -> Any:
    """Alimento do RuFaS com preço (US$/kg MS) e limites de inclusão (kg MS/dia)."""
    nutrient_standard = get_standard(standard).code
    row = _rows(nutrient_standard).get(feed_id)
    if row is None:
        raise ValueError(f"Alimento {feed_id} fora da biblioteca {nutrient_standard}")
    cls = rufas().feed_class[nutrient_standard]
    hints = typing.get_type_hints(cls)
    values: dict[str, Any] = {"rufas_id": feed_id}
    for spec in dataclasses.fields(cls):
        if spec.name == "rufas_id" or spec.name in _PER_FEED:
            continue
        values[spec.name] = _convert(spec.name, hints.get(spec.name), row.get(spec.name, "") or "")
    values.update(
        lower_limit=limits[0],
        limit=limits[1],
        purchase_cost=price,
        amount_available=1e9,
        on_farm_cost=0.0,
        buffer=_BUFFER,
    )
    return cls(**values)


def build_feeds(
    standard: str, ids: list[int], prices: Mapping[int, float], limits: Mapping[int, tuple[float, float]]
) -> list[Any]:
    return [build_feed(standard, i, prices[i], limits[i]) for i in ids]
