"""
Estilos globais do aplicativo.
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
.stApp { background-color: #0d1117; color: #e6edf3; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; }
</style>
"""

CSS_COMPONENTS = """
<style>
.topbar { background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 20px 28px; margin-bottom: 20px; position: relative; overflow: hidden; display: flex; justify-content: space-between; align-items: center; }
.topbar::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg,#a32d2d,#e24b4a,#ba7517,#e24b4a,#a32d2d); }
.topbar-title { font-size: 20px; font-weight: 700; margin-bottom: 4px; }
.topbar-sub { font-size: 12px; color: #8b949e; font-family: 'IBM Plex Mono', monospace; }
.badge { display: inline-block; background: rgba(226,75,74,.15); border: 1px solid rgba(226,75,74,.4); color: #e24b4a; padding: 2px 10px; border-radius: 20px; font-size: 10px; font-family: 'IBM Plex Mono', monospace; margin-top: 6px; }
.kpi-card { background: #161b22; border: 1px solid #21262d; border-radius: 10px; padding: 16px 18px; position: relative; overflow: hidden; text-align: center !important; }
.kpi-card .kpi-label, .kpi-card .kpi-value, .kpi-card .kpi-sub { text-align: center !important; }
.kpi-card::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px; }
.kpi-card.red::after { background: #e24b4a; }
.kpi-card.amber::after { background: #ba7517; }
.kpi-card.blue::after { background: #378add; }
.kpi-card.purple::after { background: #7f77dd; }
.kpi-card.green::after { background: #639922; }
.kpi-card.cyan::after { background: #39d2c0; }
.kpi-label { font-size: 10px; font-family: 'IBM Plex Mono', monospace; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.kpi-value { font-size: 22px; font-weight: 700; line-height: 1; margin-bottom: 3px; }
.kpi-sub { font-size: 11px; color: #8b949e; }
.alert-box { background: rgba(226,75,74,.08); border: 1px solid rgba(226,75,74,.3); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; }
.alert-box.info { background: rgba(55,138,221,.08); border-color: rgba(55,138,221,.3); }
.alert-title { font-size: 12px; font-weight: 600; color: #e24b4a; margin-bottom: 2px; }
.alert-box.info .alert-title { color: #378add; }
.alert-body { font-size: 11px; color: #8b949e; }
.sec-label { font-size: 10px; font-family: 'IBM Plex Mono', monospace; color: #8b949e; text-transform: uppercase; letter-spacing: 2px; margin: 22px 0 12px; border-bottom: 1px solid #21262d; padding-bottom: 6px; }
.comor-card { background: #0d1117; border: 1px solid #21262d; border-radius: 8px; padding: 14px; text-align: center; }
.comor-val { font-size: 22px; font-weight: 700; margin-bottom: 2px; }
.comor-lbl { font-size: 10px; color: #8b949e; font-family: 'IBM Plex Mono', monospace; text-transform: uppercase; }
.sobre-card { background: #161b22; border: 1px solid #21262d; border-radius: 10px; padding: 20px; margin-bottom: 16px; }
.sobre-card h3 { margin-top: 0; color: #e6edf3; }
.sobre-card p { color: #8b949e; font-size: 13px; line-height: 1.7; }
.sobre-card ul { color: #8b949e; font-size: 13px; line-height: 1.8; }
.sobre-card strong { color: #c9d1d9; }
</style>
"""

CSS_LAYOUT = """
<style>
[data-testid="stSidebar"] { background: #0d1117 !important; border-right: 1px solid #21262d !important; }
[data-testid="stSidebar"] label { color: #8b949e !important; font-size: 12px !important; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; background: #161b22; border-radius: 10px; padding: 4px; border: 1px solid #21262d; flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 8px 14px; font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #8b949e; background: transparent; border: none; }
.stTabs [aria-selected="true"] { background: #21262d !important; color: #e6edf3 !important; }
.app-footer { margin-top: 32px; padding: 14px; border-top: 1px solid #21262d; font-size: 10px; font-family: 'IBM Plex Mono', monospace; color: #484f58; display: flex; justify-content: space-between; }
</style>
"""