"""Benchmark v4: o custo da dieta ótima por programação linear (LP) é equivalente ao do SLSQP do RuFaS?

**Pergunta.** Para o MESMO problema (um animal, um cardápio e um conjunto de preços, padrão NASEM 2021), o custo mínimo que o LP acha é
equivalente (dentro de ±``MARGIN_PCT``) ao melhor custo que o SLSQP do RuFaS acha em ``SEEDS`` pontos iniciais aleatórios?

**O mesmo problema.** O SLSQP do RuFaS só aceita o metano entérico e o nitrogênio urinário como constantes; o módulo os calcula da
própria dieta. Para a comparação ser justa, cada caso tem DOIS LPs: o do módulo (emissões da própria dieta) e o "LP nas mesmas constantes"
do SLSQP (as emissões da dieta do módulo, fixas). A comparação PRIMÁRIA é o LP nas mesmas constantes contra o SLSQP: é o mesmo problema, então
a diferença é só de método de busca. As secundárias: o LP do módulo contra o SLSQP conferido também com as emissões da própria dieta, e o custo
de usar emissões consistentes (LP do módulo contra LP nas constantes).

**Caso** = animal × cardápio × conjunto de preços; cada caso chama ``optimize_diet`` (a rota da tela Dieta ótima). O animal é avaliado em UM
dia. Não é uma simulação completa da fazenda (por isso o tamanho do rebanho não entra aqui).

**Casos (sorteados com semente fixa).** 8 animais (4 vacas em lactação, vaca seca, novilha pré-parto e 2 novilhas em crescimento) × ``MENUS``
cardápios sorteados × ``PRICE_SETS`` + 1 conjuntos de preços. Cada cardápio sorteia, de um conjunto de alimentos com preço (os de
``feeds`` com preço padrão mais três alimentos acrescentados), 2 a 3 volumosos, 3 a 6 concentrados e 1 a 2 minerais. Cada preço é o padrão
vezes um fator uniforme de 0,5 a 1,5 (o primeiro conjunto de cada cardápio usa os preços padrão). Os preços são ilustrativos, não são cotações.

**Critério (definido antes de rodar).** Diferença do caso = (custo do LP − melhor custo do SLSQP) / melhor custo do SLSQP, em %. Casos do mesmo
animal e cardápio compartilham exigências e alimentos, então o IC de 90% é um bootstrap por agrupamento (reamostra os grupos animal × cardápio).
O LP é *equivalente* se (1) o IC de 90% da diferença média cabe em ±``MARGIN_PCT`` e (2) ao menos ``SHARE_MIN`` dos casos ficam dentro da margem.

Uso (na pasta backend)::

    ..\\.venv\\Scripts\\python -m dietopt.benchmark run --out ..\\docs\\benchmark\\v4     # retoma o que já foi feito
    ..\\.venv\\Scripts\\python -m dietopt.benchmark report --out ..\\docs\\benchmark\\v4  # só refaz o resumo, os CSVs e o relatório
"""

from __future__ import annotations

import argparse
import csv
import datetime
import json
import math
import platform
import random
import statistics
import subprocess
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
from scipy import stats as sp_stats

VERSION = "v4"
STANDARD = "NASEM"
RESOLUTION = "normal"
SEEDS = 10
MARGIN_PCT = 0.5  # margem de equivalência: 0,5% do custo (desprezível diante de dezenas de % de variação do custo com os preços)
TIE_PCT = 0.1  # abaixo desta diferença (em %) dois custos contam como iguais (a mesma da interface)
SHARE_MIN = 0.95  # fração mínima de casos dentro da margem
BOOTSTRAP_REPS = 10_000
BOOTSTRAP_SEED = 20261201
DESIGN_SEED = 20261201  # sorteia os cardápios e os preços
MENUS = 12
PRICE_SETS = 2  # além do conjunto de preços padrão
PRICE_FACTOR = (0.5, 1.5)  # fator uniforme sobre o preço padrão de cada alimento
MENU_SHAPE = {"Forage": (2, 3), "Conc": (3, 6), "Mineral": (1, 2)}  # intervalo (mín., máx.) de alimentos de cada tipo em um cardápio
EXTRA_FEEDS = {107: 0.22, 163: 0.16, 231: 0.80}  # sem preço padrão na biblioteca; preços ilustrativos (feno de leguminosa, casca de soja, fosfato bicálcico)

