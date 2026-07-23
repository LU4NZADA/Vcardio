"""
Transformacoes: idade, faixa, diag_cat, colunas temporais.
"""

import pandas as pd
from config.app import MESES_PT, BINS_IDADE, LABELS_IDADE
from analysis.classificacao import categorizar_diagnostico, classificar_achados


def processar_dados(df):
    df = df.copy()
    df["Data_Nascimento"] = pd.to_datetime(df["Data_Nascimento"], errors="coerce")
    df["Data_cadastro"] = pd.to_datetime(df["Data_cadastro"], errors="coerce")
    hoje = pd.Timestamp.now()
    df["idade"] = ((hoje - df["Data_Nascimento"]).dt.days / 365.25).round(0).astype("Int64")
    df["idade"] = df["idade"].fillna(0)
    df["Cidade"] = df["Cidade"].fillna("Nao informado").str.strip().str.title()
    df["Sexo"] = df["Sexo"].fillna("Nao especificado").str.strip()
    df.loc[df["Sexo"].str.contains("especificado", case=False, na=False), "Sexo"] = "Nao especificado"
    df["diag_cat"] = df.apply(categorizar_diagnostico, axis=1)
    df = classificar_achados(df)
    df["mes"] = df["Data_cadastro"].dt.to_period("M").dt.to_timestamp()
    df["ano"] = df["Data_cadastro"].dt.year
    df["mes_num"] = df["Data_cadastro"].dt.month
    df["mes_nome"] = df["mes_num"].map(MESES_PT)
    df["trimestre"] = "T" + ((df["Data_cadastro"].dt.month - 1) // 3 + 1).astype(str)
    df["faixa"] = pd.cut(df["idade"], bins=BINS_IDADE, labels=LABELS_IDADE, right=False)
    for col in ["Hipertenso", "Diabetes Mellitus", "Tabagista", "Etilista", "Marcapasso"]:
        df[col] = df[col].fillna(0).astype(int)
    return df