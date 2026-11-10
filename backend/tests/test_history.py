"""Histórico de execuções (D3): gravação, listagem, base, exclusão, retenção e integração com as tarefas."""

import json

import pytest

from dietopt import history
from dietopt.jobs import Cancelled, Job

SIM_PARAMS = {"feeds": [50, 110, 44], "years": 2, "milk_price": 0.45}
SIM_RESULT = {
    "summary": {"margem": 1000.0, "receita": 5000.0, "custo_alimentacao": 4000.0, "custo_vaca_dia": 4.0, "leite_kg": 9e6, "milk_price": 0.45},
    "checks_summary": {"alert": 1, "warn": 0, "ok": 4},
}  # fmt: skip
SENS_RESULT = {"rows": [{"cenario": "S1", "Res": 10.0}, {"cenario": "S2", "Res": 30.0}, {"cenario": "S3", "Res": None}]}
EVAL_RESULT = {
    "standard": "NRC", "category": "LAC_COW", "best": "B",
    "diets": [{"name": "A", "cost": 3.0, "feasible": False}, {"name": "B", "cost": 4.0, "feasible": True}],
}  # fmt: skip


@pytest.fixture(autouse=True)
def pasta(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "HISTORY_DIR", tmp_path / "_history")


def test_titulo_mostra_o_rebanho_so_quando_nao_e_o_padrao():
    grande = {**SIM_RESULT, "summary": {**SIM_RESULT["summary"], "cow_num": 250}}
    meta = history.record("simulation", {**SIM_PARAMS, "cow_num": 250}, grande)
    assert meta["title"].endswith("2 anos · 250 vacas") and meta["summary"]["cow_num"] == 250
    assert "vacas" not in history.record("simulation", SIM_PARAMS, SIM_RESULT)["title"]


def test_grava_dois_arquivos_e_devolve_os_metadados_com_resumo():
    meta = history.record("simulation", SIM_PARAMS, SIM_RESULT)
    assert meta["title"] == "Simulação do RuFaS · 3 alimentos · 2 anos" and meta["status"] == "done" and not meta["is_base"]
    assert meta["summary"]["margem"] == 1000.0 and meta["summary"]["alertas"] == 1 and meta["summary"]["n_feeds"] == 3
    assert {p.name for p in history.HISTORY_DIR.iterdir()} == {f"{meta['id']}.json", f"{meta['id']}.meta.json"}
    completo = history.get_run(meta["id"])
    assert completo["params"] == SIM_PARAMS and completo["result"] == SIM_RESULT and "search" not in completo


def test_resumo_de_cada_tipo():
    sens = history.record("sensitivity", {"factors": [{}, {}], "method": "grid"}, SENS_RESULT)["summary"]
    assert (sens["n_scenarios"], sens["n_ok"], sens["best"], sens["worst"], sens["n_factors"]) == (3, 2, 30.0, 10.0, 2)
    avaliacao = history.record("evaluation", {}, EVAL_RESULT)["summary"]
    assert (avaliacao["n_diets"], avaliacao["n_feasible"], avaliacao["best"], avaliacao["best_cost"]) == (2, 1, "B", 4.0)
    otima = {"standard": "NRC", "category": "LAC_COW", "status": "ok", "diet": {"cost": 3.8}, "rufas": {"lp_gap_pct": 0.01}, "feed_ids": [1, 2]}
    resumo = history.record("optimization", {}, otima)["summary"]
    assert (resumo["cost"], resumo["gap_pct"], resumo["n_feeds"]) == (3.8, 0.01, 2)


def test_lista_do_mais_recente_filtra_por_tipo_estado_e_texto_e_pagina():
    for _ in range(5):
        history.record("simulation", SIM_PARAMS, SIM_RESULT)
    history.record("evaluation", {}, EVAL_RESULT)
    history.record("simulation", SIM_PARAMS, None, "RuntimeError: falhou\ndetalhe")
    tudo = history.list_runs()
    assert tudo["total"] == 7 and tudo["items"][0]["status"] == "error" and tudo["items"][0]["error"] == "RuntimeError: falhou"
    assert [i["id"] for i in tudo["items"]] == sorted((i["id"] for i in tudo["items"]), reverse=True)
    assert history.list_runs(kind="evaluation")["total"] == 1 and history.list_runs(status="error")["total"] == 1
    assert history.list_runs(query="dietas")["total"] == 1
    assert history.list_runs(query="avaliação A B")["total"] == 1  # a busca também olha o nome das dietas
    pagina = history.list_runs(per_page=3, page=3)
    assert len(pagina["items"]) == 1 and pagina["pages"] == 3 and all("search" not in i for i in pagina["items"])


