"""
Graficos clinicos.
"""

import plotly.express as px
from charts.base import configurar_layout


def top_bar(df_freq, x_col, y_col, title, color="#e24b4a"):
    if df_freq.empty:
        return None
    fig = px.bar(df_freq, x=x_col, y=y_col, orientation="h",
                 text=x_col, color_discrete_sequence=[color], title=title)
    fig.update_traces(textposition="outside")
    fig.update_yaxes(categoryorder="total ascending")
    configurar_layout(fig, height=max(300, len(df_freq) * 28))
    return fig


def termos_bar(termos_df):
    if termos_df.empty:
        return None
    fig = px.bar(termos_df.head(20), x="Frequencia", y="Termo", orientation="h",
                 text="Frequencia", color_discrete_sequence=["#ba7517"],
                 title="Top 20 termos")
    fig.update_traces(textposition="outside")
    fig.update_yaxes(categoryorder="total ascending")
    configurar_layout(fig, height=460)
    return fig