import streamlit as st
from datetime import datetime
from utils.textos import t


def render_footer():
    st.markdown(f"""
    <div class="app-footer">
      <span>PIBIC/UFVJM - Edital 005/2025 - Prof. Mariana Roberta Lopes Simões</span>
      <span>Dados anonimizados - LGPD - {datetime.now().year}</span>
    </div>""", unsafe_allow_html=True)