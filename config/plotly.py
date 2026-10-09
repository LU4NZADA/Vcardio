"""
Tema Plotly - Identidade visual UFVJM (claro).
Fontes forcadas em preto (#000000) para legibilidade sobre fundo claro.
"""

PRETO = "#000000"

PLOTLY_THEME = dict(
    template="plotly_white",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#f7f8fa",
    font_color=PRETO,
    font_family="IBM Plex Mono",
    title_font_color=PRETO,
    xaxis=dict(
        gridcolor="#e7ebf1",
        linecolor="#cfd6df",
        tickfont=dict(color=PRETO),
        title_font=dict(color=PRETO),
        zerolinecolor="#e7ebf1",
    ),
    yaxis=dict(
        gridcolor="#e7ebf1",
        linecolor="#cfd6df",
        tickfont=dict(color=PRETO),
        title_font=dict(color=PRETO),
        zerolinecolor="#e7ebf1",
    ),
    coloraxis_colorbar=dict(
        tickfont=dict(color=PRETO),
        title_font=dict(color=PRETO),
    ),
    legend=dict(font=dict(color=PRETO)),
)


def aplicar_fontes_pretas(fig):
    """Garante tick/title fonts pretas mesmo se o template sobrescrever."""
    for eixo in ("xaxis", "yaxis"):
        fig.update_layout({
            eixo: {
                "tickfont": {"color": PRETO},
                "title": {"font": {"color": PRETO}},
            }
        })
    fig.update_layout(title_font_color=PRETO, font_color=PRETO)
    return fig


def chart_layout(fig, height=300, title_size=12, showlegend=False, **kw):
    base = dict(**PLOTLY_THEME, showlegend=showlegend, height=height,
                title_font_size=title_size, margin=dict(l=0, r=20, t=40, b=0))
    base.update(kw)
    fig.update_layout(**base)
    aplicar_fontes_pretas(fig)
    return fig
