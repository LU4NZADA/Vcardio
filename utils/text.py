"""
Utilidades de texto.
"""

import re
import unicodedata


def truncar(texto, max_len=50, sufixo="..."):
    if not texto or len(texto) <= max_len:
        return texto
    return texto[: max_len - len(sufixo)].rsplit(" ", 1)[0] + sufixo


def normalizar_espacos(texto):
    if not texto:
        return ""
    return re.sub(r"\s+", " ", texto).strip()


def titulo_amigavel(texto):
    texto = re.sub(r"([a-z])([A-Z])", r"\1 \2", texto)
    texto = texto.replace("_", " ").replace("-", " ")
    return texto.strip().title()


def remover_acentos(texto):
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def slugify(texto):
    texto = remover_acentos(texto).lower()
    texto = re.sub(r"[^\w\s-]", "", texto)
    texto = re.sub(r"[\s_]+", "-", texto)
    return texto.strip("-")