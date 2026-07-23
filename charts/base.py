"""
Utilidades comuns para graficos Plotly com interatividade estilo Power BI.
Todas as figuras recebem hover rico, animacoes e controles interativos.
"""

import plotly.express as px
import plotly.graph_objects as go
from config.plotly import PLOTLY_THEME
from utils.textos import t


def aplicar_tema(fig, **overrides):
    tema = {**PLOTLY_THEME}
    tema.update(overrides)
    fig.update_layout(**tema)
    return fig


def configurar_layout(fig, height=300, title_size=13, showlegend=False, **kw):
    """Layout padrao com hovermode e dragmode interativos."""
    base = dict(
        **PLOTLY_THEME,
        showlegend=showlegend,
        height=height,
        title_font_size=title_size,
        title_font_color="#e6edf3",
        margin=dict(l=0, r=20, t=50, b=0),
        hovermode="closest",
        dragmode="pan",
        newshape=dict(line_color="#e24b4a"),
    )
    if "title" in kw and isinstance(kw["title"], str):
        kw["title"] = t(kw["title"])
    base.update(kw)
    fig.update_layout(**base)

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="#161b22",
            bordercolor="#30363d",
            font_size=12,
            font_color="#e6edf3",
            font_family="IBM Plex Mono",
            namelength=-1,
        )
    )
    return fig


def bar_horizontal(df, x, y, text="", color="#e24b4a", title="", hover_extra=None):
    custom = hover_extra if hover_extra else []
    fig = px.bar(
        df, x=x, y=y, orientation="h", text=text or x,
        color_discrete_sequence=[color], title=t(title),
        custom_data=custom,
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=11, color="#c9d1d9", family="IBM Plex Mono"),
        marker=dict(line=dict(width=0), cornerradius=4),
        hovertemplate=(
            "<b>%{y}</b><br>"
            f"{x}: <b>%{{x:,.0f}}</b><br>"
            "<extra></extra>"
        ),
    )
    fig.update_yaxes(categoryorder="total ascending")
    configurar_layout(fig, height=max(280, len(df) * 36))
    return fig


def heatmap_base(df, title="", colorscale=None, height_per_row=30):
    if colorscale is None:
        colorscale = [[0, "#0d1117"], [0.25, "#1a1f2e"], [0.5, "#30363d"],
                      [0.75, "#ba7517"], [1, "#e24b4a"]]
    fig = px.imshow(
        df, text_auto=True, aspect="auto",
        color_continuous_scale=colorscale, title=t(title),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b> x %{x}<br>"
            "Valor: <b>%{z:,.1f}</b><br>"
            "<extra></extra>"
        ),
    )
    configurar_layout(fig, height=max(300, len(df) * height_per_row))
    return fig


def criar_dropdown(fig, botoes, titulo="Filtrar por:", y=1.15):
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=botoes,
                direction="down",
                showactive=True,
                x=0.0, xanchor="left",
                y=y, yanchor="top",
                bgcolor="#161b22",
                bordercolor="#30363d",
                font=dict(color="#c9d1d9", size=11, family="IBM Plex Mono"),
                active=0,
            )
        ],
        annotations=[
            dict(
                text=t(titulo), x=0.0, y=y + 0.06, xref="paper", yref="paper",
                showarrow=False, font=dict(color="#8b949e", size=10, family="IBM Plex Mono"),
            )
        ],
    )
    return fig


def criar_range_slider(fig, visible=False):
    fig.update_xaxes(
        rangeslider=dict(visible=visible, bgcolor="#161b22", bordercolor="#30363d"),
        rangeselector=dict(
            buttons=[
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1a", step="year", stepmode="backward"),
                dict(step="all", label="Tudo"),
            ],
            bgcolor="#161b22",
            activecolor="#21262d",
            bordercolor="#30363d",
            font=dict(color="#c9d1d9", size=10),
        ),
    )
    return fig


def animar_bars(fig, duracao=500):
    fig.update_traces(marker=dict(line=dict(width=0)))
    fig.layout.transition = dict(duration=duracao, easing="cubic-in-out")
    return fig