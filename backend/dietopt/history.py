"""Histórico de execuções (D3): cada simulação, análise de sensibilidade, avaliação de dietas e dieta ótima fica gravada em disco.

Cada execução vira dois arquivos em ``runs/_history``: ``<id>.json`` (parâmetros e resultado completos) e ``<id>.meta.json`` (título,
tipo, estado e um resumo pequeno), para listar sem abrir os resultados grandes. Uma execução por tipo pode ser o **cenário-base**,
a referência dos deltas dos indicadores. O histórico guarda no máximo ``MAX_RUNS`` execuções: ao passar disso apaga as mais antigas
que não sejam base.

Cada execução pode ter um **nome** e uma **nota** (editáveis). As pastas de saída do RuFaS (``runs/web_*``) não fazem parte do
histórico: ficam no disco até o usuário pedir a limpeza (``clean_folders``).
"""

from __future__ import annotations

import itertools
import json
import re
import shutil
import threading
import time
from pathlib import Path
from typing import Any, Callable, Mapping

from .herd import DEFAULT_COWS
from .jobs import Cancelled, Job
from .paths import RUNS_DIR

HISTORY_DIR = RUNS_DIR / "_history"
MAX_RUNS = 200
KINDS = ("simulation", "sensitivity", "evaluation", "optimization")
KIND_LABELS = {"simulation": "Simulação do RuFaS", "sensitivity": "Sensibilidade", "evaluation": "Avaliação de dietas", "optimization": "Dieta ótima"}
_ID = re.compile(r"^\d{8}-\d{6}-[0-9a-f]{4}$")
_FOLDER = re.compile(r"^web_[0-9a-f]{10}(_s\d{3})?$")  # pastas das simulações da interface (uma por tarefa ou por cenário da sensibilidade)
BASE_KIND = "simulation"  # só a base das simulações é usada pelas telas (indicadores da Vaca leiteira e da Sensibilidade)
MAX_NAME, MAX_NOTE = 80, 500
_LOCK = threading.RLock()
_SEQUENCE = itertools.count()  # desempata execuções do mesmo segundo: o identificador cresce com a ordem de gravação


# ---------------------------------------------------------------------------------------------------------------
# Resumo de cada tipo (o que a tabela mostra sem abrir o resultado)
# ---------------------------------------------------------------------------------------------------------------
def _simulation(params: Mapping[str, Any], result: Mapping[str, Any]) -> tuple[str, dict[str, Any], str]:
    s = result["summary"]
    n_feeds, years = len(params.get("feeds", [])), int(params.get("years", 1))
    summary = {
        "margem": s["margem"], "receita": s["receita"], "custo_alimentacao": s["custo_alimentacao"], "custo_vaca_dia": s["custo_vaca_dia"],
        "leite_kg": s["leite_kg"], "milk_price": s["milk_price"], "years": years, "n_feeds": n_feeds, "cow_num": s.get("cow_num", 100),
        "alertas": (result.get("checks_summary") or {}).get("alert", 0),
    }  # fmt: skip
    cows = s.get("cow_num", 100)
    herd = f" · {cows} vacas" if cows != 100 else ""  # o rebanho padrão não aparece no título
    return f"{n_feeds} alimentos · {years} ano{'s' if years > 1 else ''}{herd}", summary, ""


def _cows(params: Mapping[str, Any]) -> int:
    try:
        return int(params.get("cow_num") or DEFAULT_COWS)
    except (TypeError, ValueError):
        return DEFAULT_COWS


def _sensitivity(params: Mapping[str, Any], result: Mapping[str, Any]) -> tuple[str, dict[str, Any], str]:
    values = [r["Res"] for r in result["rows"] if r.get("Res") is not None]
    years, cows = int(params.get("years", 1)), _cows(params)
    summary = {
        "n_scenarios": len(result["rows"]), "n_ok": len(values), "best": max(values, default=None), "worst": min(values, default=None),
        "n_factors": len(params.get("factors", [])), "method": params.get("method", "grid"), "years": years, "cow_num": cows,
    }  # fmt: skip
    herd = f" · {cows} vacas" if cows != DEFAULT_COWS else ""
    return f"{len(result['rows'])} cenários · {len(params.get('factors', []))} fatores · {years} ano{'s' if years > 1 else ''}{herd}", summary, ""


