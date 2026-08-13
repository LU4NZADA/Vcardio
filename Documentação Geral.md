# VCARDIO - Documentacao Tecnica Automatica
**Gerado em:** 13/08/2026 11:13

## Painel Inteligente de Vigilancia Cardiovascular
### Projeto Saude Digital Movel - UFVJM

---

## 1. Visao Geral

- **Total de arquivos Python:** 96
- **Total de linhas de codigo:** 6,483
- **Rodando:** `python -m streamlit run app.py --server.headless false`
- **Dados:** `ecg.xlsx`
- **Atualizar locais:** edite `Locais.xlsx`, rode `python gerar_locais2.py`

---

## 2. Estrutura de Pastas

```
./
  |-- app.py  # ==============================================================
  |-- constants.py  # Listas de achados ECG, grupos diagnostico, coordenadas e stopwords.
  |-- constants_locais.py
  |-- fix_dist.py
  |-- fix_rotas.py
  |-- gerar_doc.py  # Gerador automatico de documentacao do VCARDIO.
  |-- gerar_locais2.py
  |-- metadata.py  # Metadados do projeto. Versao segue Semantic Versioning.
  |-- styles.py  # Estilos globais do aplicativo.

.\analysis/
  |   # Motor de analise de dados (ECG, distancias, classificacao)
  |-- arritmias.py  # Logica de negocio para arritmias.
  |-- bloqueios.py  # Logica de negocio para bloqueios.
  |-- classificacao.py  # Classificacao de diagnosticos ECG.
  |-- distancias.py  # Calculo de distancias percorridas pelo Projeto Saude Digital Movel.
  |-- ecg.py  # Operacoes sobre achados ECG.
  |-- nlp.py  # NLP para textos clinicos.
  |-- textos.py  # Geracao automatica de textos narrativos.

.\benchmark/
  |   # Testes de performance
  |-- performance.py  # Benchmark de performance.

.\charts/
  |   # Graficos Plotly (mapas, barras, heatmaps, KPIs)
  |-- base.py  # Utilidades comuns para graficos Plotly com interatividade estilo Power BI.
  |-- clinical.py  # Graficos clinicos.
  |-- comorbidities.py  # Graficos de comorbidades.
  |-- demographics.py  # Graficos demograficos com interatividade estilo Power BI.
  |-- distancias.py  # Graficos de distancias percorridas pelo projeto.
  |-- ecg.py  # Gráficos ECG com interatividade.
  |-- heatmaps.py  # Heatmaps genericos.
  |-- kpis.py  # Cards KPI.
  |-- maps.py  # Mapas Scattermapbox com hover rico e legenda de cores.
  |-- municipalities.py  # Graficos municipais com interatividade.
  |-- temporal.py  # Graficos temporais com range slider interativo.

.\components/
  |   # Componentes de UI Streamlit (filtros, cards, alertas)
  |-- alerts.py
  |-- cards.py
  |-- filters.py
  |-- footer.py
  |-- metrics.py
  |-- sidebar.py
  |-- tables.py
  |-- topbar.py

.\config/
  |   # Configuracoes globais (cores, caminhos, constantes)
  |-- app.py  # Constantes do app.
  |-- colors.py  # Paleta de cores.
  |-- paths.py  # Caminhos via pathlib.Path.
  |-- plotly.py  # Tema Plotly.
  |-- settings.py  # Configuracao central tipada. Fonte unica de verdade.

.\data/
  |   # Carregamento, validacao, processamento e indicadores
  |-- cache.py  # Cache centralizado com decorators.
  |-- indicators.py  # Calcula todos os indicadores de uma unica vez.
  |-- loader.py  # Leitura pura do Excel.
  |-- preprocess.py
  |-- validators.py  # Garante colunas obrigatorias.

.\epidemiology/
  |   # Analises epidemiologicas (alertas, prevalencia, territorial)
  |-- alerts.py  # Alertas epidemiologicos - funcoes individuais.
  |-- comorbidades.py  # Analise epidemiologica de comorbidades.
  |-- crosstab.py  # Cruzamentos: achado x variavel.
  |-- incidence.py  # Taxas de incidencia e tendencias.
  |-- prevalence.py  # Prevalencias com IC 95%.
  |-- territorial.py  # Analise territorial.

.\examples/
  |   # Dados e scripts de exemplo
  |-- generate_fake.py  # Gera dados sinteticos para testes.

.\exports/
  |   # Exportacao de relatorios (CSV, Excel, PDF)
  |-- base.py  # Interfaces (Protocolos) para exportadores.
  |-- csv.py
  |-- excel.py
  |-- pdf.py
  |-- report.py

.\models/
  |   # Modelos de dados (dataclasses, enums, schemas)
  |-- classes.py  # Entidades do dominio.
  |-- dataclasses.py  # Dataclasses para estruturas tipadas.
  |-- enums.py  # Enumeracoes do projeto.
  |-- schemas.py  # Esquemas de validacao.
  |-- score.py  # Scores de risco cardiovascular.

.\pages/
  |   # Paginas do dashboard (abas visiveis ao usuario)
  |-- clinica.py
  |-- comorbidades.py
  |-- correlacoes.py
  |-- dados.py
  |-- demografia.py  # Pagina Demografia com grafico de pizza nativo do Streamlit.
  |-- distancias.py  # Pagina Distancias — deslocamento real da equipe pelo Projeto Saude Digital Movel.
  |-- ecg.py
  |-- geral.py
  |-- municipios.py
  |-- sobre.py  # Pagina Sobre o Projeto.

.\services/
  |   # Servicos de orquestracao (dashboard, exports, relatorios)
  |-- dashboard.py  # Servico de orquestracao do dashboard.
  |-- exports.py  # Servico de exportacao.
  |-- reports.py  # Servico de relatorios.

.\statistics/
  |   # Metodos estatisticos (correlacoes, inferencia, sobrevivencia)
  |-- correlations.py  # Correlacoes estatisticas.
  |-- descriptive.py  # Estatistica descritiva.
  |-- inference.py  # Testes de hipotese.
  |-- survival.py  # Analises temporais e tendencias.

.\tests/
  |   # Testes automatizados
  |-- test_benchmark.py
  |-- test_correlations.py
  |-- test_epidemiology.py
  |-- test_exports.py
  |-- test_indicators.py
  |-- test_interfaces.py
  |-- test_loader.py
  |-- test_preprocess.py
  |-- test_risk.py
  |-- test_settings.py
  |-- test_statistics.py
  |-- test_utils.py

.\utils/
  |   # Utilitarios (formatacao, texto, tipos)
  |-- formatters.py  # Formatacao de numeros, datas e porcentagens.
  |-- text.py  # Utilidades de texto.
  |-- textos.py  # Traducao de textos visiveis para portugues correto.
  |-- types.py  # Conversao segura de tipos.
```

