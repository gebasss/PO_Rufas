"""Arquivos de cenário: salvar e abrir a configuração de uma tela como um arquivo JSON local (RF-21).

O arquivo guarda só **entradas** (alimentos, preços, limites, vaca, dietas, fatores), nunca resultados: ao abrir, a tela
recalcula. O formato é versionado (``version``) para que arquivos antigos continuem abrindo quando ele mudar; um arquivo de
versão mais nova que a deste programa é recusado com mensagem clara. Dois tipos de cenário:

* ``cow``: a tela Vaca leiteira (padrão, preço do leite, tempo, limite de leite perdido, alimentos com preço e limites) e, se
  houver, a configuração da análise de sensibilidade;
* ``module``: a tela Avaliar dietas (padrão, categoria, tipo de animal, vaca, exigências sobrescritas, alimentos, dietas e a
  configuração da dieta ótima).
"""

from __future__ import annotations

import json
import math
from datetime import datetime
from typing import Any, Callable, Mapping

from .feeds import feed_library
from .herd import DEFAULT_COWS, MAX_COWS, MIN_COWS
from .module.categories import parse_animal_type, parse_category
from .module.evaluate import MAX_DIETS
from .module.fields import FIELD_BY_KEY
from .module.optimize import MAX_SEEDS, RESOLUTIONS
from .module.requirements import REQUIREMENT_FIELDS
from .standards import get_standard

FORMAT = "dietopt-scenario"
VERSION = 1
SENSITIVITY_METHODS = ("grid", "latin")
MILK_FACTOR = "milk_price"
FILENAMES = {"cow": "cenario-vaca-leiteira.json", "module": "cenario-avaliar-dietas.json"}
# Migrações de uma versão para a seguinte: ``MIGRATIONS[n]`` converte os dados da versão n para a n + 1.
MIGRATIONS: Mapping[int, Callable[[dict[str, Any]], dict[str, Any]]] = {}


# ---------------------------------------------------------------------------------------------------------------
# Leitura de valores
# ---------------------------------------------------------------------------------------------------------------
def _number(value: Any, label: str, *, low: float | None = None, high: float | None = None, integer: bool = False) -> float | int:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label}: informe um número")
    if integer and value != int(value):
        raise ValueError(f"{label}: use um número inteiro")
    if (low is not None and value < low) or (high is not None and value > high):
        raise ValueError(f"{label}: fora da faixa aceita ({'−∞' if low is None else f'{low:g}'} a {'∞' if high is None else f'{high:g}'})")
    return int(value) if integer else float(value)


def _mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label}: formato inválido")
    return value


def _feeds(raw: Any, standard: str, warnings: list[str]) -> list[dict[str, Any]]:
    """Alimentos com preço e limites; os que não existem na biblioteca do padrão saem, com aviso."""
    if not isinstance(raw, list):
        raise ValueError("Alimentos: formato inválido")
    library = feed_library(standard)
    feeds: list[dict[str, Any]] = []
    dropped: list[int] = []
    for item in raw:
        item = _mapping(item, "Alimento")
        feed_id = int(_number(item.get("id"), "Alimento (id)", integer=True))
        if feed_id not in library:
            dropped.append(feed_id)
            continue
        if any(f["id"] == feed_id for f in feeds):
            raise ValueError(f"Alimento {feed_id} repetido")
        label = f"Alimento {feed_id}"
        price = _number(item.get("price"), f"{label}, preço", low=0)
        low = 0.0 if item.get("min") is None else _number(item.get("min"), f"{label}, mínimo", low=0)
        high = library[feed_id].default_max if item.get("max") is None else _number(item.get("max"), f"{label}, máximo", low=0)
        if low > high:
            raise ValueError(f"{label}: o mínimo ({low:g}) é maior que o máximo ({high:g})")
        feeds.append({"id": feed_id, "price": price, "min": low, "max": high})
    if dropped:
        warnings.append(f"Removidos por não existirem no padrão {standard}: {sorted(dropped)}.")
    return feeds


def _standard(raw: Mapping[str, Any]) -> str:
    return get_standard(raw.get("standard") or "NRC").code


