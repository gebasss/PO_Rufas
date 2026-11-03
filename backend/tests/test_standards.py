import csv
import json

import pytest

from dietopt.feeds import feed_library
from dietopt.rufas_adapter import Scenario, build_scenario
from dietopt.scenarios import Economics, with_defaults
from dietopt.server import feed_payload, scenario_from
from dietopt.standards import NASEM, NASEM_ONLY_TO_NRC, NRC, get_standard, library_ids

BASE_SET = [50, 110, 44, 167, 138, 230, 23]  # "Conjunto base" da interface


def test_padrao_desconhecido_e_recusado_e_vazio_vale_nrc():
    assert get_standard(None) is NRC
    assert get_standard("NASEM") is NASEM
    with pytest.raises(ValueError, match="desconhecido"):
        get_standard("INRA")


def test_bibliotecas_tem_os_alimentos_do_conjunto_base_e_so_o_nrc_tem_o_trocado():
    assert set(BASE_SET) <= library_ids("NRC")
    assert set(BASE_SET) <= library_ids("NASEM")
    assert 166 in library_ids("NRC") and 166 not in library_ids("NASEM")  # farelo de soja 44%


def test_biblioteca_nasem_traz_amido_e_ed_base_e_a_nrc_nao():
    nasem, nrc = feed_library("NASEM"), feed_library("NRC")
    assert nasem[44].starch and nasem[44].de_base
    assert nrc[44].starch is not None and nrc[44].de_base is None  # o amido existe nas duas bibliotecas (RF-27); a ED base, só no NASEM
    assert all(f.kind not in {"Milk", "Starter"} for f in nasem.values())


def test_alimento_para_a_interface_nel_so_no_nrc():
    assert "nel" in feed_payload(feed_library("NRC")[44], "NRC")
    nasem = feed_payload(feed_library("NASEM")[44], "NASEM")
    assert "nel" not in nasem and nasem["starch"] and nasem["de_base"]


def test_precos_fora_da_biblioteca_do_padrao_sao_descartados():
    prices = {44: 0.28, 166: 0.50}
    nasem = with_defaults(Scenario(name="x", nutrient_standard="NASEM"), Economics(prices=prices))
    nrc = with_defaults(Scenario(name="x", nutrient_standard="NRC"), Economics(prices=prices))
    assert nasem.feed_prices == {44: 0.28}
    assert nrc.feed_prices == prices


def test_cenario_a_partir_dos_parametros_usa_o_padrao_e_recusa_alimento_ausente():
    scenario, _ = scenario_from({"feeds": BASE_SET, "standard": "NASEM"}, "t")
    assert scenario.nutrient_standard == "NASEM"
    assert scenario_from({"feeds": BASE_SET}, "t")[0].nutrient_standard == "NRC"
    with pytest.raises(ValueError, match=r"\[166\]"):
        scenario_from({"feeds": [44, 166], "standard": "NASEM"}, "t")


def test_montagem_do_cenario_nasem_grava_limites_na_biblioteca_nasem(tmp_path):
    scenario = Scenario(
        name="t", nutrient_standard="NASEM", lac_cow_feeds=BASE_SET, feed_limits={44: (0.5, 7.0)}, feed_prices={44: 0.3}
    )
    metadata_path = build_scenario(scenario, runs_dir=tmp_path).with_name("metadata.json")
    base = metadata_path.parent
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["files"]["NASEM_Comp"]["path"].endswith(f"{NASEM.library_file}")
    assert metadata["files"]["NASEM_Comp"]["path"] != "input/data/feed/" + NASEM.library_file  # é a cópia do cenário
    with open(base / NASEM.library_file, encoding="utf-8", newline="") as handle:
        rows = {int(r["rufas_id"]): r for r in csv.DictReader(handle)}
    assert (rows[44]["lower_limit"], rows[44]["limit"]) == ("0.5", "7.0")
    feed = json.loads((base / "feed.json").read_text(encoding="utf-8"))
    assert feed["lac_cow_feeds"] == sorted(BASE_SET)
    assert json.loads((base / "config.json").read_text(encoding="utf-8"))["nutrient_standard"] == "NASEM"
    assert not (base / NRC.library_file).exists()


def test_montagem_do_cenario_nrc_troca_ids_so_nasem(tmp_path):
    scenario = Scenario(name="t", nutrient_standard="NRC", lac_cow_feeds=[44, 230])
    base = build_scenario(scenario, runs_dir=tmp_path).parent
    feed = json.loads((base / "feed.json").read_text(encoding="utf-8"))
    purchased = {p["purchased_feed"] for p in feed["purchased_feeds"]}
    assert not purchased & set(NASEM_ONLY_TO_NRC) and 230 in purchased  # 301 virou 230
    assert (base / NRC.library_file).exists()
