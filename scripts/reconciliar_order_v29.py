#!/usr/bin/env python3
"""Auditoria reproduzível da Order 16.11 contra BASE_ESTOQUE 16.11.
Somente biblioteca padrão; não altera as bases. Relatórios detalhados ficam como artifacts."""
import collections as C
import csv
import datetime as DT
import io
import json
import math
import pathlib
import posixpath
import re
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

SRC_ORDER="Order.zip"
SRC_STOCK="BASE_ESTOQUE 16.11.xlsx"
OUT=pathlib.Path("auditoria-order")
OUT.mkdir(exist_ok=True)
csv.field_size_limit(10**9)
NS="{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL="{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG="{http://schemas.openxmlformats.org/package/2006/relationships}"
def norm(v):
    return "".join(ch for ch in unicodedata.normalize("NFD",str(v or "").strip().casefold()) if unicodedata.category(ch)!="Mn").strip()
def idkey(v):
    s=str(v or "").strip()
    if s.endswith(".0") and s[:-2].isdigit():s=s[:-2]
    return s
def num(v):
    s=str(v or "").strip().replace("\u00a0","")
    if not s:return None
    s=re.sub(r"[^0-9,.\-]","",s)
    if "," in s and "." in s:s=s.replace(".","").replace(",",".") if s.rfind(",")>s.rfind(".") else s.replace(",","")
    elif "," in s:s=s.replace(",",".")
    try:
        v=float(s)
        return v if math.isfinite(v) else None
    except:return None
def date(v):
    s=str(v or "").strip()
    if not s:return ""
    for fmt in ("%d/%m/%Y %H:%M:%S","%d/%m/%Y %H:%M","%d/%m/%Y","%Y-%m-%d %H:%M:%S","%Y-%m-%d","%Y-%m-%dT%H:%M:%S"):
        try:return DT.datetime.strptime(s[:19],fmt).strftime("%Y-%m-%d")
        except:pass
    if re.match(r"^\d{4}-\d{2}-\d{2}",s):return s[:10]
    return ""
def col(i):
    n=0
    for ch in re.match(r"[A-Z]+",i).group(0):n=n*26+ord(ch)-64
    return n-1
def xlsx(z,sheet):
    strings=[]
    if "xl/sharedStrings.xml" in z.namelist():
        with z.open("xl/sharedStrings.xml") as stream:
            for _,el in ET.iterparse(stream,events=("end",)):
                if el.tag==NS+"si":
                    strings.append("".join(t.text or "" for t in el.iter(NS+"t")));el.clear()
    wb=ET.fromstring(z.read("xl/workbook.xml"))
    links={r.get("Id"):r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).findall(PKG+"Relationship")}
    matches=[a for a in wb.findall(".//"+NS+"sheet") if a.get("name")==sheet]
    if not matches:return
    loc=links[matches[0].get(REL+"id")]
    loc=loc.lstrip("/") if loc.startswith("/") else posixpath.normpath("xl/"+loc)
    headers=None
    with z.open(loc) as f:
        for _,el in ET.iterparse(f,events=("end",)):
            if el.tag!=NS+"row":continue
            r={}
            for c in el.findall(NS+"c"):
                v=c.find(NS+"v")
                if c.get("t")=="inlineStr":val="".join(t.text or "" for t in c.iter(NS+"t"))
                elif v is None:val=""
                elif c.get("t")=="s":
                    try:val=strings[int(v.text)]
                    except:val=""
                else:val=v.text or ""
                r[col(c.get("r"))]=val
            if headers is None:headers=r
            else:yield {str(headers.get(i,"")):v for i,v in r.items() if i in headers}
            el.clear()
def grade_area(text):
    s=norm(text)
    for term in ["louveira","diadema","guarulhos","suzano","taubate","sao jose","s j campos"]:
        if term in s:return "sao jose" if term=="s j campos" else term
    return ""
def csvout(file,header,rows):
    with (OUT/file).open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f,delimiter=";")
        w.writerow(header)
        for row in rows:
            w.writerow([("'"+v) if isinstance(v,str) and v.startswith(("=","+","-","@")) else v for v in row])

