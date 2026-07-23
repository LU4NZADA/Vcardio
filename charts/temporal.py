"""
Graficos temporais com range slider interativo.
"""

import plotly.express as px
from config.colors import DIAG_COLORS
from charts.base import configurar_layout, criar_range_slider


def evolucao_mensal(tempo_df):
    """Area empilhada mensal — com range slider e hover rico."""
    fig = px.area(
        tempo_df, x="Mes", y="Qtd", color="diag_cat",
        color_discrete_map=DIAG_COLORS,
        title="Evolucao mensal por categoria",
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "%{data.name}: <b>%{y:,.0f}</b><br>"
            "<extra></extra>"
        ),
        line=dict(width=1),
    )
    configurar_layout(
        fig, height=360,
        legend=dict(font_size=10, orientation="h", y=-0.15, font_color="#8b949e"),
    )
    fig.update_xaxes(tickangle=30)
    criar_range_slider(fig, visible=True)
    return fig


def taxa_alteracao(taxa_df):
    """Linha com marcadores — range slider interativo."""
    fig = px.line(
        taxa_df, x="Mes", y="Pct_Alterados",
        title="% laudos alterados por mes",
        markers=True,
        color_discrete_sequence=["#e24b4a"],
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Alterados: <b>%{y:.1f}%</b><br>"
            "<extra></extra>"
        ),
        line=dict(width=3),
        marker=dict(size=8, line=dict(width=2, color="#0d1117")),
    )
    configurar_layout(fig, height=300)
    fig.update_xaxes(tickangle=30)
    criar_range_slider(fig, visible=True)
    return fig