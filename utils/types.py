"""
Conversao segura de tipos.
"""


def as_int(valor, default=0):
    if valor is None:
        return default
    try:
        return int(valor)
    except (ValueError, TypeError):
        return default


def as_float(valor, default=0.0):
    if valor is None:
        return default
    try:
        return float(valor)
    except (ValueError, TypeError):
        return default


def as_str(valor, default=""):
    if valor is None:
        return default
    return str(valor).strip()


def safe_div(numerador, denominador, default=0.0):
    if denominador == 0:
        return default
    return numerador / denominador


def safe_round(valor, decimais=1):
    if valor is None:
        return 0.0
    return round(float(valor), decimais)


def clamp(valor, minimo, maximo):
    return max(minimo, min(valor, maximo))