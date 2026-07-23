import streamlit as st
from components import sub_header
from utils.textos import t


def render_alerts(ind):
    n = ind["n"]
    if n == 0:
        return
    alertas = []
    pct_arr = ind["n_arr"] / n
    avg_age = ind["avg_age"]
    pct_hip = 0
    for _, label, total, pct in ind["comorb_resumo"]:
        if label == "HAS":
            pct_hip = total / n
            break
    if pct_arr > 0.08:
        alertas.append(("warn", "Alta prevalência de arritmias", f"{round(pct_arr*100,1)}% dos laudos."))
    if pct_hip > 0.55:
        alertas.append(("warn", "Alto índice de hipertensão", f"{round(pct_hip*100,1)}% hipertensos."))
    if avg_age > 65:
        alertas.append(("info", "Perfil etário elevado", f"Idade média: {avg_age} anos."))
    if alertas:
        sub_header("Alertas automáticos")
        for level, titulo, corpo in alertas:
            cls = "alert-box info" if level == "info" else "alert-box"
            st.markdown(f'<div class="{cls}"><div class="alert-title">! {titulo}</div><div class="alert-body">{corpo}</div></div>', unsafe_allow_html=True)