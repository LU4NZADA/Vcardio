"""
Analise territorial.
"""

import pandas as pd
from config.app import COMORB_COLS
from constants import MUN_COORDS
from constants_locais import distrito_para_municipio


def risco_territorial(df, min_exames=1):
    """Risco territorial por municipio (local do exame)."""
    col = "Municipio_Coleta" if "Municipio_Coleta" in df.columns else "Cidade"
    risco = (df.groupby(col)
             .agg(total=("diag_cat", "count"),
                  alterados=("diag_cat", lambda x: (x != "Normal").sum()),
                  idade_media=("idade", "mean"))
             .reset_index())
    risco.rename(columns={col: "Cidade"}, inplace=True)
    risco = risco[risco["total"] >= min_exames].copy()
    risco["pct"] = (risco["alterados"] / risco["total"] * 100).round(1)
    risco["idade_media"] = risco["idade_media"].round(1)
    risco["lat"] = risco["Cidade"].map(lambda c: MUN_COORDS.get(c, (None, None))[0])
    risco["lon"] = risco["Cidade"].map(lambda c: MUN_COORDS.get(c, (None, None))[1])
    return risco.sort_values("pct", ascending=False)


def risco_territorial_distrito(df, min_exames=1):
    """Risco territorial por distrito (local do exame)."""
    df_d = df[df["Distrito"].ne("")].copy()
    if df_d.empty:
        return pd.DataFrame()

    risco = (df_d.groupby("Distrito")
             .agg(total=("diag_cat", "count"),
                  alterados=("diag_cat", lambda x: (x != "Normal").sum()),
                  idade_media=("idade", "mean"))
             .reset_index())
    risco = risco[risco["total"] >= min_exames].copy()
    risco["pct"] = (risco["alterados"] / risco["total"] * 100).round(1)
    risco["idade_media"] = risco["idade_media"].round(1)
    risco["Municipio"] = risco["Distrito"].map(distrito_para_municipio)
    risco["lat"] = risco["Municipio"].map(lambda c: MUN_COORDS.get(c, (None, None))[0])
    risco["lon"] = risco["Municipio"].map(lambda c: MUN_COORDS.get(c, (None, None))[1])
    return risco.sort_values("pct", ascending=False)


def classificar_municipios(risco_df):
    df = risco_df.copy()
    df["classificacao"] = df["pct"].apply(
        lambda p: "Critico" if p > 70 else "Alto" if p > 50 else "Moderado" if p > 30 else "Baixo")
    return df


def comorb_por_municipio(df, comorb_col, min_exames=1):
    col = "Municipio_Coleta" if "Municipio_Coleta" in df.columns else "Cidade"
    cm = (df.groupby(col)
          .agg(total=("diag_cat", "count"), positivos=(comorb_col, "sum")).reset_index())
    cm.rename(columns={col: "Cidade"}, inplace=True)
    cm = cm[cm["total"] >= min_exames].copy()
    cm["Pct"] = (cm["positivos"] / cm["total"] * 100).round(1)
    return cm.sort_values("Pct", ascending=False).head(12)