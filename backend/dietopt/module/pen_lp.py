"""Ração linear (LP) × ração do RuFaS (SLSQP) nas mesmas exigências de uma simulação da vaca leiteira (FSD, A.14).

Em cada intervalo de ração de uma simulação, o RuFaS formula a ração do lote de vacas em lactação com o SLSQP, a partir das
exigências médias do lote. Aqui o LP (``optimize.search``) é resolvido sobre **exatamente essas exigências** e os mesmos
alimentos, preços e limites, e as duas rações são comparadas. O resultado esperado é um empate: o SLSQP do RuFaS já chega perto do ótimo (medido: o total
diferiu em centésimos de ponto percentual, ver ``LINEARIZACAO.md``, 7.7). Nenhuma simulação nova é feita: o leite e as exigências são os
da simulação que já existe, e cada ração do LP é conferida com as restrições originais do RuFaS (``optimize._check``).

Duas variantes do LP, para não confundir economia de ração com mais consumo:

* **consumo livre**: o consumo pode variar na faixa que o RuFaS permite (estimativa ± 30%), como no SLSQP;
* **mesmo consumo**: o consumo é o que o SLSQP escolheu naquele intervalo (a comparação mais conservadora).

Só vale para o padrão NRC: no NASEM a oferta de energia exige metano e nitrogênio urinário do lote, que a simulação não informa.
"""

from __future__ import annotations

from typing import Any, Callable, Mapping, Sequence

from .optimize import RUFAS_TOLERANCE, _amounts, _check, _within, build_problem, search
from .requirements import compute_requirements

# Chave da exigência na saída do RuFaS (``avg_rqmts_for_LAC_COW``) -> exigência do módulo.
REQUIREMENT_MAP = {
    "NEmaint_requirement": "maintenance_energy",
    "NEa_requirement": "activity_energy",
    "NEg_requirement": "growth_energy",
    "NEpreg_requirement": "pregnancy_energy",
    "NEl_requirement": "lactation_energy",
    "MP_requirement": "metabolizable_protein",
    "Ca_requirement": "calcium",
    "P_req": "phosphorus",
    "P_req_process": "process_based_phosphorus",
    "DMIest_requirement": "dry_matter",
}
MIN_BODY_WEIGHT = 50.0
SAMPLE_RESOLUTION = "normal"  # com o consumo fixo a busca normal custa pouco mais que a rápida e fecha casos em que a rápida parava 0,6% acima
RESOLUTION = "rapida"  # a normal custa 2,5 vezes mais e muda o custo em menos de 0,1%


def _cow(requirements: Mapping[str, Any]) -> dict[str, Any]:
    """Vaca só para satisfazer a calculadora: as exigências vêm do RuFaS (sobrescritas) e só o peso entra na oferta."""
    weight = max(float(requirements.get("avg_BW") or 0.0), MIN_BODY_WEIGHT)
    return {
        "body_weight": weight, "mature_body_weight": max(700.0, weight), "parity": 2, "days_in_milk": 150, "housing": "Barn",
        "distance": 0, "milk_production": 35.0, "milk_fat": 3.7, "milk_true_protein": 3.1, "milk_lactose": 4.85,
    }  # fmt: skip


def _solve(
    requirements: Mapping[str, Any], ids: Sequence[int], prices: Mapping[int, float], limits: Mapping[int, tuple[float, float]],
    dmi_range: tuple[float, float] | None, should_stop: Callable[[], bool] | None, resolution: str = RESOLUTION,
) -> dict[str, Any] | None:  # fmt: skip
    cow = _cow(requirements)
    overrides = {name: float(requirements[key]) for key, name in REQUIREMENT_MAP.items()}
    required = compute_requirements("NRC", "LAC_COW", cow, overrides, "LAC_COW")
    problem = build_problem("NRC", "LAC_COW", "LAC_COW", cow, list(ids), prices, limits, required, dmi_range)
    best, _ = search(problem, resolution, None, should_stop)
    if best is None:
        return None
    amounts = _amounts(problem, best.x)
    check = _check(problem, "LAC_COW", cow, "LP", amounts, prices, limits)
    if dmi_range is not None and dmi_range[0] == dmi_range[1]:
        # Mesmo consumo: o consumo é o que o SLSQP escolheu e não é do LP. Nos dados reais o SLSQP passou do teto de +30% em até 0,7%
        # de um intervalo (``dmi_max``); isso não é defeito da ração do LP, então a faixa de consumo não entra na conferência.
        skip = ("dmi_min", "dmi_max")
        check = {
            **check,
            "constraints": [c for c in check["constraints"] if c.get("id") not in skip],
            "violated": [v for v in check["violated"] if v not in skip],
        }
    return {
        "cost": best.cost,
        "dmi": float(best.x.sum()),
        "amounts": {str(i): v for i, v in amounts.items()},
        "verified": _within(check, RUFAS_TOLERANCE),  # a tolerância relativa que o próprio SLSQP do RuFaS deixa passar
        "violated": list(check["violated"]),
        "tdn_percentage": best.point.tdn,
        "concentrate_percentage": best.point.conc,
    }