_MILK = {"housing": "Barn", "distance": 100}
# animal -> (categoria, tipo de animal, dados do animal)
ANIMALS: dict[str, tuple[str, str, dict[str, Any]]] = {
    "lac-alta": ("LAC_COW", "LAC_COW", dict(body_weight=650, mature_body_weight=700, parity=2, days_in_milk=100, day_of_pregnancy=60, body_condition_score_5=3.0,
                                            calving_interval=400, milk_production=40, milk_fat=3.7, milk_true_protein=3.1, milk_lactose=4.85, **_MILK)),
    "lac-media": ("LAC_COW", "LAC_COW", dict(body_weight=620, mature_body_weight=700, parity=3, days_in_milk=180, day_of_pregnancy=100, body_condition_score_5=3.0,
                                             calving_interval=400, milk_production=30, milk_fat=3.8, milk_true_protein=3.2, milk_lactose=4.85, **_MILK)),
    "lac-final": ("LAC_COW", "LAC_COW", dict(body_weight=680, mature_body_weight=720, parity=4, days_in_milk=280, day_of_pregnancy=200, body_condition_score_5=3.25,
                                             calving_interval=400, milk_production=20, milk_fat=4.0, milk_true_protein=3.3, milk_lactose=4.8, **_MILK)),
    "lac-primipara": ("LAC_COW", "LAC_COW", dict(body_weight=560, mature_body_weight=680, parity=1, days_in_milk=90, day_of_pregnancy=5, body_condition_score_5=3.0,
                                                 calving_interval=400, milk_production=35, milk_fat=3.6, milk_true_protein=3.0, milk_lactose=4.85, **_MILK)),
    "vaca-seca": ("CLOSE_UP", "DRY_COW", dict(body_weight=700, mature_body_weight=720, parity=3, day_of_pregnancy=250, **_MILK)),
    "novilha-pre-parto": ("CLOSE_UP", "HEIFER_III", dict(body_weight=580, mature_body_weight=680, average_daily_gain_heifer=0.7, day_of_pregnancy=240, **_MILK)),
    "novilha-ii": ("GROWING", "HEIFER_II", dict(body_weight=350, mature_body_weight=680, average_daily_gain_heifer=0.8, **_MILK)),
    "novilha-i": ("GROWING", "HEIFER_I", dict(body_weight=180, mature_body_weight=680, average_daily_gain_heifer=0.8, **_MILK)),
}  # fmt: skip


# ---------------------------------------------------------------------------------------------------------------------
# Casos
# ---------------------------------------------------------------------------------------------------------------------
def feed_pool() -> dict[str, dict[int, float]]:
    """Alimentos que podem entrar nos cardápios, por tipo: os da biblioteca NASEM com preço padrão e ``EXTRA_FEEDS``. id -> preço padrão."""
    from .feeds import feed_library

    library = feed_library(STANDARD)
    pool: dict[str, dict[int, float]] = {kind: {} for kind in MENU_SHAPE}
    for feed_id, feed in sorted(library.items()):
        price = feed.default_price if feed.default_price is not None else EXTRA_FEEDS.get(feed_id)
        if price is not None and feed.kind in pool:
            pool[feed.kind][feed_id] = float(price)
    return pool


def menu_of(k: int, seed: int = DESIGN_SEED) -> dict[int, float]:
    """Cardápio ``k`` (id -> preço padrão): a quantidade de alimentos de cada tipo e quais são sorteados com a semente do desenho."""
    rng = random.Random(f"{seed}-menu-{k}")
    pool = feed_pool()
    menu: dict[int, float] = {}
    for kind, (low, high) in MENU_SHAPE.items():
        count = min(rng.randint(low, high), len(pool[kind]))
        for feed_id in rng.sample(sorted(pool[kind]), count):
            menu[feed_id] = pool[kind][feed_id]
    return dict(sorted(menu.items()))


def price_sets(k: int, seed: int = DESIGN_SEED) -> list[dict[int, float]]:
    """Preços do cardápio ``k``: o padrão e ``PRICE_SETS`` sorteados (fator uniforme por alimento)."""
    rng = random.Random(f"{seed}-prices-{k}")
    base = menu_of(k, seed)
    sets = [dict(base)]
    for _ in range(PRICE_SETS):
        sets.append({i: round(p * rng.uniform(*PRICE_FACTOR), 4) for i, p in base.items()})
    return sets


