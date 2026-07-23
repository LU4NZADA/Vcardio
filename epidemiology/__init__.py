"""
Indicadores e analises populacionais.
"""

from epidemiology.prevalence import prevalencia_geral, prevalencia_por_grupo
from epidemiology.incidence import taxa_incidencia_periodo, tendencia_temporal
from epidemiology.alerts import gerar_alertas_epidemiologicos, formatar_alerta_html
from epidemiology.territorial import risco_territorial, classificar_municipios
from epidemiology.crosstab import matrix_achado_var, prev_comorb_por_achado
from epidemiology.comorbidades import resumo_comorbidades, comorb_por_sexo, comorb_por_faixa