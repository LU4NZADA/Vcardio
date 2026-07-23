"""
Enumeracoes do projeto.
"""

from enum import Enum


class Sexo(Enum):
    MASCULINO = "Masculino"
    FEMININO = "Feminino"
    NAO_ESPECIFICADO = "Nao especificado"

    @classmethod
    def valores(cls):
        return [e.value for e in cls]


class DiagnosticoECG(Enum):
    NORMAL = "Normal"
    ARRITMIA = "Arritmia"
    BLOQUEIO = "Bloqueio de Ramo"
    REPOLARIZACAO = "Alteracao de Repolarizacao"
    SOBRECARGA = "Sobrecarga Ventricular"
    OUTRAS = "Outras Alteracoes"

    @classmethod
    def valores(cls):
        return [e.value for e in cls]


class NivelRisco(Enum):
    BAIXO = "Baixo"
    MODERADO = "Moderado"
    ALTO = "Alto"
    CRITICO = "Critico"


class NivelAlerta(Enum):
    INFO = "info"
    MEDIO = "medio"
    ALTO = "alto"


class Comorbidade(Enum):
    HAS = ("Hipertenso", "HAS")
    DM = ("Diabetes Mellitus", "DM")
    TABAGISMO = ("Tabagista", "Tabagismo")
    ETILISMO = ("Etilista", "Etilismo")

    def __init__(self, col_planilha, rotulo):
        self.col_planilha = col_planilha
        self.rotulo = rotulo