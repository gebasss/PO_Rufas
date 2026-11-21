"""Benchmark v4 LP × SLSQP (``dietopt.benchmark``): desenho determinístico e estatística; sem rodar o otimizador."""

import csv

import pytest

from dietopt import benchmark as bm
from dietopt.feeds import feed_library


def row(animal="lac-alta", menu="m00", k=0, lp=100.0, same=100.0, slsqp=(100.0,), status="ok", own=None):
    """Registro sintético de um caso (o mesmo formato que ``run_case`` grava). ``own``: custos que também respeitam as emissões da dieta."""
    record = {"id": f"{animal}/{menu}/p{k}", "animal": animal, "menu": menu, "price_set": k, "prices": {}, "seed": 1, "resolution": "normal", "status": status}
    if status == "ok":
        record["lp"] = {"cost": lp, "verified": True, "seconds": 10.0, "regime": "com_desconto"}
        record["lp_same"] = {"cost": same, "verified": True, "seconds": 11.0, "regime": "com_desconto"}
        own = slsqp if own is None else own
        record["slsqp"] = [{"seed": i, "ok": True, "own_ok": c in own, "cost": c, "seconds": 0.1} for i, c in enumerate(slsqp)]
        record["emissions_used"] = {"methane_g": 450.0, "urinary_nitrogen_kg": 0.25}
    return record


# ---------------------------------------------------------------------------------------------------------------------
# Desenho
# ---------------------------------------------------------------------------------------------------------------------
def test_casos_sao_fixos_e_cobrem_animal_cardapio_e_preco():
    a, b = bm.cases(), bm.cases()
    assert a == b  # determinístico
    assert len(a) == len(bm.ANIMALS) * bm.MENUS * (bm.PRICE_SETS + 1)
    assert len({c["id"] for c in a}) == len(a)


def test_animais_nao_trazem_metano_nem_nitrogenio_informados():
    # os dois são calculados da dieta (module/emissions.py); informá-los mudaria o problema comparado
    assert all("enteric_methane" not in cow and "urinary_nitrogen" not in cow for _, _, cow in bm.ANIMALS.values())


def test_cardapios_respeitam_a_forma_e_usam_alimentos_da_biblioteca_com_preco():
    library = feed_library(bm.STANDARD)
    for k in range(bm.MENUS):
        menu = bm.menu_of(k)
        for kind, (low, high) in bm.MENU_SHAPE.items():
            count = sum(1 for i in menu if library[i].kind == kind)
            assert min(low, len(bm.feed_pool()[kind])) <= count <= high
        assert all(i in library and p > 0 for i, p in menu.items())


def test_o_conjunto_de_alimentos_tem_precos_padrao_ou_os_acrescentados():
    pool = bm.feed_pool()
    assert set(bm.EXTRA_FEEDS) <= {i for kind in pool.values() for i in kind}
    assert all(price > 0 for kind in pool.values() for price in kind.values())


def test_o_primeiro_conjunto_e_o_padrao_e_os_sorteados_ficam_na_faixa():
    low, high = bm.PRICE_FACTOR
    for k in range(bm.MENUS):
        base = bm.menu_of(k)
        sets = bm.price_sets(k)
        assert sets[0] == base and len(sets) == bm.PRICE_SETS + 1
        for prices in sets[1:]:
            assert set(prices) == set(base)
            assert all(base[i] * low * 0.999 <= p <= base[i] * high * 1.001 for i, p in prices.items())


def test_outra_semente_gera_outros_cardapios_e_precos_e_a_mesma_repete():
    assert [bm.menu_of(k, 1) for k in range(4)] == [bm.menu_of(k, 1) for k in range(4)]
    assert [bm.menu_of(k, 1) for k in range(bm.MENUS)] != [bm.menu_of(k, 2) for k in range(bm.MENUS)]
    assert bm.price_sets(0, 1)[1:] != bm.price_sets(0, 2)[1:]
    assert len({tuple(bm.menu_of(k)) for k in range(bm.MENUS)}) > 1  # os cardápios variam entre si


# ---------------------------------------------------------------------------------------------------------------------
# Estatística
# ---------------------------------------------------------------------------------------------------------------------
def test_diferenca_relativa_tem_sinal_do_lp():
    assert bm.gap_pct(99.0, 100.0) == pytest.approx(-1.0)  # LP mais barato: negativa
    assert bm.gap_pct(101.0, 100.0) == pytest.approx(1.0)


def test_bootstrap_por_agrupamento_de_valores_iguais_nao_tem_incerteza():
    assert bm.cluster_bootstrap_ci({"a": [0.2, 0.2], "b": [0.2, 0.2]}) == pytest.approx((0.2, 0.2))
    assert all(v != v for v in bm.cluster_bootstrap_ci({}))  # sem grupos: nan


def test_o_intervalo_reamostra_grupos_e_fica_largo_mesmo_com_muitos_casos_por_grupo():
    low, high = bm.cluster_bootstrap_ci({"a": [-1.0] * 12, "b": [1.0] * 12})
    assert low == pytest.approx(-1.0) and high == pytest.approx(1.0)


def test_a_primaria_compara_o_lp_nas_mesmas_constantes_com_o_melhor_slsqp():
    r = row(lp=101.0, same=100.0, slsqp=(100.4, 103.0))
    assert bm.primary_gap(r) == pytest.approx((100.0 - 100.4) / 100.4 * 100)  # não usa o LP do módulo (101)
    assert bm.consistency_cost(r) == pytest.approx(1.0)


