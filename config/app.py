"""
Constantes do app.
"""

MESES_PT = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
}

COMORB_COLS = {
    "Hipertenso": "HAS",
    "Diabetes Mellitus": "DM",
    "Tabagista": "Tabagismo",
    "Etilista": "Etilismo",
}

BINS_IDADE = [0, 18, 30, 40, 50, 60, 70, 80, 200]
LABELS_IDADE = ["<18", "18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]