---

## 3. Fluxo de Dados

```
ecg.xlsx
   |
   v
data/loader.py        -> _ler_excel()         -> DataFrame bruto
   |
   v
data/validators.py    -> verificar_colunas()   -> Normaliza colunas, cria _ach_*
   |
   v
data/preprocess.py    -> processar_dados()     -> Idade, sexo, diagnostico, distrito
   |
   v
components/filters.py -> aplicar_filtros()     -> Filtra por municipio, sexo, etc.
   |
   v
data/indicators.py    -> calcular_indicadores()-> KPIs, mapas, heatmaps, rankings
   |
   v
pages/*.py            -> render()              -> Graficos e tabelas na tela
```

---

## 4. Detalhes por Pasta e Arquivo

### 4.1 Raiz

#### `app.py`
> ==============================================================
- **Linhas:** 77

#### `constants.py`
> Listas de achados ECG, grupos diagnostico, coordenadas e stopwords.
- **Linhas:** 262

#### `constants_locais.py`
- **Linhas:** 216
- **Funcoes (6):**
  - `_norm(s)`
  - `buscar_distrito(data_cadastro, cidade)` - Busca distrito cruzando data + municipio.
  - `buscar_municipio_coleta(data_cadastro, cidade)` - Retorna o municipio onde o exame foi realizado.
  - `distrito_para_municipio(distrito)` - Retorna o municipio de um distrito.
  - `get_municipios_visitados()` - Retorna lista de municipios visitados.
  - `get_distritos_municipio(municipio)` - Retorna distritos de um municipio.

#### `fix_dist.py`
- **Linhas:** 29

#### `fix_rotas.py`
- **Linhas:** 239

#### `gerar_doc.py`
> Gerador automatico de documentacao do VCARDIO.
- **Linhas:** 316
- **Funcoes (4):**
  - `listar_arquivos(pasta, ext)`
  - `analisar_arquivo(caminho)`
  - `descricao_pasta(pasta)`
  - `gerar_documentacao()`

#### `gerar_locais2.py`
- **Linhas:** 150
- **Funcoes (1):**
  - `parse_periodo(data_str, ano)`

#### `metadata.py`
> Metadados do projeto. Versao segue Semantic Versioning.
- **Linhas:** 36
- **Funcoes (1):**
  - `info_completa()`

#### `styles.py`
> Estilos globais do aplicativo.
- **Linhas:** 74
- **Funcoes (1):**
  - `load_css()`

### 4.2 analysis
*Motor de analise de dados (ECG, distancias, classificacao)*

#### `analysis/arritmias.py`
> Logica de negocio para arritmias.
- **Linhas:** 18
- **Funcoes (3):**
  - `subcats()`
  - `ranking(df)`
  - `contar_total(df)`

