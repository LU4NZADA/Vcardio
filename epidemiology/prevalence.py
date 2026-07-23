"""
Prevalencias com IC 95%.
"""

import pandas as pd


def prevalencia_geral(df, col_diag="diag_cat"):
    n = len(df)
    if n == 0:
        return {"erro": "Amostra vazia"}
    alterados = (df[col_diag] != "Normal").sum()
    p = alterados / n
    se = (p * (1 - p) / n) ** 0.5
    return {
        "total": n, "normais": int(n - alterados), "alterados": int(alterados),
        "prev_geral": round(100 * p, 1),
        "ic_95_inf": round(100 * max(0, p - 1.96 * se), 1),
        "ic_95_sup": round(100 * min(1, p + 1.96 * se), 1),
    }


def prevalencia_por_grupo(df, col_grupo, col_diag="diag_cat"):
    rows = []
    for grupo, sub in df.groupby(col_grupo):
        n = len(sub)
        if n < 3:
            continue
        alt = (sub[col_diag] != "Normal").sum()
        p = alt / n
        se = (p * (1 - p) / n) ** 0.5
        rows.append({
            "Grupo": str(grupo), "N": n, "Alterados": int(alt),
            "Prevalencia": round(100 * p, 1),
            "IC_95_Inf": round(100 * max(0, p - 1.96 * se), 1),
            "IC_95_Sup": round(100 * min(1, p + 1.96 * se), 1),
        })
    return pd.DataFrame(rows)