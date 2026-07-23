import streamlit as st
import pandas as pd
from components import sub_header
from charts.ecg import (
    achados_bar, achados_por_sexo, achados_por_faixa,
    comorb_prevalencia, treemap_achados,
)


def render_arritmias(df, ind):
    sub_header("Ranking de arritmias por tipo")
    fig = achados_bar(ind["achados"].get("Arritmias", pd.DataFrame()),
                      "Arritmias", "#e24b4a")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhuma arritmia encontrada.")

    sub_header("Arritmias por sexo")
    fig = achados_por_sexo(ind["arr_por_sexo"], "Arritmias x Sexo")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    sub_header("Arritmias por faixa etaria")
    fig = achados_por_faixa(ind["arr_por_faixa"], "Arritmias x Faixa")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    sub_header("Comorbidades por tipo de arritmia")
    fig = comorb_prevalencia(ind["arr_comorb_prev"], "Comorbidades x Arritmia")
    if fig:
        st.plotly_chart(fig, use_container_width=True)


def render_bloqueios(df, ind):
    sub_header("Ranking de bloqueios por tipo")
    fig = achados_bar(ind["achados"].get("Bloqueios", pd.DataFrame()),
                      "Bloqueios", "#378add")
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Nenhum bloqueio encontrado.")

    sub_header("Bloqueios por sexo")
    fig = achados_por_sexo(ind["blk_por_sexo"], "Bloqueios x Sexo")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    sub_header("Bloqueios por faixa etaria")
    fig = achados_por_faixa(ind["blk_por_faixa"], "Bloqueios x Faixa",
                            [[0, "#0d1117"], [0.5, "#30363d"], [1, "#378add"]])
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    sub_header("Comorbidades por tipo de bloqueio")
    fig = comorb_prevalencia(ind["blk_comorb_prev"], "Comorbidades x Bloqueio")
    if fig:
        st.plotly_chart(fig, use_container_width=True)


def render_ecg_alteracoes(df, ind):
    achados = ind["achados"]

    for cat, title, cor in [
        ("Repolarizacao", "Tipos de repolarizacao", "#ba7517"),
        ("Sobrecargas", "Tipos de sobrecarga", "#7f77dd"),
        ("Fibroses", "Tipos de fibrose", "#d85a30"),
        ("Baixa Voltagem", "Tipos de baixa voltagem", "#8b949e"),
        ("Conducao", "Conducao", "#39d2c0"),
        ("Eixo", "Eixo cardiaco", "#e24b4a"),
    ]:
        sub_header(cat)
        data = achados.get(cat)
        if data is not None and not data.empty:
            fig = achados_bar(data, title, cor)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"Nenhum achado de {cat.lower()}.")

    # Treemap interativo (substitui o boxplot)
    sub_header("Mapa de achados por categoria")
    cat_sel = st.selectbox(
        "Categoria",
        ["Arritmias", "Bloqueios", "Repolarizacao", "Sobrecargas",
         "Fibroses", "Baixa Voltagem", "Conducao", "Eixo"],
        key="treemap_cat",
    )
    fig = treemap_achados(
        {cat_sel: achados.get(cat_sel, pd.DataFrame())},
        f"Achados — {cat_sel}",
    )
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"Nenhum achado em {cat_sel}.")