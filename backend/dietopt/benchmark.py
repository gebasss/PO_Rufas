"""Benchmark v3: o custo da dieta ótima por programação linear (LP) é equivalente ao do SLSQP do RuFaS?

**Pergunta.** Para o mesmo problema (um animal, um cardápio e um conjunto de preços, padrão NASEM 2021), o custo mínimo que o LP acha é
equivalente (dentro de ±``MARGIN_PCT``) ao melhor custo que o SLSQP do RuFaS acha em ``SEEDS`` pontos iniciais aleatórios?

**Caso** = animal × cardápio × conjunto de preços. Cada caso roda ``optimize_diet`` (a mesma rota da tela Dieta ótima): o LP e as
execuções do ``RationOptimizer`` do RuFaS para o animal em UM dia (as exigências vêm do estado do animal). Não é uma simulação
completa da fazenda; a comparação ao longo de uma simulação completa está na aba Ração linear da Vaca leiteira.

**Casos** (projetados, não sorteados de uma população): 8 animais (4 vacas em lactação, vaca seca, novilha pré-parto e duas novilhas em
crescimento) × 3 cardápios (5, 7 e 12 alimentos) × 12 conjuntos de preços (o base e 11 sorteados, de 0,5× a 2× o preço-base, semente fixa).
Os preços são ilustrativos, não são cotações. O metano entérico e o nitrogênio urinário são calculados da dieta (``module/emissions.py``).

**Critério (definido antes de rodar).** Diferença do caso = (custo do LP − melhor custo do SLSQP) / melhor custo do SLSQP, em %. Os casos
do mesmo animal e cardápio compartilham exigências e alimentos, então não são independentes: o intervalo de confiança é um bootstrap por
agrupamento (reamostra os grupos animal × cardápio). O LP é *equivalente* se (1) o IC de 90% da diferença média está dentro de ±``MARGIN_PCT``
e (2) ao menos ``SHARE_MIN`` dos casos ficam dentro dessa margem. Fora isso, o relatório diz qual condição falhou.

Uso (na pasta backend)::

    ..\\.venv\\Scripts\\python -m dietopt.benchmark run --out ..\\docs\\benchmark\\v3     # retoma o que já foi feito
    ..\\.venv\\Scripts\\python -m dietopt.benchmark report --out ..\\docs\\benchmark\\v3  # só refaz o resumo e o relatório
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import random
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

VERSION = "v3"
STANDARD = "NASEM"
RESOLUTION = "normal"
SEEDS = 10
MARGIN_PCT = 0.5  # margem de equivalência: 0,5% do custo (desprezível diante de 70% a 85% de variação do custo com os preços)
TIE_PCT = 0.1  # abaixo desta diferença (em %) dois custos contam como iguais (a mesma da interface)
SHARE_MIN = 0.95  # fração mínima de casos dentro da margem
BOOTSTRAP_REPS = 10_000
BOOTSTRAP_SEED = 20261125
PRICE_SEED = 20261125
PRICE_SETS = 11  # além do conjunto-base
PRICE_FACTOR = (0.5, 2.0)  # fator multiplicativo log-uniforme sobre o preço-base de cada alimento

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

# Preços-base ilustrativos (US$ por kg de MS). Ids da biblioteca NASEM.
_BASE = {23: 1.10, 44: 0.28, 50: 0.09, 110: 0.12, 138: 0.25, 167: 0.55, 230: 0.10}  # sangue, milho grão, silagem de milho, silagem de leguminosa, farelo de arroz, soja, calcário
MENUS: dict[str, dict[int, float]] = {
    "enxuto": {44: 0.28, 50: 0.09, 110: 0.12, 167: 0.55, 230: 0.10},
    "base": dict(_BASE),
    "amplo": {**_BASE, 107: 0.22, 163: 0.16, 193: 0.20, 194: 0.30, 231: 0.80},  # + feno de leguminosa, casca de soja, farelo e grão de trigo, fosfato bicálcico
}


# ---------------------------------------------------------------------------------------------------------------------
# Casos
# ---------------------------------------------------------------------------------------------------------------------
def price_sets(menu: str, seed: int = PRICE_SEED) -> list[dict[int, float]]:
    """O conjunto-base e ``PRICE_SETS`` sorteados (fator log-uniforme por alimento); a semente depende do cardápio, então é estável."""
    rng = random.Random(f"{seed}-{menu}")
    base = MENUS[menu]
    sets = [dict(base)]
    low, high = (math.log(f) for f in PRICE_FACTOR)
    for _ in range(PRICE_SETS):
        sets.append({i: round(p * math.exp(rng.uniform(low, high)), 4) for i, p in base.items()})
    return sets


def cases(price_seed: int = PRICE_SEED, animals: Sequence[str] | None = None, menus: Sequence[str] | None = None) -> list[dict[str, Any]]:
    """Lista fixa de casos (identificador estável): animal × cardápio × conjunto de preços."""
    out = []
    for animal in animals or ANIMALS:
        for menu in menus or MENUS:
            for k, prices in enumerate(price_sets(menu, price_seed)):
                out.append({"id": f"{animal}/{menu}/p{k}", "animal": animal, "menu": menu, "price_set": k, "prices": prices, "price_seed": price_seed})
    return out


# ---------------------------------------------------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------------------------------------------------
def run_case(case: Mapping[str, Any], resolution: str = RESOLUTION, seeds: int = SEEDS) -> dict[str, Any]:
    """Roda o LP e o SLSQP do RuFaS no caso e guarda só o que a análise usa (sem as quantidades, para o arquivo ficar pequeno)."""
    from .module.optimize import optimize_diet  # importação tardia: carrega o RuFaS

    category, animal_type, cow = ANIMALS[case["animal"]]
    prices = {str(i): p for i, p in case["prices"].items()}
    started = time.perf_counter()
    result = optimize_diet(STANDARD, category, cow, list(case["prices"]), prices, None, None, animal_type, resolution, seeds)
    record: dict[str, Any] = {k: case[k] for k in ("id", "animal", "menu", "price_set", "prices", "price_seed")}
    record |= {"resolution": resolution, "status": result["status"], "wall_seconds": time.perf_counter() - started}
    if result["status"] != "ok":
        record["slsqp_converged"] = _slsqp_on_infeasible(category, animal_type, cow, case["prices"], seeds)
        return record
    diet = result["diet"]
    record["lp"] = {"cost": diet["cost"], "verified": bool(diet["verified"]), "seconds": result["search"]["seconds"], "regime": diet["regime"]}
    record["slsqp"] = [
        {"seed": r["seed"], "ok": bool(r["success"] and r["feasible"]), "cost": float(r["cost"]), "seconds": float(r["seconds"])} for r in result["rufas"]["runs"]
    ]
    return record


def _slsqp_on_infeasible(category: str, animal_type: str, cow: Mapping[str, Any], prices: Mapping[int, float], seeds: int) -> int:
    """Quando o LP diz "sem solução", confere se o SLSQP concorda: quantas execuções convergiram (o esperado é zero)."""
    from .module import optimize as opt
    from .module.evaluate import resolve_limits
    from .module.requirements import compute_requirements

    ids = sorted(prices)
    required = compute_requirements(STANDARD, category, cow, None, animal_type)
    problem = opt.build_problem(STANDARD, category, animal_type, cow, ids, dict(prices), resolve_limits(STANDARD, ids, None), required)
    return sum(1 for r in opt.run_rufas(problem, category, seeds) if r["success"])


def load(out: Path) -> list[dict[str, Any]]:
    path = out / "resultados.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.exists() else []
    order = {c["id"]: i for i, c in enumerate(cases(rows[0]["price_seed"] if rows else PRICE_SEED))}
    return sorted(rows, key=lambda r: order.get(r["id"], len(order)))


def run(out: Path, limit: int | None = None, resolution: str = RESOLUTION, seeds: int = SEEDS, price_seed: int = PRICE_SEED,
        animals: Sequence[str] | None = None, menus: Sequence[str] | None = None) -> None:  # fmt: skip
    """Executa os casos que ainda não estão em ``resultados.jsonl`` (retoma de onde parou) e grava o relatório ao final."""
    out.mkdir(parents=True, exist_ok=True)
    path = out / "resultados.jsonl"
    done = {r["id"] for r in load(out)}
    todo = [c for c in cases(price_seed, animals, menus) if c["id"] not in done][:limit]
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


def good_costs(record: Mapping[str, Any]) -> list[float]:
    """Custos das execuções do SLSQP que convergiram e atendem às restrições originais do RuFaS."""
    return [r["cost"] for r in record["slsqp"] if r["ok"]]


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


def describe(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Medidas de um conjunto de casos resolvidos: diferença contra o melhor SLSQP, equivalência, ganhos e perdas, falhas, sementes e tempo."""
    usable = [r for r in rows if r["status"] == "ok" and good_costs(r)]
    out: dict[str, Any] = {"cases": len(rows), "solved": sum(1 for r in rows if r["status"] == "ok"), "compared": len(usable)}
    if not usable:
        return out
    gaps = [gap_pct(r["lp"]["cost"], min(good_costs(r))) for r in usable]
    groups: dict[str, list[float]] = {}
    for r, g in zip(usable, gaps):
        groups.setdefault(f"{r['animal']}/{r['menu']}", []).append(g)
    low, high = cluster_bootstrap_ci(groups)
    d = np.asarray(gaps)
    share = float((np.abs(d) <= MARGIN_PCT).mean())
    ci_ok = bool(low > -MARGIN_PCT and high < MARGIN_PCT)
    runs = [x for r in rows if r["status"] == "ok" for x in r["slsqp"]]
    spread = [(max(c) - min(c)) / min(c) * 100 for r in usable if len(c := good_costs(r)) > 1]
    lp_s = [r["lp"]["seconds"] for r in rows if r["status"] == "ok"]
    sl_s = [x["seconds"] for x in runs]
    price_effect = []  # quanto o custo ótimo varia com os preços dentro de cada animal × cardápio
    for costs in ([min(good_costs(r)) for r in usable if f"{r['animal']}/{r['menu']}" == key] for key in groups):
        if len(costs) > 1:
            price_effect.append((max(costs) - min(costs)) / min(costs) * 100)
    out |= {
        "mean": float(d.mean()), "median": float(np.median(d)), "min": float(d.min()), "max": float(d.max()), "ci90": [low, high],
        "share_within_margin": share, "ci_within_margin": ci_ok, "equivalent": ci_ok and share >= SHARE_MIN,
        "lp_cheaper": int((d < -TIE_PCT).sum()), "tie": int((np.abs(d) <= TIE_PCT).sum()), "lp_dearer": int((d > TIE_PCT).sum()),
        "lp_verified": sum(1 for r in rows if r["status"] == "ok" and r["lp"]["verified"]),
        "slsqp_runs": len(runs), "slsqp_failed": sum(1 for x in runs if not x["ok"]),
        "cases_with_a_failure": sum(1 for r in rows if r["status"] == "ok" and any(not x["ok"] for x in r["slsqp"])),
        "seed_spread_pct": {"mean": float(np.mean(spread)), "max": float(np.max(spread))} if spread else None,
        "lp_seconds_median": statistics.median(lp_s), "slsqp_seconds_median": statistics.median(sl_s) if sl_s else None,
        "price_effect_pct": {"mean": float(np.mean(price_effect)), "max": float(np.max(price_effect))} if price_effect else None,
        "outliers": sorted(({"id": r["id"], "gap_pct": g, "lp_regime": r["lp"]["regime"]} for r, g in zip(usable, gaps) if abs(g) > MARGIN_PCT), key=lambda o: -abs(o["gap_pct"])),
    }  # fmt: skip
    return out


