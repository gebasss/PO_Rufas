from dietopt.feeds import load_feed_library
from dietopt.rufas_adapter import NASEM_ONLY_TO_NRC, Scenario, failure_reason, remap_feed_ids
from dietopt.scenarios import cache_key


def test_troca_ids_so_nasem_por_nrc_em_listas_e_campos_de_id():
    feed = {
        "lac_cow_feeds": [44, 301, 302],
        "purchased_feeds": [{"purchased_feed": 301, "purchased_feed_cost": 301.0}],
        "user_defined_ration_percentages": {"lac_cow": [{"feed_type": 302, "ration_percentage": 302}]},
        "milk_reduction_maximum": 301,
    }
    out = remap_feed_ids(feed, NASEM_ONLY_TO_NRC)
    assert out["lac_cow_feeds"] == [44, 230, 167]
    assert out["purchased_feeds"][0]["purchased_feed"] == 230
    assert out["purchased_feeds"][0]["purchased_feed_cost"] == 301.0  # valores que não são ids ficam intactos
    assert out["user_defined_ration_percentages"]["lac_cow"][0] == {"feed_type": 167, "ration_percentage": 302}
    assert out["milk_reduction_maximum"] == 301


def test_tetos_padrao_evitam_mineral_como_enchimento():
    feeds = {f.id: f for f in load_feed_library()}
    assert feeds[230].default_max == 0.6  # carbonato de cálcio
    assert feeds[23].default_max == 1.0  # farinha de sangue
    assert feeds[76].default_max == 0.9  # óleo vegetal
    assert feeds[44].default_max == 100.0  # milho: sem teto
    assert all(f.kind not in {"Milk", "Starter"} for f in feeds.values())


def test_falha_do_rufas_e_resumida_na_ultima_excecao():
    console = "Traceback...\nValueError: Milk production reduction limit reached.\n\nFinished task: ..."
    assert failure_reason(console) == "ValueError: Milk production reduction limit reached."


def test_chave_de_cache_ignora_nome_mas_nao_parametros():
    a = Scenario(name="a", feed_prices={44: 0.3})
    b = Scenario(name="b", feed_prices={44: 0.3})
    c = Scenario(name="c", feed_prices={44: 0.4})
    assert cache_key(a) == cache_key(b)
    assert cache_key(a) != cache_key(c)
    assert cache_key(a) != cache_key(Scenario(name="a", feed_prices={44: 0.3}, milk_reduction_maximum=5.0))
