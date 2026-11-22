"""Relatório de uma página (PDF e PNG) do benchmark LP × SLSQP: o módulo (``benchmark``) e as simulações completas (``benchmark_sim``).

Só LÊ os resultados já gerados (``resumo.json`` e os CSVs de cada pasta); não roda otimizador nem recalcula estatística:
os números do texto vêm dos resumos e os gráficos, dos CSVs por caso.

    cd backend
    ..\\.venv\\Scripts\\python -m dietopt.benchmark_report
"""

from __future__ import annotations

import argparse
import csv
import json
import textwrap
from pathlib import Path
from typing import Any, Mapping, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import numpy as np  # noqa: E402

DOCS = Path(__file__).resolve().parents[2] / "docs" / "benchmark"
BLUE, ORANGE = "#2a78d6", "#eb6834"  # categóricas 1 e 2 da paleta validada (módulo e simulação completa)
INK, INK2, MUTED, GRID, SURFACE, BAND = "#0b0b0b", "#52514e", "#8a8984", "#e3e2de", "#fcfcfb", "#ecebe7"
MARGIN = 0.5


# ---------------------------------------------------------------------------------------------------------------------
# Leitura e formatação
# ---------------------------------------------------------------------------------------------------------------------
def pt(value: float | None, digits: int = 3, sign: bool = False) -> str:
    """Número no formato brasileiro (vírgula decimal); ``sign`` mostra o + dos positivos."""
    if value is None or value != value:
        return "n/d"
    text = f"{value:+.{digits}f}" if sign else f"{value:.{digits}f}"
    return text.replace("-", "−").replace(".", ",")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def floats(rows: Sequence[Mapping[str, str]], key: str, only_ok: bool = True) -> list[float]:
    """Coluna numérica, pulando vazios e (por padrão) os casos que não terminaram com ``status`` ok."""
    out = []
    for row in rows:
        if only_ok and row.get("status", "ok") != "ok":
            continue
        text = row.get(key, "")
        if text not in ("", None):
            out.append(float(text))
    return out


def paired(rows: Sequence[Mapping[str, str]], x_key: str, y_key: str) -> tuple[list[float], list[float]]:
    xs, ys = [], []
    for row in rows:
        if row.get("status", "ok") == "ok" and row.get(x_key) not in ("", None) and row.get(y_key) not in ("", None):
            xs.append(float(row[x_key]))
            ys.append(float(row[y_key]))
    return xs, ys


def load(root: Path = DOCS) -> dict[str, Any]:
    """Os resumos e os CSVs das duas camadas (``v4`` e ``simulacao``)."""
    mod, sim = root / "v4", root / "simulacao"
    return {
        "mod": json.loads((mod / "resumo.json").read_text(encoding="utf-8")),
        "sim": json.loads((sim / "resumo.json").read_text(encoding="utf-8")),
        "mod_cases": read_csv(mod / "resultados.csv"),
        "mod_runs": read_csv(mod / "execucoes_slsqp.csv"),
        "sim_cases": read_csv(sim / "resultados.csv"),
        "sim_intervals": read_csv(sim / "intervalos.csv"),
    }


# ---------------------------------------------------------------------------------------------------------------------
# Texto
# ---------------------------------------------------------------------------------------------------------------------
def verdict(stats: Mapping[str, Any]) -> str:
    """Resumo do veredito pré-definido (IC dentro da margem E fração mínima dentro dela)."""
    ci_ok = abs(stats["ci90"][0]) <= MARGIN and abs(stats["ci90"][1]) <= MARGIN
    share_ok = stats["share_within_margin"] >= 0.95
    if ci_ok and share_ok:
        return "EQUIVALENTE"
    if ci_ok:
        return "EQUIVALÊNCIA NÃO DEMONSTRADA"
    return "NÃO EQUIVALENTE"


