"""
==============================================================
 PAINEL INTELIGENTE DE VIGILANCIA CARDIOVASCULAR v3.6.1
 Projeto Saude Digital Movel - UFVJM
 PIBIC / Edital 005/2025
==============================================================
"""
import time
import streamlit as st
import pandas as pd
from pathlib import Path

from config.settings import settings

st.set_page_config(
    page_title=f"{settings.APP_NAME} v{settings.VERSION}",
    page_icon=settings.APP_ICON,
    layout=settings.LAYOUT,
    initial_sidebar_state=settings.SIDEBAR_STATE,
)

from styles import load_css
from logs.logger import logger, log_carregamento, log_erro, log_pipeline_total

load_css()
pipeline_inicio = time.perf_counter()
logger.info(f"Iniciando {settings.IDENTIFICACAO}")

from components.sidebar import render_header, render_footer

with st.sidebar:
    render_header()
    arquivo = st.file_uploader(
        "Carregar planilha (.xlsx)",
        type=list(settings.EXTENSOES_VALIDAS),
        help="Carregue o arquivo ecg.xlsx do Projeto Saude Digital Movel",
    )
    render_footer()

from data.cache import cached_load

if arquivo is not None:
    bytes_data = arquivo.getvalue()
    nome = arquivo.name
elif Path(settings.DADOS_PADRAO).exists():
    with open(settings.DADOS_PADRAO, "rb") as f:
        bytes_data = f.read()
    nome = settings.DADOS_PADRAO
else:
    st.warning("Carregue a planilha de exames (.xlsx) na barra lateral.")
    st.stop()

try:
    df_original = cached_load(bytes_data, nome)
    if df_original is None or not isinstance(df_original, pd.DataFrame) or df_original.empty:
        st.warning("Arquivo vazio ou sem dados validos.")
        st.stop()
    log_carregamento(nome, len(df_original), len(df_original.columns))
except Exception as e:
    log_erro("carregamento", e)
    st.error(f"Erro ao carregar: {e}")
    st.stop()

from services.dashboard import DashboardService
from components.filters import render_filtros

dashboard = DashboardService(df_original)
filtros = render_filtros(df_original)

if filtros is None:
    st.stop()

df, ind, alertas = dashboard.preparar(filtros)

if dashboard.vazio:
    st.warning("Nenhum registro encontrado com os filtros selecionados.")
    st.stop()

from components.topbar import render_topbar

render_topbar()
dashboard.render_abas(df, ind)

from components.footer import render_footer as render_app_footer

render_app_footer()

pipeline_total_ms = (time.perf_counter() - pipeline_inicio) * 1000
log_pipeline_total(pipeline_total_ms)