import pandas as pd
import unicodedata
import random


def _norm(s):
    s = str(s).strip().lower()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return " ".join(s.split())

LOCAIS = [
    ("2022-07-27", "2022-07-28", "Gouveia", "Vila Alexandre Mascarenhas", 0),
    ("2022-08-08", "2022-08-20", "Diamantina", "Cazuza", 0),
    ("2022-10-03", "2022-10-07", "Janaúba", "Vila Nova dos Poções", 0),
    ("2022-10-24", "2022-10-26", "Diamantina", "Campus JK", 0),
    ("2023-03-21", "2023-03-23", "Diamantina", "São João da Chapada/Guinda/Sopa", 94),
    ("2023-05-15", "2023-05-19", "Couto De Magalhães", "Couto Magalhães", 49),
    ("2023-06-24", "2023-06-24", "Diamantina", "Senador Mourão", 0),
    ("2023-07-04", "2023-07-07", "Presidente Kubitschek", "Presidente Kubitschek", 62),
    ("2023-07-15", "2023-07-15", "Diamantina", "Planalto de Minas", 7),
    ("2023-08-23", "2023-08-23", "São Gonçalo Rio Preto", "São Gonçalo Rio Preto", 41),
    ("2023-09-26", "2023-09-28", "Felício Dos Santos", "Felício dos Santos", 23),
    ("2023-10-17", "2023-10-20", "Minas Novas", "Minas Novas", 107),
    ("2023-10-27", "2023-10-27", "Diamantina", "Campus JK", 12),
    ("2023-10-01", "2023-10-31", "Presidente Kubitschek", "PK zona rural", 0),
    ("2023-11-07", "2023-11-10", "Itamarandiba", "Itamarandiba", 109),
    ("2023-11-23", "2023-11-23", "São Gonçalo Rio Preto", "São Gonçalo Rio Preto", 0),
    ("2023-11-25", "2023-11-25", "Diamantina", "Extração", 15),
    ("2023-12-13", "2023-12-15", "Serro", "Serro", 91),
    ("2023-12-16", "2023-12-16", "Diamantina", "Guinda", 15),
    ("2023-12-18", "2023-12-18", "Diamantina", "Vila Operária", 123),
    ("2024-01-22", "2024-01-25", "Senador Modestino Gonçalves", "Senador Modestino Gonçalves", 79),
    ("2024-01-27", "2024-01-27", "Diamantina", "Mendanha", 14),
    ("2024-02-21", "2024-02-21", "Diamantina", "Gruta de Lourdes", 18),
    ("2024-02-27", "2024-02-29", "Virgem Da Lapa", "Virgem da Lapa", 179),
    ("2024-03-01", "2024-03-31", "Diamantina", "Jardim Imperial", 40),
    ("2024-03-07", "2024-03-07", "Diamantina", "Rio Grande", 12),
    ("2024-03-18", "2024-03-21", "Datas", "Datas", 130),
    ("2024-03-23", "2024-03-23", "Diamantina", "São João Chapada", 20),
    ("2024-03-01", "2024-03-31", "Diamantina", "Palha", 19),
    ("2024-04-01", "2024-04-01", "Diamantina", "Largo", 8),
    ("2024-04-01", "2024-04-30", "Diamantina", "Gruta", 64),
    ("2024-04-01", "2024-04-30", "Diamantina", "Rio Grande", 10),
    ("2024-04-01", "2024-04-30", "Diamantina", "Jardim Imperial", 63),
    ("2024-04-01", "2024-04-30", "Diamantina", "Arraial dos Forros", 45),
    ("2024-04-01", "2024-04-30", "Congonhas Do Norte", "Congonhas do Norte", 142),
    ("2024-04-01", "2024-04-30", "Diamantina", "Diamantina (centro)", 103),
    ("2024-04-01", "2024-04-30", "Diamantina", "Inhaí", 27),
    ("2024-05-22", "2024-05-22", "Diamantina", "Maria Nunes Mendanha", 103),
    ("2024-05-25", "2024-05-25", "Diamantina", "Senador Mourão", 30),
    ("2024-06-18", "2024-06-21", "Carbonita", "Carbonita", 147),
    ("2024-06-01", "2024-06-30", "Diamantina", "Planalto", 13),
    ("2024-06-01", "2024-06-30", "Diamantina", "Jardim Imperial", 0),
    ("2024-06-01", "2024-06-30", "Diamantina", "PK", 0),
    ("2024-07-02", "2024-07-03", "Santo Antônio Do Itambé", "Santo Antônio do Itambé", 141),
    ("2024-07-05", "2024-07-05", "Diamantina", "Conselheiro Mata", 18),
    ("2024-07-01", "2024-07-31", "Couto De Magalhães", "Couto de Magalhães", 0),
    ("2024-08-01", "2024-08-31", "Diamantina", "Largo Dom João", 19),
    ("2024-08-10", "2024-08-10", "Serro", "Capivari", 37),
    ("2024-08-17", "2024-08-17", "Diamantina", "Sopa", 30),
    ("2024-08-20", "2024-08-21", "Jenipapo De Minas", "Jenipapo", 135),
    ("2024-08-01", "2024-08-31", "Diamantina", "Gruta de Lourdes", 21),
    ("2024-09-01", "2024-09-30", "Diamantina", "Diamantina (regulação)", 16),
    ("2024-09-24", "2024-09-24", "Diamantina", "Diamantina UBS ESAC", 170),
    ("2024-01-01", "2024-12-31", "São João Da Lagoa", "São João da Lagoa", 104),
    ("2024-10-01", "2024-10-31", "Diamantina", "Diamantina UBS ESAC", 119),
    ("2024-10-01", "2024-10-31", "Couto De Magalhães", "Couto de Magalhães ESAC", 54),
    ("2024-10-01", "2024-10-31", "Diamantina", "UFVJM (Servidor)", 85),
    ("2024-10-01", "2024-10-31", "Diamantina", "Cazuza", 38),
    ("2024-11-01", "2024-11-30", "Chapada Do Norte", "Chapada do Norte", 129),
    ("2024-08-01", "2024-11-30", "Porto Alegre", "Porto Alegre", 0),
    ("2024-12-01", "2024-12-31", "Diamantina", "São João da Chapada", 90),
    ("2024-12-01", "2024-12-31", "Diamantina", "Diamantina EX (1)", 0),
    ("2024-12-01", "2024-12-31", "Diamantina", "Diamantina EX (2)", 0),
    ("2025-02-01", "2025-02-28", "Diamantina", "Diamantina ESAC", 91),
    ("2025-02-01", "2025-02-28", "Serro", "São Gonçalo Rio das Pedras", 17),
    ("2025-02-01", "2025-02-28", "José Gonçalves De Minas", "José Gonçalves de Minas", 129),
    ("2025-03-01", "2025-03-31", "Diamantina", "Diamantina ESAC", 115),
    ("2025-03-01", "2025-03-31", "Teófilo Otoni", "Teófilo Otoni", 92),
    ("2025-04-01", "2025-04-30", "Diamantina", "Diamantina (Palha/Centro/Vila)", 120),
    ("2025-04-01", "2025-04-30", "Presidente Kubitschek", "PK", 29),
    ("2025-04-01", "2025-04-30", "Rio Vermelho", "Rio Vermelho", 137),
    ("2025-05-01", "2025-05-31", "Monjolos", "Monjolos", 122),
    ("2025-06-01", "2025-06-30", "Diamantina", "Diamantina (distritos regulação)", 174),
    ("2025-07-01", "2025-07-31", "Diamantina", "Diamantina (ESF/regulação)", 101),
    ("2025-07-01", "2025-07-31", "Araçuaí", "Araçuaí", 99),
    ("2025-08-01", "2025-08-31", "Diamantina", "Diamantina (regulação)", 172),
    ("2025-08-01", "2025-08-31", "Diamantina", "Diamantina", 174),
    ("2025-08-01", "2025-08-31", "Carbonita", "Carbonita", 148),
    ("2025-09-01", "2025-09-30", "Diamantina", "Diamantina", 65),
    ("2025-10-01", "2025-10-31", "Capelinha", "Capelinha", 76),
    ("2025-11-01", "2025-11-30", "Jaboticatubas", "Jaboticatubas", 72),
    ("2025-12-01", "2025-12-31", "Diamantina", "Cazuza", 66),
    ("2026-02-10", "2026-02-12", "Peçanha", "Peçanha", 109),
    ("2026-04-01", "2026-04-30", "Couto De Magalhães", "Couto de Magalhães", 120),
    ("2026-04-01", "2026-04-30", "Diamantina", "Diamantina ( Cazuza)", 0),
    ("2026-04-01", "2026-04-30", "Diamantina", "Diamantina ( PALHA)", 52),
    ("2026-04-01", "2026-04-30", "Gouveia", "Gouveia", 25),
    ("2026-04-01", "2026-04-30", "Francisco Badaró", "Francisco Badaró", 122),
    ("2026-05-01", "2026-05-31", "Diamantina", "UFVJM quem ama e esac", 148),
    ("2026-06-01", "2026-06-30", "Felício Dos Santos", "Felício dos Santos", 119),
]


