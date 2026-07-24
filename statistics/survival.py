"""
Analises temporais e tendencias.
"""

import pandas as pd
import numpy as np
try:
    try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def tendencia_temporal(df, col_periodo="mes", col_diag="diag_cat"):
    mensal = (df.groupby(col_periodo)
              .apply(lambda g: round(100 * (g[col_diag] != "Normal").mean(), 1))
              .reset_index(name="pct"))
    if len(mensal) < 3:
        return {"erro": "Minimo 3 periodos"}
    x = np.arange(len(mensal))
    y = mensal["pct"].values
    slope, intercept, r, p, se = stats.linregress(x, y)
    tendencia = "crescente" if slope > 0 and p < 0.05 else "decrescente" if slope < 0 and p < 0.05 else "estavel"
    return {
        "tendencia": tendencia, "inclinacao": round(slope, 3),
        "r_quadrado": round(r**2, 4), "p_valor": round(p, 6),
        "significativo": p < 0.05, "periodos": len(mensal),
        "variacao_absoluta": round(y[-1] - y[0], 1),
    }


def taxa_incidencia_periodo(df, col_periodo="ano", col_diag="diag_cat"):
    rows = []
    for periodo, grupo in df.groupby(col_periodo):
        n_total = len(grupo)
        n_alt = (grupo[col_diag] != "Normal").sum()
        rows.append({
            "Periodo": periodo, "N": n_total,
            "Taxa_alteracao": round(1000 * n_alt / n_total, 2) if n_total else 0,
        })
    return pd.DataFrame(rows)