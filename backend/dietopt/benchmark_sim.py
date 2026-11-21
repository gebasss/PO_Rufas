"""Benchmark de simulações completas: a ração do LP custa o mesmo que a do SLSQP dentro de uma simulação de um ano do RuFaS?

Complementa o benchmark do módulo (``benchmark.py``: um animal em um dia, melhor de 10 sementes do SLSQP). Aqui a unidade é a **simulação**
(um ano, 13 intervalos de formulação de ração, o rebanho inteiro, NASEM 2021), com o SLSQP *dentro* da simulação, como o usuário o usa: uma
execução por intervalo, sem escolher a melhor semente.

**O que é medido (e o que não é).** O RuFaS roda a simulação com o SLSQP formulando a ração do lote de vacas em lactação a cada intervalo.
Para cada intervalo, o LP é resolvido sobre **exatamente as mesmas exigências, alimentos, preços, limites e emissões do lote** (as que o RuFaS
passou ao SLSQP), e as duas rações são comparadas. A ração do LP **não volta** para a simulação (o RuFaS não aceita isso sem ser alterado,
``CONCLUSOES_PREVIAS.txt`` 3.2): a simulação segue com a ração do SLSQP, e o LP é uma segunda ração para as mesmas condições de cada intervalo.
Por isso a camada mede a diferença de **custo da ração**, não o efeito da ração do LP sobre o leite, o rebanho ou as exigências seguintes.

**Simulações (sorteadas com semente fixa).** ``MENUS`` cardápios sorteados (2 a 3 volumosos, 3 a 6 concentrados e 1 a 2 minerais, como em
``benchmark.py``) × 2 conjuntos de preços (o padrão e um sorteado, fator uniforme de 0,5 a 1,5 por alimento). Cada cardápio sorteia também o
tamanho do rebanho (``HERD_SIZES`` vacas) e a semente do RuFaS; os dois conjuntos de preços do cardápio compartilham os dois, de modo que a
diferença entre eles é só de preço. Limites de inclusão: o teto padrão de cada alimento (como na tela Vaca leiteira).

**Critério (definido antes de rodar).** Diferença da simulação = (custo médio por vaca por dia do LP − o do SLSQP) / o do SLSQP, em %, média dos
intervalos ponderada pelos dias (o mesmo número que a tela mostra); negativa = o LP é mais barato.
- *Primária*: LP de **consumo livre** (o consumo pode variar na faixa do RuFaS, estimativa ±30%, como no SLSQP) contra o SLSQP: o mesmo problema.
- *Secundária*: LP de **mesmo consumo** (o consumo que o SLSQP escolheu), a comparação mais conservadora: tira do LP a liberdade de comer menos.
- *Equivalente* se o IC de 90% da diferença média (bootstrap por cardápio: as duas simulações do cardápio não são independentes) cabe em ±``MARGIN_PCT``
  e ao menos ``SHARE_MIN`` das simulações ficam dentro da margem (o mesmo critério do v4). Se não for equivalente, o relatório diz para que lado:
  *LP mais barato além da margem* (IC inteiro abaixo de −margem), *LP mais caro além da margem* (IC inteiro acima de +margem) ou *inconclusivo*.
- Em cada intervalo o SLSQP roda UMA vez (como no uso real); ele pode parar em ótimo local, o que favorece o LP. É por isso que esta camada pode dar um
  resultado diferente do benchmark do módulo (melhor de 10 sementes).

Uso (na pasta backend)::

    ..\\.venv\\Scripts\\python -m dietopt.benchmark_sim run --out ..\\docs\\benchmark\\simulacao     # retoma o que já foi feito
    ..\\.venv\\Scripts\\python -m dietopt.benchmark_sim report --out ..\\docs\\benchmark\\simulacao  # só refaz o resumo, os CSVs e o relatório
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import shutil
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import numpy as np

from . import benchmark as bm

VERSION = "sim-v2"
STANDARD = "NASEM"
RESOLUTION = "normal"
MARGIN_PCT = bm.MARGIN_PCT
TIE_PCT = bm.TIE_PCT
SHARE_MIN = bm.SHARE_MIN
DESIGN_SEED = 20261203  # a primeira rodada (sim-v1, semente 20261202) tinha o defeito do dia 0 (ver docs/benchmark/README.md) e foi guardada em historico
MENUS = 20  # cardápios; com 2 conjuntos de preços cada, 40 simulações
HERD_SIZES = (60, 100, 200, 300)  # vacas; dentro da faixa verificada do RuFaS (60 a 500)
WORKERS = 3  # simulações ao mesmo tempo (cada uma usa cerca de 1,2 GB de memória)
MILK_REDUCTION_MAX = 5.0  # o padrão da tela Vaca leiteira


# ---------------------------------------------------------------------------------------------------------------------
# Simulações
# ---------------------------------------------------------------------------------------------------------------------
def sims(seed: int = DESIGN_SEED, menus: Sequence[int] | None = None) -> list[dict[str, Any]]:
    """Lista fixa de simulações (identificador estável): cardápio × conjunto de preços."""
    out = []
    for k in menus if menus is not None else range(MENUS):
        rng = random.Random(f"{seed}-herd-{k}")
        cows = rng.choice(HERD_SIZES)
        rufas_seed = rng.randint(1, 999_999)
        for j, prices in enumerate(bm.price_sets(k, seed)[:2]):
            out.append({"id": f"m{k:02d}/p{j}", "menu": f"m{k:02d}", "price_set": j, "prices": prices, "cows": cows, "rufas_seed": rufas_seed, "seed": seed})
    return out


def _scenario(spec: Mapping[str, Any]) -> tuple[Any, Any]:
    from .feeds import feed_library
    from .rufas_adapter import Scenario
    from .scenarios import DEFAULT_PRICES, Economics

    library = feed_library(STANDARD)
    ids = sorted(int(i) for i in spec["prices"])
    limits = {i: (0.0, float(library[i].default_max) if i in library else 100.0) for i in ids}
    prices = {int(i): float(p) for i, p in spec["prices"].items()}
    name = "bsim_" + spec["id"].replace("/", "_")
    scenario = Scenario(
        name=name, end_date="2013:365", random_seed=int(spec["rufas_seed"]), nutrient_standard=STANDARD,
        cow_num=None if int(spec["cows"]) == 100 else int(spec["cows"]), lac_cow_feeds=ids, feed_limits=limits, feed_prices=prices,
        milk_reduction_maximum=MILK_REDUCTION_MAX,
    )  # fmt: skip
    return scenario, Economics(prices={**DEFAULT_PRICES, **prices})


def run_sim(spec: Mapping[str, Any], resolution: str = RESOLUTION) -> dict[str, Any]:
    """Simula um cenário no RuFaS (ou recupera do cache) e compara, intervalo a intervalo, a ração do SLSQP com a do LP."""
    from .module.pen_lp import compare_with_simulation
    from .rufas_adapter import RUNS_DIR
    from .scenarios import evaluate

    base = {k: spec[k] for k in ("id", "menu", "price_set", "cows", "rufas_seed", "seed")} | {"feeds": sorted(int(i) for i in spec["prices"]), "resolution": resolution}
    scenario, economics = _scenario(spec)
    started = time.time()
    evaluation = evaluate(scenario, economics)
    sim_seconds = time.time() - started
    if not evaluation.ok or evaluation.result is None:
        return base | {"status": "sim_failed", "detail": evaluation.detail, "sim_seconds": sim_seconds}
    result = evaluation.result
    started = time.time()
    comparison = compare_with_simulation(result, scenario.lac_cow_feeds or [], scenario.feed_prices, scenario.feed_limits, STANDARD, resolution=resolution)
    compare_seconds = time.time() - started
    reductions = [float(r.get("avg_milk_production_reduction_pen") or 0.0) for r in result.requirements]
    intervals = []
    for row, reduction in zip(comparison["intervals"], reductions):
        item: dict[str, Any] = {"day": row["day"], "days": row["days"], "cows": row["cows"], "reduction": reduction, "slsqp": {"cost": row["slsqp"]["cost"], "dmi": row["slsqp"]["dmi"]}}
        for variant in ("lp_free", "lp_same"):
            v = row[variant]
            item[variant] = None if v is None else {key: v[key] for key in ("cost", "dmi", "verified", "seconds")}
        intervals.append(item)
    folder = Path(RUNS_DIR) / scenario.name
    if folder.exists():
        shutil.rmtree(folder, ignore_errors=True)  # o resultado já está no cache; a pasta só ocupa disco
    summary = comparison["summary"]
    return base | {
        "status": "ok" if summary.get("intervals_used") else "no_lp",
        "sim_seconds": sim_seconds, "compare_seconds": compare_seconds, "milk_kg": evaluation.milk_kg, "reduction_mean": evaluation.reduction,
        "intervals": intervals, "summary": {k: summary.get(k) for k in ("intervals_used", "days", "slsqp_cost_per_cow_day", "mean_cows")}
        | {v: {k: summary[v][k] for k in ("cost_per_cow_day", "saving_pct", "herd_saving", "all_verified")} for v in ("lp_free", "lp_same") if v in summary},
        "warnings": comparison["warnings"],
    }  # fmt: skip


def load(out: Path) -> list[dict[str, Any]]:
    path = out / "resultados.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.exists() else []
    order = {s["id"]: i for i, s in enumerate(sims(rows[0]["seed"] if rows else DESIGN_SEED))}
    return sorted(rows, key=lambda r: order.get(r["id"], len(order)))


def run(out: Path, limit: int | None = None, resolution: str = RESOLUTION, seed: int = DESIGN_SEED, menus: Sequence[int] | None = None, workers: int = WORKERS) -> None:
    """Executa as simulações que ainda não estão em ``resultados.jsonl`` (retoma de onde parou) e grava o relatório ao final."""
    out.mkdir(parents=True, exist_ok=True)
    path = out / "resultados.jsonl"
    done = {r["id"] for r in load(out)}
    todo = [s for s in sims(seed, menus) if s["id"] not in done][:limit]
    print(f"{len(done)} simulações prontas, {len(todo)} a executar (resolução {resolution}, {workers} ao mesmo tempo)", flush=True)
    started = time.time()
    with ProcessPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {pool.submit(run_sim, spec, resolution): spec for spec in todo}
        for n, future in enumerate(as_completed(futures), 1):
            spec = futures[future]
            try:
                record = future.result()
            except Exception as error:  # noqa: BLE001 - uma simulação com erro não derruba as demais; fica registrada
                record = {k: spec[k] for k in ("id", "menu", "price_set", "cows", "rufas_seed", "seed")} | {"status": "error", "detail": f"{type(error).__name__}: {error}"}
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            gap = free_gap(record)
            print(f"[{n}/{len(todo)}] {spec['id']} ({spec['cows']} vacas): {record['status']}"
                  f"{'' if gap is None else f', LP livre {bm._f(gap, 3)}%'}, {(time.time() - started) / 60:.1f} min", flush=True)  # fmt: skip
    write_report(out)


# ---------------------------------------------------------------------------------------------------------------------
# Estatística
# ---------------------------------------------------------------------------------------------------------------------
def _gap(r: Mapping[str, Any], variant: str) -> float | None:
    s = r.get("summary") or {}
    if r.get("status") != "ok" or variant not in s or not s.get("slsqp_cost_per_cow_day"):
        return None
    return bm.gap_pct(s[variant]["cost_per_cow_day"], s["slsqp_cost_per_cow_day"])


def free_gap(r: Mapping[str, Any]) -> float | None:
    """Primária: LP de consumo livre contra o SLSQP (o mesmo problema)."""
    return _gap(r, "lp_free")


def same_gap(r: Mapping[str, Any]) -> float | None:
    """Secundária: LP de mesmo consumo contra o SLSQP (a comparação conservadora)."""
    return _gap(r, "lp_same")


def verdict(d: Mapping[str, Any]) -> str:
    """Equivalente, ou para que lado o IC de 90% está além da margem, ou inconclusivo."""
    if d.get("equivalent"):
        return "equivalent"
    low, high = d["ci90"]
    if high < -MARGIN_PCT:
        return "lp_cheaper"
    if low > MARGIN_PCT:
        return "lp_dearer"
    return "inconclusive"


def describe(rows: Sequence[Mapping[str, Any]], gap_fn: Callable[[Mapping[str, Any]], float | None]) -> dict[str, Any]:
    """Medidas de uma comparação entre simulações: ``gap_fn(simulação)`` dá a diferença em % (ou ``None``)."""
    pairs = [(r, g) for r in rows if (g := gap_fn(r)) is not None]
    out: dict[str, Any] = {"simulations": len(rows), "compared": len(pairs)}
    if not pairs:
        return out
    gaps = np.asarray([g for _, g in pairs])
    groups: dict[str, list[float]] = {}
    for r, g in pairs:
        groups.setdefault(r["menu"], []).append(g)
    low, high = bm.cluster_bootstrap_ci(groups, 0.90)
    low95, high95 = bm.cluster_bootstrap_ci(groups, 0.95)
    share = float((np.abs(gaps) <= MARGIN_PCT).mean())
    ci_ok = bool(low > -MARGIN_PCT and high < MARGIN_PCT)
    out |= {
        "mean": float(gaps.mean()), "median": float(np.median(gaps)), "sd": float(gaps.std(ddof=1)) if len(gaps) > 1 else 0.0,
        "min": float(gaps.min()), "max": float(gaps.max()), "ci90": [low, high], "ci95": [low95, high95], "groups": len(groups),
        "share_within_margin": share, "ci_within_margin": ci_ok, "equivalent": ci_ok and share >= SHARE_MIN,
        "lp_cheaper": int((gaps < -TIE_PCT).sum()), "tie": int((np.abs(gaps) <= TIE_PCT).sum()), "lp_dearer": int((gaps > TIE_PCT).sum()),
        "wilcoxon_p_groups": bm.wilcoxon_p(groups),
        "outliers": sorted(({"id": r["id"], "gap_pct": float(g)} for r, g in pairs if abs(g) > MARGIN_PCT), key=lambda o: -abs(o["gap_pct"])),
    }  # fmt: skip
    out["verdict"] = verdict(out)
    return out


def interval_gaps(rows: Sequence[Mapping[str, Any]], variant: str) -> list[float]:
    """Diferença (em %) de cada intervalo em que o LP achou ração, de todas as simulações."""
    return [bm.gap_pct(i[variant]["cost"], i["slsqp"]["cost"]) for r in rows if r.get("status") == "ok" for i in r["intervals"] if i.get(variant) and i["slsqp"]["cost"] > 0]


def describe_intervals(rows: Sequence[Mapping[str, Any]], variant: str) -> dict[str, Any]:
    """Os intervalos (medidas repetidas dentro da simulação): só descrição, sem inferência (não são independentes)."""
    gaps = np.asarray(interval_gaps(rows, variant))
    total = sum(len(r["intervals"]) for r in rows if r.get("status") == "ok")
    if not len(gaps):
        return {"intervals": total, "compared": 0}
    return {
        "intervals": total, "compared": int(len(gaps)), "mean": float(gaps.mean()), "median": float(np.median(gaps)), "min": float(gaps.min()), "max": float(gaps.max()),
        "share_within_margin": float((np.abs(gaps) <= MARGIN_PCT).mean()), "lp_cheaper": int((gaps < -TIE_PCT).sum()), "tie": int((np.abs(gaps) <= TIE_PCT).sum()),
        "lp_dearer": int((gaps > TIE_PCT).sum()), "lp_dearer_beyond_margin": int((gaps > MARGIN_PCT).sum()), "lp_cheaper_beyond_margin": int((gaps < -MARGIN_PCT).sum()),
    }  # fmt: skip


def run_stats(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Falhas, verificação das rações do LP, tempos, redução de leite e peso dos preços contra o do método."""
    ok = [r for r in rows if r.get("status") == "ok"]
    ivs = [i for r in ok for i in r["intervals"]]

    def quartiles(values: Sequence[float]) -> dict[str, float] | None:
        return {"median": float(np.median(values)), "q1": float(np.percentile(values, 25)), "q3": float(np.percentile(values, 75))} if values else None

    by_menu: dict[str, list[float]] = {}
    for r in ok:
        by_menu.setdefault(r["menu"], []).append(r["summary"]["slsqp_cost_per_cow_day"])
    price_effect = [(max(c) - min(c)) / min(c) * 100 for c in by_menu.values() if len(c) > 1]
    primary = [abs(g) for r in ok if (g := free_gap(r)) is not None]
    saving = [r["summary"]["lp_free"]["saving_pct"] * r["summary"]["slsqp_cost_per_cow_day"] / 100 * 365 for r in ok if "lp_free" in r["summary"]]
    return {
        "simulations": len(rows), "ok": len(ok), "sim_failed": sum(r.get("status") == "sim_failed" for r in rows),
        "no_lp": sum(r.get("status") == "no_lp" for r in rows), "errors": sum(r.get("status") == "error" for r in rows),
        "intervals": len(ivs), "intervals_without_lp_free": sum(1 for i in ivs if not i.get("lp_free")), "intervals_without_lp_same": sum(1 for i in ivs if not i.get("lp_same")),
        "lp_free_verified": sum(1 for i in ivs if i.get("lp_free") and i["lp_free"]["verified"]), "lp_same_verified": sum(1 for i in ivs if i.get("lp_same") and i["lp_same"]["verified"]),
        "sims_with_milk_reduction": sum(1 for r in ok if r["reduction_mean"] > 1e-9), "intervals_with_milk_reduction": sum(1 for i in ivs if i["reduction"] > 1e-9),
        "seconds": {"simulation": quartiles([r["sim_seconds"] for r in ok]), "lp_per_interval": quartiles([i["lp_free"]["seconds"] for i in ivs if i.get("lp_free")]),
                    "compare_per_simulation": quartiles([r["compare_seconds"] for r in ok])},
        "price_effect_pct": {"mean": float(np.mean(price_effect)), "max": float(np.max(price_effect))} if price_effect else None,
        "method_effect_pct": {"mean_abs": float(np.mean(primary)), "max_abs": float(np.max(primary))} if primary else None,
        "saving_per_cow_year": {"mean": float(np.mean(saving)), "min": float(np.min(saving)), "max": float(np.max(saving))} if saving else None,
        "herd_saving_per_year": float(np.mean([r["summary"]["lp_free"]["herd_saving"] / max(r["summary"]["days"], 1) * 365 for r in ok if "lp_free" in r["summary"]])) if ok else None,
    }  # fmt: skip


