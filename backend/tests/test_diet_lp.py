"""Reproduz o exercício do quadro: dieta de arroz e milho (carboidratos e proteína)."""

import math

from dietopt.diet_lp import Food, NutrientBounds, solve_diet

FOODS = [
    Food("arroz", 1.50, {"carboidrato": 0.77, "proteina": 0.08}),
    Food("milho", 2.23, {"carboidrato": 0.66, "proteina": 0.14}),
]
BOUNDS = {
    "carboidrato": NutrientBounds(6.0, 9.5),
    "proteina": NutrientBounds(0.9, 1.6),
}


def test_otimo_do_quadro():
    result = solve_diet(FOODS, BOUNDS)
    assert result.feasible
    assert math.isclose(result.cost, 15.3453, abs_tol=1e-3)
    assert math.isclose(result.amounts["arroz"], 4.473, abs_tol=1e-3)
    assert math.isclose(result.amounts["milho"], 3.873, abs_tol=1e-3)
    # mínimos ativos, máximos folgados
    assert math.isclose(result.nutrient_totals["carboidrato"], 6.0, abs_tol=1e-6)
    assert math.isclose(result.nutrient_totals["proteina"], 0.9, abs_tol=1e-6)


def test_preco_sombra_do_minimo_de_proteina_e_positivo():
    result = solve_diet(FOODS, BOUNDS)
    assert result.shadow_prices["proteina_min"] > 0
    assert result.shadow_prices["carboidrato_min"] > 0


def test_inviavel_quando_maximo_menor_que_minimo():
    result = solve_diet(FOODS, {"carboidrato": NutrientBounds(6.0, 5.0)})
    assert not result.feasible
