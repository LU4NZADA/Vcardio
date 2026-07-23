import streamlit as st
from components import sub_header
from charts.heatmaps import heatmap_generic, heatmap_percent
from charts.municipalities import risco_territorial as risco_chart


def render(df, ind):
    sub_header("Heatmap: achados x faixa etaria")
    fig = heatmap_generic(ind["hm_achado_faixa"], "Achados por faixa etaria")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    sub_header("Heatmap: achados x sexo")
    fig = heatmap_generic(ind["hm_achado_sexo"], "Achados por sexo",
                          [[0, "#0d1117"], [0.25, "#1a1f2e"], [0.5, "#30363d"],
                           [0.75, "#ba7517"], [1, "#e24b4a"]])
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    sub_header("Heatmap: achados x comorbidades (%)")
    fig = heatmap_percent(ind["hm_achado_comorb"], "Comorbidades por achado ECG")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    sub_header("Heatmap: diagnostico x comorbidades (%)")
    fig = heatmap_percent(ind["hm_diag_comorb"], "Comorbidades por diagnostico")
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    sub_header("Risco territorial")
    resultado = risco_chart(ind["risco_municipio"])
    if resultado:
        if isinstance(resultado, tuple):
            fig, legenda = resultado
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(legenda, unsafe_allow_html=True)
        else:
            st.plotly_chart(resultado, use_container_width=True)