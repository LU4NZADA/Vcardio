from exports.csv import gerar_csv
from exports.excel import gerar_excel
from exports.pdf import gerar_pdf
from analysis.textos import gerar_paragrafo_completo


def gerar_relatorio_completo(df, tabela, ind):
    return {
        "csv": gerar_csv(tabela),
        "excel": gerar_excel(tabela, ind),
        "pdf": gerar_pdf(df, ind),
        "texto": gerar_paragrafo_completo(df, ind),
    }