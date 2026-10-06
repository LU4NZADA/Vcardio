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
                      "Arritmias", "#D64550")
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
                      "Bloqueios", "#2969BD")
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
                            [[0, "#f2f7fc"], [0.5, "#9cc3e8"], [1, "#2969BD"]])
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    sub_header("Comorbidades por tipo de bloqueio")
    fig = comorb_prevalencia(ind["blk_comorb_prev"], "Comorbidades x Bloqueio")
    if fig:
        st.plotly_chart(fig, use_container_width=True)


def render_ecg_alteracoes(df, ind):
    achados = ind["achados"]

    for cat, title, cor in [
        ("Repolarizacao", "Tipos de repolarizacao", "#D9902E"),
        ("Sobrecargas", "Tipos de sobrecarga", "#6D5BCA"),
        ("Fibroses", "Tipos de fibrose", "#E36B2F"),
        ("Baixa Voltagem", "Tipos de baixa voltagem", "#8B9BB4"),
        ("Conducao", "Conducao", "#0FA3B1"),
        ("Eixo", "Eixo cardiaco", "#D64550"),
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