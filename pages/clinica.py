import streamlit as st
import pandas as pd
from components import sub_header
from charts.clinical import top_bar, termos_bar
from analysis.nlp import extrair_termos
from utils.textos import t


def render(df, ind):
    sub_header("Analise de textos clinicos")
    has_hipo = not ind["hipoteses_freq"].empty
    has_ind = not ind["indicacoes_freq"].empty
    if not (has_hipo or has_ind):
        st.info("Nenhuma coluna qualitativa encontrada na planilha.")
        return
    if has_hipo:
        sub_header("Hipoteses diagnosticas")
        fig = top_bar(ind["hipoteses_freq"], "Frequencia", "Hipotese", "Top 20 hipoteses")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    if has_ind:
        sub_header("Indicacoes clinicas")
        fig = top_bar(ind["indicacoes_freq"], "Frequencia", "Indicacao", "Top 20 indicacoes", "#378add")
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    sub_header("Termos mais frequentes")
    opcoes = []
    if df["_obs"].astype(str).str.strip().ne("").any():
        opcoes.append(("Observacoes", "_obs"))
    if has_ind:
        opcoes.append(("Indicacao Clinica", "_indicacao"))
    if has_hipo:
        opcoes.append(("Hipotese Diagnostica", "_hipotese"))
    if opcoes:
        sel = st.selectbox("Campo", opcoes, format_func=lambda x: t(x[0]), key="termo_col")
        if sel:
            termos = extrair_termos(df[sel[1]])
            if not termos.empty:
                c1, c2 = st.columns([1.5, 1])
                with c1:
                    fig = termos_bar(termos)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                with c2:
                    st.markdown(f"**{t('Tabela de termos')}**")
                    st.dataframe(termos, use_container_width=True, height=440)
    sub_header("Busca textual")
    busca = st.text_input(t("Buscar nos campos clinicos"), key="busca_cli")
    if busca:
        mask = pd.Series(False, index=df.index)
        for c in ["_obs", "_indicacao", "_hipotese"]:
            mask = mask | df[c].astype(str).str.contains(busca, case=False, na=False)
        resultados = df[mask]
        st.caption(f"{len(resultados)} registro(s) para '{busca}'")
        if len(resultados) > 0:
            cols = ["Cidade", "Sexo", "idade", "diag_cat", "Data_cadastro"]
            for c in ["_obs", "_indicacao", "_hipotese"]:
                if resultados[c].astype(str).str.strip().ne("").any():
                    cols.append(c)
            display = resultados[cols].rename(columns={
                "idade": "Idade",
                "diag_cat": t("Diagnostico"),
                "Data_cadastro": "Data",
            })
            display["Data"] = pd.to_datetime(display["Data"], errors="coerce").dt.strftime("%d/%m/%Y")
            st.dataframe(display, use_container_width=True, height=350)