"""Importação de preços por CSV (RF-22): cotações em reais ou dólares viram US$ por kg de matéria seca.

Regra de conversão (LINEARIZACAO.md, 7.2)::

    preço (US$/kg MS) = preço_original / (kg por unidade comercial) / (MS do alimento, fração, se a base é matéria natural)
                        / câmbio (R$ por US$, se a moeda é BRL)

O mapeamento é pelo **id do RuFaS** ou pelo nome exato do alimento na biblioteca do padrão; o que não casa é devolvido com o
motivo, nunca descartado em silêncio. O mapeamento entre os indicadores do CEPEA e a biblioteca é do usuário (decisão L-Q3).
"""

from __future__ import annotations

import csv
import io
import math
import re
import unicodedata
from dataclasses import dataclass
from typing import Any, Mapping

from .feeds import FeedInfo, feed_library
from .standards import get_standard

# Nome de coluna (sem acento, minúsculo) -> campo; vários apelidos por campo.
COLUMN_ALIASES: Mapping[str, str] = {
    "id": "id", "rufas_id": "id",
    "alimento": "name", "nome": "name", "feed": "name", "name": "name",
    "preco": "price", "price": "price", "valor": "price",
    "moeda": "currency", "currency": "currency",
    "cambio": "fx", "fx": "fx", "taxa": "fx",
    "unidade_kg": "unit_kg", "kg_por_unidade": "unit_kg", "unit_kg": "unit_kg", "kg": "unit_kg",
    "base": "basis",
    "fonte": "source", "source": "source", "indicador": "source",
}  # fmt: skip
CURRENCIES = {"USD": "USD", "US$": "USD", "DOLAR": "USD", "BRL": "BRL", "R$": "BRL", "REAL": "BRL", "REAIS": "BRL"}
BASES = {"MS": "MS", "MATERIA SECA": "MS", "DM": "MS", "MN": "MN", "MATERIA NATURAL": "MN", "TAL COMO OFERTADO": "MN", "AS FED": "MN"}
MAX_ROWS = 2000


@dataclass(frozen=True)
class Problem:
    line: int
    text: str
    reason: str


def _plain(text: str) -> str:
    """Minúsculo, sem acento e com espaços normalizados (para comparar nomes e cabeçalhos)."""
    decomposed = unicodedata.normalize("NFKD", text)
    return re.sub(r"\s+", " ", "".join(c for c in decomposed if not unicodedata.combining(c))).strip().casefold()


def _number(text: str) -> float:
    """Número com vírgula ou ponto decimal (``1.234,56`` e ``1,234.56`` também)."""
    cleaned = text.strip().replace(" ", "")
    if "," in cleaned and "." in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".") if cleaned.rfind(",") > cleaned.rfind(".") else cleaned.replace(",", "")
    else:
        cleaned = cleaned.replace(",", ".")
    value = float(cleaned)
    if not math.isfinite(value):
        raise ValueError(text)
    return value


def _names(library: Mapping[int, FeedInfo]) -> dict[str, list[int]]:
    """Nome normalizado -> ids, para o nome curto e para "nome — descrição"."""
    out: dict[str, list[int]] = {}
    for feed in library.values():
        for text in {feed.name, f"{feed.name} — {feed.description}" if feed.description else feed.name}:
            ids = out.setdefault(_plain(text), [])
            if feed.id not in ids:
                ids.append(feed.id)
    return out


