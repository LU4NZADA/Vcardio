"""
Esquemas de validacao.
"""

import pandas as pd

COLUNAS_OBRIGATORIAS = ["Data_Nascimento", "Data_cadastro", "Cidade", "Sexo"]
COLUNAS_COMORBIDADES = ["Hipertenso", "Diabetes Mellitus", "Tabagista", "Etilista"]

COLUNAS_CLINICAS = {
    "_obs": ["Observacoes", "Observacoes", "Obs"],
    "_indicacao": ["Indicacao Clinica", "Indicacao Clinica", "Indicacao"],
    "_hipotese": ["Hipotese Diagnostica", "Hipotese Diagnóstica"],
}


def validar_schema(df):
    avisos = []
    for col in COLUNAS_OBRIGATORIAS:
        if col not in df.columns:
            avisos.append(f"Coluna obrigatoria ausente: '{col}'")
    if len(df) == 0:
        avisos.append("DataFrame vazio")
    return avisos