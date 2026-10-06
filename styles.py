"""
Estilos globais do aplicativo - tema claro institucional UFVJM.
"""

import streamlit as st


def load_css():
    st.markdown(FONTS_LINK, unsafe_allow_html=True)
    st.markdown(CSS_CORE, unsafe_allow_html=True)
    st.markdown(CSS_COMPONENTS, unsafe_allow_html=True)
    st.markdown(CSS_LAYOUT, unsafe_allow_html=True)


FONTS_LINK = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600;700&display=swap" rel="stylesheet">
"""

CSS_CORE = """
<style>
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background-color: #f7f8fa; color: #1F2430; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; }
</style>
"""

CSS_COMPONENTS = """
<style>
.topbar { background: linear-gradient(90deg, #244A7C 0%, #2969BD 40%, #0094FF 78%, #06ACFF 100%); color: #ffffff; border-radius: 12px; padding: 20px 28px; margin-bottom: 20px; position: relative; overflow: hidden; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 8px rgba(36,74,124,.18); }
.topbar::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg,#06ACFF,#0094FF,#2969BD,#244A7C); }
.topbar-title { font-size: 20px; font-weight: 700; margin-bottom: 4px; color: #ffffff; }
.topbar-sub { font-size: 12px; color: #d6e4f7; font-family: 'IBM Plex Mono', monospace; }
.badge { display: inline-block; background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.38); color: #ffffff; padding: 2px 10px; border-radius: 20px; font-size: 10px; font-family: 'IBM Plex Mono', monospace; margin-top: 6px; }
.kpi-card { background: #ffffff; border: 1px solid #DEE3EA; border-radius: 10px; padding: 16px 18px; position: relative; overflow: hidden; text-align: center !important; box-shadow: 0 1px 3px rgba(16,24,40,.06); }
.kpi-card .kpi-label, .kpi-card .kpi-value, .kpi-card .kpi-sub { text-align: center !important; }
.kpi-card::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px; }
.kpi-card.red::after { background: #D64550; }
.kpi-card.amber::after { background: #D9902E; }
.kpi-card.blue::after { background: #2969BD; }
.kpi-card.purple::after { background: #6D5BCA; }
.kpi-card.green::after { background: #2E9E5B; }
.kpi-card.cyan::after { background: #0FA3B1; }
.kpi-label { font-size: 10px; font-family: 'IBM Plex Mono', monospace; color: #64707D; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.kpi-value { font-size: 22px; font-weight: 700; line-height: 1; margin-bottom: 3px; color: #101828; }
.kpi-sub { font-size: 11px; color: #64707D; }
.alert-box { background: rgba(214,69,80,.07); border: 1px solid rgba(214,69,80,.32); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; }
.alert-box.info { background: rgba(41,105,189,.07); border-color: rgba(41,105,189,.32); }
.alert-title { font-size: 12px; font-weight: 600; color: #D64550; margin-bottom: 2px; }
.alert-box.info .alert-title { color: #2969BD; }
.alert-body { font-size: 11px; color: #4A5568; }
.sec-label { font-size: 10px; font-family: 'IBM Plex Mono', monospace; color: #64707D; text-transform: uppercase; letter-spacing: 2px; margin: 22px 0 12px; border-bottom: 1px solid #DEE3EA; padding-bottom: 6px; }
.comor-card { background: #ffffff; border: 1px solid #DEE3EA; border-radius: 8px; padding: 14px; text-align: center; }
.comor-val { font-size: 22px; font-weight: 700; margin-bottom: 2px; }
.comor-lbl { font-size: 10px; color: #64707D; font-family: 'IBM Plex Mono', monospace; text-transform: uppercase; }
.sobre-card { background: #ffffff; border: 1px solid #DEE3EA; border-radius: 10px; padding: 20px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(16,24,40,.06); }
.sobre-card h3 { margin-top: 0; color: #101828; }
.sobre-card p { color: #4A5568; font-size: 13px; line-height: 1.7; }
.sobre-card ul { color: #4A5568; font-size: 13px; line-height: 1.8; }
.sobre-card strong { color: #2969BD; }
</style>
"""

CSS_LAYOUT = """
<style>
[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #e2e6ec !important; }
[data-testid="stSidebar"] label { color: #64707D !important; font-size: 12px !important; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #ffffff; border-radius: 10px; padding: 4px; border: 1px solid #DEE3EA; flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 8px 14px; font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #64707D; background: transparent; border: none; }
.stTabs [aria-selected="true"] { background: #eaf1fa !important; color: #2969BD !important; }
.app-footer { margin-top: 32px; padding: 14px; border-top: 1px solid #DEE3EA; font-size: 10px; font-family: 'IBM Plex Mono', monospace; color: #8A94A3; display: flex; justify-content: space-between; }
</style>
"""