"""
Configuracao central tipada. Fonte unica de verdade.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Final


@dataclass(frozen=True)
class AppSettings:
    APP_NAME: str = "Painel Cardiovascular | UFVJM"
    APP_ICON: str = "\U0001fac0"
    VERSION: str = "3.6.1"
    VERSION_TITULO: str = "Painel Inteligente de Vigilancia Cardiovascular"

    PROJETO: str = "Saude Digital Movel"
    INSTITUICAO: str = "Universidade Federal dos Vales do Jequitinhonha e Mucuri"
    SIGLA: str = "UFVJM"
    CAMPUS: str = "JK"
    MINISTERIO: str = "Ministerio da Saude"
    PROGRAMA: str = "PIBIC"
    EDITAL: str = "005/2025"
    ANO: int = 2025
    AUTOR: str = "Prof. Mariana Roberta Lopes Simoes"

    REGIAO: str = "Vale do Jequitinhonha"
    ESTADO: str = "Minas Gerais"
    PAIS: str = "Brasil"

    LGPD_LEI: str = "Lei nº 13.709/2018"
    LGPD_DESCRICAO: str = "LGPD"
    DADOS_ANONIMIZADOS: bool = True

    DADOS_PADRAO: str = "ecg.xlsx"
    EXTENSOES_VALIDAS: tuple = ("xlsx",)
    IDADE_MIN: int = 1
    IDADE_MAX: int = 110

    LAYOUT: str = "wide"
    SIDEBAR_STATE: str = "expanded"

    LIMIAR_ARRITMIA: float = 8.0
    LIMIAR_HIPERTENSAO: float = 55.0
    LIMIAR_IDADE: float = 65.0
    LIMIAR_BLOQUEIO: float = 10.0
    LIMIAR_MUNICIPIO_CRITICO: float = 75.0
    MIN_EXAMES_MUNICIPIO: int = 5

    PREFIXO_ARQUIVO: str = "vigilancia_cardiovascular"

    @property
    def DATA_BUILD(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    @property
    def IDENTIFICACAO(self) -> str:
        return f"{self.VERSION_TITULO} v{self.VERSION}"

    @property
    def CREDITO(self) -> str:
        return f"PIBIC/UFVJM - Edital {self.EDITAL} - {self.AUTOR}"


settings: Final[AppSettings] = AppSettings()