def cases(seed: int = DESIGN_SEED, animals: Sequence[str] | None = None, menus: Sequence[int] | None = None) -> list[dict[str, Any]]:
    """Lista fixa de casos (identificador estável): animal × cardápio × conjunto de preços."""
    out = []
    for animal in animals or ANIMALS:
        for k in menus if menus is not None else range(MENUS):
            for j, prices in enumerate(price_sets(k, seed)):
                out.append({"id": f"{animal}/m{k:02d}/p{j}", "animal": animal, "menu": f"m{k:02d}", "price_set": j, "prices": prices, "seed": seed})
    return out


# ---------------------------------------------------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------------------------------------------------
def _slsqp_on_infeasible(category: str, animal_type: str, cow: Mapping[str, Any], prices: Mapping[int, float], seeds: int) -> int:
    """Quando o LP diz "sem solução", confere se o SLSQP concorda: quantas execuções convergiram (o esperado é zero)."""
    from .module import optimize as opt
    from .module.evaluate import resolve_limits
    from .module.requirements import compute_requirements

    ids = sorted(prices)
    required = compute_requirements(STANDARD, category, cow, None, animal_type)
    problem = opt.build_problem(STANDARD, category, animal_type, cow, ids, dict(prices), resolve_limits(STANDARD, ids, None), required)
    return sum(1 for r in opt.run_rufas(problem, category, seeds) if r["success"])


def run_case(case: Mapping[str, Any], resolution: str = RESOLUTION, seeds: int = SEEDS) -> dict[str, Any]:
    """Roda o LP do módulo, o SLSQP do RuFaS e o LP nas mesmas constantes do SLSQP; guarda só o que a análise usa."""
    from .module import optimize as opt
    from .module.evaluate import resolve_limits
    from .module.requirements import compute_requirements

    category, animal_type, cow = ANIMALS[case["animal"]]
    prices = {int(i): p for i, p in case["prices"].items()}
    ids = sorted(prices)
    started = time.perf_counter()
    result = opt.optimize_diet(STANDARD, category, cow, ids, {str(i): p for i, p in prices.items()}, None, None, animal_type, resolution, seeds)
    record: dict[str, Any] = {k: case[k] for k in ("id", "animal", "menu", "price_set", "prices", "seed")}
    record |= {"resolution": resolution, "status": result["status"]}
    if result["status"] != "ok":
        record["slsqp_converged"] = _slsqp_on_infeasible(category, animal_type, cow, prices, seeds)
        record["wall_seconds"] = time.perf_counter() - started
        return record
    diet = result["diet"]
    record["lp"] = {"cost": diet["cost"], "verified": bool(diet["verified"]), "seconds": result["search"]["seconds"], "regime": diet["regime"]}
    emissions = (diet["emissions"]["methane_g"], diet["emissions"]["urinary_nitrogen_kg"])

    limits = resolve_limits(STANDARD, ids, None)
    problem = opt.build_problem(STANDARD, category, animal_type, cow, ids, prices, limits, compute_requirements(STANDARD, category, cow, None, animal_type))
    # O mesmo problema do SLSQP: emissões fixas nas da dieta do módulo.
    fixed = replace(problem, pen=emissions)
    best, stats = opt.search(fixed, resolution)
    if best is not None:
        amounts = opt._amounts(fixed, best.x)
        check = opt._check(fixed, category, cow, "LP nas mesmas constantes", amounts, prices, limits)
        record["lp_same"] = {"cost": best.cost, "verified": bool(check["feasible"]), "seconds": stats.seconds, "regime": best.point.regime}
    runs = []
    for run in result["rufas"]["runs"]:
        # ``feasible``: conferida com as constantes que o SLSQP recebeu; ``own_ok``: também com as emissões da PRÓPRIA dieta (a definição do módulo).
        own = opt._check(problem, category, cow, "SLSQP", run["amounts"], prices, limits) if run["amounts"] else None
        ok = bool(run["success"] and run["feasible"])
        runs.append({"seed": run["seed"], "ok": ok, "own_ok": bool(ok and opt._within(own, opt.RUFAS_TOLERANCE)), "cost": float(run["cost"]), "seconds": float(run["seconds"])})
    record["slsqp"] = runs
    record["emissions_used"] = {"methane_g": emissions[0], "urinary_nitrogen_kg": emissions[1]}
    record["wall_seconds"] = time.perf_counter() - started
    return record


