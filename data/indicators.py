"""
Calcula todos os indicadores de uma unica vez.
"""

import pandas as pd
from config.app import MESES_PT, COMORB_COLS
from constants import ECG_ACHADOS
from analysis.ecg import achado_mask, contar_achado, achados_df
from epidemiology.crosstab import matrix_achado_var, prev_comorb_por_achado
from epidemiology.comorbidades import resumo_comorbidades, comorb_por_sexo, comorb_por_faixa
from epidemiology.territorial import risco_territorial, comorb_por_municipio


def _value_counts_rename(series, col_nome, col_valor="Qtd", sort_index=False, head=None):
    """value_counts compativel com pandas 2.x e 3.x."""
    vc = series.value_counts()
    if sort_index:
        vc = vc.sort_index()
    if head:
        vc = vc.head(head)
    df = vc.reset_index()
    df.columns = [col_nome, col_valor]
    return df


def calcular_indicadores(df):
    ind = {}
    n = len(df)
    ind["n"] = n
    ind["n_muns"] = df["Cidade"].nunique()
    ind["avg_age"] = round(df["idade"].mean(), 1) if n else 0
    ind["alt_pct"] = round(100 * (df["diag_cat"] != "Normal").mean(), 1) if n else 0

    _all = lambda cat: [c for cols in ECG_ACHADOS[cat].values() for c in cols]
    ind["n_arr"] = contar_achado(df, _all("Arritmias"))
    ind["n_blk"] = contar_achado(df, _all("Bloqueios"))
    ind["n_sobr"] = contar_achado(df, _all("Sobrecargas"))
    ind["n_repo"] = contar_achado(df, _all("Repolarizacao"))
    ind["n_fibr"] = contar_achado(df, _all("Fibroses"))
    ind["n_pr"] = contar_achado(df, ["PR curto"])
    ind["n_wpw"] = contar_achado(df, ["Wolff-Parkinson-White"])
    ind["n_marc"] = contar_achado(df, ["Marcapasso", "Ritmo de marcapasso"])

    ind["sexo_counts"] = _value_counts_rename(df["Sexo"], "Sexo")
    ind["ano_counts"] = _value_counts_rename(df["ano"], "Ano", sort_index=True)
    ind["faixa_counts"] = _value_counts_rename(df["faixa"], "Faixa", sort_index=True)
    ind["diag_counts"] = _value_counts_rename(df["diag_cat"], "Diagnostico")
    ind["top_municipios"] = _value_counts_rename(df["Cidade"], "Municipio", head=15)

    saz = df.groupby("mes_nome").size().reset_index(name="Qtd")
    saz["ord"] = saz["mes_nome"].map({v: k for k, v in MESES_PT.items()})
    ind["sazonalidade"] = saz.sort_values("ord")

    piram = (df[df["Sexo"].isin(["Feminino", "Masculino"])]
             .groupby(["faixa", "Sexo"], observed=True).size().reset_index(name="Qtd"))
    piram["Val"] = piram.apply(lambda r: -r["Qtd"] if r["Sexo"] == "Masculino" else r["Qtd"], axis=1)
    ind["piramide"] = piram

    ind["achados"] = {}
    for cat, subcats in ECG_ACHADOS.items():
        ind["achados"][cat] = achados_df(df, subcats)

    sub_arr = ECG_ACHADOS["Arritmias"]
    sub_blk = ECG_ACHADOS["Bloqueios"]
    ind["arr_por_sexo"] = matrix_achado_var(df, sub_arr, "Sexo")
    ind["arr_por_faixa"] = matrix_achado_var(df, sub_arr, "faixa")
    ind["arr_comorb_prev"] = prev_comorb_por_achado(df, sub_arr, COMORB_COLS)
    ind["blk_por_sexo"] = matrix_achado_var(df, sub_blk, "Sexo")
    ind["blk_por_faixa"] = matrix_achado_var(df, sub_blk, "faixa")
    ind["blk_comorb_prev"] = prev_comorb_por_achado(df, sub_blk, COMORB_COLS)

    ind["comorb_resumo"] = resumo_comorbidades(df)
    ind["comorb_sexo"] = comorb_por_sexo(df)
    ind["comorb_faixa"] = comorb_por_faixa(df)
    ind["sexo_diag_crosstab"] = pd.crosstab(
        df["Sexo"], df["diag_cat"], normalize="index"
    ).round(3) * 100

    tempo = df.groupby(["mes", "diag_cat"]).size().reset_index(name="Qtd")
    tempo["Mes"] = tempo["mes"].dt.strftime("%b/%y")
    ind["temporal_mensal"] = tempo

    taxa = (df.groupby("mes")
            .apply(lambda g: round(100 * (g["diag_cat"] != "Normal").mean(), 1),
                   include_groups=False)
            .reset_index(name="Pct_Alterados"))
    taxa["Mes"] = taxa["mes"].dt.strftime("%b/%y")
    ind["taxa_alteracao"] = taxa

    ind["risco_municipio"] = risco_territorial(df)
    mapa = ind["risco_municipio"].copy()
    mapa.rename(columns={"total": "exames"}, inplace=True)
    ind["mapa_dados"] = mapa

    todos_cols = {}
    for cat, subcats in ECG_ACHADOS.items():
        for nome in subcats:
            c = f"_ach_{nome}"
            if c in df.columns and df[c].sum() > 0:
                todos_cols[nome] = c
    ind["todos_achados_cols"] = todos_cols

    hm_data = []
    for nome, col_name in todos_cols.items():
        for fx in sorted(df["faixa"].dropna().unique()):
            sub = df[df["faixa"] == fx]
            cnt = int(sub[col_name].sum())
            if cnt > 0:
                hm_data.append({"Achado": nome, "Faixa": str(fx), "N": cnt})
    ind["hm_achado_faixa"] = (
        pd.DataFrame(hm_data).pivot(index="Achado", columns="Faixa", values="N").fillna(0)
        if hm_data else pd.DataFrame()
    )

    hm_sex = []
    for nome, col_name in todos_cols.items():
        for sexo in ["Feminino", "Masculino"]:
            sub = df[df["Sexo"] == sexo]
            cnt = int(sub[col_name].sum())
            if cnt > 0:
                hm_sex.append({"Achado": nome, "Sexo": sexo, "N": cnt})
    ind["hm_achado_sexo"] = (
        pd.DataFrame(hm_sex).pivot(index="Achado", columns="Sexo", values="N").fillna(0)
        if hm_sex else pd.DataFrame()
    )

    hm_comorb = []
    for nome, col_name in todos_cols.items():
        sub = df[df[col_name] == 1]
        if len(sub) >= 3:
            row = {"Achado": nome, "N": len(sub)}
            for ccol, label in COMORB_COLS.items():
                if ccol in sub.columns:
                    row[label] = round(100 * sub[ccol].mean(), 1)
            hm_comorb.append(row)
    ind["hm_achado_comorb"] = (
        pd.DataFrame(hm_comorb).set_index("Achado").drop(columns="N", errors="ignore")
        if hm_comorb else pd.DataFrame()
    )

    comor_diag = pd.DataFrame()
    for ccol, label in COMORB_COLS.items():
        if ccol in df.columns:
            comor_diag[label] = df.groupby("diag_cat")[ccol].mean().round(3) * 100
    ind["hm_diag_comorb"] = comor_diag

    top_muns = df["Cidade"].value_counts().head(15).index.tolist()
    df_top = df[df["Cidade"].isin(top_muns)]

    def _mun_matrix(subcats):
        rows = []
        for nome, cols in subcats.items():
            for mun in top_muns:
                sub = df_top[df_top["Cidade"] == mun]
                cnt = contar_achado(sub, cols)
                if cnt > 0:
                    rows.append({"Municipio": mun, "Achado": nome, "N": cnt})
        if rows:
            return pd.DataFrame(rows).pivot(
                index="Municipio", columns="Achado", values="N"
            ).fillna(0)
        return pd.DataFrame()

    ind["mun_arr_matrix"] = _mun_matrix(ECG_ACHADOS["Arritmias"])
    ind["mun_blk_matrix"] = _mun_matrix(ECG_ACHADOS["Bloqueios"])

    ind["comorb_mun_rankings"] = {}
    for ccol in COMORB_COLS:
        if ccol in df.columns:
            ind["comorb_mun_rankings"][ccol] = comorb_por_municipio(df, ccol)

    ind["boxplot_data"] = {}
    for cat, subcats in ECG_ACHADOS.items():
        pieces = []
        for nome, cols in subcats.items():
            mask = achado_mask(df, cols)
            sub = df[mask][["idade"]].copy()
            if len(sub) >= 3:
                sub["Achado"] = nome
                pieces.append(sub)
        ind["boxplot_data"][cat] = pd.concat(pieces) if pieces else pd.DataFrame()

    todos_ach = pd.DataFrame()
    for subcats in ECG_ACHADOS.values():
        d = achados_df(df, subcats)
        if not d.empty:
            todos_ach = pd.concat([todos_ach, d])
    ind["top10_achados"] = (
        todos_ach.sort_values("Casos", ascending=False)
        .drop_duplicates("Achado").head(10)
        if not todos_ach.empty else pd.DataFrame()
    )

    hip_df = df[df["_hipotese"].astype(str).str.strip().ne("")]
    if len(hip_df) > 0:
        hip_vc = _value_counts_rename(hip_df["_hipotese"], "Hipotese", "Frequencia", head=20)
        ind["hipoteses_freq"] = hip_vc
    else:
        ind["hipoteses_freq"] = pd.DataFrame()

    ind_df = df[df["_indicacao"].astype(str).str.strip().ne("")]
    if len(ind_df) > 0:
        ind_vc = _value_counts_rename(ind_df["_indicacao"], "Indicacao", "Frequencia", head=20)
        ind["indicacoes_freq"] = ind_vc
    else:
        ind["indicacoes_freq"] = pd.DataFrame()

    return ind