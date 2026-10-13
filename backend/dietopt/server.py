"""Servidor web local (apenas biblioteca padrão): API JSON + arquivos estáticos do front-end.

    python -m dietopt.server [--port 8000]
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import mimetypes
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from . import lactation
from .diet_lp import Food, NutrientBounds, solve_diet
from .feeds import load_feed_library
from .jobs import Job, JobManager
from .rufas_adapter import PROJECT_ROOT, Scenario
from .scenarios import DEFAULT_MILK_PRICE, DEFAULT_PRICES, Economics, evaluate
from .sensitivity import Factor, run_sensitivity

FRONTEND = PROJECT_ROOT / "frontend"
JOBS = JobManager()
FEEDS = {feed.id: feed for feed in load_feed_library()}


def clean(value: Any) -> Any:
    """Troca NaN/inf por None para o JSON ser válido."""
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    return value


# ----------------------------------------------------------------------------------------------------------------
# Exercício do quadro (PL rápido)
# ----------------------------------------------------------------------------------------------------------------
def toy_problem(payload: dict[str, Any]) -> dict[str, Any]:
    foods = [
        Food(f["name"], float(f["cost"]), {k: float(v) for k, v in f["nutrients"].items()}, float(f.get("max", math.inf)))
        for f in payload["foods"]
    ]
    bounds = {n: NutrientBounds(float(b["min"]), float(b.get("max", math.inf))) for n, b in payload["bounds"].items()}
    result = solve_diet(foods, bounds)
    return {
        "feasible": result.feasible,
        "status": result.status,
        "cost": result.cost,
        "amounts": result.amounts,
        "nutrient_totals": result.nutrient_totals,
        "shadow_prices": result.shadow_prices,
        "reduced_costs": result.reduced_costs,
    }


def toy_sensitivity(payload: dict[str, Any]) -> dict[str, Any]:
    """Tabela de cenários do quadro: varia custos e limites de nutrientes e registra o custo ótimo (``Res``)."""
    factors = payload["factors"]  # [{"target": "cost:Arroz" | "min:Proteina" | "max:Carboidrato", "low", "high", "n"}]
    levels = [
        [f["low"] + (f["high"] - f["low"]) * i / max(f["n"] - 1, 1) for i in range(f["n"])] for f in factors
    ]
    rows = []
    for index, point in enumerate(itertools.product(*levels), start=1):
        scenario = json.loads(json.dumps(payload["problem"]))
        for factor, value in zip(factors, point):
            kind, name = factor["target"].split(":", 1)
            if kind == "cost":
                next(f for f in scenario["foods"] if f["name"] == name)["cost"] = value
            else:
                scenario["bounds"][name][kind] = value
        solved = toy_problem(scenario)
        row: dict[str, Any] = {"cenario": f"S{index}"}
        for factor, value in zip(factors, point):
            row[factor["target"]] = round(value, 4)
        row["Res"] = round(solved["cost"], 4) if solved["feasible"] else None
        row["amounts"] = {k: round(v, 4) for k, v in solved["amounts"].items()}
        rows.append(row)
    return {"columns": [f["target"] for f in factors] + ["Res"], "rows": rows}


# ----------------------------------------------------------------------------------------------------------------
# Simulações do RuFaS
# ----------------------------------------------------------------------------------------------------------------
def feed_limits_from(params: dict[str, Any]) -> dict[int, tuple[float, float]]:
    """Limites de inclusão: os informados pelo usuário, ou os tetos padrão do tipo de alimento."""
    given = {int(k): (float(v[0]), float(v[1])) for k, v in (params.get("limits") or {}).items()}
    limits = {}
    for feed_id in params["feeds"]:
        feed = FEEDS.get(int(feed_id))
        default = (0.0, feed.default_max if feed else 100.0)
        limits[int(feed_id)] = given.get(int(feed_id), default)
    return limits


def scenario_from(params: dict[str, Any], name: str) -> tuple[Scenario, Economics]:
    prices = {int(k): float(v) for k, v in (params.get("prices") or {}).items()}
    milk_price = float(params.get("milk_price", DEFAULT_MILK_PRICE))
    years = max(1, min(int(params.get("years", 1)), 3))
    scenario = Scenario(
        name=name,
        end_date=f"{2012 + years}:365",
        random_seed=int(params.get("seed", 42)),
        nutrient_standard="NRC",
        cow_num=params.get("cow_num"),
        lac_cow_feeds=[int(i) for i in params["feeds"]],
        feed_limits=feed_limits_from(params),
        feed_prices=prices,
        # Quando a ração não atende às exigências, o RuFaS reduz o leite (0,25 kg por tentativa) até este limite e,
        # passando dele, aborta. Um limite maior deixa a simulação degradar e a margem refletir o leite perdido.
        milk_reduction_maximum=float(params.get("max_milk_reduction", 5.0)),
    )
    economics = Economics(milk_price=milk_price, prices={**DEFAULT_PRICES, **prices})
    return scenario, economics


def feed_label(feed_id: int | str) -> str:
    feed = FEEDS.get(int(feed_id))
    return f"{feed.name} — {feed.description}" if feed else str(feed_id)


def simulation_payload(scenario: Scenario, economics: Economics) -> dict[str, Any]:
    evaluation = evaluate(scenario, economics)
    if not evaluation.ok or evaluation.result is None:
        raise RuntimeError(f"Simulação do RuFaS falhou: {evaluation.detail}")
    result = evaluation.result
    prices = {**DEFAULT_PRICES, **scenario.feed_prices}
    feed_ids = sorted({fid for ration in result.ration_kg_per_cow for fid in ration if fid != "dry_matter_intake_total"}, key=int)
    curves = lactation.lactation_curve(result.wood or None)
    return {
        "summary": evaluation.as_row() | {"milk_price": economics.milk_price, "reducao_leite": evaluation.reduction, "max_reducao": scenario.milk_reduction_maximum},
        "feeds": [{"id": int(i), "label": feed_label(i), "price": prices.get(int(i))} for i in feed_ids],
        "daily": {"day": result.days, "milk_kg": result.milk_kg, "milking_cows": result.milking_cows, "avg_dim": result.avg_dim},
        "intervals": {
            "day": result.interval_days,
            "ration": result.ration_kg_per_cow,
            "cows": result.cows_in_pen,
            "requirements": [
                {k: r.get(k) for k in ("NEl_requirement", "NEmaint_requirement", "MP_requirement", "Ca_requirement", "P_req", "DMIest_requirement", "avg_BW")}
                for r in result.requirements
            ],
            "cost_per_cow_day": [
                sum(kg * prices.get(int(fid), 0.0) for fid, kg in ration.items() if fid != "dry_matter_intake_total")
                for ration in result.ration_kg_per_cow
            ],
        },
        "lactation": {
            "curves": curves,
            "wood": result.wood or lactation.DEFAULT_WOOD,
            "wood_from_rufas": bool(result.wood),
            "milestones": lactation.milestones(),
        },
        "average_ration": evaluation.ration,
    }


def simulate_work(job: Job) -> dict[str, Any]:
    scenario, economics = scenario_from(job.params, f"web_{job.id}")
    job.total = 1
    payload = simulation_payload(scenario, economics)
    job.done = 1
    return payload


def sensitivity_work(job: Job) -> dict[str, Any]:
    scenario, economics = scenario_from(job.params, f"web_{job.id}")
    factors = [Factor(str(f["key"]), str(f["label"]), float(f["low"]), float(f["high"])) for f in job.params["factors"]]

    def progress(done: int, total: int) -> None:
        job.done, job.total = done, total

    return run_sensitivity(
        scenario,
        factors,
        economics,
        method=job.params.get("method", "grid"),
        n=int(job.params.get("n", 2)),
        workers=int(job.params.get("workers", 2)),
        on_progress=progress,
    ) | {"feeds": [{"id": int(i), "label": feed_label(i)} for i in job.params["feeds"]]}


# ----------------------------------------------------------------------------------------------------------------
# HTTP
# ----------------------------------------------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "DietOpt/1.0"

    def log_message(self, fmt: str, *args: Any) -> None:  # silencia o log de cada requisição
        pass

    _head_only = False

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not self._head_only:
            self.wfile.write(body)

    def do_HEAD(self) -> None:  # noqa: N802 - o Next.js pré-carrega rotas com HEAD
        self._head_only = True
        self.do_GET()

    def _json(self, data: Any, status: int = 200) -> None:
        self._send(status, json.dumps(clean(data), ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def _body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(length) or b"{}")

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            if path == "/api/feeds":
                return self._json(
                    [
                        {**feed.__dict__, "nel": round(feed.nel_mcal_per_kg, 3), "default_max": feed.default_max}
                        for feed in sorted(FEEDS.values(), key=lambda f: (f.kind, f.name))
                    ]
                )
            if path == "/api/defaults":
                return self._json({"milk_price": DEFAULT_MILK_PRICE, "prices": DEFAULT_PRICES})
            if path == "/api/lactation":
                return self._json(
                    {
                        "curves": lactation.lactation_curve(None),
                        "wood": lactation.DEFAULT_WOOD,
                        "milestones": lactation.milestones(),
                    }
                )
            if path == "/api/jobs":
                return self._json(JOBS.list())
            if path.startswith("/api/jobs/"):
                job = JOBS.get(path.rsplit("/", 1)[-1])
                return self._json(job.public()) if job else self._json({"error": "job não encontrado"}, 404)
            return self._static(path)
        except Exception as exc:  # noqa: BLE001
            self._json({"error": f"{type(exc).__name__}: {exc}"}, 500)

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        try:
            body = self._body()
            if path == "/api/toy":
                return self._json(toy_problem(body))
            if path == "/api/toy/sensitivity":
                return self._json(toy_sensitivity(body))
            if path == "/api/jobs/simulate":
                return self._json(JOBS.submit("simulate", body, simulate_work).public(include_result=False), 202)
            if path == "/api/jobs/sensitivity":
                return self._json(JOBS.submit("sensitivity", body, sensitivity_work).public(include_result=False), 202)
            self._json({"error": "rota não encontrada"}, 404)
        except Exception as exc:  # noqa: BLE001
            self._json({"error": f"{type(exc).__name__}: {exc}"}, 500)

    def _static(self, path: str) -> None:
        target = (FRONTEND / ("index.html" if path in ("", "/") else path.lstrip("/"))).resolve()
        if target.is_dir():  # o export estático do Next.js gera /vaca/index.html
            target = target / "index.html"
        if not target.is_file() and target.name.endswith(".__PAGE__.txt"):
            # No Windows o export grava `__next.vaca/__PAGE__.txt`, mas o navegador pede `__next.vaca.__PAGE__.txt`.
            target = target.with_name(target.name.removesuffix(".__PAGE__.txt")) / "__PAGE__.txt"
        if FRONTEND.resolve() not in target.parents and target != FRONTEND.resolve() or not target.is_file():
            return self._send(404, b"nao encontrado", "text/plain; charset=utf-8")
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type in ("application/javascript", "application/json"):
            content_type += "; charset=utf-8"
        self._send(200, target.read_bytes(), content_type)


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor local do otimizador de dieta com RuFaS")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Servidor em http://{args.host}:{args.port}  (Ctrl+C para parar)", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