def buscar_distrito(data_cadastro, cidade):
    """Busca distrito cruzando data + municipio."""
    if not data_cadastro or not cidade:
        return ""
    cn = _norm(cidade)

    # Cidades visitadas pela equipe
    cidades_visitadas = set()
    for _, _, mun, _, _ in LOCAIS:
        cidades_visitadas.add(_norm(mun))

    # 1. Match exato: data + municipio
    candidatos = []
    for ini_str, fim_str, mun, dist, ecg in LOCAIS:
        if _norm(mun) != cn:
            continue
        ini = pd.Timestamp(ini_str)
        fim = pd.Timestamp(fim_str)
        if ini <= data_cadastro < fim + pd.Timedelta(days=1):
            candidatos.append((dist, max(int(ecg) if ecg else 0, 1)))

    if len(candidatos) == 1:
        return candidatos[0][0]
    elif len(candidatos) > 1:
        total = sum(e for _, e in candidatos)
        r = random.Random(int(data_cadastro.timestamp())).random() * total
        acum = 0
        for dist, ecg in candidatos:
            acum += ecg
            if r <= acum:
                return dist
        return candidatos[-1][0]

    # 2. Paciente de cidade visitada mas fora do periodo = posto fixo
    if cn in cidades_visitadas:
        return cidade.strip().title()

    # 3. Paciente de cidade NUNCA visitada = fez exame em campo
    candidatos_data = []
    for ini_str, fim_str, mun, dist, ecg in LOCAIS:
        ini = pd.Timestamp(ini_str)
        fim = pd.Timestamp(fim_str)
        if ini <= data_cadastro <= fim:
            candidatos_data.append((dist, max(int(ecg) if ecg else 0, 1), mun))

    if candidatos_data:
        if len(candidatos_data) == 1:
            return candidatos_data[0][0]
        total = sum(e for _, e, _ in candidatos_data)
        r = random.Random(int(data_cadastro.timestamp()) + 777).random() * total
        acum = 0
        for dist, ecg, _ in candidatos_data:
            acum += ecg
            if r <= acum:
                return dist
        return candidatos_data[-1][0]

    return "Diamantina"



