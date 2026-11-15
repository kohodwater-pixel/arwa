import json,subprocess,time,os,sys,re
from urllib.parse import unquote
r=json.load(open('results.json'))
old=json.load(open('../search/results.json'))
for k,v in old.items():
    if 'Ithlib' in k and k not in r: r[k]=v
json.dump(r,open('results_all.json','w'))
pats=sys.argv[1:]
keys=[k for k in r if any(re.search(p,unquote(k)) for p in pats)]
idx=json.load(open('idx.json')) if os.path.exists('idx.json') else {}
for k in keys:
    if k in idx: continue
    n=len(idx); p=f'th/{n:03d}.jpg'
    u=r[k][0].split('?')[0].replace('thumb.wikimedia.org','upload.wikimedia.org')
    ok=False
    for a in range(4):
        c=subprocess.run(['curl','-sS','-A','CreativeAgencyBot/1.0 (open-licence image research)','-o',p+'.tmp','-w','%{http_code}',u],capture_output=True,text=True)
        if c.stdout.strip()=='200': os.replace(p+'.tmp',p); ok=True; break
        time.sleep(35)
    if ok: idx[k]=n; json.dump(idx,open('idx.json','w')); print(n,unquote(k)[5:70],flush=True)
    else: print('FAIL',unquote(k)[5:70],flush=True)
    time.sleep(8)