print("INICIANDO_CONFERENCIA_FONTES")
cad={}
cad_sap=C.defaultdict(set)
factor_conflicts=C.Counter()
malha=C.defaultdict(set)
factory={}
factorymap={}
grades=C.defaultdict(dict)
dpar={}
with zipfile.ZipFile(SRC_STOCK) as z:
    for r in xlsx(z,"CAD"):
        eg=idkey(r.get("Cód_Prod"));sap=idkey(r.get("Cod S4"));ratio=num(r.get("Quantidade_prod_pallet"))
        if not eg:continue
        item=cad.setdefault(eg,{"sap":sap,"ratios":set()})
        if ratio is not None and ratio>0:item["ratios"].add(ratio)
        if sap:cad_sap[sap].add(eg)
    for eg,item in cad.items():
        if len(item["ratios"])>1:factor_conflicts[eg]+=1
    for r in xlsx(z,"Malha"):
        comercial=idkey(r.get("Destino Comercial"));sap=idkey(r.get("SKU SAP"));orig=idkey(r.get("Fábrica Origem SAP")).upper()
        if comercial and sap and orig:malha[(comercial,sap)].add(orig)
    for r in xlsx(z,"Estoque Fabricas"):
        br=idkey(r.get("Orig. S4")).upper();eg=idkey(r.get("Sku PCA"));pca=idkey(r.get("Orig. PCA"))
        if not br or not eg:continue
        d1=num(r.get("D1"))
        factory[(br,eg)]=d1
        if pca:factorymap.setdefault(br,pca)
    for name in ("Estoque CDD Louveira","Estoque CDD Diadema","Estoque CDD Guarulhos",
                 "Estoque CDD Suzano","Estoque CDD Taubate","Estoque CDD São José"):
        cdd=grade_area(name)
        for r in xlsx(z,name):
            sku=idkey(r.get("CodigoProduto"));vol=num(r.get("SaldoDisponivel"))
            if sku:grades[cdd][sku]=vol
    for r in xlsx(z,"DeParaCDD"):
        cli=idkey(r.get("ClientEG"));cdd=grade_area(r.get("CDD Footptint"))
        if cli and cdd:dpar.setdefault(cli,set()).add(cdd)
print("FONTES_INDEXADAS",json.dumps({"CAD_eg":len(cad),"malha_key_comercial_sap":len(malha),"factory_sku_origin":len(factory),"dpar_clientes":len(dpar)},ensure_ascii=False))

