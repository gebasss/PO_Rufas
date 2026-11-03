"""Avaliação de dietas já montadas para uma vaca (FSD, Anexo B.6): custo, oferta e folga de cada restrição, erro de
linearização e ordenação da menos para a mais recomendada.

Para cada dieta, as exigências são calculadas com a própria dieta como "ração anterior" (TDN, FDN e energia), as restrições
são linearizadas na dieta (``linear.build``) e a oferta original vem das próprias funções de restrição do otimizador do
RuFaS (``RationOptimizer``), de modo que a identidade no ponto de referência é verificável.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import numpy as np

from ..feeds import feed_library
from ..standards import get_standard, library_ids
from . import linear
from .categories import constraints_for, parse_animal_type, parse_category
from .fields import DIET_FIELDS
from .library import build_feeds
from .requirements import RequirementsResult, compute_requirements
from .rufas import rufas

MAX_DIETS = 10  # (a confirmar com o professor; FSD B.4)
PERTURBATION = (0.95, 1.05)  # quantidades escaladas para medir o erro de linearização fora do ponto; erro relativo à oferta original (LINEARIZACAO.md, 6 e 10)
BINDING_MARGIN = 0.005  # "no limite": folga de até 0,5% da exigência
VIOLATION_TOLERANCE = 1e-9


@dataclass(frozen=True)
class Diet:
    name: str
    amounts: dict[int, float]  # id do RuFaS -> kg de MS por dia


def parse_diets(raw: Any, standard: str) -> tuple[list[Diet], list[str]]:
    """Valida as dietas; alimentos fora da biblioteca do padrão são removidos, com aviso (FSD B.4)."""
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)) or not raw:
        raise ValueError("Informe ao menos uma dieta")
    if len(raw) > MAX_DIETS:
        raise ValueError(f"No máximo {MAX_DIETS} dietas por avaliação")
    known = library_ids(standard)
    diets: list[Diet] = []
    warnings: list[str] = []
    for index, item in enumerate(raw, 1):
        name = str(item.get("name") or "").strip()
        if not name:
            raise ValueError(f"Dieta {index}: informe o nome")
        if any(d.name == name for d in diets):
            raise ValueError(f"Nome de dieta repetido: {name!r}")
        amounts: dict[int, float] = {}
        removed = []
        for key, value in (item.get("amounts") or {}).items():
            feed_id = int(key)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0 or not np.isfinite(value):
                raise ValueError(f"Dieta {name!r}, alimento {feed_id}: quantidade deve ser um número maior ou igual a zero")
            if feed_id not in known:
                removed.append(feed_id)
            elif value > 0:
                amounts[feed_id] = float(value)
        if removed:
            warnings.append(f"Dieta {name!r}: removidos por não existirem no padrão {standard}: {sorted(removed)}.")
        if not amounts:
            raise ValueError(f"Dieta {name!r}: sem alimentos com quantidade maior que zero na biblioteca {standard}")
        diets.append(Diet(name, amounts))
    return diets, warnings


def resolve_limits(standard: str, feed_ids: Sequence[int], given: Mapping[Any, Any] | None) -> dict[int, tuple[float, float]]:
    """Limites de inclusão (kg MS/dia): os informados ou os tetos padrão do alimento (FSD 14.2)."""
    library = feed_library(standard)
    given = {int(k): v for k, v in (given or {}).items()}
    out = {}
    for feed_id in feed_ids:
        low, high = given.get(feed_id) or (0.0, library[feed_id].default_max)
        low, high = float(low), float(high)
        if low < 0 or high < low:
            raise ValueError(f"Alimento {feed_id}: limites inválidos ({low:g} a {high:g})")
        out[feed_id] = (low, high)
    return out


def _derived_inputs(standard: str, feeds: Sequence[Any], x: np.ndarray, body_weight: float) -> dict[str, float]:
    """Valores da ração anterior (TDN, energia, FDN) calculados da própria dieta, como o RuFaS faz com a ração do dia anterior."""
    rf = rufas()
    dmi = float(x.sum())
    out: dict[str, float] = {}
    if standard == "NRC":
        ref = linear.reference(feeds, x, body_weight)
        out["tdn_percentage"] = float(sum(a * fd.TDN for a, fd in zip(x, feeds)) / dmi)
        total_me = 0.0
        for amount, fd in zip(x, feeds):
            me = rf.supply.calculate_actual_metabolizable_energy(
                [rf.feed_in_ration(1.0, fd)], {fd.rufas_id: fd.DE * ref.discount}
            )
            total_me += amount * me[fd.rufas_id]
        out["net_energy_diet_concentration"] = float(total_me / dmi)
    else:
        out["ndf_percentage"] = float(sum(a * fd.NDF for a, fd in zip(x, feeds)) / dmi)
    return out


def classify_slack(slack: float, requirement: float) -> str:
    scale = max(abs(requirement), 1e-9)
    if slack < -VIOLATION_TOLERANCE * max(scale, 1.0):
        return "violada"
    return "no_limite" if slack <= BINDING_MARGIN * scale else "ok"


def _nonlinear_supply(spec_name: str, constraint: linear.LinearConstraint, x: np.ndarray, config: Any) -> float:
    slack = float(getattr(rufas().optimizer, spec_name)(x, config))
    return slack + constraint.requirement if constraint.sense == "ge" else constraint.requirement - slack


def evaluate_diet(
    standard: str,
    category: str,
    animal_type: str,
    cow: Mapping[str, Any],
    overrides: Mapping[str, Any] | None,
    diet: Diet,
    prices: Mapping[int, float],
    limits: Mapping[int, tuple[float, float]],
    pen: tuple[float, float] | None,
    fixed: RequirementsResult | None = None,
) -> dict[str, Any]:
    """Avalia uma dieta. Com ``fixed``, usa essas exigências (as da otimização) em vez de calcular as da própria dieta."""
    rf = rufas()
    ids = sorted(diet.amounts)
    feeds = build_feeds(standard, ids, prices, limits)
    x = np.array([diet.amounts[i] for i in ids], dtype=float)
    body_weight = float(cow["body_weight"])

    if fixed is None:
        derived = _derived_inputs(standard, feeds, x, body_weight)
        cow_for_diet = {**{k: v for k, v in derived.items() if k in DIET_FIELDS[standard]}, **{k: v for k, v in cow.items() if v not in (None, "")}}
        required = compute_requirements(standard, category, cow_for_diet, overrides, animal_type)
    else:
        required = fixed
    nutrition = required.nutrition_requirements

    config = rf.ration_config(
        nutrient_standard=rf.standard[standard],
        animal_requirements=nutrition,
        pen_available_feeds=feeds,
        initial_dry_matter_requirement=nutrition.dry_matter,
        initial_protein_requirement=nutrition.metabolizable_protein,
        pen_average_body_weight=body_weight,
        pen_average_enteric_methane=pen[0] if pen else None,
        pen_average_urine_nitrogen=pen[1] if pen else None,
    )
    constraints = linear.build(standard, animal_type, feeds, x, nutrition, body_weight, pen)
    specs = {spec.id: spec for spec in constraints_for(standard, animal_type)}

    rows: list[dict[str, Any]] = []
    violation = 0.0
    for constraint in constraints:
        if constraint.unavailable:
            rows.append({**_base_row(constraint), "status": "indisponivel", "note": constraint.unavailable})
            continue
        supply_linear = constraint.supply(x)
        supply_nonlinear = _nonlinear_supply(specs[constraint.id].rufas_name, constraint, x, config)
        probes = []
        if constraint.kind == "A":  # erro fora do ponto: coeficientes congelados em x, quantidades escaladas
            for scale in PERTURBATION:
                moved = x * scale
                probes.append(
                    {
                        "scale": scale,
                        "supply_linear": float(constraint.supply(moved)),
                        "supply_nonlinear": float(_nonlinear_supply(specs[constraint.id].rufas_name, constraint, moved, config)),
                    }
                )
        error = max((abs(p["supply_linear"] - p["supply_nonlinear"]) / max(abs(p["supply_nonlinear"]), 1e-9) * 100 for p in probes), default=0.0)
        rows.append(_report(constraint, supply_linear, supply_nonlinear, error, probes))
        violation += _shortfall(constraint, supply_linear)

    for feed_id, amount in zip(ids, x):
        low, high = limits[feed_id]
        for bound, sense, label in ((low, "ge", "mínimo"), (high, "le", "máximo")):
            if sense == "ge" and bound <= 0:
                continue
            limit = linear.LinearConstraint(
                f"limit_{sense}_{feed_id}", f"Limite {label} do alimento {feed_id}", "kg/dia", "L", sense, bound, (linear.Piece(np.eye(len(ids))[ids.index(feed_id)]),)
            )
            row = _report(limit, float(amount), float(amount), 0.0)
            rows.append(row)
            violation += _shortfall(limit, float(amount))

    cost = float(sum(prices[i] * a for i, a in zip(ids, x)))
    reference = linear.reference(feeds, x, body_weight)
    violated = [r["id"] for r in rows if r["status"] == "violada"]
    unavailable = [r["id"] for r in rows if r["status"] == "indisponivel"]
    warnings = list(required.warnings)
    if standard == "NRC" and 58.0 <= reference.tdn_percentage <= 62.0:
        warnings.append(
            f"TDN de {reference.tdn_percentage:.1f}%: perto de 60% o desconto de ingestão do NRC é descontínuo; "
            "pequenas variações da dieta mudam muito a energia ofertada."
        )
    if unavailable:
        warnings.append("Restrições sem cálculo por falta de dados: " + ", ".join(unavailable) + ".")
    return {
        "name": diet.name,
        "cost": cost,
        "cost_per_kg": cost / float(x.sum()),
        "feasible": not violated,
        "violation": violation,
        "violated": violated,
        "incomplete": bool(unavailable),
        "intake": {
            "dry_matter": float(x.sum()),
            "tdn_percentage": reference.tdn_percentage,
            "concentrate_percentage": reference.concentrate_percentage,
            "intake_discount": reference.discount if standard == "NRC" else None,
            "total_starch_kg": reference.total_starch if standard == "NASEM" else None,
        },
        "requirements": required.requirements,
        "constraints": rows,
        "warnings": warnings,
    }


def _base_row(constraint: linear.LinearConstraint) -> dict[str, Any]:
    return {
        "id": constraint.id,
        "label": constraint.label,
        "unit": constraint.unit,
        "kind": constraint.kind,
        "sense": constraint.sense,
        "requirement": constraint.requirement,
    }


def _report(
    constraint: linear.LinearConstraint,
    supply_linear: float,
    supply_nonlinear: float,
    error_pct: float,
    probes: Sequence[Mapping[str, float]] = (),
) -> dict[str, Any]:
    slack = supply_linear - constraint.requirement if constraint.sense == "ge" else constraint.requirement - supply_linear
    return {
        **_base_row(constraint),
        "supply_linear": float(supply_linear),
        "supply_nonlinear": float(supply_nonlinear),
        "error_pct": float(error_pct),
        "slack": float(slack),
        "status": classify_slack(slack, constraint.requirement),
        "probes": [dict(p) for p in probes],  # ofertas com as quantidades escaladas (só classe A), para a comparação com o RuFaS
    }


def _shortfall(constraint: linear.LinearConstraint, supply: float) -> float:
    """Falta normalizada pela exigência (0 se cumprida)."""
    slack = supply - constraint.requirement if constraint.sense == "ge" else constraint.requirement - supply
    return max(0.0, -slack) / max(abs(constraint.requirement), 1e-9)


def rank(diets: Sequence[Mapping[str, Any]]) -> tuple[list[str], str | None]:
    """Da menos para a mais recomendada: inviáveis por violação decrescente, depois viáveis por custo decrescente."""
    infeasible = sorted((d for d in diets if not d["feasible"]), key=lambda d: -d["violation"])
    feasible = sorted((d for d in diets if d["feasible"]), key=lambda d: -d["cost"])
    ordered = [d["name"] for d in infeasible + feasible]
    return ordered, (feasible[-1]["name"] if feasible else None)


def pen_inputs(standard: str, cow: Mapping[str, Any]) -> tuple[float, float] | None:
    methane, nitrogen = cow.get("enteric_methane"), cow.get("urinary_nitrogen")
    if standard != "NASEM" or (methane in (None, "") and nitrogen in (None, "")):
        return None
    if methane in (None, "") or nitrogen in (None, ""):
        raise ValueError("Informe os dois: metano entérico e nitrogênio urinário do lote (ou nenhum)")
    return float(methane), float(nitrogen)


def evaluate_diets(
    standard: str | None,
    category: str | None,
    cow: Mapping[str, Any],
    diets: Any,
    prices: Mapping[Any, Any],
    overrides: Mapping[str, Any] | None = None,
    limits: Mapping[Any, Any] | None = None,
    animal_type: str | None = None,
) -> dict[str, Any]:
    nutrient_standard = get_standard(standard).code
    category_ = parse_category(category)
    animal = parse_animal_type(category_, animal_type)
    parsed, warnings = parse_diets(diets, nutrient_standard)
    used = sorted({i for diet in parsed for i in diet.amounts})
    price_map = {int(k): float(v) for k, v in (prices or {}).items()}
    missing = [i for i in used if i not in price_map]
    if missing:
        raise ValueError(f"Informe o preço (US$/kg MS) dos alimentos: {missing}")
    if any(p < 0 for p in price_map.values()):
        raise ValueError("Os preços devem ser maiores ou iguais a zero")
    limit_map = resolve_limits(nutrient_standard, used, limits)
    pen = pen_inputs(nutrient_standard, cow)

    baseline = compute_requirements(nutrient_standard, category_.value, cow, overrides, animal)
    results = [
        evaluate_diet(nutrient_standard, category_.value, animal, cow, overrides, diet, price_map, limit_map, pen)
        for diet in parsed
    ]
    if nutrient_standard == "NASEM":
        warnings += [
            "Replicado do RuFaS: o amido total entra em kg (e não em % da MS) na digestibilidade da FDN; a oferta de "
            "proteína segue o método do NRC; a FDN da ração anterior vai às exigências como fração.",
        ]
    ordered, best = rank(results)
    return {
        "standard": nutrient_standard,
        "category": category_.value,
        "animal_type": animal,
        "requirements": baseline.requirements,
        "requirement_warnings": baseline.warnings,
        "diets": results,
        "ranking": ordered,
        "best": best,
        "warnings": warnings,
    }