def test_a_secundaria_so_aceita_slsqp_que_respeita_as_emissoes_da_propria_dieta():
    r = row(lp=100.0, same=99.0, slsqp=(98.0, 100.2), own=(100.2,))  # a execução de 98,0 só é viável com as constantes
    assert bm.primary_gap(r) == pytest.approx((99.0 - 98.0) / 98.0 * 100)
    assert bm.consistent_gap(r) == pytest.approx((100.0 - 100.2) / 100.2 * 100)
    assert bm.consistent_gap(row(slsqp=(98.0,), own=())) is None  # nenhuma execução consistente: o caso não entra


def test_equivalente_quando_todas_as_diferencas_sao_minimas():
    rows = [row(f"a{a}", f"m{m}", k, same=100.0 + 0.01 * (-1) ** k) for a in range(2) for m in range(2) for k in range(4)]
    d = bm.describe_gaps(rows, bm.primary_gap)
    assert d["equivalent"] and d["share_within_margin"] == 1.0 and d["outliers"] == []
    assert d["lp_cheaper"] + d["tie"] + d["lp_dearer"] == d["compared"] == 16 and d["groups"] == 4


def test_nao_equivalente_quando_muitos_casos_saem_da_margem():
    rows = [row("lac-alta", "m00", k, same=99.0 if k < 4 else 100.0) for k in range(10)]  # 4 de 10 com o LP 1% mais barato
    d = bm.describe_gaps(rows, bm.primary_gap)
    assert d["share_within_margin"] == pytest.approx(0.6) and not d["equivalent"]
    assert len(d["outliers"]) == 4 and d["lp_cheaper"] == 4


def test_caso_sem_execucao_viavel_do_slsqp_nao_entra_na_comparacao():
    r = row()
    r["slsqp"] = [{"seed": 0, "ok": False, "own_ok": False, "cost": 90.0, "seconds": 0.1}]
    d = bm.describe_gaps([r, row(k=1)], bm.primary_gap)
    assert d["cases"] == 2 and d["compared"] == 1


def test_wilcoxon_usa_a_media_de_cada_grupo():
    groups = {f"g{i}": [0.1 + 0.01 * i] * 3 for i in range(8)}  # todos os grupos com o LP acima: efeito sistemático
    assert bm.wilcoxon_p(groups) < 0.05
    assert bm.wilcoxon_p({"a": [0.0], "b": [0.0]}) is None  # só zeros


def test_solver_stats_conta_falhas_sementes_tempos_e_peso_dos_precos():
    failed = row(k=1, same=150.0, slsqp=(150.0, 153.0))
    failed["slsqp"].append({"seed": 9, "ok": False, "own_ok": False, "cost": 1.0, "seconds": 0.3})
    s = bm.solver_stats([row(k=0), failed])
    assert s["slsqp_runs"] == 4 and s["slsqp_failed"] == 1 and s["cases_with_a_failure"] == 1
    assert s["seed_spread_pct"]["max"] == pytest.approx(2.0)
    assert s["seconds"]["lp"]["median"] == 10.0 and s["seconds"]["slsqp"]["q1"] <= s["seconds"]["slsqp"]["q3"]
    assert s["price_effect_pct"]["max"] == pytest.approx(50.0)  # 100 contra 150 no mesmo animal e cardápio


# ---------------------------------------------------------------------------------------------------------------------
# Saídas
# ---------------------------------------------------------------------------------------------------------------------
def test_caso_sem_solucao_do_lp_e_listado_e_nao_quebra_o_resumo():
    rows = [row(k=0), {**row(k=1, status="infeasible"), "slsqp_converged": 0}]
    s = bm.summarize(rows)
    assert s["solver"]["solved"] == 1 and s["unsolved"] == [{"id": "lac-alta/m00/p1", "status": "infeasible", "slsqp_converged": 0}]
    text = bm.report_text(s, {"resolution": "normal", "seeds": 10, **bm.versions()})
    assert "SEM SOLUÇÃO NO LP (1 casos)" in text and "em 1 deles" in text


def test_relatorio_traz_primaria_secundarias_por_animal_e_versoes():
    rows = [row(a, f"m0{m}", k) for a in ("lac-alta", "vaca-seca") for m in range(2) for k in range(3)]
    text = bm.report_text(bm.summarize(rows), {"resolution": "normal", "seeds": 10, **bm.versions()})
    assert "COMPARAÇÃO PRIMÁRIA" in text and "SECUNDÁRIA 1" in text and "SECUNDÁRIA 2" in text and "POR ANIMAL" in text
    assert "VEREDITO: EQUIVALENTE" in text and "RuFaS 1.0.6" in text and "commit" in text


def test_csv_tem_uma_linha_por_caso_e_uma_por_execucao(tmp_path):
    rows = [row(k=0, slsqp=(100.0, 101.0)), {**row(k=1, status="infeasible"), "slsqp_converged": 0}]
    bm.write_csv(tmp_path, rows)
    cases = list(csv.DictReader((tmp_path / "resultados.csv").open(encoding="utf-8")))
    runs = list(csv.DictReader((tmp_path / "execucoes_slsqp.csv").open(encoding="utf-8")))
    assert [c["id"] for c in cases] == ["lac-alta/m00/p0", "lac-alta/m00/p1"] and cases[1]["status"] == "infeasible"
    assert len(runs) == 2 and float(cases[0]["primary_gap_pct"]) == 0.0


def test_versoes_registram_commit_e_rufas():
    v = bm.versions()
    assert v["rufas"] == "1.0.6" and v["commit"] and set(v) >= {"python", "numpy", "scipy", "dirty", "date"}
