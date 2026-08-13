"""
Pagina Distancias — deslocamento real da equipe pelo Projeto Saude Digital Movel.
A equipe parte de Diamantina ate o Distrito onde o exame foi realizado.
"""

import streamlit as st
import pandas as pd
from components import sub_header
from charts.kpis import render_kpi_row
from analysis.distancias import calcular_distancias_distritos
from charts.distancias import grafico_rotas_distritos, grafico_mapa_distritos


def render(df, ind):
    sub_header("Deslocamento real da equipe — Projeto Saude Digital Movel")

    dist = calcular_distancias_distritos(df)

    render_kpi_row([
        ("red", "Total estimado", f"{dist['total_estimado_km']:,.0f} km",
         "ida e volta para todos os locais"),
        ("amber", "Percurso minimo", f"{dist['distancia_minima_percurso_km']:,.0f} km",
         "rota otimizada (MST)"),
        ("blue", "Media por local", f"{dist['media_km_por_local']:,.0f} km",
         "ida e volta media"),
        ("purple", "Locais visitados", f"{dist['total_locais']}",
         f"{dist['locais_com_coords']} com coordenadas"),
        ("green", "Base do projeto", f"{dist['cidade_base']}",
         "ponto de partida da equipe"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    sub_header("Rede de deslocamento entre locais de exame")
    fig_mapa = grafico_mapa_distritos(dist)
    if fig_mapa:
        st.plotly_chart(fig_mapa, use_container_width=True)

    sub_header("Distancia de Diamantina ate cada local de exame")
    fig_rotas = grafico_rotas_distritos(dist)
    if fig_rotas:
        st.plotly_chart(fig_rotas, use_container_width=True)

    sub_header("Rotas detalhadas")
    rotas_df = pd.DataFrame(dist["rotas"])
    if not rotas_df.empty:
        if "km_ida_volta" in rotas_df.columns:
            rotas_df = rotas_df.sort_values("km_ida_volta", ascending=False).head(25)
            rotas_df = rotas_df[["origem", "destino", "municipio", "exames", "km", "km_ida_volta"]].reset_index(drop=True)
            rotas_df.index += 1
            rotas_df.columns = ["Base", "Destino", "Municipio", "Exames", "Distancia ida (km)", "Distancia ida+volta (km)"]
        else:
            rotas_df = rotas_df.sort_values("km", ascending=False).head(25)
            rotas_df = rotas_df.reset_index(drop=True)
            rotas_df.index += 1
            rotas_df.columns = ["Base", "Destino", "Municipio", "Exames", "Distancia (km)"]
        st.dataframe(rotas_df, use_container_width=True)

    sub_header("Exames por local de coleta")
    locais_df = pd.DataFrame(dist["exames_por_local"]).sort_values("exames", ascending=False)
    if not locais_df.empty:
        locais_df = locais_df.reset_index(drop=True)
        locais_df.index += 1
        locais_df.columns = ["Distrito", "Municipio", "Exames"]
        st.dataframe(locais_df, use_container_width=True)