def summarize(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    clean = [r for r in rows if r.get("status") == "ok" and r["reduction_mean"] <= 1e-9]
    by_cows = {str(c): describe([r for r in rows if r.get("cows") == c], free_gap) for c in sorted({r["cows"] for r in rows if r.get("cows")})}
    return {
        "version": VERSION, "standard": STANDARD, "margin_pct": MARGIN_PCT, "tie_pct": TIE_PCT, "share_min": SHARE_MIN,
        "primary": describe(rows, free_gap), "same_dmi": describe(rows, same_gap),
        "intervals_free": describe_intervals(rows, "lp_free"), "intervals_same": describe_intervals(rows, "lp_same"),
        "without_milk_reduction": describe(clean, free_gap), "by_herd_size": by_cows, "run": run_stats(rows),
        "failed": [{"id": r["id"], "status": r["status"], "detail": str(r.get("detail", ""))[:200]} for r in rows if r.get("status") != "ok"],
    }  # fmt: skip


# ---------------------------------------------------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------------------------------------------------
_f = bm._f
_VERDICT = {
    "equivalent": "EQUIVALENTE", "lp_cheaper": "LP MAIS BARATO além da margem", "lp_dearer": "LP MAIS CARO além da margem", "inconclusive": "INCONCLUSIVO (nem equivalente nem além da margem)",
}


def verdict_text(d: Mapping[str, Any]) -> str:
    """O veredito em palavras. O caso do IC dentro da margem sem a fração mínima de simulações dentro dela é dito por extenso."""
    if d["verdict"] == "inconclusive" and d["ci_within_margin"]:
        return f"equivalência NÃO demonstrada (a média cabe na margem, mas só {_f(d['share_within_margin'] * 100, 1)}% das simulações ficam dentro dela)"
    return _VERDICT[d["verdict"]]


def _cmp_lines(name: str, d: Mapping[str, Any], summary: Mapping[str, Any]) -> list[str]:
    if not d.get("compared"):
        return [f"{name}: nenhuma simulação comparável"]
    lines = [
        name,
        f"  n = {d['compared']} simulações em {d['groups']} cardápios; média {_f(d['mean'], 3)}% (mediana {_f(d['median'], 3)}%, desvio {_f(d['sd'], 3)}%; de {_f(d['min'], 2)}% a {_f(d['max'], 2)}%)",
        f"  IC de 90% por cardápio: {_f(d['ci90'][0], 3)}% a {_f(d['ci90'][1], 3)}%; IC de 95%: {_f(d['ci95'][0], 3)}% a {_f(d['ci95'][1], 3)}%; Wilcoxon sobre as médias dos cardápios: p = {_f(d['wilcoxon_p_groups'], 3)}",
        f"  dentro da margem: {_f(d['share_within_margin'] * 100, 1)}% (mínimo {_f(summary['share_min'] * 100, 0)}%); LP mais barato / empate / mais caro: {d['lp_cheaper']} / {d['tie']} / {d['lp_dearer']}",
        f"  VEREDITO: {verdict_text(d)} (IC dentro da margem: {'sim' if d['ci_within_margin'] else 'não'}; fração dentro da margem: {'sim' if d['share_within_margin'] >= summary['share_min'] else 'não'})",
        f"  [análise posterior ao desenho, só descrição] limite superior do IC de 90%: {_f(d['ci90'][1], 3)}% (o LP custa, em média, no máximo isso a mais); simulações com o LP mais caro além da margem: "
        f"{sum(1 for o in d['outliers'] if o['gap_pct'] > 0)}; mais barato além da margem: {sum(1 for o in d['outliers'] if o['gap_pct'] < 0)}",
    ]
    if d["outliers"]:
        lines.append(f"  fora da margem ({len(d['outliers'])}): " + "; ".join(f"{o['id']} {_f(o['gap_pct'], 2)}%" for o in d["outliers"][:12]))
    return lines


def _interval_line(name: str, d: Mapping[str, Any]) -> str:
    if not d.get("compared"):
        return f"  {name}: nenhum intervalo comparável"
    return (
        f"  {name}: {d['compared']} de {d['intervals']} intervalos; média {_f(d['mean'], 3)}% (mediana {_f(d['median'], 3)}%; de {_f(d['min'], 2)}% a {_f(d['max'], 2)}%); "
        f"LP mais barato / empate / mais caro: {d['lp_cheaper']} / {d['tie']} / {d['lp_dearer']}; além da margem: {d['lp_cheaper_beyond_margin']} mais barato e {d['lp_dearer_beyond_margin']} mais caro"
    )


def report_text(summary: Mapping[str, Any], meta: Mapping[str, Any]) -> str:
    s = summary["run"]
    lines = [
        f"BENCHMARK DE SIMULAÇÕES COMPLETAS {summary['version']}: LP × SLSQP do RuFaS dentro de uma simulação de 1 ano (padrão {summary['standard']} 2021)",
        f"Margem de equivalência ±{_f(summary['margin_pct'], 1)}%; empate até {_f(summary['tie_pct'], 1)}%; LP na resolução {meta['resolution']}; o SLSQP roda UMA vez por intervalo (como no uso real).",
        "Diferença da simulação = (custo médio por vaca por dia do LP − o do SLSQP) / o do SLSQP, em %, ponderada pelos dias dos 13 intervalos; negativa = o LP é mais barato. Preços ilustrativos.",
        f"Simulações: {s['simulations']}; concluídas com comparação: {s['ok']}; falhas do RuFaS: {s['sim_failed']}; sem ração no LP: {s['no_lp']}; erros: {s['errors']}. Intervalos: {s['intervals']}.",
        f"Rações do LP que atendem às restrições originais do RuFaS: consumo livre {s['lp_free_verified']} de {s['intervals'] - s['intervals_without_lp_free']}; mesmo consumo {s['lp_same_verified']} de {s['intervals'] - s['intervals_without_lp_same']}"
        f" (intervalos sem ração no LP: {s['intervals_without_lp_free']} e {s['intervals_without_lp_same']}).",
        "",
        *_cmp_lines("COMPARAÇÃO PRIMÁRIA (o mesmo problema: LP de consumo livre contra o SLSQP)", summary["primary"], summary),
        "",
        *_cmp_lines("SECUNDÁRIA (LP de mesmo consumo, o que o SLSQP escolheu, contra o SLSQP; mais conservadora)", summary["same_dmi"], summary),
        "",
        "INTERVALOS (medidas repetidas dentro da simulação: só descrição, sem inferência)",
        _interval_line("consumo livre", summary["intervals_free"]),
        _interval_line("mesmo consumo", summary["intervals_same"]),
        "",
        "SENSIBILIDADE",
        f"  Simulações em que o RuFaS reduziu o leite por falta de ração: {s['sims_with_milk_reduction']} de {s['ok']} ({s['intervals_with_milk_reduction']} intervalos).",
    ]
    clean = summary["without_milk_reduction"]
    if clean.get("compared"):
        lines += [f"  Só as simulações sem redução de leite (n = {clean['compared']}): média {_f(clean['mean'], 3)}%, IC de 90% {_f(clean['ci90'][0], 3)}% a {_f(clean['ci90'][1], 3)}%, {verdict_text(clean)}."]
    for cows, d in summary["by_herd_size"].items():
        if d.get("compared"):
            lines.append(f"  Rebanho de {cows} vacas: n = {d['compared']}, média {_f(d['mean'], 3)}%, IC de 90% {_f(d['ci90'][0], 3)}% a {_f(d['ci90'][1], 3)}% (poucas simulações; indicação).")
    lines += ["", "TEMPO E PESO PRÁTICO"]
    sec = s["seconds"]
    if sec["simulation"]:
        lines.append(f"  Simulação do RuFaS (1 ano, com o SLSQP dentro): mediana {_f(sec['simulation']['median'], 0)} s (quartis {_f(sec['simulation']['q1'], 0)} a {_f(sec['simulation']['q3'], 0)} s; as simulações já em cache contam 0 s).")
    if sec["lp_per_interval"]:
        lines.append(f"  LP, uma ração (consumo livre): mediana {_f(sec['lp_per_interval']['median'], 1)} s (quartis {_f(sec['lp_per_interval']['q1'], 1)} a {_f(sec['lp_per_interval']['q3'], 1)} s). O tempo do SLSQP por intervalo não é medido aqui (ver o benchmark do módulo).")
    if s["price_effect_pct"] and s["method_effect_pct"]:
        lines.append(
            f"  O custo da ração do SLSQP varia {_f(s['price_effect_pct']['mean'], 0)}% em média (até {_f(s['price_effect_pct']['max'], 0)}%) entre os dois conjuntos de preços do mesmo cardápio; "
            f"a diferença entre os métodos é de {_f(s['method_effect_pct']['mean_abs'], 3)}% em média (máx. {_f(s['method_effect_pct']['max_abs'], 2)}%)."
        )
    if s["saving_per_cow_year"]:
        q = s["saving_per_cow_year"]
        lines.append(f"  Economia do LP de consumo livre por vaca em lactação por ano: média US$ {_f(q['mean'], 2)} (de {_f(q['min'], 2)} a {_f(q['max'], 2)}); no rebanho, média US$ {_f(s['herd_saving_per_year'], 0)} por ano.")
    if summary["failed"]:
        lines += ["", f"SIMULAÇÕES SEM COMPARAÇÃO ({len(summary['failed'])}):"] + [f"  {f['id']}: {f['status']} {f['detail']}" for f in summary["failed"]]
    lines += [
        "",
        "Como ler: cada simulação é um rebanho de um cardápio e um conjunto de preços sorteados (semente fixa), não uma amostra de fazendas; a conclusão vale para essa família.",
        "A ração do LP NÃO volta para a simulação (o RuFaS não aceita isso sem ser alterado): a simulação segue com a ração do SLSQP e o LP é resolvido sobre as mesmas condições de cada intervalo.",
        "Por isso a camada mede a diferença de custo da ração, não o efeito da ração do LP sobre o leite ou as exigências seguintes.",
        f"Versões: commit {meta['commit']}{' (com alterações não commitadas)' if meta['dirty'] else ''}; RuFaS {meta['rufas']}; Python {meta['python']}, numpy {meta['numpy']}, scipy {meta['scipy']}; {meta['platform']}; {meta['date']}.",
        "Reprodução: cd backend; ..\\.venv\\Scripts\\python -m dietopt.benchmark_sim run --out ..\\docs\\benchmark\\simulacao",
    ]
    return "\n".join(lines) + "\n"


def write_csv(out: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    """Dados brutos em CSV: um arquivo por simulação e outro por intervalo."""
    with (out / "resultados.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "menu", "price_set", "cows", "rufas_seed", "status", "feeds", "sim_seconds", "milk_kg", "milk_reduction_mean", "slsqp_cost", "lp_free_cost", "lp_same_cost",
                         "free_gap_pct", "same_gap_pct", "herd_saving_free_usd"])  # fmt: skip
        for r in rows:
            s = r.get("summary") or {}
            writer.writerow([
                r["id"], r["menu"], r["price_set"], r["cows"], r["rufas_seed"], r["status"], " ".join(map(str, r.get("feeds", []))), r.get("sim_seconds", ""), r.get("milk_kg", ""),
                r.get("reduction_mean", ""), s.get("slsqp_cost_per_cow_day", ""), s.get("lp_free", {}).get("cost_per_cow_day", ""), s.get("lp_same", {}).get("cost_per_cow_day", ""),
                "" if free_gap(r) is None else free_gap(r), "" if same_gap(r) is None else same_gap(r), s.get("lp_free", {}).get("herd_saving", ""),
            ])  # fmt: skip
    with (out / "intervalos.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "day", "days", "cows", "milk_reduction", "slsqp_cost", "slsqp_dmi", "lp_free_cost", "lp_free_dmi", "lp_free_verified", "lp_free_seconds", "lp_same_cost", "lp_same_verified"])
        for r in rows:
            for i in r.get("intervals", []):
                f, a = i.get("lp_free") or {}, i.get("lp_same") or {}
                writer.writerow([r["id"], i["day"], i["days"], i["cows"], i["reduction"], i["slsqp"]["cost"], i["slsqp"]["dmi"], f.get("cost", ""), f.get("dmi", ""), f.get("verified", ""),
                                 f.get("seconds", ""), a.get("cost", ""), a.get("verified", "")])  # fmt: skip


def write_report(out: Path) -> None:
    rows = load(out)
    meta = {"resolution": next((r["resolution"] for r in rows if "resolution" in r), RESOLUTION), **bm.versions()}
    summary = summarize(rows) | {"meta": meta}
    (out / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    write_csv(out, rows)
    text = report_text(summary, meta)
    (out / "RELATORIO.txt").write_text(text, encoding="utf-8")
    print(text)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=("run", "report", "sims"))
    parser.add_argument("--out", type=Path, default=Path("..") / "docs" / "benchmark" / "simulacao")
    parser.add_argument("--limit", type=int, default=None, help="máximo de simulações a executar nesta chamada")
    parser.add_argument("--resolution", default=RESOLUTION, choices=("rapida", "normal", "fina"))
    parser.add_argument("--seed", type=int, default=DESIGN_SEED, help="outra semente = outros cardápios, rebanhos e preços (simulações novas)")
    parser.add_argument("--menus", nargs="+", type=int, default=None, help="números dos cardápios (0 a %d)" % (MENUS - 1))
    parser.add_argument("--workers", type=int, default=WORKERS)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.command == "sims":
        print(json.dumps(sims(args.seed, args.menus), ensure_ascii=False, indent=1))
    elif args.command == "run":
        run(args.out, args.limit, args.resolution, args.seed, args.menus, args.workers)
    else:
        write_report(args.out)


if __name__ == "__main__":
    sys.exit(main())
