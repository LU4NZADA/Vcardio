"""
Graficos municipais com interatividade.
"""

import plotly.express as px
import plotly.graph_objects as go
from charts.base import configurar_layout


def risco_territorial(risco_df):
    """Ranking de risco com cores por nivel e hover detalhado."""
    risco = risco_df.sort_values("pct").tail(15)
    if risco.empty:
        return None

    # Cores por nivel de risco
    cores = []
    for p in risco["pct"]:
        if p > 70:
            cores.append("#D64550")
        elif p > 50:
            cores.append("#D9902E")
        elif p > 30:
            cores.append("#E8C547")
        else:
            cores.append("#2E9E5B")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=risco["Cidade"], x=risco["pct"],
        orientation="h",
        marker=dict(color=cores, cornerradius=4, line=dict(width=0)),
        text=risco["pct"].apply(lambda x: f"{x}%"),
        textposition="outside",
        textfont=dict(size=11, color="#000000"),
        customdata=risco[["total", "alterados", "idade_media"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Alterados: <b>%{x:.1f}%</b><br>"
            "Total exames: %{customdata[0]:,.0f}<br>"
            "Laudos alterados: %{customdata[1]:,.0f}<br>"
            "Idade media: %{customdata[2]:.1f} anos<br>"
            "<extra></extra>"
        ),
    ))
    fig.add_vline(
        x=50, line_dash="dash", line_color="rgba(214,69,80,0.5)",
        annotation_text="Limiar 50%", annotation_font_color="#D64550",
    )
    fig.update_yaxes(categoryorder="total ascending")
    configurar_layout(
        fig, height=400,
        title="% laudos alterados (min 5 exames) — Cores por nivel de risco",
        margin=dict(l=0, r=60, t=50, b=0),
    )
    fig.update_xaxes(range=[0, 110], ticksuffix="%")

    # Legenda de cores
    legenda = (
        '<span style="color:#2E9E5B">● Baixo (&lt;30%)</span>  '
        '<span style="color:#E8C547">● Moderado (30-50%)</span>  '
        '<span style="color:#D9902E">● Alto (50-70%)</span>  '
        '<span style="color:#D64550">● Critico (&gt;70%)</span>'
    )
    return fig, legenda


def comorb_municipio(cm_df, label):
    """Ranking de comorbidade por municipio — hover detalhado."""
    if cm_df.empty:
        return None
    cm = cm_df.sort_values("Pct")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=cm["Cidade"], x=cm["Pct"],
        orientation="h",
        marker=dict(
            color=cm["Pct"],
            colorscale=[[0, "#eef3f9"], [0.5, "#D9902E"], [1, "#D64550"]],
            showscale=False,
            cornerradius=4, line=dict(width=0),
        ),
        text=cm["Pct"].apply(lambda x: f"{x}%"),
        textposition="outside",
        textfont=dict(size=11, color="#000000"),
        customdata=cm[["total", "positivos"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            f"{label}: <b>%{{x:.1f}}%</b><br>"
            "Total: %{customdata[0]:,.0f}<br>"
            "Positivos: %{customdata[1]:,.0f}<br>"
            "<extra></extra>"
        ),
    ))
    fig.update_yaxes(categoryorder="total ascending")
    configurar_layout(
        fig, height=360,
        title=f"Top municipios por {label} (%)",
    )
    return fig