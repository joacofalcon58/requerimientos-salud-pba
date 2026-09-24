exec(open(__file__.replace('selected.py','analyze.py'),encoding='utf-8').read().split('out={}')[0])
idx=collections.defaultdict(list)
for r in f:
 if r['anio'] in ['2022','2023','2024']:idx[r['establecimiento_id']].append(r)
for id in ['21000039','76000329','30100011','65800199','42700049','1400022']:
 rows=idx[id];r=next(r for r in d if r['establecimiento_id']==id)
 print(r['establecimiento_nombre'], 'camas',sum(n(x,'promedio_camas_disponibles') for x in rows)/3,'PD anuales',sum(n(x,'pacientes_dias') for x in rows)/3,'egresos anuales',sum(n(x,'egresos') for x in rows)/3,'occ',sum(n(x,'pacientes_dias') for x in rows)/sum(n(x,'dias_camas_disponible') for x in rows),'giro',sum(n(x,'egresos') for x in rows)/sum(n(x,'promedio_camas_disponibles') for x in rows))
print('SAT with year >100',[(r['establecimiento_nombre'],[(x['anio'],n(x,'pacientes_dias')/n(x,'dias_camas_disponible')) for x in idx[r['establecimiento_id']] if n(x,'dias_camas_disponible')>0 and n(x,'pacientes_dias')>n(x,'dias_camas_disponible')]) for r in d if r['Clasificacion Capacidad']=='Saturado' and any(n(x,'dias_camas_disponible')>0 and n(x,'pacientes_dias')>n(x,'dias_camas_disponible') for x in idx[r['establecimiento_id']])])
print('LOS only agudos',sum(r['Segmento']=='Agudos' and r['Desempeno Internacion']=='Peor desempeno' and n(r,'Mort Ratio')<2 for r in d))
print('2024 components deltas', {k:sum(n(r,k) for r in f if r['anio']=='2024')-sum(n(r,k) for r in f if r['anio']=='2023') for k in consultas})
