"""Campos de entrada da vaca e o uso de cada um por padrão e tipo de animal (FSD, Anexo B.3).

O uso de cada campo foi medido em 01/11/2026 alterando um campo por vez nas calculadoras de exigência do RuFaS e vendo
se o resultado mudava. ``required`` = sem valor padrão, o usuário precisa informar; ``optional`` = a calculadora usa o
campo, mas aceita vazio; campo fora de ``usage`` = a calculadora ignora.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Usage = Literal["required", "optional"]


@dataclass(frozen=True)
class FieldSpec:
    key: str
    label: str
    unit: str
    minimum: float | None = None
    maximum: float | None = None
    integer: bool = False
    choices: tuple[str, ...] = ()
    group: str = "vaca"  # "vaca" ou "dieta" (valores que, na avaliação de uma dieta, vêm da própria dieta)


# Faixas de sanidade da entrada (evitam erro de digitação e de unidade); não são limites científicos.
FIELDS: tuple[FieldSpec, ...] = (
    FieldSpec("body_weight", "Peso corporal", "kg", 50, 1500),
    FieldSpec("mature_body_weight", "Peso à maturidade", "kg", 200, 1500),
    FieldSpec("parity", "Paridade", "número de partos", 0, 15, integer=True),
    FieldSpec("days_in_milk", "Dias em lactação", "dias", 1, 800, integer=True),
    FieldSpec("day_of_pregnancy", "Dia de gestação", "dias", 1, 285, integer=True),
    FieldSpec("body_condition_score_5", "Escore de condição corporal", "1 a 5", 1, 5),
    FieldSpec("milk_production", "Produção de leite", "kg/dia", 0, 100),
    FieldSpec("milk_fat", "Gordura do leite", "%", 0, 10),
    FieldSpec("milk_true_protein", "Proteína verdadeira do leite", "%", 0, 10),
    FieldSpec("milk_lactose", "Lactose do leite", "%", 0, 10),
    FieldSpec("average_daily_gain_heifer", "Ganho médio diário da novilha", "kg/dia", 0, 2),
    FieldSpec("days_born", "Idade", "dias de vida", 1, 1500, integer=True),
    FieldSpec("calving_interval", "Intervalo entre partos", "dias", 300, 800, integer=True),
    FieldSpec("housing", "Alojamento", "", choices=("Barn", "Grazing")),
    FieldSpec("distance", "Distância percorrida", "m", 0, 20000),
    FieldSpec("process_based_phosphorus_requirement", "Fósforo do processo", "g/dia", 0, 500),
    FieldSpec("enteric_methane", "Metano entérico do lote", "g/dia", 0, 1500, group="lote"),
    FieldSpec("urinary_nitrogen", "Nitrogênio urinário do lote", "kg/dia", 0, 2, group="lote"),
    FieldSpec("ndf_percentage", "FDN da ração anterior", "% da MS", 0, 100, group="dieta"),
    FieldSpec("tdn_percentage", "TDN da ração anterior", "% da MS", 0, 100, group="dieta"),
    FieldSpec("net_energy_diet_concentration", "Energia da ração anterior", "Mcal/kg", 0, 5, group="dieta"),
    FieldSpec("previous_temperature", "Temperatura anterior", "°C", -40, 50, group="dieta"),
)
FIELD_BY_KEY = {spec.key: spec for spec in FIELDS}

_MILK = "milk_production milk_fat milk_true_protein milk_lactose"

# Campos sem valor padrão, por tipo de animal. ``body_condition_score_5`` e ``days_born`` dependem do padrão (ver ``usage``).
_REQUIRED = {
    "LAC_COW": f"body_weight mature_body_weight parity days_in_milk housing distance {_MILK}".split(),
    "DRY_COW": "body_weight mature_body_weight parity day_of_pregnancy housing distance".split(),
    "HEIFER_I": "body_weight mature_body_weight average_daily_gain_heifer housing distance".split(),
    "HEIFER_II": "body_weight mature_body_weight average_daily_gain_heifer housing distance".split(),
    "HEIFER_III": "body_weight mature_body_weight average_daily_gain_heifer day_of_pregnancy housing distance".split(),
}

# Campos que alteram o resultado da calculadora, por (padrão, tipo de animal).
_COMMON = "body_weight mature_body_weight housing distance"
_USED = {
    ("NRC", "LAC_COW"): f"{_COMMON} parity days_in_milk calving_interval {_MILK}".split(),
    ("NRC", "DRY_COW"): f"{_COMMON} parity day_of_pregnancy calving_interval".split(),
    ("NRC", "HEIFER_I"): f"{_COMMON} average_daily_gain_heifer body_condition_score_5 days_born".split(),
    ("NRC", "HEIFER_II"): f"{_COMMON} average_daily_gain_heifer body_condition_score_5 days_born".split(),
    ("NRC", "HEIFER_III"): f"{_COMMON} average_daily_gain_heifer body_condition_score_5 days_born day_of_pregnancy".split(),
    ("NASEM", "LAC_COW"): f"{_COMMON} parity days_in_milk day_of_pregnancy calving_interval body_condition_score_5 {_MILK}".split(),
    ("NASEM", "DRY_COW"): f"{_COMMON} parity day_of_pregnancy days_in_milk calving_interval".split(),
    ("NASEM", "HEIFER_I"): f"{_COMMON} parity day_of_pregnancy average_daily_gain_heifer".split(),
    ("NASEM", "HEIFER_II"): f"{_COMMON} parity day_of_pregnancy days_in_milk average_daily_gain_heifer".split(),
    ("NASEM", "HEIFER_III"): f"{_COMMON} parity day_of_pregnancy days_in_milk average_daily_gain_heifer".split(),
}

# Campos da ração anterior: o NRC usa TDN, energia e temperatura; o NASEM usa a FDN. Todos têm padrão do RuFaS.
DIET_FIELDS = {
    "NRC": ("tdn_percentage", "net_energy_diet_concentration", "previous_temperature"),
    "NASEM": ("ndf_percentage",),
}


# Entradas do lote que o RuFaS usa na energia do NASEM (média dos valores do dia anterior dos animais do lote). Não entram
# nas calculadoras de exigência; servem à oferta de energia (LINEARIZACAO.md, 7.3).
PEN_FIELDS = {"NRC": (), "NASEM": ("enteric_methane", "urinary_nitrogen")}


def usage(key: str, standard: str, animal_type: str) -> Usage | None:
    """Como a calculadora do padrão usa o campo para o tipo de animal (``None`` = ignora)."""
    if key == "process_based_phosphorus_requirement" or key in DIET_FIELDS[standard] or key in PEN_FIELDS[standard]:
        return "optional"
    if key not in _USED[(standard, animal_type)]:
        return None
    required = set(_REQUIRED[animal_type])
    if animal_type == "LAC_COW" and standard == "NASEM":
        required.add("body_condition_score_5")
    if animal_type.startswith("HEIFER") and standard == "NRC":
        required |= {"body_condition_score_5", "days_born"}
    return "required" if key in required else "optional"


def fields_for(standard: str, animal_type: str) -> list[dict]:
    """Campos que a calculadora do padrão usa para o tipo de animal, na ordem de ``FIELDS``."""
    rows = []
    for spec in FIELDS:
        mode = usage(spec.key, standard, animal_type)
        if mode is None:
            continue
        rows.append(
            {
                "key": spec.key,
                "label": spec.label,
                "unit": spec.unit,
                "required": mode == "required",
                "min": spec.minimum,
                "max": spec.maximum,
                "integer": spec.integer,
                "choices": list(spec.choices),
                "group": spec.group,
            }
        )
    return rows
