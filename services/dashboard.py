"""
Servico de orquestracao do dashboard.
"""

import pandas as pd
import streamlit as st
from data.indicators import calcular_indicadores
from epidemiology.alerts import gerar_alertas_epidemiologicos
from logs.logger import logger, log_filtros, log_indicadores


class DashboardService:
    def __init__(self, df_original):
        self.df_original = df_original
        self.df_filtrado = None
        self.indicadores = None
        self.alertas = []

    @property
    def vazio(self):
        return self.df_filtrado is None or len(self.df_filtrado) == 0

    def aplicar_filtros(self, filtros):
        from components.filters import aplicar_filtros as _aplicar
        self.df_filtrado = _aplicar(self.df_original, filtros)
        log_filtros(len(self.df_original), len(self.df_filtrado))
        return self

    def calcular_indicadores(self):
        self.indicadores = calcular_indicadores(self.df_filtrado)
        log_indicadores(self.indicadores)
        return self.indicadores

    def gerar_alertas(self):
        self.alertas = gerar_alertas_epidemiologicos(self.df_filtrado, self.indicadores)
        self.indicadores["alertas"] = self.alertas
        return self.alertas

    def preparar(self, filtros):
        self.aplicar_filtros(filtros)
        if self.vazio:
            return self.df_filtrado, {}, []
        self.calcular_indicadores()
        self.gerar_alertas()
        self.indicadores["n_total"] = len(self.df_original)
        self.indicadores["n_muns_total"] = self.df_original["Cidade"].nunique()
        return self.df_filtrado, self.indicadores, self.alertas

    def render_abas(self, df, ind):
        from pages import (
            geral, demografia, ecg, comorbidades as comorb_page,
            correlacoes, municipios, clinica, dados, distancias, sobre,
        )

        tabs = st.tabs([
            "Geral", "Demografia", "Arritmias", "Bloqueios",
            "ECG", "Comorbidades", "Correlacoes", "Municipios",
            "Distancias", "Clinica", "Dados", "Sobre",
        ])

        with tabs[0]:
            geral.render(df, ind)
        with tabs[1]:
            demografia.render(df, ind)
        with tabs[2]:
            ecg.render_arritmias(df, ind)
        with tabs[3]:
            ecg.render_bloqueios(df, ind)
        with tabs[4]:
            ecg.render_ecg_alteracoes(df, ind)
        with tabs[5]:
            comorb_page.render(df, ind)
        with tabs[6]:
            correlacoes.render(df, ind)
        with tabs[7]:
            municipios.render(df, ind)
        with tabs[8]:
            distancias.render(df, ind)
        with tabs[9]:
            clinica.render(df, ind)
        with tabs[10]:
            dados.render(df, ind)
        with tabs[11]:
            sobre.render()