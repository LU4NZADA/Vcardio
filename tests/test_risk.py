import pandas as pd


def test_risco_filtro_minimo():
    from epidemiology.territorial import risco_territorial
    df = pd.DataFrame({"Cidade": ["A"] * 10 + ["B"] * 3,
                        "diag_cat": ["Normal"] * 5 + ["Arritmia"] * 5 + ["Normal"] * 3})
    r = risco_territorial(df, min_exames=5)
    assert len(r) == 1


def test_risco_calculo():
    from epidemiology.territorial import risco_territorial
    df = pd.DataFrame({"Cidade": ["X"] * 10,
                        "diag_cat": ["Normal"] * 3 + ["Arritmia"] * 7})
    r = risco_territorial(df, min_exames=1)
    assert r.iloc[0]["pct"] == 70.0