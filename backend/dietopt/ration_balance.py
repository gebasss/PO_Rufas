"""Balanço nutricional da ração obtida na simulação (RF-19): oferta × exigência de energia, proteína, cálcio, fósforo, consumo e fibra.

Os números vêm do próprio RuFaS: ``NutritionEvaluator`` calcula, a cada intervalo de formulação, a diferença entre a oferta
da ração e a exigência média do lote; a simulação as guarda (``avg_eval_results_for_LAC_COW``) e este módulo as resume
(média dos intervalos e o pior intervalo). Convenções do RuFaS, por nutriente:

* energia (total, mantença com atividade, lactação com gestação, crescimento), cálcio e fósforo: oferta − exigência
  (negativa = déficit);
* proteína metabolizável e consumo: 0 se estiver na faixa aceita (de 1 a 1,5 × a exigência; de 0,7 a 1,3 × o estimado),
  senão a distância até o limite violado (negativa abaixo, positiva acima);
* FDN total: 0 entre 25% e 45%, senão a distância (pontos percentuais); FDN de forragem: % − 15; gordura: 7 − %.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Any, Mapping, Sequence

TOLERANCE = 1e-3  # a otimização do RuFaS deixa a FDN em 45,0000006%


@dataclass(frozen=True)
class Row:
    """Uma linha do balanço: como ler a diferença do RuFaS e a exigência (ou limite) a que ela se refere."""

    id: str
    label: str
    unit: str
    difference: str  # chave de ``avg_eval_results_for_LAC_COW``
    kind: str  # "surplus": oferta − exigência; "range": 0 dentro da faixa; "floor": % − mínimo; "ceiling": máximo − %
    requirement: tuple[str, ...] = ()  # chaves de ``avg_rqmts_for_LAC_COW`` somadas
    note: str = ""


ROWS: tuple[Row, ...] = (
    Row("total_energy", "Energia total", "Mcal/dia", "total_energy_difference", "surplus",
        ("NEmaint_requirement", "NEa_requirement", "NEg_requirement", "NEpreg_requirement", "NEl_requirement")),
    Row("maintenance_energy", "Energia de mantença e atividade", "Mcal/dia", "maintenance_energy_difference", "surplus",
        ("NEmaint_requirement", "NEa_requirement")),
    Row("lactation_energy", "Energia de lactação e gestação", "Mcal/dia", "lactation_energy_difference", "surplus",
        ("NEl_requirement", "NEpreg_requirement")),
    Row("growth_energy", "Energia de crescimento", "Mcal/dia", "growth_energy_difference", "surplus", ("NEg_requirement",)),
    Row("metabolizable_protein", "Proteína metabolizável", "g/dia", "metabolizable_protein_difference", "range",
        ("MP_requirement",), "Aceita de 1 a 1,5 vezes a exigência."),
    Row("calcium", "Cálcio", "g/dia", "calcium_difference", "surplus", ("Ca_requirement",)),
    Row("phosphorus", "Fósforo", "g/dia", "phosphorus_difference", "surplus", ("P_req",),
        "A exigência é a maior entre a de fósforo e a do processo."),
    Row("dry_matter", "Consumo de matéria seca", "kg/dia", "dry_matter_difference", "range", ("DMIest_requirement",),
        "Aceito de 0,7 a 1,3 vezes o consumo estimado (a exigência mostrada é o estimado)."),
    Row("ndf", "FDN total", "% da MS", "ndf_percent_difference", "range", (), "Aceita de 25% a 45%."),
    Row("forage_ndf", "FDN de forragem", "% da MS", "forage_ndf_percent_difference", "floor", (), "Mínimo de 15%."),
    Row("fat", "Gordura", "% da MS", "fat_percent_difference", "ceiling", (), "Máximo de 7%."),
)  # fmt: skip


def _requirement(row: Row, requirements: Mapping[str, Any]) -> float | None:
    if not row.requirement:
        return None
    values = [requirements.get(key) for key in row.requirement]
    if any(v is None for v in values):
        return None
    total = float(sum(values))
    if row.id == "phosphorus":
        total = max(total, float(requirements.get("P_req_process") or 0.0))
    return total


def _status(row: Row, difference: float) -> str:
    """``ok`` ou ``deficit`` (energia, cálcio, fósforo, FDN de forragem, gordura) ou ``fora`` (faixa)."""
    if row.kind == "range":
        return "ok" if abs(difference) <= TOLERANCE else "fora"
    return "ok" if difference >= -TOLERANCE else "deficit"


def build_balance(
    evaluations: Sequence[Mapping[str, Any]],
    requirements: Sequence[Mapping[str, Any]],
    observed: Mapping[str, float] | None = None,
) -> list[dict[str, Any]]:
    """Linhas do balanço (média dos intervalos e pior intervalo); vazio se o RuFaS não devolveu a avaliação.

    ``observed`` traz os valores da ração média onde a oferta não sai da diferença (``dry_matter``, ``ndf``,
    ``forage_ndf`` e ``fat``, em kg ou % da MS).
    """
    out: list[dict[str, Any]] = []
    for row in ROWS:
        pairs = [(e, r) for e, r in zip(evaluations, requirements) if e.get(row.difference) is not None]
        if not pairs:
            continue
        differences = [float(e[row.difference]) for e, _ in pairs]
        needs = [_requirement(row, r) for _, r in pairs]
        requirement = mean(n for n in needs if n is not None) if all(n is not None for n in needs) and needs else None
        # "Pior" = a diferença mais desfavorável: a menor (déficit) ou, nas faixas, a mais distante de zero.
        worst = max(differences, key=abs) if row.kind == "range" else min(differences)
        average = mean(differences)
        item: dict[str, Any] = {
            "id": row.id,
            "label": row.label,
            "unit": row.unit,
            "kind": row.kind,
            "requirement": requirement,
            "difference": average,
            "worst_difference": worst,
            "status": _status(row, worst),
            "note": row.note,
        }
        if requirement is not None and row.kind == "surplus":
            item["supply"] = requirement + average
            item["margin_pct"] = average / requirement * 100 if requirement else None
        elif observed and row.id in observed:
            item["supply"] = observed[row.id]
        out.append(item)
    return out
