"""Benchmark de simulações completas (``dietopt.benchmark_sim``): desenho determinístico e estatística; sem rodar o RuFaS."""

import csv
import json

import pytest

from dietopt import benchmark_sim as bs


def interval(slsqp=3.0, free=3.0, same=3.0, reduction=0.0, days=28):
    out = {"day": 0, "days": days, "cows": 80, "reduction": reduction, "slsqp": {"cost": slsqp, "dmi": 25.0}}
    out["lp_free"] = None if free is None else {"cost": free, "dmi": 25.0, "verified": True, "seconds": 5.0}
    out["lp_same"] = None if same is None else {"cost": same, "dmi": 25.0, "verified": True, "seconds": 4.0}
    return out


def sim(menu="m00", k=0, slsqp=3.0, free=3.0, same=None, status="ok", reduction=0.0, cows=100, intervals=None):
    """Registro sintético de uma simulação (o mesmo formato que ``run_sim`` grava)."""
    record = {"id": f"{menu}/p{k}", "menu": menu, "price_set": k, "cows": cows, "rufas_seed": 1, "seed": 1, "feeds": [1, 2], "resolution": "normal", "status": status}
    if status != "ok":
        return record | {"detail": "falhou"}
    same = free if same is None else same
    return record | {
        "sim_seconds": 40.0, "compare_seconds": 120.0, "milk_kg": 1e6, "reduction_mean": reduction,
        "intervals": intervals or [interval(slsqp, free, same, reduction) for _ in range(13)],
        "summary": {
            "intervals_used": 13, "days": 364, "slsqp_cost_per_cow_day": slsqp, "mean_cows": 80.0,
            "lp_free": {"cost_per_cow_day": free, "saving_pct": (slsqp - free) / slsqp * 100, "herd_saving": (slsqp - free) * 80 * 364, "all_verified": True},
            "lp_same": {"cost_per_cow_day": same, "saving_pct": (slsqp - same) / slsqp * 100, "herd_saving": (slsqp - same) * 80 * 364, "all_verified": True},
        },
        "warnings": [],
    }  # fmt: skip


# ---------------------------------------------------------------------------------------------------------------------
# Desenho
# ---------------------------------------------------------------------------------------------------------------------
def test_simulacoes_sao_fixas_e_cobrem_cardapio_e_preco():
    a, b = bs.sims(), bs.sims()
    assert a == b
    assert len(a) == bs.MENUS * 2
    assert len({s["id"] for s in a}) == len(a)


def test_os_dois_conjuntos_de_precos_do_cardapio_compartilham_rebanho_e_semente_do_rufas():
    by_menu = {}
    for s in bs.sims():
        by_menu.setdefault(s["menu"], []).append(s)
    for pair in by_menu.values():
        assert len(pair) == 2
        assert pair[0]["cows"] == pair[1]["cows"] and pair[0]["rufas_seed"] == pair[1]["rufas_seed"]
        assert set(pair[0]["prices"]) == set(pair[1]["prices"])
        assert pair[0]["prices"] != pair[1]["prices"]  # só o preço muda


def test_rebanhos_ficam_na_faixa_verificada_e_variam():
    cows = {s["cows"] for s in bs.sims()}
    assert cows <= set(bs.HERD_SIZES) and all(60 <= c <= 500 for c in cows) and len(cows) > 1


def test_outra_semente_gera_outras_simulacoes_e_a_mesma_repete():
    assert bs.sims(1) == bs.sims(1)
    assert [s["prices"] for s in bs.sims(1)] != [s["prices"] for s in bs.sims(2)]


def test_cenario_usa_nasem_o_tetos_padrao_e_o_rebanho_sorteado():
    spec = bs.sims()[0]
    scenario, economics = bs._scenario(spec)
    assert scenario.nutrient_standard == "NASEM" and scenario.end_date == "2013:365"
    assert scenario.cow_num == (None if spec["cows"] == 100 else spec["cows"])
    assert scenario.lac_cow_feeds == sorted(int(i) for i in spec["prices"])
    assert all(low == 0.0 and high > 0 for low, high in scenario.feed_limits.values())
    assert all(economics.prices[int(i)] == p for i, p in spec["prices"].items())  # os preços do sorteio valem sobre os padrões