def buscar_municipio_coleta(data_cadastro, cidade):
    """Retorna o municipio onde o exame foi realizado."""
    if not data_cadastro or not cidade:
        return ""
    cn = _norm(cidade)
    cidades_com_exames = {_norm(m) for _, _, m, _, ecg in LOCAIS if int(ecg) > 0}

    # 1. Match exato: data + municipio
    for ini_str, fim_str, mun, dist, ecg in LOCAIS:
        if _norm(mun) != cn:
            continue
        ini = pd.Timestamp(ini_str)
        fim = pd.Timestamp(fim_str)
        if ini <= data_cadastro < fim + pd.Timedelta(days=1):
            return mun.strip().title()

    # 2. Cidade visitada com exames = posto fixo
    if cn in cidades_com_exames:
        return cidade.strip().title()

    # 3. Cidade nunca visitada = tenta achar por data
    for ini_str, fim_str, mun, dist, ecg in LOCAIS:
        ini = pd.Timestamp(ini_str)
        fim = pd.Timestamp(fim_str)
        if ini <= data_cadastro < fim + pd.Timedelta(days=1):
            return mun.strip().title()

    return "Diamantina"


def distrito_para_municipio(distrito):
    """Retorna o municipio de um distrito."""
    if not distrito:
        return ""
    dist_norm = _norm(distrito)
    for _, _, mun, dist, _ in LOCAIS:
        if _norm(dist) == dist_norm:
            return mun.strip().title()
    return ""


def get_municipios_visitados():
    """Retorna lista de municipios visitados."""
    return sorted({mun.strip().title() for _, _, mun, _, _ in LOCAIS})


def get_distritos_municipio(municipio):
    """Retorna distritos de um municipio."""
    mun_norm = _norm(municipio)
    return sorted({dist for _, _, mun, dist, _ in LOCAIS if _norm(mun) == mun_norm and dist})
