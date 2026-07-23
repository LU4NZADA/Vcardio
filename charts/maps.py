"""
Mapas Scattermapbox com hover rico e legenda de cores.
"""

import plotly.graph_objects as go
from config.plotly import PLOTLY_THEME
from components.filters import CIDADES_FORA_MG


def mapa_risco(mapa_df):
    """Mapa de risco com tamanhos proporcionais e hover detalhado."""
    mp = mapa_df.dropna(subset=["lat"]).copy()
    mp = mp[~mp["Cidade"].isin(CIDADES_FORA_MG)]
    if mp.empty:
        return None

    mp["size"] = mp["exames"].apply(lambda x: max(16, min(x * 2, 55)))
    mp["cor"] = mp["pct"].apply(
        lambda p: "#e24b4a" if p > 70 else "#ba7517" if p > 50
        else "#e8c547" if p > 30 else "#639922"
    )
    mp["risco"] = mp["pct"].apply(
        lambda p: "Critico" if p > 70 else "Alto" if p > 50
        else "Moderado" if p > 30 else "Baixo"
    )

    fig = go.Figure()

    fig.add_trace(go.Scattermapbox(
        lat=mp["lat"], lon=mp["lon"], mode="markers+text",
        marker=dict(size=mp["size"], color=mp["cor"], opacity=0.85, sizemode="area"),
        text=mp["Cidade"], textposition="top right",
        textfont=dict(size=9, color="#c9d1d9", family="IBM Plex Mono"),
        customdata=mp[["exames", "alterados", "pct", "risco"]].values,
        hovertemplate=(
            "<b>%{text}</b><br>"
            "--------------------<br>"
            "Exames total: <b>%{customdata[0]:,.0f}</b><br>"
            "Laudos alterados: <b>%{customdata[1]:,.0f}</b><br>"
            "% Alterados: <b>%{customdata[2]:.1f}%</b><br>"
            "Classificacao: <b>%{customdata[3]}</b><br>"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        annotations=[
            dict(
                text=(
                    '<span style="color:#639922">Baixo (&lt;30%)</span><br>'
                    '<span style="color:#e8c547">Moderado (30-50%)</span><br>'
                    '<span style="color:#ba7517">Alto (50-70%)</span><br>'
                    '<span style="color:#e24b4a">Critico (&gt;70%)</span>'
                ),
                x=0.01, y=0.99, xref="paper", yref="paper",
                showarrow=False,
                bgcolor="rgba(13,17,23,0.85)",
                bordercolor="#30363d", borderwidth=1,
                borderpad=8,
                font=dict(size=10, family="IBM Plex Mono", color="#c9d1d9"),
                align="left",
            ),
        ],
    )

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=-17.5, lon=-42.5), zoom=6.5,
        ),
        **PLOTLY_THEME, height=560, margin=dict(l=0, r=0, t=10, b=0),
        hoverlabel=dict(
            bgcolor="#161b22", bordercolor="#30363d",
            font_size=12, font_color="#e6edf3", font_family="IBM Plex Mono",
        ),
    )
    return fig


def mapa_simples(mapa_df, cidade_destaque=None, df=None):
    """Mapa simples de distribuicao com opcao de destaque."""
    from constants import MUN_COORDS

    # Se mapa_df nao tem lat/lon, monta direto do df
    if "lat" not in mapa_df.columns or mapa_df["lat"].isna().all():
        if df is not None:
            contagem = df.groupby("Cidade").size().reset_index(name="exames")
            contagem["lat"] = contagem["Cidade"].map(lambda c: MUN_COORDS.get(c, (None, None))[0])
            contagem["lon"] = contagem["Cidade"].map(lambda c: MUN_COORDS.get(c, (None, None))[1])
            contagem["pct"] = 0
            contagem["alterados"] = 0
            mp = contagem
        else:
            mp = mapa_df.copy()
    else:
        mp = mapa_df.copy()

    mp = mp[~mp["Cidade"].isin(CIDADES_FORA_MG)]
    mp = mp.dropna(subset=["lat"])
    if mp.empty:
        return None

    mp["size"] = mp["exames"].apply(lambda x: max(16, min(x * 1.5, 50)))

    fig = go.Figure()

    if cidade_destaque:
        fig.add_trace(go.Scattermapbox(
            lat=mp["lat"], lon=mp["lon"], mode="markers+text",
            marker=dict(size=mp["size"], color="#e24b4a", opacity=0.35, sizemode="area"),
            text=mp["Cidade"], textposition="top right",
            textfont=dict(size=8, color="#8b949e", family="IBM Plex Mono"),
            customdata=mp[["exames"]].values,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Exames: <b>%{customdata[0]:,.0f}</b><br>"
                "<extra></extra>"
            ),
        ))

        lat_d, lon_d = MUN_COORDS.get(cidade_destaque, (-17.5, -42.5))
        exames_d = mp[mp["Cidade"] == cidade_destaque]["exames"]
        if not exames_d.empty:
            n_exames = int(exames_d.iloc[0])
        elif df is not None:
            n_exames = int(len(df[df["Cidade"] == cidade_destaque]))
        else:
            n_exames = 0

        fig.add_trace(go.Scattermapbox(
            lat=[lat_d], lon=[lon_d], mode="markers+text",
            marker=dict(size=45, color="#e8c547", opacity=1.0, sizemode="area"),
            text=[f"{cidade_destaque} ({n_exames} exames)"],
            textposition="top right",
            textfont=dict(size=13, color="#e8c547", family="IBM Plex Mono"),
            hovertemplate=(
                f"<b>{cidade_destaque}</b><br>"
                f"Exames: <b>{n_exames:,.0f}</b><br>"
                "<extra></extra>"
            ),
        ))

        center = dict(lat=lat_d, lon=lon_d)
        zoom = 11
    else:
        fig.add_trace(go.Scattermapbox(
            lat=mp["lat"], lon=mp["lon"], mode="markers+text",
            marker=dict(size=mp["size"], color="#e24b4a", opacity=0.8, sizemode="area"),
            text=mp["Cidade"], textposition="top right",
            textfont=dict(size=9, color="#c9d1d9", family="IBM Plex Mono"),
            customdata=mp[["exames"]].values,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Exames: <b>%{customdata[0]:,.0f}</b><br>"
                "<extra></extra>"
            ),
        ))

        center = dict(lat=-17.5, lon=-42.5)
        zoom = 6.5

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=center, zoom=zoom,
        ),
        **PLOTLY_THEME, height=460, margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
    )
    return fig