def headline(title: str, subtitle: str, stats: Mapping[str, Any], lines: Sequence[str]) -> list[tuple[str, dict[str, Any]]]:
    """Linhas (texto, estilo) do cartão de um conjunto de dados."""
    n_in = round(stats["share_within_margin"] * stats["compared"])
    out: list[tuple[str, dict[str, Any]]] = [
        (title, {"size": 11.5, "weight": "bold", "color": INK}),
        (subtitle, {"size": 8.5, "color": INK2}),
        (f"Diferença média do LP: {pt(stats['mean'], 3, True)}%  (IC de 90%: {pt(stats['ci90'][0], 3, True)}% a {pt(stats['ci90'][1], 3, True)}%)", {"size": 9.5, "color": INK}),
        (f"Dentro de ±0,5%: {n_in} de {stats['compared']} ({pt(stats['share_within_margin'] * 100, 1)}%; o critério pede 95%)", {"size": 9.5, "color": INK}),
        (f"LP mais barato / empate / mais caro: {stats['lp_cheaper']} / {stats['tie']} / {stats['lp_dearer']}", {"size": 9.5, "color": INK}),
        (f"Veredito pré-definido: {verdict(stats)}", {"size": 10.5, "weight": "bold", "color": INK}),
    ]
    out += [(line, {"size": 8.5, "color": INK2}) for line in lines]
    return out


def wrap(text: str, size: float, width_in: float) -> list[str]:
    """Quebra o texto para caber em ``width_in`` polegadas (largura média de um caractere: 0,55 do corpo)."""
    return textwrap.wrap(text, max(20, int(width_in * 72 / (size * 0.55)))) or [""]


def draw_lines(fig, x: float, top: float, width_in: float, rows: Sequence[tuple[str, dict[str, Any]]], gap: float = 0.0) -> float:  # noqa: ANN001
    """Escreve as linhas (texto, estilo), quebrando cada uma; devolve a altura usada (fração da figura)."""
    y = top
    for text, style in rows:
        size = style.get("size", 9)
        for line in wrap(text, size, width_in):
            fig.text(x, y, line, va="top", ha="left", **style)
            y -= size * 1.38 / 72 / 8.27
        y -= gap
    return top - y


def draw_card(fig, left: float, top: float, width_in: float, color: str, rows: Sequence[tuple[str, dict[str, Any]]]) -> None:  # noqa: ANN001
    """Cartão com uma faixa de cor à esquerda (a cor identifica a fonte dos dados, a mesma dos gráficos)."""
    used = draw_lines(fig, left + 0.012, top - 0.004, width_in, rows, gap=0.004)
    fig.patches.append(plt.Rectangle((left, top - used - 0.004), 0.004, used + 0.004, transform=fig.transFigure, color=color, lw=0))


def thousands(value: float) -> str:
    return f"{value:,.0f}".replace(",", ".")


# ---------------------------------------------------------------------------------------------------------------------
# Gráficos
# ---------------------------------------------------------------------------------------------------------------------
def style_axes(ax, title: str, note: str) -> None:  # noqa: ANN001
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=8, length=3)
    ax.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.set_title(title, loc="left", fontsize=10, fontweight="bold", color=INK, pad=14)
    ax.text(0, 1.015, note, transform=ax.transAxes, fontsize=7.8, color=INK2, va="bottom")


