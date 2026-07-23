"""
Dataclasses para estruturas tipadas.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ResultadoAnalise:
    nome: str
    descricao: str
    dataframe: object
    gerado_em: datetime = field(default_factory=datetime.now)


@dataclass
class FiltroAplicado:
    campo: str
    tipo: str
    valores: list = field(default_factory=list)


@dataclass
class ExportConfig:
    incluir_csv: bool = True
    incluir_excel: bool = True
    incluir_pdf: bool = True
    prefixo_arquivo: str = "vigilancia_cardiovascular"