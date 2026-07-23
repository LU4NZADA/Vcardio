import streamlit as st
from utils.textos import t


def render_header():
    st.markdown("### VCARDIO")
    st.markdown('<span style="font-size:11px;color:#e24b4a;font-family:monospace">PIBIC - UFVJM - Edital 005/2025</span>', unsafe_allow_html=True)
    st.markdown("---")


def render_footer():
    st.markdown("---")
    st.markdown(t('<div style="font-size:11px;color:#8b949e;line-height:1.6">Painel de vigilância cardiovascular com análise de <strong style="color:#c9d1d9">todos os achados ECG</strong>.</div>'), unsafe_allow_html=True)