exec(open(__file__.replace('detail.py','analyze.py'),encoding='utf-8').read().split('out={}')[0])
a=json.loads((p/'analysis.json').read_text(encoding='utf-8'))
geo={r['municipio_id']:r for r in read('010.csv')}
byid=collections.defaultdict(list)
for r in f:byid[r['establecimiento_id']].append(r)
delta=a['annual'][-1]['demand']-a['annual'][0]['demand']
print('GROWTH',delta,delta/a['annual'][0]['demand'],(a['annual'][-1]['demand']/a['annual'][0]['demand'])**(1/19)-1)
print('2020',a['annual'][15]['demand']/a['annual'][14]['demand']-1,'2024',a['annual'][-1]['demand']/a['annual'][-2]['demand']-1)
for group in ['region_sanitaria','municipio_nombre']:
 g=collections.defaultdict(lambda:[0,0])
 for r in f:
  if r['anio'] not in ['2005','2024']:continue
  name=geo.get(r['municipio_id'],{}).get(group,'SIN MATCH')
  g[name][0 if r['anio']=='2005' else 1]+=dem(r)
 vals=sorted([(name,v[0],v[1],v[1]-v[0],(v[1]-v[0])/delta) for name,v in g.items()],key=lambda v:v[3],reverse=True)
 print(group,json.dumps(vals[:15],ensure_ascii=False))
 print('top5share',sum(v[3] for v in vals[:5])/delta)
print('PERFORMANCE COUNTS',collections.Counter(r['Segmento'] for r in d if r['Desempeno Internacion']=='Peor desempeno'))
print('LOS ONLY',sum(r['Desempeno Internacion']=='Peor desempeno' and n(r,'Mort Ratio')<2 for r in d))
for cls in ['Saturado','Subutilizado','Anomalia de datos']:
 rr=[r for r in d if r['Clasificacion Capacidad']==cls]
 print('CLASS',cls,len(rr),sum(n(r,'Camas 22_24') for r in rr))
 if cls=='Saturado':print('SAT ALL YEARS',sum(len([x for x in byid[r['establecimiento_id']] if x['anio'] in ['2022','2023','2024'] and n(x,'dias_camas_disponible')>0 and n(x,'pacientes_dias')/n(x,'dias_camas_disponible')>=.9])==3 for r in rr))
ids=['37100084','76000329','21000039','25200617','65800199','42700049','1400022','51501436','58100033','46600049','30100011','26001035']
for id in ids:
 r=next(r for r in d if r['establecimiento_id']==id)
 print('DETAIL',r['establecimiento_nombre'],id)
 for x in sorted(byid[id],key=lambda x:x['anio']):
  if x['anio']<'2018':continue
  e=n(x,'egresos');dc=n(x,'dias_camas_disponible')
  print(x['anio'],x['establecimiento_nombre'],'egresos',e,'LOS',n(x,'dias_estadia')/e if e else None,'mort',n(x,'defunciones')/e if e else None,'occ',n(x,'pacientes_dias')/dc if dc else None,'PD',n(x,'pacientes_dias'))
print('RECENT DIFFERENT NAMES',sum(len(set(x['establecimiento_nombre'] for x in rows if x['anio'] in ['2022','2023','2024']))>1 for id,rows in byid.items() if id))
print('RECENT BLANKS', {k:sum(x[k]=='' for x in f if x['anio'] in ['2022','2023','2024']) for k in ['egresos','dias_estadia','defunciones','pacientes_dias','dias_camas_disponible']})