# ---------------------------------------------------------------------------------------------------------------
# Cenário da tela Vaca leiteira
# ---------------------------------------------------------------------------------------------------------------
def _sensitivity(raw: Any, feed_ids: set[int]) -> dict[str, Any]:
    raw = _mapping(raw, "Sensibilidade")
    method = raw.get("method", "grid")
    if method not in SENSITIVITY_METHODS:
        raise ValueError(f"Sensibilidade: método desconhecido {method!r} (use {' ou '.join(SENSITIVITY_METHODS)})")
    factors: dict[str, dict[str, Any]] = {}
    for key, item in _mapping(raw.get("factors") or {}, "Sensibilidade, fatores").items():
        if key != MILK_FACTOR and (not key.isdigit() or int(key) not in feed_ids):
            continue  # fator de um alimento que não está no cenário
        item = _mapping(item, f"Fator {key}")
        if not isinstance(item.get("on"), bool):
            raise ValueError(f"Fator {key}: o campo \"on\" deve ser verdadeiro ou falso")
        factors[key] = {"on": item["on"], "low": _number(item.get("low"), f"Fator {key}, valor baixo"), "high": _number(item.get("high"), f"Fator {key}, valor alto")}
    return {"method": method, "levels": _number(raw.get("levels", 3), "Sensibilidade, níveis", low=2, high=12, integer=True), "factors": factors}


def _cow_scenario(raw: Mapping[str, Any], warnings: list[str]) -> dict[str, Any]:
    standard = _standard(raw)
    params = _mapping(raw.get("params"), "Parâmetros")
    feeds = _feeds(raw.get("feeds"), standard, warnings)
    out: dict[str, Any] = {
        "standard": standard,
        "params": {
            "milkPrice": _number(params.get("milkPrice"), "Preço do leite", low=0),
            "years": _number(params.get("years"), "Anos de simulação", low=1, high=3, integer=True),
            "maxReduction": _number(params.get("maxReduction"), "Redução máxima de leite", low=0),
            # arquivos salvos antes do RF-13 não têm o rebanho: valem o padrão do exemplo
            "cowNum": _number(params.get("cowNum", DEFAULT_COWS), "Vacas no rebanho", low=MIN_COWS, high=MAX_COWS, integer=True),
        },
        "feeds": feeds,
    }
    if raw.get("sensitivity") is not None:
        out["sensitivity"] = _sensitivity(raw["sensitivity"], {f["id"] for f in feeds})
    return out


# ---------------------------------------------------------------------------------------------------------------
# Cenário da tela Avaliar dietas
# ---------------------------------------------------------------------------------------------------------------
def _cow_values(raw: Any) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for key, value in _mapping(raw or {}, "Vaca").items():
        spec = FIELD_BY_KEY.get(key)
        if spec is None:
            raise ValueError(f"Vaca: campo desconhecido {key!r}")
        if value is None or value == "":
            continue  # campo ainda vazio no rascunho
        if spec.choices:
            if value not in spec.choices:
                raise ValueError(f"{spec.label}: use {' ou '.join(spec.choices)}")
            values[key] = value
        else:
            values[key] = _number(value, spec.label)
    return values


def _overrides(raw: Any) -> dict[str, float]:
    out = {}
    for key, value in _mapping(raw or {}, "Exigências sobrescritas").items():
        if key not in REQUIREMENT_FIELDS:
            raise ValueError(f"Exigência desconhecida: {key!r}")
        out[key] = float(_number(value, REQUIREMENT_FIELDS[key][0], low=0))
    return out