def load(out: Path) -> list[dict[str, Any]]:
    path = out / "resultados.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.exists() else []
    order = {c["id"]: i for i, c in enumerate(cases(rows[0]["seed"] if rows else DESIGN_SEED))}
    return sorted(rows, key=lambda r: order.get(r["id"], len(order)))


def run(out: Path, limit: int | None = None, resolution: str = RESOLUTION, seeds: int = SEEDS, seed: int = DESIGN_SEED,
        animals: Sequence[str] | None = None, menus: Sequence[int] | None = None) -> None:  # fmt: skip
    """Executa os casos que ainda não estão em ``resultados.jsonl`` (retoma de onde parou) e grava o relatório ao final."""
    out.mkdir(parents=True, exist_ok=True)
    path = out / "resultados.jsonl"
    done = {r["id"] for r in load(out)}
    todo = [c for c in cases(seed, animals, menus) if c["id"] not in done][:limit]
    print(f"{len(done)} casos prontos, {len(todo)} a executar (resolução {resolution}, {seeds} sementes)", flush=True)
    for n, case in enumerate(todo, 1):
        record = run_case(case, resolution, seeds)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        lp = record.get("lp", {}).get("cost")
        print(f"[{n}/{len(todo)}] {case['id']}: {record['status']}, LP {lp if lp is None else round(lp, 4)}, {record['wall_seconds']:.1f} s", flush=True)
    write_report(out)


# ---------------------------------------------------------------------------------------------------------------------
# Estatística
# ---------------------------------------------------------------------------------------------------------------------
def gap_pct(lp: float, reference: float) -> float:
    """Diferença relativa do custo do LP sobre o de referência, em %: negativa = o LP é mais barato."""
    return (lp - reference) / reference * 100


def costs_of(record: Mapping[str, Any], key: str = "ok") -> list[float]:
    """Custos das execuções do SLSQP que convergiram e atendem às restrições (``ok``: com as constantes; ``own_ok``: também com as emissões da dieta)."""
    return [r["cost"] for r in record.get("slsqp", []) if r[key]]


def primary_gap(r: Mapping[str, Any]) -> float | None:
    """LP nas mesmas constantes contra o melhor SLSQP: o mesmo problema."""
    best = costs_of(r)
    return gap_pct(r["lp_same"]["cost"], min(best)) if r["status"] == "ok" and "lp_same" in r and best else None


def consistent_gap(r: Mapping[str, Any]) -> float | None:
    """LP do módulo contra o melhor SLSQP que também atende às restrições com as emissões da própria dieta."""
    best = costs_of(r, "own_ok")
    return gap_pct(r["lp"]["cost"], min(best)) if r["status"] == "ok" and best else None


def consistency_cost(r: Mapping[str, Any]) -> float | None:
    """Custo de usar emissões consistentes: LP do módulo contra LP nas mesmas constantes."""
    return gap_pct(r["lp"]["cost"], r["lp_same"]["cost"]) if r["status"] == "ok" and "lp_same" in r else None


def cluster_bootstrap_ci(groups: Mapping[str, Sequence[float]], level: float = 0.90, reps: int = BOOTSTRAP_REPS, seed: int = BOOTSTRAP_SEED) -> tuple[float, float]:
    """Intervalo percentil da média das diferenças, reamostrando os GRUPOS (animal × cardápio), não os casos."""
    keys = sorted(groups)
    if not keys:
        return (math.nan, math.nan)
    arrays = [np.asarray(groups[k], dtype=float) for k in keys]
    rng = np.random.default_rng(seed)
    means = np.empty(reps)
    for i in range(reps):
        picked = rng.integers(0, len(arrays), len(arrays))
        means[i] = np.concatenate([arrays[j] for j in picked]).mean()
    tail = (1 - level) / 2 * 100
    low, high = np.percentile(means, [tail, 100 - tail])
    return float(low), float(high)


def wilcoxon_p(groups: Mapping[str, Sequence[float]]) -> float | None:
    """Wilcoxon de postos sinalizados (bilateral) sobre a média de cada grupo (os grupos são as unidades independentes); zeros são descartados."""
    means = [float(np.mean(v)) for v in groups.values()]
    d = [m for m in means if abs(m) > 1e-9]
    return float(sp_stats.wilcoxon(d).pvalue) if d else None


