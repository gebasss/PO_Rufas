"""Exportação de CSV e relatórios (RF-20): conteúdo, escape de texto do usuário e despacho."""

import csv
import io
from datetime import datetime

import pytest

from dietopt.exports import export_file, module_report, sensitivity_csv, sensitivity_report, simulation_csv, simulation_report
from dietopt.module.evaluate import evaluate_diets

AGORA = datetime(2026, 11, 3, 15, 0)
SIM = {
    "summary": {"cenario": "web_x", "margem": 1234567.5, "receita": 2000000.0, "custo_alimentacao": 765432.5, "custo_vaca_dia": 4.01,
                "leite_kg": 5_000_000.0, "milk_price": 0.45, "reducao_leite": 0.0, "max_reducao": 5.0},
    "feeds": [{"id": 50, "label": "Corn, Yellow — Corn silage <b>x</b>", "price": 0.09}, {"id": 110, "label": "Legumes — Silage", "price": 0.12}],
    "average_ration": {"50": 12.0, "110": 20.0, "138": 0.0, "dry_matter_intake_total": 32.0},
    "checks": [{"id": "V1", "label": "Consumo", "status": "alert", "value": "+29,5%", "limit": "ok até +12%", "detail": "", "metrics": {}}],
    "balance": [{"id": "calcium", "label": "Cálcio", "unit": "g/dia", "kind": "surplus", "requirement": 70.9, "supply": 315.6, "difference": 244.7, "worst_difference": 241.5, "status": "ok", "note": ""}],
}  # fmt: skip
SENS = {
    "columns": ["Corn silage", "Preço do leite", "Res"],
    "feeds": [{"id": 50, "label": "Silagem de milho"}, {"id": 110, "label": "Silagem de leguminosa"}],
    "rows": [
        {"cenario": "S1", "Corn silage": 0.08, "Preço do leite": 0.4, "Res": 1000.0, "leite_kg": 5e6, "receita": 2e6, "custo_alimentacao": 7e5, "custo_vaca_dia": 3.9, "reducao_leite": 0.0, "ration": {"50": 12.0, "110": 20.0}},
        {"cenario": "S2", "Corn silage": 0.1, "Preço do leite": 0.5, "Res": 3000.0, "leite_kg": 5e6, "receita": 2.5e6, "custo_alimentacao": 8e5, "custo_vaca_dia": 4.1, "reducao_leite": 0.3, "ration": {"50": 10.0, "110": 22.0}},
        {"cenario": "S3", "Corn silage": 0.12, "Preço do leite": 0.6, "Res": None, "erro": "RuntimeError: falhou"},
    ],
    "effects": [{"fator": "Corn silage", "spearman": -0.8}, {"fator": "Preço do leite", "spearman": None}],
}  # fmt: skip


def linhas(texto):
    return list(csv.reader(io.StringIO(texto)))


def test_csv_da_racao_media_tem_participacao_e_custo_e_ignora_o_que_nao_entra():
    tabela = linhas(simulation_csv(SIM))
    assert tabela[0] == ["id", "alimento", "kg_ms_vaca_dia", "pct_da_dieta", "preco_usd_kg_ms", "custo_usd_vaca_dia"]
    assert [r[0] for r in tabela[1:3]] == ["110", "50"]  # do maior para o menor; 138 (0 kg) e o total do RuFaS ficam fora
    assert float(tabela[1][3]) == pytest.approx(62.5) and float(tabela[1][5]) == pytest.approx(20 * 0.12)
    assert tabela[-1][1] == "TOTAL" and float(tabela[-1][2]) == pytest.approx(32.0) and float(tabela[-1][5]) == pytest.approx(12 * 0.09 + 20 * 0.12)


def test_csv_da_sensibilidade_traz_fatores_resultado_e_uma_coluna_por_alimento():
    tabela = linhas(sensitivity_csv(SENS))
    assert tabela[0][:4] == ["cenario", "Corn silage", "Preço do leite", "Res"]
    assert "kg_ms: Silagem de milho" in tabela[0] and tabela[0][-1] == "erro"
    s1, s3 = tabela[1], tabela[3]
    assert float(s1[3]) == 1000.0 and float(s1[tabela[0].index("kg_ms: Silagem de milho")]) == 12.0
    assert s3[3] == "" and s3[-1].startswith("RuntimeError")  # cenário que falhou: sem números inventados


