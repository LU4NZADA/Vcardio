"""
Cards KPI.
"""

import streamlit as st


def render_kpi_row(kpis):
    cols = st.columns(len(kpis))
    for col, (cor, label, valor, sub) in zip(cols, kpis):
        with col:
            st.markdown(f"""<div class="kpi-card {cor}">
              <div class="kpi-label">{label}</div>
              <div class="kpi-value">{valor}</div>
              <div class="kpi-sub">{sub}</div></div>""", unsafe_allow_html=True)


def render_comorb_cards(comorb_data):
    cols = st.columns(len(comorb_data))
    for col, (cor, lbl, val, pct) in zip(cols, comorb_data):
        with col:
            st.markdown(f"""<div class="comor-card">
              <div class="comor-val" style="color:{cor}">{pct}%</div>
              <div style="font-size:13px;color:#c9d1d9">{val:,}</div>
              <div class="comor-lbl">{lbl}</div></div>""", unsafe_allow_html=True)