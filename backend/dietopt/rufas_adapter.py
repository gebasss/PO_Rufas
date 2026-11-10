"""Adaptador que usa o RuFaS (vendor/RuFaS) como simulador.

Cada cenário vira uma pasta em ``runs/<id>/`` com cópias editadas dos arquivos de entrada, um metadata e um arquivo
de tasks próprios. O RuFaS roda em um subprocesso com ``vendor/RuFaS`` como diretório de trabalho (ele só entende
caminhos relativos a esse diretório) e os resultados são lidos dos JSONs gerados pelos filtros de saída.

Observação importante: o validador de caminhos do RuFaS rejeita caracteres acentuados (``[a-zA-Z0-9_\\-\\. ]``).
Por isso todo caminho passado ao RuFaS é *relativo* a ``vendor/RuFaS``.
"""

from __future__ import annotations

import copy
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .herd import scale_herd
from .paths import INPUT, PROJECT_ROOT, PYTHON, RUFAS_DIR, RUNS_DIR
from .standards import NASEM_ONLY_TO_NRC, get_standard

EXAMPLE = "freestall"  # exemplo do RuFaS usado como base dos cenários


def rel(path: Path) -> str:
    """Caminho relativo a vendor/RuFaS, com barras normais (e barra final para pastas)."""
    text = os.path.relpath(path, RUFAS_DIR).replace("\\", "/")
    return text + "/" if path.suffix == "" else text


def remap_feed_ids(node: Any, mapping: dict[int, int], key: str | None = None) -> Any:
    """Troca ids de alimentos em todo o JSON de alimentos (listas de ids e campos que guardam um id)."""
    id_fields = {"feed_type", "purchased_feed"}
    if isinstance(node, dict):
        return {k: remap_feed_ids(v, mapping, k) for k, v in node.items()}
    if isinstance(node, list):
        return [remap_feed_ids(v, mapping, key) for v in node]
    if isinstance(node, int) and not isinstance(node, bool) and (key in id_fields or key and key.endswith("_feeds")):
        return mapping.get(node, node)
    return node


