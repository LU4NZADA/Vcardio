"""
Leitura pura do Excel.
"""

import pandas as pd


def _ler_excel(caminho):
    return pd.read_excel(caminho)