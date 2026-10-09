"""
Tema Plotly - Identidade visual UFVJM (claro).
"""

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#f7f8fa",
    font_color="#000000",
    font_family="IBM Plex Mono",
    xaxis=dict(gridcolor="#e7ebf1", linecolor="#cfd6df"),
    yaxis=dict(gridcolor="#e7ebf1", linecolor="#cfd6df"),
)


def chart_layout(fig, height=300, title_size=12, showlegend=False, **kw):
    base = dict(**PLOTLY_THEME, showlegend=showlegend, height=height,
                title_font_size=title_size, margin=dict(l=0, r=20, t=40, b=0))
    base.update(kw)
    fig.update_layout(**base)
    return fig