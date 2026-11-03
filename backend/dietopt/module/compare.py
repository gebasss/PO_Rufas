"""Comparação do modelo linear com o RuFaS, fase 1 (FSD, Anexo B.8; LINEARIZACAO.md, seção 6).

Para a mesma vaca, o mesmo lote e a mesma dieta, compara a oferta e a folga de cada restrição **linearizada** com a **original**
do RuFaS (as funções de restrição do ``RationOptimizer``). O relatório é calculado sobre o resultado de ``evaluate_diets``
(função pura): erro no ponto de referência, erro com as quantidades de −5% a +5% (classe A, coeficientes congelados), conferência
do estado (viável ou violada) e resumo por dieta e geral, contra uma tolerância em % da oferta original.
"""

from __future__ import annotations

import csv
import io
from typing import Any, Mapping

from .evaluate import PERTURBATION, classify_slack

TOLERANCE_PCT = 1.0  # LINEARIZACAO.md, seção 6 (a confirmar com o professor: L-Q1)
IDENTITY_TOLERANCE = 1e-6  # B.9-1: no ponto de referência a oferta linear é igual à original
LIMIT_PREFIX = "limit_"  # limites por alimento são dados do usuário, sem função equivalente no RuFaS

CSV_COLUMNS = (
    "dieta", "restricao_id", "restricao", "unidade", "classe", "sentido", "exigencia", "oferta_linear", "oferta_rufas",
    "folga_linear", "folga_rufas", "erro_no_ponto_pct",
    *(f"erro_x{scale:g}_pct" for scale in PERTURBATION),
    "erro_max_pct", "dentro_da_tolerancia", "estado_linear", "estado_rufas", "mesmo_estado_nas_sondas",
)  # fmt: skip


def _error_pct(supply_linear: float, supply_original: float) -> float:
    """Erro com sinal da oferta linear, em % da oferta original."""
    return (supply_linear - supply_original) / max(abs(supply_original), 1e-9) * 100


def _slack(sense: str, supply: float, requirement: float) -> float:
    return supply - requirement if sense == "ge" else requirement - supply


def _violated(sense: str, supply: float, requirement: float) -> bool:
    return classify_slack(_slack(sense, supply, requirement), requirement) == "violada"


def compare_row(row: Mapping[str, Any], tolerance_pct: float) -> dict[str, Any]:
    """Compara uma restrição já avaliada; as indisponíveis ficam de fora dos números, com a nota do que falta."""
    base = {key: row[key] for key in ("id", "label", "unit", "kind", "sense", "requirement")}
    if row["status"] == "indisponivel":
        return {**base, "status_linear": "indisponivel", "note": row.get("note")}
    sense, requirement = row["sense"], row["requirement"]
    linear_supply, original = row["supply_linear"], row["supply_nonlinear"]
    probes = [
        {
            "scale": probe["scale"],
            "supply_linear": probe["supply_linear"],
            "supply_original": probe["supply_nonlinear"],
            "slack_linear": _slack(sense, probe["supply_linear"], requirement),
            "slack_original": _slack(sense, probe["supply_nonlinear"], requirement),
            "error_pct": _error_pct(probe["supply_linear"], probe["supply_nonlinear"]),
            "same_state": _violated(sense, probe["supply_linear"], requirement) == _violated(sense, probe["supply_nonlinear"], requirement),
        }
        for probe in row["probes"]
    ]
    point_error = _error_pct(linear_supply, original)
    max_error = max([abs(point_error), *(abs(p["error_pct"]) for p in probes)])
    return {
        **base,
        "supply_linear": linear_supply,
        "supply_original": original,
        "slack_linear": row["slack"],
        "slack_original": _slack(sense, original, requirement),
        "point_error_pct": point_error,
        "probes": probes,
        "max_error_pct": max_error,
        "within_tolerance": max_error <= tolerance_pct,
        "identity_ok": abs(linear_supply - original) <= IDENTITY_TOLERANCE * max(1.0, abs(original)),
        "status_linear": row["status"],
        "status_original": classify_slack(_slack(sense, original, requirement), requirement),
        "same_state_in_probes": all(p["same_state"] for p in probes),
    }