# ---------------------------------------------------------------------------------------------------------------------
# Estatística
# ---------------------------------------------------------------------------------------------------------------------
def test_diferenca_da_simulacao_e_relativa_ao_slsqp_e_negativa_quando_o_lp_e_mais_barato():
    r = sim(slsqp=4.0, free=3.96, same=4.04)
    assert bs.free_gap(r) == pytest.approx(-1.0)
    assert bs.same_gap(r) == pytest.approx(1.0)
    assert bs.free_gap(sim(status="sim_failed")) is None
    assert bs.free_gap(sim(status="no_lp")) is None


def test_equivalente_quando_o_ic_cabe_na_margem_e_quase_todas_estao_dentro():
    rows = [sim(f"m{k:02d}", j, slsqp=3.0, free=3.0 * (1 + d / 100)) for k, d in enumerate([0.0, 0.05, -0.05, 0.09, -0.09, 0.0, 0.02, -0.02]) for j in range(2)]
    d = bs.describe(rows, bs.free_gap)
    assert d["compared"] == 16 and d["groups"] == 8
    assert d["equivalent"] and d["verdict"] == "equivalent"
    assert d["tie"] == 16 and d["lp_cheaper"] == 0 and d["lp_dearer"] == 0
    assert d["outliers"] == []


def test_lp_mais_barato_alem_da_margem_quando_o_ic_inteiro_fica_abaixo_dela():
    rows = [sim(f"m{k:02d}", j, slsqp=3.0, free=3.0 * (1 - (0.8 + 0.02 * k) / 100)) for k in range(8) for j in range(2)]
    d = bs.describe(rows, bs.free_gap)
    assert not d["equivalent"] and d["verdict"] == "lp_cheaper"
    assert d["lp_cheaper"] == 16 and len(d["outliers"]) == 16


def test_lp_mais_caro_alem_da_margem_e_inconclusivo_quando_o_ic_cruza_a_margem():
    dearer = bs.describe([sim(f"m{k:02d}", 0, slsqp=3.0, free=3.0 * 1.01) for k in range(6)], bs.free_gap)
    assert dearer["verdict"] == "lp_dearer"
    mixed = bs.describe([sim(f"m{k:02d}", 0, slsqp=3.0, free=3.0 * (1 + d / 100)) for k, d in enumerate([-2, 1.5, -1, 2, 0.8, -1.6])], bs.free_gap)
    assert mixed["verdict"] == "inconclusive"


def test_ic_nao_e_equivalente_quando_poucas_simulacoes_ficam_dentro_da_margem():
    # a média está na margem, mas 3 de 10 simulações passam dela: a fração mínima não é atendida
    deltas = [0.0] * 7 + [0.9, -0.9, 0.9]
    d = bs.describe([sim(f"m{k:02d}", 0, slsqp=3.0, free=3.0 * (1 + x / 100)) for k, x in enumerate(deltas)], bs.free_gap)
    assert d["share_within_margin"] == pytest.approx(0.7) and not d["equivalent"]


def test_intervalos_sao_so_descritos_e_contam_lados_e_alem_da_margem():
    ivs = [interval(3.0, 3.0), interval(3.0, 2.9), interval(3.0, 3.05), interval(3.0, None)]
    rows = [sim(intervals=ivs)]
    d = bs.describe_intervals(rows, "lp_free")
    assert d["intervals"] == 4 and d["compared"] == 3  # o intervalo sem ração no LP não entra
    assert (d["lp_cheaper"], d["tie"], d["lp_dearer"]) == (1, 1, 1)
    assert d["lp_cheaper_beyond_margin"] == 1 and d["lp_dearer_beyond_margin"] == 1


def test_run_stats_conta_falhas_verificacao_reducao_de_leite_e_peso_dos_precos():
    rows = [
        sim("m00", 0, slsqp=3.0, free=2.99), sim("m00", 1, slsqp=4.5, free=4.49, reduction=0.5),
        sim("m01", 0, status="sim_failed"), sim("m02", 0, status="no_lp"), sim("m03", 0, status="error"),
    ]  # fmt: skip
    s = bs.run_stats(rows)
    assert (s["simulations"], s["ok"], s["sim_failed"], s["no_lp"], s["errors"]) == (5, 2, 1, 1, 1)
    assert s["intervals"] == 26 and s["lp_free_verified"] == 26 and s["intervals_without_lp_free"] == 0
    assert s["sims_with_milk_reduction"] == 1 and s["intervals_with_milk_reduction"] == 13
    assert s["price_effect_pct"]["mean"] == pytest.approx(50.0)  # 3,0 contra 4,5 no mesmo cardápio
    assert s["method_effect_pct"]["max_abs"] < 1.0
    assert s["seconds"]["lp_per_interval"]["median"] == 5.0


