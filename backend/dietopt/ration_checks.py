"""Verificações de consistência da ração obtida na simulação (RF-27; FSD, Anexo A.4).

As verificações só **informam**: não mudam margem, custo nem ração. Cada uma devolve ``{id, label, status, value, limit,
detail}`` com ``status`` em ``ok``, ``warn`` (atenção) ou ``alert`` (alerta). Os limiares marcados "a confirmar" no FSD são
constantes deste módulo.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .feeds import FeedInfo

DMI_KEY = "dry_matter_intake_total"
STATUS_RANK = {"ok": 0, "warn": 1, "alert": 2}

# V1: consumo da ração acima do estimado (RMSE da equação de consumo do NASEM: 12,1%; o RuFaS aceita até +30%) (a confirmar)
INTAKE_WARN_PCT, INTAKE_ALERT_PCT = 12.0, 24.0
# V2: limites de FDN total do RuFaS (``MINIMUM_RATION_NDF`` e ``MAXIMUM_RATION_NDF``) e a margem de "atenção"
NDF_MIN, NDF_MAX, NDF_MARGIN = 25.0, 45.0, 0.5
# V3: Tabela 5-1 do NASEM (p. 70): FDN de forragem mínima de 15 a 19%, com FDN total mínima e amido máximo correspondentes
FORAGE_NDF_ALERT_BELOW, FORAGE_NDF_FULL = 15.0, 19.0
STARCH_MARGIN = 2.0
# V4: gordura (extrato etéreo) da ração; o teto do RuFaS é ``MAXIMUM_RATION_FAT`` (7%)
FAT_WARN, FAT_MAX = 5.0, 7.0
# V5: leite perdido por ração insuficiente: alerta a partir desta fração da redução máxima configurada (a confirmar)
MILK_LOSS_ALERT_FRACTION, MILK_LOSS_TOLERANCE = 0.5, 0.005
TOLERANCE = 1e-3  # a otimização do RuFaS deixa a FDN em 45,0000006%: vale como 45

TABLE_5_1_NOTE = (
    "Tabela 5-1 do NASEM: dieta em TMR, forragem com tamanho de partícula adequado e milho moído seco como fonte "
    "predominante de amido."
)


@dataclass(frozen=True)
class Composition:
    """Composição de uma ração (kg de MS por vaca e por dia ponderados, em % da MS)."""

    dmi: float
    ndf: float
    forage_ndf: float
    starch: float
    fat: float


def composition(ration: Mapping[Any, float], library: Mapping[int, FeedInfo]) -> Composition | None:
    """Composição da ração (feed id -> kg de MS); ``None`` se não houver alimento conhecido com quantidade."""
    amounts = {int(k): float(v) for k, v in ration.items() if k != DMI_KEY and float(v) > 0 and int(k) in library}
    total = sum(amounts.values())
    if total <= 0:
        return None

    def weighted(value) -> float:
        return sum(kg * value(library[i]) for i, kg in amounts.items()) / total

    return Composition(
        dmi=total,
        ndf=weighted(lambda f: f.ndf),
        forage_ndf=weighted(lambda f: f.ndf if f.kind == "Forage" else 0.0),
        starch=weighted(lambda f: f.starch or 0.0),
        fat=weighted(lambda f: f.ee),
    )


def _n(value: float, digits: int = 1) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def _worse(a: str, b: str) -> str:
    return a if STATUS_RANK[a] >= STATUS_RANK[b] else b


def _combine(average: str, worst: str) -> str:
    """O estado da média, elevado a no máximo "atenção" se o pior intervalo estiver pior."""
    return _worse(average, "warn" if STATUS_RANK[worst] > STATUS_RANK[average] else average)


def _row(check_id: str, label: str, status: str, value: str, limit: str, detail: str, **metrics: float) -> dict[str, Any]:
    return {"id": check_id, "label": label, "status": status, "value": value, "limit": limit, "detail": detail, "metrics": metrics}


# ---- V1
def _intake_status(excess_pct: float) -> str:
    return "alert" if excess_pct > INTAKE_ALERT_PCT else "warn" if excess_pct > INTAKE_WARN_PCT else "ok"


def check_intake(intake: Sequence[float], estimated: Sequence[float]) -> dict[str, Any] | None:
    """V1: consumo da ração × consumo estimado, por intervalo; a média decide e o pior intervalo pode elevar a "atenção"."""
    excess = [(i / e - 1) * 100 for i, e in zip(intake, estimated) if e and e > 0]
    if not excess:
        return None
    mean, worst = sum(excess) / len(excess), max(excess)
    status = _combine(_intake_status(mean), _intake_status(worst))
    return _row(
        "V1", "Consumo de matéria seca × estimado", status,
        f"{mean:+.1f}% em média (pior intervalo {worst:+.1f}%)".replace(".", ","),
        f"ok até +{INTAKE_WARN_PCT:g}%; alerta acima de +{INTAKE_ALERT_PCT:g}%",
        "O erro típico da equação de consumo do NASEM é 12,1%. O RuFaS aceita a ração até 30% acima do estimado, "
        "então uma ração no teto pode ser irreal.",
        mean_excess_pct=mean, worst_excess_pct=worst,
    )  # fmt: skip


# ---- V2
def _ndf_status(ndf: float) -> str:
    if ndf < NDF_MIN - TOLERANCE or ndf > NDF_MAX + TOLERANCE:
        return "alert"
    return "warn" if ndf < NDF_MIN + NDF_MARGIN or ndf > NDF_MAX - NDF_MARGIN else "ok"


def check_total_ndf(average: Composition, worst: Sequence[Composition] = ()) -> dict[str, Any]:
    """V2: FDN total da ração (% da MS) dentro dos limites do RuFaS (25% a 45%)."""
    status = _combine(_ndf_status(average.ndf), max((_ndf_status(c.ndf) for c in worst), key=STATUS_RANK.get, default="ok"))
    return _row(
        "V2", "FDN total da ração", status, f"{_n(average.ndf)}% da MS", f"de {NDF_MIN:g}% a {NDF_MAX:g}% (RuFaS)",
        "O otimizador do RuFaS costuma parar no teto de 45%. O NASEM só traz o mínimo de 25%.",
        ndf=average.ndf,
    )  # fmt: skip


# ---- V3
def table_5_1(forage_ndf: float) -> tuple[float, float] | None:
    """(FDN total mínima, amido máximo) em % da MS da Tabela 5-1 para a FDN de forragem; ``None`` abaixo de 15%."""
    if forage_ndf < FORAGE_NDF_ALERT_BELOW - TOLERANCE:
        return None
    shortfall = max(0.0, FORAGE_NDF_FULL - forage_ndf)
    return NDF_MIN + 2 * shortfall, 30.0 - 2 * shortfall


def _table_status(c: Composition) -> str:
    limits = table_5_1(c.forage_ndf)
    if limits is None:
        return "alert"
    ndf_min, starch_max = limits
    if c.ndf < ndf_min - TOLERANCE or c.starch > starch_max + TOLERANCE:
        return "alert"
    return "warn" if c.forage_ndf < FORAGE_NDF_FULL or c.starch > starch_max - STARCH_MARGIN else "ok"


def check_table_5_1(average: Composition, worst: Sequence[Composition] = ()) -> dict[str, Any]:
    """V3: FDN de forragem, FDN total e amido contra a Tabela 5-1 do NASEM."""
    status = _combine(_table_status(average), max((_table_status(c) for c in worst), key=STATUS_RANK.get, default="ok"))
    limits = table_5_1(average.forage_ndf)
    limit = (
        "FDN de forragem abaixo de 15%: fora da tabela"
        if limits is None
        else f"FDN total ≥ {_n(limits[0])}% e amido ≤ {_n(limits[1])}%"
    )
    return _row(
        "V3", "FDN de forragem, FDN total e amido (Tabela 5-1)", status,
        f"FDN de forragem {_n(average.forage_ndf)}%, FDN total {_n(average.ndf)}%, amido {_n(average.starch)}%", limit,
        TABLE_5_1_NOTE, forage_ndf=average.forage_ndf, ndf=average.ndf, starch=average.starch,
    )  # fmt: skip


# ---- V4
def _fat_status(fat: float) -> str:
    return "alert" if fat > FAT_MAX + TOLERANCE else "warn" if fat > FAT_WARN else "ok"


def check_fat(average: Composition, worst: Sequence[Composition] = ()) -> dict[str, Any]:
    """V4: gordura (extrato etéreo) da ração, em % da MS."""
    status = _combine(_fat_status(average.fat), max((_fat_status(c.fat) for c in worst), key=STATUS_RANK.get, default="ok"))
    return _row(
        "V4", "Gordura da ração", status, f"{_n(average.fat)}% da MS", f"ok até {FAT_WARN:g}%; teto {FAT_MAX:g}% (RuFaS e NASEM)",
        "O NASEM recomenda menos de 5% de gordura no início da lactação e no máximo 7% no total.", fat=average.fat,
    )  # fmt: skip


# ---- V5
def check_milk_loss(reduction: float, maximum: float) -> dict[str, Any]:
    """V5: leite perdido por ração insuficiente (kg/vaca/dia), já calculado pelo RuFaS."""
    if reduction <= MILK_LOSS_TOLERANCE:
        status = "ok"
    elif maximum > 0 and reduction >= MILK_LOSS_ALERT_FRACTION * maximum:
        status = "alert"
    else:
        status = "warn"
    return _row(
        "V5", "Leite perdido por ração insuficiente", status, f"{_n(reduction, 2)} kg/vaca/dia",
        f"ok sem perda; alerta a partir de {_n(MILK_LOSS_ALERT_FRACTION * maximum, 2)} kg (metade da redução máxima)",
        "O RuFaS reduz o leite (0,25 kg por tentativa) quando a ração não atende às exigências.", reduction=reduction,
    )  # fmt: skip


def _intake_of(ration: Mapping[Any, float]) -> float:
    """Consumo total de MS de uma ração: o campo do RuFaS ou, na falta dele, a soma dos alimentos."""
    return float(ration.get(DMI_KEY) or sum(float(v) for k, v in ration.items() if k != DMI_KEY))


def consistency_checks(
    intervals: Sequence[Mapping[Any, float]],
    estimated_intake: Sequence[float | None],
    average_ration: Mapping[Any, float],
    library: Mapping[int, FeedInfo],
    milk_reduction: float,
    max_milk_reduction: float,
) -> list[dict[str, Any]]:
    """V1 a V5 da ração média e dos intervalos de formulação (uma ração por intervalo)."""
    per_interval = [c for c in (composition(r, library) for r in intervals) if c]
    average = composition(average_ration, library)
    checks: list[dict[str, Any]] = []
    intake = check_intake([_intake_of(r) for r in intervals], [e or 0.0 for e in estimated_intake])
    if intake:
        checks.append(intake)
    if average:
        checks += [check_total_ndf(average, per_interval), check_table_5_1(average, per_interval), check_fat(average, per_interval)]
    checks.append(check_milk_loss(milk_reduction, max_milk_reduction))
    return checks


def summarize(checks: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    return {status: sum(c["status"] == status for c in checks) for status in STATUS_RANK}
