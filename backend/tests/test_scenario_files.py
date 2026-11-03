"""Arquivos de cenário (RF-21): ida e volta, validação, versão e migração."""

import json
from datetime import datetime

import pytest

from dietopt import scenario_files
from dietopt.scenario_files import FORMAT, VERSION, pack, unpack

COW = {
    "standard": "NRC",
    "params": {"milkPrice": 0.5, "years": 2, "maxReduction": 5},
    "feeds": [{"id": 50, "price": 0.09, "min": 0, "max": 100}, {"id": 44, "price": 0.28, "min": 1.5, "max": None}, {"id": 999999, "price": 1, "min": 0, "max": 1}],
    "sensitivity": {"method": "latin", "levels": 4, "factors": {"44": {"on": True, "low": 0.2, "high": 0.4}, "milk_price": {"on": False, "low": 0.4, "high": 0.6}, "138": {"on": True, "low": 0.1, "high": 0.2}}},
}  # fmt: skip
MODULE = {
    "standard": "NASEM", "category": "LAC_COW", "animalType": "LAC_COW",
    "cow": {"body_weight": 650, "parity": 2, "housing": "Barn", "milk_fat": None, "distance": ""},
    "override": {"calcium": 80.0},
    "feeds": [{"id": 50, "price": 0.09, "min": 0, "max": 100}, {"id": 110, "price": 0.12, "min": 0, "max": 100}],
    "diets": [{"name": "A", "amounts": {"50": 10, "110": 15, "44": 3}}, {"name": "B", "amounts": {}}],
    "tolerance": 2.5, "resolution": "fina", "seeds": 3,
}  # fmt: skip
AGORA = datetime(2026, 11, 3, 16, 0, 0)


def volta(kind, data):
    arquivo = pack(kind, data, AGORA)
    return arquivo, unpack(arquivo["content"])


def test_envelope_traz_formato_versao_tipo_data_e_dados_legiveis():
    arquivo = pack("cow", COW, AGORA)
    envelope = json.loads(arquivo["content"])
    assert envelope["format"] == FORMAT and envelope["version"] == VERSION and envelope["kind"] == "cow"
    assert envelope["saved_at"] == "2026-11-03T16:00:00" and arquivo["filename"].endswith(".json") and "\n  " in arquivo["content"]


def test_cenario_da_vaca_volta_igual_e_alimento_fora_da_biblioteca_e_removido_com_aviso():
    arquivo, lido = volta("cow", COW)
    assert lido["kind"] == "cow" and lido["version"] == VERSION
    assert [f["id"] for f in lido["data"]["feeds"]] == [50, 44]  # o id 999999 não existe
    assert lido["data"]["feeds"][1]["max"] == 100.0  # máximo vazio vale o teto padrão do alimento (kg/dia)
    assert lido["data"]["params"] == COW["params"]
    assert set(lido["data"]["sensitivity"]["factors"]) == {"44", "milk_price"}  # o fator do 138 não está no cenário
    assert unpack(arquivo["content"])["data"] == lido["data"]  # idempotente
    assert pack("cow", lido["data"], AGORA)["content"] == arquivo["content"]


def test_aviso_de_alimento_removido_aparece_so_ao_abrir():
    arquivo = pack("cow", {**COW, "feeds": COW["feeds"]}, AGORA)
    # o arquivo salvo já não tem o alimento inexistente; um arquivo feito à mão com ele avisa ao abrir
    envelope = json.loads(arquivo["content"])
    envelope["data"]["feeds"].append({"id": 999999, "price": 1, "min": 0, "max": 1})
    assert "999999" in unpack(json.dumps(envelope))["warnings"][0]