groups={}
metrics=C.Counter()
rowstatuses=C.Counter()
unitbytype=C.Counter()
with zipfile.ZipFile(SRC_ORDER) as z:
    name=next(x for x in z.namelist() if x.lower().endswith(".csv"))
    with z.open(name) as b:
        reader=csv.DictReader(io.TextIOWrapper(b,encoding="utf-8-sig",errors="replace",newline=""),delimiter=";")
        headers=set(reader.fieldnames or [])
        essential={"Nº Pedido ERP","Cliente EG","SKU EG","Qtd. Original","Qtd. Atualizada",
                   "Qtd. Carro com remessa","Qtd. Carro sem remessa","Qtd. Faturada","Tipo Pedido","Unidade"}
        if not essential<=headers:raise RuntimeError("Cabeçalhos necessários ausentes: "+repr(sorted(essential-headers)))
        for i,r in enumerate(reader,1):
            metrics["rows"]+=1
            typ=idkey(r.get("Tipo Pedido")).upper()
            status=idkey(r.get("Status"))
            unit=idkey(r.get("Unidade")).upper()
            rowstatuses[status]+=1
            unitbytype[(typ,unit)]+=1
            k=tuple(idkey(r.get(n)) for n in ("Nº Pedido ERP","Cliente EG","SKU EG"))
            if not all(k):metrics["invalid_key_rows"]+=1;continue
            g=groups.get(k)
            if g is None:
                g=groups[k]={"k":k,"network":idkey(r.get("Nome Rede")),"client":idkey(r.get("Nome Cliente SAP")),
                            "commercial":idkey(r.get("Cód. Comercial")),"order_sap":idkey(r.get("SKU SAP")),
                            "type":C.Counter(),"status":C.Counter(),"units":C.Counter(),"count":0,
                            "original":None,"original_hl":None,"original_plt":None,"first_key":None,
                            "orig_variants":set(),"updated":0.0,"carWith":0.0,"carWithout":0.0,
                            "billed":0.0,"confirmed":0.0,"noCar":0.0,"raw_negative":0,
                            "overlaps":0,"mov_incomplete":0,"notCX":0,
                            "mixed_commercial":False,"mixed_network":False,
                            "status_cancel_rows":0,"type_status":C.Counter(),"active_types":set(),"type_movement_pending":C.Counter(),"validity":"","first_creation":""}
            g["count"]+=1;g["type"][typ]+=1;g["status"][status]+=1;g["units"][unit]+=1
            g["type_status"][(typ,status)]+=1
            if norm(status) not in ('cancelada','aguardando cancelamento') and typ:g["active_types"].add(typ)
            if norm(status)=="cancelada":g["status_cancel_rows"]+=1
            if g["commercial"]!=idkey(r.get("Cód. Comercial")):g["mixed_commercial"]=True
            if g["network"]!=idkey(r.get("Nome Rede")):g["mixed_network"]=True
            original=num(r.get("Qtd. Original"));hl=num(r.get("Volume HL"));plt=num(r.get("Volume Palete"))
            g["orig_variants"].add((original,hl,plt))
            creation=date(r.get("Data de Criação"));expiry=date(r.get("Data de Vencimento"))
            creation_sort=creation if creation else "9999-99-99"
            validity_sort=date(r.get("Data de Vencimento Original")) or expiry or "9999-99-99"
            rank=(creation_sort,validity_sort,i)
            if g["first_key"] is None or rank<g["first_key"]:
                g["first_key"]=rank;g["original"]=original;g["original_hl"]=hl;g["original_plt"]=plt
                g["validity"]=expiry;g["first_creation"]=creation
            if unit!="CX":g["notCX"]+=1;continue
            values={n:num(r.get(n)) for n in ("Qtd. Atualizada","Qtd. Carro com remessa","Qtd. Carro sem remessa","Qtd. Faturada","Qtd. Confirmada","Qtd. Sem carro")}
            if any(values[n] is None for n in ("Qtd. Atualizada","Qtd. Carro com remessa","Qtd. Carro sem remessa","Qtd. Faturada")):
                g["mov_incomplete"]+=1;continue
            g["updated"]+=values["Qtd. Atualizada"]
            g["carWith"]+=values["Qtd. Carro com remessa"]
            g["carWithout"]+=values["Qtd. Carro sem remessa"]
            g["billed"]+=values["Qtd. Faturada"]
            g["type_movement_pending"][typ]+=values["Qtd. Atualizada"]-values["Qtd. Carro com remessa"]-values["Qtd. Carro sem remessa"]-values["Qtd. Faturada"]
            g["confirmed"]+=values["Qtd. Confirmada"] or 0
            g["noCar"]+=values["Qtd. Sem carro"] or 0
            if values["Qtd. Carro com remessa"]+values["Qtd. Faturada"]>values["Qtd. Atualizada"]+1e-8:g["overlaps"]+=1
            if values["Qtd. Atualizada"]-values["Qtd. Carro com remessa"]-values["Qtd. Carro sem remessa"]-values["Qtd. Faturada"]<-1e-8:g["raw_negative"]+=1

summary={"sources":{"order_zip":SRC_ORDER,"order_csv":name,"estoque":SRC_STOCK},
         "counts":{"rows":metrics["rows"],"invalid_key_rows":metrics["invalid_key_rows"],"unique_keys":len(groups),
                   "repeated_keys":sum(g["count"]>1 for g in groups.values()),
                   "repeated_key_excess_rows":sum(g["count"]-1 for g in groups.values())},
         "status_rows":dict(rowstatuses),"type_unit_rows":{"/".join(k):v for k,v in unitbytype.items()},
         "cad":{"unique_eg":len(cad),"conflicting_ratio_skus":len(factor_conflicts)},
         "comparisons":{},"by_type":{}}
