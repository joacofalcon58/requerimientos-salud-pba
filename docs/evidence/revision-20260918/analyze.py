import csv,json,pathlib,collections,statistics
p=pathlib.Path(__file__).parent
def read(n):return [{k.split('[',1)[1][:-1]:v for k,v in r.items()} for r in csv.DictReader((p/n).open(encoding='utf-8'))]
f=read('008.csv');d=read('009.csv')
def num(v):return float(v.replace(',','.')) if v else 0
def n(r,k):return num(r[k])
consultas=['consultas_medicas','consultas_odontologicas','consultas_paramedicas','interconsultas']
def dem(r):return sum(n(r,k) for k in consultas)
out={}
ys=sorted(set(int(r['anio']) for r in f))
out['annual']=[{'year':y,'demand':sum(dem(r) for r in f if int(r['anio'])==y),'rows':sum(int(r['anio'])==y for r in f),'components':{k:sum(n(r,k) for r in f if int(r['anio'])==y) for k in consultas}} for y in ys]
for group in ['municipio_nombre','region_sanitaria']:
 vals=[]
 for g in set(r[group] for r in f):
  a=sum(dem(r) for r in f if r[group]==g and r['anio']=='2005');b=sum(dem(r) for r in f if r[group]==g and r['anio']=='2024')
  vals.append({'name':g,'2005':a,'2024':b,'delta':b-a,'pct':b/a-1 if a else None})
 out[group]=sorted(vals,key=lambda r:r['delta'],reverse=True)
out['classes']=dict(collections.Counter(r['Clasificacion Capacidad'] for r in d))
out['segments']=dict(collections.Counter(r['Segmento'] for r in d))
fields=['establecimiento_id','establecimiento_nombre','Dependencia','Municipio','Camas 22_24','Ocupacion 22_24','Giro 22_24','Egresos Anual 22_24','Estadia Media 22_24','Mortalidad 22_24','LOS Ratio','Mort Ratio','Segmento']
for cls in ['Saturado','Subutilizado','Anomalia de datos']:
 out[cls]=[{k:r[k] for k in fields} for r in sorted(d,key=lambda r:n(r,'Camas 22_24'),reverse=True) if r['Clasificacion Capacidad']==cls]
out['performance']= [{k:r[k] for k in fields} for r in sorted(d,key=lambda r:n(r,'Mort Ratio'),reverse=True) if r['Desempeno Internacion']=='Peor desempeno']
out['benchmarks']={dep:{'los':statistics.median(n(r,'Estadia Media 22_24') for r in d if r['Dependencia']==dep and r['Segmento']=='Agudos' and n(r,'Egresos Anual 22_24')>=100),'mort':statistics.median(n(r,'Mortalidad 22_24') for r in d if r['Dependencia']==dep and r['Segmento']=='Agudos' and n(r,'Egresos Anual 22_24')>=100),'count':sum(r['Dependencia']==dep and r['Segmento']=='Agudos' and n(r,'Egresos Anual 22_24')>=100 for r in d)} for dep in ['Municipal','Provincial','Nacional']}
out['duplicates']=[(k,v) for k,v in collections.Counter((r['anio'],r['establecimiento_id']) for r in f).items() if v>1]
recent=[r for r in f if r['anio'] in ['2022','2023','2024']]
out['recent_incomplete']=[{'id':r['establecimiento_id'],'name':r['establecimiento_nombre'],'years':sorted(set(x['anio'] for x in recent if x['establecimiento_id']==r['establecimiento_id']))} for r in d if r['Segmento']=='Agudos' and len(set(x['anio'] for x in recent if x['establecimiento_id']==r['establecimiento_id']))<3]
out['history']={r['establecimiento_id']:[{k:x[k] for k in ['anio','establecimiento_nombre','municipio_nombre','dependencia','egresos','dias_estadia','defunciones','pacientes_dias','dias_camas_disponible','promedio_camas_disponibles']} for x in f if x['establecimiento_id']==r['establecimiento_id']] for r in d if r['Desempeno Internacion']=='Peor desempeno' or r['Clasificacion Capacidad']=='Saturado'}
(p/'analysis.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k not in ['history','duplicates','municipio_nombre']},ensure_ascii=False,indent=2))
print('TOP MUNICIPALITIES',json.dumps(out['municipio_nombre'][:15],ensure_ascii=False));print('BOTTOM MUNICIPALITIES',json.dumps(out['municipio_nombre'][-6:],ensure_ascii=False));print('duplicate keys',len(out['duplicates']))
