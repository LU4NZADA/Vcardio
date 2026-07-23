"""
Calculo de distancias percorridas pelo Projeto Saude Digital Movel.
A equipe parte de Diamantina (base) ate a cidade natal de cada paciente
para realizar os exames ECG. Apenas cidades de Minas Gerais sao consideradas.
"""

import math
from itertools import combinations
from constants import MUN_COORDS


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_r, lon1_r = math.radians(lat1), math.radians(lon1)
    lat2_r, lon2_r = math.radians(lat2), math.radians(lon2)
    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def calcular_distancia_base(cidade_origem, cidades_destino):
    if cidade_origem not in MUN_COORDS:
        return 0.0, []
    base = MUN_COORDS[cidade_origem]
    rotas = []
    total = 0.0
    for cidade in cidades_destino:
        if cidade in MUN_COORDS and cidade != cidade_origem:
            dist = haversine(base[0], base[1], MUN_COORDS[cidade][0], MUN_COORDS[cidade][1])
            total += dist * 2
            rotas.append({"origem": cidade_origem, "destino": cidade, "km": round(dist, 1)})
    return round(total, 1), rotas


def calcular_distancia_minima(cidades_visitadas):
    coords = {c: MUN_COORDS[c] for c in cidades_visitadas if c in MUN_COORDS}
    if len(coords) < 2:
        return 0.0, []

    visitados = set()
    nao_visitados = set(coords.keys())
    primeiro = nao_visitados.pop()
    visitados.add(primeiro)
    total = 0.0
    arestas = []

    while nao_visitados:
        menor_dist = float("inf")
        melhor_cidade = None
        melhor_de = None
        for v in visitados:
            for nv in nao_visitados:
                d = haversine(coords[v][0], coords[v][1], coords[nv][0], coords[nv][1])
                if d < menor_dist:
                    menor_dist = d
                    melhor_cidade = nv
                    melhor_de = v
        if melhor_cidade:
            total += menor_dist
            arestas.append({"de": melhor_de, "para": melhor_cidade, "km": round(menor_dist, 1)})
            visitados.add(melhor_cidade)
            nao_visitados.remove(melhor_cidade)

    return round(total, 1), arestas


def calcular_todas_distancias(cidades_visitadas, cidade_base="Diamantina"):
    # Apenas cidades que existem em MUN_COORDS (so MG)
    cidades_com_coords = [c for c in cidades_visitadas if c in MUN_COORDS]
    cidades_sem_coords = len(cidades_visitadas) - len(cidades_com_coords)

    dist_base, rotas_base = calcular_distancia_base(cidade_base, cidades_com_coords)
    dist_minima, arestas = calcular_distancia_minima(cidades_com_coords)
    total_estimado = sum(r["km"] * 2 for r in rotas_base)

    pares = []
    for c1, c2 in combinations(cidades_com_coords, 2):
        d = haversine(MUN_COORDS[c1][0], MUN_COORDS[c1][1],
                      MUN_COORDS[c2][0], MUN_COORDS[c2][1])
        pares.append({"de": c1, "para": c2, "km": round(d, 1)})
    pares.sort(key=lambda x: x["km"], reverse=True)

    proximos = sorted(pares, key=lambda x: x["km"])[:10]

    distancias_base = []
    for c in cidades_com_coords:
        d = haversine(MUN_COORDS[cidade_base][0], MUN_COORDS[cidade_base][1],
                      MUN_COORDS[c][0], MUN_COORDS[c][1])
        distancias_base.append({"Cidade": c, "km": round(d, 1)})
    distancias_base.sort(key=lambda x: x["km"], reverse=True)

    return {
        "cidade_base": cidade_base,
        "total_cidades_visitadas": len(cidades_visitadas),
        "cidades_mg": len(cidades_com_coords),
        "cidades_fora_mg": cidades_sem_coords,
        "cidades_com_coordenadas": len(cidades_com_coords),
        "distancia_base_ida_volta_km": dist_base,
        "distancia_minima_percurso_km": dist_minima,
        "total_estimado_km": total_estimado,
        "rotas": rotas_base,
        "arestas_mst": arestas,
        "pares_mais_distantes": pares[:10],
        "pares_mais_proximos": proximos,
        "cidades_mais_distantes_base": distancias_base[:15],
        "media_km_por_cidade": round(total_estimado / max(len(cidades_com_coords), 1), 1),
    }