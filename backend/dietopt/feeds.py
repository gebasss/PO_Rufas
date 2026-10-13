"""Biblioteca de alimentos da NRC (2001) do RuFaS, para a interface e para o PL rápido."""

from __future__ import annotations

import csv
from dataclasses import dataclass

from .rufas_adapter import INPUT
from .scenarios import DEFAULT_PRICES

# Alimentos que não fazem sentido na ração de vacas em lactação (líquidos de bezerro, iniciador, sais soltos).
EXCLUDED_CATEGORIES = {"Calf Liquid Feed", "Starter"}
MINERAL_CATEGORY = "Vitamin/Mineral"


@dataclass(frozen=True)
class FeedInfo:
    id: int
    name: str
    description: str
    kind: str  # Forage / Conc / Mineral ...
    category: str
    dm: float  # % da matéria natural
    cp: float  # % da MS
    ndf: float
    ee: float
    tdn: float
    calcium: float
    phosphorus: float
    default_price: float | None  # US$/kg MS (ilustrativo)

    @property
    def default_max(self) -> float:
        """Inclusão máxima padrão (kg por vaca por dia, unidade do ``limit`` do RuFaS) para evitar soluções irreais.

        Sem um teto, um mineral barato vira "enchimento" que cumpre o consumo de matéria seca a baixo custo.
        Tetos usuais de formulação para ~30 kg de MS/dia: minerais 2% (0,6 kg), gorduras 3% (0,9 kg) e farinhas
        proteicas de origem animal ~1 kg.
        """
        if self.kind == "Mineral" or self.category == MINERAL_CATEGORY:
            return 0.6
        if self.ee >= 80:
            return 0.9
        if self.cp >= 60:
            return 1.0
        return 100.0

    @property
    def nel_mcal_per_kg(self) -> float:
        """NEL (Mcal/kg MS) pela Eq. 2-3 da NRC (2001): 0,0245 * TDN(%) - 0,12."""
        return 0.0245 * self.tdn - 0.12


def load_feed_library() -> list[FeedInfo]:
    descriptions = {}
    with open(INPUT / "data" / "feed" / "user_feeds.csv", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            descriptions[int(row["rufas_id"])] = row
    feeds = []
    with open(INPUT / "data" / "feed" / "NRC_comp.csv", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            feed_id = int(row["rufas_id"])
            info = descriptions[feed_id]
            if row["Fd_Category"] in EXCLUDED_CATEGORIES or row["feed_type"] in {"Milk", "Starter"}:
                continue
            feeds.append(
                FeedInfo(
                    id=feed_id,
                    name=info["Name"].strip().title(),
                    description=info["feed_description"].strip(),
                    kind=row["feed_type"],
                    category=row["Fd_Category"],
                    dm=float(row["DM"]),
                    cp=float(row["CP"]),
                    ndf=float(row["NDF"]),
                    ee=float(row["EE"]),
                    tdn=float(row["TDN"]),
                    calcium=float(row["calcium"]),
                    phosphorus=float(row["phosphorus"]),
                    default_price=DEFAULT_PRICES.get(feed_id),
                )
            )
    return feeds