def test_cenario_do_modulo_volta_normalizado_sem_resultados_e_sem_campos_vazios():
    _, lido = volta("module", MODULE)
    dados = lido["data"]
    assert dados["standard"] == "NASEM" and dados["category"] == "LAC_COW" and dados["resolution"] == "fina" and dados["seeds"] == 3
    assert dados["cow"] == {"body_weight": 650.0, "parity": 2.0, "housing": "Barn"}  # vazios saem
    assert dados["override"] == {"calcium": 80.0} and dados["tolerance"] == 2.5
    assert dados["diets"][0]["amounts"] == {"50": 10.0, "110": 15.0}  # o 44 não está na tabela
    assert lido["warnings"] == []  # o arquivo salvo já saiu normalizado
    envelope = json.loads(pack("module", MODULE, AGORA)["content"])
    envelope["data"]["diets"][0]["amounts"]["44"] = 3
    assert "alimento 44" in " ".join(unpack(json.dumps(envelope))["warnings"])  # um arquivo feito à mão avisa ao abrir


@pytest.mark.parametrize(
    "kind,mudanca,trecho",
    [
        ("cow", {"params": {"milkPrice": -1, "years": 1, "maxReduction": 5}}, "Preço do leite"),
        ("cow", {"params": {"milkPrice": 0.5, "years": 9, "maxReduction": 5}}, "Anos"),
        ("cow", {"feeds": [{"id": 50, "price": None, "min": 0, "max": 1}]}, "preço"),
        ("cow", {"feeds": [{"id": 50, "price": 1, "min": 5, "max": 1}]}, "mínimo"),
        ("cow", {"feeds": [{"id": 50, "price": 1}, {"id": 50, "price": 2}]}, "repetido"),
        ("cow", {"sensitivity": {"method": "x"}}, "método"),
        ("cow", {"sensitivity": {"levels": 99}}, "níveis"),
        ("module", {"category": "XX"}, "Categoria"),
        ("module", {"animalType": "HEIFER_I"}, "pertence"),
        ("module", {"cow": {"inexistente": 1}}, "desconhecido"),
        ("module", {"cow": {"housing": "Lua"}}, "Alojamento"),
        ("module", {"override": {"xx": 1}}, "desconhecida"),
        ("module", {"resolution": "enorme"}, "Resolução"),
        ("module", {"seeds": 99}, "Execuções"),
        ("module", {"diets": [{"name": str(i), "amounts": {}} for i in range(11)]}, "No máximo"),
        ("module", {"diets": [{"name": "x" * 101, "amounts": {}}]}, "nome"),
    ],
)
def test_dados_invalidos_sao_recusados_ao_salvar_com_o_motivo(kind, mudanca, trecho):
    base = COW if kind == "cow" else MODULE
    with pytest.raises(ValueError, match=trecho):
        pack(kind, {**base, **mudanca}, AGORA)


@pytest.mark.parametrize(
    "texto,trecho",
    [
        ("não é json", "JSON"),
        ("[1, 2]", "não é um cenário"),
        (json.dumps({"format": "outro", "version": 1}), "não é um cenário"),
        (json.dumps({"format": FORMAT, "kind": "cow", "data": {}}), "versão"),
        (json.dumps({"format": FORMAT, "version": VERSION + 1, "kind": "cow", "data": {}}), "mais nova"),
        (json.dumps({"format": FORMAT, "version": VERSION, "kind": "xyz", "data": {}}), "Tipo de cenário"),
        (json.dumps({"format": FORMAT, "version": VERSION, "kind": "cow", "data": []}), "formato inválido"),
    ],
)
def test_arquivo_invalido_e_recusado_ao_abrir_com_o_motivo(texto, trecho):
    with pytest.raises(ValueError, match=trecho):
        unpack(texto)


def test_arquivo_com_bom_e_aceito():
    assert unpack("\ufeff" + pack("cow", COW, AGORA)["content"])["kind"] == "cow"


def test_arquivo_de_versao_antiga_passa_pela_migracao(monkeypatch):
    monkeypatch.setattr(scenario_files, "VERSION", 2)
    monkeypatch.setattr(scenario_files, "MIGRATIONS", {1: lambda d: {**d, "params": {"milkPrice": d["preco_do_leite"], "years": 1, "maxReduction": 5}}})
    antigo = {"format": FORMAT, "version": 1, "kind": "cow", "data": {"standard": "NRC", "preco_do_leite": 0.7, "feeds": []}}
    lido = unpack(json.dumps(antigo))
    assert lido["version"] == 2 and lido["data"]["params"]["milkPrice"] == 0.7
