"""Benchmark estatístico: dieta ótima por programação linear (LP) contra o SLSQP do RuFaS, em casos fixos e reproduzíveis.

Pergunta: o custo da dieta do LP é *equivalente* ao do melhor SLSQP do RuFaS (diferença relativa dentro de uma margem), e o que
cada método tem de diferente (estabilidade, falhas, tempo)? O desenho está em ``docs/CONCLUSOES_PREVIAS.txt`` (seção 5).

Os casos são **projetados**, não sorteados de uma população real: 4 vacas × (preços-base + 8 conjuntos de preços sorteados com
semente fixa) × os 2 padrões (NASEM e NRC). Tudo é determinístico (``VERSION`` identifica o desenho); só os tempos variam de uma
máquina para outra. Cada caso roda ``optimize_diet`` (a mesma rota da tela Dieta ótima do Ruminante Singular): o LP com a
resolução pedida e N execuções do ``RationOptimizer`` do RuFaS, cada uma com uma semente de ponto inicial.

Uso (na pasta backend)::

    ..\\.venv\\Scripts\\python -m dietopt.benchmark run --out ..\\docs\\benchmark     # retoma o que já foi feito
    ..\\.venv\\Scripts\\python -m dietopt.benchmark report --out ..\\docs\\benchmark  # só refaz o resumo e o relatório
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
from scipy import stats as sp_stats

VERSION = "v2"  # v2 (20/11/2026): o metano e o nitrogênio urinário do NASEM são calculados da dieta (v1 os fixava em 400 g/dia e 0,2 kg/dia)
RESOLUTION = "normal"
SEEDS = 10
TIE_PCT = 0.1  # diferença (em %) abaixo da qual dois custos contam como iguais (a mesma da interface)
MARGIN_PCT = 0.5  # margem de equivalência (decisão de 20/11/2026; ver CONCLUSOES_PREVIAS, 5.2)
MARGINS = (0.1, 0.25, 0.5, 1.0)  # margens mostradas no relatório, para ver o quanto a conclusão depende da escolha
BOOTSTRAP_REPS = 10_000
BOOTSTRAP_SEED = 20261120
PRICE_SEED = 20261120
PRICE_SETS = 8  # além do conjunto-base
PRICE_FACTOR = (0.5, 2.0)  # fator multiplicativo log-uniforme sobre o preço-base de cada alimento
STANDARDS = ("NASEM", "NRC")

FEEDS = [23, 44, 50, 110, 138, 167, 230]  # conjunto base (LINEARIZACAO.md, 10.1); existem nos dois padrões
BASE_PRICES = {23: 1.10, 44: 0.28, 50: 0.09, 110: 0.12, 138: 0.25, 167: 0.55, 230: 0.10}  # ilustrativos, não são cotações
# O metano e o nitrogênio urinário do NASEM não são entradas: o módulo os calcula da dieta (``module/emissions.py``), e o SLSQP do RuFaS,
# que só aceita constantes, recebe os valores da dieta do LP.

COWS: dict[str, dict[str, Any]] = {
    "alta": dict(body_weight=650, mature_body_weight=700, parity=2, days_in_milk=100, day_of_pregnancy=60, body_condition_score_5=3.0,
                 calving_interval=400, milk_production=40, milk_fat=3.7, milk_true_protein=3.1, milk_lactose=4.85, housing="Barn", distance=100),
    "media": dict(body_weight=620, mature_body_weight=700, parity=3, days_in_milk=180, day_of_pregnancy=100, body_condition_score_5=3.0,
                  calving_interval=400, milk_production=30, milk_fat=3.8, milk_true_protein=3.2, milk_lactose=4.85, housing="Barn", distance=100),
    "final": dict(body_weight=680, mature_body_weight=720, parity=4, days_in_milk=280, day_of_pregnancy=200, body_condition_score_5=3.25,
                  calving_interval=400, milk_production=20, milk_fat=4.0, milk_true_protein=3.3, milk_lactose=4.8, housing="Barn", distance=100),
    "primipara": dict(body_weight=560, mature_body_weight=680, parity=1, days_in_milk=90, day_of_pregnancy=5, body_condition_score_5=3.0,
                      calving_interval=400, milk_production=35, milk_fat=3.6, milk_true_protein=3.0, milk_lactose=4.85, housing="Barn", distance=100),
}  # fmt: skip


def price_sets(seed: int = PRICE_SEED) -> list[dict[int, float]]:
    """Conjunto-base e ``PRICE_SETS`` conjuntos sorteados (fator log-uniforme de 0,5 a 2 por alimento, semente fixa).

    Outra ``seed`` dá casos NOVOS com o mesmo desenho (validação fora da amostra de uma mudança feita depois de ver os resultados)."""
    rng = random.Random(seed)
    sets = [dict(BASE_PRICES)]
    low, high = (math.log(f) for f in PRICE_FACTOR)
    for _ in range(PRICE_SETS):
        sets.append({i: round(BASE_PRICES[i] * math.exp(rng.uniform(low, high)), 4) for i in FEEDS})
    return sets


def cases(price_seed: int = PRICE_SEED, standards: Sequence[str] = STANDARDS) -> list[dict[str, Any]]:
    """Lista fixa de casos (id estável): padrão × vaca × conjunto de preços."""
    sets = price_sets(price_seed)
    out = []
    for standard in standards:
        for cow_name, cow in COWS.items():
            for k, prices in enumerate(sets):
                out.append(
                    {
                        "id": f"{standard}-{cow_name}-p{k}",
                        "standard": standard,
                        "cow_name": cow_name,
                        "price_set": k,
                        "cow": dict(cow),
                        "prices": prices,
                        "price_seed": price_seed,
                    }
                )
    return out


# ---------------------------------------------------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------------------------------------------------
def run_case(case: Mapping[str, Any], resolution: str = RESOLUTION, seeds: int = SEEDS) -> dict[str, Any]:
    """Roda o LP e o SLSQP do RuFaS no caso e devolve só o que a análise usa (sem as quantidades, para o arquivo ficar pequeno)."""
    from .module.optimize import optimize_diet  # importação tardia: carrega o RuFaS

    started = time.perf_counter()
    result = optimize_diet(
        case["standard"], "LAC_COW", case["cow"], FEEDS, {str(i): p for i, p in case["prices"].items()}, None, None, "LAC_COW", resolution, seeds
    )
    record: dict[str, Any] = {
        "id": case["id"], "standard": case["standard"], "cow_name": case["cow_name"], "price_set": case["price_set"],
        "prices": case["prices"], "price_seed": case.get("price_seed", PRICE_SEED), "resolution": resolution, "status": result["status"], "wall_seconds": time.perf_counter() - started,
    }  # fmt: skip
    if result["status"] != "ok":
        return record
    diet = result["diet"]
    record["lp"] = {"cost": diet["cost"], "verified": bool(diet["verified"]), "seconds": result["search"]["seconds"], "regime": diet["regime"]}
    record["slsqp"] = [
        {"seed": r["seed"], "success": bool(r["success"]), "feasible": bool(r["feasible"]), "cost": float(r["cost"]), "seconds": float(r["seconds"])}
        for r in result["rufas"]["runs"]
    ]
    return record


def run(
    out: Path, limit: int | None = None, resolution: str = RESOLUTION, seeds: int = SEEDS, price_seed: int = PRICE_SEED,
    standards: Sequence[str] = STANDARDS,
) -> None:
    """Executa os casos que ainda não estão em ``resultados.jsonl`` (retoma de onde parou) e grava o relatório ao final."""
    out.mkdir(parents=True, exist_ok=True)
    path = out / "resultados.jsonl"
    done = {json.loads(line)["id"] for line in path.read_text(encoding="utf-8").splitlines() if line.strip()} if path.exists() else set()
    todo = [c for c in cases(price_seed, standards) if c["id"] not in done][:limit]
    print(f"{len(done)} casos prontos, {len(todo)} a executar (resolução {resolution}, {seeds} sementes)", flush=True)
    for n, case in enumerate(todo, 1):
        record = run_case(case, resolution, seeds)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        lp = record.get("lp", {}).get("cost")
        print(f"[{n}/{len(todo)}] {case['id']}: {record['status']}, LP {lp if lp is None else round(lp, 4)}, {record['wall_seconds']:.1f} s", flush=True)
    write_report(out)


def load(out: Path) -> list[dict[str, Any]]:
    path = out / "resultados.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    order = {c["id"]: i for i, c in enumerate(cases())}
    return sorted(rows, key=lambda r: order.get(r["id"], len(order)))


# ---------------------------------------------------------------------------------------------------------------------
# Estatística
# ---------------------------------------------------------------------------------------------------------------------
def gap_pct(lp: float, reference: float) -> float:
    """Diferença relativa do custo do LP sobre o de referência, em %: negativa = o LP é mais barato."""
    return (lp - reference) / reference * 100


def feasible_costs(record: Mapping[str, Any]) -> list[float]:
    """Custos das execuções do SLSQP que convergiram e atendem às restrições originais do RuFaS."""
    return [r["cost"] for r in record["slsqp"] if r["success"] and r["feasible"]]


def tost(values: Sequence[float], margin: float) -> dict[str, float]:
    """Teste de equivalência pareado (duas provas unilaterais, TOST) para a média das diferenças contra ±``margin`` (em %).

    H0: |média| >= margem; rejeitar (p < 0,05) significa equivalência. Usa a distribuição t de Student (n − 1 g.l.).
    """
    d = np.asarray(values, dtype=float)
    n = len(d)
    mean = float(d.mean())
    sd = float(d.std(ddof=1)) if n > 1 else 0.0
    if sd == 0.0:
        p = 0.0 if abs(mean) < margin else 1.0
    else:
        se = sd / math.sqrt(n)
        p_low = float(1 - sp_stats.t.cdf((mean + margin) / se, n - 1))  # H0: média <= −margem
        p_up = float(sp_stats.t.cdf((mean - margin) / se, n - 1))  # H0: média >= +margem
        p = max(p_low, p_up)
    return {"p": p, "equivalent": p < 0.05}


def bootstrap_ci(values: Sequence[float], level: float = 0.90, reps: int = BOOTSTRAP_REPS, seed: int = BOOTSTRAP_SEED) -> tuple[float, float]:
    """Intervalo percentil de bootstrap para a média; o de 90% dentro de ±margem equivale ao TOST a 5%."""
    d = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    means = d[rng.integers(0, len(d), (reps, len(d)))].mean(axis=1)
    tail = (1 - level) / 2 * 100
    low, high = np.percentile(means, [tail, 100 - tail])
    return float(low), float(high)


def wilcoxon_p(values: Sequence[float]) -> float | None:
    """Teste de Wilcoxon de postos sinalizados (bilateral) para a mediana das diferenças diferente de zero; zeros são descartados."""
    d = np.asarray([v for v in values if abs(v) > 1e-9], dtype=float)
    if len(d) < 1:
        return None
    return float(sp_stats.wilcoxon(d).pvalue)


def describe(values: Sequence[float], margin: float = MARGIN_PCT) -> dict[str, Any]:
    """Resumo de uma amostra de diferenças relativas (em %): posição, dispersão, equivalência e ganhos e perdas."""
    d = np.asarray(values, dtype=float)
    if len(d) == 0:
        return {"n": 0}
    low, high = bootstrap_ci(d)
    return {
        "n": len(d),
        "mean": float(d.mean()), "median": float(np.median(d)), "sd": float(d.std(ddof=1)) if len(d) > 1 else 0.0,
        "min": float(d.min()), "max": float(d.max()),
        "ci90": [low, high],
        "tost_p": tost(d, margin)["p"],
        "equivalent_by_margin": {str(m): {"tost": tost(d, m)["equivalent"], "ci90": bool(low > -m and high < m)} for m in MARGINS},
        "within_margin": int((np.abs(d) <= margin).sum()),
        "lp_cheaper": int((d < -TIE_PCT).sum()), "tie": int((np.abs(d) <= TIE_PCT).sum()), "lp_dearer": int((d > TIE_PCT).sum()),
        "wilcoxon_p": wilcoxon_p(d),
    }  # fmt: skip


def summarize(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Todas as medidas do benchmark, por padrão e juntos."""
    out: dict[str, Any] = {"version": VERSION, "margin_pct": MARGIN_PCT, "tie_pct": TIE_PCT, "groups": {}}
    for label, subset in [(s, [r for r in rows if r["standard"] == s]) for s in STANDARDS] + [("todos", list(rows))]:
        ok = [r for r in subset if r["status"] == "ok"]
        usable = [r for r in ok if feasible_costs(r)]
        d_best = [gap_pct(r["lp"]["cost"], min(feasible_costs(r))) for r in usable]
        d_median = [gap_pct(r["lp"]["cost"], statistics.median(feasible_costs(r))) for r in usable]
        first = [next((x for x in r["slsqp"] if x["seed"] == 0), None) for r in ok]
        d_single = [gap_pct(r["lp"]["cost"], f["cost"]) for r, f in zip(ok, first) if f and f["success"] and f["feasible"]]
        runs = [x for r in ok for x in r["slsqp"]]
        failed = [x for x in runs if not (x["success"] and x["feasible"])]
        excess = [(max(c) - min(c)) / min(c) * 100 for r in usable if len(c := feasible_costs(r)) > 1]
        cv = [statistics.stdev(c) / statistics.mean(c) * 100 for r in usable if len(c := feasible_costs(r)) > 1]
        lp_seconds = [r["lp"]["seconds"] for r in ok]
        slsqp_seconds = [x["seconds"] for x in runs]
        spreads = []
        for standard, cow in {(r["standard"], r["cow_name"]) for r in usable}:  # nunca mistura padrões: o custo de cada um é outro
            costs = [min(feasible_costs(r)) for r in usable if r["standard"] == standard and r["cow_name"] == cow]
            if len(costs) > 1:
                spreads.append((max(costs) - min(costs)) / min(costs) * 100)
        out["groups"][label] = {
            "cases": len(subset), "ok": len(ok), "infeasible": len(subset) - len(ok),
            "lp_verified": sum(1 for r in ok if r["lp"]["verified"]),
            "d_best": describe(d_best), "d_median": describe(d_median), "d_single": describe(d_single),
            "slsqp_runs": len(runs), "slsqp_failed": len(failed),
            "slsqp_failed_pct": len(failed) / len(runs) * 100 if runs else None,
            "cases_with_a_failure": sum(1 for r in ok if any(not (x["success"] and x["feasible"]) for x in r["slsqp"])),
            "seed_excess_pct": {"mean": float(np.mean(excess)), "max": float(np.max(excess))} if excess else None,
            "seed_cv_pct": {"mean": float(np.mean(cv)), "max": float(np.max(cv))} if cv else None,
            "cases_single_run_worse_than_margin": sum(1 for v in d_single if v < -MARGIN_PCT),
            "lp_seconds_median": statistics.median(lp_seconds) if lp_seconds else None,
            "slsqp_seconds_median": statistics.median(slsqp_seconds) if slsqp_seconds else None,
            "time_ratio": statistics.median(lp_seconds) / statistics.median(slsqp_seconds) if lp_seconds and slsqp_seconds else None,
            "price_effect_pct": {"mean": float(np.mean(spreads)), "max": float(np.max(spreads))} if spreads else None,
            "method_effect_pct": {"mean_abs": float(np.mean(np.abs(d_best))), "max_abs": float(np.max(np.abs(d_best)))} if d_best else None,
            "mean_cost": statistics.mean(r["lp"]["cost"] for r in ok) if ok else None,
            "outliers": sorted(
                ({"id": r["id"], "gap_pct": g, "lp_regime": r["lp"]["regime"]} for r, g in zip(usable, d_best) if abs(g) > MARGIN_PCT),
                key=lambda o: -abs(o["gap_pct"]),
            ),
        }  # fmt: skip
    return out


