"""Benchmark v3 LP × SLSQP (``dietopt.benchmark``): desenho determinístico e estatística; sem rodar o RuFaS."""

import pytest

from dietopt import benchmark as bm


def row(animal="lac-alta", menu="base", k=0, lp=100.0, slsqp=(100.0,), status="ok"):
    """Registro sintético de um caso (o mesmo formato que ``run_case`` grava)."""
    record = {"id": f"{animal}/{menu}/p{k}", "animal": animal, "menu": menu, "price_set": k, "prices": {}, "price_seed": 1, "resolution": "normal", "status": status}
    if status == "ok":
        record["lp"] = {"cost": lp, "verified": True, "seconds": 10.0, "regime": "com_desconto"}
        record["slsqp"] = [{"seed": i, "ok": True, "cost": c, "seconds": 0.1} for i, c in enumerate(slsqp)]
    return record


def test_casos_sao_fixos_e_cobrem_animal_cardapio_e_preco():
    a, b = bm.cases(), bm.cases()
    assert a == b  # determinístico
    assert len(a) == len(bm.ANIMALS) * len(bm.MENUS) * (bm.PRICE_SETS + 1)
    assert len({c["id"] for c in a}) == len(a)


def test_animais_nao_trazem_metano_nem_nitrogenio_informados():
    # os dois são calculados da dieta (module/emissions.py); informá-los mudaria o problema comparado
    assert all("enteric_methane" not in cow and "urinary_nitrogen" not in cow for _, _, cow in bm.ANIMALS.values())


def test_o_primeiro_conjunto_e_o_base_e_os_sorteados_ficam_na_faixa():
    low, high = bm.PRICE_FACTOR
    for menu, base in bm.MENUS.items():
        sets = bm.price_sets(menu)
        assert sets[0] == base and len(sets) == bm.PRICE_SETS + 1
        for prices in sets[1:]:
            assert set(prices) == set(base)
            for feed, price in prices.items():
                assert base[feed] * low * 0.999 <= price <= base[feed] * high * 1.001


def test_outra_semente_gera_outros_precos_e_a_mesma_semente_repete():
    assert bm.price_sets("base", 1) == bm.price_sets("base", 1)
    assert bm.price_sets("base", 1)[1:] != bm.price_sets("base", 2)[1:]
    assert bm.price_sets("base")[1:] != bm.price_sets("amplo")[1:]  # cardápios diferentes não repetem o sorteio


def test_diferenca_relativa_tem_sinal_do_lp():
    assert bm.gap_pct(99.0, 100.0) == pytest.approx(-1.0)  # LP mais barato: negativa
    assert bm.gap_pct(101.0, 100.0) == pytest.approx(1.0)


def test_bootstrap_por_agrupamento_de_valores_iguais_nao_tem_incerteza():
    assert bm.cluster_bootstrap_ci({"a": [0.2, 0.2], "b": [0.2, 0.2]}) == pytest.approx((0.2, 0.2))
    assert all(map(lambda v: v != v, bm.cluster_bootstrap_ci({})))  # sem grupos: nan


def test_o_intervalo_reamostra_grupos_e_fica_mais_largo_que_o_dos_casos():
    # dois grupos muito diferentes: reamostrar grupos dá um intervalo largo, mesmo com muitos casos por grupo
    low, high = bm.cluster_bootstrap_ci({"a": [-1.0] * 12, "b": [1.0] * 12})
    assert low == pytest.approx(-1.0) and high == pytest.approx(1.0)


def test_equivalente_quando_todas_as_diferencas_sao_minimas():
    rows = [row(a, m, k, lp=100.0 + 0.01 * (-1) ** k) for a in ("lac-alta", "lac-media") for m in ("base", "amplo") for k in range(4)]
    d = bm.describe(rows)
    assert d["equivalent"] and d["share_within_margin"] == 1.0 and d["outliers"] == []
    assert d["lp_cheaper"] + d["tie"] + d["lp_dearer"] == d["compared"] == 16


def test_nao_equivalente_quando_muitos_casos_saem_da_margem():
    rows = [row("lac-alta", "base", k, lp=99.0 if k < 4 else 100.0) for k in range(10)]  # 4 de 10 com o LP 1% mais barato
    d = bm.describe(rows)
    assert d["share_within_margin"] == pytest.approx(0.6) and not d["equivalent"]
    assert len(d["outliers"]) == 4 and d["lp_cheaper"] == 4


def test_a_referencia_e_o_melhor_slsqp_e_so_conta_execucoes_viaveis():
    r = row(lp=100.0, slsqp=(100.4, 103.0))
    r["slsqp"].append({"seed": 9, "ok": False, "cost": 50.0, "seconds": 0.1})  # não viável: não pode virar referência
    d = bm.describe([r])
    assert d["mean"] == pytest.approx((100.0 - 100.4) / 100.4 * 100)
    assert d["slsqp_failed"] == 1 and d["cases_with_a_failure"] == 1 and d["seed_spread_pct"]["max"] == pytest.approx((103.0 - 100.4) / 100.4 * 100)


def test_caso_sem_execucao_viavel_do_slsqp_nao_entra_na_comparacao():
    r = row()
    r["slsqp"] = [{"seed": 0, "ok": False, "cost": 90.0, "seconds": 0.1}]
    d = bm.describe([r, row(k=1)])
    assert d["cases"] == 2 and d["compared"] == 1


def test_caso_sem_solucao_do_lp_e_listado_e_nao_quebra_o_resumo():
    rows = [row(k=0), {**row(k=1, status="infeasible"), "slsqp_converged": 0}]
    s = bm.summarize(rows)
    assert s["overall"]["solved"] == 1 and s["unsolved"] == [{"id": "lac-alta/base/p1", "status": "infeasible", "slsqp_converged": 0}]
    text = bm.report_text(s, {"resolution": "normal", "seeds": 10, "python": "3", "numpy": "2"})
    assert "SEM SOLUÇÃO NO LP (1)" in text and "em 1 deles" in text


def test_o_efeito_dos_precos_vem_do_custo_otimo_dentro_de_cada_animal_e_cardapio():
    rows = [row(k=0, lp=100.0, slsqp=(100.0,)), row(k=1, lp=150.0, slsqp=(150.0,))]
    assert bm.describe(rows)["price_effect_pct"]["max"] == pytest.approx(50.0)


def test_relatorio_traz_veredito_geral_por_animal_e_por_cardapio():
    rows = [row(a, m, k) for a in ("lac-alta", "vaca-seca") for m in ("base", "enxuto") for k in range(3)]
    text = bm.report_text(bm.summarize(rows), {"resolution": "normal", "seeds": 10, "python": "3", "numpy": "2"})
    assert "VEREDITO: EQUIVALENTE" in text and "POR ANIMAL" in text and "POR CARDÁPIO" in text
    assert "vaca-seca" in text and "enxuto" in text