counter=C.Counter();stats=C.defaultdict(C.Counter);formation=C.defaultdict(lambda:{"pending":0.0,"qualified":0.0,"skus":0,"unknown":0,"alt":0})
originSku=C.defaultdict(float);altsets=C.defaultdict(set);originStock={}
cdSku=C.defaultdict(float)
rows=[];exceptions=[];mixed_rows=[];weekly=(DT.date(2026,11,16),DT.date(2026,11,22))
for k,g in groups.items():
    typvals={t for t in g["type"] if t}
    typ=next(iter(typvals)) if len(typvals)==1 else ("MISTO" if typvals else "")
    unitset={t for t in g["units"] if t}
    complete=(g["notCX"]==0 and g["mov_incomplete"]==0)
    pending=round(g["updated"]-g["carWith"]-g["carWithout"]-g["billed"],8) if complete else None
    original=g["original"]
    filled=100*g["billed"]/original if complete and original is not None and original>0 else None
    eg=k[2];c=cad.get(eg)
    sap=c["sap"] if c else ""
    ratios=c["ratios"] if c else set()
    ratio=next(iter(ratios)) if len(ratios)==1 else None
    market=(g["commercial"],sap)
    origins=malha.get(market,set()) if sap else set()
    fallback=(g["commercial"].lstrip("0"),sap)
    if not origins and fallback!=market:origins=malha.get(fallback,set())
    stock_found=sum((b,eg) in factory for b in origins)
    positives=sum((factory.get((b,eg)) or 0)>0 for b in origins)
    cdd=dpar.get(k[1],set())
    cdd_name=next(iter(cdd)) if len(cdd)==1 else ""
    grade=grades.get(cdd_name,{}).get(eg[:-1]) if cdd_name and len(eg)>1 else None
    week=False
    if g["validity"]:
        try:
            v=DT.date.fromisoformat(g["validity"])
            week=weekly[0]<=v<=weekly[1]
        except:pass
    reason=[]
    if not complete:reason.append("MOVIMENTO_NAO_CONVERSIVEL_OU_INCOMPLETO")
    if len(typvals)!=1:reason.append("TIPO_PEDIDO_AMBIGUO")
    if not sap:reason.append("SEM_CAD_EG_SAP")
    if typ=="ASVD" and not (ratio and ratio>0):reason.append("SEM_FATOR_CAD_CX_PLT")
    if typ=="ASVD" and not origins:reason.append("SEM_MALHA_COMERCIAL_SAP")
    if typ=="ASVD" and origins and stock_found==0:reason.append("SEM_PAR_FABRICA_SKU")
    if typ=="ASCD" and not cdd_name:reason.append("SEM_DEPARA_CDD")
    if typ=="ASCD" and cdd_name and grade is None:reason.append("SEM_SKU_GRADE_CDD")
    if g["mixed_commercial"]:reason.append("COMERCIAL_DIVERGENTE_NA_CHAVE")
    if g["mixed_network"]:reason.append("REDE_DIVERGENTE_NA_CHAVE")
    if len(g["orig_variants"])>1:reason.append("ORIGINAL_DIVERGENTE_NA_CHAVE")
    if pending is not None and pending<0:reason.append("PENDENTE_NEGATIVO")
    if g["overlaps"]:reason.append("POSSIVEL_SOBREPOSICAO_REMESSA_FATURADO")
    if filled is not None and filled>100:reason.append("FATURADO_MAIOR_QUE_ORIGINAL")
    if typ=='MISTO':
        counter['mixed_groups']+=1
        active={t for t in g['active_types'] if t in ('ASCD','ASVD')}
        if len(active)==1:
            counter['mixed_keys_with_one_non_cancel_type']+=1
            counter['mixed_keys_with_one_non_cancel_type_pending_CX']+=pending if pending is not None else 0
            counter['mixed_keys_only_active_'+next(iter(active))]+=1
        elif len(active)>1:
            counter['mixed_keys_with_both_non_cancel_types']+=1
            counter['mixed_keys_with_both_non_cancel_types_pending_CX']+=pending if pending is not None else 0
        else:
            counter['mixed_keys_with_no_non_cancel_type']+=1
            counter['mixed_keys_with_no_non_cancel_type_pending_CX']+=pending if pending is not None else 0
        mixed_rows.append([*k,g['network'],g['commercial'],g['validity'],g['count'],
             '|'.join(sorted(active)),g['type'].get('ASCD',0),g['type'].get('ASVD',0),
             round(g['type_movement_pending']['ASCD'],2),round(g['type_movement_pending']['ASVD'],2),
             pending,g['status_cancel_rows'],len(g['orig_variants'])])
        for t in ('ASCD','ASVD'):
            counter['mixed_pending_segment_'+t+'_CX']+=g['type_movement_pending'][t]
        if complete and pending is not None and pending>0:counter['mixed_positive_pending_groups']+=1
    if g["count"]>1:counter["repeat_groups"]+=1
    if g["overlaps"]:counter["overlap_groups"]+=1;counter["overlap_rows"]+=g["overlaps"]
    if g["raw_negative"]:counter["raw_negative_rows"]+=g["raw_negative"]
    if len(g["orig_variants"])>1:counter["original_divergent_groups"]+=1
    if g["mixed_commercial"]:counter["commercial_divergent_groups"]+=1
    if g["mixed_network"]:counter["network_divergent_groups"]+=1
    if complete:
        if pending==0 and g['updated']>0 and g['carWithout']==0 and g['carWith']+g['billed']>=g['updated']-1e-7 and g['overlaps']==0:
            counter['attended_item_keys_by_movements']+=1
        elif pending==0:
            counter['zero_pending_but_not_attended']+=1
        elif pending>0 and (g['carWith']>0 or g['billed']>0):
            counter['partially_attended_item_keys']+=1
        elif pending>0:counter['pending_without_any_remessa_or_billing']+=1
        counter["complete_groups"]+=1
        counter["volume_updated_CX"]+=g["updated"]
        counter["volume_remessa_CX"]+=g["carWith"]
        counter["volume_sem_remessa_CX"]+=g["carWithout"]
        counter["volume_faturado_CX"]+=g["billed"]
        counter["volume_pending_calculado_CX"]+=pending
        if pending<0:counter["negative_pending_groups"]+=1
        if pending==0:counter["zero_pending_groups"]+=1
        if pending>0:counter["positive_pending_groups"]+=1
        if filled is not None and filled>100:counter["overbilling_groups"]+=1
        if original is not None:counter["original_selected_CX"]+=original
        for typ2 in [typ,"ALL"]:
            t=stats[typ2];t["complete_keys"]+=1;t["atualizada_CX"]+=g["updated"];t["marcado_CX"]+=g["carWith"]
            t["sem_remessa_CX"]+=g["carWithout"];t["faturado_CX"]+=g["billed"];t["pending_CX"]+=pending
            if pending<0:t["neg_pending_keys"]+=1
            if week:t["week_16_22_keys"]+=1;t["week_16_22_pending_CX"]+=pending
    else:counter["incomplete_groups"]+=1
    if typ=="ASVD":
        counter["asvd_groups"]+=1
        if c:counter["asvd_eg_with_cad"]+=1
        if origins:counter["asvd_with_malha"]+=1
        if stock_found:counter["asvd_with_factory_sku"]+=1
        if positives:counter["asvd_with_D1_positive_origin"]+=1
        if complete and pending is not None and pending>0 and ratio and ratio>0:
            pplt=pending/ratio
            for br in origins:
                originSku[(br,eg)]+=pplt
                altsets[eg].add(br)
                originStock[(br,eg)]=factory.get((br,eg))
    elif typ=="ASCD":
        counter["ascd_groups"]+=1
        if cdd_name:counter["ascd_with_dpar"]+=1
        if grade is not None:counter["ascd_with_grade"]+=1
        if pending is not None and pending>0 and cdd_name and grade is not None:
            cdSku[(cdd_name,eg)]+=pending
        if pending is not None and pending>0 and grade is not None:
            if grade>=pending:counter["ascd_individual_fully_covered"]+=1
            elif grade>0:counter["ascd_individual_partial"]+=1
    row=[*k,g["network"],g["client"],g["commercial"],typ,"|".join(sorted(unitset)),g["validity"],
         g["count"],original,g["original_hl"],g["original_plt"],g["updated"] if complete else None,
         g["carWith"] if complete else None,g["carWithout"] if complete else None,
         g["billed"] if complete else None,pending,filled,
         sap,ratio,len(origins),stock_found,positives,cdd_name,grade,
         len(g["orig_variants"]),g["overlaps"],"|".join(reason)]
    rows.append(row)
    if reason:exceptions.append(row)
