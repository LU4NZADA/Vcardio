"""
Graficos demograficos com interatividade estilo Power BI.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from charts.base import configurar_layout


def sexo_pie(sexo_counts):
    df = sexo_counts.copy()
    df = df.dropna(subset=["Sexo"])
    df["Qtd"] = pd.to_numeric(df["Qtd"], errors="coerce").fillna(0).astype(int)
    df = df[df["Qtd"] > 0]

    paleta = {
        "Feminino": "#e24b4a",
        "Masculino": "#378add",
    }
    cores = [paleta.get(s, "#30363d") for s in df["Sexo"]]

    fig = go.Figure(go.Pie(
        labels=df["Sexo"].tolist(),
        values=df["Qtd"].tolist(),
        hole=0.6,
        marker=dict(colors=cores, line=dict(color="#0d1117", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11, color="#c9d1d9"),
        hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>",
        pull=[0.02] * len(df),
    ))
    configurar_layout(
        fig, height=300,
        legend=dict(font_size=10, orientation="h", y=-0.15, font_color="#8b949e"),
    )
    return fig


def ano_bar(ano_counts):
    fig = px.bar(
        ano_counts, x="Ano", y="Qtd", text="Qtd",
        title="Exames por ano", color_discrete_sequence=["#e24b4a"],
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=11, color="#c9d1d9"),
        marker=dict(cornerradius=4, line=dict(width=0)),
        hovertemplate="<b>Ano %{x}</b><br>Exames: <b>%{y:,.0f}</b><extra></extra>",
    )
    configurar_layout(fig, height=300)
    return fig


def faixa_bar(faixa_counts):
    fig = px.bar(
        faixa_counts, x="Faixa", y="Qtd", text="Qtd",
        title="Exames por faixa etaria", color_discrete_sequence=["#7f77dd"],
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=11, color="#c9d1d9"),
        marker=dict(cornerradius=4, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Exames: <b>%{y:,.0f}</b><extra></extra>",
    )
    configurar_layout(fig, height=300)
    return fig


def piramide(piram_df):
    fig = px.bar(
        piram_df, x="Val", y="faixa", color="Sexo", orientation="h",
        color_discrete_map={"Feminino": "#e24b4a", "Masculino": "#378add"},
        title="Piramide etaria por sexo", barmode="overlay",
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>%{data.name}: <b>%{customdata[0]:,.0f}</b><extra></extra>",
        customdata=piram_df[["Qtd"]].values,
    )
    fig.update_xaxes(tickvals=[], title="")
    configurar_layout(
        fig, height=340,
        legend=dict(font_size=10, orientation="h", y=-0.1, font_color="#8b949e"),
    )
    return fig


def top_municipios(top_df):
    cores = [
        "#e24b4a" if i == 0 else "#ba7517" if i < 3 else "#30363d"
        for i in range(len(top_df))
    ]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top_df["Municipio"], y=top_df["Qtd"],
        marker=dict(color=cores, cornerradius=4, line=dict(width=0)),
        text=top_df["Qtd"], textposition="outside",
        textfont=dict(size=11, color="#c9d1d9"),
        hovertemplate="<b>%{x}</b><br>Exames: <b>%{y:,.0f}</b><extra></extra>",
    ))
    configurar_layout(fig, height=320, title="Top 15 municipios")
    fig.update_xaxes(tickangle=30)
    return fig


def sazonalidade(saz_df):
    fig = px.bar(
        saz_df, x="mes_nome", y="Qtd", text="Qtd",
        title="Sazonalidade dos exames", color_discrete_sequence=["#ba7517"],
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=11, color="#c9d1d9"),
        marker=dict(cornerradius=4, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Exames: <b>%{y:,.0f}</b><extra></extra>",
    )
    configurar_layout(fig, height=280)
    return fig