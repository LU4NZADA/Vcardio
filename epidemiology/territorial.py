"""
Analise territorial.
"""

import pandas as pd
from config.app import COMORB_COLS
from constants import MUN_COORDS


def risco_territorial(df, min_exames=1):
    risco = (df.groupby("Cidade")
             .agg(total=("diag_cat", "count"),
                  alterados=("diag_cat", lambda x: (x != "Normal").sum()),
                  idade_media=("idade", "mean"))
             .reset_index())
    risco = risco[risco["total"] >= min_exames].copy()
    risco["pct"] = (risco["alterados"] / risco["total"] * 100).round(1)
    risco["idade_media"] = risco["idade_media"].round(1)
    risco["lat"] = risco["Cidade"].map(lambda c: MUN_COORDS.get(c, (None, None))[0])
    risco["lon"] = risco["Cidade"].map(lambda c: MUN_COORDS.get(c, (None, None))[1])
    return risco.sort_values("pct", ascending=False)


def classificar_municipios(risco_df):
    df = risco_df.copy()
    df["classificacao"] = df["pct"].apply(
        lambda p: "Critico" if p > 70 else "Alto" if p > 50 else "Moderado" if p > 30 else "Baixo")
    return df


def comorb_por_municipio(df, comorb_col, min_exames=1):
    cm = (df.groupby("Cidade")
          .agg(total=("diag_cat", "count"), positivos=(comorb_col, "sum")).reset_index())
    cm = cm[cm["total"] >= min_exames].copy()
    cm["Pct"] = (cm["positivos"] / cm["total"] * 100).round(1)
    return cm.sort_values("Pct", ascending=False).head(12)