def compare_diet(diet: Mapping[str, Any], tolerance_pct: float) -> dict[str, Any]:
    rows = [compare_row(row, tolerance_pct) for row in diet["constraints"] if not row["id"].startswith(LIMIT_PREFIX)]
    compared = [row for row in rows if "max_error_pct" in row]
    worst = max(compared, key=lambda row: row["max_error_pct"], default=None)
    return {
        "name": diet["name"],
        "feasible": diet["feasible"],
        "incomplete": diet["incomplete"],
        "n_compared": len(compared),
        "n_unavailable": len(rows) - len(compared),
        "max_error_pct": worst["max_error_pct"] if worst else 0.0,
        "worst_constraint": {"id": worst["id"], "label": worst["label"]} if worst else None,
        "n_above_tolerance": sum(not row["within_tolerance"] for row in compared),
        "within_tolerance": all(row["within_tolerance"] for row in compared),
        "identity_ok": all(row["identity_ok"] for row in compared),
        "same_state_in_probes": all(row["same_state_in_probes"] for row in compared),
        "intake": diet["intake"],
        "constraints": rows,
    }


def build_report(evaluation: Mapping[str, Any], tolerance_pct: float = TOLERANCE_PCT) -> dict[str, Any]:
    """Relatório de comparação linear × RuFaS a partir do resultado de ``evaluate_diets``."""
    if tolerance_pct < 0:
        raise ValueError("A tolerância deve ser maior ou igual a zero")
    diets = [compare_diet(diet, tolerance_pct) for diet in evaluation["diets"]]
    worst = max(diets, key=lambda diet: diet["max_error_pct"], default=None)
    return {
        "standard": evaluation["standard"],
        "category": evaluation["category"],
        "animal_type": evaluation["animal_type"],
        "tolerance_pct": tolerance_pct,
        "scales": list(PERTURBATION),
        "diets": diets,
        "summary": {
            "n_diets": len(diets),
            "n_compared": sum(diet["n_compared"] for diet in diets),
            "max_error_pct": worst["max_error_pct"] if worst else 0.0,
            "worst": {"diet": worst["name"], **worst["worst_constraint"]} if worst and worst["worst_constraint"] else None,
            "n_above_tolerance": sum(diet["n_above_tolerance"] for diet in diets),
            "n_diets_above_tolerance": sum(not diet["within_tolerance"] for diet in diets),
            "identity_ok": all(diet["identity_ok"] for diet in diets),
            "same_state_in_probes": all(diet["same_state_in_probes"] for diet in diets),
        },
        "warnings": list(evaluation["warnings"]),
    }


def _num(value: float | None) -> str:
    return "" if value is None else f"{value:.6g}"


def report_csv(report: Mapping[str, Any]) -> str:
    """Uma linha por dieta e restrição comparada (vírgula como separador, ponto decimal)."""
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(CSV_COLUMNS)
    scales = report["scales"]
    for diet in report["diets"]:
        for row in diet["constraints"]:
            if "max_error_pct" not in row:
                continue
            by_scale = {p["scale"]: p["error_pct"] for p in row["probes"]}
            writer.writerow(
                [
                    diet["name"], row["id"], row["label"], row["unit"], row["kind"], row["sense"], _num(row["requirement"]),
                    _num(row["supply_linear"]), _num(row["supply_original"]), _num(row["slack_linear"]), _num(row["slack_original"]),
                    _num(row["point_error_pct"]),
                    *(_num(by_scale.get(scale)) for scale in scales),
                    _num(row["max_error_pct"]), "sim" if row["within_tolerance"] else "não", row["status_linear"], row["status_original"],
                    "sim" if row["same_state_in_probes"] else "não",
                ]
            )  # fmt: skip
    return out.getvalue()
