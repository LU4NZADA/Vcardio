import pandas as pd
import numpy as np


def _make_df_processado(n=20):
    from data.validators import verificar_colunas
    from data.preprocess import processar_dados
    df = pd.DataFrame({
        "Data_Nascimento": pd.date_range("1960-01-01", periods=n, freq="5Y"),
        "Data_cadastro": pd.date_range("2023-01-01", periods=n, freq="ME"),
        "Cidade": (["Teofilo Otoni"] * 10 + ["Diamantina"] * 10),
        "Sexo": (["Feminino", "Masculino"] * (n // 2)),
        "Hipertenso": [0, 1] * (n // 2),
        "Diabetes Mellitus": [1, 0] * (n // 2),
        "Tabagista": [0, 0] * n, "Etilista": [0] * n,
        "Ritmo sinusal": [1] * n, "Taquicardia sinusal": [0] * 18 + [1, 1],
    })
    return processar_dados(verificar_colunas(df))


def test_indicadores_chaves():
    from data.indicators import calcular_indicadores
    df = _make_df_processado()
    ind = calcular_indicadores(df)
    for k in ["n", "n_muns", "avg_age", "n_arr", "n_blk", "achados", "risco_municipio"]:
        assert k in ind


def test_n_correto():
    from data.indicators import calcular_indicadores
    df = _make_df_processado(20)
    ind = calcular_indicadores(df)
    assert ind["n"] == 20