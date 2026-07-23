"""
Traducao de textos visiveis para portugues correto.
Usar: from utils.textos import t
Exemplo: t("Distribuicao etaria") -> "Distribuição etária"
"""

CORRECOES = {
    # Municipio
    "municipio": "município",
    "Municipio": "Município",
    "municipios": "municípios",
    "Municipios": "Municípios",
    "Municipio (MG)": "Município (MG)",

    # Diagnostico
    "diagnostico": "diagnóstico",
    "Diagnostico": "Diagnóstico",
    "Diagnosticos": "Diagnósticos",

    # Distribuicao
    "Distribuicao": "Distribuição",
    "distribuicao": "distribuição",

    # Demografica
    "demografica": "demográfica",
    "Demografica": "Demográfica",

    # Etaria
    "etaria": "etária",
    "Etaria": "Etária",
    "etario": "etário",
    "Etario": "Etário",

    # Clinica
    "clinica": "clínica",
    "Clinica": "Clínica",
    "clinico": "clínico",
    "Clinico": "Clínico",
    "clinicos": "clínicos",

    # Epidemiologico
    "epidemiologico": "epidemiológico",
    "Epidemiologico": "Epidemiológico",
    "epidemiologica": "epidemiológica",
    "Epidemiologica": "Epidemiológica",

    # Hipotese
    "hipotese": "hipótese",
    "Hipotese": "Hipótese",
    "hipoteses": "hipóteses",
    "Hipoteses": "Hipóteses",

    # Indicacao
    "indicacao": "indicação",
    "Indicacao": "Indicação",
    "indicacoes": "indicações",
    "Indicacoes": "Indicações",

    # Frequencia
    "frequencia": "frequência",
    "Frequencia": "Frequência",

    # Correlacoes
    "Correlacoes": "Correlações",
    "correlacoes": "correlações",

    # Comorbidade
    "comorbidade": "comorbidade",
    "Comorbidade": "Comorbidade",

    # Populacao
    "Populacao": "População",
    "populacao": "população",
    "Populacional": "Populacional",

    # IneVigilancia
    "Vigilancia": "Vigilância",
    "vigilancia": "vigilância",

    # Saude
    "Saude": "Saúde",
    "saude": "saúde",

    # Movel
    "Movel": "Móvel",
    "movel": "móvel",

    # Evolucao
    "Evolucao": "Evolução",
    "evolucao": "evolução",

    # Distancia
    "Distancia": "Distância",
    "distancia": "distância",
    "Distancias": "Distâncias",
    "distancias": "distâncias",

    # Analise
    "Analise": "Análise",
    "analise": "análise",

    # Prevalencia
    "Prevalencia": "Prevalência",
    "prevalencia": "prevalência",

    # Incidencia
    "Incidencia": "Incidência",
    "incidencia": "incidência",

    # Exportacao
    "Exportacao": "Exportação",
    "exportacao": "exportação",

    # Alteracao
    "Alteracao": "Alteração",
    "alteracao": "alteração",
    "Alteracoes": "Alterações",
    "alteracoes": "alterações",

    # Observacoes
    "Observacoes": "Observações",
    "observacoes": "observações",

    # Classificacao
    "Classificacao": "Classificação",
    "classificacao": "classificação",

    # Validacao
    "Validacao": "Validação",
    "validacao": "validação",

    # Configuracao
    "Configuracao": "Configuração",
    "configuracao": "configuração",

    # Informacoes
    "Informacoes": "Informações",
    "informacoes": "informações",

    # Sazonalidade
    "Sazonalidade": "Sazonalidade",

    # Versao
    "Versao": "Versão",
    "versao": "versão",

    # Protecao
    "Protecao": "Proteção",
    "protecao": "proteção",

    # Palavras comuns
    "nao": "não",
    "Nao": "Não",
    "minimo": "mínimo",
    "Minimo": "Mínimo",
    "minima": "mínima",
    "media": "média",
    "Media": "Média",
    "medio": "médio",
    "Medio": "Médio",
    "cardiaco": "cardíaco",
    "cardiaca": "cardíaca",
    "Cardiaco": "Cardíaco",
    "automaticos": "automáticos",
    "Automaticos": "Automáticos",
    "automatico": "automático",
    "Automatico": "Automático",
    "importancia": "importância",
    "Importancia": "Importância",
    "critico": "crítico",
    "Critico": "Crítico",
    "obrigatoria": "obrigatória",
    "Obrigatoria": "Obrigatória",
    "Repolarizacao": "Repolarização",
    "repolarizacao": "repolarização",
    "Conducao": "Condução",
    "conducao": "condução",
    "Frequencia": "Frequência",
    "frequencia": "frequência",

    # Termos especificos do painel
    "Achados mais frequentes": "Achados mais frequentes",
    "Mapa interativo": "Mapa interativo",
    "Mapa de achados por categoria": "Mapa de achados por categoria",
    "Mapa de achados ECG": "Mapa de achados ECG",
    "Mapa de todos os achados ECG": "Mapa de todos os achados ECG",
    "Ficha detalhada do municipio": "Ficha detalhada do município",
    "Ver detalhes de um municipio (opcional)": "Ver detalhes de um município (opcional)",
    "Selecione o municipio": "Selecione o município",
    "Selecione um municipio no mapa para ver detalhes": "Selecione um município no mapa para ver detalhes",
    "Municipio (MG)": "Município (MG)",
    "Ranking epidemiologico": "Ranking epidemiológico",
    "Municipio x Arritmia": "Município x Arritmia",
    "Municipio x Bloqueio": "Município x Bloqueio",
    "Arritmias por municipio": "Arritmias por município",
    "Bloqueios por municipio": "Bloqueios por município",
    "Distribuicao territorial": "Distribuição territorial",
    "Distribuicao demografica": "Distribuição demográfica",
    "Distribuicao por faixa etaria": "Distribuição por faixa etária",
    "Distribuicao por sexo": "Distribuição por sexo",
    "Diagnostico ECG": "Diagnóstico ECG",
    "Exames por ano": "Exames por ano",
    "Exames por faixa etaria": "Exames por faixa etária",
    "Piramide etaria por sexo": "Pirâmide etária por sexo",
    "Piramide etaria": "Pirâmide etária",
    "Top 15 municipios": "Top 15 municípios",
    "Sazonalidade dos exames": "Sazonalidade dos exames",
    "Achados ECG encontrados": "Achados ECG encontrados",
    "Achados ECG": "Achados ECG",
    "Exames realizados": "Exames realizados",
    "Analise de Textos Clinicos": "Análise de Textos Clínicos",
    "Nenhuma coluna qualitativa encontrada na planilha.": "Nenhuma coluna qualitativa encontrada na planilha.",
    "Dados anonimizados": "Dados anonimizados",
    "laudos alterados": "laudos alterados",
    "Laudos alterados": "Laudos alterados",
    "exames realizados": "exames realizados",
    "ida e volta para todas as cidades": "ida e volta para todas as cidades",
    "ida e volta media": "ida e volta média",
    "rota otimizada (MST)": "rota otimizada (MST)",
    "ponto de partida da equipe": "ponto de partida da equipe",
    "fora de MG ignoradas": "fora de MG ignoradas",
    "Exames por faixa": "Exames por faixa",
    "Arritmias x Faixa": "Arritmias x Faixa",
    "Arritmias x Sexo": "Arritmias x Sexo",
    "Bloqueios x Faixa": "Bloqueios x Faixa",
    "Bloqueios x Sexo": "Bloqueios x Sexo",
    "Comorbidades x Arritmia": "Comorbidades x Arritmia",
    "Comorbidades x Bloqueio": "Comorbidades x Bloqueio",
    "Arritmias por faixa etaria": "Arritmias por faixa etária",
    "Bloqueios por faixa etaria": "Bloqueios por faixa etária",
    "Distribuicao etaria por achado": "Distribuição etária por achado",
    "Mapa de risco epidemiologico": "Mapa de risco epidemiológico",
    "Deslocamento da equipe": "Deslocamento da equipe",
    "Rotas detalhadas (Top 20)": "Rotas detalhadas (Top 20)",
    "Pares de municipios mais distantes entre si": "Pares de municípios mais distantes entre si",
    "Distancia de Diamantina ate cada municipio de MG": "Distância de Diamantina até cada município de MG",
    "Rede de deslocamento entre municipios de MG": "Rede de deslocamento entre municípios de MG",
    "Risco Territorial": "Risco Territorial",
    "Sobre o Projeto": "Sobre o Projeto",
    "Periodo": "Período",
    "taxa de alteracao": "taxa de alteração",
    "Taxa de alteracao": "Taxa de alteração",
    "Nenhuma arritmia encontrada": "Nenhuma arritmia encontrada",
    "Nenhum bloqueio encontrado": "Nenhum bloqueio encontrado",
    "Nenhum achado": "Nenhum achado",
    "Nenhum achado ECG neste municipio": "Nenhum achado ECG neste município",
    "Nenhum municipio": "Nenhum município",
    "nenhum municipio": "nenhum município",
    "Nenhum exame encontrado para": "Nenhum exame encontrado para",
    "Nenhuma coluna qualitativa encontrada": "Nenhuma coluna qualitativa encontrada",
    "Buscar nos campos clinicos": "Buscar nos campos clínicos",
    "Buscar na tabela": "Buscar na tabela",
    "Top 20": "Top 20",
    "Top 10": "Top 10",
    "Registro(s) para": "Registro(s) para",
    "registros": "registros",
    "não encontrado": "não encontrado",
    "Nao informado": "Não informado",
    "Nao especificado": "Não especificado",
    "Arquivo nao encontrado": "Arquivo não encontrado",
    "Erro ao carregar": "Erro ao carregar",
}


def t(texto):
    """Aplica correcoes de portugues apenas no texto visivel."""
    if not isinstance(texto, str):
        return texto
    resultado = texto
    for errado, correto in CORRECOES.items():
        resultado = resultado.replace(errado, correto)
    return resultado