"""Auditoria independente, somente leitura; imprime apenas agregados."""
import csv, io, zipfile, pathlib, re, unicodedata, collections as C, json, hashlib
from decimal import Decimal, InvalidOperation
from datetime import datetime
csv.field_size_limit(10**9)
def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKD',str(s or '').strip().casefold().lstrip('\ufeff')) if not unicodedata.combining(c))
def ident(s):
    s=str(s or '').strip().lstrip('\ufeff')
    if re.fullmatch(r'\d+[.,]0+',s): s=re.split('[.,]',s)[0]
    return (s.lstrip('0') or '0') if s.isdigit() else s.upper()
def day(s):
    s=str(s or '').strip()
    for fmt,n in [('%d/%m/%Y',10),('%Y-%m-%d',10)]:
        try:return datetime.strptime(s[:n],fmt).date().isoformat()
        except ValueError:pass
    return ''
def qty(s):
    s=str(s or '').strip().replace(' ','')
    if not s:return None
    if ',' in s:s=s.replace('.','').replace(',','.')
    try:
        q=Decimal(s)
        return q if q.is_finite() else None
    except InvalidOperation:return None
def rows(b):
    sample=b.read(20000); b.seek(0)
    enc='utf-16' if sample.startswith((b'\xff\xfe',b'\xfe\xff')) else 'utf-8-sig'
    try:sample.decode(enc,errors='strict')
    except UnicodeError:enc='cp1252'
    f=io.TextIOWrapper(b,encoding=enc,errors='replace',newline='')
    def lines():
        for line in f:
            if '\x00' in line:line=line.replace('\x00','')
            if line.strip():yield line
    it=csv.reader(lines(),delimiter=';')
    heads=[norm(x) for x in next(it)]
    for r in it:
        if len(r)!=len(heads):continue
        yield dict(zip(heads,r))
def get(r,s):return r.get(norm(s),'')
def code(r,s):return ident(get(r,s))
def source(path):
    if path.suffix.lower()=='.zip':
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if name.lower().endswith('.csv'):
                    with z.open(name) as b:yield from rows(b)
    else:
        with path.open('rb') as b:yield from rows(b)
history_path=next(pathlib.Path('.').glob('*ExportReportOrderHistory.csv'))
H=[]; seen=set();hstats=C.Counter()
for r in source(history_path):
    q=qty(get(r,'Qtd. Pedida')); p=code(r,'Nº Pedido ERP'); e=code(r,'EAN'); cp=code(r,'Código Produto Cliente'); c=code(r,'CNPJ Cliente'); d=day(get(r,'Data de Criação')); item=code(r,'Número do Item')
    sig=tuple(r.items())
    if sig in seen:hstats['linhas_identicas']+=1;continue
    seen.add(sig)
    H.append((p,e,cp,c,d,item,q,norm(get(r,'Origem'))))
    hstats['linhas']+=1
    if q is not None:hstats['entrada_cx']+=q