def _interval_lengths(starts: Sequence[int], total_days: int) -> list[int]:
    ends = [*starts[1:], total_days]
    return [max(int(end) - int(start), 1) for start, end in zip(starts, ends)]


def compare_with_simulation(
    simulation: Any,
    feed_ids: Sequence[int],
    prices: Mapping[int, float],
    limits: Mapping[int, tuple[float, float]],
    standard: str = "NRC",
    on_progress: Callable[[int, int], None] | None = None,
    should_stop: Callable[[], bool] | None = None,
) -> dict[str, Any]:
    """Compara, intervalo a intervalo, a ração do SLSQP da simulação com a do LP sobre as mesmas exigências.

    ``simulation`` é um ``SimulationResult``; ``feed_ids``, ``prices`` e ``limits`` são os do cenário simulado.
    """
    if standard != "NRC":
        raise ValueError("A comparação com a ração linear só está disponível para o padrão NRC.")
    ids = sorted({int(i) for i in feed_ids})
    missing = [i for i in ids if i not in prices]
    if missing:
        raise ValueError(f"Informe o preço (US$/kg MS) dos alimentos: {missing}")
    steps = len(simulation.requirements)
    if not steps or len(simulation.ration_kg_per_cow) != steps:
        raise ValueError("A simulação não traz as exigências e a ração por intervalo.")
    price = {i: float(prices[i]) for i in ids}
    bounds = {i: (float(limits[i][0]), float(limits[i][1])) if i in limits else (0.0, 100.0) for i in ids}
    lengths = _interval_lengths(simulation.interval_days, len(simulation.days))
    cows = list(simulation.cows_in_pen) + [0] * (steps - len(simulation.cows_in_pen))

    total = 2 * steps
    done = 0
    if on_progress:
        on_progress(0, total)  # a barra já mostra o total antes do primeiro intervalo (sem "Na fila…")

    def one(index: int) -> dict[str, Any]:
        nonlocal done
        ration = simulation.ration_kg_per_cow[index]
        slsqp_amounts = {str(k): float(v) for k, v in ration.items() if k != "dry_matter_intake_total" and float(v) > 0}
        slsqp_dmi = float(ration.get("dry_matter_intake_total") or sum(slsqp_amounts.values()))
        slsqp_cost = sum(v * price.get(int(k), 0.0) for k, v in slsqp_amounts.items())
        requirements = simulation.requirements[index]
        variants = []
        for dmi_range in (None, (slsqp_dmi, slsqp_dmi)):
            variants.append(_solve(requirements, ids, price, bounds, dmi_range, should_stop))
            done += 1
            if on_progress:
                on_progress(done, total)
        return {
            "day": int(simulation.interval_days[index]),
            "days": lengths[index],
            "cows": int(cows[index]),
            "slsqp": {"cost": slsqp_cost, "dmi": slsqp_dmi, "amounts": slsqp_amounts},
            "lp_free": variants[0],
            "lp_same": variants[1],
        }

    intervals = [one(index) for index in range(steps)]  # em fila: threads não aceleram (o Python segura o cálculo)
    warnings: list[str] = []
    for row in intervals:
        if row["lp_free"] is None or row["lp_same"] is None:
            warnings.append(f"Intervalo do dia {row['day']}: o LP não achou ração viável nas restrições do RuFaS.")
        elif not (row["lp_free"]["verified"] and row["lp_same"]["verified"]):
            warnings.append(f"Intervalo do dia {row['day']}: a ração do LP viola uma restrição original do RuFaS por diferença numérica.")
    return {
        "standard": standard,
        "feed_ids": ids,
        "intervals": intervals,
        "summary": _summary(intervals, ids),
        "warnings": warnings,
    }


