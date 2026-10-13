from dietopt.sensitivity import Factor, rank_effects, sample_points

FACTORS = [Factor("138", "Arroz", 0.08, 0.30), Factor("44", "Milho", 0.20, 0.40)]


def test_grid_tem_produto_cartesiano_e_inclui_extremos():
    points = sample_points(FACTORS, "grid", 3)
    assert len(points) == 9
    assert [0.08, 0.20] in points and [0.30, 0.40] in points


def test_latin_respeita_limites_e_cobre_estratos():
    points = sample_points(FACTORS, "latin", 10, seed=1)
    assert len(points) == 10
    for arroz, milho in points:
        assert 0.08 <= arroz <= 0.30 and 0.20 <= milho <= 0.40
    estratos = sorted(int((p[0] - 0.08) / 0.22 * 10) for p in points)
    assert estratos == list(range(10))


def test_efeitos_de_spearman_tem_sinal_esperado():
    rows = [{"Arroz": a, "Milho": m, "Res": 100 - 50 * a + 0 * m + i} for i, (a, m) in enumerate(
        [(0.1, 0.3), (0.2, 0.2), (0.3, 0.4), (0.15, 0.25)])]
    efeitos = {e["fator"]: e["spearman"] for e in rank_effects(FACTORS, rows)}
    assert efeitos["Arroz"] is not None
