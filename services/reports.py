"""
Servico de relatorios.
"""

import pandas as pd
from analysis.textos import gerar_resumo_textual, gerar_paragrafo_completo
from statistics.descriptive import resumo_completo
from epidemiology.prevalence import prevalencia_geral


class ReportService:
    def __init__(self, df, ind):
        self.df = df
        self.ind = ind

    def texto_completo(self):
        return gerar_paragrafo_completo(self.df, self.ind)

    def resumo_executivo(self):
        return {
            "total_exames": self.ind["n"],
            "municipios": self.ind["n_muns"],
            "idade_media": self.ind["avg_age"],
            "pct_alterados": self.ind["alt_pct"],
            "texto_narrativo": self.texto_completo(),
        }