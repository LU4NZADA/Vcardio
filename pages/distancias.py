"""
Pagina Distancias — mostra deslocamento da equipe pelo Projeto Saude Digital Movel.
A equipe parte de Diamantina ate a cidade natal de cada paciente para coletar ECG.
"""

import streamlit as st
import pandas as pd
from components import sub_header
from charts.kpis import render_kpi_row
from analysis.distancias import calcular_todas_distancias
from charts.distancias import grafico_rotas, grafico_mapa_distancias


def render(df, ind):
    sub_header("Deslocamento da equipe — Projeto Saude Digital Movel")

    cidades_visitadas = sorted(df["Cidade"].unique().tolist())
    dist = calcular_todas_distancias(cidades_visitadas, cidade_base="Diamantina")

    render_kpi_row([
        ("red", "Total estimado", f"{dist['total_estimado_km']:,.0f} km",
         "ida e volta para todas as cidades"),
        ("amber", "Percurso minimo", f"{dist['distancia_minima_percurso_km']:,.0f} km",
         "rota otimizada (MST)"),
        ("blue", "Media por cidade", f"{dist['media_km_por_cidade']:,.0f} km",
         "ida e volta media"),
        ("purple", "Cidades visitadas", f"{dist['total_cidades_visitadas']}",
         f"{dist['cidades_com_coordenadas']} com coordenadas"),
        ("green", "Base do projeto", f"{dist['cidade_base']}",
         "ponto de partida da equipe"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    sub_header("Rede de deslocamento entre cidades natal dos pacientes")
    fig_mapa = grafico_mapa_distancias(dist, None)
    if fig_mapa:
        st.plotly_chart(fig_mapa, use_container_width=True)

    sub_header("Distancia de Diamantina ate cada cidade natal")
    fig_rotas = grafico_rotas(dist)
    if fig_rotas:
        st.plotly_chart(fig_rotas, use_container_width=True)

    sub_header("Rotas detalhadas (Top 20)")
    rotas_df = pd.DataFrame(dist["rotas"]).sort_values("km", ascending=False).head(20)
    if not rotas_df.empty:
        rotas_df = rotas_df.reset_index(drop=True)
        rotas_df.index += 1
        rotas_df.columns = ["Base", "Cidade Natal", "Distancia (km)"]
        st.dataframe(rotas_df, use_container_width=True)

    sub_header("Pares de cidades mais distantes entre si")
    pares_df = pd.DataFrame(dist["pares_mais_distantes"])
    if not pares_df.empty:
        pares_df = pares_df.reset_index(drop=True)
        pares_df.index += 1
        pares_df.columns = ["Cidade A", "Cidade B", "Distancia (km)"]
        st.dataframe(pares_df, use_container_width=True)