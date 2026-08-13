"""
Gerador automatico de documentacao do VCARDIO.
"""

import os
import ast
import datetime


def listar_arquivos(pasta, ext=".py"):
    arquivos = []
    for raiz, dirs, files in os.walk(pasta):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", ".streamlit", "logs")]
        for f in sorted(files):
            if f.endswith(ext) and not f.startswith("__"):
                arquivos.append(os.path.join(raiz, f))
    return arquivos


def analisar_arquivo(caminho):
    info = {
        "caminho": caminho,
        "nome": os.path.basename(caminho),
        "pasta": os.path.dirname(caminho),
        "docstring": "",
        "imports": [],
        "classes": [],
        "funcoes": [],
        "linhas": 0,
    }
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            codigo = f.read()
        info["linhas"] = len(codigo.splitlines())
        tree = ast.parse(codigo)
        doc = ast.get_docstring(tree)
        if doc:
            info["docstring"] = doc.strip().split("\n")[0][:100]
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    info["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    info["imports"].append(node.module)
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                cls = {
                    "nome": node.name,
                    "docstring": (ast.get_docstring(node) or "").strip().split("\n")[0][:80],
                    "metodos": [],
                }
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        cls["metodos"].append({
                            "nome": item.name,
                            "docstring": (ast.get_docstring(item) or "").strip().split("\n")[0][:60],
                        })
                info["classes"].append(cls)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                info["funcoes"].append({
                    "nome": node.name,
                    "docstring": (ast.get_docstring(node) or "").strip().split("\n")[0][:60],
                    "args": [a.arg for a in node.args.args if a.arg != "self"],
                })
    except Exception as e:
        info["docstring"] = f"Erro ao analisar: {e}"
    return info


def descricao_pasta(pasta):
    descricoes = {
        "analysis": "Motor de analise de dados (ECG, distancias, classificacao)",
        "benchmark": "Testes de performance",
        "charts": "Graficos Plotly (mapas, barras, heatmaps, KPIs)",
        "components": "Componentes de UI Streamlit (filtros, cards, alertas)",
        "config": "Configuracoes globais (cores, caminhos, constantes)",
        "data": "Carregamento, validacao, processamento e indicadores",
        "epidemiology": "Analises epidemiologicas (alertas, prevalencia, territorial)",
        "examples": "Dados e scripts de exemplo",
        "exports": "Exportacao de relatorios (CSV, Excel, PDF)",
        "logs": "Sistema de logging",
        "models": "Modelos de dados (dataclasses, enums, schemas)",
        "pages": "Paginas do dashboard (abas visiveis ao usuario)",
        "services": "Servicos de orquestracao (dashboard, exports, relatorios)",
        "statistics": "Metodos estatisticos (correlacoes, inferencia, sobrevivencia)",
        "tests": "Testes automatizados",
        "utils": "Utilitarios (formatacao, texto, tipos)",
    }
    nome = os.path.basename(pasta)
    return descricoes.get(nome, "")


def gerar_documentacao():
    pasta_raiz = "."
    arquivos = listar_arquivos(pasta_raiz)
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    linhas = []
    w = linhas.append

    w("# VCARDIO - Documentacao Tecnica Automatica")
    w(f"**Gerado em:** {agora}")
    w("")
    w("## Painel Inteligente de Vigilancia Cardiovascular")
    w("### Projeto Saude Digital Movel - UFVJM")
    w("")
    w("---")
    w("")

    # 1. Visao Geral
    w("## 1. Visao Geral")
    w("")
    total_arquivos = len(arquivos)
    total_linhas = 0
    for arq in arquivos:
        info = analisar_arquivo(arq)
        total_linhas += info["linhas"]
    w(f"- **Total de arquivos Python:** {total_arquivos}")
    w(f"- **Total de linhas de codigo:** {total_linhas:,}")
    w("- **Rodando:** `python -m streamlit run app.py --server.headless false`")
    w("- **Dados:** `ecg.xlsx`")
    w("- **Atualizar locais:** edite `Locais.xlsx`, rode `python gerar_locais2.py`")
    w("")
    w("---")
    w("")

    # 2. Estrutura
    w("## 2. Estrutura de Pastas")
    w("")
    w("```")
    pastas_ordenadas = sorted(set(os.path.dirname(a) for a in arquivos))
    for pasta in pastas_ordenadas:
        nome = pasta if pasta != "." else "."
        desc = descricao_pasta(pasta)
        if nome == ".":
            arquivos_raiz = [a for a in arquivos if os.path.dirname(a) == "."]
            w(f"{nome}/")
            for a in arquivos_raiz:
                info = analisar_arquivo(a)
                doc = info["docstring"]
                linha = f"  |-- {info['nome']}"
                if doc:
                    linha += f"  # {doc}"
                w(linha)
        else:
            arquivos_pasta = [a for a in arquivos if os.path.dirname(a) == pasta]
            if arquivos_pasta:
                w("")
                w(f"{pasta}/")
                if desc:
                    w(f"  |   # {desc}")
                for a in arquivos_pasta:
                    info = analisar_arquivo(a)
                    doc = info["docstring"]
                    linha = f"  |-- {info['nome']}"
                    if doc:
                        linha += f"  # {doc}"
                    w(linha)
    w("```")
    w("")
    w("---")
    w("")

    # 3. Fluxo de dados
    w("## 3. Fluxo de Dados")
    w("")
    w("```")
    w("ecg.xlsx")
    w("   |")
    w("   v")
    w("data/loader.py        -> _ler_excel()         -> DataFrame bruto")
    w("   |")
    w("   v")
    w("data/validators.py    -> verificar_colunas()   -> Normaliza colunas, cria _ach_*")
    w("   |")
    w("   v")
    w("data/preprocess.py    -> processar_dados()     -> Idade, sexo, diagnostico, distrito")
    w("   |")
    w("   v")
    w("components/filters.py -> aplicar_filtros()     -> Filtra por municipio, sexo, etc.")
    w("   |")
    w("   v")
    w("data/indicators.py    -> calcular_indicadores()-> KPIs, mapas, heatmaps, rankings")
    w("   |")
    w("   v")
    w("pages/*.py            -> render()              -> Graficos e tabelas na tela")
    w("```")
    w("")
    w("---")
    w("")

    # 4. Detalhes por pasta
    w("## 4. Detalhes por Pasta e Arquivo")
    w("")
    idx = 1
    for pasta in pastas_ordenadas:
        arquivos_pasta = [a for a in arquivos if os.path.dirname(a) == pasta]
        if not arquivos_pasta:
            continue
        nome_pasta = os.path.basename(pasta) if pasta != "." else "Raiz"
        desc = descricao_pasta(pasta)
        w(f"### 4.{idx} {nome_pasta}")
        if desc:
            w(f"*{desc}*")
        w("")
        for arq in arquivos_pasta:
            info = analisar_arquivo(arq)
            rel = os.path.relpath(arq, pasta_raiz).replace("\\", "/")
            w(f"#### `{rel}`")
            if info["docstring"]:
                w(f"> {info['docstring']}")
            w(f"- **Linhas:** {info['linhas']}")
            if info["funcoes"]:
                w(f"- **Funcoes ({len(info['funcoes'])}):**")
                for func in info["funcoes"]:
                    args = ", ".join(func["args"]) if func["args"] else ""
                    doc = f" - {func['docstring']}" if func["docstring"] else ""
                    w(f"  - `{func['nome']}({args})`{doc}")
            if info["classes"]:
                w(f"- **Classes ({len(info['classes'])}):**")
                for cls in info["classes"]:
                    doc = f" - {cls['docstring']}" if cls["docstring"] else ""
                    w(f"  - `{cls['nome']}`{doc}")
                    for met in cls["metodos"]:
                        mdoc = f" - {met['docstring']}" if met["docstring"] else ""
                        w(f"    - `{met['nome']}()`{mdoc}")
            w("")
        idx += 1

    w("---")
    w("")

    # 5. Dependencias
    w("## 5. Mapa de Dependencias")
    w("")
    w("| Arquivo | Importa de |")
    w("|---|---|")
    prefixos_projeto = [
        "data.", "analysis.", "charts.", "components.", "config.",
        "epidemiology.", "pages.", "services.", "constants",
        "styles", "metadata"
    ]
    for arq in arquivos:
        info = analisar_arquivo(arq)
        rel = os.path.relpath(arq, pasta_raiz).replace("\\", "/")
        imports_projeto = [
            imp for imp in set(info["imports"])
            if any(imp.startswith(p) for p in prefixos_projeto)
        ]
        if imports_projeto:
            deps = ", ".join(f"`{d}`" for d in sorted(imports_projeto)[:8])
            w(f"| `{rel}` | {deps} |")
    w("")
    w("---")
    w("")

    # 6. Funcoes publicas
    w("## 6. Funcoes Publicas (API Interna)")
    w("")
    w("| Funcao | Arquivo | Descricao |")
    w("|---|---|---|")
    for arq in arquivos:
        info = analisar_arquivo(arq)
        rel = os.path.relpath(arq, pasta_raiz).replace("\\", "/")
        for func in info["funcoes"]:
            if not func["nome"].startswith("_") and func["docstring"]:
                args = ", ".join(func["args"][:3]) if func["args"] else ""
                w(f"| `{func['nome']}({args})` | `{rel}` | {func['docstring']} |")
    w("")
    w("---")
    w("")

    # 7. Comandos uteis
    w("## 7. Comandos Uteis")
    w("")
    w("```bash")
    w("# Rodar o app")
    w("python -m streamlit run app.py --server.headless false")
    w("")
    w("# Atualizar locais de campo")
    w("python gerar_locais2.py")
    w("")
    w("# Rodar testes")
    w("python -m pytest tests/")
    w("```")
    w("")
    w("---")
    w("")

    # 8. Como expandir
    w("## 8. Como Expandir")
    w("")
    w("### Adicionar novo municipio visitado:")
    w("1. Edite `Locais.xlsx` com periodo, municipio, distrito, exames")
    w("2. Rode `python gerar_locais2.py`")
    w("3. Adicione coordenadas em `constants.py` -> `MUN_COORDS`")
    w("")
    w("### Adicionar novo achado ECG:")
    w("1. Adicione em `constants.py` -> `ECG_ACHADOS`")
    w("2. A coluna `_ach_*` e criada automaticamente pelo `validators.py`")
    w("")
    w("### Adicionar nova aba:")
    w("1. Crie `pages/nova_aba.py` com funcao `render(df, ind)`")
    w("2. Importe em `services/dashboard.py` -> `render_abas()`")
    w("3. Adicione na lista `st.tabs([...])`")
    w("4. Use `key='unico'` em cada `st.plotly_chart()`")

    texto = "\n".join(linhas)
    with open("DOCUMENTACAO.md", "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"OK - DOCUMENTACAO.md gerado ({len(linhas)} linhas, {len(arquivos)} arquivos)")


if __name__ == "__main__":
    gerar_documentacao()