"""
Classificacao de diagnosticos ECG.
"""

import pandas as pd
from constants import GRUPOS, ECG_ACHADOS

PRIORIDADE_DIAGNOSTICO = {
    "Arritmia": 1, "Bloqueio de Ramo": 2,
    "Sobrecarga Ventricular": 3, "Alteracao de Repolarizacao": 4,
    "Outras Alteracoes": 5, "Normal": 99,
}


def categorizar_diagnostico(row):
    for cat, cols in GRUPOS.items():
        for c in cols:
            if c in row.index and row[c] == 1:
                return cat
    if "Ritmo sinusal" in row.index and row["Ritmo sinusal"] == 1:
        return "Normal"
    return "Outras Alteracoes"


def priorizar_achados(row, categorias=None):
    if categorias is None:
        categorias = GRUPOS
    encontrados = []
    for cat, cols in categorias.items():
        if cat == "Normal":
            continue
        for c in cols:
            if c in row.index and row[c] == 1:
                encontrados.append(cat)
                break
    encontrados = list(dict.fromkeys(encontrados))
    if not encontrados:
        return {"principal": "Normal", "secundarios": [], "total_achados": 0}
    encontrados.sort(key=lambda x: PRIORIDADE_DIAGNOSTICO.get(x, 99))
    return {
        "principal": encontrados[0],
        "secundarios": encontrados[1:],
        "total_achados": len(encontrados),
    }


def classificar_achados(df):
    df = df.copy()
    for cat, subcats in ECG_ACHADOS.items():
        for nome, cols in subcats.items():
            col_name = f"_ach_{nome}"
            existentes = [c for c in cols if c in df.columns]
            df[col_name] = df[existentes].eq(1).any(axis=1).astype(int) if existentes else 0
    return df