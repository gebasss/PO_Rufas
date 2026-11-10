"""Tamanho do rebanho da simulação (RF-13).

O exemplo ``freestall`` do RuFaS tem 100 vacas e, junto, o resto do rebanho (bezerras, novilhas, reposição) e o tamanho-alvo
(``herd_num``): o RuFaS vende novilhas prenhes quando as vacas e novilhas prenhes passam de 103% do alvo e compra reposição
quando ficam abaixo de 101%. Mudar só ``cow_num`` não muda o rebanho de verdade (o alvo continua em 100 e o RuFaS o
recompõe), então aqui o rebanho inteiro é escalado junto com o número de vacas. As baias (``number_of_stalls``) também: o RuFaS recusa
a simulação se algum lote passa da lotação máxima das suas baias.
"""

from __future__ import annotations

import math
from typing import Any

DEFAULT_COWS = 100  # vacas do exemplo ``freestall``
# Faixa verificada com simulações reais (``docs/FSD.md``, RF-13). Abaixo de 60 vacas o RuFaS falha: com 50, por exemplo, um
# lote que esvazia (o das bezerras) e depois recebe um animal monta a lista de alimentos errada e divide por zero. O teto de 500
# é o maior tamanho medido (1 ano: 57 s e 0,96 GB, contra 27 s e 0,68 GB com 100 vacas).
MIN_COWS = 60
MAX_COWS = 500
# Acima disso a interface avisa do tempo e da memória de cada simulação.
WARN_COWS = 250

# Contagens do rebanho inicial do exemplo que crescem com o número de vacas.
_SCALED = ("calf_num", "heiferI_num", "heiferII_num", "heiferIII_num_springers", "replace_num")


def herd_limits() -> dict[str, int]:
    """Padrão e limites do número de vacas, para a interface."""
    return {"default": DEFAULT_COWS, "min": MIN_COWS, "max": MAX_COWS, "warn": WARN_COWS}


def parse_cow_num(value: Any) -> int | None:
    """Valida o número de vacas informado. ``None`` (ou o padrão do exemplo) mantém o rebanho do exemplo."""
    if value is None or value == "":
        return None
    if isinstance(value, bool) or (isinstance(value, float) and not value.is_integer()):
        raise ValueError(f"Número de vacas inválido: {value!r}. Use um número inteiro.")
    try:
        cows = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"Número de vacas inválido: {value!r}. Use um número inteiro.") from None
    if not MIN_COWS <= cows <= MAX_COWS:
        raise ValueError(f"Número de vacas fora do intervalo: {cows}. Use de {MIN_COWS} a {MAX_COWS}.")
    return None if cows == DEFAULT_COWS else cows


def scale_herd(animal: dict[str, Any], cows: int) -> dict[str, Any]:
    """Devolve a cópia do arquivo ``animal`` com o rebanho e as baias proporcionais a ``cows`` vacas."""
    info = animal["herd_information"]
    factor = cows / info["cow_num"]
    herd = dict(info)
    herd["cow_num"] = cows
    herd["herd_num"] = cows
    for key in _SCALED:
        herd[key] = max(1, round(info[key] * factor))
    pens = [{**pen, "number_of_stalls": max(1, math.ceil(pen["number_of_stalls"] * factor))} for pen in animal["pen_information"]]

    return {**animal, "herd_information": herd, "pen_information": pens}
