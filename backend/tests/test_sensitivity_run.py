"""Análise de sensibilidade: tamanho e limites, cache de simulações, receita pelo preço do leite, falhas, efeitos e cancelamento."""

import pytest

from dietopt import sensitivity
from dietopt.jobs import Cancelled
from dietopt.rufas_adapter import Scenario
from dietopt.scenarios import Economics, Evaluation
from dietopt.sensitivity import (
    MAX_LEVELS,
    MAX_SAMPLES,
    MAX_SIMULATIONS,
    Factor,
    check_plan,
    plan_size,
    rank_effects,
    run_sensitivity,
)

ARROZ = Factor("138", "Arroz", 0.10, 0.30)
MILHO = Factor("44", "Milho", 0.20, 0.40)
LEITE = Factor("milk_price", "Leite", 0.40, 0.60)
BASE = Scenario(name="base", feed_prices={138: 0.2, 44: 0.3})
ECONOMICS = Economics(milk_price=0.5)


class SimulacaoFalsa:
    """Substitui ``evaluate_many``: leite fixo, custo = soma dos preços dos alimentos × 1000 (e falha se pedido)."""

    def __init__(self, falhar_quando=lambda scenario: False):
        self.cenarios = []
        self.falhar_quando = falhar_quando

    def __call__(self, scenarios, economics, workers=2):
        resultado = []
        for scenario in scenarios:
            self.cenarios.append(scenario)
            if self.falhar_quando(scenario):
                resultado.append(Evaluation(name=scenario.name, ok=False, seconds=0.0, detail="RuFaS falhou"))
                continue
            custo = 1000 * sum(scenario.feed_prices.values())
            resultado.append(
                Evaluation(name=scenario.name, ok=True, seconds=0.0, milk_kg=10_000.0, feed_cost=custo, ration={"138": 5.0, "44": 0.0})
            )
        return resultado


@pytest.fixture
def simulacao(monkeypatch):
    falsa = SimulacaoFalsa()
    monkeypatch.setattr(sensitivity, "evaluate_many", falsa)
    return falsa


# ---------------------------------------------------------------------------------------------------- tamanho
def test_tamanho_da_grade_e_n_elevado_ao_numero_de_fatores():
    assert plan_size(n_feed_factors=2, n_factors=3, method="grid", n=4) == (64, 16)


def test_preco_do_leite_nao_gera_simulacao_nova():
    assert plan_size(n_feed_factors=0, n_factors=1, method="grid", n=5) == (5, 1)
    assert plan_size(n_feed_factors=0, n_factors=1, method="latin", n=7) == (7, 1)


def test_hipercubo_latino_faz_uma_simulacao_por_amostra_quando_ha_alimento():
    assert plan_size(n_feed_factors=2, n_factors=3, method="latin", n=10) == (10, 10)


def test_sem_fatores_nao_ha_cenarios():
    assert plan_size(0, 0, "grid", 3) == (0, 0)


def test_analise_pequena_passa_na_validacao():
    assert check_plan([ARROZ, MILHO, LEITE], "grid", 3) == (27, 9)


def test_analise_enorme_e_recusada_antes_de_montar_os_cenarios():
    fatores = [Factor(str(i), f"Alimento {i}", 0.1, 0.2) for i in range(8)]

    with pytest.raises(ValueError, match=f"limite é {MAX_SIMULATIONS}"):
        check_plan(fatores, "grid", MAX_LEVELS)


def test_so_o_preco_do_leite_cabe_com_qualquer_numero_de_niveis():
    assert check_plan([LEITE], "grid", MAX_LEVELS) == (MAX_LEVELS, 1)


def test_um_alimento_e_o_leite_com_12_niveis_ainda_cabem_mas_dois_alimentos_nao():
    assert check_plan([ARROZ, LEITE], "grid", MAX_LEVELS) == (144, 12)

    with pytest.raises(ValueError, match="simulações"):
        check_plan([ARROZ, MILHO, LEITE], "grid", MAX_LEVELS)  # 12² = 144 simulações


@pytest.mark.parametrize("n", [0, 1, MAX_LEVELS + 1, 2.5e9])
def test_niveis_fora_da_faixa_da_grade_sao_recusados(n):
    with pytest.raises(ValueError, match="níveis"):
        check_plan([ARROZ], "grid", n)


def test_amostras_do_hipercubo_latino_chegam_a_100():
    assert check_plan([ARROZ], "latin", MAX_SAMPLES) == (MAX_SAMPLES, MAX_SAMPLES)

    with pytest.raises(ValueError, match="amostras"):
        check_plan([ARROZ], "latin", MAX_SAMPLES + 1)


def test_metodo_desconhecido_sem_fator_e_fator_repetido_sao_recusados():
    with pytest.raises(ValueError, match="Método"):
        check_plan([ARROZ], "sobol", 3)
    with pytest.raises(ValueError, match="ao menos um fator"):
        check_plan([], "grid", 3)
    with pytest.raises(ValueError, match="repetidos"):
        check_plan([ARROZ, Factor("139", "Arroz", 0.1, 0.2)], "grid", 3)


def test_run_sensitivity_recusa_antes_de_simular(simulacao):
    fatores = [Factor(str(i), f"Alimento {i}", 0.1, 0.2) for i in range(8)]

    with pytest.raises(ValueError):
        run_sensitivity(BASE, fatores, ECONOMICS, method="grid", n=MAX_LEVELS)

    assert simulacao.cenarios == []


