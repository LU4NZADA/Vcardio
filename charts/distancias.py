"""
Gráficos de distâncias percorridas pelo projeto.
"""

import pandas as pd
import plotly.graph_objects as go
from charts.base import configurar_layout


def grafico_rotas(distancias):
    data = distancias["cidades_mais_distantes_base"]
    if not data:
        return None
    df = pd.DataFrame(data).head(15)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df["Cidade"], x=df["km"], orientation="h",
        marker=dict(
            color=df["km"],
            colorscale=[[0, "#639922"], [0.5, "#ba7517"], [1, "#e24b4a"]],
            showscale=False, cornerradius=4, line=dict(width=0),
        ),
        text=df["km"].apply(lambda x: f"{x:,.0f} km"),
        textposition="outside", textfont=dict(size=11, color="#c9d1d9"),
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Distância da base: <b>%{x:,.1f} km</b><br>"
            f"Base: {distancias['cidade_base']}<br>"
            "<extra></extra>"
        ),
    ))
    fig.update_yaxes(categoryorder="total ascending")
    configurar_layout(
        fig, height=400,
        title=f"Distância de {distancias['cidade_base']} até cada município (km)",
        xaxis_title="Distância (km)",
    )
    return fig


def grafico_mapa_distancias(distancias, mapa_coords):
    if not distancias["arestas_mst"]:
        return None
    from constants import MUN_COORDS

    fig = go.Figure()

    # Linhas de conexao - todas juntas em um unico trace
    lats = []
    lons = []
    for aresta in distancias["arestas_mst"]:
        de_coords = MUN_COORDS.get(aresta["de"])
        para_coords = MUN_COORDS.get(aresta["para"])
        if de_coords and para_coords:
            lats.extend([de_coords[0], para_coords[0], None])
            lons.extend([de_coords[1], para_coords[1], None])

    if lats:
        fig.add_trace(go.Scattermapbox(
            lat=lats, lon=lons, mode="lines",
            line=dict(width=1.5, color="rgba(226,75,74,0.4)"),
            hoverinfo="skip",
            showlegend=False,
        ))

    # Pontos das cidades
    cidades_visitadas = [c for c in distancias["rotas"] if c.get("destino")]
    pts = pd.DataFrame([
        {"Cidade": r["destino"],
         "lat": MUN_COORDS[r["destino"]][0],
         "lon": MUN_COORDS[r["destino"]][1],
         "km": r["km"]}
        for r in cidades_visitadas
        if r["destino"] in MUN_COORDS
    ])

    if not pts.empty:
        fig.add_trace(go.Scattermapbox(
            lat=pts["lat"], lon=pts["lon"], mode="markers",
            marker=dict(size=8, color="#e24b4a", opacity=0.9),
            text=pts["Cidade"],
            customdata=pts[["km"]].values,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Distância da base: <b>%{customdata[0]:,.1f} km</b><br>"
                "<extra></extra>"
            ),
            showlegend=False,
        ))

    # Base (Diamantina)
    base = MUN_COORDS.get(distancias["cidade_base"])
    if base:
        fig.add_trace(go.Scattermapbox(
            lat=[base[0]], lon=[base[1]], mode="markers+text",
            marker=dict(size=18, color="#e8c547", symbol="star"),
            text=[f"BASE: {distancias['cidade_base']}"],
            textposition="top right",
            textfont=dict(size=11, color="#e8c547", family="IBM Plex Mono"),
            hovertemplate=f"<b>BASE: {distancias['cidade_base']}</b><extra></extra>",
            showlegend=False,
        ))

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=-17.5, lon=-42.5), zoom=6.5,
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