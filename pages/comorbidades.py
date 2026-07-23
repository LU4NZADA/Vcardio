import streamlit as st
from components import sub_header
from charts.kpis import render_comorb_cards
from charts.comorbidities import comorb_sexo, comorb_faixa, sexo_diag_crosstab


def render(df, ind):
    sub_header("Comorbidades na amostra")
    cores = ["#e24b4a", "#ba7517", "#8b949e", "#378add"]
    cards = [(cor, lbl, val, pct) for (_, lbl, val, pct), cor in zip(ind["comorb_resumo"], cores)]
    render_comorb_cards(cards)
    sub_header("Comorbidades por sexo")
    fig = comorb_sexo(ind["comorb_sexo"])
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    sub_header("Comorbidades por faixa etaria")
    fig = comorb_faixa(ind["comorb_faixa"])
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    sub_header("Sexo x diagnostico")
    fig = sexo_diag_crosstab(ind["sexo_diag_crosstab"])
    if fig:
        st.plotly_chart(fig, use_container_width=True)