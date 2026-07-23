"""
Formatacao de numeros, datas e porcentagens.
"""

from datetime import datetime


def fmt_br(n, decimais=0):
    if decimais > 0:
        inteiro, decimal = f"{n:.{decimais}f}".split(".")
    else:
        inteiro = str(int(round(n)))
        decimal = ""
    inteiro_fmt = f"{int(inteiro):,}".replace(",", ".")
    return f"{inteiro_fmt},{decimal}" if decimal else inteiro_fmt


def fmt_pct(valor, decimais=1):
    return f"{round(valor, decimais)}%"


def fmt_date(data, formato="%d/%m/%Y"):
    if data is None:
        return ""
    if hasattr(data, "strftime"):
        return data.strftime(formato)
    return str(data)


def fmt_idade(idade):
    i = int(round(idade))
    return "1 ano" if i == 1 else f"{i} anos"