def _evaluation(params: Mapping[str, Any], result: Mapping[str, Any]) -> tuple[str, dict[str, Any], str]:
    diets = result["diets"]
    best = next((d for d in diets if d["name"] == result.get("best")), None)
    summary = {
        "standard": result["standard"], "category": result["category"], "n_diets": len(diets), "n_feasible": sum(d["feasible"] for d in diets),
        "best": result.get("best"), "best_cost": best["cost"] if best else None,
    }  # fmt: skip
    return f"{len(diets)} dietas · {result['standard']}", summary, " ".join(d["name"] for d in diets)


def _optimization(params: Mapping[str, Any], result: Mapping[str, Any]) -> tuple[str, dict[str, Any], str]:
    diet = result.get("diet") or {}
    summary = {
        "standard": result["standard"], "category": result["category"], "status": result["status"], "cost": diet.get("cost"),
        "gap_pct": (result.get("rufas") or {}).get("lp_gap_pct"), "resolution": result.get("resolution"), "n_feeds": len(result.get("feed_ids", [])),
    }  # fmt: skip
    return f"{len(result.get('feed_ids', []))} alimentos · {result['standard']}", summary, ""


SUMMARIZERS: Mapping[str, Callable[[Mapping[str, Any], Mapping[str, Any]], tuple[str, dict[str, Any], str]]] = {
    "simulation": _simulation, "sensitivity": _sensitivity, "evaluation": _evaluation, "optimization": _optimization,
}  # fmt: skip


# ---------------------------------------------------------------------------------------------------------------
# Arquivos
# ---------------------------------------------------------------------------------------------------------------
def _check_id(run_id: str) -> str:
    if not isinstance(run_id, str) or not _ID.match(run_id):
        raise ValueError(f"Identificador de execução inválido: {run_id!r}")
    return run_id


def _paths(run_id: str) -> tuple[Path, Path]:
    return HISTORY_DIR / f"{run_id}.json", HISTORY_DIR / f"{run_id}.meta.json"


def _write(path: Path, data: Any) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":"), default=str), encoding="utf-8")
    temp.replace(path)  # troca atômica: quem lista nunca vê um arquivo pela metade


def _read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _public(data: Mapping[str, Any]) -> dict[str, Any]:
    """Sem os campos só de busca."""
    return {k: v for k, v in data.items() if k not in ("search", "search_base")}


def _metas() -> list[dict[str, Any]]:
    if not HISTORY_DIR.exists():
        return []
    metas = []
    for path in HISTORY_DIR.glob("*.meta.json"):
        try:
            metas.append(_read(path))
        except (OSError, json.JSONDecodeError):
            continue  # arquivo corrompido ou sendo escrito: fica de fora da lista
    return sorted(metas, key=lambda meta: meta["id"], reverse=True)


# ---------------------------------------------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------------------------------------------
def record(kind: str, params: Mapping[str, Any], result: Mapping[str, Any] | None, error: str | None = None) -> dict[str, Any]:
    """Grava uma execução (``result`` ``None`` com ``error`` = execução que falhou) e devolve os metadados."""
    if kind not in KINDS:
        raise ValueError(f"Tipo de execução desconhecido: {kind!r}")
    detail, summary, search = SUMMARIZERS[kind](params, result) if result is not None else ("falhou", {}, "")
    now = time.time()
    meta = {
        "id": f"{time.strftime('%Y%m%d-%H%M%S', time.localtime(now))}-{next(_SEQUENCE) % 0x10000:04x}",
        "kind": kind,
        "created": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now)),
        "title": f"{KIND_LABELS[kind]} · {detail}",
        "status": "error" if result is None else "done",
        "error": error.strip().splitlines()[0][:300] if error and error.strip() else None,
        "summary": summary,
        "is_base": False,
        "name": "",
        "note": "",
        "search_base": f"{KIND_LABELS[kind]} {detail} {search}".lower(),  # o que vem da execução; a busca soma o nome e a nota
    }
    meta["search"] = meta["search_base"]
    with _LOCK:
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        full, small = _paths(meta["id"])
        _write(full, {**meta, "params": params, "result": result})
        _write(small, meta)
        _prune()
    return meta


