"""Tamanho do rebanho (RF-13): validação do número de vacas e escala do rebanho inteiro."""

import json

import pytest

from dietopt.herd import DEFAULT_COWS, MAX_COWS, MIN_COWS, parse_cow_num, scale_herd
from dietopt.rufas_adapter import Scenario, build_scenario
from dietopt.scenarios import cache_key
from dietopt.server import scenario_from

BASE = {
    "herd_information": {
        "calf_num": 8,
        "heiferI_num": 44,
        "heiferII_num": 38,
        "heiferIII_num_springers": 5,
        "cow_num": 100,
        "replace_num": 500,
        "herd_num": 100,
        "breed": "HO",
    },
    "pen_information": [
        {"animal_combination": "CALF", "number_of_stalls": 15},
        {"animal_combination": "LAC_COW", "number_of_stalls": 88},
    ],
    "housing": "barn",
}


def test_sem_valor_ou_o_padrao_mantem_o_rebanho_do_exemplo():
    assert parse_cow_num(None) is None
    assert parse_cow_num("") is None
    assert parse_cow_num(DEFAULT_COWS) is None  # mesma chave de cache de "não informado"


@pytest.mark.parametrize("value, expected", [(MIN_COWS, MIN_COWS), (250, 250), ("200", 200), (150.0, 150), (MAX_COWS, MAX_COWS)])
def test_numero_valido(value, expected):
    assert parse_cow_num(value) == expected


@pytest.mark.parametrize("value", [MIN_COWS - 1, MAX_COWS + 1, 0, -5, 12.5, "muitas", True, [100]])
def test_numero_invalido_e_recusado(value):
    with pytest.raises(ValueError, match="vacas"):
        parse_cow_num(value)


def test_escala_o_rebanho_inteiro_e_o_alvo():
    animal = scale_herd(BASE, 200)
    scaled = animal["herd_information"]
    assert (scaled["cow_num"], scaled["herd_num"]) == (200, 200)
    assert (scaled["calf_num"], scaled["heiferI_num"], scaled["heiferII_num"], scaled["heiferIII_num_springers"]) == (16, 88, 76, 10)
    assert scaled["replace_num"] == 1000
    assert scaled["breed"] == "HO" and animal["housing"] == "barn"
    assert BASE["herd_information"]["cow_num"] == 100  # a entrada não é alterada


def test_baias_acompanham_o_rebanho_arredondando_para_cima():
    pens = {pen["animal_combination"]: pen["number_of_stalls"] for pen in scale_herd(BASE, 250)["pen_information"]}
    assert pens == {"CALF": 38, "LAC_COW": 220}  # 15 × 2,5 = 37,5 → 38
    assert all(pen["number_of_stalls"] >= 1 for pen in scale_herd(BASE, MIN_COWS)["pen_information"])


def test_rebanho_pequeno_mantem_ao_menos_um_animal_por_categoria():
    animal = scale_herd(BASE, MIN_COWS)
    scaled = animal["herd_information"]
    assert scaled["cow_num"] == scaled["herd_num"] == MIN_COWS
    assert all(scaled[key] >= 1 for key in ("calf_num", "heiferI_num", "heiferII_num", "heiferIII_num_springers", "replace_num"))


def test_montagem_do_cenario_escreve_o_rebanho_escalado(tmp_path):
    base = build_scenario(Scenario(name="t", cow_num=40), runs_dir=tmp_path).parent
    info = json.loads((base / "animal.json").read_text(encoding="utf-8"))["herd_information"]
    assert info["cow_num"] == info["herd_num"] == 40
    assert info["heiferI_num"] == 18  # 44 × 0,4
    pens = {pen["animal_combination"]: pen["number_of_stalls"] for pen in json.loads((base / "animal.json").read_text(encoding="utf-8"))["pen_information"]}
    assert pens["CALF"] == 6  # 15 × 0,4


def test_sem_numero_o_exemplo_fica_como_esta(tmp_path):
    base = build_scenario(Scenario(name="t"), runs_dir=tmp_path).parent
    info = json.loads((base / "animal.json").read_text(encoding="utf-8"))["herd_information"]
    assert (info["cow_num"], info["herd_num"]) == (100, 100)


def test_o_numero_de_vacas_muda_a_chave_do_cache():
    params = {"feeds": [44, 230], "standard": "NRC"}
    padrao, grande = (scenario_from({**params, **extra}, "t")[0] for extra in ({}, {"cow_num": 200}))
    assert cache_key(padrao) != cache_key(grande)
    assert cache_key(scenario_from({**params, "cow_num": DEFAULT_COWS}, "t")[0]) == cache_key(padrao)


def test_servidor_recusa_numero_fora_do_intervalo():
    with pytest.raises(ValueError, match="fora do intervalo"):
        scenario_from({"feeds": [44, 230], "cow_num": MAX_COWS + 1}, "t")