# ---------------------------------------------------------------------------------------------------------------------
# Relatório
# ---------------------------------------------------------------------------------------------------------------------
def _f(value: float | None, digits: int = 3) -> str:
    return "-" if value is None else f"{value:.{digits}f}".replace(".", ",")


def _verdict(group: Mapping[str, Any]) -> str:
    best = group["d_best"]
    if not best["n"]:
        return "sem casos"
    by = best["equivalent_by_margin"][str(MARGIN_PCT)]
    return "EQUIVALENTE" if by["tost"] and by["ci90"] else "equivalência não demonstrada"


def report_text(summary: Mapping[str, Any], meta: Mapping[str, Any]) -> str:
    lines = [
        f"BENCHMARK LP × SLSQP DO RuFaS — desenho {summary['version']}",
        f"Margem de equivalência: ±{_f(summary['margin_pct'], 2)}% do custo; empate: até {_f(summary['tie_pct'], 1)}%. "
        f"Resolução do LP: {meta.get('resolution', RESOLUTION)}; {meta.get('seeds', SEEDS)} sementes do SLSQP por caso; semente dos preços: {meta.get('price_seed', PRICE_SEED)}.",
        "Diferença = (custo do LP − custo do SLSQP) / custo do SLSQP, em %; negativa = o LP é mais barato. Custos ilustrativos (não são cotações).",
        "",
    ]
    for label, g in summary["groups"].items():
        title = {"NASEM": "NASEM 2021", "NRC": "NRC 2001", "todos": "Os dois padrões juntos"}[label]
        lines += [f"== {title}: {g['ok']} de {g['cases']} casos resolvidos ({g['infeasible']} sem solução); dietas do LP que atendem às restrições do RuFaS: {g['lp_verified']} de {g['ok']}"]
        for key, name in (("d_best", "LP contra o MELHOR SLSQP (de 10 sementes)"), ("d_median", "LP contra a MEDIANA do SLSQP"), ("d_single", "LP contra UMA execução do SLSQP (semente 0)")):
            d = g[key]
            if not d["n"]:
                continue
            lines.append(f"  {name}: n = {d['n']}; média {_f(d['mean'], 4)}%, mediana {_f(d['median'], 4)}%, mín. {_f(d['min'], 3)}%, máx. {_f(d['max'], 3)}%")
            lines.append(
                f"    IC 90% (bootstrap) da média: {_f(d['ci90'][0], 4)}% a {_f(d['ci90'][1], 4)}%; TOST p = {_f(d['tost_p'], 4)}; "
                f"Wilcoxon p = {_f(d['wilcoxon_p'], 4)}; LP mais barato / empate / LP mais caro: {d['lp_cheaper']} / {d['tie']} / {d['lp_dearer']}"
            )
            marg = "; ".join(f"±{_f(float(m), 2)}%: {'sim' if v['tost'] and v['ci90'] else 'não'}" for m, v in d["equivalent_by_margin"].items())
            lines.append(f"    Equivalência (TOST e IC 90% concordam) por margem: {marg}")
        lines.append(f"  Casos fora da margem (LP contra o melhor SLSQP): {len(g['outliers'])}")
        lines += [f"    {o['id']}: {_f(o['gap_pct'], 3)}% (regime do LP: {o['lp_regime']})" for o in g["outliers"][:8]]
        lines += [
            f"  Falhas do SLSQP: {g['slsqp_failed']} de {g['slsqp_runs']} execuções ({_f(g['slsqp_failed_pct'], 1)}%), em {g['cases_with_a_failure']} caso(s); o LP resolveu {g['ok']} de {g['cases']}.",
        ]
        if g["seed_excess_pct"]:
            lines.append(
                f"  Entre sementes (execuções viáveis): a pior custa em média {_f(g['seed_excess_pct']['mean'], 3)}% e no máximo {_f(g['seed_excess_pct']['max'], 3)}% mais que a melhor; "
                f"CV médio {_f(g['seed_cv_pct']['mean'], 3)}%. Uma única execução custou mais que o LP além da margem em {g['cases_single_run_worse_than_margin']} casos."
            )
        lines.append(f"  Tempo (mediana): LP {_f(g['lp_seconds_median'], 1)} s por problema; SLSQP {_f(g['slsqp_seconds_median'], 2)} s por execução; razão {_f(g['time_ratio'], 0)}×.")
        if g["price_effect_pct"] and g["method_effect_pct"]:
            lines.append(
                f"  Efeito dos preços × efeito do método: o custo ótimo varia de {_f(g['price_effect_pct']['mean'], 0)}% (média por vaca; máx. {_f(g['price_effect_pct']['max'], 0)}%) "
                f"entre os conjuntos de preços; a diferença entre os métodos é de {_f(g['method_effect_pct']['mean_abs'], 4)}% em média (máx. {_f(g['method_effect_pct']['max_abs'], 3)}%)."
            )
        lines.append(f"  VEREDITO (margem ±{_f(summary['margin_pct'], 2)}%): {_verdict(g)}")
        means = [summary["groups"][s_]["d_best"].get("mean") for s_ in STANDARDS]
        if label == "todos" and all(m is not None for m in means) and means[0] * means[1] < 0:
            lines.append(
                "  ATENÇÃO: o agregado mistura efeitos de sinais opostos (diferença média "
                + " e ".join(f"{_f(m, 3)}% no {s_}" for m, s_ in zip(means, STANDARDS))
                + "); os efeitos se compensam. Vale o veredito de cada padrão, não este."
            )
        lines.append("")
    lines += [
        "Como ler: o teste de equivalência (TOST) só diz que a diferença MÉDIA está dentro da margem; o máximo mostra o pior caso. Os casos são projetados",
        "(4 vacas × 9 conjuntos de preços), não uma amostra aleatória de fazendas: a conclusão vale para essa família de casos.",
        f"Reprodução: cd backend; ..\\.venv\\Scripts\\python -m dietopt.benchmark run --out ..\\docs\\benchmark   (cerca de 20 a 30 min; Python {meta.get('python', '?')}, numpy {meta.get('numpy', '?')}, scipy {meta.get('scipy', '?')}).",
    ]
    return "\n".join(lines) + "\n"


