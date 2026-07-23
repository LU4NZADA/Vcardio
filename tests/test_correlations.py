import pandas as pd
import numpy as np


def test_fatores_associados():
    from statistics.correlations import fatores_associados
    np.random.seed(42)
    df = pd.DataFrame({
        "diag_cat": np.random.choice(["Normal", "Arritmia"], 200),
        "Hipertenso": np.random.choice([0, 1], 200),
        "Diabetes Mellitus": np.random.choice([0, 1], 200),
    })
    r = fatores_associados(df)
    assert isinstance(r, pd.DataFrame)
    assert "Fator" in r.columns