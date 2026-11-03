"""Importação de preços por CSV (RF-22): conversão para US$/kg de MS e mapeamento por id ou nome."""

import pytest

from dietopt.feeds import feed_library
from dietopt.prices import import_prices

NRC = feed_library("NRC")


def preco(resultado, feed_id):
    return resultado["prices"][str(feed_id)]


def test_dolar_por_kg_de_ms_entra_sem_conversao():
    r = import_prices("NRC", "id,preco\n50,0.09\n110,0.12\n")
    assert preco(r, 50) == 0.09 and preco(r, 110) == 0.12 and r["problems"] == []
    assert r["items"][0]["name"] == NRC[50].name and r["standard"] == "NRC"


def test_reais_por_saca_na_materia_natural_viram_dolar_por_kg_de_ms():  # LINEARIZACAO.md, 7.2
    r = import_prices("NRC", "id,preco,moeda,cambio,unidade_kg,base\n44,70,BRL,5.0,60,MN\n")
    esperado = 70 / 60 / (NRC[44].dm / 100) / 5.0
    assert preco(r, 44) == pytest.approx(esperado)
    assert "BRL" in r["items"][0]["original"] and "60 kg" in r["items"][0]["original"]


def test_cambio_da_tela_vale_para_linhas_sem_cambio_e_o_da_linha_prevalece():
    csv = "id;preco;moeda;cambio\n50;0,50;BRL;\n110;0,60;BRL;4\n"
    r = import_prices("NRC", csv, default_fx=5.0)
    assert preco(r, 50) == pytest.approx(0.10) and preco(r, 110) == pytest.approx(0.15)


def test_reais_sem_cambio_e_um_problema_com_o_motivo():
    r = import_prices("NRC", "id,preco,moeda\n50,0.5,BRL\n")
    assert r["prices"] == {} and "câmbio" in r["problems"][0]["reason"] and r["problems"][0]["line"] == 2


def test_nome_exato_sem_acento_e_caixa_encontra_o_alimento_e_ausente_e_listado():
    nome = f"{NRC[44].name} — {NRC[44].description}".upper()  # os nomes da biblioteca têm vírgulas: entre aspas no CSV
    r = import_prices("NRC", f'alimento,preco\n"{nome}",0.3\nArroz em grão,0.2\n')
    assert preco(r, 44) == 0.3
    assert len(r["problems"]) == 1 and "não encontrado" in r["problems"][0]["reason"] and "Arroz" in r["problems"][0]["text"]


def test_id_inexistente_na_biblioteca_do_padrao_e_problema():
    r = import_prices("NASEM", "id,preco\n166,0.4\n44,0.3\n")  # o farelo de soja 44% (166) só existe no NRC
    assert list(r["prices"]) == ["44"] and "166" in r["problems"][0]["reason"] and "NASEM" in r["problems"][0]["reason"]


def test_separador_ponto_e_virgula_virgula_decimal_bom_e_comentarios_sao_aceitos():
    csv = "\ufeff# cotações de 03/11\nPreço;ID;Fonte\n0,25;138;CEPEA arroz\n\n"
    r = import_prices("NRC", csv)
    assert preco(r, 138) == 0.25 and r["items"][0]["source"] == "CEPEA arroz"


@pytest.mark.parametrize(
    "linha,trecho",
    [("50,abc", "preço inválido"), ("50,-1", "negativo"), ("xx,0.1", "id inválido"), ("50,1,EUR", "moeda"), ("50,1,USD,,0", "kg por unidade"), (",0.1", "sem id nem nome")],
)
def test_linhas_invalidas_viram_problemas_sem_derrubar_as_outras(linha, trecho):
    r = import_prices("NRC", f"id,preco,moeda,cambio,unidade_kg\n{linha}\n110,0.12\n".replace("\n50,1,USD,,0", "\n50,1,USD,,0"))
    assert preco(r, 110) == 0.12 and any(trecho in p["reason"] for p in r["problems"])


def test_id_repetido_vale_o_ultimo_com_aviso():
    r = import_prices("NRC", "id,preco\n50,0.1\n50,0.2\n")
    assert preco(r, 50) == 0.2 and "já veio na linha 2" in r["warnings"][0]


@pytest.mark.parametrize("texto,mensagem", [("", "vazio"), ("id\n50\n", "preço"), ("preco\n1\n", "identificação")])
def test_cabecalho_incompleto_e_recusado(texto, mensagem):
    with pytest.raises(ValueError, match=mensagem):
        import_prices("NRC", texto)


def test_cambio_invalido_e_padrao_desconhecido_sao_recusados():
    with pytest.raises(ValueError, match="câmbio"):
        import_prices("NRC", "id,preco\n50,1\n", default_fx=0)
    with pytest.raises(ValueError, match="Padrão"):
        import_prices("XYZ", "id,preco\n50,1\n")


def test_nome_curto_que_serve_a_varios_alimentos_e_ambiguo_e_pede_o_id():
    r = import_prices("NRC", f'alimento,preco\n"{NRC[44].name}",0.3\n')
    assert r["prices"] == {} and "mais de um alimento" in r["problems"][0]["reason"] and "44" in r["problems"][0]["reason"]