def write_report(out: Path) -> None:
    rows = load(out)
    resolution = next((r["resolution"] for r in rows), RESOLUTION)
    seeds = max((len(r["slsqp"]) for r in rows if "slsqp" in r), default=SEEDS)
    price_seed = next((r["price_seed"] for r in rows if "price_seed" in r), PRICE_SEED)
    meta = {"price_seed": price_seed, "resolution": resolution, "seeds": seeds, "python": platform.python_version(), "numpy": np.__version__, "scipy": __import__("scipy").__version__}
    summary = summarize(rows)
    summary["meta"] = meta
    (out / "resumo.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    text = report_text(summary, meta)
    (out / f"RELATORIO_BENCHMARK_{VERSION}.txt").write_text(text, encoding="utf-8")
    print(text)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("command", choices=("run", "report", "cases"))
    parser.add_argument("--out", type=Path, default=Path("..") / "docs" / "benchmark")
    parser.add_argument("--limit", type=int, default=None, help="máximo de casos a executar nesta chamada")
    parser.add_argument("--resolution", default=RESOLUTION, choices=("rapida", "normal", "fina"))
    parser.add_argument("--seeds", type=int, default=SEEDS)
    parser.add_argument("--price-seed", type=int, default=PRICE_SEED, help="outra semente = outros conjuntos de preços (casos novos)")
    parser.add_argument("--standards", nargs="+", default=list(STANDARDS), choices=STANDARDS)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # o console do Windows (cp1252) não tem o sinal de menos
    if args.command == "cases":
        print(json.dumps(cases(args.price_seed, args.standards), ensure_ascii=False, indent=1))
    elif args.command == "run":
        run(args.out, args.limit, args.resolution, args.seeds, args.price_seed, args.standards)
    else:
        write_report(args.out)


if __name__ == "__main__":
    sys.exit(main())
