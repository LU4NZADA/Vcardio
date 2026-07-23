"""
Alertas epidemiologicos - funcoes individuais.
"""

import pandas as pd
from models.enums import NivelAlerta


def alerta_arritmia(n_arr, n_total, limiar=8.0):
    if n_total == 0:
        return None
    pct = round(100 * n_arr / n_total, 1)
    if pct > limiar:
        return {"nivel": NivelAlerta.ALTO, "titulo": "Alta prevalencia de arritmias",
                "descricao": f"{pct}% dos laudos indicam arritmia ({n_arr} de {n_total}).",
                "recomendacao": "Investigar fatores de risco associados."}
    return None


def alerta_hipertensao(ind, limiar=55.0):
    n = ind["n"]
    if n == 0:
        return None
    pct_hip = 0
    for _, label, total, pct in ind["comorb_resumo"]:
        if label == "HAS":
            pct_hip = total / n * 100
            break
    if pct_hip > limiar:
        return {"nivel": NivelAlerta.ALTO, "titulo": "Alto indice de hipertensao",
                "descricao": f"{round(pct_hip,1)}% dos pacientes sao hipertensos.",
                "Recomendacao": "Reforcar acoes de educacao em saude."}
    return None


def alerta_idade(avg_age, limiar=65.0):
    if avg_age > limiar:
        return {"nivel": NivelAlerta.INFO, "titulo": "Perfil etario elevado",
                "descricao": f"Idade media de {avg_age} anos.", "recomendacao": ""}
    return None


def alerta_bloqueios(n_blk, n_total, limiar=10.0):
    if n_total == 0:
        return None
    pct = round(100 * n_blk / n_total, 1)
    if pct > limiar:
        return {"nivel": NivelAlerta.MEDIO, "titulo": "Prevalencia elevada de bloqueios",
                "descricao": f"{pct}% apresentam bloqueios.", "recomendacao": ""}
    return None


def alerta_wpw(n_wpw):
    if n_wpw > 0:
        return {"nivel": NivelAlerta.MEDIO, "titulo": "WPW detectados",
                "descricao": f"{n_wpw} caso(s) identificado(s).", "recomendacao": ""}
    return None


def alerta_municipios_criticos(risco_df, limiar=75.0, min_exames=5):
    critico = risco_df[(risco_df["total"] >= min_exames) & (risco_df["pct"] > limiar)]
    if len(critico) > 0:
        nomes = ", ".join(critico["Cidade"].head(3).tolist())
        return {"nivel": NivelAlerta.ALTO, "titulo": "Municipios com risco critico",
                "descricao": f"{len(critico)} municipio(s): {nomes}.",
                "recomendacao": "Priorizar acoes de saude cardiovascular."}
    return None


def gerar_alertas_epidemiologicos(df, ind):
    alertas = []
    for fn, args, kwargs in [
        (alerta_arritmia, (ind["n_arr"], ind["n"]), {}),
        (alerta_hipertensao, (ind,), {}),
        (alerta_idade, (ind["avg_age"],), {}),
        (alerta_bloqueios, (ind["n_blk"], ind["n"]), {}),
        (alerta_wpw, (ind["n_wpw"],), {}),
        (alerta_municipios_criticos, (ind["risco_municipio"],), {}),
    ]:
        resultado = fn(*args, **kwargs)
        if resultado is not None:
            alertas.append(resultado)
    return alertas


def formatar_alerta_html(alerta):
    nivel = alerta["nivel"]
    css = "alert-box info" if nivel == NivelAlerta.INFO else "alert-box"
    icone = "i" if nivel == NivelAlerta.INFO else "!"
    return f'<div class="{css}"><div class="alert-title">{icone} {alerta["titulo"]}</div><div class="alert-body">{alerta["descricao"]}</div></div>'