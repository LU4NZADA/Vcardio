import pandas as pd
from io import BytesIO
from components import fmt


def gerar_excel(tabela, ind):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        tabela.to_excel(w, index=False, sheet_name="Dados")
        resumo = pd.DataFrame({
            "Indicador": ["Total exames", "Municipios", "Idade media", "Arritmias",
                          "Bloqueios", "Laudos alterados (%)"],
            "Valor": [fmt(ind["n"]), ind["n_muns"], ind["avg_age"],
                      ind["n_arr"], ind["n_blk"], f"{ind['alt_pct']}%"],
        })
        resumo.to_excel(w, index=False, sheet_name="Resumo")
    return buf.getvalue()