hids={h[0] for h in H if h[0]}
def audit(path):
    index=C.defaultdict(list); orders=set(); stats=C.Counter(); units=C.Counter(); datecols=C.Counter(); headers=[]
    for r in source(path):
        if not headers:headers=list(r)
        stats['linhas']+=1
        p=code(r,'Nº Pedido ERP')
        if not p:continue
        orders.add(p)
        if p not in hids:continue
        if 'teste' in norm(get(r,'Nome Cliente SAP')) or 'teste' in norm(get(r,'Nome Rede')):stats['teste_excluido']+=1;continue
        e=code(r,'EAN');cp=code(r,'Código Produto Cliente');c=code(r,'CNPJ Cliente');eg=code(r,'SKU EG');client=code(r,'Cliente EG')
        ecc=day(get(r,'Data Captação ECC'));created=day(get(r,'Data de Criação'))
        unit=norm(get(r,'Unidade'));units[unit]+=1
        datecols['ecc_preenchida']+=bool(ecc);datecols['criacao_preenchida']+=bool(created)
        mov=tuple(qty(get(r,f)) for f in ['Qtd. Atualizada','Qtd. Carro com remessa','Qtd. Carro sem remessa','Qtd. Faturada'])
        index[p].append((e,cp,c,eg,client,ecc,created,unit,mov))
    res={'arquivo':path.name,'headers':headers,'linhas':stats['linhas'],'pedidos_distintos':len(orders),'pedidos_history_presentes':len(orders&hids),'pedidos_history_total':len(hids),'unidades_nos_pedidos_vinculaveis':dict(units),'datas':dict(datecols),'por_origem':{}}
    stages=C.defaultdict(C.Counter); grouped=C.defaultdict(list); used=C.Counter()
    for i,(p,e,cp,c,d,item,q,orig) in enumerate(H):
        s=stages[orig];s['history_linhas']+=1;s['history_cx']+=q or 0
        cand=index.get(p,[])
        if p in orders:s['pedido_linhas']+=1;s['pedido_cx']+=q or 0
        if e:match=[x for x in cand if x[0]==e]
        else:match=[x for x in cand if cp and c and x[2]==c and (x[1]==cp or (not x[1] and x[3]==cp))]
        if not match:continue
        s['produto_linhas']+=1;s['produto_cx']+=q or 0
        if any(x[5]==d and d for x in match):s['data_ecc_linhas']+=1
        if any(x[6]==d and d for x in match):s['data_criacao_linhas']+=1
        if any(x[2]==c for x in match):s['cnpj_coincide_linhas']+=1
        exact=[x for x in match if d and (x[5] or x[6])==d]
        if not exact:continue
        s['data_regra_linhas']+=1;s['data_regra_cx']+=q or 0
        keys={(x[4],x[3]) for x in exact if x[4] and x[3]}
        if len(keys)!=1 or any(not x[3] or not x[4] for x in exact):s['eg_ambiguo_ou_ausente']+=1;continue
        k=(p,*next(iter(keys)),d)
        grouped[k].append((orig,q,exact));s['eg_linhas']+=1
    for k,hh in grouped.items():
        # Um movimento só é contabilizado uma vez. Vários History na mesma chave exigem auditoria.
        if len(hh)!=1:
            for orig,q,exact in hh:stages[orig]['chave_history_ambigua']+=1
            continue
        orig,q,exact=hh[0];s=stages[orig]
        if q is None or q<=0 or any(x[7]!='cx' or any(v is None for v in x[8]) for x in exact):s['unidade_ou_movimento_pendente']+=1;continue
        a,m,sm,f=[sum(x[8][i] for x in exact) for i in range(4)]
        pend=a-m-sm-f
        s['chaves_calculaveis']+=1;s['entrada_vinculada_cx']+=q;s['faturado_cx']+=f;s['marcado_cx']+=m;s['pendente_cx']+=pend
        if abs(pend-(q-f-m))>Decimal('0.01'):s['divergencia_pendente']+=1
    for orig,s in stages.items():
        a=s['entrada_vinculada_cx']
        s=dict(s);s['fill_rate_pct']=100*s['faturado_cx']/a if a else None;s['entregue_marcado_pct']=100*(s['faturado_cx']+s['marcado_cx'])/a if a else None
        res['por_origem'][orig]=s
    return res
out={'history':dict(hstats),'pedidos_history':len(hids),'fontes':{},'auditoria':[]}
for p in [history_path,pathlib.Path('Order.zip'),pathlib.Path('BASE_ESTOQUE 16.11.xlsx'),*pathlib.Path('.').glob('*ExportReportLoadItem.zip')]:
    if p.exists():out['fontes'][p.name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
for p in [pathlib.Path('Order.zip'),*pathlib.Path('.').glob('*ExportReportLoadItem.zip')]:
    if p.exists():out['auditoria'].append(audit(p))
with zipfile.ZipFile('BASE_ESTOQUE 16.11.xlsx') as z:
    import xml.etree.ElementTree as ET
    root=ET.fromstring(z.read('xl/workbook.xml'))
    out['abas_estoque']=[x.attrib['name'] for x in root.iter() if x.tag.endswith('}sheet')]
out['limites']='Movimentos em CX apenas. Sem rateio de ambiguidades. Estoque inventariado; qualificação será comparada com auditoria legada separada. Nenhum identificador comercial publicado.'
dest=pathlib.Path('auditoria-v45');dest.mkdir(exist_ok=True)
s=json.dumps(out,ensure_ascii=False,indent=2,default=lambda v:float(v) if isinstance(v,Decimal) else str(v))
(dest/'history_order.json').write_text(s,encoding='utf-8')
print(s)