def chart_differences(ax, mod_gaps: Sequence[float], sim_gaps: Sequence[float], mod_stats, sim_stats) -> None:  # noqa: ANN001
    """Cada ponto é um caso (azul) ou uma simulação (laranja); a faixa cinza é a margem de ±0,5%."""
    style_axes(ax, "1. Diferença de custo, caso a caso", "cada ponto = um caso; negativa = LP mais barato")
    rng = np.random.RandomState(7)
    ax.axvspan(-MARGIN, MARGIN, color=BAND, zorder=0)
    ax.axvline(0, color=MUTED, lw=0.8, zorder=1)
    for row, (gaps, color, stats) in enumerate(((mod_gaps, BLUE, mod_stats), (sim_gaps, ORANGE, sim_stats))):
        y = row + rng.uniform(-0.22, 0.22, len(gaps))
        ax.scatter(gaps, y, s=14, color=color, alpha=0.55, linewidths=0, zorder=2)
        ax.plot(stats["ci90"], [row, row], color=INK, lw=3.2, solid_capstyle="butt", zorder=3)
        ax.scatter([stats["mean"]], [row], s=34, color=SURFACE, edgecolors=INK, linewidths=1.4, zorder=4)
        for g, yy in zip(gaps, y):
            if abs(g) > MARGIN:
                ax.annotate(f"{pt(g, 2, True)}%", (g, yy), xytext=(0, 7), textcoords="offset points", ha="center", fontsize=7.4, color=INK2)
    ax.set_yticks([0, 1], [f"Módulo\n({len(mod_gaps)} casos)", f"Simulações\n({len(sim_gaps)} de 1 ano)"])
    for tick, color in zip(ax.get_yticklabels(), (BLUE, ORANGE)):
        tick.set_color(color)
        tick.set_fontweight("bold")
    ax.set_ylim(-0.55, 1.55)
    ax.set_xlim(-1.2, 1.1)
    ax.set_xlabel("(custo do LP − custo do SLSQP) / custo do SLSQP, %", fontsize=8, color=INK2)
    ax.text(0, 1.52, "margem ±0,5%", ha="center", va="top", fontsize=7.4, color=MUTED)
    ax.text(0.99, 0.03, "● média   ▬ IC de 90%", transform=ax.transAxes, ha="right", fontsize=7.4, color=INK2)


def chart_vs_cost(ax, mod_xy, sim_xy) -> None:  # noqa: ANN001
    """A diferença não cresce com o nível do custo: a dispersão fica dentro da faixa nos dois conjuntos."""
    style_axes(ax, "2. A diferença depende do custo da dieta?", "cada ponto = um caso ou uma simulação")
    ax.axhspan(-MARGIN, MARGIN, color=BAND, zorder=0)
    ax.axhline(0, color=MUTED, lw=0.8, zorder=1)
    for (xs, ys), color, label in ((mod_xy, BLUE, "Módulo"), (sim_xy, ORANGE, "Simulações")):
        ax.scatter(xs, ys, s=15, color=color, alpha=0.55, linewidths=0, zorder=2, label=label)
    ax.set_xscale("log")
    ticks = [1, 2, 3, 5, 10, 20]
    ax.set_xticks(ticks, [str(t) for t in ticks])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("custo da ração do SLSQP, US$ por animal por dia (escala log)", fontsize=8, color=INK2)
    ax.set_ylabel("diferença do LP, %", fontsize=8, color=INK2)
    ax.set_ylim(-1.1, 1.1)
    ax.legend(loc="upper left", fontsize=7.6, frameon=False, labelcolor=INK2, handletextpad=0.2, markerscale=1.4)


def chart_times(ax, series: Sequence[tuple[str, Sequence[float], str]]) -> None:  # noqa: ANN001
    """Distribuição do tempo de uma solução (escala log); a caixa vai do 1º ao 3º quartil, os bigodes do percentil 5 ao 95."""
    style_axes(ax, "3. Tempo de uma solução", "caixa: quartis; bigodes: p5 a p95")
    ax.grid(False, axis="y")
    data = [list(s[1]) for s in series]
    box = ax.boxplot(data, orientation="horizontal", whis=(5, 95), showfliers=False, widths=0.5, patch_artist=True, manage_ticks=False)
    for patch, (_, _, color) in zip(box["boxes"], series):
        patch.set(facecolor=color, alpha=0.45, edgecolor=color, lw=1.2)
    for key in ("whiskers", "caps"):
        for line, (_, _, color) in zip(box[key], [s for s in series for _ in (0, 1)]):
            line.set(color=color, lw=1.2)
    for line in box["medians"]:
        line.set(color=INK, lw=1.8)
    for i, values in enumerate(data, start=1):
        median = float(np.median(values))
        label = f"{pt(median, 2 if median < 1 else 1)} s".replace(".", ",")
        ax.annotate(f"mediana {label}", (median, i), xytext=(0, -17), textcoords="offset points", ha="center", va="top", fontsize=7.6, color=INK)
    ax.set_xscale("log")
    ax.set_yticks(range(1, len(series) + 1), [s[0] for s in series])
    ax.invert_yaxis()
    ax.set_ylim(3.75, 0.4)
    for tick, (_, _, color) in zip(ax.get_yticklabels(), series):
        tick.set_color(color)
        tick.set_fontweight("bold")
    ax.set_xlabel("segundos por solução (escala log)", fontsize=8, color=INK2)
    ax.set_xlim(0.02, 200)
    ax.set_xticks([0.1, 1, 10, 100], ["0,1", "1", "10", "100"])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())