def _diets(raw: Any, feed_ids: set[int], warnings: list[str]) -> list[dict[str, Any]]:
    if not isinstance(raw, list):
        raise ValueError("Dietas: formato inválido")
    if len(raw) > MAX_DIETS:
        raise ValueError(f"No máximo {MAX_DIETS} dietas")
    diets = []
    for index, item in enumerate(raw, 1):
        item = _mapping(item, f"Dieta {index}")
        name = item.get("name", "")
        if not isinstance(name, str) or len(name) > 100:
            raise ValueError(f"Dieta {index}: o nome deve ser um texto de até 100 caracteres")
        amounts: dict[str, float] = {}
        for key, value in _mapping(item.get("amounts") or {}, f"Dieta {index}, quantidades").items():
            if not str(key).isdigit() or int(key) not in feed_ids:
                warnings.append(f"Dieta {name or index}: o alimento {key} não está na tabela e foi removido.")
                continue
            amounts[str(int(key))] = float(_number(value, f"Dieta {name or index}, alimento {key}", low=0))
        diets.append({"name": name, "amounts": amounts})
    return diets


def _module_scenario(raw: Mapping[str, Any], warnings: list[str]) -> dict[str, Any]:
    standard = _standard(raw)
    category = parse_category(raw.get("category"))
    animal = parse_animal_type(category, raw.get("animalType"))
    feeds = _feeds(raw.get("feeds"), standard, warnings)
    resolution = raw.get("resolution", "normal")
    if resolution not in RESOLUTIONS:
        raise ValueError(f"Resolução desconhecida: {resolution!r} (use {', '.join(RESOLUTIONS)})")
    return {
        "standard": standard,
        "category": category.value,
        "animalType": animal,
        "cow": _cow_values(raw.get("cow")),
        "override": _overrides(raw.get("override")),
        "feeds": feeds,
        "diets": _diets(raw.get("diets"), {f["id"] for f in feeds}, warnings),
        "tolerance": float(_number(raw.get("tolerance", 1.0), "Tolerância do erro", low=0)),
        "resolution": resolution,
        "seeds": _number(raw.get("seeds", 5), "Execuções do RuFaS", low=0, high=MAX_SEEDS, integer=True),
    }


NORMALIZERS: Mapping[str, Callable[[Mapping[str, Any], list[str]], dict[str, Any]]] = {"cow": _cow_scenario, "module": _module_scenario}


# ---------------------------------------------------------------------------------------------------------------
# Arquivo
# ---------------------------------------------------------------------------------------------------------------
def _kind(kind: Any) -> str:
    if kind not in NORMALIZERS:
        raise ValueError(f"Tipo de cenário desconhecido: {kind!r} (use {' ou '.join(NORMALIZERS)})")
    return str(kind)


def pack(kind: str, data: Any, now: datetime | None = None) -> dict[str, str]:
    """Valida os dados da tela e devolve o arquivo (``filename`` e ``content``, um JSON legível)."""
    kind = _kind(kind)
    normalized = NORMALIZERS[kind](_mapping(data, "Cenário"), [])
    envelope = {"format": FORMAT, "version": VERSION, "kind": kind, "saved_at": (now or datetime.now()).isoformat(timespec="seconds"), "data": normalized}
    return {"filename": FILENAMES[kind], "mime": "application/json;charset=utf-8", "content": json.dumps(envelope, ensure_ascii=False, indent=2) + "\n"}


def unpack(text: str) -> dict[str, Any]:
    """Lê e valida um arquivo de cenário. Devolve ``kind``, ``version``, ``saved_at``, ``data`` e ``warnings``."""
    try:
        envelope = json.loads(text.lstrip("﻿"))
    except (json.JSONDecodeError, AttributeError):
        raise ValueError("O arquivo não é um JSON válido") from None
    if not isinstance(envelope, dict) or envelope.get("format") != FORMAT:
        raise ValueError("O arquivo não é um cenário do Dieta Ótima com RuFaS")
    version = envelope.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version < 1:
        raise ValueError("O arquivo não informa a versão do formato")
    if version > VERSION:
        raise ValueError(f"O arquivo é da versão {version} do formato, mais nova que a {VERSION} deste programa; atualize o programa")
    kind = _kind(envelope.get("kind"))
    data = _mapping(envelope.get("data"), "Cenário")
    for old in range(version, VERSION):
        data = MIGRATIONS[old](dict(data))
    warnings: list[str] = []
    return {"kind": kind, "version": VERSION, "saved_at": envelope.get("saved_at"), "data": NORMALIZERS[kind](data, warnings), "warnings": warnings}
