import pandas as pd
import numpy as np


def _make_df(n=200):
    np.random.seed(42)
    return pd.DataFrame({
        "idade": np.random.randint(20, 80, n),
        "Cidade": np.random.choice(["A", "B", "C"], n),
        "Sexo": np.random.choice(["Feminino", "Masculino"], n),
        "Hipertenso": np.random.choice([0, 1], n),
        "Diabetes Mellitus": np.random.choice([0, 1], n),
        "Tabagista": np.random.choice([0, 1], n),
        "Etilista": np.random.choice([0, 1], n),
        "diag_cat": np.random.choice(["Normal", "Arritmia", "Bloqueio de Ramo"], n, p=[0.5, 0.3, 0.2]),
        "ano": np.random.choice([2022, 2023, 2024], n),
    })


def test_prevalencia_geral():
    from epidemiology.prevalence import prevalencia_geral
    df = _make_df(100)
    r = prevalencia_geral(df)
    assert r["total"] == 100
    assert r["normais"] + r["alterados"] == 100


def test_prevalencia_por_grupo():
    from epidemiology.prevalence import prevalencia_por_grupo
    r = prevalencia_por_grupo(_make_df(200), "Sexo")
    assert len(r) == 2


def test_resumo_comorbidades():
    from epidemiology.comorbidades import resumo_comorbidades
    r = resumo_comorbidades(_make_df(200))
    assert len(r) == 4


def test_alertas():
    from epidemiology.alerts import gerar_alertas_epidemiologicos
    df = _make_df(200)
    ind = {"n": 200, "n_arr": 80, "n_blk": 40, "n_wpw": 2, "avg_age": 70, "n_muns": 3,
           "comorb_resumo": [("Hipertenso", "HAS", 120, 60.0)],
           "risco_municipio": pd.DataFrame({"Cidade": ["A"], "total": [100], "alterados": [80], "pct": [80.0]})}
    alertas = gerar_alertas_epidemiologicos(df, ind)
    assert len(alertas) > 0