#### `analysis/bloqueios.py`
> Logica de negocio para bloqueios.
- **Linhas:** 18
- **Funcoes (3):**
  - `subcats()`
  - `ranking(df)`
  - `contar_total(df)`

#### `analysis/classificacao.py`
> Classificacao de diagnosticos ECG.
- **Linhas:** 54
- **Funcoes (3):**
  - `categorizar_diagnostico(row)`
  - `priorizar_achados(row, categorias)`
  - `classificar_achados(df)`

#### `analysis/distancias.py`
> Calculo de distancias percorridas pelo Projeto Saude Digital Movel.
- **Linhas:** 167
- **Funcoes (4):**
  - `haversine(lat1, lon1, lat2, lon2)`
  - `_coords_municipio(nome)` - Busca coordenadas de um municipio, tentando com e sem acento
  - `_distrito_para_municipio(distrito_nome)` - Busca o municipio real de um distrito na tabela LOCAIS.
  - `calcular_distancias_distritos(df)` - Calcula rotas: Diamantina -> cada municipio -> Diamantina (i

#### `analysis/ecg.py`
> Operacoes sobre achados ECG.
- **Linhas:** 42
- **Funcoes (4):**
  - `achado_mask(df, colunas)`
  - `contar_achado(df, colunas)`
  - `achados_df(df, subcats)`
  - `extrair_termos(textos, min_len, top_n)`

#### `analysis/nlp.py`
> NLP para textos clinicos.
- **Linhas:** 38
- **Funcoes (3):**
  - `normalizar_texto(texto)`
  - `extrair_termos(textos, min_len, top_n)`
  - `gerar_nuvem_dados(textos, min_len, max_termos)`

#### `analysis/textos.py`
> Geracao automatica de textos narrativos.
- **Linhas:** 58
- **Funcoes (2):**
  - `gerar_resumo_textual(df, ind)`
  - `gerar_paragrafo_completo(df, ind)`

### 4.3 benchmark
*Testes de performance*

#### `benchmark/performance.py`
> Benchmark de performance.
- **Linhas:** 53
- **Funcoes (2):**
  - `medir_tempo(func)`
  - `medir_memoria(func)`
- **Classes (1):**
  - `BenchmarkSuite`
    - `__init__()`
    - `executar()`
    - `relatorio()`
    - `tempo_total()`

### 4.4 charts
*Graficos Plotly (mapas, barras, heatmaps, KPIs)*

#### `charts/base.py`
> Utilidades comuns para graficos Plotly com interatividade estilo Power BI.
- **Linhas:** 138
- **Funcoes (7):**
  - `aplicar_tema(fig)`
  - `configurar_layout(fig, height, title_size, showlegend)` - Layout padrao com hovermode e dragmode interativos.
  - `bar_horizontal(df, x, y, text, color, title, hover_extra)`
  - `heatmap_base(df, title, colorscale, height_per_row)`
  - `criar_dropdown(fig, botoes, titulo, y)`
  - `criar_range_slider(fig, visible)`
  - `animar_bars(fig, duracao)`

#### `charts/clinical.py`
> Graficos clinicos.
- **Linhas:** 29
- **Funcoes (2):**
  - `top_bar(df_freq, x_col, y_col, title, color)`
  - `termos_bar(termos_df)`

#### `charts/comorbidities.py`
> Graficos de comorbidades.
- **Linhas:** 37
- **Funcoes (3):**
  - `comorb_sexo(df_cs)`
  - `comorb_faixa(df_cf)`
  - `sexo_diag_crosstab(crosstab_df)`

#### `charts/demographics.py`
> Graficos demograficos com interatividade estilo Power BI.
- **Linhas:** 118
- **Funcoes (6):**
  - `sexo_pie(sexo_counts)`
  - `ano_bar(ano_counts)`
  - `faixa_bar(faixa_counts)`
  - `piramide(piram_df)`
  - `top_municipios(top_df)`
  - `sazonalidade(saz_df)`

#### `charts/distancias.py`
> Graficos de distancias percorridas pelo projeto.
- **Linhas:** 142
- **Funcoes (2):**
  - `grafico_rotas_distritos(dist)`
  - `grafico_mapa_distritos(dist)`

#### `charts/ecg.py`
> Gráficos ECG com interatividade.
- **Linhas:** 189
- **Funcoes (6):**
  - `achados_bar(df_ach, title, color)`
  - `achados_por_sexo(matrix_df, title)`
  - `achados_por_faixa(matrix_df, title, colorscale)`
  - `comorb_prevalencia(prev_df, title)`
  - `boxplot_idade(box_df, title)`
  - `treemap_achados(achados_dict, title)` - Treemap interativo com tamanhos proporcionais e hover detalh

#### `charts/heatmaps.py`
> Heatmaps genericos.
- **Linhas:** 28
- **Funcoes (2):**
  - `heatmap_generic(pivot_df, title, colorscale)`
  - `heatmap_percent(pivot_df, title, colorscale)`

#### `charts/kpis.py`
> Cards KPI.
- **Linhas:** 25
- **Funcoes (2):**
  - `render_kpi_row(kpis)`
  - `render_comorb_cards(comorb_data)`

#### `charts/maps.py`
> Mapas Scattermapbox com hover rico e legenda de cores.
- **Linhas:** 167
- **Funcoes (2):**
  - `mapa_risco(mapa_df, titulo_col)` - Mapa de risco com tamanhos proporcionais e hover detalhado.
  - `mapa_simples(mapa_df, cidade_destaque, df)` - Mapa simples de distribuicao com opcao de destaque.

#### `charts/municipalities.py`
> Graficos municipais com interatividade.
- **Linhas:** 101
- **Funcoes (2):**
  - `risco_territorial(risco_df)` - Ranking de risco com cores por nivel e hover detalhado.
  - `comorb_municipio(cm_df, label)` - Ranking de comorbidade por municipio — hover detalhado.

#### `charts/temporal.py`
> Graficos temporais com range slider interativo.
- **Linhas:** 54
- **Funcoes (2):**
  - `evolucao_mensal(tempo_df)` - Area empilhada mensal — com range slider e hover rico.
  - `taxa_alteracao(taxa_df)` - Linha com marcadores — range slider interativo.

### 4.5 components
*Componentes de UI Streamlit (filtros, cards, alertas)*

#### `components/alerts.py`
- **Linhas:** 28
- **Funcoes (1):**
  - `render_alerts(ind)`

#### `components/cards.py`
- **Linhas:** 3

#### `components/filters.py`
- **Linhas:** 119
- **Funcoes (4):**
  - `_init_session_defaults(df)`
  - `_limpar_filtros(df)`
  - `render_filtros(df_original)`
  - `aplicar_filtros(df, filtros)`

#### `components/footer.py`
- **Linhas:** 11
- **Funcoes (1):**
  - `render_footer()`

#### `components/metrics.py`
- **Linhas:** 8
- **Funcoes (1):**
  - `metric_row(metrics)`

#### `components/sidebar.py`
- **Linhas:** 13
- **Funcoes (2):**
  - `render_header()`
  - `render_footer()`

#### `components/tables.py`
- **Linhas:** 16
- **Funcoes (1):**
  - `render_tabela(df, rename_map, busca_label)`

#### `components/topbar.py`
- **Linhas:** 16
- **Funcoes (1):**
  - `render_topbar()`

### 4.6 config
*Configuracoes globais (cores, caminhos, constantes)*

#### `config/app.py`
> Constantes do app.
- **Linhas:** 18

#### `config/colors.py`
> Paleta de cores.
- **Linhas:** 18

#### `config/paths.py`
> Caminhos via pathlib.Path.
- **Linhas:** 37
- **Funcoes (5):**
  - `ensure_dir(path)`
  - `path_dados(nome)`
  - `path_asset(nome)`
  - `path_log(nome)`
  - `path_export(nome)`

#### `config/plotly.py`
> Tema Plotly.
- **Linhas:** 20
- **Funcoes (1):**
  - `chart_layout(fig, height, title_size, showlegend)`

#### `config/settings.py`
> Configuracao central tipada. Fonte unica de verdade.
- **Linhas:** 66
- **Classes (1):**
  - `AppSettings`
    - `DATA_BUILD()`
    - `IDENTIFICACAO()`
    - `CREDITO()`

### 4.7 data
*Carregamento, validacao, processamento e indicadores*

#### `data/cache.py`
> Cache centralizado com decorators.
- **Linhas:** 60
- **Funcoes (5):**
  - `cache_dataframe(func)`
  - `cache_analysis(func)`
  - `timed(func)`
  - `invalidate()`
  - `cached_load(path_or_buffer)`

#### `data/indicators.py`
> Calcula todos os indicadores de uma unica vez.
- **Linhas:** 228
- **Funcoes (2):**
  - `_value_counts_rename(series, col_nome, col_valor, sort_index, head)` - value_counts compativel com pandas 2.x e 3.x.
  - `calcular_indicadores(df)`

#### `data/loader.py`
> Leitura pura do Excel.
- **Linhas:** 9
- **Funcoes (1):**
  - `_ler_excel(caminho)`

#### `data/preprocess.py`
- **Linhas:** 59
- **Funcoes (1):**
  - `processar_dados(df)`

#### `data/validators.py`
> Garante colunas obrigatorias.
- **Linhas:** 63
- **Funcoes (2):**
  - `_encontrar_col(df, candidatos)`
  - `verificar_colunas(df)`

### 4.8 epidemiology
*Analises epidemiologicas (alertas, prevalencia, territorial)*

#### `epidemiology/alerts.py`
> Alertas epidemiologicos - funcoes individuais.
- **Linhas:** 90
- **Funcoes (8):**
  - `alerta_arritmia(n_arr, n_total, limiar)`
  - `alerta_hipertensao(ind, limiar)`
  - `alerta_idade(avg_age, limiar)`
  - `alerta_bloqueios(n_blk, n_total, limiar)`
  - `alerta_wpw(n_wpw)`
  - `alerta_municipios_criticos(risco_df, limiar, min_exames)`
  - `gerar_alertas_epidemiologicos(df, ind)`
  - `formatar_alerta_html(alerta)`

#### `epidemiology/comorbidades.py`
> Analise epidemiologica de comorbidades.
- **Linhas:** 41
- **Funcoes (3):**
  - `resumo_comorbidades(df)`
  - `comorb_por_sexo(df)`
  - `comorb_por_faixa(df)`

#### `epidemiology/crosstab.py`
> Cruzamentos: achado x variavel.
- **Linhas:** 34
- **Funcoes (2):**
  - `matrix_achado_var(df, subcats, var_col)`
  - `prev_comorb_por_achado(df, subcats, comorb_cols_map)`

#### `epidemiology/incidence.py`
> Taxas de incidencia e tendencias.
- **Linhas:** 8

#### `epidemiology/prevalence.py`
> Prevalencias com IC 95%.
- **Linhas:** 38
- **Funcoes (2):**
  - `prevalencia_geral(df, col_diag)`
  - `prevalencia_por_grupo(df, col_grupo, col_diag)`

#### `epidemiology/territorial.py`
> Analise territorial.
- **Linhas:** 60
- **Funcoes (4):**
  - `risco_territorial(df, min_exames)` - Risco territorial por municipio (cidade de origem).
  - `risco_territorial_distrito(df, min_exames)` - Risco territorial por distrito (local do exame).
  - `classificar_municipios(risco_df)`
  - `comorb_por_municipio(df, comorb_col, min_exames)`

### 4.9 examples
*Dados e scripts de exemplo*

#### `examples/generate_fake.py`
> Gera dados sinteticos para testes.
- **Linhas:** 69
- **Funcoes (1):**
  - `gerar_dados_sinteticos(n, seed)`

### 4.10 exports
*Exportacao de relatorios (CSV, Excel, PDF)*

#### `exports/base.py`
> Interfaces (Protocolos) para exportadores.
- **Linhas:** 26
- **Classes (3):**
  - `BaseExporter`
    - `export()`
  - `CSVExporter`
    - `export()`
  - `ExcelExporter`
    - `export()`

#### `exports/csv.py`
- **Linhas:** 2
- **Funcoes (1):**
  - `gerar_csv(tabela)`

#### `exports/excel.py`
- **Linhas:** 17
- **Funcoes (1):**
  - `gerar_excel(tabela, ind)`

#### `exports/pdf.py`
- **Linhas:** 58
- **Funcoes (1):**
  - `gerar_pdf(df, ind)`

#### `exports/report.py`
- **Linhas:** 13
- **Funcoes (1):**
  - `gerar_relatorio_completo(df, tabela, ind)`

### 4.11 models
*Modelos de dados (dataclasses, enums, schemas)*

#### `models/classes.py`
> Entidades do dominio.
- **Linhas:** 84
- **Classes (5):**
  - `Paciente`
    - `__init__()`
    - `faixa_etaria()`
    - `total_comorbidades()`
  - `ExameECG`
    - `__init__()`
    - `tem_alteracao()`
  - `Laudo`
    - `__init__()`
    - `eh_normal()`
  - `AchadoECG`
    - `__init__()`
  - `Municipio`
    - `__init__()`
    - `pct_alterados()`

#### `models/dataclasses.py`
> Dataclasses para estruturas tipadas.
- **Linhas:** 29
- **Classes (3):**
  - `ResultadoAnalise`
  - `FiltroAplicado`
  - `ExportConfig`

#### `models/enums.py`
> Enumeracoes do projeto.
- **Linhas:** 52
- **Classes (5):**
  - `Sexo`
    - `valores()`
  - `DiagnosticoECG`
    - `valores()`
  - `NivelRisco`
  - `NivelAlerta`
  - `Comorbidade`
    - `__init__()`

#### `models/schemas.py`
> Esquemas de validacao.
- **Linhas:** 24
- **Funcoes (1):**
  - `validar_schema(df)`

#### `models/score.py`
> Scores de risco cardiovascular.
- **Linhas:** 67
- **Funcoes (4):**
  - `score_risco_individual(row)`
  - `classificar_risco(score)`
  - `calcular_scores(df)`
  - `score_municipal(df, min_exames)`

### 4.12 pages
*Paginas do dashboard (abas visiveis ao usuario)*

#### `pages/clinica.py`
- **Linhas:** 66
- **Funcoes (1):**
  - `render(df, ind)`

#### `pages/comorbidades.py`
- **Linhas:** 23
- **Funcoes (1):**
  - `render(df, ind)`

#### `pages/correlacoes.py`
- **Linhas:** 43
- **Funcoes (1):**
  - `render(df, ind)`

#### `pages/dados.py`
- **Linhas:** 53
- **Funcoes (1):**
  - `render(df, ind)`

#### `pages/demografia.py`
> Pagina Demografia com grafico de pizza nativo do Streamlit.
- **Linhas:** 128
- **Funcoes (1):**
  - `render(df, ind)`

#### `pages/distancias.py`
> Pagina Distancias — deslocamento real da equipe pelo Projeto Saude Digital Movel.
- **Linhas:** 65
- **Funcoes (1):**
  - `render(df, ind)`

#### `pages/ecg.py`
- **Linhas:** 96
- **Funcoes (3):**
  - `render_arritmias(df, ind)`
  - `render_bloqueios(df, ind)`
  - `render_ecg_alteracoes(df, ind)`

#### `pages/geral.py`
- **Linhas:** 133
- **Funcoes (2):**
  - `_render_kpis_municipio(df, municipio)`
  - `render(df, ind)`

#### `pages/municipios.py`
- **Linhas:** 306
- **Funcoes (3):**
  - `render_ficha_distrito(df, distrito)`
  - `render_ficha_municipio(df, municipio)` - Ficha completa de um municipio visitado.
  - `render(df, ind)`

#### `pages/sobre.py`
> Pagina Sobre o Projeto.
- **Linhas:** 173
- **Funcoes (1):**
  - `render()`

### 4.13 services
*Servicos de orquestracao (dashboard, exports, relatorios)*

#### `services/dashboard.py`
> Servico de orquestracao do dashboard.
- **Linhas:** 84
- **Classes (1):**
  - `DashboardService`
    - `__init__()`
    - `vazio()`
    - `aplicar_filtros()`
    - `calcular_indicadores()`
    - `gerar_alertas()`
    - `preparar()`
    - `render_abas()`

#### `services/exports.py`
> Servico de exportacao.
- **Linhas:** 31
- **Classes (1):**
  - `ExportService`
    - `__init__()`
    - `csv()`
    - `excel()`
    - `pdf()`

#### `services/reports.py`
> Servico de relatorios.
- **Linhas:** 26
- **Classes (1):**
  - `ReportService`
    - `__init__()`
    - `texto_completo()`
    - `resumo_executivo()`

### 4.14 statistics
*Metodos estatisticos (correlacoes, inferencia, sobrevivencia)*

#### `statistics/correlations.py`
> Correlacoes estatisticas.
- **Linhas:** 52
- **Funcoes (2):**
  - `matriz_correlacao_comorb(df, cols_comorb, col_diag)`
  - `fatores_associados(df, col_alterado, cols_fatores)`

#### `statistics/descriptive.py`
> Estatistica descritiva.
- **Linhas:** 63
- **Funcoes (3):**
  - `resumo_completo(series, nome)`
  - `resumo_por_grupo(series, grupos, nome_var)`
  - `comparar_medias(series1, series2, nome1, nome2)`

#### `statistics/inference.py`
> Testes de hipotese.
- **Linhas:** 48
- **Funcoes (2):**
  - `teste_associacao(var1, var2)`
  - `teste_mannwhitney(s1, s2)`

#### `statistics/survival.py`
> Analises temporais e tendencias.
- **Linhas:** 37
- **Funcoes (2):**
  - `tendencia_temporal(df, col_periodo, col_diag)`
  - `taxa_incidencia_periodo(df, col_periodo, col_diag)`

### 4.15 tests
*Testes automatizados*

#### `tests/test_benchmark.py`
- **Linhas:** 11
- **Funcoes (1):**
  - `test_benchmark_suite()`

#### `tests/test_correlations.py`
- **Linhas:** 15
- **Funcoes (1):**
  - `test_fatores_associados()`

#### `tests/test_epidemiology.py`
- **Linhas:** 47
- **Funcoes (5):**
  - `_make_df(n)`
  - `test_prevalencia_geral()`
  - `test_prevalencia_por_grupo()`
  - `test_resumo_comorbidades()`
  - `test_alertas()`

#### `tests/test_exports.py`
- **Linhas:** 18
- **Funcoes (2):**
  - `test_csv_bytes()`
  - `test_excel_bytes()`

#### `tests/test_indicators.py`
- **Linhas:** 33
- **Funcoes (3):**
  - `_make_df_processado(n)`
  - `test_indicadores_chaves()`
  - `test_n_correto()`

#### `tests/test_interfaces.py`
- **Linhas:** 21
- **Funcoes (3):**
  - `test_csv_exporter()`
  - `test_cache_decorators_import()`
  - `test_settings_immutability()`

#### `tests/test_loader.py`
- **Linhas:** 8
- **Funcoes (1):**
  - `test_ler_excel_arquivo_inexistente()`

#### `tests/test_preprocess.py`
- **Linhas:** 44
- **Funcoes (4):**
  - `_make_df_base(n)`
  - `test_idade_calculada()`
  - `test_diag_cat_atribuido()`
  - `test_colunas_temporais()`

#### `tests/test_risk.py`
- **Linhas:** 17
- **Funcoes (2):**
  - `test_risco_filtro_minimo()`
  - `test_risco_calculo()`

#### `tests/test_settings.py`
- **Linhas:** 26
- **Funcoes (4):**
  - `test_settings_campos()`
  - `test_settings_semver()`
  - `test_settings_limiares()`
  - `test_metadata_consistencia()`

#### `tests/test_statistics.py`
- **Linhas:** 19
- **Funcoes (2):**
  - `test_resumo_completo()`
  - `test_comparar_medias()`

#### `tests/test_utils.py`
- **Linhas:** 33
- **Funcoes (6):**
  - `test_fmt_br()`
  - `test_fmt_pct()`
  - `test_truncar()`
  - `test_as_int()`
  - `test_safe_div()`
  - `test_clamp()`

### 4.16 utils
*Utilitarios (formatacao, texto, tipos)*

#### `utils/formatters.py`
> Formatacao de numeros, datas e porcentagens.
- **Linhas:** 32
- **Funcoes (4):**
  - `fmt_br(n, decimais)`
  - `fmt_pct(valor, decimais)`
  - `fmt_date(data, formato)`
  - `fmt_idade(idade)`

#### `utils/text.py`
> Utilidades de texto.
- **Linhas:** 38
- **Funcoes (5):**
  - `truncar(texto, max_len, sufixo)`
  - `normalizar_espacos(texto)`
  - `titulo_amigavel(texto)`
  - `remover_acentos(texto)`
  - `slugify(texto)`

#### `utils/textos.py`
> Traducao de textos visiveis para portugues correto.
- **Linhas:** 272
- **Funcoes (1):**
  - `t(texto)` - Aplica correcoes de portugues apenas no texto visivel.

#### `utils/types.py`
> Conversao segura de tipos.
- **Linhas:** 43
- **Funcoes (6):**
  - `as_int(valor, default)`
  - `as_float(valor, default)`
  - `as_str(valor, default)`
  - `safe_div(numerador, denominador, default)`
  - `safe_round(valor, decimais)`
  - `clamp(valor, minimo, maximo)`

---

## 5. Mapa de Dependencias

| Arquivo | Importa de |
|---|---|
| `app.py` | `components.filters`, `components.footer`, `components.sidebar`, `components.topbar`, `config.settings`, `data.cache`, `services.dashboard`, `styles` |
| `metadata.py` | `config.settings` |
| `analysis/arritmias.py` | `analysis.ecg`, `constants` |
| `analysis/bloqueios.py` | `analysis.ecg`, `constants` |
| `analysis/classificacao.py` | `constants` |
| `analysis/distancias.py` | `constants`, `constants_locais` |
| `analysis/ecg.py` | `constants` |
| `analysis/nlp.py` | `constants` |
| `charts/base.py` | `config.plotly` |
| `charts/clinical.py` | `charts.base` |
| `charts/comorbidities.py` | `charts.base` |
| `charts/demographics.py` | `charts.base` |
| `charts/distancias.py` | `charts.base`, `constants` |
| `charts/ecg.py` | `charts.base` |
| `charts/heatmaps.py` | `charts.base` |
| `charts/maps.py` | `config.plotly`, `constants` |
| `charts/municipalities.py` | `charts.base` |
| `charts/temporal.py` | `charts.base`, `config.colors` |
| `components/cards.py` | `charts.kpis` |
| `components/filters.py` | `config.app`, `config.colors`, `constants_locais` |
| `data/cache.py` | `data.loader`, `data.preprocess`, `data.validators` |
| `data/indicators.py` | `analysis.ecg`, `config.app`, `constants`, `epidemiology.comorbidades`, `epidemiology.crosstab`, `epidemiology.territorial` |
| `data/preprocess.py` | `analysis.classificacao`, `config.app`, `constants_locais` |
| `data/validators.py` | `constants` |
| `epidemiology/comorbidades.py` | `config.app` |
| `epidemiology/crosstab.py` | `analysis.ecg` |
| `epidemiology/territorial.py` | `config.app`, `constants`, `constants_locais` |
| `exports/pdf.py` | `constants` |
| `exports/report.py` | `analysis.textos` |
| `pages/clinica.py` | `analysis.nlp`, `charts.clinical` |
| `pages/comorbidades.py` | `charts.comorbidities`, `charts.kpis` |
| `pages/correlacoes.py` | `charts.heatmaps`, `charts.municipalities` |
| `pages/dados.py` | `constants` |
| `pages/demografia.py` | `charts.demographics`, `charts.kpis` |
| `pages/distancias.py` | `analysis.distancias`, `charts.distancias`, `charts.kpis` |
| `pages/ecg.py` | `charts.ecg` |
| `pages/geral.py` | `analysis.ecg`, `charts.ecg`, `charts.kpis`, `charts.maps`, `components.alerts`, `config.app`, `config.colors`, `constants` |
| `pages/municipios.py` | `analysis.ecg`, `charts.ecg`, `charts.heatmaps`, `charts.kpis`, `charts.maps`, `charts.municipalities`, `config.app`, `config.colors` |
| `services/dashboard.py` | `components.filters`, `data.indicators`, `epidemiology.alerts` |
| `services/reports.py` | `analysis.textos`, `epidemiology.prevalence` |
| `tests/test_epidemiology.py` | `epidemiology.alerts`, `epidemiology.comorbidades`, `epidemiology.prevalence` |
| `tests/test_indicators.py` | `data.indicators`, `data.preprocess`, `data.validators` |
| `tests/test_interfaces.py` | `config.settings`, `data.cache` |
| `tests/test_loader.py` | `data.loader` |
| `tests/test_preprocess.py` | `data.preprocess`, `data.validators` |
| `tests/test_risk.py` | `epidemiology.territorial` |
| `tests/test_settings.py` | `config.settings`, `metadata` |

---

## 6. Funcoes Publicas (API Interna)

| Funcao | Arquivo | Descricao |
|---|---|---|
| `buscar_distrito(data_cadastro, cidade)` | `constants_locais.py` | Busca distrito cruzando data + municipio. |
| `buscar_municipio_coleta(data_cadastro, cidade)` | `constants_locais.py` | Retorna o municipio onde o exame foi realizado. |
| `distrito_para_municipio(distrito)` | `constants_locais.py` | Retorna o municipio de um distrito. |
| `get_municipios_visitados()` | `constants_locais.py` | Retorna lista de municipios visitados. |
| `get_distritos_municipio(municipio)` | `constants_locais.py` | Retorna distritos de um municipio. |
| `calcular_distancias_distritos(df)` | `analysis/distancias.py` | Calcula rotas: Diamantina -> cada municipio -> Diamantina (i |
| `configurar_layout(fig, height, title_size)` | `charts/base.py` | Layout padrao com hovermode e dragmode interativos. |
| `treemap_achados(achados_dict, title)` | `charts/ecg.py` | Treemap interativo com tamanhos proporcionais e hover detalh |
| `mapa_risco(mapa_df, titulo_col)` | `charts/maps.py` | Mapa de risco com tamanhos proporcionais e hover detalhado. |
| `mapa_simples(mapa_df, cidade_destaque, df)` | `charts/maps.py` | Mapa simples de distribuicao com opcao de destaque. |
| `risco_territorial(risco_df)` | `charts/municipalities.py` | Ranking de risco com cores por nivel e hover detalhado. |
| `comorb_municipio(cm_df, label)` | `charts/municipalities.py` | Ranking de comorbidade por municipio — hover detalhado. |
| `evolucao_mensal(tempo_df)` | `charts/temporal.py` | Area empilhada mensal — com range slider e hover rico. |
| `taxa_alteracao(taxa_df)` | `charts/temporal.py` | Linha com marcadores — range slider interativo. |
| `risco_territorial(df, min_exames)` | `epidemiology/territorial.py` | Risco territorial por municipio (cidade de origem). |
| `risco_territorial_distrito(df, min_exames)` | `epidemiology/territorial.py` | Risco territorial por distrito (local do exame). |
| `render_ficha_municipio(df, municipio)` | `pages/municipios.py` | Ficha completa de um municipio visitado. |
| `t(texto)` | `utils/textos.py` | Aplica correcoes de portugues apenas no texto visivel. |

---

## 7. Comandos Uteis

```bash
# Rodar o app
python -m streamlit run app.py --server.headless false

# Atualizar locais de campo
python gerar_locais2.py

# Rodar testes
python -m pytest tests/
```

---

## 8. Como Expandir

### Adicionar novo municipio visitado:
1. Edite `Locais.xlsx` com periodo, municipio, distrito, exames
2. Rode `python gerar_locais2.py`
3. Adicione coordenadas em `constants.py` -> `MUN_COORDS`

### Adicionar novo achado ECG:
1. Adicione em `constants.py` -> `ECG_ACHADOS`
2. A coluna `_ach_*` e criada automaticamente pelo `validators.py`

### Adicionar nova aba:
1. Crie `pages/nova_aba.py` com funcao `render(df, ind)`
2. Importe em `services/dashboard.py` -> `render_abas()`
3. Adicione na lista `st.tabs([...])`
4. Use `key='unico'` em cada `st.plotly_chart()`