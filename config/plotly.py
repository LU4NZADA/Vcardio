"""
Tema Plotly.
"""

PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#161b22",
    font_color="#c9d1d9",
    font_family="IBM Plex Mono",
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
)


def chart_layout(fig, height=300, title_size=12, showlegend=False, **kw):
    base = dict(**PLOTLY_THEME, showlegend=showlegend, height=height,
                title_font_size=title_size, margin=dict(l=0, r=20, t=40, b=0))
    base.update(kw)
    fig.update_layout(**base)
    return fig