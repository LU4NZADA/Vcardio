"""
Estatistica descritiva.
"""

import pandas as pd
import numpy as np
try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def resumo_completo(series, nome="Variavel"):
    s = series.dropna()
    n = len(s)
    if n < 2:
        return {"nome": nome, "n": n, "erro": "Dados insuficientes"}
    media = s.mean()
    desvio = s.std()
    se = desvio / np.sqrt(n)
    if HAS_SCIPY:
        t_crit = stats.t.ppf(0.975, df=n - 1)
    else:
        t_crit = 1.96
    return {
        "nome": nome, "n": n, "media": round(media, 2),
        "mediana": round(s.median(), 2), "desvio_padrao": round(desvio, 2),
        "minimo": round(s.min(), 2), "maximo": round(s.max(), 2),
        "q1": round(s.quantile(0.25), 2), "q3": round(s.quantile(0.75), 2),
        "ic_95_inf": round(media - t_crit * se, 2),
        "ic_95_sup": round(media + t_crit * se, 2),
    }


def resumo_por_grupo(series, grupos, nome_var="Valor"):
    rows = []
    for nome_grupo, sub in series.groupby(grupos):
        r = resumo_completo(sub, str(nome_grupo))
        if "erro" not in r:
            r["Grupo"] = str(nome_grupo)
            rows.append(r)
    return pd.DataFrame(rows).set_index("Grupo") if rows else pd.DataFrame()


def comparar_medias(series1, series2, nome1="G1", nome2="G2"):
    if not HAS_SCIPY:
        return {"erro": "scipy nao instalado"}
    s1, s2 = series1.dropna(), series2.dropna()
    if len(s1) < 2 or len(s2) < 2:
        return {"erro": "Dados insuficientes"}
    t_stat, t_p = stats.ttest_ind(s1, s2)
    pooled = np.sqrt(((len(s1)-1)*s1.var() + (len(s2)-1)*s2.var()) / (len(s1)+len(s2)-2))
    d = abs(s1.mean() - s2.mean()) / pooled if pooled > 0 else 0
    return {
        "nome_grupo1": nome1, "nome_grupo2": nome2,
        "n1": len(s1), "n2": len(s2),
        "media1": round(s1.mean(), 2), "media2": round(s2.mean(), 2),
        "t_stat": round(t_stat, 4), "t_p": round(t_p, 6),
        "significativo_005": t_p < 0.05,
        "d_cohen": round(d, 3),
    }