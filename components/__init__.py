"""
Componentes reutilizaveis.
"""

import streamlit as st
from utils.textos import t


def sub_header(text):
    st.markdown(f'<div class="sec-label">{t(text)}</div>', unsafe_allow_html=True)


def fmt(n):
    return f"{n:,}".replace(",", ".")