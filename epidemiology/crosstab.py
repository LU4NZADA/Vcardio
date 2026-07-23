"""
Cruzamentos: achado x variavel.
"""

import pandas as pd
from analysis.ecg import achado_mask


def matrix_achado_var(df, subcats, var_col):
    var_vals = sorted(df[var_col].dropna().unique())
    rows = []
    for nome, cols in subcats.items():
        mask = achado_mask(df, cols)
        sub = df[mask]
        if len(sub) >= 2:
            row = {"Achado": nome}
            for v in var_vals:
                row[str(v)] = int((sub[var_col] == v).sum())
            rows.append(row)
    return pd.DataFrame(rows).set_index("Achado") if rows else pd.DataFrame()


def prev_comorb_por_achado(df, subcats, comorb_cols_map):
    rows = []
    for nome, cols in subcats.items():
        mask = achado_mask(df, cols)
        sub = df[mask]
        if len(sub) >= 3:
            row = {"Achado": nome, "N": len(sub)}
            for ccol in comorb_cols_map:
                if ccol in sub.columns:
                    row[comorb_cols_map[ccol]] = round(100 * sub[ccol].mean(), 1)
            rows.append(row)
    return pd.DataFrame(rows).set_index("Achado") if rows else pd.DataFrame()