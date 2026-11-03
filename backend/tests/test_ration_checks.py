"""Verificações de consistência (RF-27, FSD A.4) e balanço nutricional (RF-19) da ração obtida."""

import pytest

from dietopt.feeds import feed_library
from dietopt.ration_balance import build_balance
from dietopt.ration_checks import (
    Composition,
    check_fat,
    check_intake,
    check_milk_loss,
    check_table_5_1,
    check_total_ndf,
    composition,
    consistency_checks,
    summarize,
    table_5_1,
)
from dietopt.rufas_results import parse_outputs

NRC = feed_library("NRC")


def comp(ndf=35.0, forage=30.0, starch=20.0, fat=3.0):
    return Composition(dmi=25.0, ndf=ndf, forage_ndf=forage, starch=starch, fat=fat)


@pytest.mark.parametrize("consumo,esperado", [(33.5, "alert"), (29.6, "warn"), (28.0, "ok")])
def test_v1_consumo_contra_o_estimado(consumo, esperado):  # A.4.5-1
    assert check_intake([consumo], [25.8])["status"] == esperado


def test_v1_media_decide_e_o_pior_intervalo_so_eleva_a_atencao():
    resultado = check_intake([26.0, 26.0, 33.5], [25.8, 25.8, 25.8])  # média +10,5%, pior +29,8%
    assert resultado["status"] == "warn" and resultado["metrics"]["worst_excess_pct"] > 24
    assert check_intake([1.0], [0.0]) is None  # sem consumo estimado não há o que comparar


def test_v2_fdn_total_no_limite_do_rufas_e_atencao_e_fora_e_alerta():  # A.4.5-3
    assert check_total_ndf(comp(ndf=45.0))["status"] == "warn"
    assert check_total_ndf(comp(ndf=45.0000006))["status"] == "warn"  # o RuFaS deixa a FDN em 45,0000006%
    assert check_total_ndf(comp(ndf=46.0))["status"] == "alert"
    assert check_total_ndf(comp(ndf=24.0))["status"] == "alert"
    assert check_total_ndf(comp(ndf=35.0))["status"] == "ok"


def test_tabela_5_1_interpola_entre_15_e_19_de_fdn_de_forragem():
    assert table_5_1(19.0) == (25.0, 30.0) and table_5_1(35.0) == (25.0, 30.0)
    assert table_5_1(17.0) == (29.0, 26.0) and table_5_1(15.0) == (33.0, 22.0)
    assert table_5_1(14.0) is None


def test_v3_racao_com_fdn_total_abaixo_do_minimo_da_tabela_falha():  # A.4.5-2
    assert check_table_5_1(comp(forage=17.0, ndf=28.0, starch=25.0))["status"] == "alert"  # mínimo de FDN total: 29%
    assert check_table_5_1(comp(forage=17.0, ndf=30.0, starch=24.0))["status"] == "warn"  # cumpre, mas com forragem < 19%
    assert check_table_5_1(comp(forage=14.0, ndf=40.0, starch=10.0))["status"] == "alert"  # abaixo de 15%: fora da tabela
    assert check_table_5_1(comp(forage=30.0, ndf=35.0, starch=29.0))["status"] == "warn"  # amido a menos de 2 pontos do máximo
    assert check_table_5_1(comp(forage=30.0, ndf=35.0, starch=20.0))["status"] == "ok"


def test_v3_pior_intervalo_pode_elevar_o_estado_a_atencao():
    resultado = check_table_5_1(comp(forage=30.0, ndf=35.0, starch=20.0), [comp(forage=30.0, ndf=35.0, starch=29.5)])
    assert resultado["status"] == "warn"


def test_v4_gordura():  # A.4.5-4
    assert check_fat(comp(fat=7.0))["status"] == "warn"
    assert check_fat(comp(fat=7.2))["status"] == "alert"
    assert check_fat(comp(fat=4.9))["status"] == "ok"


def test_v5_leite_perdido():
    assert check_milk_loss(0.0, 5.0)["status"] == "ok"
    assert check_milk_loss(1.0, 5.0)["status"] == "warn"
    assert check_milk_loss(2.5, 5.0)["status"] == "alert"


def test_composicao_pondera_pela_quantidade_e_usa_so_forragem_na_fdn_de_forragem():
    racao = {"50": 10.0, "44": 10.0, "dry_matter_intake_total": 20.0}  # silagem de milho imatura e milho moído seco
    c = composition(racao, NRC)
    assert c.dmi == 20.0
    assert c.ndf == pytest.approx((10 * NRC[50].ndf + 10 * NRC[44].ndf) / 20)
    assert c.forage_ndf == pytest.approx(10 * NRC[50].ndf / 20)  # só a forragem entra
    assert c.starch == pytest.approx((10 * NRC[50].starch + 10 * NRC[44].starch) / 20) and c.starch > 0
    assert composition({"dry_matter_intake_total": 0.0}, NRC) is None