def describe_gaps(rows: Sequence[Mapping[str, Any]], gap_fn) -> dict[str, Any]:  # noqa: ANN001
    """Medidas de uma comparação: ``gap_fn(caso)`` dá a diferença em % (ou ``None`` se o caso não entra)."""
    pairs = [(r, g) for r in rows if (g := gap_fn(r)) is not None]
    out: dict[str, Any] = {"cases": len(rows), "compared": len(pairs)}
    if not pairs:
        return out
    gaps = np.asarray([g for _, g in pairs])
    groups: dict[str, list[float]] = {}
    for r, g in pairs:
        groups.setdefault(f"{r['animal']}/{r['menu']}", []).append(g)
    low, high = cluster_bootstrap_ci(groups, 0.90)
    low95, high95 = cluster_bootstrap_ci(groups, 0.95)
    share = float((np.abs(gaps) <= MARGIN_PCT).mean())
    ci_ok = bool(low > -MARGIN_PCT and high < MARGIN_PCT)
    out |= {
        "mean": float(gaps.mean()), "median": float(np.median(gaps)), "sd": float(gaps.std(ddof=1)) if len(gaps) > 1 else 0.0,
        "min": float(gaps.min()), "max": float(gaps.max()), "ci90": [low, high], "ci95": [low95, high95], "groups": len(groups),
        "share_within_margin": share, "ci_within_margin": ci_ok, "equivalent": ci_ok and share >= SHARE_MIN,
        "lp_cheaper": int((gaps < -TIE_PCT).sum()), "tie": int((np.abs(gaps) <= TIE_PCT).sum()), "lp_dearer": int((gaps > TIE_PCT).sum()),
        "wilcoxon_p_groups": wilcoxon_p(groups),
        "outliers": sorted(({"id": r["id"], "gap_pct": float(g), "lp_regime": r["lp"]["regime"]} for r, g in pairs if abs(g) > MARGIN_PCT), key=lambda o: -abs(o["gap_pct"])),
    }  # fmt: skip
    return out


