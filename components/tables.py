import streamlit as st


def render_tabela(df, rename_map=None, busca_label="Buscar na tabela"):
    tabela = df.copy()
    if rename_map:
        tabela = tabela.rename(columns=rename_map)
    busca = st.text_input(busca_label, "")
    if busca:
        mask = tabela.astype(str).apply(lambda row: row.str.contains(busca, case=False, na=False)).any(axis=1)
        tabela_f = tabela[mask]
    else:
        tabela_f = tabela
    st.caption(f"{len(tabela_f):,} de {len(tabela):,} registros.")
    st.dataframe(tabela_f, use_container_width=True, height=400)
    return tabela