def write_feed_library(path: Path, scenario: "Scenario") -> None:
    """Copia a biblioteca do padrão do cenário aplicando os limites de inclusão (``limit``/``lower_limit``)."""
    standard = get_standard(scenario.nutrient_standard)
    with open(standard.library_path, encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    for row in rows:
        feed_id = int(float(row["rufas_id"]))
        if feed_id in scenario.feed_limits:
            lower, upper = scenario.feed_limits[feed_id]
            row["lower_limit"], row["limit"] = str(lower), str(upper)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: Path, content: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(content, handle, indent=2, ensure_ascii=False)


@dataclass
class Scenario:
    """Parâmetros de um cenário. ``None`` mantém o valor do exemplo do RuFaS."""

    name: str
    start_date: str = "2013:1"
    end_date: str = "2013:365"
    random_seed: int = 42
    nutrient_standard: str = "NRC"  # "NRC" ou "NASEM"
    cow_num: int | None = None  # vacas do rebanho; o rebanho todo é escalado junto (``herd.py``)
    # Ração das vacas em lactação: {rufas_id: percentual da MS}. Se None, o RuFaS formula a ração (otimizador próprio).
    lac_cow_ration: dict[int, float] | None = None
    ration_tolerance: float | None = None
    # Alimentos que o otimizador do RuFaS pode usar para as vacas em lactação (ignorado se lac_cow_ration for dado).
    lac_cow_feeds: list[int] | None = None
    # Limites de inclusão por alimento, em kg por animal por dia (unidade de limit/lower_limit no RuFaS).
    feed_limits: dict[int, tuple[float, float]] = field(default_factory=dict)
    feed_prices: dict[int, float] = field(default_factory=dict)  # rufas_id -> $/kg
    milk_reduction_maximum: float | None = None
    filters: dict[str, list[str]] = field(default_factory=dict)  # nome do filtro -> regexes


def build_scenario(scenario: Scenario, runs_dir: Path = RUNS_DIR) -> Path:
    """Escreve os arquivos de entrada do cenário e devolve o caminho do metadata do Task Manager."""
    base = runs_dir / scenario.name
    if base.exists():
        shutil.rmtree(base)
    (base / "filters").mkdir(parents=True)

    config = load_json(INPUT / "data" / "config" / f"example_{EXAMPLE}_config.json")
    config["start_date"] = scenario.start_date
    config["end_date"] = scenario.end_date
    config["random_seed"] = scenario.random_seed
    standard = get_standard(scenario.nutrient_standard)
    config["nutrient_standard"] = standard.code
    dump_json(base / "config.json", config)

    animal = load_json(INPUT / "data" / "animal" / f"example_{EXAMPLE}_animal.json")
    if scenario.cow_num is not None:
        animal = scale_herd(animal, scenario.cow_num)
    animal["ration"]["user_input"] = scenario.lac_cow_ration is not None
    dump_json(base / "animal.json", animal)

    feed = load_json(INPUT / "data" / "feed" / "example_Midwest_feed.json")
    if standard.id_remap:
        feed = remap_feed_ids(feed, standard.id_remap)
    if scenario.lac_cow_ration is not None:
        feed["lac_cow_feeds"] = sorted(scenario.lac_cow_ration)
        feed["user_defined_ration_percentages"]["lac_cow"] = [
            {"feed_type": fid, "ration_percentage": pct} for fid, pct in scenario.lac_cow_ration.items()
        ]
        if scenario.ration_tolerance is not None:
            feed["user_defined_ration_percentages"]["tolerance"] = scenario.ration_tolerance
    if scenario.lac_cow_feeds is not None and scenario.lac_cow_ration is None:
        feed["lac_cow_feeds"] = sorted(scenario.lac_cow_feeds)
    known = {p["purchased_feed"] for p in feed["purchased_feeds"]}
    for fid, price in scenario.feed_prices.items():
        if fid in known:
            for p in feed["purchased_feeds"]:
                if p["purchased_feed"] == fid:
                    p["purchased_feed_cost"] = price
        else:
            feed["purchased_feeds"].append({"purchased_feed": fid, "purchased_feed_cost": price, "buffer": 0.15})
            feed["allowances"].append(
                {
                    "purchased_feed": fid,
                    "runtime_purchase_allowance": 1000.0,
                    "advance_purchase_allowance": 1000.0,
                    "planning_cycle_allowance": 1000.0,
                }
            )
    if scenario.milk_reduction_maximum is not None:
        feed["milk_reduction_maximum"] = scenario.milk_reduction_maximum
    dump_json(base / "feed.json", feed)
    library = base / standard.library_file
    write_feed_library(library, scenario)

    metadata = load_json(INPUT / "metadata" / f"example_{EXAMPLE}_dairy_metadata.json")
    metadata["files"]["config"]["path"] = rel(base / "config.json")
    metadata["files"]["animal"]["path"] = rel(base / "animal.json")
    metadata["files"]["feed"]["path"] = rel(base / "feed.json")
    metadata["files"][standard.metadata_key]["path"] = rel(library)
    dump_json(base / "metadata.json", metadata)

    for filter_name, patterns in scenario.filters.items():
        dump_json(base / "filters" / f"json_{filter_name}.json", {"name": filter_name, "filters": patterns})

    tasks = {
        "parallel_workers": 1,
        "tasks": [
            {
                "task_type": "SIMULATION_SINGLE_RUN",
                "metadata_file_path": rel(base / "metadata.json"),
                "output_prefix": scenario.name,
                "log_verbosity": "errors",
                "random_seed": scenario.random_seed,
                "filters_directory": rel(base / "filters"),
                "csv_output_directory": rel(base / "csv"),
                "json_output_directory": rel(base / "json"),
                "report_directory": rel(base / "reports"),
                "graphics_directory": rel(base / "graphics"),
                "logs_directory": rel(base / "logs"),
            }
        ],
    }
    dump_json(base / "tasks.json", tasks)
    task_manager_metadata = load_json(INPUT / "task_manager_metadata.json")
    task_manager_metadata["files"]["tasks"]["path"] = rel(base / "tasks.json")
    dump_json(base / "task_manager_metadata.json", task_manager_metadata)
    return base / "task_manager_metadata.json"


@dataclass
class RunResult:
    scenario: str
    ok: bool
    seconds: float
    folder: Path
    stdout_tail: str = ""

    def read_json_outputs(self) -> dict[str, Any]:
        """Lê todos os JSONs de saída gerados pelos filtros."""
        merged: dict[str, Any] = {}
        for path in sorted((self.folder / "json").glob("*.json")):
            merged[path.name] = load_json(path)
        return merged


def run_scenario(scenario: Scenario, timeout: int = 3600) -> RunResult:
    """Monta e executa o cenário no RuFaS."""
    metadata = build_scenario(scenario)
    folder = RUNS_DIR / scenario.name
    started = time.time()
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    process = subprocess.run(
        [
            str(PYTHON),
            "main.py",
            "-p",
            rel(metadata),
            "-g",
            "-s",
            "-o",
            rel(folder / "out"),
            "-l",
            rel(folder / "tm_logs"),
        ],
        cwd=RUFAS_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        env=env,
    )
    seconds = time.time() - started
    console = (process.stdout or "") + (process.stderr or "")
    (folder / "console.log").write_text(console, encoding="utf-8")
    # O Task Manager sai com código 0 mesmo quando a tarefa falha; o sinal confiável é o resumo da tarefa.
    succeeded = process.returncode == 0 and "Finished task: 1/1 with 0 error(s)" in console
    return RunResult(scenario.name, succeeded, seconds, folder, "" if succeeded else failure_reason(console))


def failure_reason(console: str) -> str:
    """Última mensagem de exceção do log do RuFaS, em uma linha."""
    lines = [line.strip() for line in console.splitlines() if re.match(r"^\w*(Error|Exception)", line.strip())]
    return lines[-1] if lines else console.strip()[-300:]


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "smoke"
    result = run_scenario(Scenario(name=name, filters={"all": [".*"]}, cow_num=20))
    print(f"ok={result.ok} {result.seconds:.1f}s")
    print(result.stdout_tail)
