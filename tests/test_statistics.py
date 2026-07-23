import pandas as pd
import numpy as np


def test_resumo_completo():
    from statistics.descriptive import resumo_completo
    s = pd.Series([10, 20, 30, 40, 50])
    r = resumo_completo(s, "Teste")
    assert r["n"] == 5
    assert r["media"] == 30.0


def test_comparar_medias():
    from statistics.descriptive import comparar_medias
    np.random.seed(42)
    s1 = pd.Series(np.random.normal(60, 10, 100))
    s2 = pd.Series(np.random.normal(40, 10, 100))
    r = comparar_medias(s1, s2)
    assert r["significativo_005"] is True