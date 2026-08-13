import pandas as pd
import re

MESES = {
    'jan':1,'fev':2,'mar':3,'abr':4,'mai':5,'jun':6,
    'jul':7,'ago':8,'set':9,'out':10,'nov':11,'dez':12,
    'janeiro':1,'fevereiro':2,'marco':3,'abril':4,'maio':5,'junho':6,
    'julho':7,'agosto':8,'setembro':9,'outubro':10,'novembro':11,'dezembro':12
}

df = pd.read_excel('Locais.xlsx', header=None)

linhas = []
for i, row in df.iterrows():
    if i < 2:
        continue
    ano = row[0]
    data_str = str(row[1]).strip() if pd.notna(row[1]) else ''
    distrito = str(row[2]).strip() if pd.notna(row[2]) else ''
    municipio = str(row[5]).strip() if pd.notna(row[5]) else ''
    ecg = row[6] if pd.notna(row[6]) else 0
    if 'SUBTOTAL' in data_str.upper() or 'TOTAL' in str(ano).upper() or '---' in str(ano):
        continue
    if not municipio or municipio == 'nan':
        continue
    try:
        ano = int(ano)
    except:
        continue
    linhas.append({'ano':ano,'data_str':data_str,'distrito':distrito,'municipio':municipio,'ecg':ecg})

def parse_periodo(data_str, ano):
    data_str = data_str.strip().lower()
    m = re.match(r'(\w+)-(\w+)\s+\d{4}', data_str)
    if m:
        mes_ini = MESES.get(m.group(1)[:3])
        mes_fim = MESES.get(m.group(2)[:3])
        if mes_ini and mes_fim:
            ini = pd.Timestamp(year=ano, month=mes_ini, day=1)
            fim = pd.Timestamp(year=ano, month=mes_fim, day=pd.Timestamp(year=ano,month=mes_fim,day=1).days_in_month)
            return ini, fim
    m = re.match(r'(\d{1,2})(?:-(\d{1,2}))?\s+(\w+)', data_str)
    if m:
        dia_ini = int(m.group(1))
        dia_fim = int(m.group(2)) if m.group(2) else dia_ini
        mes_str = m.group(3).lower()
        mes = MESES.get(mes_str)
        if not mes:
            for k,v in MESES.items():
                if k.startswith(mes_str[:3]): mes=v; break
        if mes:
            try:
                return pd.Timestamp(year=ano,month=mes,day=dia_ini), pd.Timestamp(year=ano,month=mes,day=dia_fim)
            except: pass
    for k,v in sorted(MESES.items(), key=lambda x:-len(x[0])):
        if k in data_str:
            ini = pd.Timestamp(year=ano,month=v,day=1)
            return ini, pd.Timestamp(year=ano,month=v,day=ini.days_in_month)
    if re.match(r'^\d{4}$', data_str):
        return pd.Timestamp(year=ano,month=1,day=1), pd.Timestamp(year=ano,month=12,day=31)
    return None, None

registros = []
for l in linhas:
    ini, fim = parse_periodo(l['data_str'], l['ano'])
    if ini and fim:
        registros.append({'data_inicio':ini,'data_fim':fim,'municipio':l['municipio'].title().strip(),'distrito':l['distrito'],'ecg':l['ecg'],'ano':l['ano']})
        print(f"  {l['data_str']:20s} -> {ini.date()} a {fim.date()} | {l['municipio']:30s} | {l['distrito']:25s} | ECG: {l['ecg']}")

with open('constants_locais.py', 'w', encoding='utf-8') as f:
    f.write('import pandas as pd\nimport unicodedata\nimport random\n\n')

    f.write('''
def _norm(s):
    s = str(s).strip().lower()
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return " ".join(s.split())
''')

    f.write('\nLOCAIS = [\n')
    for r in registros:
        m = r['municipio'].replace('"','\\"')
        d = r['distrito'].replace('"','\\"')
        e = int(r['ecg']) if r['ecg'] else 0
        f.write(f'    ("{r["data_inicio"].strftime("%Y-%m-%d")}", "{r["data_fim"].strftime("%Y-%m-%d")}", "{m}", "{d}", {e}),\n')
    f.write(']\n\n')

    f.write('''
def buscar_distrito(data_cadastro, cidade):
    """Busca distrito cruzando data + municipio."""
    if not data_cadastro or not cidade:
        return ""
    cn = _norm(cidade)

    # Cidades visitadas pela equipe
    cidades_visitadas = set()
    for _, _, mun, _, _ in LOCAIS:
        cidades_visitadas.add(_norm(mun))

    # 1. Match exato: data + municipio
    candidatos = []
    for ini_str, fim_str, mun, dist, ecg in LOCAIS:
        if _norm(mun) != cn:
            continue
        ini = pd.Timestamp(ini_str)
        fim = pd.Timestamp(fim_str)
        if ini <= data_cadastro < fim + pd.Timedelta(days=1):
            candidatos.append((dist, max(int(ecg) if ecg else 0, 1)))

    if len(candidatos) == 1:
        return candidatos[0][0]
    elif len(candidatos) > 1:
        total = sum(e for _, e in candidatos)
        r = random.Random(int(data_cadastro.timestamp())).random() * total
        acum = 0
        for dist, ecg in candidatos:
            acum += ecg
            if r <= acum:
                return dist
        return candidatos[-1][0]

    # 2. Paciente de cidade visitada mas fora do periodo = posto fixo
    if cn in cidades_visitadas:
        return cidade.strip().title()

    # 3. Paciente de cidade NUNCA visitada = fez exame em campo
    candidatos_data = []
    for ini_str, fim_str, mun, dist, ecg in LOCAIS:
        ini = pd.Timestamp(ini_str)
        fim = pd.Timestamp(fim_str)
        if ini <= data_cadastro <= fim:
            candidatos_data.append((dist, max(int(ecg) if ecg else 0, 1), mun))

    if candidatos_data:
        if len(candidatos_data) == 1:
            return candidatos_data[0][0]
        total = sum(e for _, e, _ in candidatos_data)
        r = random.Random(int(data_cadastro.timestamp()) + 777).random() * total
        acum = 0
        for dist, ecg, _ in candidatos_data:
            acum += ecg
            if r <= acum:
                return dist
        return candidatos_data[-1][0]

    return ""
''')

print(f"\nGerado: constants_locais.py | Total: {len(registros)} periodos")