for (br,eg),pendplt in originSku.items():
    found=originStock.get((br,eg))
    r=formation[br];r["pending"]+=pendplt;r["skus"]+=1
    if len(altsets[eg])>1:r["alt"]+=1
    if found is None:r["unknown"]+=1
    else:r["qualified"]+=min(pendplt,max(0,found))
if not rows:raise RuntimeError("Nenhuma chave de Order processada")
for br,x in formation.items():
    x["full_cars_24PLT"]=math.floor(x["qualified"]/24)
    x["pending_next_car_PLT"]=24-x["qualified"]%24
summary["comparisons"]={k:round(v,2) if isinstance(v,float) else v for k,v in counter.items()}
summary["by_type"]={k:{n:round(v,2) if isinstance(v,float) else v for n,v in ct.items()} for k,ct in stats.items()}
summary["order_source_has_pending_column"]=False
summary["caveat"]="Pendente CX derivado dos quatro movimentos; a Order não fornece coluna independente Pendente. Totais de estoque são potenciais e não reservas; origens alternativas não podem ser somadas como alocação única."
summary["VD_formation"]={k:{x:round(v,2) if isinstance(v,float) else v for x,v in values.items()} for k,values in formation.items()}
summary["CD_coverage_by_center"]={}
for (cdd,eg),pend in cdSku.items():
    ref=grades[cdd].get(eg[:-1])
    g=summary["CD_coverage_by_center"].setdefault(cdd,{"pending_CX":0.0,"qualified_CX":0.0,"skus":0})
    g["pending_CX"]+=pend;g["qualified_CX"]+=min(pend,max(0,ref or 0));g["skus"]+=1
