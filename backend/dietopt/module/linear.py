"""Modelo linear das restrições nutricionais do otimizador do RuFaS (LINEARIZACAO.md, seção 4).

Cada restrição vira ``oferta(x) = combinação de partes afins`` em ``x`` (kg de MS por dia de cada alimento), comparada com
uma exigência constante. As classes são:

* **L** (linear): consumo, cálcio, fósforo e limites por alimento: exatas.
* **E** (razão): FDN, FDN de forragem e gordura (% da MS): a oferta é ``Σ aᵢ·xᵢ / DMI_ref`` e o sinal da folga é exato em
  qualquer ``x`` porque a restrição equivale a ``Σ (aᵢ − c)·xᵢ ≥ 0`` (``homogeneous``).
* **A** (aproximada): energia e proteína metabolizável. Os coeficientes por alimento dependem de escalares globais da dieta
  (desconto de ingestão, taxas de passagem, consumo, amido total); ficam **congelados no ponto de referência** ``x_ref``.
  No ponto de referência a oferta linear é igual à do RuFaS; fora dele há erro (medido por ``evaluate``).

``min`` (proteína) e ``max`` (energia total do NRC) ficam como combinação das partes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Sequence

import numpy as np

from .categories import Constraint, constraints_for
from .rufas import rufas

PERCENT = 100.0  # GeneralConstants.FRACTION_TO_PERCENTAGE do RuFaS
# Constantes da oferta de proteína metabolizável e da energia do NASEM, como no RuFaS (nutrition_supply_calculator.py).
MICROBIAL_PER_TDN, MICROBIAL_PER_RDP, MICROBIAL_EFFICIENCY, ENDOGENOUS_PER_KG = 0.13, 0.85, 0.64, 0.4 * 11.8
METHANE_ENERGY, URINE_ENERGY = 13.28, 0.0146  # Mcal por kg de CH4; Mcal por g de N urinário


@dataclass(frozen=True)
class Piece:
    """Parte afim ``a·x + c``."""

    a: np.ndarray
    c: float = 0.0

    def at(self, x: np.ndarray) -> float:
        return float(self.a @ x + self.c)


@dataclass(frozen=True)
class LinearConstraint:
    id: str
    label: str
    unit: str
    kind: str  # L, E ou A
    sense: Literal["ge", "le"]  # oferta ≥ exigência, ou oferta ≤ exigência
    requirement: float
    pieces: tuple[Piece, ...] = ()
    combine: Literal["single", "min", "max"] = "single"
    homogeneous: np.ndarray | None = None  # classe E: coeficientes de ``Σ (aᵢ − c)·xᵢ ≥ 0`` (ou ``≤ 0``)
    unavailable: str | None = None  # motivo, quando falta um dado para calcular a oferta

    def supply(self, x: np.ndarray) -> float:
        values = [piece.at(x) for piece in self.pieces]
        return min(values) if self.combine == "min" else max(values) if self.combine == "max" else values[0]

    def slack(self, x: np.ndarray) -> float:
        diff = self.supply(x) - self.requirement
        return diff if self.sense == "ge" else -diff


@dataclass(frozen=True)
class Reference:
    """Escalares globais da dieta de referência, que os coeficientes de classe A congelam."""

    dmi: float
    discount: float  # desconto de ingestão do NRC (D)
    tdn_percentage: float
    concentrate_percentage: float
    total_starch: float  # kg; o RuFaS usa kg na digestibilidade da FDN do NASEM (LINEARIZACAO.md, 4.7)


def reference(feeds: Sequence[Any], x_ref: np.ndarray, body_weight: float) -> Reference:
    rf = rufas()
    in_ration = [rf.feed_in_ration(float(a), fd) for a, fd in zip(x_ref, feeds)]
    dmi = float(np.sum(x_ref))
    tdn = float(sum(a * fd.TDN for a, fd in zip(x_ref, feeds)) / dmi)
    conc = float(rf.supply._calculate_percentage_of_concentrates(in_ration, dmi))
    starch = float(sum(a * fd.starch * 0.01 for a, fd in zip(x_ref, feeds)))
    discount = float(rf.supply.calculate_nutrient_intake_discount(in_ration, body_weight))
    return Reference(dmi, discount, tdn, conc, starch)


def _one(feed: Any) -> list[Any]:
    return [rufas().feed_in_ration(1.0, feed)]


def _per_feed(feeds: Sequence[Any], func) -> np.ndarray:
    return np.array([func(fd) for fd in feeds], dtype=float)


def _energy_nrc(feeds: Sequence[Any], ref: Reference) -> dict[str, np.ndarray]:
    """Energia líquida por kg de cada alimento (manutenção, lactação, crescimento) com o desconto D congelado."""
    supply = rufas().supply
    out: dict[str, list[float]] = {"maintenance": [], "lactation": [], "growth": []}
    for fd in feeds:
        digestible = {fd.rufas_id: fd.DE * ref.discount}
        me = supply.calculate_actual_metabolizable_energy(_one(fd), digestible)
        out["maintenance"].append(supply.calculate_actual_maintenance_net_energy(_one(fd), me))
        out["lactation"].append(supply.calculate_actual_lactation_net_energy(_one(fd), me, digestible))
        out["growth"].append(supply.calculate_actual_growth_net_energy(_one(fd), me))
    return {k: np.array(v, dtype=float) for k, v in out.items()}


def _protein(feeds: Sequence[Any], ref: Reference, body_weight: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Coeficientes da PM: (via TDN, via PDR, PNDR digestível + endógena), por kg de cada alimento, com taxas congeladas."""
    supply = rufas().supply
    in_ration = [rufas().feed_in_ration(1.0, fd) for fd in feeds]
    rates = supply._calculate_protein_passage_rates(in_ration, ref.dmi, body_weight, ref.concentrate_percentage)
    rdp = supply._calculate_rumen_degradable_protein_percentages(in_ration, rates)
    rup = supply._calculate_rumen_undegradable_protein_percentages(in_ration, rdp)
    via_tdn = np.array([MICROBIAL_PER_TDN * 1000 * fd.TDN * ref.discount / PERCENT for fd in feeds])
    via_rdp = np.array([MICROBIAL_PER_RDP * 1000 * rdp[fd.rufas_id] / PERCENT for fd in feeds])
    rup_part = np.array([1000 * (rup[fd.rufas_id] / PERCENT) * (fd.dRUP / PERCENT) + ENDOGENOUS_PER_KG for fd in feeds])
    return via_tdn, via_rdp, rup_part


