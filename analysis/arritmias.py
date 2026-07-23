"""
Logica de negocio para arritmias.
"""

from analysis.ecg import achados_df, contar_achado
from constants import ECG_ACHADOS


def subcats():
    return ECG_ACHADOS["Arritmias"]


def ranking(df):
    return achados_df(df, subcats())


def contar_total(df):
    return contar_achado(df, [c for v in subcats().values() for c in v])