for g in summary["CD_coverage_by_center"].values():
    g["pending_CX"]=round(g["pending_CX"],2);g["qualified_CX"]=round(g["qualified_CX"],2)
headers=["Pedido ERP","Cliente EG","SKU EG","Rede","Cliente","Comercial","Tipo Pedido","Unidades","Vencimento",
         "Linhas da chave","Original CX","Original HL","Original PLT","Atualizada CX","Carro com Remessa CX",
         "Carro sem Remessa CX","Faturado CX","Pendente Calculado CX","Fill Rate bruto %",
         "SAP da CAD Cod S4","CX por PLT","Origens Malha","Origens com SKU na fábrica",
         "Origens D1 positivo","CDD","Grade CD em CX","Variantes Original","Linhas sobreposição","Diagnóstico"]
csvout("conciliacao_por_pedido_cliente_sku.csv",headers,rows)
csvout("divergencias_e_pendencias.csv",headers,exceptions)
csvout("chaves_tipo_pedido_misto.csv",['Pedido ERP','Cliente EG','SKU EG','Rede','Comercial','Validade','Linhas',
       'Tipo não cancelado','Linhas ASCD','Linhas ASVD','Pendente movimentos ASCD CX','Pendente movimentos ASVD CX',
       'Pendente da chave CX','Linhas canceladas','Variantes de Original'],mixed_rows)
csvout("formacao_por_fabrica.csv",
       ["Fábrica BR","Código PCA","Pendente PLT (oportunidades)","Qualificado PLT","Carros 24 PLT (potenciais)",
        "PLT faltantes próximo carro","SKUs","SKUs com origens alternativas","SKUs sem D1"],
       [[br,factorymap.get(br,""),round(x["pending"],2),round(x["qualified"],2),x["full_cars_24PLT"],
         round(x["pending_next_car_PLT"],2),x["skus"],x["alt"],x["unknown"]] for br,x in sorted(formation.items())])
(OUT/"resumo_reconciliacao.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
print("AUDITORIA_ORDER_V29_SUMMARY_START")
print(json.dumps(summary,ensure_ascii=False))
print("AUDITORIA_ORDER_V29_SUMMARY_END")
print("ARQUIVOS_DE_EVIDENCIA",json.dumps({p.name:p.stat().st_size for p in OUT.iterdir() if p.is_file()},ensure_ascii=False))


# QA v53: preserva a auditoria v29 e inclui os insumos do mesmo commit para teste local.
if __name__ == '__main__':
    import pathlib, shutil, hashlib, json
    root=pathlib.Path('.')
    out=pathlib.Path('auditoria-order/insumos-v53')
    out.mkdir(parents=True,exist_ok=True)
    sources=[root/'Order.zip',root/'BASE_ESTOQUE 16.11.xlsx',*root.glob('*ExportReportOrderHistory.csv')]
    manifest=[]
    for source in sources:
        shutil.copy2(source,out/source.name)
        manifest.append({'file':source.name,'bytes':source.stat().st_size,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    (out/'manifesto.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('QA_V53_INSUMOS',json.dumps(manifest,ensure_ascii=False))
