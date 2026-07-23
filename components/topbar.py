import streamlit as st
from datetime import datetime


def render_topbar():
    st.markdown(f"""
    <div class="topbar">
      <div>
        <div class="topbar-title">Painel Inteligente de Vigilância Cardiovascular</div>
        <div class="topbar-sub">Saúde Digital Móvel - UFVJM - Vale do Jequitinhonha</div>
        <div class="badge">PIBIC / EDITAL 005/2025</div>
      </div>
      <div style="text-align:right;font-size:11px;color:#8b949e;font-family:monospace">
        Atualizado em<br><strong style="color:#c9d1d9;font-size:13px">{datetime.now():%d/%m/%Y %H:%M}</strong>
      </div>
    </div>""", unsafe_allow_html=True)