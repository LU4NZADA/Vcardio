import streamlit as st
import pandas as pd
from config.colors import DIAG_COLORS
from config.app import COMORB_COLS

CIDADES_FORA_MG = {
    "Sao Paulo", "Campinas", "Ribeirao Preto", "Guarulhos", "Santo Andre",
    "Barueri", "Carapicuiba", "Diadema", "Suzano", "Taboao Da Serra",
    "Franco Da Rocha", "Atibaia", "Braganca Paulista", "Piracicaba", "Assis",
    "Ipeuna", "Itarare", "Maringa", "Mirandopolis", "Caraguatatuba",
    "Guararapes", "Sapezal",
    "Rio De Janeiro", "Duque De Caxias", "Nova Iguacu", "Macae",
    "Porto Alegre", "Manaus", "Brasilia", "Acarape", "Hidrolandia",
    "Massaranduba", "Picui", "Venturosa", "Lencois", "Araquari",
    "Uruacu", "Ponte Alta Do Tocantins", "Colatina", "Itabuna",
    "Agua Clara", "Cantagalo","Caetite",
}

def render_filtros(df_original):
    filtros = {}
    with st.sidebar:
        st.markdown("### Filtros")
        municipios = sorted([
            c for c in df_original["Cidade"].dropna().unique()
            if c not in CIDADES_FORA_MG
        ])
        filtros["mun"] = st.multiselect("Município (MG)", municipios, default=municipios)
        filtros["sex"] = st.multiselect("Sexo", ["Feminino", "Masculino", "Nao especificado"],
                                        default=["Feminino", "Masculino", "Nao especificado"])
        filtros["diag"] = st.multiselect("Diagnostico", list(DIAG_COLORS.keys()),
                                         default=list(DIAG_COLORS.keys()))
        with st.expander("Comorbidades"):
            filtros["hip"] = st.selectbox("Hipertenso", ["Todos", "Sim", "Nao"])
            filtros["diab"] = st.selectbox("Diabetes", ["Todos", "Sim", "Nao"])
            filtros["tab"] = st.selectbox("Tabagista", ["Todos", "Sim", "Nao"])
            filtros["etil"] = st.selectbox("Etilista", ["Todos", "Sim", "Nao"])
        if df_original["Data_cadastro"].notna().any():
            d_min = df_original["Data_cadastro"].min().date()
            d_max = df_original["Data_cadastro"].max().date()
            filtros["data"] = st.date_input("Periodo", value=(d_min, d_max), min_value=d_min, max_value=d_max)
        else:
            filtros["data"] = None
    return filtros


def aplicar_filtros(df, filtros):
    if filtros["mun"]:
        df = df[df["Cidade"].isin(filtros["mun"])]
    if filtros["sex"]:
        df = df[df["Sexo"].isin(filtros["sex"])]
    if filtros["diag"]:
        df = df[df["diag_cat"].isin(filtros["diag"])]
    for key, col in [("hip", "Hipertenso"), ("diab", "Diabetes Mellitus"),
                     ("tab", "Tabagista"), ("etil", "Etilista")]:
        val = filtros.get(key, "Todos")
        if val == "Sim":
            df = df[df[col] == 1]
        elif val == "Nao":
            df = df[df[col] == 0]
    data = filtros.get("data")
    if data and len(data) == 2:
        dt_fim = pd.Timestamp(data[1]) + pd.Timedelta(days=1)
        mask_data = (
            (df["Data_cadastro"] >= pd.Timestamp(data[0])) &
            (df["Data_cadastro"] < dt_fim)
        ) | df["Data_cadastro"].isna()
        df = df[mask_data]
    return df