def test_sensibilidade_sem_reducao_de_leite_e_por_tamanho_do_rebanho():
    rows = [sim("m00", 0, free=3.0, cows=60), sim("m01", 0, free=2.9, cows=100, reduction=1.0), sim("m02", 0, free=3.0, cows=100)]
    s = bs.summarize(rows)
    assert s["without_milk_reduction"]["compared"] == 2
    assert set(s["by_herd_size"]) == {"60", "100"} and s["by_herd_size"]["100"]["compared"] == 2
    assert [f["status"] for f in bs.summarize([*rows, sim("m03", 0, status="sim_failed")])["failed"]] == ["sim_failed"]


# ---------------------------------------------------------------------------------------------------------------------
# Relatório e arquivos
# ---------------------------------------------------------------------------------------------------------------------
def test_relatorio_traz_veredito_ressalva_da_ração_e_reproducao(tmp_path):
    rows = [sim(f"m{k:02d}", j, slsqp=3.0, free=3.0 * (1 - 0.003)) for k in range(6) for j in range(2)]
    (tmp_path / "resultados.jsonl").write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    bs.write_report(tmp_path)
    text = (tmp_path / "RELATORIO.txt").read_text(encoding="utf-8")
    assert "EQUIVALENTE" in text and "COMPARAÇÃO PRIMÁRIA" in text and "NÃO volta para a simulação" in text
    assert "benchmark_sim run" in text and "commit" in text
    assert "-0,000" not in text
    summary = json.loads((tmp_path / "resumo.json").read_text(encoding="utf-8"))
    assert summary["primary"]["equivalent"] and summary["meta"]["commit"]


def test_csvs_trazem_uma_linha_por_simulacao_e_por_intervalo(tmp_path):
    rows = [sim("m00", 0, slsqp=3.0, free=2.9), sim("m00", 1, status="sim_failed")]
    (tmp_path / "resultados.jsonl").write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    bs.write_csv(tmp_path, bs.load(tmp_path))
    sims_csv = list(csv.DictReader((tmp_path / "resultados.csv").open(encoding="utf-8")))
    assert [r["status"] for r in sims_csv] == ["ok", "sim_failed"]
    assert float(sims_csv[0]["free_gap_pct"]) == pytest.approx(-100 / 30) and sims_csv[1]["free_gap_pct"] == ""
    ivs_csv = list(csv.DictReader((tmp_path / "intervalos.csv").open(encoding="utf-8")))
    assert len(ivs_csv) == 13 and ivs_csv[0]["lp_free_verified"] == "True"


def test_carregar_ordena_pelo_desenho_e_ignora_arquivo_ausente(tmp_path):
    assert bs.load(tmp_path) == []
    ids = [s["id"] for s in bs.sims()]
    shuffled = [sim(ids[3][:3], int(ids[3][-1])), sim(ids[0][:3], int(ids[0][-1]))]
    (tmp_path / "resultados.jsonl").write_text("\n".join(json.dumps(r) for r in shuffled), encoding="utf-8")
    assert [r["id"] for r in bs.load(tmp_path)] == [ids[0], ids[3]]


def test_veredito_em_palavras_diz_quando_o_ic_cabe_mas_poucas_simulacoes_ficam_dentro():
    deltas = [0.0] * 7 + [-0.9, -0.9, -0.9]  # média dentro da margem, 3 de 10 fora (todas com o LP mais barato)
    d = bs.describe([sim(f"m{k:02d}", 0, slsqp=3.0, free=3.0 * (1 + x / 100)) for k, x in enumerate(deltas)], bs.free_gap)
    assert d["verdict"] == "inconclusive" and d["ci_within_margin"]
    assert "NÃO demonstrada" in bs.verdict_text(d) and "70,0%" in bs.verdict_text(d)
