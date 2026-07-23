"""
Pagina Sobre o Projeto.
"""

import streamlit as st


def render():
    st.markdown("""
    <style>
    .sobre-hero {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 40px;
        margin-bottom: 24px;
        text-align: center;
    }
    .sobre-hero h1 {
        color: #e6edf3;
        font-size: 28px;
        margin-bottom: 8px;
    }
    .sobre-hero .sub {
        color: #e24b4a;
        font-size: 14px;
        font-family: 'IBM Plex Mono', monospace;
        letter-spacing: 0.05em;
    }
    .sobre-hero .desc {
        color: #8b949e;
        font-size: 14px;
        max-width: 700px;
        margin: 20px auto 0;
        line-height: 1.7;
    }
    .sobre-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 16px;
    }
    .sobre-card h3 {
        color: #e6edf3;
        font-size: 16px;
        margin-bottom: 16px;
        border-bottom: 2px solid #e24b4a;
        padding-bottom: 8px;
        display: inline-block;
    }
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }
    .info-item {
        background: #0d1117;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 14px;
    }
    .info-item .label {
        color: #8b949e;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 4px;
    }
    .info-item .valor {
        color: #e6edf3;
        font-size: 14px;
        font-weight: 600;
    }
    .lgpd-box {
        background: #0d1117;
        border: 1px solid #639922;
        border-radius: 10px;
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .lgpd-icon {
        font-size: 36px;
        color: #639922;
        min-width: 50px;
        text-align: center;
    }
    .lgpd-text {
        color: #8b949e;
        font-size: 13px;
        line-height: 1.6;
    }
    .lgpd-text strong {
        color: #639922;
    }
    .tech-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
    }
    .tech-item {
        background: #0d1117;
        border: 1px solid #21262d;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }
    .tech-item .nome {
        color: #e6edf3;
        font-size: 13px;
        font-weight: 600;
    }
    .tech-item .det {
        color: #8b949e;
        font-size: 11px;
        margin-top: 4px;
    }
    </style>

    <div class="sobre-hero">
        <h1>Painel Inteligente de Vigil\u00e2ncia Cardiovascular</h1>
        <div class="sub">PIBIC / UFVJM / EDITAL 005/2025</div>
        <div class="desc">
            Dashboard interativo para vigil\u00e2ncia epidemiol\u00f3gica cardiovascular,
            desenvolvido no \u00e2mbito do Projeto Sa\u00fade Digital M\u00f3vel, iniciativa do
            Minist\u00e9rio da Sa\u00fade em parceria com a UFVJM.
        </div>
    </div>

    <div class="sobre-card">
        <h3>Informa\u00e7\u00f5es Institucionais</h3>
        <div class="info-grid">
            <div class="info-item">
                <div class="label">Programa</div>
                <div class="valor">PIBIC</div>
            </div>
            <div class="info-item">
                <div class="label">Edital</div>
                <div class="valor">005/2025</div>
            </div>
            <div class="info-item">
                <div class="label">Proponente</div>
                <div class="valor">Prof. Mariana Roberta Lopes Sim\u00f5es</div>
            </div>
            <div class="info-item">
                <div class="label">Institui\u00e7\u00e3o</div>
                <div class="valor">UFVJM - Campus JK</div>
            </div>
            <div class="info-item">
                <div class="label">Regi\u00e3o</div>
                <div class="valor">Vale do Jequitinhonha, MG</div>
            </div>
            <div class="info-item">
                <div class="label">Base do Projeto</div>
                <div class="valor">Diamantina, MG</div>
            </div>
        </div>
    </div>

    <div class="sobre-card">
        <h3>Prote\u00e7\u00e3o de Dados</h3>
        <div class="lgpd-box">
            <div class="lgpd-icon">&#128274;</div>
            <div class="lgpd-text">
                Todos os dados s\u00e3o <strong>anonimizados</strong> em conformidade com a
                <strong>LGPD - Lei n\u00ba 13.709/2018</strong>.<br>
                Nenhum dado pessoal identific\u00e1vel \u00e9 armazenado ou transmitido.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)