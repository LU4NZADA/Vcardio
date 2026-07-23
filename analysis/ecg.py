"""
Operacoes sobre achados ECG.
"""

import re
from collections import Counter
import pandas as pd
from constants import STOP_WORDS_PT


def achado_mask(df, colunas):
    existentes = [c for c in colunas if c in df.columns]
    if not existentes:
        return pd.Series(False, index=df.index)
    return df[existentes].eq(1).any(axis=1)


def contar_achado(df, colunas):
    return int(achado_mask(df, colunas).sum())


def achados_df(df, subcats):
    rows = []
    n = len(df)
    for nome, cols in subcats.items():
        cnt = contar_achado(df, cols)
        if cnt > 0:
            pct = round(100 * cnt / n, 1) if n else 0
            rows.append({"Achado": nome, "Casos": cnt, "%": pct})
    if not rows:
        return pd.DataFrame(columns=["Achado", "Casos", "%"])
    return pd.DataFrame(rows).sort_values("Casos", ascending=False).reset_index(drop=True)


def extrair_termos(textos, min_len=3, top_n=30):
    termos = Counter()
    for texto in textos.dropna():
        palavras = re.findall(r"[a-zA-Záeíóúâêîôûãõç]+", str(texto).lower())
        for p in palavras:
            if len(p) >= min_len and p not in STOP_WORDS_PT:
                termos[p] += 1
    return pd.DataFrame(termos.most_common(top_n), columns=["Termo", "Frequencia"])