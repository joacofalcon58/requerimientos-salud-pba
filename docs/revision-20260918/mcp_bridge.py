import subprocess,json,sys,time,pathlib
root=pathlib.Path(__file__).parent
p=subprocess.Popen([r'C:\Users\joaco\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-x64\server\powerbi-modeling-mcp.exe','--read-only'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=open(__file__+'.log','w'),text=True,encoding='utf-8')
i=0
def call(method,params):
 global i
 i+=1
 p.stdin.write(json.dumps({'jsonrpc':'2.0','id':i,'method':method,'params':params})+'\n');p.stdin.flush()
 while True:
  line=p.stdout.readline()
  if not line: raise RuntimeError('Server closed')
  try: r=json.loads(line)
  except: continue
  if r.get('id')==i:return r
print(json.dumps(call('initialize',{'protocolVersion':'2024-11-05','capabilities':{},'clientInfo':{'name':'review','version':'1'}})),flush=True)
p.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n');p.stdin.flush()
(root/'tools.json').write_text(json.dumps(call('tools/list',{})),encoding='utf-8')
print('Ready',flush=True)
while True:
 for f in sorted(root.glob('request-*.json')):
  out=f.with_name(f.name.replace('request-','response-'))
  if out.exists():continue
  try: result=call('tools/call',json.loads(f.read_text(encoding='utf-8-sig')))
  except Exception as e: result={'error':str(e)}
  out.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
  print(out.name,flush=True)
 time.sleep(.2)