def test_so_uma_base_por_tipo_e_so_execucao_concluida_pode_ser_base():
    a, b = (history.record("simulation", SIM_PARAMS, SIM_RESULT) for _ in range(2))
    avaliacao = history.record("evaluation", {}, EVAL_RESULT)
    history.set_base(a["id"])
    history.set_base(avaliacao["id"])
    assert history.base_run("simulation")["id"] == a["id"] and history.base_run("evaluation")["id"] == avaliacao["id"]
    history.set_base(b["id"])  # troca a base da simulação; a da avaliação fica
    assert history.base_run("simulation")["id"] == b["id"] and history.base_run("evaluation")["id"] == avaliacao["id"]
    assert history.get_run(a["id"])["is_base"] is False and history.get_run(b["id"])["is_base"] is True
    history.set_base(b["id"], False)
    assert history.base_run("simulation") is None and history.base_run("sensitivity") is None
    falha = history.record("simulation", SIM_PARAMS, None, "Erro")
    with pytest.raises(ValueError, match="concluída"):
        history.set_base(falha["id"])


def test_exclui_e_recusa_identificador_invalido_ou_inexistente():
    meta = history.record("simulation", SIM_PARAMS, SIM_RESULT)
    history.delete_run(meta["id"])
    assert history.list_runs()["total"] == 0 and list(history.HISTORY_DIR.iterdir()) == []
    for acao in (history.get_run, history.delete_run, history.set_base):
        with pytest.raises(ValueError, match="não encontrada"):
            acao(meta["id"])
        with pytest.raises(ValueError, match="inválido"):
            acao("../../etc/passwd")


def test_retencao_apaga_as_mais_antigas_menos_a_base(monkeypatch):
    monkeypatch.setattr(history, "MAX_RUNS", 3)
    primeira = history.record("simulation", SIM_PARAMS, SIM_RESULT)
    history.set_base(primeira["id"])
    ids = [history.record("simulation", SIM_PARAMS, SIM_RESULT)["id"] for _ in range(4)]
    restantes = {m["id"] for m in history.list_runs(per_page=100)["items"]}
    assert primeira["id"] in restantes and len(restantes) == 4  # as 3 mais recentes e a base
    assert ids[0] not in restantes and ids[-1] in restantes


def test_filtros_invalidos_sao_recusados():
    for kwargs in ({"kind": "x"}, {"status": "x"}, {"page": 0}, {"per_page": 500}):
        with pytest.raises(ValueError):
            history.list_runs(**kwargs)
    with pytest.raises(ValueError):
        history.record("x", {}, {})


def test_tarefa_envolvida_grava_o_resultado_com_run_id_a_falha_com_o_motivo_e_ignora_o_cancelamento():
    job = Job(id="t", kind="simulate", params=SIM_PARAMS)
    resultado = history.with_history("simulation", lambda j: SIM_RESULT)(job)
    assert history.get_run(resultado["run_id"])["result"] == SIM_RESULT and resultado["summary"] == SIM_RESULT["summary"]

    def falha(j):
        raise RuntimeError("RuFaS caiu")

    with pytest.raises(RuntimeError):
        history.with_history("simulation", falha)(job)
    erro = history.list_runs(status="error")["items"][0]
    assert erro["error"] == "RuntimeError: RuFaS caiu" and history.get_run(erro["id"])["result"] is None

    def cancela(j):
        raise Cancelled

    total = history.list_runs()["total"]
    with pytest.raises(Cancelled):
        history.with_history("optimization", cancela)(job)
    assert history.list_runs()["total"] == total  # cancelar não é execução


def test_arquivo_de_metadados_corrompido_fica_fora_da_lista():
    meta = history.record("simulation", SIM_PARAMS, SIM_RESULT)
    (history.HISTORY_DIR / "20200101-000000-abcd.meta.json").write_text("{não é json", encoding="utf-8")
    assert [m["id"] for m in history.list_runs()["items"]] == [meta["id"]]
    json.loads((history.HISTORY_DIR / f"{meta['id']}.meta.json").read_text(encoding="utf-8"))