def _rows(text: str) -> tuple[list[str], list[tuple[int, list[str]]]]:
    """Cabeçalho (campos conhecidos, ``""`` nos demais) e as linhas de dados com o número da linha no arquivo."""
    text = text.lstrip("﻿")
    first = next((line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")), "")
    delimiter = ";" if first.count(";") > first.count(",") else "\t" if first.count("\t") > first.count(",") else ","
    reader = csv.reader(io.StringIO(text), delimiter=delimiter)
    header: list[str] | None = None
    rows: list[tuple[int, list[str]]] = []
    for line_number, row in enumerate(reader, 1):
        if not row or not any(cell.strip() for cell in row) or row[0].lstrip().startswith("#"):
            continue
        if header is None:
            header = [COLUMN_ALIASES.get(_plain(cell).replace(" ", "_"), "") for cell in row]
            continue
        rows.append((line_number, row))
    if header is None:
        raise ValueError("O arquivo está vazio")
    return header, rows


def import_prices(standard: str | None, text: str, default_fx: float | None = None) -> dict[str, Any]:
    """Preços em US$/kg de MS por id do RuFaS, mais o que não pôde ser lido.

    Colunas (cabeçalho obrigatório; ordem livre): ``id`` ou ``alimento`` (um dos dois), ``preco`` e, opcionais, ``moeda``
    (``USD`` ou ``BRL``; padrão USD), ``cambio`` (R$ por US$), ``unidade_kg`` (kg por unidade comercial; padrão 1), ``base``
    (``MS`` ou ``MN``; padrão MS) e ``fonte``. Separador ``,``, ``;`` ou tabulação; vírgula decimal aceita.
    """
    code = get_standard(standard).code
    library = feed_library(code)
    names = _names(library)
    if default_fx is not None and (not math.isfinite(default_fx) or default_fx <= 0):
        raise ValueError("O câmbio deve ser um número maior que zero (R$ por US$)")
    header, rows = _rows(text)
    if "price" not in header:
        raise ValueError("Falta a coluna de preço (preco)")
    if "id" not in header and "name" not in header:
        raise ValueError("Falta a coluna de identificação: id (do RuFaS) ou alimento")
    if len(rows) > MAX_ROWS:
        raise ValueError(f"No máximo {MAX_ROWS} linhas por arquivo")

    items: dict[int, dict[str, Any]] = {}
    problems: list[Problem] = []
    warnings: list[str] = []
    for line, cells in rows:
        raw = {field: cells[i].strip() for i, field in enumerate(header) if field and i < len(cells)}
        shown = ", ".join(cell.strip() for cell in cells)
        try:
            feed = _find_feed(raw, library, names, code)
            price, note = _convert(raw, feed, default_fx)
        except ValueError as exc:
            problems.append(Problem(line, shown, str(exc)))
            continue
        if feed.id in items:
            warnings.append(f"Linha {line}: {feed.name} já veio na linha {items[feed.id]['line']}; vale a última.")
        items[feed.id] = {"line": line, "id": feed.id, "name": feed.name, "price": price, "original": note, "source": raw.get("source", "")}
    return {
        "standard": code,
        "prices": {str(i): item["price"] for i, item in items.items()},
        "items": sorted(items.values(), key=lambda item: item["line"]),
        "problems": [problem.__dict__ for problem in problems],
        "warnings": warnings,
    }


def _find_feed(raw: Mapping[str, str], library: Mapping[int, FeedInfo], names: Mapping[str, list[int]], code: str) -> FeedInfo:
    if raw.get("id"):
        try:
            feed_id = int(float(raw["id"].replace(",", ".")))
        except ValueError:
            raise ValueError(f"id inválido: {raw['id']!r}") from None
        if feed_id not in library:
            raise ValueError(f"o id {feed_id} não existe na biblioteca {code}")
        return library[feed_id]
    if raw.get("name"):
        ids = names.get(_plain(raw["name"]), [])
        if not ids:
            raise ValueError(f"alimento {raw['name']!r} não encontrado na biblioteca {code} (use o id do RuFaS)")
        if len(ids) > 1:
            raise ValueError(f"o nome {raw['name']!r} serve a mais de um alimento (ids {sorted(ids)}); use o id do RuFaS")
        return library[ids[0]]
    raise ValueError("linha sem id nem nome do alimento")


def _convert(raw: Mapping[str, str], feed: FeedInfo, default_fx: float | None) -> tuple[float, str]:
    """Preço em US$/kg de MS e a descrição do valor original."""
    try:
        value = _number(raw.get("price", ""))
    except ValueError:
        raise ValueError(f"preço inválido: {raw.get('price', '')!r}") from None
    if value < 0:
        raise ValueError("o preço não pode ser negativo")
    currency = CURRENCIES.get(_plain(raw.get("currency") or "USD").upper())
    if currency is None:
        raise ValueError(f"moeda desconhecida: {raw['currency']!r} (use USD ou BRL)")
    basis = BASES.get(_plain(raw.get("basis") or "MS").upper())
    if basis is None:
        raise ValueError(f"base desconhecida: {raw['basis']!r} (use MS ou MN)")
    try:
        unit_kg = _number(raw["unit_kg"]) if raw.get("unit_kg") else 1.0
    except ValueError:
        raise ValueError(f"kg por unidade inválido: {raw['unit_kg']!r}") from None
    if unit_kg <= 0:
        raise ValueError("os kg por unidade devem ser maiores que zero")
    price = value / unit_kg
    if basis == "MN":
        if feed.dm <= 0:
            raise ValueError(f"{feed.name} não tem teor de matéria seca na biblioteca para converter da matéria natural")
        price /= feed.dm / 100
    if currency == "BRL":
        try:
            fx = _number(raw["fx"]) if raw.get("fx") else default_fx
        except ValueError:
            raise ValueError(f"câmbio inválido: {raw['fx']!r}") from None
        if not fx or fx <= 0:
            raise ValueError("preço em reais sem câmbio (coluna cambio ou o campo de câmbio da tela)")
        price /= fx
    unit = f" por {unit_kg:g} kg" if unit_kg != 1 else " por kg"
    return price, f"{value:g} {currency}{unit} ({basis})"
