import pathlib,json,sys,time
root=pathlib.Path(__file__).parent
key=sys.argv[1]
query=pathlib.Path(sys.argv[2]).read_text(encoding='utf-8-sig')
req={'name':'dax_query_operations','arguments':{'request':{'operation':'Execute','query':query,'maxRows':50000}}}
(root/f'request-{key}.json').write_text(json.dumps(req),encoding='utf-8')
out=root/f'response-{key}.json'
for _ in range(240):
 if out.exists():break
 time.sleep(.25)
d=json.loads(out.read_text(encoding='utf-8'))
for c in d.get('result',{}).get('content',[]):
 if c['type']=='resource':
  t=c['resource'].get('text','')
  (root/f'{key}.csv').write_text(t,encoding='utf-8')
  print(t[:45000])
 elif c['type']=='text':print(c['text'])
