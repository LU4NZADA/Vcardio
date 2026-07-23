"""
Heatmaps genericos.
"""

import plotly.express as px
from charts.base import configurar_layout


def heatmap_generic(pivot_df, title, colorscale=None):
    if pivot_df.empty:
        return None
    if colorscale is None:
        colorscale = [[0, "#0d1117"], [0.5, "#30363d"], [1, "#e24b4a"]]
    fig = px.imshow(pivot_df, text_auto=True, aspect="auto",
                    color_continuous_scale=colorscale, title=title)
    configurar_layout(fig, height=max(300, len(pivot_df) * 28))
    return fig


def heatmap_percent(pivot_df, title, colorscale=None):
    if pivot_df.empty:
        return None
    if colorscale is None:
        colorscale = [[0, "#0d1117"], [0.5, "#30363d"], [1, "#ba7517"]]
    fig = px.imshow(pivot_df, text_auto=".1f", aspect="auto",
                    color_continuous_scale=colorscale, title=title)
    configurar_layout(fig, height=max(300, len(pivot_df) * 28))
    return fig