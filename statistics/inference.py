"""
Testes de hipotese.
"""

import pandas as pd
import numpy as np
from scipy import stats


def teste_associacao(var1, var2):
    tab = pd.crosstab(var1, var2)
    if tab.shape[0] < 2 or tab.shape[1] < 2:
        return {"erro": "Tabela insuficiente"}
    chi2, p, dof, esperado = stats.chi2_contingency(tab)
    n = tab.sum().sum()
    k = min(tab.shape) - 1
    v = np.sqrt(chi2 / (n * k)) if k > 0 and n > 0 else 0
    fisher_p = None
    if (esperado < 5).any() and tab.shape == (2, 2):
        _, fisher_p = stats.fisher_exact(tab)
    return {
        "tabela": tab, "qui_quadrado": round(chi2, 4), "gl": dof,
        "p_qui_quadrado": round(p, 6),
        "fisher_p": round(fisher_p, 6) if fisher_p else None,
        "v_cramer": round(v, 4), "significativo_005": (fisher_p if fisher_p else p) < 0.05,
    }


def teste_mannwhitney(s1, s2):
    s1, s2 = s1.dropna(), s2.dropna()
    if len(s1) < 3 or len(s2) < 3:
        return {"erro": "Dados insuficientes"}
    stat, p = stats.mannwhitneyu(s1, s2, alternative="two-sided")
    return {
        "n1": len(s1), "n2": len(s2),
        "mediana1": round(s1.median(), 2), "mediana2": round(s2.median(), 2),
        "U_stat": round(stat, 2), "p_valor": round(p, 6),
        "significativo_005": p < 0.05,
    }