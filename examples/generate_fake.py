"""
Gera dados sinteticos para testes.
Uso: python examples/generate_fake.py
"""

import pandas as pd
import numpy as np
from pathlib import Path


def gerar_dados_sinteticos(n=500, seed=42):
    np.random.seed(seed)
    municipios = ["Teofilo Otoni", "Diamantina", "Capelinha", "Almenara",
                  "Aracuai", "Itambacuri", "Minas Novas", "Turmalina",
                  "Pedra Azul", "Grao Mogol", "Itamarandiba", "Salinas",
                  "Montes Claros", "Porteirinha", "Janauba", "Serro",
                  "Curvelo", "Bocaiuva", "Novo Cruzeiro", "Gouveia"]
    hoje = pd.Timestamp("2025-06-01")
    nascimentos = [hoje - pd.Timedelta(days=int(d)) for d in np.random.randint(18*365, 90*365, n)]
    cadastros = pd.date_range("2022-01-01", "2025-05-31", periods=n)
    pesos = np.random.dirichlet(np.ones(len(municipios)) * 2)
    pesos[0] *= 3
    pesos = pesos / pesos.sum()

    df = pd.DataFrame({
        "Data_Nascimento": nascimentos, "Data_cadastro": cadastros,
        "Cidade": np.random.choice(municipios, n, p=pesos),
        "Sexo": np.random.choice(["Feminino", "Masculino"], n, p=[0.58, 0.42]),
        "Hipertenso": np.random.choice([0, 1], n, p=[0.45, 0.55]),
        "Diabetes Mellitus": np.random.choice([0, 1], n, p=[0.65, 0.35]),
        "Tabagista": np.random.choice([0, 1], n, p=[0.75, 0.25]),
        "Etilista": np.random.choice([0, 1], n, p=[0.85, 0.15]),
    })

    achados_prob = {
        "Tracado dentro dos limites de normalidade": 0.35, "Ritmo sinusal": 0.85,
        "Taquicardia sinusal": 0.08, "Bradicardia sinusal": 0.04,
        "Arritmia sinusal": 0.03, "Fibrilacao atrial": 0.03,
        "Extrassystole atrial": 0.05, "Extrassystole ventricular": 0.04,
        "Bloqueio incompleto de ramo direito": 0.06, "Bloqueio completo de ramo direito": 0.03,
        "Bloqueio atrioventricular do 1 grau": 0.04,
        "Alteracoes inespecificas da repolarizacao ventricular": 0.10,
        "Padrao de repolarizacao precoce": 0.04,
        "Provavel sobrecarga ventricular direita": 0.03,
        "Provavel sobrecarga ventricular esquerda": 0.04,
        "Fibrose septal": 0.02, "PR curto": 0.02, "Wolff-Parkinson-White": 0.005,
        "Baixa voltagem do QRS no plano frontal": 0.02,
    }
    for col, prob in achados_prob.items():
        df[col] = np.random.choice([0, 1], n, p=[1 - prob, prob])
    mask_normal = df["Tracado dentro dos limites de normalidade"] == 1
    for col in achados_prob:
        if col not in ("Ritmo sinusal", "Tracado dentro dos limites de normalidade"):
            df.loc[mask_normal, col] = 0

    hipoteses = ["Avaliacao de rotina", "Dor toracica", "Dispneia", "Palpitacoes",
                 "Hipertensao arterial", "Diabetes mellitus", "Pre-operatorio"]
    indicacoes = ["Avaliacao cardiologica", "Check-up", "Pre-operatorio", "Triagem comunitaria"]
    df["Hipotese Diagnostica"] = np.random.choice(hipoteses, n)
    df["Indicacao Clinica"] = np.random.choice(indicacoes, n)
    df["Observacoes"] = ""
    return df


if __name__ == "__main__":
    df = gerar_dados_sinteticos(500)
    saida = Path(__file__).parent / "fake_ecg.xlsx"
    df.to_excel(saida, index=False)
    print(f"Gerado: {saida} ({len(df)} linhas, {len(df.columns)} colunas)")