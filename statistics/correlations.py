"""
Correlacoes estatisticas.
"""

import pandas as pd
import numpy as np



def matriz_correlacao_comorb(df, cols_comorb, col_diag="diag_cat"):
    dummies = pd.get_dummies(df[col_diag], prefix="diag")
    binarias = df[cols_comorb].join(dummies)
    n = len(binarias)
    colunas = binarias.columns.tolist()
    matriz = pd.DataFrame(np.eye(len(colunas)), index=colunas, columns=colunas)
    for i, c1 in enumerate(colunas):
        for j, c2 in enumerate(colunas):
            if i >= j:
                continue
            tab = pd.crosstab(binarias[c1], binarias[c2])
            if tab.shape == (2, 2):
                chi2 = stats.chi2_contingency(tab)[0]
                phi = np.sqrt(chi2 / n) if n > 0 else 0
                conjunta = ((binarias[c1] == 1) & (binarias[c2] == 1)).sum()
                esperada = (binarias[c1].sum() * binarias[c2].sum()) / n
                sinal = 1 if conjunta >= esperada else -1
                matriz.loc[c1, c2] = round(phi * sinal, 3)
                matriz.loc[c2, c1] = round(phi * sinal, 3)
    return matriz


def fatores_associados(df, col_alterado="diag_cat", cols_fatores=None):
    df = df.copy()
    df["_alterado"] = (df[col_alterado] != "Normal").astype(int)
    if cols_fatores is None:
        cols_fatores = [c for c in ["Hipertenso", "Diabetes Mellitus", "Tabagista", "Etilista"] if c in df.columns]
    rows = []
    for col in cols_fatores:
        tab = pd.crosstab(df["_alterado"], df[col])
        if tab.shape == (2, 2):
            chi2, p, _, _ = stats.chi2_contingency(tab)
            n = len(df)
            v = np.sqrt(chi2 / n) if n > 0 else 0
            rows.append({
                "Fator": col,
                "Pct_Alterados": round(df[df["_alterado"]==1][col].mean()*100, 1),
                "Pct_Normais": round(df[df["_alterado"]==0][col].mean()*100, 1),
                "Qui2": round(chi2, 2), "p": round(p, 4),
                "V_Cramer": round(v, 3),
                "Significativo": "Sim" if p < 0.05 else "Nao",
            })
    return pd.DataFrame(rows).sort_values("p").reset_index(drop=True)