"""Exigências nutricionais de uma vaca, calculadas pelas calculadoras do RuFaS (NRC 2001 ou NASEM 2021).

As calculadoras rodam isoladas, sem iniciar uma simulação. O RuFaS é importado só na primeira chamada. As exigências
são constantes do problema linear (LINEARIZACAO.md, seção 3.2): dependem só da vaca, não das quantidades dos alimentos.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from functools import cache
from types import SimpleNamespace
from typing import Any, Mapping

from ..paths import RUFAS_DIR
from ..standards import get_standard
from .categories import parse_animal_type, parse_category
from .fields import DIET_FIELDS, FIELD_BY_KEY, FIELDS, usage

# Exigências que o usuário pode sobrescrever (nome do atributo de ``NutritionRequirements`` -> rótulo e unidade).
REQUIREMENT_FIELDS: Mapping[str, tuple[str, str]] = {
    "maintenance_energy": ("Energia de mantença", "Mcal/dia"),
    "activity_energy": ("Energia de atividade", "Mcal/dia"),
    "growth_energy": ("Energia de crescimento", "Mcal/dia"),
    "pregnancy_energy": ("Energia de gestação", "Mcal/dia"),
    "lactation_energy": ("Energia de lactação", "Mcal/dia"),
    "metabolizable_protein": ("Proteína metabolizável", "g/dia"),
    "calcium": ("Cálcio", "g/dia"),
    "phosphorus": ("Fósforo", "g/dia"),
    "process_based_phosphorus": ("Fósforo do processo", "g/dia"),
    "dry_matter": ("Consumo de matéria seca estimado", "kg/dia"),
}

# Argumentos que a calculadora exige mesmo quando ignora o campo (valores neutros; não alteram o resultado).
_NEUTRAL = {
    "parity": 0,
    "day_of_pregnancy": None,
    "days_in_milk": None,
    "calving_interval": 0,  # 0 desliga o ganho de peso da vaca jovem (guarda ``calving_interval != 0`` das calculadoras)
    "average_daily_gain_heifer": None,
    "body_condition_score_5": 3.0,
    "milk_production": 0.0,
    "milk_fat": 3.7,
    "milk_true_protein": 3.1,
    "milk_lactose": 4.85,
    "days_born": 1,
    "process_based_phosphorus_requirement": 0.0,
}


@dataclass(frozen=True)
class RequirementsResult:
    standard: str
    category: str
    animal_type: str
    requirements: dict[str, float]  # já com as sobrescritas
    calculated: dict[str, float]  # como saíram da calculadora
    overridden: list[str]
    inputs: dict[str, Any]  # valores efetivamente enviados à calculadora (inclui os padrões do RuFaS)
    warnings: list[str] = field(default_factory=list)


@cache
def _rufas() -> SimpleNamespace:
    """Importa as peças do RuFaS sob demanda (``vendor/RuFaS`` vai ao fim do ``sys.path`` para não sombrear módulos nossos)."""
    if str(RUFAS_DIR) not in sys.path:
        sys.path.append(str(RUFAS_DIR))
    from RUFAS.biophysical.animal.animal_module_constants import AnimalModuleConstants
    from RUFAS.biophysical.animal.data_types.animal_types import AnimalType
    from RUFAS.biophysical.animal.nutrients.nasem_requirements_calculator import NASEMRequirementsCalculator
    from RUFAS.biophysical.animal.nutrients.nrc_requirements_calculator import NRCRequirementsCalculator

    return SimpleNamespace(
        constants=AnimalModuleConstants,
        animal_type=AnimalType,
        calculators={"NRC": NRCRequirementsCalculator, "NASEM": NASEMRequirementsCalculator},
    )


# Valor do RuFaS para a ração anterior quando o animal ainda não tem uma (``Animal.calculate_requirements``).
# A temperatura vem de ``AnimalRequirements`` (15 °C). O RuFaS guarda a FDN padrão como 0,3 e a passa à calculadora, que a
# trata como porcentagem: o módulo replica isso (LINEARIZACAO.md, 4.7) e avisa.
_PREVIOUS_TEMPERATURE = 15.0


def rufas_diet_defaults() -> dict[str, float]:
    """Padrões do RuFaS para os campos da ração anterior, nas unidades da interface (% da MS, Mcal/kg, °C)."""
    constants = _rufas().constants
    return {
        "tdn_percentage": constants.DEFAULT_TDN_PERCENTAGE * 100,
        "net_energy_diet_concentration": constants.DEFAULT_NET_ENERGY_DIET_CONCENTRATION,
        "ndf_percentage": constants.DEFAULT_NDF_PERCENTAGE,
        "previous_temperature": _PREVIOUS_TEMPERATURE,
    }


def _number(key: str, value: Any) -> float | int | str:
    spec = FIELD_BY_KEY[key]
    if spec.choices:
        if value not in spec.choices:
            raise ValueError(f"{spec.label}: use {' ou '.join(spec.choices)} (recebido {value!r})")
        return value
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError(f"{spec.label}: valor numérico esperado (recebido {value!r})")
    try:
        number = float(value)
    except ValueError:
        raise ValueError(f"{spec.label}: valor numérico esperado (recebido {value!r})") from None
    if not math.isfinite(number):
        raise ValueError(f"{spec.label}: valor finito esperado")
    if spec.integer:
        if number != int(number):
            raise ValueError(f"{spec.label}: número inteiro esperado (recebido {value!r})")
        number = int(number)
    low, high = spec.minimum, spec.maximum
    if (low is not None and number < low) or (high is not None and number > high):
        raise ValueError(f"{spec.label}: {number:g} fora da faixa aceita, de {low:g} a {high:g} {spec.unit}".rstrip())
    return number


def _blank(value: Any) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def validate_cow(standard: str, animal_type: str, cow: Mapping[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Valida os campos da vaca para o padrão e o tipo de animal. Devolve (valores, avisos)."""
    unknown = sorted(set(cow) - set(FIELD_BY_KEY))
    if unknown:
        raise ValueError(f"Campos desconhecidos: {', '.join(unknown)}")
    values: dict[str, Any] = {}
    warnings: list[str] = []
    for spec in FIELDS:
        mode = usage(spec.key, standard, animal_type)
        given = cow.get(spec.key)
        if mode is None:
            if not _blank(given):
                warnings.append(f"{spec.label}: o padrão {standard} ignora este campo para {animal_type}.")
            continue
        if _blank(given):
            if mode == "required":
                raise ValueError(f"{spec.label} é obrigatório para {animal_type} no padrão {standard}")
            continue
        values[spec.key] = _number(spec.key, given)
    return values, warnings


