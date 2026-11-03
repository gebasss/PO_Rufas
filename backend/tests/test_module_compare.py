"""Comparação do modelo linear com o RuFaS, fase 1 (FSD, Anexo B.8)."""

import csv
import io

import pytest

from dietopt.module.api import compare_payload
from dietopt.module.compare import CSV_COLUMNS, TOLERANCE_PCT, build_report, report_csv
from dietopt.module.evaluate import PERTURBATION, evaluate_diets

LACTACAO = dict(
    body_weight=650, mature_body_weight=700, parity=2, days_in_milk=100, calving_interval=400,
    milk_production=40, milk_fat=3.7, milk_true_protein=3.1, milk_lactose=4.85,
    housing="Barn", distance=100, day_of_pregnancy=60, body_condition_score_5=3.0,
)  # fmt: skip
LOTE = dict(enteric_methane=400, urinary_nitrogen=0.2)  # valores de teste (energia do NASEM)
PRECOS = {23: 1.10, 44: 0.28, 50: 0.09, 110: 0.12, 138: 0.25, 167: 0.55, 230: 0.10}
RACAO_RUFAS = {"name": "RuFaS", "amounts": {50: 11.87, 110: 19.42, 44: 0.63, 167: 0.63, 230: 0.6, 23: 0.03}}  # TDN 59,97%, D = 1
RACAO_CONCENTRADO = {"name": "Concentrado", "amounts": {50: 9, 110: 10, 44: 8, 167: 3, 230: 0.2}}  # TDN 69,9%, D < 1 no NRC
RACAO_SILAGEM = {"name": "Só silagem", "amounts": {50: 15, 110: 15}}
DIETAS = [RACAO_RUFAS, RACAO_CONCENTRADO, RACAO_SILAGEM]


def avaliar(standard, cow, diets=DIETAS):
    return evaluate_diets(standard, "LAC_COW", cow, diets, PRECOS)


def diet(report, name):
    return next(d for d in report["diets"] if d["name"] == name)


def row(report, name, constraint):
    return next(c for c in diet(report, name)["constraints"] if c["id"] == constraint)


@pytest.mark.parametrize("standard,cow", [("NRC", LACTACAO), ("NASEM", {**LACTACAO, **LOTE})])
def test_identidade_no_ponto_em_todas_as_dietas(standard, cow):  # B.9-1
    report = build_report(avaliar(standard, cow))
    assert report["summary"]["identity_ok"]
    for d in report["diets"]:
        for c in d["constraints"]:
            assert abs(c["point_error_pct"]) < 1e-6, (d["name"], c["id"])


def test_limites_por_alimento_nao_entram_na_comparacao():
    report = build_report(avaliar("NRC", LACTACAO))
    assert all(not c["id"].startswith("limit_") for d in report["diets"] for c in d["constraints"])


def test_restricoes_exatas_nao_tem_sondas_e_as_aproximadas_tem_uma_por_escala():
    report = build_report(avaliar("NRC", LACTACAO))
    for d in report["diets"]:
        for c in d["constraints"]:
            if c["kind"] == "A":
                assert [p["scale"] for p in c["probes"]] == list(PERTURBATION), c["id"]
            else:
                assert c["probes"] == [] and c["max_error_pct"] == pytest.approx(0.0, abs=1e-6), c["id"]


def test_erro_das_sondas_tem_sinal_e_o_maximo_e_o_maior_em_modulo():
    report = build_report(avaliar("NRC", LACTACAO, [RACAO_CONCENTRADO]))
    energia = row(report, "Concentrado", "ne_maintenance")
    erros = [p["error_pct"] for p in energia["probes"]]
    assert energia["max_error_pct"] == pytest.approx(max(abs(e) for e in erros))
    assert max(abs(e) for e in erros) > TOLERANCE_PCT  # D < 1: a energia linearizada erra mais de 1% a ±5%
    assert not energia["within_tolerance"]


