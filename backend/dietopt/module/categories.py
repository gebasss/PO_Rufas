"""Categorias que o RuFaS otimiza e as restrições que valem em cada uma (LINEARIZACAO.md, seções 2 e 3.1)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping


class Category(str, Enum):
    LAC_COW = "LAC_COW"  # vaca em lactação
    CLOSE_UP = "CLOSE_UP"  # vaca seca e novilha pré-parto
    GROWING = "GROWING"  # novilhas I e II


# Tipos de animal do RuFaS (``AnimalType``) de cada categoria; o primeiro é o padrão.
CATEGORY_ANIMAL_TYPES: Mapping[Category, tuple[str, ...]] = MappingProxyType(
    {
        Category.LAC_COW: ("LAC_COW",),
        Category.CLOSE_UP: ("DRY_COW", "HEIFER_III"),
        Category.GROWING: ("HEIFER_II", "HEIFER_I"),
    }
)

CATEGORY_LABELS: Mapping[Category, str] = MappingProxyType(
    {
        Category.LAC_COW: "Vaca em lactação",
        Category.CLOSE_UP: "Vaca seca e novilha pré-parto",
        Category.GROWING: "Novilha em crescimento",
    }
)


def parse_category(value: str | None) -> Category:
    try:
        return Category(value)
    except ValueError:
        raise ValueError(f"Categoria desconhecida: {value!r} (use {', '.join(c.value for c in Category)})") from None


def parse_animal_type(category: Category, value: str | None) -> str:
    """Tipo de animal pedido (``None`` vale o padrão da categoria); precisa pertencer à categoria."""
    types = CATEGORY_ANIMAL_TYPES[category]
    if value is None:
        return types[0]
    if value not in types:
        raise ValueError(f"Tipo de animal {value!r} não pertence à categoria {category.value} (use {', '.join(types)})")
    return value


@dataclass(frozen=True)
class Constraint:
    id: str
    label: str
    rufas_name: str  # função de restrição do otimizador do RuFaS
    kind: str  # classe de linearização: L, E ou A (LINEARIZACAO.md, seção 4)


def constraints_for(standard: str, animal_type: str) -> list[Constraint]:
    """Restrições nutricionais do otimizador do RuFaS para o padrão e o tipo de animal."""
    common = [
        Constraint("dmi", "Consumo de matéria seca", "DMI_constraint_lower/upper", "L"),
        Constraint("calcium", "Cálcio", "calcium_constraint", "L"),
        Constraint("phosphorus", "Fósforo", "phosphorus_constraint", "L"),
        Constraint("ndf_min", "FDN total mínima", "NDF_constraint_lower", "E"),
        Constraint("ndf_max", "FDN total máxima", "NDF_constraint_upper", "E"),
        Constraint("forage_ndf", "FDN de forragem mínima", "forage_NDF_constraint", "E"),
        Constraint("fat", "Gordura máxima", "fat_constraint", "E"),
    ]
    if standard == "NASEM":
        energy = [Constraint("ne_nasem", "Energia líquida (NASEM)", "NASEM_net_energy_constraint", "A")]
    else:
        energy = [
            Constraint("ne_maintenance", "Energia de mantença e atividade", "NE_maintenance_and_activity_constraint", "A"),
            Constraint("ne_growth", "Energia de crescimento", "NE_growth_constraint", "A"),
        ]
        if animal_type == "LAC_COW":  # novilhas e vacas secas não têm NE_lactation nem NE_total no modo NRC
            energy += [
                Constraint("ne_lactation", "Energia de lactação", "NE_lactation_constraint", "A"),
                Constraint("ne_total", "Energia total (maior das três ofertas)", "NE_total_constraint", "A"),
            ]
    protein = [
        Constraint("protein_min", "Proteína metabolizável mínima", "protein_constraint_lower", "A"),
        Constraint("protein_max", "Proteína metabolizável máxima", "protein_constraint_upper", "A"),
    ]
    return common + energy + protein
