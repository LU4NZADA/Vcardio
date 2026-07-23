"""
Servico de exportacao.
"""

import pandas as pd
from exports.csv import gerar_csv
from exports.excel import gerar_excel
from exports.pdf import gerar_pdf
from logs.logger import log_exportacao


class ExportService:
    def __init__(self, df, tabela, ind):
        self.df = df
        self.tabela = tabela
        self.ind = ind

    def csv(self):
        r = gerar_csv(self.tabela)
        log_exportacao("CSV", True)
        return r

    def excel(self):
        r = gerar_excel(self.tabela, self.ind)
        log_exportacao("Excel", True)
        return r

    def pdf(self):
        r = gerar_pdf(self.df, self.ind)
        log_exportacao("PDF", r is not None)
        return r