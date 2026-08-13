import streamlit as st
import pandas as pd
from datetime import datetime
from components import sub_header
from constants import ECG_ACHADOS
from exports.csv import gerar_csv
from exports.excel import gerar_excel
from exports.pdf import gerar_pdf


def render(df, ind):
    sub_header("Tabela de dados detalhados")
    colunas = {"Cidade": "Municipio", "Distrito": "Distrito", "diag_cat": "Diagnostico", "Sexo": "Sexo",
               "idade": "Idade", "Data_cadastro": "Data do Exame",
               "Hipertenso": "Hipertenso", "Diabetes Mellitus": "Diabetes",
               "Tabagista": "Tabagista", "Etilista": "Etilista"}
    achado_names = {}
    for cat, subcats in ECG_ACHADOS.items():
        for nome in subcats:
            c = f"_ach_{nome}"
            if c in df.columns and df[c].sum() > 0:
                colunas[c] = nome
                achado_names[c] = nome
    cols_pres = [c for c in colunas if c in df.columns]
    tabela = df[cols_pres].rename(columns=colunas).sort_values("Data do Exame", ascending=False).reset_index(drop=True)
    tabela["Data do Exame"] = pd.to_datetime(tabela["Data do Exame"], errors="coerce").dt.strftime("%d/%m/%Y")
    for nc, dn in achado_names.items():
        if dn in tabela.columns:
            tabela[dn] = tabela[dn].map({1: "V", 0: ""})
    busca = st.text_input("Buscar na tabela", "")
    if busca:
        mask = tabela.astype(str).apply(lambda row: row.str.contains(busca, case=False, na=False)).any(axis=1)
        tabela_f = tabela[mask]
    else:
        tabela_f = tabela
    st.caption(f"{len(tabela_f):,} de {len(tabela):,} registros.")
    st.dataframe(tabela_f, use_container_width=True, height=450)
    sub_header("Exportacao")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("CSV", data=gerar_csv(tabela),
                           file_name=f"vigilancia_{datetime.now():%Y%m%d}.csv", mime="text/csv", use_container_width=True)
    with c2:
        st.download_button("Excel", data=gerar_excel(tabela, ind),
                           file_name=f"vigilancia_{datetime.now():%Y%m%d}.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with c3:
        pdf = gerar_pdf(df, ind)
        if pdf:
            st.download_button("PDF", data=pdf,
                               file_name=f"relatorio_{datetime.now():%Y%m%d}.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.info("Instale fpdf2: pip install fpdf2")