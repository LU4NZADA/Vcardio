"""
Scores de risco cardiovascular.
"""

import pandas as pd


def score_risco_individual(row):
    score = 0
    idade = row.get("idade", 0)
    if pd.notna(idade):
        if idade >= 75:
            score += 3
        elif idade >= 60:
            score += 2
        elif idade >= 50:
            score += 1
    if row.get("Hipertenso", 0) == 1:
        score += 2
    if row.get("Diabetes Mellitus", 0) == 1:
        score += 1
    if row.get("Tabagista", 0) == 1:
        score += 1
    if row.get("Etilista", 0) == 1:
        score += 1
    diag = row.get("diag_cat", "")
    if diag == "Arritmia":
        score += 2
    elif diag == "Bloqueio de Ramo":
        score += 1
    elif diag in ("Alteracao de Repolarizacao", "Sobrecarga Ventricular"):
        score += 1
    return min(score, 10)


def classificar_risco(score):
    if score <= 2:
        return "Baixo"
    elif score <= 5:
        return "Moderado"
    elif score <= 7:
        return "Alto"
    return "Muito Alto"


def calcular_scores(df):
    df = df.copy()
    df["score_risco"] = df.apply(score_risco_individual, axis=1)
    df["class_risco"] = df["score_risco"].apply(classificar_risco)
    return df


def score_municipal(df, min_exames=5):
    mun = (df.groupby("Cidade")
           .agg(total=("diag_cat", "count"),
                alterados=("diag_cat", lambda x: (x != "Normal").sum()),
                idade_media=("idade", "mean"),
                pct_hip=("Hipertenso", "mean"),
                pct_diab=("Diabetes Mellitus", "mean"))
           .reset_index())
    mun = mun[mun["total"] >= min_exames].copy()
    mun["pct_alt"] = (mun["alterados"] / mun["total"] * 100).round(1)
    mun["score_mun"] = (
        mun["pct_alt"] * 0.5 + mun["pct_hip"] * 100 * 0.2 +
        mun["pct_diab"] * 100 * 0.15 + mun["idade_media"] / 100 * 50 * 0.15
    ).round(1)
    return mun.sort_values("score_mun", ascending=False)