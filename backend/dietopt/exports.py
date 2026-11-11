"""Exportação de tabelas (CSV) e relatórios (HTML autônomo, imprimível) dos resultados (RF-20).

Todas as funções recebem o mesmo JSON que a interface já tem na tela (resultado da simulação, da sensibilidade, do módulo
ampliado) e devolvem texto; não recalculam nada. O CSV usa vírgula como separador e ponto decimal; o relatório mostra
números no formato brasileiro e escapa todo texto vindo do usuário.
"""

from __future__ import annotations

import csv
import io
from datetime import datetime
from html import escape
from typing import Any, Callable, Mapping, Sequence

DMI_KEY = "dry_matter_intake_total"
STATUS_TEXT = {"ok": "Ok", "warn": "Atenção", "alert": "Alerta", "deficit": "Déficit", "fora": "Fora da faixa"}
SITUATION = {"ok": "Atende", "no_limite": "No limite", "violada": "Violada", "indisponivel": "Indisponível"}


# ---------------------------------------------------------------------------------------------------------------
# Formatação
# ---------------------------------------------------------------------------------------------------------------
def _cell(value: Any) -> str:
    """Valor de uma célula de CSV: números com até 6 algarismos significativos; ``None`` vira vazio."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "sim" if value else "não"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def _csv(header: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(header)
    for row in rows:
        writer.writerow([_cell(value) for value in row])
    return out.getvalue()


def _br(value: Any, digits: int = 2) -> str:
    """Número no formato brasileiro (``1.234,56``); ``—`` quando não há valor."""
    if value is None or (isinstance(value, float) and value != value):
        return "—"
    text = f"{value:,.{digits}f}"
    return text.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def _usd(value: Any, digits: int = 2) -> str:
    return "—" if value is None else f"US$ {_br(value, digits)}"


# ---------------------------------------------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------------------------------------------
def simulation_csv(sim: Mapping[str, Any], meta: Mapping[str, Any] | None = None) -> str:
    """Ração média da simulação: kg de MS por vaca e por dia, participação, preço e custo de cada alimento."""
    prices = {str(f["id"]): f.get("price") for f in sim["feeds"]}
    labels = {str(f["id"]): f["label"] for f in sim["feeds"]}
    ration = {k: float(v) for k, v in sim["average_ration"].items() if k != DMI_KEY and float(v) > 1e-6}
    total = sum(ration.values())
    rows = []
    for feed_id, kg in sorted(ration.items(), key=lambda item: -item[1]):
        price = prices.get(feed_id)
        rows.append([feed_id, labels.get(feed_id, feed_id), kg, kg / total * 100 if total else None, price, kg * price if price is not None else None])
    cost = sum(row[5] for row in rows if row[5] is not None)
    rows.append(["", "TOTAL", total, 100.0 if total else None, "", cost])
    return _csv(["id", "alimento", "kg_ms_vaca_dia", "pct_da_dieta", "preco_usd_kg_ms", "custo_usd_vaca_dia"], rows)


def sensitivity_csv(result: Mapping[str, Any], meta: Mapping[str, Any] | None = None) -> str:
    """Tabela de cenários da sensibilidade: fatores, margem (``Res``), indicadores e a ração de cada cenário."""
    factors = [c for c in result["columns"] if c != "Res"]
    feeds = [(str(f["id"]), f["label"]) for f in result["feeds"]]
    header = ["cenario", *factors, "Res", "leite_kg", "receita", "custo_alimentacao", "custo_vaca_dia", "reducao_leite", *(f"kg_ms: {label}" for _, label in feeds), "erro"]
    rows = []
    for row in result["rows"]:
        ration = row.get("ration") or {}
        rows.append(
            [
                row["cenario"], *(row.get(f) for f in factors), row.get("Res"), row.get("leite_kg"), row.get("receita"),
                row.get("custo_alimentacao"), row.get("custo_vaca_dia"), row.get("reducao_leite"),
                *(ration.get(feed_id) for feed_id, _ in feeds), row.get("erro", ""),
            ]
        )  # fmt: skip
    return _csv(header, rows)


def module_csv(evaluation: Mapping[str, Any], meta: Mapping[str, Any] | None = None) -> str:
    """Avaliação das dietas: uma linha por dieta e restrição, com a posição no ranking (1 = mais recomendada)."""
    position = {name: len(evaluation["ranking"]) - index for index, name in enumerate(evaluation["ranking"])}
    rows = []
    for diet in sorted(evaluation["diets"], key=lambda d: position[d["name"]]):
        for c in diet["constraints"]:
            rows.append(
                [
                    position[diet["name"]], diet["name"], diet["cost"], diet["feasible"], diet["violation"], c["id"], c["label"], c["unit"], c["kind"],
                    c["sense"], c["requirement"], c.get("supply_linear"), c.get("supply_nonlinear"), c.get("error_pct"), c.get("slack"),
                    SITUATION.get(c["status"], c["status"]),
                ]
            )  # fmt: skip
    header = ["posicao", "dieta", "custo_usd_dia", "viavel", "violacao", "restricao_id", "restricao", "unidade", "classe", "sentido", "exigencia", "oferta_linear", "oferta_rufas", "erro_pct", "folga", "estado"]
    return _csv(header, rows)


# ---------------------------------------------------------------------------------------------------------------
# Relatório HTML
# ---------------------------------------------------------------------------------------------------------------
CSS = """
:root{color-scheme:light}body{font:14px/1.5 system-ui,Segoe UI,Arial,sans-serif;color:#1d2530;margin:2rem auto;max-width:60rem;padding:0 1rem}
h1{font-size:1.6rem;margin:.2rem 0}h2{font-size:1.1rem;margin:1.8rem 0 .5rem;border-bottom:1px solid #ccd3dc;padding-bottom:.2rem}
.sub{color:#5b6573;margin:0 0 1rem}.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));gap:.6rem}
.kpi{border:1px solid #ccd3dc;border-radius:.5rem;padding:.5rem .7rem}.kpi b{display:block;font-size:1.15rem}.kpi span{color:#5b6573;font-size:.8rem}
table{border-collapse:collapse;width:100%;margin:.4rem 0}th,td{border-bottom:1px solid #e2e6eb;padding:.3rem .5rem;text-align:left;vertical-align:top}
th{background:#f3f5f8;font-weight:600}td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}.note{background:#fff8e6;border:1px solid #ecd9a0;border-radius:.4rem;padding:.5rem .7rem;white-space:pre-wrap}
.muted{color:#5b6573;font-size:.85rem}footer{margin-top:2rem;color:#5b6573;font-size:.8rem}@media print{body{margin:0;max-width:none}h2{break-after:avoid}table,.kpi{break-inside:avoid}}
"""  # fmt: skip


def _table(header: Sequence[str], rows: Sequence[Sequence[Any]], numeric: Sequence[int] = ()) -> str:
    head = "".join(f'<th class="{"n" if i in numeric else ""}">{escape(str(h))}</th>' for i, h in enumerate(header))
    body = "".join("<tr>" + "".join(f'<td class="{"n" if i in numeric else ""}">{escape(str(c))}</td>' for i, c in enumerate(row)) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _kpis(items: Sequence[tuple[str, str]]) -> str:
    return '<div class="kpis">' + "".join(f'<div class="kpi"><b>{escape(value)}</b><span>{escape(label)}</span></div>' for label, value in items) + "</div>"


def _page(title: str, subtitle: str, sections: Sequence[str], meta: Mapping[str, Any], now: datetime | None = None) -> str:
    note = str(meta.get("note") or "").strip()
    stamp = (now or datetime.now()).strftime("%d/%m/%Y %H:%M")
    notes = f'<h2>Observações</h2><p class="note">{escape(note)}</p>' if note else ""
    return (
        f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{escape(title)}</title><style>{CSS}</style></head><body><h1>{escape(title)}</h1><p class=\"sub\">{escape(subtitle)}</p>"
        f'{"".join(sections)}{notes}<footer>Gerado em {stamp} por Dieta Ótima com RuFaS. Preços em US$ por kg de matéria seca, como informados na tela; '
        f"os resultados dependem deles e dos limites escolhidos.</footer></body></html>"
    )


def _checks_section(checks: Sequence[Mapping[str, Any]]) -> list[str]:
    if not checks:
        return []
    rows = [[STATUS_TEXT.get(c["status"], c["status"]), f"{c['id']} {c['label']}", c["value"], c["limit"]] for c in checks]
    return ["<h2>Verificações de consistência</h2>", _table(["Estado", "Verificação", "Valor obtido", "Limite"], rows)]


def _balance_section(balance: Sequence[Mapping[str, Any]]) -> list[str]:
    if not balance:
        return []
    rows = [
        [b["label"], b["unit"], _br(b.get("requirement")), _br(b.get("supply")), _br(b["difference"]), _br(b["worst_difference"]), STATUS_TEXT.get(b["status"], b["status"])]
        for b in balance
    ]  # fmt: skip
    return [
        "<h2>Balanço nutricional</h2>",
        _table(["Nutriente", "Unidade", "Exigência", "Oferta", "Diferença (média)", "Pior intervalo", "Estado"], rows, numeric=(2, 3, 4, 5)),
        '<p class="muted">Calculado pelo próprio RuFaS a cada intervalo de 30 dias. Positivo = sobra; negativo = falta.</p>',
    ]


def simulation_report(sim: Mapping[str, Any], meta: Mapping[str, Any] | None = None, now: datetime | None = None) -> str:
    meta = meta or {}
    s = sim["summary"]
    limits = sim.get("limits") or meta.get("limits") or {}
    labels = {str(f["id"]): f["label"] for f in sim["feeds"]}
    prices = {str(f["id"]): f.get("price") for f in sim["feeds"]}
    ration = {k: float(v) for k, v in sim["average_ration"].items() if k != DMI_KEY and float(v) > 1e-6}
    total = sum(ration.values())
    rows = []
    for feed_id, kg in sorted(ration.items(), key=lambda item: -item[1]):
        low, high = limits.get(feed_id) or (None, None)
        rows.append([labels.get(feed_id, feed_id), _br(prices.get(feed_id), 3), _br(low), _br(high), _br(kg), f"{_br(kg / total * 100 if total else None, 1)}%"])
    sections = [
        "<h2>Indicadores</h2>",
        _kpis(
            [
                ("Margem sobre custo de alimentação", _usd(s.get("margem"), 0)), ("Receita do leite", _usd(s.get("receita"), 0)),
                ("Custo de alimentação (rebanho)", _usd(s.get("custo_alimentacao"), 0)), ("Custo da ração, vaca em lactação", f"{_usd(s.get('custo_vaca_dia'))}/dia"),
                ("Leite total", f"{_br((s.get('leite_kg') or 0) / 1000, 0)} t"), ("Preço do leite", f"{_usd(s.get('milk_price'), 3)}/kg"),
                ("Vacas no rebanho", _br(s.get("cow_num", 100), 0)),
                ("Leite perdido por ração insuficiente", f"{_br(s.get('reducao_leite'))} kg/vaca/dia"),
            ]
        ),  # fmt: skip
        "<h2>Ração média e preços</h2>",
        _table(["Alimento", "Preço (US$/kg MS)", "Mín. (kg/dia)", "Máx. (kg/dia)", "kg MS/vaca/dia", "% da dieta"], rows, numeric=(1, 2, 3, 4, 5)),
        *_checks_section(sim.get("checks") or []),
        *_balance_section(sim.get("balance") or []),
    ]
    return _page("Relatório da simulação do RuFaS", f"Cenário {s.get('cenario', '')} · {meta.get('standard', 'NRC 2001')}", sections, meta, now)


def sensitivity_report(result: Mapping[str, Any], meta: Mapping[str, Any] | None = None, now: datetime | None = None) -> str:
    meta = meta or {}
    factors = [c for c in result["columns"] if c != "Res"]
    valid = [r for r in result["rows"] if r.get("Res") is not None]
    labels = {str(f["id"]): f["label"] for f in result["feeds"]}
    sections: list[str] = []
    if valid:
        best, worst = max(valid, key=lambda r: r["Res"]), min(valid, key=lambda r: r["Res"])
        ration = ", ".join(f"{labels.get(k, k)} {_br(v, 1)} kg" for k, v in sorted((best.get("ration") or {}).items(), key=lambda kv: -kv[1])[:5])
        sections += [
            "<h2>Resumo</h2>",
            _kpis(
                [
                    ("Cenários", f"{len(result['rows'])} ({len(valid)} com resultado)"), (f"Melhor margem: {best['cenario']}", _usd(best["Res"], 0)),
                    (f"Pior margem: {worst['cenario']}", _usd(worst["Res"], 0)), ("Diferença entre o melhor e o pior", _usd(best["Res"] - worst["Res"], 0)),
                ]
            ),  # fmt: skip
            f"<p>No melhor cenário ({escape(best['cenario'])}), a ração é: {escape(ration) if ration else '—'}.</p>",
        ]
    rows = [
        [r["cenario"], *(_br(r.get(f), 3) for f in factors), "falhou" if r.get("Res") is None else _usd(r["Res"], 0), _br(r.get("custo_vaca_dia")), _br(r.get("reducao_leite")) if (r.get("reducao_leite") or 0) > 0.005 else "—"]
        for r in result["rows"]
    ]  # fmt: skip
    sections += [
        "<h2>Tabela de cenários</h2>",
        _table(["Cenário", *factors, "Res (margem)", "US$/vaca/dia", "Leite perdido"], rows, numeric=tuple(range(1, len(factors) + 4))),
    ]
    effects = [(e["fator"], _br(e["spearman"])) for e in result.get("effects", []) if e.get("spearman") is not None]
    if effects:
        sections += ["<h2>Efeito de cada fator sobre a margem</h2>", _table(["Fator", "Correlação de Spearman"], effects, numeric=(1,))]
    return _page("Relatório da análise de sensibilidade", f"{len(result['rows'])} cenários · {meta.get('standard', 'NRC 2001')}", sections, meta, now)


def module_report(evaluation: Mapping[str, Any], meta: Mapping[str, Any] | None = None, now: datetime | None = None) -> str:
    meta = meta or {}
    optimal = meta.get("optimal") or None
    names = {str(k): v for k, v in (meta.get("feed_names") or {}).items()}
    ranking = list(reversed(evaluation["ranking"]))
    diets = {d["name"]: d for d in evaluation["diets"]}
    optimal_cost = optimal["diet"]["cost"] if optimal and optimal.get("diet") else None
    rows = []
    for index, name in enumerate(ranking, 1):
        d = diets[name]
        state = "Inviável" if not d["feasible"] else "Viável, incompleta" if d.get("incomplete") else "Viável"
        deviation = "" if optimal_cost is None else f"{(d['cost'] - optimal_cost) / optimal_cost * 100:+.1f}%".replace(".", ",")
        violated = ", ".join(c["label"] for c in d["constraints"] if c["status"] == "violada")
        row = [f"{index}º", name, state, _usd(d["cost"]), _br(d["violation"], 3) if d["violation"] > 0 else "—"]
        rows.append(row + ([deviation] if optimal_cost is not None else []) + [violated])
    head = ["Posição", "Dieta", "Estado", "Custo (US$/dia)", "Violação", *(["Desvio do ótimo"] if optimal_cost is not None else []), "Restrições violadas"]
    best = evaluation.get("best")
    sections = [
        "<h2>Ranking das dietas informadas</h2>",
        _table(head, rows, numeric=(3, 4)),
        f"<p>Melhor entre as informadas: <b>{escape(best)}</b>. Não é a dieta ótima.</p>" if best else "<p>Nenhuma das dietas informadas atende a todas as restrições.</p>",
    ]
    if optimal and optimal.get("status") == "ok" and optimal.get("diet"):
        diet = optimal["diet"]
        amount_rows = [[names.get(k, k), _br(v)] for k, v in sorted(diet["amounts"].items(), key=lambda kv: -kv[1])]
        sections += [
            "<h2>Dieta ótima (linear)</h2>",
            _kpis([("Custo", f"{_usd(diet['cost'])}/dia"), ("Consumo de MS", f"{_br(diet['scalars']['dmi'])} kg/dia"), ("TDN%", f"{_br(diet['scalars']['tdn_percentage'], 1)}%"), ("Concentrado", f"{_br(diet['scalars']['concentrate_percentage'], 1)}%")]),
            _table(["Alimento", "kg MS/dia"], amount_rows, numeric=(1,)),
            f'<p class="muted">{"Confere com as restrições originais do RuFaS." if diet.get("verified") else "Atenção: viola alguma restrição original do RuFaS."}</p>',
        ]
        rufas = optimal.get("rufas")
        if rufas and rufas.get("cost_min") is not None:
            sections += [
                "<h2>Comparação com o otimizador do RuFaS</h2>",
                _table(["Medida", "Valor"], [["Custo do LP em relação ao melhor do RuFaS", f"{rufas['lp_gap_pct']:+.3f}%".replace(".", ",")], ["Melhor do RuFaS", _usd(rufas["cost_min"], 4)], ["Mediana do RuFaS", _usd(rufas["cost_median"], 4)], ["Execuções viáveis", f"{rufas['n_success']} de {rufas['n_runs']}"]]),
            ]
    sub = f"{meta.get('standard', evaluation.get('standard', ''))} · {evaluation.get('category', '')}"
    return _page("Relatório da avaliação de dietas", sub, sections, meta, now)


# ---------------------------------------------------------------------------------------------------------------
# Despacho
# ---------------------------------------------------------------------------------------------------------------
BUILDERS: Mapping[tuple[str, str], tuple[Callable[..., str], str, str, str]] = {
    ("csv", "simulation"): (simulation_csv, "racao-media.csv", "text/csv;charset=utf-8", "﻿"),
    ("csv", "sensitivity"): (sensitivity_csv, "cenarios-sensibilidade.csv", "text/csv;charset=utf-8", "﻿"),
    ("csv", "module"): (module_csv, "avaliacao-de-dietas.csv", "text/csv;charset=utf-8", "﻿"),
    ("report", "simulation"): (simulation_report, "relatorio-simulacao.html", "text/html;charset=utf-8", ""),
    ("report", "sensitivity"): (sensitivity_report, "relatorio-sensibilidade.html", "text/html;charset=utf-8", ""),
    ("report", "module"): (module_report, "relatorio-avaliacao-de-dietas.html", "text/html;charset=utf-8", ""),
}  # fmt: skip


def export_file(fmt: str, screen: str, data: Mapping[str, Any], meta: Mapping[str, Any] | None = None) -> dict[str, str]:
    """Arquivo pedido (``fmt``: ``csv`` ou ``report``; ``screen``: simulation, sensitivity ou module)."""
    try:
        build, filename, mime, prefix = BUILDERS[(fmt, screen)]
    except KeyError:
        raise ValueError(f"Exportação desconhecida: {fmt}/{screen}") from None
    if not isinstance(data, Mapping) or not data:
        raise ValueError("Não há resultado para exportar")
    try:
        content = build(data, meta or {})
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Resultado incompleto para exportar ({type(exc).__name__}: {exc})") from None
    return {"filename": filename, "mime": mime, "content": prefix + content}
