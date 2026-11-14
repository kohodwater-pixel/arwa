import json,subprocess,time,os,sys
r=json.load(open('search/results.json')); sel=json.load(open('search/sel.json'))
jobs=[(4,1920,'dl_a'),(45,1920,'dl_b'),(12,3840,'dl_c'),(35,1920,'dl_c2')]
for i,w,d in jobs:
    os.makedirs(d,exist_ok=True); p=f'{d}/{i}_{w}.jpg'
    if os.path.exists(p): continue
    u=r[sel[i]][0].split('?')[0].replace('thumb.wikimedia.org','upload.wikimedia.org').replace('/250px-',f'/{w}px-')
    for a in range(6):
        c=subprocess.run(['curl','-sS','-A','CreativeAgencyBot/1.0 (open-licence image research)','-o',p+'.tmp','-w','%{http_code}',u],capture_output=True,text=True)
        print(i,w,c.stdout,flush=True)
        if c.stdout.strip()=='200': os.replace(p+'.tmp',p); break
        time.sleep(50)
    time.sleep(15)
