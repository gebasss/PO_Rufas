"""Curva de lactação de Wood (RF-14): fórmula, marcos, produção em 305 dias e os parâmetros de referência do RuFaS."""

import json
import math
from pathlib import Path

import pytest

from dietopt import lactation
from dietopt.rufas_results import parse_outputs

RUFAS_INPUT = Path(__file__).resolve().parents[2] / "vendor/RuFaS/input/data/animal/lactation_curve_adjustment_inputs.json"


def test_wood_segue_a_formula_y_igual_l_t_elevado_a_m_vezes_exp_menos_n_t():
    esperado = 20.0 * 100**0.25 * math.exp(-0.004 * 100)

    assert lactation.wood_yield(100, 20.0, 0.25, 0.004) == pytest.approx(esperado)


def test_curva_tem_um_valor_por_dia_e_uma_curva_por_paridade():
    curvas = lactation.lactation_curve(None, days=330)

    assert set(curvas) == {1, 2, 3}
    assert all(len(valores) == 330 for valores in curvas.values())
    assert curvas[1][0] == pytest.approx(lactation.wood_yield(1, **lactation.DEFAULT_WOOD[1]))


def test_curva_usa_os_parametros_informados_no_lugar_dos_de_referencia():
    curvas = lactation.lactation_curve({1: {"l": 10.0, "m": 0.2, "n": 0.003}}, days=10)

    assert set(curvas) == {1}
    assert curvas[1][4] == pytest.approx(lactation.wood_yield(5, 10.0, 0.2, 0.003))


def test_pico_e_o_maximo_da_curva_e_o_dia_conta_a_partir_de_1():
    dia, kg = lactation.peak([1.0, 3.0, 2.0])

    assert (dia, kg) == (2, 3.0)


def test_pico_da_curva_de_wood_cai_em_t_igual_m_sobre_n():
    # derivada de y(t) = 0 em t = m / n
    p = lactation.DEFAULT_WOOD[2]
    dia, _ = lactation.peak(lactation.lactation_curve({2: p})[2])

    assert dia == pytest.approx(p["m"] / p["n"], abs=1)


def test_leite_em_305_dias_soma_so_os_305_primeiros_dias():
    curva = [1.0] * 400

    assert lactation.milk_305(curva) == 305.0


def test_marcos_do_quadro_pev_60_gestacao_270_secagem_60():
    assert lactation.milestones() == {"pev": 60, "proximo_parto": 330, "secagem": 270}


def test_marcos_acompanham_os_parametros():
    assert lactation.milestones(pev_days=90, gestation_days=280, dry_off_days_before_calving=45) == {
        "pev": 90,
        "proximo_parto": 370,
        "secagem": 325,
    }


@pytest.mark.skipif(not RUFAS_INPUT.exists(), reason="vendor/RuFaS não está presente")
def test_parametros_de_referencia_batem_com_o_arquivo_de_entrada_do_rufas():
    """Se o RuFaS mudar a média ou os ajustes de paridade, o fallback da tela fica desatualizado e este teste avisa."""
    dados = json.loads(RUFAS_INPUT.read_text(encoding="utf-8"))
    media = dados["parameter_mean_values"]
    ajustes = dados["adjustments"]["parity"]
    # O RuFaS escala os ajustes de m por 1e-2 e os de n por 1e-4 (M_/N_ADJUSTMENT_SCALING_FACTOR).
    for paridade, a in ajustes.items():
        esperado = {
            "l": media["parameter_l_mean"] + a["l"],
            "m": media["parameter_m_mean"] + a["m"] * 1e-2,
            "n": media["parameter_n_mean"] + a["n"] * 1e-4,
        }
        assert lactation.DEFAULT_WOOD[int(paridade)] == pytest.approx(esperado)


def test_valores_de_referencia_ficam_na_faixa_de_uma_vaca_holandesa():
    for paridade, curva in lactation.lactation_curve(None).items():
        dia, pico = lactation.peak(curva)

        assert 30 <= pico <= 60, paridade
        assert 40 <= dia <= 120, paridade
        assert 8000 <= lactation.milk_305(curva) <= 15000, paridade


def test_parametros_da_curva_saem_do_resultado_do_rufas():
    saidas = {
        "arquivo.json": {
            f"AnimalModuleReporter.parity_{paridade}_lactation_curve_parameter__{letra}": {"values": [valor, valor + 1]}
            for paridade, parametros in {1: (15.0, 0.24, 0.0024), 2: (22.0, 0.23, 0.0036)}.items()
            for letra, valor in zip("lmn", parametros)
        }
    }

    wood = parse_outputs(saidas).wood

    # só o primeiro valor da série vale (o parâmetro ajustado no início da simulação)
    assert wood == {1: {"l": 15.0, "m": 0.24, "n": 0.0024}, 2: {"l": 22.0, "m": 0.23, "n": 0.0036}}