def test_conjunto_das_verificacoes_nao_muda_a_racao_e_resume_os_estados():
    intervalos = [{"50": 12.0, "110": 19.0, "44": 0.7, "167": 0.6, "230": 0.6, "dry_matter_intake_total": 32.9}] * 3
    media = {"50": 12.0, "110": 19.0, "44": 0.7, "167": 0.6, "230": 0.6}
    checks = consistency_checks(intervalos, [25.8] * 3, media, NRC, 0.0, 5.0)
    assert [c["id"] for c in checks] == ["V1", "V2", "V3", "V4", "V5"]
    assert next(c for c in checks if c["id"] == "V1")["status"] == "alert"  # +27,5% do estimado
    assert sum(summarize(checks).values()) == 5 and summarize(checks)["alert"] >= 1
    assert all(set(c) == {"id", "label", "status", "value", "limit", "detail", "metrics"} for c in checks)


AVALIACAO = {
    "total_energy_difference": 6.65, "maintenance_energy_difference": 38.6, "lactation_energy_difference": 16.9,
    "growth_energy_difference": 28.7, "metabolizable_protein_difference": 0.0, "calcium_difference": 244.4,
    "phosphorus_difference": 1.52, "dry_matter_difference": 0.0, "ndf_percent_difference": 6e-07,
    "forage_ndf_percent_difference": 29.6, "fat_percent_difference": 4.7,
}  # fmt: skip
EXIGENCIAS = {
    "NEmaint_requirement": 10.04, "NEa_requirement": 0.017, "NEg_requirement": 0.486, "NEpreg_requirement": 0.314,
    "NEl_requirement": 31.15, "MP_requirement": 2821.9, "Ca_requirement": 72.2, "P_req": 65.3, "P_req_process": 0.0,
    "DMIest_requirement": 25.77,
}  # fmt: skip


def linha(balanco, id_):
    return next(r for r in balanco if r["id"] == id_)


def test_balanco_usa_as_diferencas_do_rufas_e_soma_as_exigencias_de_energia():
    balanco = build_balance([AVALIACAO], [EXIGENCIAS])
    total = linha(balanco, "total_energy")
    assert total["requirement"] == pytest.approx(10.04 + 0.017 + 0.486 + 0.314 + 31.15)
    assert total["supply"] == pytest.approx(total["requirement"] + 6.65)
    assert total["margin_pct"] == pytest.approx(6.65 / total["requirement"] * 100) and total["status"] == "ok"
    assert linha(balanco, "lactation_energy")["requirement"] == pytest.approx(31.15 + 0.314)
    assert all(r["status"] == "ok" for r in balanco)  # a FDN de 45,0000006% está dentro da tolerância
    assert "supply" not in linha(balanco, "metabolizable_protein")  # só se sabe que está na faixa


def test_balanco_marca_deficit_e_fora_da_faixa_e_usa_o_pior_intervalo():
    ruim = {**AVALIACAO, "calcium_difference": -5.0, "metabolizable_protein_difference": -120.0, "fat_percent_difference": -0.4}
    balanco = build_balance([AVALIACAO, ruim], [EXIGENCIAS, EXIGENCIAS])
    assert linha(balanco, "calcium")["status"] == "deficit" and linha(balanco, "calcium")["worst_difference"] == -5.0
    assert linha(balanco, "calcium")["difference"] == pytest.approx((244.4 - 5.0) / 2)
    assert linha(balanco, "metabolizable_protein")["status"] == "fora"
    assert linha(balanco, "metabolizable_protein")["worst_difference"] == -120.0
    assert linha(balanco, "fat")["status"] == "deficit"  # 7 − gordura < 0: passou do teto
    assert linha(balanco, "total_energy")["status"] == "ok"


def test_balanco_vazio_quando_o_rufas_nao_devolveu_a_avaliacao():
    assert build_balance([], [EXIGENCIAS]) == []


def test_leitura_da_avaliacao_do_rufas_no_resultado_da_simulacao():
    saida = {
        "x.json": {
            "Animal.report_average_nutrient_evaluation_results.avg_eval_results_for_LAC_COW": {
                "values": [AVALIACAO, {**AVALIACAO, "calcium_difference": 1.0}],
                "info_maps": [{"simulation_day": 30}, {"simulation_day": 60}],
            }
        }
    }
    resultado = parse_outputs(saida)
    assert [e["calcium_difference"] for e in resultado.evaluations] == [244.4, 1.0]


def test_balanco_traz_o_valor_observado_onde_a_oferta_nao_sai_da_diferenca():
    balanco = build_balance([AVALIACAO], [EXIGENCIAS], {"dry_matter": 33.4, "ndf": 45.0, "forage_ndf": 44.6, "fat": 2.3})
    assert linha(balanco, "ndf")["supply"] == 45.0 and linha(balanco, "fat")["supply"] == 2.3
    assert linha(balanco, "dry_matter")["supply"] == 33.4 and linha(balanco, "dry_matter")["requirement"] == pytest.approx(25.77)
