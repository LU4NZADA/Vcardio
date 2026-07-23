import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from components import sub_header, fmt
from charts.kpis import render_kpi_row
from charts.maps import mapa_risco
from charts.municipalities import risco_territorial as risco_chart, comorb_municipio
from charts.ecg import achados_bar
from charts.heatmaps import heatmap_generic
from config.app import COMORB_COLS
from config.colors import DIAG_COLORS
from constants import ECG_ACHADOS


def render_ficha_municipio(df, municipio):
    """Ficha completa de um municipio especifico."""
    mun_df = df[df["Cidade"] == municipio].copy()
    n = len(mun_df)
    if n == 0:
        st.warning(f"Nenhum exame encontrado para {municipio}.")
        return

    st.markdown(f"### {municipio}")

    altos = (mun_df["diag_cat"] != "Normal").sum()
    pct_alt = round(100 * altos / n, 1) if n else 0
    avg_idade = round(mun_df["idade"].mean(), 1) if n else 0
    n_fem = (mun_df["Sexo"] == "Feminino").sum()
    n_masc = (mun_df["Sexo"] == "Masculino").sum()

    render_kpi_row([
        ("red", "Total exames", fmt(n), municipio),
        ("amber", "Alterados", f"{pct_alt}%", f"{altos} laudos"),
        ("blue", "Idade media", f"{avg_idade}", "anos"),
        ("purple", "Feminino", fmt(n_fem), f"{round(100*n_fem/n,1)}%"),
        ("green", "Masculino", fmt(n_masc), f"{round(100*n_masc/n,1)}%"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    sub_header("Diagnostico ECG")
    diag_counts = mun_df["diag_cat"].value_counts().reset_index()
    diag_counts.columns = ["Diagnostico", "Qtd"]
    cols_diag = st.columns(len(diag_counts))
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
        achados_tabela = achados_completo[["Achado", "Categoria", "Casos", "%"]].reset_index(drop=True)
        achados_tabela.index += 1
        st.dataframe(achados_tabela, use_container_width=True)
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

    # Faixa etaria
    sub_header("Distribuicao por faixa etaria")
    faixa_counts = mun_df["faixa"].value_counts().sort_index().reset_index()
    faixa_counts.columns = ["Faixa", "Qtd"]
    fig = go.Figure(go.Bar(
        x=faixa_counts["Faixa"].tolist(),
        y=faixa_counts["Qtd"].tolist(),
        text=faixa_counts["Qtd"].tolist(),
        textposition="outside",
        marker=dict(color="#7f77dd", cornerradius=4, line=dict(width=0)),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#161b22",
        font=dict(color="#c9d1d9", family="IBM Plex Mono"),
        height=280,
        margin=dict(l=0, r=20, t=30, b=0),
        title=dict(text="Distribuicao por faixa etaria", font=dict(size=13, color="#e6edf3")),
    )
    st.plotly_chart(fig, use_container_width=True)

    sub_header("Exames realizados")
    cols_mostrar = ["idade", "Sexo", "diag_cat", "Data_cadastro", "Hipertenso",
                    "Diabetes Mellitus", "Tabagista", "Etilista"]
    cols_presentes = [c for c in cols_mostrar if c in mun_df.columns]
    tabela = mun_df[cols_presentes].copy()
    tabela.columns = [c.replace("idade", "Idade")
                      .replace("diag_cat", "Diagnostico")
                      .replace("Data_cadastro", "Data")
                      .replace("Diabetes Mellitus", "Diabetes")
                      for c in tabela.columns]
    tabela["Data"] = pd.to_datetime(tabela["Data"], errors="coerce").dt.strftime("%d/%m/%Y")
    tabela = tabela.sort_values("Data", ascending=False).reset_index(drop=True)
    tabela.index += 1
    st.dataframe(tabela, use_container_width=True, height=300)


def render(df, ind):
    sub_header("Mapa interativo")
    resultado = mapa_risco(ind["mapa_dados"])
    if resultado:
        st.plotly_chart(resultado, use_container_width=True)

    sub_header("Ranking epidemiologico")
    rank = ind["risco_municipio"].copy()
    rank = rank[rank["total"] >= 1].sort_values("total", ascending=False).head(15)
    rd = rank[["Cidade", "total", "alterados", "idade_media", "pct"]].copy()
    rd.columns = ["Municipio", "Exames", "Alterados", "Idade Media", "% Alterado"]
    rd = rd.reset_index(drop=True)
    rd.index += 1
    st.dataframe(rd, use_container_width=True)

    sub_header("Ranking por comorbidade")
    comorb_sel = st.selectbox(
        "Comorbidade", list(COMORB_COLS.keys()),
        format_func=lambda x: COMORB_COLS[x], key="comorb_mun",
    )
    cm_df = ind["comorb_mun_rankings"].get(comorb_sel)
    if cm_df is not None and not cm_df.empty:
        fig = comorb_municipio(cm_df, COMORB_COLS[comorb_sel])
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    sub_header("Municipio x Arritmia")
    fig = heatmap_generic(
        ind["mun_arr_matrix"], "Arritmias por municipio",
        [[0, "#0d1117"], [0.5, "#30363d"], [1, "#e24b4a"]],
    )
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    sub_header("Municipio x Bloqueio")
    fig = heatmap_generic(
        ind["mun_blk_matrix"], "Bloqueios por municipio",
        [[0, "#0d1117"], [0.5, "#30363d"], [1, "#378add"]],
    )
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    sub_header("Ficha detalhada do municipio")
    from components.filters import CIDADES_FORA_MG
    municipios_lista = sorted([
        c for c in df["Cidade"].unique().tolist()
        if c not in CIDADES_FORA_MG
    ])
    mun_sel = st.selectbox(
        "Selecione o municipio",
        municipios_lista,
        key="ficha_mun",
    )
    if mun_sel:
        render_ficha_municipio(df, mun_sel)