def solver_stats(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Falhas e variação entre sementes do SLSQP, tempos e peso dos preços contra o do método."""
    ok = [r for r in rows if r["status"] == "ok"]
    runs = [x for r in ok for x in r["slsqp"]]
    spread = [(max(c) - min(c)) / min(c) * 100 for r in ok if len(c := costs_of(r)) > 1]
    cv = [statistics.pstdev(c) / statistics.mean(c) * 100 for r in ok if len(c := costs_of(r)) > 1]
    lp_s = [r["lp"]["seconds"] for r in ok]
    same_s = [r["lp_same"]["seconds"] for r in ok if "lp_same" in r]
    sl_s = [x["seconds"] for x in runs]

    def quartiles(values: Sequence[float]) -> dict[str, float] | None:
        return {"median": float(np.median(values)), "q1": float(np.percentile(values, 25)), "q3": float(np.percentile(values, 75))} if values else None

    by_cluster: dict[str, list[float]] = {}
    for r in ok:
        if costs_of(r):
            by_cluster.setdefault(f"{r['animal']}/{r['menu']}", []).append(min(costs_of(r)))
    price_effect = [(max(c) - min(c)) / min(c) * 100 for c in by_cluster.values() if len(c) > 1]
    primary = [abs(g) for r in ok if (g := primary_gap(r)) is not None]
    return {
        "solved": len(ok), "cases": len(rows),
        "lp_verified": sum(1 for r in ok if r["lp"]["verified"]), "lp_same_verified": sum(1 for r in ok if r.get("lp_same", {}).get("verified")),
        "slsqp_runs": len(runs), "slsqp_failed": sum(1 for x in runs if not x["ok"]), "slsqp_not_own_ok": sum(1 for x in runs if x["ok"] and not x["own_ok"]),
        "cases_with_a_failure": sum(1 for r in ok if any(not x["ok"] for x in r["slsqp"])),
        "seed_spread_pct": {"mean": float(np.mean(spread)), "max": float(np.max(spread))} if spread else None,
        "seed_cv_pct": {"mean": float(np.mean(cv)), "max": float(np.max(cv))} if cv else None,
        "seconds": {"lp": quartiles(lp_s), "lp_same": quartiles(same_s), "slsqp": quartiles(sl_s)},
        "price_effect_pct": {"mean": float(np.mean(price_effect)), "max": float(np.max(price_effect))} if price_effect else None,
        "method_effect_pct": {"mean_abs": float(np.mean(primary)), "max_abs": float(np.max(primary))} if primary else None,
    }  # fmt: skip


def summarize(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Tudo o que o relatório mostra."""
    return {
        "version": VERSION, "standard": STANDARD, "margin_pct": MARGIN_PCT, "tie_pct": TIE_PCT, "share_min": SHARE_MIN,
        "primary": describe_gaps(rows, primary_gap),
        "consistent": describe_gaps(rows, consistent_gap),
        "consistency_cost": describe_gaps(rows, consistency_cost),
        "by_animal": {a: describe_gaps([r for r in rows if r["animal"] == a], primary_gap) for a in ANIMALS if any(r["animal"] == a for r in rows)},
        "solver": solver_stats(rows),
        "unsolved": [{"id": r["id"], "status": r["status"], "slsqp_converged": r.get("slsqp_converged")} for r in rows if r["status"] != "ok"],
    }  # fmt: skip


# ---------------------------------------------------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------------------------------------------------
def _f(value: float | None, digits: int = 3) -> str:
    if value is None:
        return "-"
    text = f"{value:.{digits}f}"
    if float(text) == 0:  # evita "-0,000"
        text = text.lstrip("-")
    return text.replace(".", ",")


def _cmp_lines(name: str, d: Mapping[str, Any], summary: Mapping[str, Any]) -> list[str]:
    if not d.get("compared"):
        return [f"{name}: nenhum caso comparável"]
    lines = [
        name,
        f"  n = {d['compared']} casos em {d['groups']} grupos animal × cardápio; média {_f(d['mean'], 3)}% (mediana {_f(d['median'], 3)}%, desvio {_f(d['sd'], 3)}%; de {_f(d['min'], 2)}% a {_f(d['max'], 2)}%)",
        f"  IC de 90% por agrupamento: {_f(d['ci90'][0], 3)}% a {_f(d['ci90'][1], 3)}%; IC de 95%: {_f(d['ci95'][0], 3)}% a {_f(d['ci95'][1], 3)}%; Wilcoxon sobre as médias dos grupos: p = {_f(d['wilcoxon_p_groups'], 3)}",
        f"  dentro da margem: {_f(d['share_within_margin'] * 100, 1)}% (mínimo {_f(summary['share_min'] * 100, 0)}%); LP mais barato / empate / mais caro: {d['lp_cheaper']} / {d['tie']} / {d['lp_dearer']}",
        f"  VEREDITO: {'EQUIVALENTE' if d['equivalent'] else 'equivalência NÃO demonstrada'} (IC dentro da margem: {'sim' if d['ci_within_margin'] else 'não'}; fração dentro da margem: {'sim' if d['share_within_margin'] >= summary['share_min'] else 'não'})",
    ]
    if d["outliers"]:
        lines.append(f"  fora da margem ({len(d['outliers'])}): " + "; ".join(f"{o['id']} {_f(o['gap_pct'], 2)}%" for o in d["outliers"][:12]))
    return lines


def report_text(summary: Mapping[str, Any], meta: Mapping[str, Any]) -> str:
    s = summary["solver"]
    lines = [
        f"BENCHMARK {summary['version']}: LP × SLSQP do RuFaS (padrão {summary['standard']} 2021)",
        f"Margem de equivalência ±{_f(summary['margin_pct'], 1)}%; empate até {_f(summary['tie_pct'], 1)}%; LP na resolução {meta['resolution']}; {meta['seeds']} sementes do SLSQP por caso.",
        "Diferença = (custo do LP − melhor custo do SLSQP) / melhor custo do SLSQP, em %; negativa = o LP é mais barato. Preços ilustrativos.",
        f"Casos: {s['cases']}; com dieta no LP: {s['solved']}. Dietas verificadas com as restrições do RuFaS: LP do módulo {s['lp_verified']} de {s['solved']}; LP nas mesmas constantes {s['lp_same_verified']} de {s['solved']}.",
        "",
        "COMPARAÇÃO PRIMÁRIA (o mesmo problema: LP nas mesmas constantes do SLSQP contra o melhor SLSQP)",
        *_cmp_lines("", summary["primary"], summary)[1:],
        "",
        *_cmp_lines("SECUNDÁRIA 1 (o produto: LP do módulo, com emissões da própria dieta, contra o melhor SLSQP que também as respeita)", summary["consistent"], summary),
        "",
        *_cmp_lines("SECUNDÁRIA 2 (custo de usar emissões consistentes: LP do módulo contra LP nas mesmas constantes)", summary["consistency_cost"], summary),
        "",
        "SLSQP E TEMPO",
        f"  Falhas do SLSQP: {s['slsqp_failed']} de {s['slsqp_runs']} execuções ({_f(s['slsqp_failed'] / s['slsqp_runs'] * 100, 1) if s['slsqp_runs'] else '-'}%), em {s['cases_with_a_failure']} casos; "
        f"{s['slsqp_not_own_ok']} execuções convergiram mas violam a energia com as emissões da própria dieta.",
    ]
    if s["seed_spread_pct"]:
        lines.append(
            f"  Entre sementes (execuções viáveis): a pior custa em média {_f(s['seed_spread_pct']['mean'], 3)}% e no máximo {_f(s['seed_spread_pct']['max'], 2)}% mais que a melhor; "
            f"coeficiente de variação médio {_f(s['seed_cv_pct']['mean'], 3)}% (máx. {_f(s['seed_cv_pct']['max'], 2)}%)."
        )
    for key, label in (("lp", "LP do módulo"), ("lp_same", "LP nas mesmas constantes"), ("slsqp", "SLSQP (por execução)")):
        q = s["seconds"][key]
        if q:
            lines.append(f"  Tempo, {label}: mediana {_f(q['median'], 2)} s (quartis {_f(q['q1'], 2)} a {_f(q['q3'], 2)} s).")
    if s["seconds"]["lp"] and s["seconds"]["slsqp"]:
        lines.append(f"  Razão das medianas (LP do módulo / SLSQP): {_f(s['seconds']['lp']['median'] / s['seconds']['slsqp']['median'], 0)} vezes.")
    if s["price_effect_pct"] and s["method_effect_pct"]:
        lines.append(
            f"  Peso prático: o custo ótimo varia {_f(s['price_effect_pct']['mean'], 0)}% em média (até {_f(s['price_effect_pct']['max'], 0)}%) entre os conjuntos de preços do mesmo animal e cardápio; "
            f"a diferença entre os métodos é de {_f(s['method_effect_pct']['mean_abs'], 3)}% em média (máx. {_f(s['method_effect_pct']['max_abs'], 2)}%)."
        )
    lines += ["", "POR ANIMAL (comparação primária; poucos casos por linha, leia como indicação)"]
    for a, d in summary["by_animal"].items():
        if d.get("compared"):
            lines.append(f"  {a:<18} n={d['compared']:>3}  média {_f(d['mean'], 3):>7}%  IC90 {_f(d['ci90'][0], 3)} a {_f(d['ci90'][1], 3)}  dentro da margem {_f(d['share_within_margin'] * 100, 0)}%  {'equivalente' if d['equivalent'] else 'NÃO demonstrado'}")
        else:
            lines.append(f"  {a:<18} nenhum caso comparável")
    if summary["unsolved"]:
        agree = sum(1 for u in summary["unsolved"] if u.get("slsqp_converged") == 0)
        lines += ["", f"SEM SOLUÇÃO NO LP ({len(summary['unsolved'])} casos); o SLSQP também não convergiu em nenhuma semente em {agree} deles" + ("" if agree == len(summary["unsolved"]) else " (ATENÇÃO: nos demais o SLSQP achou dieta; ver resultados.jsonl)") + "."]
    lines += [
        "",
        "Como ler: os casos são sorteados (animais fixos × cardápios e preços sorteados com semente fixa), não uma amostra de fazendas; a conclusão vale para essa família.",
        "O animal é avaliado em um dia (não é uma simulação completa). O IC reamostra os grupos animal × cardápio, que compartilham exigências.",
        f"Versões: commit {meta['commit']}{' (com alterações não commitadas)' if meta['dirty'] else ''}; RuFaS {meta['rufas']}; Python {meta['python']}, numpy {meta['numpy']}, scipy {meta['scipy']}; {meta['platform']}; {meta['date']}.",
        f"Reprodução: cd backend; ..\\.venv\\Scripts\\python -m dietopt.benchmark run --out ..\\docs\\benchmark\\{summary['version']}",
    ]
    return "\n".join(lines) + "\n"


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, check=True, cwd=Path(__file__).resolve().parent).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def versions() -> dict[str, Any]:
    """Versões e commit do que gerou os dados (para a reprodução)."""
    import scipy

    rufas = "?"
    pyproject = Path(__file__).resolve().parents[2] / "vendor" / "RuFaS" / "pyproject.toml"
    if pyproject.exists():
        for line in pyproject.read_text(encoding="utf-8").splitlines():
            if line.startswith("version"):
                rufas = line.split("=", 1)[1].strip().strip('"')
                break
    return {
        "commit": _git("rev-parse", "--short", "HEAD") or "?", "dirty": bool(_git("status", "--porcelain", "--", ".")), "rufas": rufas,
        "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__, "platform": platform.platform(),
        "date": datetime.date.today().isoformat(),
    }  # fmt: skip