def test_relatorio_da_simulacao_tem_indicadores_racao_verificacoes_e_balanco_em_formato_brasileiro():
    html = simulation_report({**SIM, "limits": {"50": [0.0, 15.0]}}, {"note": "Revisar o teto da silagem."}, AGORA)
    assert "US$ 1.234.568" in html and "5.000 t" in html and "03/11/2026 15:00" in html
    assert "Verificações de consistência" in html and "Alerta" in html and "Balanço nutricional" in html
    assert "15,00" in html and "Revisar o teto da silagem." in html  # limite da tela e observação do usuário


def test_relatorio_escapa_texto_do_usuario_e_nomes_de_alimentos():
    html = simulation_report(SIM, {"note": "<script>alert(1)</script>"}, AGORA)
    assert "<script>" not in html and "&lt;script&gt;" in html
    assert "<b>x</b>" not in html and "&lt;b&gt;x&lt;/b&gt;" in html


def test_relatorio_da_sensibilidade_destaca_melhor_e_pior_cenario_e_lista_o_que_falhou():
    html = sensitivity_report(SENS, {}, AGORA)
    assert "Melhor margem: S2" in html and "Pior margem: S1" in html and "falhou" in html
    assert "Silagem de milho 10,0 kg" in html and "−0,80" not in html and "-0,80" in html  # efeito de Spearman; o fator sem valor não aparece
    assert "Preço do leite</td><td class=\"n\">—" not in html


LACTACAO = dict(
    body_weight=650, mature_body_weight=700, parity=2, days_in_milk=100, calving_interval=400,
    milk_production=40, milk_fat=3.7, milk_true_protein=3.1, milk_lactose=4.85,
    housing="Barn", distance=100, day_of_pregnancy=60, body_condition_score_5=3.0,
)  # fmt: skip
PRECOS = {23: 1.10, 44: 0.28, 50: 0.09, 110: 0.12, 138: 0.25, 167: 0.55, 230: 0.10}
DIETAS = [
    {"name": "Silagem e concentrado", "amounts": {50: 11.87, 110: 19.42, 44: 0.63, 167: 0.63, 230: 0.6, 23: 0.03}},
    {"name": "Só silagem", "amounts": {50: 15, 110: 15}},
]


@pytest.fixture(scope="module")
def avaliacao():
    return evaluate_diets("NRC", "LAC_COW", LACTACAO, DIETAS, PRECOS)


def test_csv_e_relatorio_do_modulo_ordenam_da_mais_recomendada_e_incluem_o_otimo(avaliacao):
    arquivo = export_file("csv", "module", avaliacao)
    assert arquivo["filename"].endswith(".csv") and arquivo["content"].startswith("﻿")
    tabela = linhas(arquivo["content"].lstrip("﻿"))
    pos = tabela[0].index("posicao")
    assert {r[pos] for r in tabela[1:]} == {"1", "2"} and all(r[tabela[0].index("dieta")] for r in tabela[1:])
    otimo = {"status": "ok", "diet": {"cost": 3.8, "scalars": {"dmi": 33.0, "tdn_percentage": 60.0, "concentrate_percentage": 3.0}, "amounts": {"50": 12.0}, "verified": True},
             "rufas": {"cost_min": 3.79, "cost_median": 3.8, "n_success": 5, "n_runs": 5, "lp_gap_pct": 0.1}}  # fmt: skip
    html = module_report(avaliacao, {"optimal": otimo, "feed_names": {50: "Silagem de milho"}, "standard": "NRC 2001"}, AGORA)
    assert "Desvio do ótimo" in html and "Dieta ótima (linear)" in html and "Silagem de milho" in html and "+0,100%" in html
    assert "Desvio do ótimo" not in module_report(avaliacao, {}, AGORA)  # sem a dieta ótima, sem a coluna


def test_despacho_devolve_nome_tipo_e_conteudo_e_recusa_pedidos_invalidos():
    arquivo = export_file("report", "simulation", SIM, {"note": "x"})
    assert arquivo["filename"] == "relatorio-simulacao.html" and arquivo["mime"].startswith("text/html") and arquivo["content"].startswith("<!doctype html>")
    with pytest.raises(ValueError, match="desconhecida"):
        export_file("pdf", "simulation", SIM)
    with pytest.raises(ValueError, match="resultado"):
        export_file("csv", "simulation", {})
    with pytest.raises(ValueError, match="incompleto"):
        export_file("csv", "sensitivity", {"columns": ["Res"]})
