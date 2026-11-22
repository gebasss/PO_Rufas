"""Relatório de uma página (``dietopt.benchmark_report``): formatação e geração a partir dos resultados já gravados."""

import pytest

from dietopt import benchmark_report as rep


def test_numero_em_formato_brasileiro_com_sinal_de_menos_tipografico():
    assert rep.pt(-0.0054, 3, True) == "−0,005"
    assert rep.pt(0.1, 1, True) == "+0,1"
    assert rep.pt(None) == "n/d" and rep.pt(float("nan")) == "n/d"
    assert rep.thousands(4460.4) == "4.460"


def test_veredito_pre_definido_exige_o_ic_e_a_fracao_dentro_da_margem():
    ok = {"ci90": [-0.07, 0.07], "share_within_margin": 0.96}
    assert rep.verdict(ok) == "EQUIVALENTE"
    assert rep.verdict({**ok, "share_within_margin": 0.933}) == "EQUIVALÊNCIA NÃO DEMONSTRADA"
    assert rep.verdict({**ok, "ci90": [-0.2, 0.7]}) == "NÃO EQUIVALENTE"


def test_colunas_pulam_vazios_e_casos_sem_solucao():
    rows = [{"status": "ok", "x": "1.5"}, {"status": "ok", "x": ""}, {"status": "infeasible", "x": "9"}]
    assert rep.floats(rows, "x") == [1.5]
    assert rep.floats(rows, "x", only_ok=False) == [1.5, 9.0]


def test_pagina_e_gerada_dos_resultados_gravados(tmp_path):
    if not (rep.DOCS / "v4" / "resumo.json").exists() or not (rep.DOCS / "simulacao" / "resumo.json").exists():
        pytest.skip("resultados do benchmark ausentes")
    paths = rep.write(tmp_path / "pagina")
    assert [p.suffix for p in paths] == [".pdf", ".png"] and all(p.stat().st_size > 10_000 for p in paths)
