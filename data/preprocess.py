import pandas as pd
from config.app import MESES_PT, BINS_IDADE, LABELS_IDADE
from analysis.classificacao import categorizar_diagnostico, classificar_achados
from constants_locais import buscar_distrito, buscar_municipio_coleta


def processar_dados(df):
    df = df.copy()
    df["Data_Nascimento"] = pd.to_datetime(df["Data_Nascimento"], errors="coerce")
    df["Data_cadastro"] = pd.to_datetime(df["Data_cadastro"], errors="coerce")
    hoje = pd.Timestamp.now()
    df["idade"] = ((hoje - df["Data_Nascimento"]).dt.days / 365.25).round(0).astype("Int64")
    df["idade"] = df["idade"].fillna(0)
    df["Cidade"] = df["Cidade"].fillna("Nao informado").str.strip().str.title()
    
    def processar_dados(df):
        df = df.copy()
        df["Data_Nascimento"] = pd.to_datetime(df["Data_Nascimento"], errors="coerce")
        df["Data_cadastro"] = pd.to_datetime(df["Data_cadastro"], errors="coerce")
        hoje = pd.Timestamp.now()
        df["idade"] = ((hoje - df["Data_Nascimento"]).dt.days / 365.25).round(0).astype("Int64")
        df["idade"] = df["idade"].fillna(0)
        df["Cidade"] = df["Cidade"].fillna("Nao informado").str.strip().str.title()

        # =============================================
        # FILTRO: manter apenas municipios do VJ
        # =============================================
    

        df["Sexo"] = df["Sexo"].fillna("Nao especificado").str.strip()
        df.loc[df["Sexo"].str.contains("especificado", case=False, na=False), "Sexo"] = "Nao especificado"
        df["diag_cat"] = df.apply(categorizar_diagnostico, axis=1)
        df = classificar_achados(df)
        df["mes"] = df["Data_cadastro"].dt.to_period("M").dt.to_timestamp()
        df["ano"] = df["Data_cadastro"].dt.year
        df["mes_num"] = df["Data_cadastro"].dt.month
        df["mes_nome"] = df["mes_num"].map(MESES_PT)
        df["trimestre"] = "T" + ((df["Data_cadastro"].dt.month - 1) // 3 + 1).astype(str)
        df["faixa"] = pd.cut(df["idade"], bins=BINS_IDADE, labels=LABELS_IDADE, right=False)
        for col in ["Hipertenso", "Diabetes Mellitus", "Tabagista", "Etilista", "Marcapasso"]:
            df[col] = df[col].fillna(0).astype(int)

        df["Distrito"] = df.apply(lambda r: buscar_distrito(r["Data_cadastro"], r["Cidade"]), axis=1)
        _dist_map = {}
        for _, _, mun, dist, _ in LOCAIS:
            dn = _norm(dist)
            if dn not in _dist_map:
                _dist_map[dn] = dist.strip()
            mn = _norm(mun)
            if mn not in _dist_map:
                _dist_map[mn] = dist.strip()
        def _norm_dist(s):
            if not s or s.strip() == "":
                return ""
            sn = _norm(s)
            if sn in _dist_map:
                return _dist_map[sn]
            return s.strip()
        df["Distrito"] = df["Distrito"].apply(_norm_dist)
        df["Municipio_Coleta"] = df.apply(lambda r: buscar_municipio_coleta(r["Data_cadastro"], r["Cidade"]), axis=1)
        _mun_canon = {}
        for _, _, m, _, _ in LOCAIS:
            mt = m.strip().title()
            _mun_canon[_norm(m)] = mt
        df["Municipio_Coleta"] = df["Municipio_Coleta"].apply(
            lambda s: _mun_canon.get(_norm(s), s.strip().title()) if s else s
        )

        return df
