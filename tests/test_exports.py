import pandas as pd


def test_csv_bytes():
    from exports.csv import gerar_csv
    tabela = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    r = gerar_csv(tabela)
    assert isinstance(r, bytes)
    assert len(r) > 0


def test_excel_bytes():
    from exports.excel import gerar_excel
    tabela = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    ind = {"n": 2, "n_muns": 1, "avg_age": 40, "n_arr": 0, "n_blk": 0, "alt_pct": 50.0}
    r = gerar_excel(tabela, ind)
    assert isinstance(r, bytes)
    assert len(r) > 100