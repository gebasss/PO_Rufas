"""Acesso ao código do RuFaS (v1.0.6, sem modificação) que o módulo usa: calculadoras de exigência e de oferta, otimizador.

O RuFaS é importado só na primeira chamada. ``vendor/RuFaS`` vai ao fim do ``sys.path`` para não sombrear módulos nossos.
"""

from __future__ import annotations

import sys
from functools import cache
from types import SimpleNamespace

from ..paths import RUFAS_DIR


@cache
def rufas() -> SimpleNamespace:
    if str(RUFAS_DIR) not in sys.path:
        sys.path.append(str(RUFAS_DIR))
    from RUFAS.biophysical.animal.animal_module_constants import AnimalModuleConstants
    from RUFAS.biophysical.animal.data_types.animal_types import AnimalType
    from RUFAS.biophysical.animal.nutrients.nasem_requirements_calculator import NASEMRequirementsCalculator
    from RUFAS.biophysical.animal.nutrients.nrc_requirements_calculator import NRCRequirementsCalculator
    from RUFAS.biophysical.animal.nutrients.nutrition_supply_calculator import FeedInRation, NutritionSupplyCalculator
    from RUFAS.biophysical.animal.ration.ration_optimizer import RationConfig, RationOptimizer
    from RUFAS.data_structures.feed_storage_to_animal_connection import (
        FeedCategorization,
        FeedComponentType,
        NASEMFeed,
        NRCFeed,
    )
    from RUFAS.data_structures.feed_storage_to_animal_connection import NutrientStandard as RufasStandard
    from RUFAS.units import MeasurementUnits

    return SimpleNamespace(
        constants=AnimalModuleConstants,
        animal_type=AnimalType,
        calculators={"NRC": NRCRequirementsCalculator, "NASEM": NASEMRequirementsCalculator},
        supply=NutritionSupplyCalculator,
        feed_in_ration=FeedInRation,
        optimizer=RationOptimizer,
        ration_config=RationConfig,
        feed_class={"NRC": NRCFeed, "NASEM": NASEMFeed},
        feed_categorization=FeedCategorization,
        feed_component_type=FeedComponentType,
        standard={"NRC": RufasStandard.NRC, "NASEM": RufasStandard.NASEM},
        units=MeasurementUnits,
    )