def _summary(intervals: Sequence[dict[str, Any]], ids: Sequence[int]) -> dict[str, Any]:
    """Médias ponderadas pelos dias do intervalo e economia do rebanho (vacas em lactação × dias × diferença de custo)."""
    usable = [row for row in intervals if row["lp_free"] and row["lp_same"]]
    days = sum(row["days"] for row in usable)
    if not days:
        return {"intervals_used": 0}

    def mean(getter: Callable[[dict[str, Any]], float]) -> float:
        return sum(getter(row) * row["days"] for row in usable) / days

    def herd(variant: str) -> float:
        return sum((row["slsqp"]["cost"] - row[variant]["cost"]) * row["cows"] * row["days"] for row in usable)

    slsqp = mean(lambda r: r["slsqp"]["cost"])
    summary: dict[str, Any] = {
        "intervals_used": len(usable),
        "days": days,
        "slsqp_cost_per_cow_day": slsqp,
        "slsqp_dmi": mean(lambda r: r["slsqp"]["dmi"]),
        "mean_cows": sum(r["cows"] * r["days"] for r in usable) / days,
    }
    for variant in ("lp_free", "lp_same"):
        cost = mean(lambda r, v=variant: r[v]["cost"])
        summary[variant] = {
            "cost_per_cow_day": cost,
            "dmi": mean(lambda r, v=variant: r[v]["dmi"]),
            "saving_per_cow_day": slsqp - cost,
            "saving_pct": (slsqp - cost) / slsqp * 100 if slsqp else 0.0,
            "herd_saving": herd(variant),
            "mean_amounts": {
                str(i): mean(lambda r, v=variant, k=str(i): r[v]["amounts"].get(k, 0.0)) for i in ids
            },
            "all_verified": all(r[variant]["verified"] for r in usable),
        }
    summary["slsqp_mean_amounts"] = {str(i): mean(lambda r, k=str(i): r["slsqp"]["amounts"].get(k, 0.0)) for i in ids}
    return summary


def sample_indices(steps: int, sample: int) -> list[int]:
    """``sample`` intervalos igualmente espaçados, do primeiro ao último (todos, se ``sample`` >= ``steps``)."""
    if sample >= steps:
        return list(range(steps))
    if sample <= 1:
        return [0]
    return sorted({round(i * (steps - 1) / (sample - 1)) for i in range(sample)})


def compare_sample(
    simulation: Any,
    feed_ids: Sequence[int],
    prices: Mapping[int, float],
    limits: Mapping[int, tuple[float, float]],
    sample: int = 4,
    should_stop: Callable[[], bool] | None = None,
) -> dict[str, Any]:
    """Versão curta de ``compare_with_simulation`` para muitas simulações (Sensibilidade): só a variante de **mesmo consumo**
    (a conservadora) e só ``sample`` intervalos igualmente espaçados.

    Devolve o custo médio por vaca por dia do SLSQP e do LP nos intervalos usados (ponderado pelos dias), a diferença em % e se
    todas as rações do LP atendem às restrições originais do RuFaS.
    """
    ids = sorted({int(i) for i in feed_ids})
    steps = len(simulation.requirements)
    if not steps or len(simulation.ration_kg_per_cow) != steps:
        raise ValueError("A simulação não traz as exigências e a ração por intervalo.")
    price = {i: float(prices[i]) for i in ids}
    bounds = {i: (float(limits[i][0]), float(limits[i][1])) if i in limits else (0.0, 100.0) for i in ids}
    lengths = _interval_lengths(simulation.interval_days, len(simulation.days))
    rows = []
    for index in sample_indices(steps, sample):
        ration = simulation.ration_kg_per_cow[index]
        amounts = {str(k): float(v) for k, v in ration.items() if k != "dry_matter_intake_total" and float(v) > 0}
        dmi = float(ration.get("dry_matter_intake_total") or sum(amounts.values()))
        slsqp_cost = sum(v * price.get(int(k), 0.0) for k, v in amounts.items())
        lp = _solve(simulation.requirements[index], ids, price, bounds, (dmi, dmi), should_stop, SAMPLE_RESOLUTION)
        rows.append({"day": int(simulation.interval_days[index]), "days": lengths[index], "slsqp": slsqp_cost, "lp": lp})
    usable = [r for r in rows if r["lp"] is not None]
    days = sum(r["days"] for r in usable)
    if not days:
        return {"intervals_sampled": len(rows), "intervals_used": 0}
    slsqp = sum(r["slsqp"] * r["days"] for r in usable) / days
    lp_cost = sum(r["lp"]["cost"] * r["days"] for r in usable) / days
    return {
        "intervals_sampled": len(rows),
        "intervals_used": len(usable),
        "slsqp_cost": slsqp,
        "lp_cost": lp_cost,
        "diff_pct": (lp_cost / slsqp - 1) * 100 if slsqp else 0.0,
        "verified": all(r["lp"]["verified"] for r in usable),
    }