def build(
    standard: str,
    animal_type: str,
    feeds: Sequence[Any],
    x_ref: np.ndarray,
    requirements: Any,
    body_weight: float,
    pen: tuple[float, float] | None,
) -> list[LinearConstraint]:
    """Restrições do padrão e do tipo de animal, linearizadas em ``x_ref``.

    ``requirements`` é o ``NutritionRequirements`` do RuFaS (já com as sobrescritas); ``pen`` = (metano entérico em g/dia,
    nitrogênio urinário em kg/dia), só para a energia do NASEM.
    """
    return build_at(standard, animal_type, feeds, reference(feeds, x_ref, body_weight), requirements, body_weight, pen)


def build_at(
    standard: str,
    animal_type: str,
    feeds: Sequence[Any],
    ref: Reference,
    requirements: Any,
    body_weight: float,
    pen: tuple[float, float] | None,
) -> list[LinearConstraint]:
    """Como ``build``, mas com os escalares globais dados (``Reference``): é o que a otimização usa para parametrizá-los."""
    rf = rufas()
    const = rf.constants
    n = len(feeds)
    ones = np.ones(n)
    ndf = _per_feed(feeds, lambda fd: fd.NDF)
    ee = _per_feed(feeds, lambda fd: fd.EE)
    forage = _per_feed(feeds, lambda fd: rf.supply.calculate_forage_neutral_detergent_fiber_content(_one(fd)) * PERCENT)
    calcium = _per_feed(feeds, lambda fd: rf.supply.calculate_calcium_supply(_one(fd)))
    phosphorus = _per_feed(feeds, lambda fd: rf.supply.calculate_phosphorus_supply(_one(fd)))
    energy = _energy_nrc(feeds, ref) if standard == "NRC" else None
    via_tdn = via_rdp = rup_part = None
    nasem_digestible = None
    if standard == "NASEM":
        nasem_digestible = _per_feed(
            feeds,
            lambda fd: rf.supply.calculate_NASEM_digestible_energy(_one(fd), ref.dmi, body_weight, ref.total_starch),
        )
    via_tdn, via_rdp, rup_part = _protein(feeds, ref, body_weight)

    req = requirements
    cap = const.DMI_CONSTRAINT_FRACTION
    constraints: dict[str, LinearConstraint] = {}

    def add(constraint: LinearConstraint) -> None:
        constraints[constraint.id] = constraint

    add(LinearConstraint("dmi_min", "", "kg/dia", "L", "ge", req.dry_matter * (1 - cap), (Piece(ones),)))
    add(LinearConstraint("dmi_max", "", "kg/dia", "L", "le", req.dry_matter * (1 + cap), (Piece(ones),)))
    add(LinearConstraint("calcium", "", "g/dia", "L", "ge", req.calcium, (Piece(calcium),)))
    add(LinearConstraint("phosphorus", "", "g/dia", "L", "ge", max(req.phosphorus, req.process_based_phosphorus), (Piece(phosphorus),)))
    for cid, sense, values, limit in (
        ("ndf_min", "ge", ndf, const.MINIMUM_RATION_NDF),
        ("ndf_max", "le", ndf, const.MAXIMUM_RATION_NDF),
        ("forage_ndf", "ge", forage, const.MINIMUM_RATION_FORAGE_NDF),
        ("fat", "le", ee, const.MAXIMUM_RATION_FAT),
    ):
        add(LinearConstraint(cid, "", "% da MS", "E", sense, limit, (Piece(values / ref.dmi),), homogeneous=values - limit))
    if energy is not None:
        add(LinearConstraint("ne_maintenance", "", "Mcal/dia", "A", "ge", req.maintenance_energy + req.activity_energy, (Piece(energy["maintenance"]),)))
        add(LinearConstraint("ne_growth", "", "Mcal/dia", "A", "ge", req.growth_energy, (Piece(energy["growth"]),)))
        add(LinearConstraint("ne_lactation", "", "Mcal/dia", "A", "ge", req.lactation_energy + req.pregnancy_energy, (Piece(energy["lactation"]),)))
        pieces = tuple(Piece(energy[k]) for k in ("maintenance", "growth", "lactation"))
        add(LinearConstraint("ne_total", "", "Mcal/dia", "A", "ge", req.total_energy_requirement, pieces, combine="max"))
    else:
        missing = None if pen is not None else "Informe o metano entérico e o nitrogênio urinário do lote (LINEARIZACAO.md, 7.3)."
        constant = 0.0 if pen is None else -const.EFF_OF_ME_USE * (METHANE_ENERGY * pen[0] * 0.001 + URINE_ENERGY * pen[1] * 1000)
        add(
            LinearConstraint(
                "ne_nasem", "", "Mcal/dia", "A", "ge", req.total_energy_requirement,
                (Piece(const.EFF_OF_ME_USE * nasem_digestible, constant),), unavailable=missing,
            )  # fmt: skip
        )
    protein = (
        Piece(MICROBIAL_EFFICIENCY * via_tdn + rup_part),
        Piece(MICROBIAL_EFFICIENCY * via_rdp + rup_part),
    )
    add(LinearConstraint("protein_min", "", "g/dia", "A", "ge", req.metabolizable_protein, protein, combine="min"))
    add(
        LinearConstraint(
            "protein_max", "", "g/dia", "A", "le", req.metabolizable_protein * const.PROTEIN_UPPER_LIMIT_FACTOR, protein, combine="min"
        )
    )
    # Ordem e rótulos vêm da lista de restrições da categoria (``constraints_for``).
    ordered = []
    for constraint in constraints_for(standard, animal_type):
        found = constraints[constraint.id]
        ordered.append(_labelled(found, constraint))
    return ordered


def _labelled(found: LinearConstraint, spec: Constraint) -> LinearConstraint:
    from dataclasses import replace

    return replace(found, label=spec.label)