def write_csv(out: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    """Dados brutos em CSV: um arquivo por caso e outro por execução do SLSQP."""
    cases_header = ["id", "animal", "menu", "price_set", "status", "lp_cost", "lp_verified", "lp_regime", "lp_seconds", "lp_same_cost", "lp_same_verified", "lp_same_seconds",
                    "slsqp_best_cost", "slsqp_best_own_cost", "primary_gap_pct", "consistent_gap_pct", "consistency_cost_pct", "methane_g", "urinary_nitrogen_kg"]  # fmt: skip
    with (out / "resultados.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(cases_header)
        for r in rows:
            ok = r["status"] == "ok"
            em = r.get("emissions_used", {})
            writer.writerow([
                r["id"], r["animal"], r["menu"], r["price_set"], r["status"],
                r["lp"]["cost"] if ok else "", r["lp"]["verified"] if ok else "", r["lp"]["regime"] if ok else "", r["lp"]["seconds"] if ok else "",
                r.get("lp_same", {}).get("cost", ""), r.get("lp_same", {}).get("verified", ""), r.get("lp_same", {}).get("seconds", ""),
                min(costs_of(r), default=""), min(costs_of(r, "own_ok"), default=""),
                "" if primary_gap(r) is None else primary_gap(r), "" if consistent_gap(r) is None else consistent_gap(r),
                "" if consistency_cost(r) is None else consistency_cost(r), em.get("methane_g", ""), em.get("urinary_nitrogen_kg", ""),
            ])  # fmt: skip
    with (out / "execucoes_slsqp.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "seed", "ok", "own_ok", "cost", "seconds"])
        for r in rows:
            for x in r.get("slsqp", []):
                writer.writerow([r["id"], x["seed"], x["ok"], x["own_ok"], x["cost"], x["seconds"]])


def write_report(out: Path) -> None:
    rows = load(out)
    meta = {"resolution": next((r["resolution"] for r in rows), RESOLUTION), "seeds": max((len(r["slsqp"]) for r in rows if "slsqp" in r), default=SEEDS), **versions()}
    summary = summarize(rows) | {"meta": meta}
    (out / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    write_csv(out, rows)
    text = report_text(summary, meta)
    (out / "RELATORIO.txt").write_text(text, encoding="utf-8")
    print(text)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=("run", "report", "cases"))
    parser.add_argument("--out", type=Path, default=Path("..") / "docs" / "benchmark" / VERSION)
    parser.add_argument("--limit", type=int, default=None, help="máximo de casos a executar nesta chamada")
    parser.add_argument("--resolution", default=RESOLUTION, choices=("rapida", "normal", "fina"))
    parser.add_argument("--seeds", type=int, default=SEEDS)
    parser.add_argument("--seed", type=int, default=DESIGN_SEED, help="outra semente = outros cardápios e preços (casos novos)")
    parser.add_argument("--animals", nargs="+", choices=list(ANIMALS), default=None)
    parser.add_argument("--menus", nargs="+", type=int, default=None, help="números dos cardápios (0 a %d)" % (MENUS - 1))
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # o console do Windows (cp1252) não tem o sinal de menos
    if args.command == "cases":
        print(json.dumps(cases(args.seed, args.animals, args.menus), ensure_ascii=False, indent=1))
    elif args.command == "run":
        run(args.out, args.limit, args.resolution, args.seeds, args.seed, args.animals, args.menus)
    else:
        write_report(args.out)


if __name__ == "__main__":
    sys.exit(main())
