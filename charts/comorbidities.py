"""
Graficos de comorbidades.
"""

import plotly.express as px
from charts.base import configurar_layout


def comorb_sexo(df_cs):
    if df_cs.empty:
        return None
    fig = px.bar(df_cs, x="Comorbidade", y="Pct", color="Sexo", barmode="group",
                 color_discrete_map={"Feminino": "#e24b4a", "Masculino": "#378add"},
                 text="Pct", title="Comorbidades por sexo")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    configurar_layout(fig, height=280)
    return fig


def comorb_faixa(df_cf):
    if df_cf.empty:
        return None
    fig = px.line(df_cf, x="Faixa", y="Pct", color="Comorbidade",
                  markers=True, title="Comorbidades por faixa etaria",
                  color_discrete_sequence=["#e24b4a", "#ba7517", "#8b949e", "#378add"])
    configurar_layout(fig, height=300)
    return fig


def sexo_diag_crosstab(crosstab_df):
    if crosstab_df.empty:
        return None
    fig = px.imshow(crosstab_df, text_auto=".1f", aspect="auto",
                    color_continuous_scale=[[0, "#0d1117"], [0.5, "#30363d"], [1, "#639922"]],
                    title="% diagnostico por sexo")
    configurar_layout(fig, height=220)
    return fig