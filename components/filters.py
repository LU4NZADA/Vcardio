import streamlit as st
import pandas as pd
from config.colors import DIAG_COLORS
from config.app import COMORB_COLS
from constants_locais import LOCAIS, _norm


def _init_session_defaults(df: pd.DataFrame):
    if "filtros_inicializados" in st.session_state:
        return
    st.session_state.filtros_inicializados = True
    st.session_state.filtro_mun = sorted(df["Cidade"].dropna().unique().tolist())
    st.session_state.filtro_sex = ["Feminino", "Masculino", "Nao especificado"]
    st.session_state.filtro_diag = list(DIAG_COLORS.keys())
    st.session_state.filtro_hip = "Todos"
    st.session_state.filtro_diab = "Todos"
    st.session_state.filtro_tab = "Todos"
    st.session_state.filtro_etil = "Todos"
    st.session_state.filtro_faixa = []
    st.session_state.filtro_distrito = []
    if df["Data_cadastro"].notna().any():
        st.session_state.filtro_data = (df["Data_cadastro"].min().date(), df["Data_cadastro"].max().date())
    else:
        st.session_state.filtro_data = None


def _limpar_filtros(df: pd.DataFrame):
    st.session_state.filtro_mun = sorted(df["Cidade"].dropna().unique().tolist())
    st.session_state.filtro_sex = ["Feminino", "Masculino", "Nao especificado"]
    st.session_state.filtro_diag = list(DIAG_COLORS.keys())
    st.session_state.filtro_hip = "Todos"
    st.session_state.filtro_diab = "Todos"
    st.session_state.filtro_tab = "Todos"
    st.session_state.filtro_etil = "Todos"
    st.session_state.filtro_faixa = []
    st.session_state.filtro_distrito = []
    if df["Data_cadastro"].notna().any():
        st.session_state.filtro_data = (df["Data_cadastro"].min().date(), df["Data_cadastro"].max().date())
    st.rerun()


def render_filtros(df_original: pd.DataFrame) -> dict:
    _init_session_defaults(df_original)
    with st.sidebar:
        st.markdown("### Filtros")
        if st.button("Limpar todos os filtros", use_container_width=True, type="secondary"):
            _limpar_filtros(df_original)
        st.divider()
        municipios = sorted(df_original["Cidade"].dropna().unique().tolist())
        filtros_mun = st.multiselect("Municipio", options=municipios, key="filtro_mun")
        if filtros_mun:
            muns_norm = [_norm(m) for m in filtros_mun]
            distritos_locais = sorted(set(d for _, _, m, d, _ in LOCAIS if _norm(m) in muns_norm and d))
        else:
            distritos_locais = []
        atuais = [d for d in st.session_state.get("filtro_distrito", []) if d in distritos_locais]
        if not atuais and distritos_locais:
            atuais = distritos_locais
        filtros_distrito = st.multiselect("Distrito", options=distritos_locais, default=atuais, key="filtro_distrito") if distritos_locais else []
        filtros_sex = st.multiselect("Sexo", options=["Feminino", "Masculino", "Nao especificado"], key="filtro_sex")
        filtros_diag = st.multiselect("Diagnostico", options=list(DIAG_COLORS.keys()), key="filtro_diag")
        with st.expander("Comorbidades", expanded=False):
            filtro_hip = st.selectbox("Hipertenso", ["Todos", "Sim", "Nao"], key="filtro_hip")
            filtro_diab = st.selectbox("Diabetes", ["Todos", "Sim", "Nao"], key="filtro_diab")
            filtro_tab = st.selectbox("Tabagista", ["Todos", "Sim", "Nao"], key="filtro_tab")
            filtro_etil = st.selectbox("Etilista", ["Todos", "Sim", "Nao"], key="filtro_etil")
        if df_original["Data_cadastro"].notna().any():
            d_min = df_original["Data_cadastro"].min().date()
            d_max = df_original["Data_cadastro"].max().date()
            filtros_data = st.date_input("Periodo", min_value=d_min, max_value=d_max, key="filtro_data")
        else:
            filtros_data = None
        filtros = {
            "mun": filtros_mun, "distrito": filtros_distrito, "sex": filtros_sex,
            "diag": filtros_diag, "hip": filtro_hip, "diab": filtro_diab,
            "tab": filtro_tab, "etil": filtro_etil, "data": filtros_data,
        }
        df_temp = aplicar_filtros(df_original, filtros)
        n_total = len(df_original)
        n_filtrado = len(df_temp)
        pct = (n_filtrado / n_total * 100) if n_total > 0 else 0
        st.divider()
        if n_filtrado == 0:
            st.error(f"**0** de **{n_total:,}** registros")
        elif n_filtrado == n_total:
            st.success(f"**{n_filtrado:,}** de **{n_total:,}** registros (100%)")
        else:
            st.info(f"**{n_filtrado:,}** de **{n_total:,}** registros ({pct:.1f}%)")
    return filtros


def aplicar_filtros(df: pd.DataFrame, filtros: dict) -> pd.DataFrame:
    df = df.copy()
    muns_sel = filtros.get("mun", [])
    if muns_sel:
        col = "Municipio_Coleta" if "Municipio_Coleta" in df.columns else "Cidade"
        df = df[df[col].isin(muns_sel)]
    if "Sexo" in df.columns:
        df = df[df["Sexo"].isin(filtros.get("sex", []))]
    if "diag_cat" in df.columns:
        df = df[df["diag_cat"].isin(filtros.get("diag", []))]
    for key, col in [("hip", "Hipertenso"), ("diab", "Diabetes Mellitus"), ("tab", "Tabagista"), ("etil", "Etilista")]:
        val = filtros.get(key, "Todos")
        if col not in df.columns:
            continue
        if val == "Sim":
            df = df[df[col] == 1]
        elif val == "Nao":
            df = df[df[col] == 0]
    data = filtros.get("data")
    if isinstance(data, (tuple, list)) and len(data) == 2 and "Data_cadastro" in df.columns:
        dt_inicio = pd.Timestamp(data[0])
        dt_fim = pd.Timestamp(data[1]) + pd.Timedelta(days=1)
        df = df[(df["Data_cadastro"] >= dt_inicio) & (df["Data_cadastro"] < dt_fim)]
    return df