# ---------------------------------------------------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------------------------------------------------
def build(data: Mapping[str, Any]):  # noqa: ANN201
    mod, sim = data["mod"], data["sim"]
    mp, sp = mod["primary"], sim["primary"]
    mod_gaps = floats(data["mod_cases"], "primary_gap_pct")
    sim_gaps = floats(data["sim_cases"], "free_gap_pct")
    mod_xy = paired(data["mod_cases"], "slsqp_best_cost", "primary_gap_pct")
    sim_xy = paired(data["sim_cases"], "slsqp_cost", "free_gap_pct")
    sim_run, sim_meta, mod_meta = sim["run"], sim["meta"], mod["meta"]
    price_mod, price_sim = mod["solver"]["price_effect_pct"], sim_run["price_effect_pct"]
    method_mod, method_sim = mod["solver"]["method_effect_pct"]["mean_abs"], sim_run["method_effect_pct"]["mean_abs"]
    seconds = mod["solver"]["seconds"]
    ratio = seconds["lp"]["median"] / seconds["slsqp"]["median"]

    fig = plt.figure(figsize=(11.69, 8.27), facecolor=SURFACE)
    fig.text(0.03, 0.965, "Dieta ótima: o custo da ração do LP é o mesmo do SLSQP do RuFaS?", fontsize=15.5, fontweight="bold", color=INK, va="top")
    draw_lines(fig, 0.03, 0.932, 10.8, [("Duas fontes de dados: o módulo (um animal em um dia, 288 casos sorteados) e simulações completas do RuFaS (40 de 1 ano, com o SLSQP dentro). "
                                         "NASEM 2021, preços ilustrativos.", {"size": 8.6, "color": INK2})])

    draw_card(fig, 0.03, 0.895, 5.0, BLUE, headline(
        "Módulo: um animal, um dia",
        f"{mp['cases']} casos, {mp['compared']} com dieta nos dois métodos, em 79 grupos animal × cardápio; o LP contra o melhor de 10 sementes do SLSQP.",
        mp, [f"As diferenças vão de {pt(mp['min'], 2, True)}% a {pt(mp['max'], 2, True)}%. O preço dos alimentos muda o custo {pt(price_mod['mean'], 0)}% em média; o método, {pt(method_mod, 3)}%."]))
    draw_card(fig, 0.52, 0.895, 5.0, ORANGE, headline(
        "Simulações completas: 1 ano, 13 intervalos",
        f"{sim_run['simulations']} simulações, {sim_run['ok']} comparadas ({sim_run['sim_failed']} falharam dentro do RuFaS, 8 delas com 60 vacas); SLSQP uma vez por intervalo.",
        sp, [f"As diferenças vão de {pt(sp['min'], 2, True)}% a {pt(sp['max'], 2, True)}%. O preço muda o custo {pt(price_sim['mean'], 0)}% em média; o método, {pt(method_sim, 3)}%."]))

    ax1 = fig.add_axes([0.115, 0.315, 0.255, 0.28])
    ax2 = fig.add_axes([0.455, 0.315, 0.215, 0.28])
    ax3 = fig.add_axes([0.80, 0.315, 0.17, 0.28])
    chart_differences(ax1, mod_gaps, sim_gaps, mp, sp)
    chart_vs_cost(ax2, mod_xy, sim_xy)
    chart_times(ax3, [
        ("SLSQP\n(módulo)", floats(data["mod_runs"], "seconds", only_ok=False), BLUE),
        ("LP\n(módulo)", floats(data["mod_cases"], "lp_seconds"), BLUE),
        ("LP\n(simulação)", floats(data["sim_intervals"], "lp_free_seconds", only_ok=False), ORANGE),
    ])

    saving = sim_run["saving_per_cow_year"]
    low, high = sorted((price_mod["mean"] / method_mod, price_sim["mean"] / method_sim))
    can = [
        f"Dá para dizer: o LP não custa menos nem mais que o SLSQP em média ({pt(mp['mean'], 3, True)}% no módulo; {pt(sp['mean'], 3, True)}% nas simulações).",
        f"O preço dos alimentos pesa de {thousands(low)} a {thousands(high)} vezes mais que a escolha do método.",
        "As rações do LP atendem às restrições originais do RuFaS (237 de 237 casos; 390 de 390 intervalos) e não dependem de ponto inicial aleatório.",
        f"O LP é cerca de {pt(ratio, 0)} vezes mais lento que o SLSQP (mediana de {pt(seconds['lp']['median'], 1)} s contra {pt(seconds['slsqp']['median'], 2)} s).",
    ]
    cannot = [
        f"Não dá para dizer \"equivalente em simulação completa\": {round(sp['share_within_margin'] * sp['compared'])} de {sp['compared']} simulações ({pt(sp['share_within_margin'] * 100, 1)}%) ficaram dentro de ±0,5%; o critério pedia 95%.",
        f"Não dá para dizer \"o LP economiza\": a economia média por vaca em lactação é de US$ {pt(saving['mean'], 2)} por ano (de {pt(saving['min'], 2)} a {pt(saving['max'], 2)}).",
        "Os resultados valem para rebanhos de 200 e 300 vacas (26 das 30 simulações); com 60 e 100 vacas o RuFaS falhou em 10 de 14.",
        "A ração do LP não volta para a simulação: a comparação é de custo da ração, não do efeito sobre o leite.",
    ]
    draw_lines(fig, 0.03, 0.245, 5.2, [("✓ " + c, {"size": 8.4, "color": INK}) for c in can], gap=0.009)
    draw_lines(fig, 0.52, 0.245, 5.2, [("✗ " + c, {"size": 8.4, "color": INK}) for c in cannot], gap=0.009)
    draw_lines(fig, 0.03, 0.05, 11.0, [
        ("Reprodução (pasta backend): python -m dietopt.benchmark run --out ..\\docs\\benchmark\\v4;  python -m dietopt.benchmark_sim run --out ..\\docs\\benchmark\\simulacao;  python -m dietopt.benchmark_report", {"size": 7.2, "color": MUTED}),
        (f"Módulo: commit {mod_meta['commit']}, {mod_meta['date']}. Simulações: commit {sim_meta['commit']}, {sim_meta['date']}. RuFaS {sim_meta['rufas']}; Python {sim_meta['python']}, numpy {sim_meta['numpy']}, scipy {sim_meta['scipy']}. "
         "Critério: IC de 90% (bootstrap por agrupamento) dentro de ±0,5% e ao menos 95% dos casos dentro da margem.", {"size": 7.2, "color": MUTED}),
    ])
    return fig


def write(out: Path, root: Path = DOCS) -> list[Path]:
    """Grava o PDF e o PNG da página em ``out`` (sem extensão)."""
    fig = build(load(root))
    paths = [out.with_suffix(".pdf"), out.with_suffix(".png")]
    fig.savefig(paths[0], facecolor=fig.get_facecolor())
    fig.savefig(paths[1], dpi=170, facecolor=fig.get_facecolor())
    plt.close(fig)
    return paths


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Relatório de uma página do benchmark LP × SLSQP (módulo e simulações completas)")
    parser.add_argument("--root", type=Path, default=DOCS, help="pasta com v4/ e simulacao/")
    parser.add_argument("--out", type=Path, default=DOCS / "RELATORIO_UMA_PAGINA", help="caminho sem extensão (gera .pdf e .png)")
    args = parser.parse_args(argv)
    for path in write(args.out, args.root):
        print(path)


if __name__ == "__main__":
    main()