def _prune() -> None:
    metas = _metas()
    for meta in metas[MAX_RUNS:][::-1]:  # as mais antigas primeiro
        if not meta["is_base"]:
            for path in _paths(meta["id"]):
                path.unlink(missing_ok=True)


def list_runs(kind: str | None = None, status: str | None = None, query: str = "", page: int = 1, per_page: int = 10) -> dict[str, Any]:
    """Execuções (mais recentes primeiro) com filtro por tipo e estado, busca por texto e paginação."""
    if kind not in (None, "") and kind not in KINDS:
        raise ValueError(f"Tipo de execução desconhecido: {kind!r}")
    if status not in (None, "", "done", "error"):
        raise ValueError(f"Estado desconhecido: {status!r}")
    if not 1 <= per_page <= 100 or page < 1:
        raise ValueError("Página ou tamanho de página inválido")
    terms = query.lower().split()
    with _LOCK:
        metas = [
            m for m in _metas()
            if (not kind or m["kind"] == kind) and (not status or m["status"] == status) and all(t in m["search"] or t in m["id"] for t in terms)
        ]  # fmt: skip
    start = (page - 1) * per_page
    items = [_public(m) for m in metas[start : start + per_page]]
    return {"items": items, "total": len(metas), "page": page, "per_page": per_page, "pages": max(1, -(-len(metas) // per_page))}


def get_run(run_id: str) -> dict[str, Any]:
    full, _ = _paths(_check_id(run_id))
    with _LOCK:
        if not full.exists():
            raise ValueError(f"Execução não encontrada: {run_id}")
        data = _read(full)
    return _public(data)


def delete_run(run_id: str) -> None:
    paths = _paths(_check_id(run_id))
    with _LOCK:
        if not paths[0].exists():
            raise ValueError(f"Execução não encontrada: {run_id}")
        for path in paths:
            path.unlink(missing_ok=True)


def set_base(run_id: str, value: bool = True) -> dict[str, Any]:
    """Marca (ou desmarca) a simulação como cenário-base; só uma pode ser a base. Desmarcar vale para qualquer tipo."""
    full, small = _paths(_check_id(run_id))
    with _LOCK:
        if not full.exists():
            raise ValueError(f"Execução não encontrada: {run_id}")
        meta = _read(small)
        if value and meta["kind"] != BASE_KIND:
            raise ValueError("Só uma simulação pode ser o cenário-base: as outras execuções não usam base")
        if value and meta["status"] != "done":
            raise ValueError("Só uma execução concluída pode ser o cenário-base")
        if value:
            for other in _metas():
                if other["kind"] == meta["kind"] and other["is_base"] and other["id"] != run_id:
                    _write(_paths(other["id"])[1], {**other, "is_base": False})
                    data = _read(_paths(other["id"])[0])
                    _write(_paths(other["id"])[0], {**data, "is_base": False})
        meta["is_base"] = bool(value)
        _write(small, meta)
        _write(full, {**_read(full), "is_base": meta["is_base"]})
    return _public(meta)


def _text(value: Any, label: str, limit: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{label}: texto esperado")
    text = " ".join(value.split()) if label == "Nome" else value.strip()  # o nome fica numa linha só; a nota pode ter parágrafos
    if len(text) > limit:
        raise ValueError(f"{label}: no máximo {limit} caracteres (recebido {len(text)})")
    return text


def update_run(run_id: str, name: Any = None, note: Any = None) -> dict[str, Any]:
    """Muda o nome e/ou a nota da execução (``None`` mantém; texto vazio apaga)."""
    full, small = _paths(_check_id(run_id))
    new = {"name": None if name is None else _text(name, "Nome", MAX_NAME), "note": None if note is None else _text(note, "Nota", MAX_NOTE)}
    with _LOCK:
        if not full.exists():
            raise ValueError(f"Execução não encontrada: {run_id}")
        meta = _read(small)
        meta.update({k: v for k, v in new.items() if v is not None})
        base = meta.get("search_base", meta["search"])
        meta["search_base"] = base
        meta["search"] = " ".join(filter(None, (base, meta.get("name", "").lower(), meta.get("note", "").lower())))
        _write(small, meta)
        _write(full, {**_read(full), **meta})
    return _public(meta)


def base_run(kind: str) -> dict[str, Any] | None:
    """Metadados (com o resumo) do cenário-base do tipo, ou ``None``."""
    if kind not in KINDS:
        raise ValueError(f"Tipo de execução desconhecido: {kind!r}")
    with _LOCK:
        return next((_public(m) for m in _metas() if m["kind"] == kind and m["is_base"]), None)


# ---------------------------------------------------------------------------------------------------------------
# Pastas de saída do RuFaS (runs/web_*)
# ---------------------------------------------------------------------------------------------------------------
def _folders() -> list[Path]:
    if not RUNS_DIR.exists():
        return []
    return [p for p in RUNS_DIR.iterdir() if p.is_dir() and _FOLDER.match(p.name)]


def _size(folder: Path) -> int:
    total = 0
    for path in folder.rglob("*"):
        try:
            if path.is_file():
                total += path.stat().st_size
        except OSError:
            continue  # arquivo que sumiu durante a contagem
    return total


def storage_report() -> dict[str, int]:
    """Quantas pastas de simulação da interface há em ``runs/`` e quanto espaço ocupam (o histórico em si é pequeno)."""
    folders = _folders()
    history = sum(p.stat().st_size for p in HISTORY_DIR.glob("*.json")) if HISTORY_DIR.exists() else 0
    return {"folders": len(folders), "folders_bytes": sum(_size(p) for p in folders), "history_bytes": history}


def clean_folders() -> dict[str, int]:
    """Apaga as pastas ``runs/web_*`` (entradas, logs e saídas brutas do RuFaS). Não toca no histórico nem no cache de resultados:
    os resultados das execuções continuam abertos, e rodar o mesmo cenário de novo reaproveita o cache."""
    removed = failed = freed = 0
    for folder in _folders():
        size = _size(folder)
        shutil.rmtree(folder, ignore_errors=True)
        if folder.exists():
            failed += 1
        else:
            removed, freed = removed + 1, freed + size
    return {"removed": removed, "failed": failed, "freed_bytes": freed}


# ---------------------------------------------------------------------------------------------------------------
# Integração com as tarefas
# ---------------------------------------------------------------------------------------------------------------
def with_history(kind: str, work: Callable[[Job], dict[str, Any]]) -> Callable[[Job], dict[str, Any]]:
    """Envolve o trabalho de uma tarefa: grava o resultado (ou a falha) no histórico e devolve o resultado com ``run_id``."""

    def run(job: Job) -> dict[str, Any]:
        try:
            result = work(job)
        except (Cancelled, ValueError):
            raise  # cancelar não é execução; ValueError é pedido recusado na validação (parâmetros inválidos), que também não é
        except Exception as exc:  # noqa: BLE001 - a falha do RuFaS também é uma execução (com o motivo)
            record(kind, job.params, None, f"{type(exc).__name__}: {exc}")
            raise
        return {**result, "run_id": record(kind, job.params, result)["id"]}

    return run
