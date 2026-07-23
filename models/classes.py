"""
Entidades do dominio.
"""


class Paciente:
    def __init__(self, cidade, sexo, idade, hipertenso=False,
                 diabetico=False, tabagista=False, etilista=False):
        self.cidade = cidade
        self.sexo = sexo
        self.idade = idade
        self.hipertenso = hipertenso
        self.diabetico = diabetico
        self.tabagista = tabagista
        self.etilista = etilista
        self.exames = []
        self.laudos = []

    @property
    def faixa_etaria(self):
        bins = [(18, "<18"), (30, "18-29"), (40, "30-39"), (50, "40-49"),
                (60, "50-59"), (70, "60-69"), (80, "70-79")]
        for limite, rotulo in bins:
            if self.idade < limite:
                return rotulo
        return "80+"

    @property
    def total_comorbidades(self):
        return sum([self.hipertenso, self.diabetico, self.tabagista, self.etilista])


class ExameECG:
    def __init__(self, data, cidade, achados=None, ritmo_sinusal=True):
        self.data = data
        self.cidade = cidade
        self.achados = achados or []
        self.ritmo_sinusal = ritmo_sinusal
        self.paciente = None

    @property
    def tem_alteracao(self):
        return len(self.achados) > 0


class Laudo:
    CATEGORIAS = ["Normal", "Arritmia", "Bloqueio de Ramo",
                  "Alteracao de Repolarizacao", "Sobrecarga Ventricular",
                  "Outras Alteracoes"]

    def __init__(self, data, diagnostico, hipotese="", indicacao="", observacoes=""):
        self.data = data
        self.diagnostico = diagnostico
        self.hipotese = hipotese
        self.indicacao = indicacao
        self.observacoes = observacoes
        self.exame = None
        self.paciente = None

    @property
    def eh_normal(self):
        return self.diagnostico == "Normal"


class AchadoECG:
    def __init__(self, nome, categoria, colunas_origem):
        self.nome = nome
        self.categoria = categoria
        self.colunas_origem = colunas_origem


class Municipio:
    def __init__(self, nome, lat=None, lon=None):
        self.nome = nome
        self.lat = lat
        self.lon = lon
        self.total_exames = 0
        self.total_alterados = 0

    @property
    def pct_alterados(self):
        if self.total_exames == 0:
            return 0.0
        return round(100 * self.total_alterados / self.total_exames, 1)