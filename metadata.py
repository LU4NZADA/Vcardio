"""
Metadados do projeto. Versao segue Semantic Versioning.
"""

from config.settings import settings

VERSAO = settings.VERSION
VERSAO_TITULO = settings.VERSION_TITULO
PROJETO = settings.PROJETO
INSTITUICAO = settings.INSTITUICAO
SIGLA_INSTITUICAO = settings.SIGLA
CAMPUS = settings.CAMPUS
MINISTERIO = settings.MINISTERIO
PROGRAMA = settings.PROGRAMA
EDITAL = settings.EDITAL
ANO = settings.ANO
AUTOR_PRINCIPAL = settings.AUTOR
REGIAO = settings.REGIAO
ESTADO = settings.ESTADO
PAIS = settings.PAIS
LGPD_LEI = settings.LGPD_LEI
LGPD_DESCRICAO = settings.LGPD_DESCRICAO
DADOS_ANONIMIZADOS = settings.DADOS_ANONIMIZADOS
DATA_BUILD = settings.DATA_BUILD


def info_completa() -> str:
    return f"""
{settings.IDENTIFICACAO}
{settings.PROJETO} - {settings.SIGLA}
{settings.PROGRAMA} / Edital {settings.EDITAL}
Autor: {settings.AUTOR}
Regiao: {settings.REGIAO}, {settings.ESTADO}, {settings.PAIS}
Build: {settings.DATA_BUILD}
LGPD: {settings.LGPD_LEI} ({settings.LGPD_DESCRICAO})
""".strip()