def _arguments(standard: str, animal_type: str, values: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, float], list[str]]:
    """Argumentos da calculadora do RuFaS (fração no TDN, padrões do RuFaS na ração anterior) e os padrões usados."""
    rufas = _rufas()
    args: dict[str, Any] = {
        "animal_type": getattr(rufas.animal_type, animal_type),
        **{key: values.get(key, neutral) for key, neutral in _NEUTRAL.items()},
        **{key: values[key] for key in ("body_weight", "mature_body_weight", "housing", "distance")},
    }
    if standard == "NASEM":
        args.pop("days_born")  # só a calculadora NRC recebe a idade
        args["lactating"] = animal_type == "LAC_COW"
    warnings: list[str] = []
    if "calving_interval" not in values and values.get("parity") in (1, 2) and animal_type in ("LAC_COW", "DRY_COW"):
        warnings.append(
            "Intervalo entre partos vazio: sem o ganho de peso da vaca de 1ª ou 2ª paridade "
            "(as calculadoras tratam 0 assim); informe-o para incluir esse ganho."
        )
    defaults = rufas_diet_defaults()
    used_defaults: dict[str, float] = {}
    for key in DIET_FIELDS[standard]:
        if key in values:
            diet_value = values[key]
        else:
            diet_value = used_defaults[key] = defaults[key]
            warnings.append(
                f"{FIELD_BY_KEY[key].label}: usado o padrão do RuFaS ({defaults[key]:g} {FIELD_BY_KEY[key].unit}); "
                "na avaliação de uma dieta vem da própria dieta."
            )
        if key == "tdn_percentage":
            args["TDN_percentage"] = diet_value / 100  # a calculadora espera fração
        else:
            args[key] = diet_value
    if standard == "NASEM" and "ndf_percentage" in used_defaults:
        warnings.append("O RuFaS guarda a FDN padrão como 0,3 e a calculadora a trata como porcentagem; replicado.")
    return args, used_defaults, warnings


def compute_requirements(
    standard: str | None,
    category: str,
    cow: Mapping[str, Any],
    overrides: Mapping[str, Any] | None = None,
    animal_type: str | None = None,
) -> RequirementsResult:
    """Exigências da vaca pelo padrão, com as sobrescritas do usuário (nome do atributo -> valor)."""
    nutrient_standard = get_standard(standard).code
    category_ = parse_category(category)
    animal = parse_animal_type(category_, animal_type)
    values, warnings = validate_cow(nutrient_standard, animal, cow)
    overrides = dict(overrides or {})
    bad = sorted(set(overrides) - set(REQUIREMENT_FIELDS))
    if bad:
        raise ValueError(f"Exigências desconhecidas para sobrescrever: {', '.join(bad)}")

    args, used_defaults, default_warnings = _arguments(nutrient_standard, animal, values)
    calculator = _rufas().calculators[nutrient_standard]
    result = calculator.calculate_requirements(**args)
    calculated = {name: float(getattr(result, name)) for name in REQUIREMENT_FIELDS}
    if not all(math.isfinite(v) for v in calculated.values()):
        raise ValueError("A calculadora do RuFaS devolveu valor inválido; confira os campos da vaca.")

    final = dict(calculated)
    for name, value in overrides.items():
        label, unit = REQUIREMENT_FIELDS[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError(f"{label}: valor numérico maior ou igual a zero esperado (recebido {value!r})")
        final[name] = float(value)
    inputs = {**values, **used_defaults}
    return RequirementsResult(
        standard=nutrient_standard,
        category=category_.value,
        animal_type=animal,
        requirements=final,
        calculated=calculated,
        overridden=sorted(overrides),
        inputs=inputs,
        warnings=warnings + default_warnings,
    )
