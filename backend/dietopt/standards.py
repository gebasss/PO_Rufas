"""Padrões nutricionais aceitos pelo RuFaS (NRC 2001 e NASEM 2021) e o que muda de um para o outro.

Cada padrão é um valor imutável que descreve onde o RuFaS lê a biblioteca de alimentos e como ajustar o exemplo-base. O
resto do código recebe o padrão por parâmetro em vez de testar o texto ``"NRC"`` ou ``"NASEM"`` em vários lugares.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from functools import cache
from types import MappingProxyType
from typing import Mapping

from .paths import FEED_DATA_DIR

# Alimentos do exemplo que só existem na biblioteca NASEM -> equivalentes na biblioteca NRC.
# 301 "Farm ES Mineral Mix" -> 230 carbonato de cálcio; 302 "Farm ES Midwest BP Blend" -> 167 farelo de soja 48% PB.
NASEM_ONLY_TO_NRC: Mapping[int, int] = MappingProxyType({301: 230, 302: 167})


@dataclass(frozen=True)
class NutrientStandard:
    code: str  # valor de ``nutrient_standard`` no RuFaS
    label: str
    library_file: str  # CSV da biblioteca de alimentos, em ``vendor/RuFaS/input/data/feed``
    metadata_key: str  # chave do arquivo da biblioteca no metadata do RuFaS
    id_remap: Mapping[int, int] = field(default_factory=dict)  # trocas de id no ``feed.json`` do exemplo-base

    @property
    def library_path(self):
        return FEED_DATA_DIR / self.library_file


NRC = NutrientStandard("NRC", "NRC 2001", "NRC_comp.csv", "NRC_Comp", NASEM_ONLY_TO_NRC)
NASEM = NutrientStandard("NASEM", "NASEM 2021", "NASEM_Comp_with_TDN_urea.csv", "NASEM_Comp")

STANDARDS: Mapping[str, NutrientStandard] = MappingProxyType({s.code: s for s in (NRC, NASEM)})


def get_standard(code: str | None) -> NutrientStandard:
    """Devolve o padrão pelo código (``None`` vale NRC). Código desconhecido levanta ``ValueError``."""
    try:
        return STANDARDS[code or NRC.code]
    except KeyError:
        raise ValueError(f"Padrão nutricional desconhecido: {code!r} (use {' ou '.join(STANDARDS)})") from None


@cache
def library_ids(code: str) -> frozenset[int]:
    """Ids de alimento presentes na biblioteca do padrão."""
    with open(get_standard(code).library_path, encoding="utf-8-sig", newline="") as handle:
        return frozenset(int(float(row["rufas_id"])) for row in csv.DictReader(handle) if row["rufas_id"])
