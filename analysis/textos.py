"""
Geracao automatica de textos narrativos.
"""


def gerar_resumo_textual(df, ind):
    n = ind["n"]
    textos = {}

    textos["resumo"] = (
        f"Foram analisados {n:,} exames eletrocardiograficos provenientes de "
        f"{ind['n_muns']} municipios do Vale do Jequitinhonha. "
        f"A idade media dos pacientes foi de {ind['avg_age']} anos. "
        f"{ind['alt_pct']}% dos laudos apresentaram pelo menos uma alteracao."
    ).replace(",", ".")

    n_arr = ind["n_arr"]
    if n_arr > 0:
        pct_arr = round(100 * n_arr / n, 1)
        df_arr = ind["achados"].get("Arritmias")
        mais_comum = ""
        if df_arr is not None and not df_arr.empty:
            top = df_arr.iloc[0]
            mais_comum = f" A arritmia mais frequente foi {top['Achado']} ({top['Casos']} casos)."
        textos["arritmias"] = f"Foram identificadas {n_arr} arritmias ({pct_arr}%).{mais_comum}"
    else:
        textos["arritmias"] = "Nenhuma arritmia foi identificada."

    n_blk = ind["n_blk"]
    if n_blk > 0:
        textos["bloqueios"] = f"Registrou-se {n_blk} bloqueios ({round(100*n_blk/n,1)}%)."
    else:
        textos["bloqueios"] = "Nenhum bloqueio foi identificado."

    comorb_frases = []
    for _, label, total, pct in ind["comorb_resumo"]:
        comorb_frases.append(f"{label}: {total} ({pct}%)")
    if comorb_frases:
        textos["comorbidades"] = "Comorbidades: " + "; ".join(comorb_frases) + "."

    risco = ind["risco_municipio"]
    risco_alto = risco[(risco["total"] >= 5) & (risco["pct"] > 70)]
    if len(risco_alto) > 0:
        mun_risco = ", ".join(risco_alto["Cidade"].head(5).tolist())
        textos["risco"] = f"Municipios com risco critico (>70%): {mun_risco}."
    else:
        textos["risco"] = "Nenhum municipio com risco superior a 70%."

    textos["conclusao"] = (
        "Os dados reforcam a importancia da vigilancia cardiovascular ativa "
        "no Vale do Jequitinhonha."
    )
    return textos


def gerar_paragrafo_completo(df, ind):
    textos = gerar_resumo_textual(df, ind)
    return "\n\n".join(v for v in textos.values() if v)