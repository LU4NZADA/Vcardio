"""
Gráficos ECG com interatividade.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from charts.base import configurar_layout


def achados_bar(df_ach, title, color="#e24b4a"):
    if df_ach.empty:
        return None
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_ach["Achado"], x=df_ach["Casos"],
        orientation="h",
        marker=dict(
            color=df_ach["%"],
            colorscale=[[0, "#21262d"], [0.3, "#30363d"], [0.6, color], [1, color]],
            showscale=True,
            colorbar=dict(
                title=dict(text="%", font=dict(color="#8b949e", size=10)),
                tickfont=dict(color="#8b949e", size=9),
                len=0.6, thickness=12,
                bgcolor="rgba(0,0,0,0)",
                bordercolor="#30363d",
            ),
            cornerradius=4, line=dict(width=0),
        ),
        text=df_ach["Casos"],
        textposition="outside",
        textfont=dict(size=11, color="#c9d1d9"),
        customdata=df_ach["%"],
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Casos: <b>%{x:,.0f}</b><br>"
            "Prevalencia: <b>%{customdata:.1f}%</b><br>"
            "<extra></extra>"
        ),
    ))
    fig.update_yaxes(categoryorder="total ascending")
    configurar_layout(fig, height=max(300, len(df_ach) * 38), title=title)
    return fig


def achados_por_sexo(matrix_df, title):
    if matrix_df.empty:
        return None
    melted = matrix_df.reset_index().melt(
        id_vars="Achado", var_name="Sexo", value_name="Qtd"
    )
    fig = px.bar(
        melted, x="Achado", y="Qtd", color="Sexo", barmode="group",
        color_discrete_map={"Feminino": "#e24b4a", "Masculino": "#378add"},
        title=title,
    )
    fig.update_traces(
        marker=dict(cornerradius=3, line=dict(width=0)),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "%{data.name}: <b>%{y:,.0f}</b><br>"
            "<extra></extra>"
        ),
    )
    configurar_layout(
        fig, height=360,
        legend=dict(font_size=10, orientation="h", y=-0.2, font_color="#8b949e"),
    )
    fig.update_xaxes(tickangle=20)
    return fig


def achados_por_faixa(matrix_df, title, colorscale=None):
    if matrix_df.empty:
        return None
    if colorscale is None:
        colorscale = [[0, "#0d1117"], [0.25, "#1a1f2e"], [0.5, "#30363d"],
                      [0.75, "#ba7517"], [1, "#e24b4a"]]
    fig = px.imshow(
        matrix_df, text_auto=True, aspect="auto",
        color_continuous_scale=colorscale, title=title,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Faixa: %{x}<br>"
            "Casos: <b>%{z:,.0f}</b><br>"
            "<extra></extra>"
        ),
    )
    configurar_layout(fig, height=max(320, len(matrix_df) * 30))
    return fig


def comorb_prevalencia(prev_df, title):
    if prev_df.empty:
        return None
    data = prev_df.drop(columns="N", errors="ignore")
    fig = px.imshow(
        data.T, text_auto=".1f", aspect="auto",
        color_continuous_scale=[[0, "#0d1117"], [0.25, "#1a1f2e"],
                                [0.5, "#30363d"], [0.75, "#ba7517"], [1, "#e24b4a"]],
        title=title,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Achado: %{x}<br>"
            "Prevalencia: <b>%{z:.1f}%</b><br>"
            "<extra></extra>"
        ),
    )
    configurar_layout(fig, height=240)
    return fig


def boxplot_idade(box_df, title):
    if box_df.empty:
        return None
    fig = px.box(
        box_df, x="Achado", y="idade", color="Achado",
        title=title, labels={"idade": "Idade (anos)", "Achado": ""},
    )
    fig.update_traces(
        hoverinfo="x+y+name",
        marker=dict(opacity=0.7),
        boxpoints="outliers",
        jitter=0.3,
    )
    configurar_layout(fig, height=340, showlegend=False)
    return fig


def treemap_achados(achados_dict, title="Mapa de achados ECG"):
    """Treemap interativo com tamanhos proporcionais e hover detalhado."""
    rows = []
    for cat, df_ach in achados_dict.items():
        if df_ach is not None and not df_ach.empty:
            for _, r in df_ach.iterrows():
                rows.append({
                    "Categoria": cat,
                    "Achado": r["Achado"],
                    "Casos": int(r["Casos"]),
                    "Prevalencia": float(r["%"]),
                })
    if not rows:
        return None

    df = pd.DataFrame(rows)
    df["label"] = df.apply(
        lambda r: f"{r['Achado']}<br>{r['Casos']} casos ({r['Prevalencia']:.1f}%)",
        axis=1,
    )

    paleta = {
        "Arritmias": "#e24b4a",
        "Bloqueios": "#378add",
        "Repolarizacao": "#ba7517",
        "Sobrecargas": "#7f77dd",
        "Fibroses": "#d85a30",
        "Baixa Voltagem": "#8b949e",
        "Conducao": "#39d2c0",
        "Eixo": "#e8c547",
    }

    fig = px.treemap(
        df,
        path=["Categoria", "Achado"],
        values="Casos",
        color="Categoria",
        color_discrete_map=paleta,
        title=title,
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Casos: <b>%{value:,.0f}</b><br>"
            "<extra></extra>"
        ),
        textinfo="label+value+percent parent",
        textfont=dict(size=12, color="#e6edf3"),
        marker=dict(cornerradius=4, line=dict(width=2, color="#0d1117")),
    )
    configurar_layout(
        fig, height=500, title_size=13,
        margin=dict(l=10, r=10, t=50, b=10),
    )
    return fig