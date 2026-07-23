"""
Pagina Demografia com grafico de pizza nativo do Streamlit.
"""

import streamlit as st
from components import sub_header, fmt
from charts.kpis import render_kpi_row
from charts.demographics import ano_bar, faixa_bar, piramide, top_municipios, sazonalidade


def render(df, ind):
    sub_header("Distribuicao demografica")

    n = ind["n"]
    n_fem = int((df["Sexo"] == "Feminino").sum())
    n_masc = int((df["Sexo"] == "Masculino").sum())

    render_kpi_row([
        ("red", "Total exames", fmt(n), f"{ind['n_muns']} municipios"),
        ("amber", "Alterados", f"{ind['alt_pct']}%", "dos exames"),
        ("blue", "Idade media", f"{ind['avg_age']}", "anos"),
        ("purple", "Masculino", fmt(n_masc), "exames"),
        ("green", "Feminino", fmt(n_fem), "exames"),
    ])

    # Grafico de pizza nativo do Streamlit
    sub_header("Exames por sexo")
    import plotly.graph_objects as go

    fig = go.Figure(data=[go.Pie(
        labels=["Feminino", "Masculino"],
        values=[n_fem, n_masc],
        hole=0.6,
        marker=dict(colors=["#e24b4a", "#378add"]),
        textinfo="label+percent",
        textfont=dict(size=11, color="#c9d1d9"),
    )])
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#161b22",
        font=dict(color="#c9d1d9", family="IBM Plex Mono"),
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=True,
        legend=dict(font=dict(color="#8b949e")),
        title=dict(text="Distribuicao por sexo", font=dict(color="#e6edf3")),
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        sub_header("Exames por ano")
        fig = ano_bar(ind["ano_counts"])
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        sub_header("Exames por faixa etaria")
        fig = faixa_bar(ind["faixa_counts"])
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    sub_header("Piramide etaria")
    fig = piramide(ind["piramide"])
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        sub_header("Top 15 municipios")
        fig = top_municipios(ind["top_municipios"])
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        sub_header("Sazonalidade dos exames")
        fig = sazonalidade(ind["sazonalidade"])
        if fig:
            st.plotly_chart(fig, use_container_width=True)