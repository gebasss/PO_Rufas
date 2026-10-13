"""Curva de lactação de Wood e marcos reprodutivos (PEV e gestação) do gráfico do professor.

    y(t) = l * t^m * exp(-n * t)        (kg de leite por dia, t = dias em lactação)

Os parâmetros (l, m, n) por paridade vêm do próprio RuFaS (já calibrados para a fazenda simulada). O PEV
(período de espera voluntário) é o número de dias após o parto antes da primeira inseminação; se a vaca emprenha
logo após o PEV, o parto seguinte ocorre aproximadamente ``PEV + gestação`` dias depois do parto atual.
"""

from __future__ import annotations

import math

# Fallback quando não há simulação: média base do RuFaS (l=19.9, m=0.247, n=0.003376) mais o ajuste de paridade de
# input/data/animal/lactation_curve_adjustment_inputs.json (m e n escalados por 1e-2 e 1e-4), sem os ajustes de
# ano, região e frequência de ordenha. Os valores calibrados da simulação (SimulationResult.wood) têm prioridade.
DEFAULT_WOOD = {
    1: {"l": 19.9 - 4.18, "m": 0.247 - 0.37e-2, "n": 0.003376 - 9.31e-4 * 1.0},
    2: {"l": 19.9 + 2.16, "m": 0.247 - 1.20e-2, "n": 0.003376 + 2.66e-4},
    3: {"l": 19.9 + 2.02, "m": 0.247 + 1.57e-2, "n": 0.003376 + 6.65e-4},
}


def wood_yield(day: int, l: float, m: float, n: float) -> float:
    return l * day**m * math.exp(-n * day)


def lactation_curve(wood: dict[int, dict[str, float]] | None, days: int = 330) -> dict[int, list[float]]:
    params = wood or DEFAULT_WOOD
    return {parity: [wood_yield(d, p["l"], p["m"], p["n"]) for d in range(1, days + 1)] for parity, p in params.items()}


def milestones(pev_days: int = 60, gestation_days: int = 270, dry_off_days_before_calving: int = 60) -> dict[str, int]:
    """Marcos ao longo da lactação, em dias em lactação (DIM)."""
    calving_next = pev_days + gestation_days
    return {
        "pev": pev_days,
        "proximo_parto": calving_next,
        "secagem": calving_next - dry_off_days_before_calving,
    }


def peak(curve: list[float]) -> tuple[int, float]:
    day = max(range(len(curve)), key=curve.__getitem__)
    return day + 1, curve[day]


def milk_305(curve: list[float]) -> float:
    return float(sum(curve[:305]))
