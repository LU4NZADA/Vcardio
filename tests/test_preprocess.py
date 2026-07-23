import pandas as pd


def _make_df_base(n=10):
    return pd.DataFrame({
        "Data_Nascimento": pd.date_range("1960-01-01", periods=n, freq="5Y"),
        "Data_cadastro": pd.date_range("2023-01-01", periods=n, freq="ME"),
        "Cidade": ["Teofilo Otoni"] * n,
        "Sexo": (["Feminino", "Masculino"] * (n // 2 + 1))[:n],
        "Hipertenso": [0, 1] * (n // 2),
        "Diabetes Mellitus": [0, 0] * (n // 2),
        "Tabagista": [0, 1] * (n // 2),
        "Etilista": [0] * n,
        "Ritmo sinusal": [1] * n,
    })


def test_idade_calculada():
    from data.validators import verificar_colunas
    from data.preprocess import processar_dados
    df = _make_df_base(5)
    df = verificar_colunas(df)
    resultado = processar_dados(df)
    assert "idade" in resultado.columns
    assert resultado["idade"].notna().all()


def test_diag_cat_atribuido():
    from data.validators import verificar_colunas
    from data.preprocess import processar_dados
    df = _make_df_base(5)
    df = verificar_colunas(df)
    resultado = processar_dados(df)
    assert "diag_cat" in resultado.columns


def test_colunas_temporais():
    from data.validators import verificar_colunas
    from data.preprocess import processar_dados
    df = _make_df_base(5)
    df = verificar_colunas(df)
    resultado = processar_dados(df)
    for col in ["mes", "ano", "mes_num", "mes_nome", "trimestre"]:
        assert col in resultado.columns