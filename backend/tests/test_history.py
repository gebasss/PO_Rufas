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
    sens_meta = history.record("sensitivity", {"factors": [{}, {}], "method": "grid", "years": 2, "cow_num": 200}, SENS_RESULT)
    sens = sens_meta["summary"]
    assert (sens["n_scenarios"], sens["n_ok"], sens["best"], sens["worst"], sens["n_factors"]) == (3, 2, 30.0, 10.0, 2)
    assert (sens["years"], sens["cow_num"]) == (2, 200) and sens_meta["title"].endswith("3 cenários · 2 fatores · 2 anos · 200 vacas")
    padrao = history.record("sensitivity", {"factors": [{}], "method": "grid"}, SENS_RESULT)
    assert padrao["title"].endswith("1 fatores · 1 ano") and padrao["summary"]["cow_num"] == 100  # sem o rebanho padrão no título
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


def test_so_uma_simulacao_concluida_pode_ser_a_base():
    a, b = (history.record("simulation", SIM_PARAMS, SIM_RESULT) for _ in range(2))
    history.set_base(a["id"])
    assert history.base_run("simulation")["id"] == a["id"]
    history.set_base(b["id"])  # troca a base
    assert history.base_run("simulation")["id"] == b["id"]
    assert history.get_run(a["id"])["is_base"] is False and history.get_run(b["id"])["is_base"] is True
    history.set_base(b["id"], False)
    assert history.base_run("simulation") is None
    falha = history.record("simulation", SIM_PARAMS, None, "Erro")
    with pytest.raises(ValueError, match="concluída"):
        history.set_base(falha["id"])


def test_as_outras_execucoes_nao_usam_base_mas_uma_base_antiga_pode_ser_desmarcada():
    for kind, result in (("evaluation", EVAL_RESULT), ("sensitivity", SENS_RESULT)):
        meta = history.record(kind, {}, result)
        with pytest.raises(ValueError, match="Só uma simulação"):
            history.set_base(meta["id"])
        assert history.base_run(kind) is None
    antiga = history.record("evaluation", {}, EVAL_RESULT)
    path = history.HISTORY_DIR / f"{antiga['id']}.meta.json"
    path.write_text(json.dumps({**antiga, "is_base": True}), encoding="utf-8")  # base marcada por uma versão anterior
    assert history.base_run("evaluation")["id"] == antiga["id"]
    assert history.set_base(antiga["id"], False)["is_base"] is False and history.base_run("evaluation") is None


def test_nome_e_nota_aparecem_na_lista_entram_na_busca_e_tem_limite():
    meta = history.record("simulation", SIM_PARAMS, SIM_RESULT)
    assert meta["name"] == "" and meta["note"] == "" and "search_base" not in history.get_run(meta["id"])
    novo = history.update_run(meta["id"], "  Farelo  mais\n caro ", "Teste com\nsoja a US$ 0,60")
    assert novo["name"] == "Farelo mais caro" and novo["note"] == "Teste com\nsoja a US$ 0,60"
    assert history.list_runs(query="farelo caro")["total"] == 1 and history.list_runs(query="SOJA")["total"] == 1
    assert history.list_runs(query="3 alimentos")["total"] == 1  # a busca pelo título continua valendo
    assert history.get_run(meta["id"])["name"] == "Farelo mais caro" and "search" not in history.list_runs()["items"][0]
    assert history.update_run(meta["id"], note="")["name"] == "Farelo mais caro"  # None mantém; vazio apaga
    assert history.list_runs(query="soja")["total"] == 0 and history.get_run(meta["id"])["note"] == ""
    history.update_run(meta["id"], name="")
    assert history.list_runs(query="farelo")["total"] == 0
    for kwargs, motivo in (({"name": "x" * 81}, "80"), ({"note": "x" * 501}, "500"), ({"name": 3}, "texto")):
        with pytest.raises(ValueError, match=motivo):
            history.update_run(meta["id"], **kwargs)
    with pytest.raises(ValueError, match="inválido"):
        history.update_run("../x", "a")


def test_execucao_gravada_antes_do_nome_continua_listada_e_editavel():
    meta = history.record("simulation", SIM_PARAMS, SIM_RESULT)
    for path in (history.HISTORY_DIR / f"{meta['id']}.meta.json", history.HISTORY_DIR / f"{meta['id']}.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        for key in ("name", "note", "search_base"):
            data.pop(key)
        path.write_text(json.dumps(data), encoding="utf-8")
    assert "name" not in history.list_runs()["items"][0]
    history.update_run(meta["id"], "Antiga")
    assert history.list_runs(query="antiga simulação")["total"] == 1


def test_limpeza_apaga_so_as_pastas_web_e_conta_o_espaco(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "RUNS_DIR", tmp_path)
    for nome, tamanho in (("web_139373ee57_s001", 100), ("web_139373ee57_s002", 50), ("web_1c83d70a6c", 10)):
        (tmp_path / nome / "out").mkdir(parents=True)
        (tmp_path / nome / "out" / "r.json").write_bytes(b"x" * tamanho)
    for nome in ("e8_NRC", "sens_s001", "_cache", "web_nao_e_da_interface"):
        (tmp_path / nome).mkdir()
        (tmp_path / nome / "f.txt").write_text("fica", encoding="utf-8")
    meta = history.record("simulation", SIM_PARAMS, SIM_RESULT)
    relatorio = history.storage_report()
    assert relatorio["folders"] == 3 and relatorio["folders_bytes"] == 160 and relatorio["history_bytes"] > 0
    resultado = history.clean_folders()
    assert resultado == {"removed": 3, "failed": 0, "freed_bytes": 160}
    assert sorted(p.name for p in tmp_path.iterdir()) == ["_cache", "_history", "e8_NRC", "sens_s001", "web_nao_e_da_interface"]
    assert history.get_run(meta["id"])["result"] == SIM_RESULT  # o histórico não é tocado
    assert history.storage_report()["folders"] == 0 and history.clean_folders()["removed"] == 0


def test_limpeza_sem_pasta_runs_nao_falha(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "RUNS_DIR", tmp_path / "nao_existe")
    assert history.storage_report()["folders"] == 0 and history.clean_folders() == {"removed": 0, "failed": 0, "freed_bytes": 0}


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

    def recusa(j):
        raise ValueError("Esta análise exigiria 4.096 simulações do RuFaS; o limite é 100.")

    with pytest.raises(ValueError):
        history.with_history("sensitivity", recusa)(job)
    assert history.list_runs()["total"] == total  # pedido recusado na validação também não é execução


def test_arquivo_de_metadados_corrompido_fica_fora_da_lista():
    meta = history.record("simulation", SIM_PARAMS, SIM_RESULT)
    (history.HISTORY_DIR / "20200101-000000-abcd.meta.json").write_text("{não é json", encoding="utf-8")
    assert [m["id"] for m in history.list_runs()["items"]] == [meta["id"]]
    json.loads((history.HISTORY_DIR / f"{meta['id']}.meta.json").read_text(encoding="utf-8"))
