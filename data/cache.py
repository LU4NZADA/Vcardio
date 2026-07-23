"""
Cache centralizado com decorators.
"""

import time
import pandas as pd
import streamlit as st
from functools import wraps
from logs.logger import logger


def cache_dataframe(func):
    @st.cache_data(show_spinner="Carregando dados...")
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        tempo_ms = (time.perf_counter() - inicio) * 1000
        if isinstance(resultado, pd.DataFrame):
            logger.info(f"[CACHE] {func.__qualname__}: {len(resultado):,} linhas, {tempo_ms:.1f} ms")
        return resultado
    return wrapper


def cache_analysis(func):
    @st.cache_data(show_spinner="Calculando indicadores...")
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        tempo_ms = (time.perf_counter() - inicio) * 1000
        logger.info(f"[CACHE] {func.__qualname__}: {tempo_ms:.1f} ms")
        return resultado
    return wrapper


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        tempo_ms = (time.perf_counter() - inicio) * 1000
        logger.info(f"[TIMED] {func.__qualname__}: {tempo_ms:.1f} ms")
        return resultado
    return wrapper


def invalidate():
    st.cache_data.clear()
    logger.info("[CACHE] Cache limpo")


@st.cache_data(ttl=0, show_spinner="Carregando dados...")
def cached_load(path_or_buffer):
    from data.loader import _ler_excel
    from data.validators import verificar_colunas
    from data.preprocess import processar_dados
    raw = _ler_excel(path_or_buffer)
    raw = verificar_colunas(raw)
    return processar_dados(raw)