"""
Calculo de distancias percorridas pelo Projeto Saude Digital Movel.
A equipe parte de Diamantina (base) ate o local onde o exame foi realizado.
"""

import math
from itertools import combinations
from constants import MUN_COORDS
from constants_locais import LOCAIS, _norm


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1_r, lon1_r = math.radians(lat1), math.radians(lon1)
    lat2_r, lon2_r = math.radians(lat2), math.radians(lon2)
    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def _coords_municipio(nome):
    """Busca coordenadas de um municipio, tentando com e sem acento."""
    if nome in MUN_COORDS:
        return MUN_COORDS[nome]
    norm = _norm(nome)
    for k, v in MUN_COORDS.items():
        if _norm(k) == norm:
            return v
    return None


def _distrito_para_municipio(distrito_nome):
    """Busca o municipio real de um distrito na tabela LOCAIS."""
    dist_norm = _norm(distrito_nome)
    for _, _, mun, dist, _ in LOCAIS:
        if _norm(dist) == dist_norm:
            return mun
    return None


def calcular_distancias_distritos(df):
    """Calcula rotas: Diamantina -> cada municipio -> Diamantina (ida e volta)."""
    cidade_base = "Diamantina"
    base_coords = _coords_municipio(cidade_base)

    # Conta exames por municipio de coleta
    col = "Municipio_Coleta" if "Municipio_Coleta" in df.columns else "Cidade"
    contagem = df[df[col].ne("") & (df[col].str.strip().ne(""))].groupby(col).size().reset_index(name="exames")

    municipios_visitados = []
    rotas = []
    total_estimado = 0.0

    for _, row in contagem.iterrows():
        mun = row[col]
        if not mun or not mun.strip():
            continue
        exames = int(row["exames"])
        mn = _norm(mun)

        # Diamantina fica na base, distancia zero
        if mn == _norm(cidade_base):
            municipios_visitados.append({
                "municipio": mun.strip().title(),
                "lat": base_coords[0] if base_coords else 0,
                "lon": base_coords[1] if base_coords else 0,
                "exames": exames,
                "distritos": [],
                "km": 0,
                "km_ida_volta": 0,
            })
            continue

        coords = _coords_municipio(mun)
        if not coords or not base_coords:
            continue

        km_ida = haversine(base_coords[0], base_coords[1], coords[0], coords[1])
        km_ida_volta = round(km_ida * 2, 1)

        # Distritos desse municipio
        distritos_do_mun = [
            (d, int(e)) for _, _, m, d, e in LOCAIS
            if _norm(m) == mn and d and int(e) > 0
        ]

        rotas.append({
            "origem": cidade_base,
            "destino": mun.strip().title(),
            "municipio": mun.strip().title(),
            "exames": exames,
            "km": round(km_ida, 1),
            "km_ida_volta": km_ida_volta,
        })

        municipios_visitados.append({
            "municipio": mun.strip().title(),
            "lat": coords[0],
            "lon": coords[1],
            "exames": exames,
            "distritos": [d for d, _ in distritos_do_mun],
            "km": round(km_ida, 1),
            "km_ida_volta": km_ida_volta,
        })

        total_estimado += km_ida_volta

    # MST entre municipios visitados (exceto Diamantina)
    coords_muns = {m["municipio"]: (m["lat"], m["lon"]) for m in municipios_visitados if m["km"] > 0}
    muns_list = list(coords_muns.keys())
    dist_minima = 0.0
    arestas = []

    if len(muns_list) >= 2:
        visitados = set()
        nao_visitados = set(muns_list)
        primeiro = cidade_base
        visitados.add(primeiro)
        nao_visitados.discard(primeiro)

        while nao_visitados:
            menor_dist = float("inf")
            melhor = None
            melhor_de = None
            for v in visitados:
                for nv in nao_visitados:
                    c1 = coords_muns.get(v, base_coords if v == cidade_base else None)
                    c2 = coords_muns.get(nv)
                    if not c1 or not c2:
                        continue
                    d = haversine(c1[0], c1[1], c2[0], c2[1])
                    if d < menor_dist:
                        menor_dist = d
                        melhor = nv
                        melhor_de = v
            if melhor:
                dist_minima += menor_dist
                arestas.append({"de": melhor_de, "para": melhor, "km": round(menor_dist, 1)})
                visitados.add(melhor)
                nao_visitados.discard(melhor)

    # Exames por local (distritos) - conta do DataFrame real
    exames_por_local = []
    if "Distrito" in df.columns:
        dist_real = df[df["Distrito"].ne("")].groupby("Distrito").size().reset_index(name="exames")
        for _, row in dist_real.iterrows():
            d = row["Distrito"]
            mun = _distrito_para_municipio(d) or d
            exames_por_local.append({
                "distrito": d,
                "municipio": mun.strip().title(),
                "exames": int(row["exames"]),
            })

    return {
        "cidade_base": cidade_base,
        "base_coords": base_coords,
        "total_locais": len([m for m in municipios_visitados if m["km"] > 0]),
        "locais_com_coords": len(rotas),
        "total_estimado_km": round(total_estimado, 1),
        "distancia_minima_percurso_km": round(dist_minima * 2, 1),
        "media_km_por_local": round(total_estimado / max(len(rotas), 1), 1),
        "rotas": rotas,
        "arestas_mst": arestas,
        "municipios_visitados": municipios_visitados,
        "exames_por_local": exames_por_local,
        "coords_muns": coords_muns,
    }