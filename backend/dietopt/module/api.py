"""Corpos de resposta das rotas ``/api/module/*`` (FSD, Anexo B.7). O servidor só lê o pedido e chama estas funções."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

from ..standards import get_standard
from .categories import CATEGORY_ANIMAL_TYPES, CATEGORY_LABELS, constraints_for, parse_animal_type, parse_category
from .fields import fields_for
from .compare import TOLERANCE_PCT, build_report, report_csv
from .evaluate import evaluate_diets
from .requirements import REQUIREMENT_FIELDS, compute_requirements, rufas_diet_defaults

DEFAULT_STANDARD = "NASEM"  # padrão principal do módulo (o NRC é apoio)


def defaults_payload(standard: str | None, category: str | None, animal_type: str | None = None) -> dict[str, Any]:
    """Campos da vaca da categoria (unidade, obrigatoriedade, faixa), restrições aplicáveis e padrões do RuFaS."""
    nutrient_standard = get_standard(standard or DEFAULT_STANDARD)
    category_ = parse_category(category)
    animal = parse_animal_type(category_, animal_type)
    return {
        "standard": nutrient_standard.code,
        "category": category_.value,
        "label": CATEGORY_LABELS[category_],
        "animal_type": animal,
        "animal_types": list(CATEGORY_ANIMAL_TYPES[category_]),
        "fields": fields_for(nutrient_standard.code, animal),
        "diet_defaults": rufas_diet_defaults(),
        "requirement_fields": [
            {"key": key, "label": label, "unit": unit} for key, (label, unit) in REQUIREMENT_FIELDS.items()
        ],
        "constraints": [asdict(constraint) for constraint in constraints_for(nutrient_standard.code, animal)],
    }


def evaluate_payload(body: Mapping[str, Any]) -> dict[str, Any]:
    """Avaliação e ordenação das dietas informadas (FSD, Anexo B.7)."""
    return evaluate_diets(
        body.get("standard") or DEFAULT_STANDARD,
        body.get("category"),
        body.get("cow") or {},
        body.get("diets"),
        body.get("prices") or {},
        body.get("requirements_override"),
        body.get("limits"),
        body.get("animal_type"),
    )


def compare_payload(body: Mapping[str, Any]) -> dict[str, Any]:
    """Comparação do modelo linear com o RuFaS (FSD, Anexo B.8, fase 1), com o mesmo corpo da avaliação e ``tolerance_pct?``."""
    tolerance = body.get("tolerance_pct")
    report = build_report(evaluate_payload(body), TOLERANCE_PCT if tolerance in (None, "") else float(tolerance))
    return {**report, "csv": report_csv(report)}


def requirements_payload(body: Mapping[str, Any]) -> dict[str, Any]:
    """Exigências calculadas da vaca, com as sobrescritas do usuário."""
    result = compute_requirements(
        body.get("standard") or DEFAULT_STANDARD,
        body.get("category"),
        body.get("cow") or {},
        body.get("requirements_override"),
        body.get("animal_type"),
    )
    return result.to_dict()
