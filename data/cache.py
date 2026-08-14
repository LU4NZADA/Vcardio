# VCARDIO cache v2 - atualizado

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


@st.cache_data(show_spinner="Carregando dados...")
def cached_load(bytes_data, filename):
    """Recebe bytes puros (hashable pelo Streamlit)."""
    import io
    from data.loader import _ler_excel
    from data.validators import verificar_colunas
    from data.preprocess import processar_dados

    buffer = io.BytesIO(bytes_data)
    raw = _ler_excel(buffer)

    if raw is None or raw.empty:
        return pd.DataFrame()

    raw = verificar_colunas(raw)
    result = processar_dados(raw)

    if result is None:
        return pd.DataFrame()

    return result