import pandas as pd
import pytest


def test_ler_excel_arquivo_inexistente():
    from data.loader import _ler_excel
    with pytest.raises(FileNotFoundError):
        _ler_excel("arquivo_que_nao_existe.xlsx")