def summarize(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Tudo o que o relatório mostra: o total e, em separado, cada animal e cada cardápio."""
    return {
        "version": VERSION, "standard": STANDARD, "margin_pct": MARGIN_PCT, "tie_pct": TIE_PCT, "share_min": SHARE_MIN,
        "overall": describe(rows),
        "by_animal": {a: describe([r for r in rows if r["animal"] == a]) for a in ANIMALS if any(r["animal"] == a for r in rows)},
        "by_menu": {m: describe([r for r in rows if r["menu"] == m]) for m in MENUS if any(r["menu"] == m for r in rows)},
        "unsolved": [{"id": r["id"], "status": r["status"], "slsqp_converged": r.get("slsqp_converged")} for r in rows if r["status"] != "ok"],
    }  # fmt: skip


# ---------------------------------------------------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------------------------------------------------
def _f(value: float | None, digits: int = 3) -> str:
    return "-" if value is None else f"{value:.{digits}f}".replace(".", ",")


def _line(label: str, g: Mapping[str, Any]) -> str:
    if not g.get("compared"):
        return f"  {label:<20} {g['solved']} de {g['cases']} resolvidos; nenhum comparável"
    verdict = "equivalente" if g["equivalent"] else "NÃO demonstrado"
    return (f"  {label:<20} n={g['compared']:>3}  média {_f(g['mean'], 3):>7}%  IC90 {_f(g['ci90'][0], 3)} a {_f(g['ci90'][1], 3)}  mín {_f(g['min'], 2)}  máx {_f(g['max'], 2)}  "
            f"dentro da margem {_f(g['share_within_margin'] * 100, 0)}%  LP<=/=/>: {g['lp_cheaper']}/{g['tie']}/{g['lp_dearer']}  {verdict}")  # fmt: skip


def report_text(summary: Mapping[str, Any], meta: Mapping[str, Any]) -> str:
    o = summary["overall"]
    lines = [
        f"BENCHMARK {summary['version']}: LP × SLSQP do RuFaS (padrão {summary['standard']} 2021)",
        f"Margem de equivalência ±{_f(summary['margin_pct'], 1)}%; empate até {_f(summary['tie_pct'], 1)}%; LP na resolução {meta['resolution']}; {meta['seeds']} sementes do SLSQP por caso.",
        "Diferença = (custo do LP − melhor custo do SLSQP) / melhor custo do SLSQP, em %; negativa = o LP é mais barato. Preços ilustrativos.",
        "",
        "RESULTADO GERAL",
        f"  Casos: {o['cases']}; resolvidos pelo LP: {o['solved']}; comparáveis (ao menos uma execução viável do SLSQP): {o['compared']}; "
        f"dietas do LP que atendem às restrições do RuFaS: {o.get('lp_verified', 0)} de {o['solved']}.",
    ]
    if o.get("compared"):
        lines += [
            f"  Diferença média {_f(o['mean'], 3)}% (mediana {_f(o['median'], 3)}%; de {_f(o['min'], 2)}% a {_f(o['max'], 2)}%). IC de 90% por agrupamento: {_f(o['ci90'][0], 3)}% a {_f(o['ci90'][1], 3)}%.",
            f"  Dentro da margem: {_f(o['share_within_margin'] * 100, 1)}% dos casos (mínimo exigido {_f(summary['share_min'] * 100, 0)}%). LP mais barato / empate / mais caro: {o['lp_cheaper']} / {o['tie']} / {o['lp_dearer']}.",
            f"  VEREDITO: {'EQUIVALENTE' if o['equivalent'] else 'equivalência NÃO demonstrada'} "
            f"(IC dentro da margem: {'sim' if o['ci_within_margin'] else 'não'}; fração dentro da margem: {'sim' if o['share_within_margin'] >= summary['share_min'] else 'não'}).",
            f"  Falhas do SLSQP: {o['slsqp_failed']} de {o['slsqp_runs']} execuções ({_f(o['slsqp_failed'] / o['slsqp_runs'] * 100, 1)}%), em {o['cases_with_a_failure']} casos; o LP resolveu {o['solved']} de {o['cases']}.",
        ]
        if o["seed_spread_pct"]:
            lines.append(f"  Entre as sementes do SLSQP (execuções viáveis): a pior custa, em média, {_f(o['seed_spread_pct']['mean'], 3)}% e, no máximo, {_f(o['seed_spread_pct']['max'], 2)}% mais que a melhor.")
        lines.append(f"  Tempo (mediana): LP {_f(o['lp_seconds_median'], 1)} s por problema; SLSQP {_f(o['slsqp_seconds_median'], 2)} s por execução.")
        if o["price_effect_pct"]:
            lines.append(f"  Os preços mexem muito mais no custo que o método: o custo ótimo varia {_f(o['price_effect_pct']['mean'], 0)}% em média (até {_f(o['price_effect_pct']['max'], 0)}%) entre os conjuntos de preços; a diferença entre métodos é de centésimos a décimos.")
        if o["outliers"]:
            lines.append(f"  Casos fora da margem ({len(o['outliers'])}):")
            lines += [f"    {x['id']}: {_f(x['gap_pct'], 3)}% (regime do LP: {x['lp_regime']})" for x in o["outliers"][:15]]
    lines += ["", "POR ANIMAL (cada linha tem seu próprio IC; poucos casos por linha, leia como indicação)"]
    lines += [_line(a, g) for a, g in summary["by_animal"].items()]
    lines += ["", "POR CARDÁPIO"]
    lines += [_line(m, g) for m, g in summary["by_menu"].items()]
    if summary["unsolved"]:
        agree = sum(1 for u in summary["unsolved"] if u.get("slsqp_converged") == 0)
        lines += [
            "",
            f"SEM SOLUÇÃO NO LP ({len(summary['unsolved'])}); o SLSQP também não convergiu em nenhuma semente em {agree} deles"
            + ("" if agree == len(summary["unsolved"]) else " (ATENÇÃO: nos demais o SLSQP achou dieta; ver resultados.jsonl)")
            + ": " + ", ".join(u["id"] for u in summary["unsolved"][:30]),
        ]
    lines += [
        "",
        "Como ler: os casos são projetados (animais × cardápios × preços), não uma amostra de fazendas; a conclusão vale para essa família de casos.",
        "O animal é avaliado em um dia (não é uma simulação completa). O IC reamostra os grupos animal × cardápio, que compartilham exigências.",
        f"Reprodução: cd backend; ..\\.venv\\Scripts\\python -m dietopt.benchmark run --out ..\\docs\\benchmark\\v3   (Python {meta['python']}, numpy {meta['numpy']}).",
    ]
    return "\n".join(lines) + "\n"


def write_report(out: Path) -> None:
    rows = load(out)
    meta = {
        "resolution": next((r["resolution"] for r in rows), RESOLUTION), "seeds": max((len(r["slsqp"]) for r in rows if "slsqp" in r), default=SEEDS),
        "price_seed": next((r["price_seed"] for r in rows), PRICE_SEED), "python": platform.python_version(), "numpy": np.__version__,
    }  # fmt: skip
    summary = summarize(rows) | {"meta": meta}
    (out / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    text = report_text(summary, meta)
    (out / "RELATORIO.txt").write_text(text, encoding="utf-8")
    print(text)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=("run", "report", "cases"))
    parser.add_argument("--out", type=Path, default=Path("..") / "docs" / "benchmark" / "v3")
    parser.add_argument("--limit", type=int, default=None, help="máximo de casos a executar nesta chamada")
    parser.add_argument("--resolution", default=RESOLUTION, choices=("rapida", "normal", "fina"))
    parser.add_argument("--seeds", type=int, default=SEEDS)
    parser.add_argument("--price-seed", type=int, default=PRICE_SEED, help="outra semente = outros conjuntos de preços (casos novos)")
    parser.add_argument("--animals", nargs="+", choices=list(ANIMALS), default=None)
    parser.add_argument("--menus", nargs="+", choices=list(MENUS), default=None)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # o console do Windows (cp1252) não tem o sinal de menos
    if args.command == "cases":
        print(json.dumps(cases(args.price_seed, args.animals, args.menus), ensure_ascii=False, indent=1))
    elif args.command == "run":
        run(args.out, args.limit, args.resolution, args.seeds, args.price_seed, args.animals, args.menus)
    else:
        write_report(args.out)


if __name__ == "__main__":
    sys.exit(main())
