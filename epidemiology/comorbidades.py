"""
Analise epidemiologica de comorbidades.
"""

import pandas as pd
from config.app import COMORB_COLS


def resumo_comorbidades(df):
    n = len(df)
    resultado = []
    for ccol, label in COMORB_COLS.items():
        if ccol in df.columns:
            total = int(df[ccol].sum())
            pct = round(100 * total / n, 1) if n else 0
            resultado.append((ccol, label, total, pct))
    return resultado


def comorb_por_sexo(df):
    rows = []
    for ccol, label in COMORB_COLS.items():
        if ccol not in df.columns:
            continue
        for sexo in ["Feminino", "Masculino"]:
            sub = df[df["Sexo"] == sexo]
            if len(sub) > 0:
                rows.append({"Comorbidade": label, "Sexo": sexo, "Pct": round(100 * sub[ccol].mean(), 1)})
    return pd.DataFrame(rows)


def comorb_por_faixa(df):
    rows = []
    for ccol, label in COMORB_COLS.items():
        if ccol not in df.columns:
            continue
        for fx in sorted(df["faixa"].dropna().unique()):
            sub = df[df["faixa"] == fx]
            if len(sub) >= 5:
                rows.append({"Faixa": str(fx), "Comorbidade": label, "Pct": round(100 * sub[ccol].mean(), 1)})
    return pd.DataFrame(rows)