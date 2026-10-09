import streamlit as st
from utils.textos import t


def render_header():
    st.markdown("### VCARDIO")
    st.markdown('<span style="font-size:11px;color:#000000;font-family:monospace">PIBIC - UFVJM - Edital 005/2025</span>', unsafe_allow_html=True)
    st.markdown("---")


def render_footer():
    st.markdown("---")
    st.markdown(t('<div style="font-size:11px;color:#000000;line-height:1.6">Painel de vigilância cardiovascular com análise de <strong style="color:#000000">todos os achados ECG</strong>.</div>'), unsafe_allow_html=True)