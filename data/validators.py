"""
Garante colunas obrigatorias.
"""

from constants import ECG_ACHADOS


def _encontrar_col(df, candidatos):
    for c in candidatos:
        if c in df.columns:
            return c
    return None


def verificar_colunas(df):
    for col in ["Hipertenso", "Diabetes Mellitus", "Tabagista", "Etilista", "Marcapasso"]:
        if col not in df.columns:
            df[col] = 0
        df[col] = df[col].fillna(0).astype(int)

    for col in ["Data_Nascimento", "Data_cadastro"]:
        if col not in df.columns:
            df[col] = None

    if "Cidade" not in df.columns:
        df["Cidade"] = "Nao informado"
    if "Sexo" not in df.columns:
        df["Sexo"] = "Nao especificado"

    obs_cands = ["Observacoes", u"Observa\u00e7\u00f5es", "Obs"]
    ind_cands = ["Indicacao Clinica", u"Indica\u00e7\u00e3o Cl\u00ednica", u"Indica\u00e7\u00e3o"]
    hip_cands = ["Hipotese Diagnostica", u"Hip\u00f3tese Diagn\u00f3stica"]

    for alias, cands in [("_obs", obs_cands), ("_indicacao", ind_cands), ("_hipotese", hip_cands)]:
        found = _encontrar_col(df, cands)
        if found:
            df[alias] = df[found]
        else:
            df[alias] = ""

    for cat, subcats in ECG_ACHADOS.items():
        for nome, cols in subcats.items():
            for c in cols:
                if c not in df.columns:
                    df[c] = 0

    if "Ritmo sinusal" not in df.columns:
        df["Ritmo sinusal"] = 0

    return df