"""Metano entérico e nitrogênio urinário como saídas da dieta: as equações lineares contra as funções originais do RuFaS."""

import numpy as np
import pytest

from dietopt.module import emissions
from dietopt.module.library import build_feeds

IDS = [23, 44, 50, 110, 138, 167, 230]
COW = {"body_weight": 650.0, "days_in_milk": 100, "milk_true_protein": 3.1, "milk_production": 40.0}


def feeds():
    return build_feeds("NASEM", IDS, {i: 0.2 for i in IDS}, {i: (0.0, 100.0) for i in IDS})


@pytest.mark.parametrize("animal_type", ["LAC_COW", "DRY_COW", "HEIFER_II", "HEIFER_III", "HEIFER_I"])
def test_equacoes_lineares_reproduzem_as_funcoes_originais_do_rufas(animal_type):
    fd = feeds()
    em = emissions.coefficients(fd, animal_type)
    rng = np.random.default_rng(7)
    for _ in range(12):
        x = rng.uniform(0.05, 14.0, len(IDS))  # consumo de 5 a 60 kg: bem acima dos pisos do RuFaS (2 kg)
        methane, urine = em.of_diet(x)
        original = emissions.of_diet_rufas(fd, x, animal_type, COW)
        assert methane == pytest.approx(original[0], rel=1e-9)
        assert urine == pytest.approx(original[1], rel=1e-9)


def test_metano_e_linear_nas_quantidades_e_nao_tem_constante():
    fd = feeds()
    em = emissions.coefficients(fd, "LAC_COW")
    x = np.array([0.1, 2.0, 11.5, 18.0, 0.8, 1.2, 0.4])
    assert em.of_diet(2 * x)[0] == pytest.approx(2 * em.of_diet(x)[0])  # homogêneo
    a, b = em.of_diet(x), em.of_diet(x + 1.0)
    assert (b[0] - a[0]) == pytest.approx(float(em.methane.sum()))  # o acréscimo é a soma dos coeficientes


def test_ordem_de_grandeza_de_uma_dieta_de_vaca_em_lactacao():
    x = np.array([0.1, 2.0, 11.5, 18.0, 0.8, 1.2, 0.4])  # 34 kg de MS
    methane, urine = emissions.coefficients(feeds(), "LAC_COW").of_diet(x)
    assert 600 < methane < 900 and 0.2 < urine < 0.4  # g/dia e kg/dia; a simulação do RuFaS dá cerca de 705 g e 0,25 kg


def test_piso_do_rufas_no_nitrogenio_urinario_so_vale_em_consumo_muito_baixo():
    fd = feeds()
    pouco = np.array([0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0])  # 0,2 kg de MS: abaixo dos pisos de consumo do RuFaS
    _, urine_rufas = emissions.of_diet_rufas(fd, pouco, "LAC_COW", COW)
    assert urine_rufas == pytest.approx(0.022)  # o piso de 22 g
    assert emissions.coefficients(fd, "LAC_COW").of_diet(pouco)[1] != pytest.approx(0.022)


def test_valores_de_partida_do_usuario():
    assert (emissions.DEFAULT_METHANE_G, emissions.DEFAULT_URINE_N_KG) == (450.0, 0.25)