# ---------------------------------------------------------------------------------------------------- execução
def test_so_preco_do_leite_roda_uma_simulacao_e_recalcula_a_receita(simulacao):
    saida = run_sensitivity(BASE, [LEITE], ECONOMICS, method="grid", n=3)

    assert len(simulacao.cenarios) == 1
    receitas = [row["receita"] for row in saida["rows"]]
    assert receitas == [4000.0, 5000.0, 6000.0]  # 10.000 kg × 0,40 / 0,50 / 0,60
    custo = saida["rows"][0]["custo_alimentacao"]
    assert [row["Res"] for row in saida["rows"]] == [4000.0 - custo, 5000.0 - custo, 6000.0 - custo]


def test_cada_combinacao_de_precos_de_alimentos_vira_uma_simulacao(simulacao):
    saida = run_sensitivity(BASE, [ARROZ, MILHO, LEITE], ECONOMICS, method="grid", n=2)

    assert len(saida["rows"]) == 8
    assert len(simulacao.cenarios) == 4  # o leite não multiplica as simulações
    precos = {(s.feed_prices[138], s.feed_prices[44]) for s in simulacao.cenarios}
    assert precos == {(0.1, 0.2), (0.1, 0.4), (0.3, 0.2), (0.3, 0.4)}


def test_precos_dos_demais_alimentos_ficam_como_na_base(simulacao):
    base = Scenario(name="base", feed_prices={138: 0.2, 44: 0.3, 99: 0.7})

    run_sensitivity(base, [ARROZ], ECONOMICS, method="grid", n=2)

    assert all(s.feed_prices[99] == 0.7 and s.feed_prices[44] == 0.3 for s in simulacao.cenarios)


def test_colunas_seguem_a_ordem_dos_fatores_e_terminam_em_res(simulacao):
    saida = run_sensitivity(BASE, [ARROZ, LEITE], ECONOMICS, method="grid", n=2)

    assert saida["columns"] == ["Arroz", "Leite", "Res"]
    assert {"cenario", "Arroz", "Leite", "Res", "leite_kg", "receita", "custo_alimentacao", "ration"} <= set(saida["rows"][0])
    assert saida["rows"][0]["ration"] == {"138": 5.0}  # alimentos com 0 kg não aparecem


def test_cenario_que_falha_vira_res_nulo_com_o_motivo_e_nao_zero(monkeypatch):
    falsa = SimulacaoFalsa(falhar_quando=lambda scenario: scenario.feed_prices[138] > 0.2)
    monkeypatch.setattr(sensitivity, "evaluate_many", falsa)

    saida = run_sensitivity(BASE, [ARROZ], ECONOMICS, method="grid", n=2)

    ok, falhou = saida["rows"]
    assert ok["Res"] is not None
    assert falhou["Res"] is None and falhou["erro"] == "RuFaS falhou" and "receita" not in falhou


def test_progresso_conta_simulacoes_nao_cenarios(simulacao):
    visto = []

    run_sensitivity(BASE, [ARROZ, MILHO, LEITE], ECONOMICS, method="grid", n=2, workers=2, on_progress=lambda d, t: visto.append((d, t)))

    assert visto == [(2, 4), (4, 4)]


def test_cancelar_para_antes_do_proximo_lote(simulacao):
    pedidos = iter([False, True])

    with pytest.raises(Cancelled):
        run_sensitivity(BASE, [ARROZ, MILHO], ECONOMICS, method="grid", n=2, workers=2, should_cancel=lambda: next(pedidos))

    assert len(simulacao.cenarios) == 2  # só o primeiro lote rodou


# ---------------------------------------------------------------------------------------------------- efeitos
def linhas(pares):
    return [{"Arroz": a, "Leite": m, "Res": res} for a, m, res in pares]


def test_variacao_em_dolares_e_o_efeito_do_minimo_ao_maximo_da_faixa():
    # grade 2×2: o arroz de 0,1 a 0,3 tira 100 da margem; o leite de 0,4 a 0,6 põe 500
    rows = linhas([(0.1, 0.4, 1000), (0.1, 0.6, 1500), (0.3, 0.4, 900), (0.3, 0.6, 1400)])

    efeitos = {e["fator"]: e for e in rank_effects([ARROZ, LEITE], rows)}

    assert efeitos["Arroz"]["swing"] == pytest.approx(-100.0)
    assert efeitos["Leite"]["swing"] == pytest.approx(500.0)
    assert efeitos["Leite"]["swing_pct"] == pytest.approx(100 * 500 / 1200, abs=0.01)


def test_spearman_pode_ser_forte_mesmo_quando_o_efeito_em_dolares_e_minusculo():
    # o caso que motivou a variação em US$: o milho tem correlação -1, mas muda a margem em 0,01%
    rows = [{"Milho": 0.2 + 0.1 * i, "Res": 100_000 - 5 * i} for i in range(3)]

    (efeito,) = rank_effects([MILHO], rows)

    assert efeito["spearman"] == -1.0
    assert abs(efeito["swing_pct"]) < 0.02


def test_fator_que_nao_variou_fica_sem_efeito():
    rows = [{"Arroz": 0.2, "Res": 100.0}, {"Arroz": 0.2, "Res": 110.0}, {"Arroz": 0.2, "Res": 120.0}]

    (efeito,) = rank_effects([ARROZ], rows)

    assert efeito == {"fator": "Arroz", "spearman": None, "swing": None, "swing_pct": None}


def test_cenarios_que_falharam_nao_entram_nos_efeitos():
    rows = [{"Arroz": 0.1, "Res": 100.0}, {"Arroz": 0.2, "Res": None}, {"Arroz": 0.3, "Res": 80.0}]

    (efeito,) = rank_effects([ARROZ], rows)

    assert efeito["swing"] == pytest.approx(-20.0)
    assert efeito["spearman"] is None  # só 2 válidos: pouco para a correlação
