"""
Heatmaps genericos.
"""

import plotly.express as px
from charts.base import configurar_layout


def heatmap_generic(pivot_df, title, colorscale=None):
    if pivot_df.empty:
        return None
    if colorscale is None:
        colorscale = [[0, "#f2f7fc"], [0.5, "#9cc3e8"], [1, "#D64550"]]
    fig = px.imshow(pivot_df, text_auto=True, aspect="auto",
                    color_continuous_scale=colorscale, title=title)
    configurar_layout(fig, height=max(300, len(pivot_df) * 28))
    return fig


def heatmap_percent(pivot_df, title, colorscale=None):
    if pivot_df.empty:
        return None
    if colorscale is None:
        colorscale = [[0, "#f2f7fc"], [0.5, "#9cc3e8"], [1, "#D9902E"]]
    fig = px.imshow(pivot_df, text_auto=".1f", aspect="auto",
                    color_continuous_scale=colorscale, title=title)
    configurar_layout(fig, height=max(300, len(pivot_df) * 28))
    return fig