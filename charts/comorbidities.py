"""
Graficos de comorbidades.
"""

import plotly.express as px
from charts.base import configurar_layout


def comorb_sexo(df_cs):
    if df_cs.empty:
        return None
    fig = px.bar(df_cs, x="Comorbidade", y="Pct", color="Sexo", barmode="group",
                 color_discrete_map={"Feminino": "#D64550", "Masculino": "#2969BD"},
                 text="Pct", title="Comorbidades por sexo")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    configurar_layout(fig, height=280)
    return fig


def comorb_faixa(df_cf):
    if df_cf.empty:
        return None
    fig = px.line(df_cf, x="Faixa", y="Pct", color="Comorbidade",
                  markers=True, title="Comorbidades por faixa etaria",
                  color_discrete_sequence=["#2969BD", "#D9902E", "#8B9BB4", "#244A7C"])
    configurar_layout(fig, height=300)
    return fig


def sexo_diag_crosstab(crosstab_df):
    if crosstab_df.empty:
        return None
    fig = px.imshow(crosstab_df, text_auto=".1f", aspect="auto",
                    color_continuous_scale=[[0, "#f2f7fc"], [0.5, "#cfe3d8"], [1, "#2E9E5B"]],
                    title="% diagnostico por sexo")
    configurar_layout(fig, height=220)
    return fig