"""
Logging centralizado.
"""

import logging
import sys
from config.paths import LOG_DIR, path_log


def _criar_logger(nome="vcardio", nivel=logging.INFO):
    logger = logging.getLogger(nome)
    if logger.handlers:
        return logger
    logger.setLevel(nivel)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(nivel)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(str(path_log("app.log")), encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    return logger


logger = _criar_logger()


def log_carregamento(arquivo, n_linhas, n_colunas):
    logger.info(f"Planilha: {arquivo} | {n_linhas:,} linhas x {n_colunas} colunas")


def log_filtros(n_original, n_filtrado):
    pct = round(100 * n_filtrado / n_original, 1) if n_original else 0
    logger.info(f"Filtros: {n_original:,} -> {n_filtrado:,} ({pct}%)")


def log_indicadores(ind):
    logger.info(f"Indicadores: {ind['n']} exames, {ind['n_muns']} mun, {ind['n_arr']} arr")


def log_erro(contexto, erro):
    logger.error(f"[{contexto}] {type(erro).__name__}: {erro}")


def log_exportacao(formato, sucesso):
    logger.info(f"Exportacao {formato}: {'sucesso' if sucesso else 'falha'}")


def log_pipeline_total(tempo_ms):
    logger.info(f"[PIPELINE] Tempo total: {tempo_ms:.1f} ms")