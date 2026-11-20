"""Metano entérico e nitrogênio urinário como **saídas** da dieta (LINEARIZACAO.md, 7.3).

No NASEM a energia metabolizável é a digestível menos a perdida no metano e na urina: o RuFaS desconta
``METHANE_ENERGY · CH4 + URINE_ENERGY · N urinário`` da oferta. O RuFaS tem equação para os dois, e ambas são **lineares nas
quantidades** ``x`` (kg de MS por dia de cada alimento), de modo que entram na restrição de energia sem aproximação:

* **Metano** (g/dia), modelo IPCC (o configurado no RuFaS para vacas e novilhas)::

      CH4 = (0,065 / 0,05565) · Σ xᵢ · GEᵢ,   GEᵢ = 0,263·PB + 0,522·EE + 0,198·FDN + 0,160·(100 − cinzas − FDN − PB − EE)

  (``GE`` em MJ/kg de MS; as concentrações dos alimentos em % da MS). O produto "consumo × concentração" da fórmula do RuFaS é
  a soma ``Σ xᵢ · conc.ᵢ``, por isso não há aproximação. Os modelos Mutian e Mills do RuFaS não são o configurado e não entram.
* **Nitrogênio urinário** (kg/dia) = N do esterco − N fecal, com ``S = Σ xᵢ · PBᵢ`` (kg·%)::

      vaca em lactação:   (20,3 + 0,654·k·S)/1000 − (−18,5 + 10,1·Σx)/1000
      vaca seca, novilha: (15,1 + 0,83·k·S)/1000 − (0,345 + 0,317·k·S)/1000,   k = 1000·0,16·0,01 = 1,6 g de N por kg·%

  Fica fora o piso do RuFaS (0,022 kg na lactação, 0,017 kg nas outras), que só vale para consumos muito baixos: a verificação
  contra as funções originais (``of_diet_rufas``) mostra se algum dia ele entra.

Se o usuário informar o metano e o nitrogênio urinário do lote, eles valem como constantes (como o RuFaS faz com a média do lote
simulado). Quando nem a equação serve nem há entrada, os valores de partida são ``DEFAULT_*`` (decisão de 20/11/2026).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import numpy as np

from .rufas import rufas

DEFAULT_METHANE_G = 450.0  # g/dia: valor de partida/fallback quando não há entrada nem equação aplicável
DEFAULT_URINE_N_KG = 0.25  # kg/dia

IPCC_FRACTION = 0.065  # fração da energia bruta que vira metano (IPCC, 2006), como em ``_calculate_IPCC_methane``
# Nitrogênio urinário (kg) = N do esterco − N fecal, dos mesmos coeficientes de ``manure_excretion_calculator.py`` do RuFaS.
LACTATING = {"manure_const": 20.3, "manure_slope": 0.654, "fecal_const": -18.5, "fecal_per_dmi": 10.1, "fecal_slope": 0.0}
DRY_OR_HEIFER = {"manure_const": 15.1, "manure_slope": 0.83, "fecal_const": 0.345, "fecal_per_dmi": 0.0, "fecal_slope": 0.317}


@dataclass(frozen=True)
class Emissions:
    """Metano e nitrogênio urinário como funções afins de ``x``: ``valor = coeficiente · x + constante``."""

    methane: np.ndarray  # g/dia por kg de MS de cada alimento
    urine_n: np.ndarray  # kg/dia por kg de MS de cada alimento
    urine_n_constant: float  # kg/dia

    def of_diet(self, x: np.ndarray) -> tuple[float, float]:
        """(metano em g/dia, nitrogênio urinário em kg/dia) da dieta ``x`` pelas equações lineares (sem o piso do RuFaS)."""
        return float(self.methane @ x), float(self.urine_n @ x + self.urine_n_constant)


def _equation(animal_type: str) -> Mapping[str, float]:
    return LACTATING if animal_type == "LAC_COW" else DRY_OR_HEIFER


def coefficients(feeds: Sequence[Any], animal_type: str) -> Emissions:
    """Coeficientes lineares do metano e do nitrogênio urinário para os alimentos (objetos do RuFaS) e o tipo de animal."""
    rf = rufas()
    g_per_mj = IPCC_FRACTION / rf.general_constants.MJ_CH4_TO_G_CH4
    n_per_kg_percent = (  # g de N por kg·% de PB da dieta
        rf.general_constants.KG_TO_GRAMS * rf.user_constants.PROTEIN_TO_NITROGEN * rf.general_constants.PERCENTAGE_TO_FRACTION
    )
    eq = _equation(animal_type)
    ge = np.array(
        [0.263 * fd.CP + 0.522 * fd.EE + 0.198 * fd.NDF + 0.160 * (100.0 - fd.ash - fd.NDF - fd.CP - fd.EE) for fd in feeds], dtype=float
    )
    crude = np.array([fd.CP for fd in feeds], dtype=float)
    per_kg = (eq["manure_slope"] - eq["fecal_slope"]) * n_per_kg_percent * crude - eq["fecal_per_dmi"]
    constant = eq["manure_const"] - eq["fecal_const"]
    return Emissions(g_per_mj * ge, per_kg * rf.general_constants.GRAMS_TO_KG, constant * rf.general_constants.GRAMS_TO_KG)


def _supply(feeds: Sequence[Any], x: np.ndarray) -> Any:
    """``NutritionSupply`` da dieta só com a composição (o que as equações de metano e de nitrogênio usam), sem estado de classe."""
    rf = rufas()
    in_ration = [rf.feed_in_ration(float(a), fd) for a, fd in zip(x, feeds)]
    content = {n: rf.supply._calculate_nutritive_content(in_ration, n) for n in ("NDF", "EE", "CP", "ADF", "ash", "potassium", "starch")}
    zero = 0.0
    wet = float(sum(a / (fd.DM * rf.general_constants.PERCENTAGE_TO_FRACTION) for a, fd in zip(x, feeds)))  # a urina da lactação usa a MS %
    return rf.nutrition_supply(
        metabolizable_energy=zero, maintenance_energy=zero, lactation_energy=zero, growth_energy=zero, metabolizable_protein=zero,
        calcium=zero, phosphorus=zero, dry_matter=float(np.sum(x)), wet_matter=wet, ndf_supply=content["NDF"], forage_ndf_supply=zero,
        fat_supply=content["EE"], crude_protein=content["CP"], adf_supply=content["ADF"], digestible_energy_supply=zero, tdn_supply=zero,
        lignin_supply=zero, ash_supply=content["ash"], potassium_supply=content["potassium"], starch_supply=content["starch"],
        byproduct_supply=zero,
    )  # fmt: skip


def of_diet_rufas(feeds: Sequence[Any], x: np.ndarray, animal_type: str, cow: Mapping[str, Any]) -> tuple[float, float]:
    """(metano g/dia, nitrogênio urinário kg/dia) da dieta pelas **funções originais do RuFaS** (com os pisos dele).

    ``cow`` traz o peso, os dias em lactação e o leite (só a água da urina os usa; o nitrogênio depende da dieta)."""
    rf = rufas()
    supply = _supply(feeds, x)
    methane = float(rf.methane._calculate_IPCC_methane(supply))
    weight = float(cow.get("body_weight") or 600.0)
    if animal_type == "LAC_COW":
        _, excreta = rf.manure.calculate_cow_manure(
            True, weight, int(float(cow.get("days_in_milk") or 150)), float(cow.get("milk_true_protein") or 3.1),
            float(cow.get("milk_production") or 30.0), 0.0, 0.0, supply,
        )  # fmt: skip
    elif animal_type == "DRY_COW":
        _, excreta = rf.manure.calculate_cow_manure(False, weight, 0, 0.0, 0.0, 0.0, 0.0, supply)
    else:
        _, excreta = rf.manure.calculate_heifer_manure(weight, 0.0, 0.0, supply)
    return methane, float(excreta.urine_nitrogen)
