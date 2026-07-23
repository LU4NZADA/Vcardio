"""
NLP para textos clinicos.
"""

import re
from collections import Counter
import pandas as pd
from constants import STOP_WORDS_PT


def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = texto.strip().lower()
    texto = re.sub(r"[^\w\sáeíóúâêîôûãõç]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def extrair_termos(textos, min_len=3, top_n=30):
    termos = Counter()
    for texto in textos.dropna():
        texto_norm = normalizar_texto(str(texto))
        palavras = re.findall(r"[a-záeíóúâêîôûãõç]+", texto_norm)
        for p in palavras:
            if len(p) >= min_len and p not in STOP_WORDS_PT:
                termos[p] += 1
    return pd.DataFrame(termos.most_common(top_n), columns=["Termo", "Frequencia"])


def gerar_nuvem_dados(textos, min_len=3, max_termos=100):
    termos = Counter()
    for texto in textos.dropna():
        texto_norm = normalizar_texto(str(texto))
        palavras = re.findall(r"[a-záeíóúâêîôûãõç]+", texto_norm)
        for p in palavras:
            if len(p) >= min_len and p not in STOP_WORDS_PT:
                termos[p] += 1
    return dict(termos.most_common(max_termos))