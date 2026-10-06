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
                          [[0, "#f2f7fc"], [0.25, "#cfe3f4"], [0.5, "#9cc3e8"],
                           [0.75, "#D9902E"], [1, "#D64550"]])
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

    sub_header("Risco territorial por local do exame")
    if "risco_distrito" in ind and not ind["risco_distrito"].empty:
        rd = ind["risco_distrito"].copy()
        rd.rename(columns={"Distrito": "Cidade", "total": "total"}, inplace=True)
        resultado = risco_chart(rd)
        if resultado:
            if isinstance(resultado, tuple):
                fig, legenda = resultado
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(legenda, unsafe_allow_html=True)
            else:
                st.plotly_chart(resultado, use_container_width=True)
    else:
        st.info("Nenhum distrito identificado.")