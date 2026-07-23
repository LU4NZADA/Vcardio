import streamlit as st
import pandas as pd
from components import sub_header, fmt
from charts.kpis import render_kpi_row
from components.alerts import render_alerts
from charts.ecg import achados_bar
from charts.maps import mapa_simples
from config.app import COMORB_COLS
from config.colors import DIAG_COLORS
from constants import ECG_ACHADOS


def _render_kpis_municipio(df, municipio):
    mun_df = df[df["Cidade"] == municipio].copy()
    n = len(mun_df)
    if n == 0:
        st.warning(f"Nenhum exame encontrado para {municipio}.")
        return

    altos = (mun_df["diag_cat"] != "Normal").sum()
    pct_alt = round(100 * altos / n, 1)
    avg_idade = round(mun_df["idade"].mean(), 1)
    n_fem = int((mun_df["Sexo"] == "Feminino").sum())
    n_masc = int((mun_df["Sexo"] == "Masculino").sum())

    from analysis.ecg import contar_achado
    _all = lambda cat: [c for cols in ECG_ACHADOS[cat].values() for c in cols]
    n_arr = contar_achado(mun_df, _all("Arritmias"))
    n_blk = contar_achado(mun_df, _all("Bloqueios"))

    render_kpi_row([
        ("red", municipio, fmt(n), "exames realizados"),
        ("amber", "Alterados", f"{pct_alt}%", f"{altos} laudos"),
        ("blue", "Idade media", f"{avg_idade}", "anos"),
        ("purple", "Feminino", fmt(n_fem), f"{round(100*n_fem/n,1)}%"),
        ("green", "Masculino", fmt(n_masc), f"{round(100*n_masc/n,1)}%"),
    ])
    st.markdown("<br>", unsafe_allow_html=True)
    render_kpi_row([
        ("red", "Arritmias", fmt(n_arr), f"{round(100*n_arr/n,1)}%" if n else "-"),
        ("blue", "Bloqueios", fmt(n_blk), f"{round(100*n_blk/n,1)}%" if n else "-"),
        ("amber", "Hipertenso", fmt(int(mun_df["Hipertenso"].sum())), "pacientes"),
        ("purple", "Diabetes", fmt(int(mun_df["Diabetes Mellitus"].sum())), "pacientes"),
        ("cyan", "Tabagista", fmt(int(mun_df["Tabagista"].sum())), "pacientes"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    sub_header("Diagnostico ECG")
    diag_counts = mun_df["diag_cat"].value_counts().reset_index()
    diag_counts.columns = ["Diagnostico", "Qtd"]
    cols_diag = st.columns(max(len(diag_counts), 1))
    for col, (_, row) in zip(cols_diag, diag_counts.iterrows()):
        cor = DIAG_COLORS.get(row["Diagnostico"], "#8b949e")
        pct = round(100 * row["Qtd"] / n, 1)
        with col:
            st.markdown(
                f"""<div class="kpi-card" style="border-bottom: 3px solid {cor}">
                <div class="kpi-label">{row['Diagnostico']}</div>
                <div class="kpi-value" style="color:{cor}">{row['Qtd']}</div>
                <div class="kpi-sub">{pct}%</div></div>""",
                unsafe_allow_html=True,
            )

    sub_header("Achados ECG encontrados")
    from analysis.ecg import achados_df
    todos_achados = []
    for cat, subcats in ECG_ACHADOS.items():
        ach = achados_df(mun_df, subcats)
        if not ach.empty:
            ach["Categoria"] = cat
            todos_achados.append(ach)
    if todos_achados:
        achados_completo = pd.concat(todos_achados).sort_values("Casos", ascending=False)
        fig = achados_bar(achados_completo, f"Achados ECG - {municipio}", "#e24b4a")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum achado ECG neste municipio.")

    sub_header("Comorbidades")
    comorb_data = []
    cores = ["#e24b4a", "#ba7517", "#8b949e", "#378add"]
    for (ccol, lbl), cor in zip(COMORB_COLS.items(), cores):
        if ccol in mun_df.columns:
            total = int(mun_df[ccol].sum())
            pct = round(100 * total / n, 1) if n else 0
            comorb_data.append((cor, lbl, total, pct))
    if comorb_data:
        cols_c = st.columns(len(comorb_data))
        for col, (cor, lbl, total, pct) in zip(cols_c, comorb_data):
            with col:
                st.markdown(
                    f"""<div class="comor-card">
                    <div class="comor-val" style="color:{cor}">{pct}%</div>
                    <div style="font-size:13px;color:#c9d1d9">{total}</div>
                    <div class="comor-lbl">{lbl}</div></div>""",
                    unsafe_allow_html=True,
                )


def render(df, ind):
    mun_sel = st.selectbox(
        "Ver detalhes de um municipio (opcional)",
        ["(Geral)"] + sorted(df["Cidade"].unique().tolist()),
        key="mun_geral",
    )

    if mun_sel == "(Geral)":
        n_total = ind.get("n_total", ind["n"])
        n_muns_total = ind.get("n_muns_total", ind["n_muns"])
        render_kpi_row([
            ("red", "Exames", fmt(n_total), f"{n_muns_total} municipios"),
            ("amber", "Idade media", f"{ind['avg_age']}", "anos"),
            ("blue", "Arritmias", fmt(ind["n_arr"]),
             f"{round(100*ind['n_arr']/n_total,1)}%"),
            ("purple", "Bloqueios", fmt(ind["n_blk"]),
             f"{round(100*ind['n_blk']/n_total,1)}%"),
            ("green", "Alterados", f"{ind['alt_pct']}%", "laudos alterados"),
        ])
        st.markdown("<br>", unsafe_allow_html=True)
        render_kpi_row([
            ("red", "Repolarizacao", fmt(ind["n_repo"]), "achados"),
            ("blue", "Sobrecargas", fmt(ind["n_sobr"]), "achados"),
            ("purple", "Fibroses", fmt(ind["n_fibr"]), "achados"),
            ("cyan", "PR curto/WPW", f"{ind['n_pr']}/{ind['n_wpw']}", "achados"),
            ("green", "Marcapassos", fmt(ind["n_marc"]), "pacientes"),
        ])
        render_alerts(ind)

        sub_header("Top 10 achados ECG")
        if not ind["top10_achados"].empty:
            fig = achados_bar(ind["top10_achados"], "Achados mais frequentes")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    else:
        _render_kpis_municipio(df, mun_sel)

    sub_header("Distribuicao territorial")
    cidade_para_mapa = mun_sel if mun_sel != "(Geral)" else None
    fig = mapa_simples(ind["mapa_dados"], cidade_destaque=cidade_para_mapa, df=df)
    if fig:
        st.plotly_chart(fig, use_container_width=True)