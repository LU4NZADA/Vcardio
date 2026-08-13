"""
Graficos de distancias percorridas pelo projeto.
"""

import pandas as pd
import plotly.graph_objects as go
from charts.base import configurar_layout
from constants import MUN_COORDS


def grafico_rotas_distritos(dist):
    rotas = dist["rotas"]
    if not rotas:
        return None

    # Agrupa por municipio para o grafico
    mun_dist = {}
    for r in rotas:
        mun = r["municipio"]
        if mun not in mun_dist:
            mun_dist[mun] = {"km": r["km"], "exames": 0}
        mun_dist[mun]["exames"] += r["exames"]

    df = pd.DataFrame([
        {"Local": f"{mun} ({info['exames']} exames)", "km": info["km"], "exames": info["exames"]}
        for mun, info in mun_dist.items()
    ]).sort_values("km", ascending=False).head(15)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["Local"], x=df["km"], orientation="h",
        marker=dict(
            color=df["km"],
            colorscale=[[0, "#639922"], [0.5, "#ba7517"], [1, "#e24b4a"]],
            showscale=False, cornerradius=4, line=dict(width=0),
        ),
        text=df["km"].apply(lambda x: f"{x:,.0f} km"),
        textposition="outside", textfont=dict(size=11, color="#c9d1d9"),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Distancia da base: <b>%{x:,.1f} km</b><br>"
            f"Base: {dist['cidade_base']}<br>"
            "<extra></extra>"
        ),
    ))
    fig.update_yaxes(categoryorder="total ascending")
    configurar_layout(
        fig, height=400,
        title=f"Distancia de {dist['cidade_base']} ate cada local de exame (km)",
        xaxis_title="Distancia (km)",
    )
    return fig


def grafico_mapa_distritos(dist):
    arestas = dist["arestas_mst"]
    muns = dist["municipios_visitados"]
    base_coords = dist.get("base_coords")
    cidade_base = dist.get("cidade_base", "Diamantina")

    if not muns:
        return None

    fig = go.Figure()

    # Linhas de conexao (MST)
    lats = []
    lons = []
    coords_muns = dist.get("coords_muns", {})
    for aresta in arestas:
        c1 = coords_muns.get(aresta["de"])
        c2 = coords_muns.get(aresta["para"])
        if c1 and c2:
            lats.extend([c1[0], c2[0], None])
            lons.extend([c1[1], c2[1], None])

    # Linhas da base ate cada municipio
    if base_coords:
        for m in muns:
            lats.extend([base_coords[0], m["lat"], None])
            lons.extend([base_coords[1], m["lon"], None])

    if lats:
        fig.add_trace(go.Scattermapbox(
            lat=lats, lon=lons, mode="lines",
            line=dict(width=1, color="rgba(226,75,74,0.3)"),
            hoverinfo="skip", showlegend=False,
        ))

    # Pontos dos municipios visitados
    if muns:
        fig.add_trace(go.Scattermapbox(
            lat=[m["lat"] for m in muns],
            lon=[m["lon"] for m in muns],
            mode="markers",
            marker=dict(
                size=[max(8, min(20, m["exames"] / 5)) for m in muns],
                color="#e24b4a", opacity=0.8,
            ),
            text=[f"{m['municipio']} ({m['exames']} exames)" for m in muns],
            hovertemplate="<b>%{text}</b><extra></extra>",
            showlegend=False,
        ))

    # Base (Diamantina)
    if base_coords:
        fig.add_trace(go.Scattermapbox(
            lat=[base_coords[0]], lon=[base_coords[1]], mode="markers+text",
            marker=dict(size=18, color="#e8c547", symbol="star"),
            text=[f"BASE: {cidade_base}"],
            textposition="top right",
            textfont=dict(size=11, color="#e8c547", family="IBM Plex Mono"),
            hovertemplate=f"<b>BASE: {cidade_base}</b><extra></extra>",
            showlegend=False,
        ))

    # Centrar mapa
    if muns:
        lats_all = [m["lat"] for m in muns]
        lons_all = [m["lon"] for m in muns]
        if base_coords:
            lats_all.append(base_coords[0])
            lons_all.append(base_coords[1])
        center_lat = sum(lats_all) / len(lats_all)
        center_lon = sum(lons_all) / len(lons_all)
    else:
        center_lat, center_lon = -17.5, -42.5

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=center_lat, lon=center_lon), zoom=7,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#161b22",
        font_color="#c9d1d9",
        font_family="IBM Plex Mono",
        height=560,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
    )
    return fig