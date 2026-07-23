def gerar_csv(tabela):
    return tabela.to_csv(index=False).encode("utf-8")