def test_dieta_sem_desconto_fica_dentro_da_tolerancia_e_a_com_desconto_nao():
    report = build_report(avaliar("NRC", LACTACAO))
    assert diet(report, "RuFaS")["within_tolerance"] and diet(report, "RuFaS")["max_error_pct"] <= TOLERANCE_PCT
    concentrado = diet(report, "Concentrado")
    assert not concentrado["within_tolerance"] and concentrado["n_above_tolerance"] >= 1
    assert concentrado["worst_constraint"]["id"] in {"ne_maintenance", "ne_lactation", "ne_growth", "ne_total"}
    assert report["summary"]["worst"]["diet"] == "Concentrado" and report["summary"]["max_error_pct"] == concentrado["max_error_pct"]
    assert report["summary"]["n_diets_above_tolerance"] >= 1


def test_tolerancia_maior_aceita_o_que_a_menor_recusa():
    evaluation = avaliar("NRC", LACTACAO, [RACAO_CONCENTRADO])
    estreita = build_report(evaluation, 1.0)
    larga = build_report(evaluation, 10.0)
    assert estreita["summary"]["n_above_tolerance"] > 0 == larga["summary"]["n_above_tolerance"]
    assert larga["tolerance_pct"] == 10.0
    with pytest.raises(ValueError):
        build_report(evaluation, -1)


def test_folga_original_e_a_oferta_original_menos_a_exigencia():
    report = build_report(avaliar("NRC", LACTACAO))
    calcio = row(report, "RuFaS", "calcium")  # piso: oferta − exigência
    assert calcio["slack_original"] == pytest.approx(calcio["supply_original"] - calcio["requirement"])
    teto = row(report, "RuFaS", "fat")  # teto: exigência − oferta
    assert teto["slack_original"] == pytest.approx(teto["requirement"] - teto["supply_original"])
    assert calcio["slack_linear"] == pytest.approx(calcio["slack_original"])


def test_restricao_indisponivel_fica_fora_dos_numeros_com_a_nota():
    report = build_report(avaliar("NASEM", LACTACAO))  # sem metano e N urinário
    d = diet(report, "RuFaS")
    energia = row(report, "RuFaS", "ne_nasem")
    assert energia["status_linear"] == "indisponivel" and "max_error_pct" not in energia and energia["note"]
    assert d["n_unavailable"] == 1 and d["incomplete"] and d["n_compared"] == len(d["constraints"]) - 1


def test_estado_igual_nas_sondas_quando_a_folga_nao_cruza_zero():
    report = build_report(avaliar("NRC", LACTACAO, [RACAO_RUFAS]))
    assert report["summary"]["same_state_in_probes"]


def test_csv_tem_uma_linha_por_dieta_e_restricao_comparada():
    report = build_report(avaliar("NRC", LACTACAO))
    linhas = list(csv.reader(io.StringIO(report_csv(report))))
    assert tuple(linhas[0]) == CSV_COLUMNS
    assert len(linhas) - 1 == report["summary"]["n_compared"]
    indice = {nome: i for i, nome in enumerate(CSV_COLUMNS)}
    energia = next(l for l in linhas[1:] if l[indice["dieta"]] == "Concentrado" and l[indice["restricao_id"]] == "ne_maintenance")
    assert energia[indice["dentro_da_tolerancia"]] == "não"
    assert float(energia[indice["erro_max_pct"]]) > TOLERANCE_PCT
    assert energia[indice["erro_x0.95_pct"]] != "" and energia[indice["erro_x1.05_pct"]] != ""
    exata = next(l for l in linhas[1:] if l[indice["restricao_id"]] == "calcium")
    assert exata[indice["erro_x0.95_pct"]] == ""  # classe L: sem sondas


def test_payload_da_rota_traz_o_relatorio_o_csv_e_a_tolerancia_pedida():
    corpo = {"standard": "NRC", "category": "LAC_COW", "cow": LACTACAO, "diets": [RACAO_RUFAS], "prices": PRECOS, "tolerance_pct": 2.5}
    resposta = compare_payload(corpo)
    assert resposta["tolerance_pct"] == 2.5 and resposta["csv"].startswith(",".join(CSV_COLUMNS))
    assert resposta["diets"][0]["name"] == "RuFaS"
    assert compare_payload({**corpo, "tolerance_pct": ""})["tolerance_pct"] == TOLERANCE_PCT


def test_nasem_traz_o_aviso_de_replicacao():
    report = build_report(avaliar("NASEM", {**LACTACAO, **LOTE}))
    assert any("amido" in w for w in report["warnings"])
