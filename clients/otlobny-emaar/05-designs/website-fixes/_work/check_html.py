import json,re,sys,urllib.request
def get(port,path):
    req=urllib.request.Request(f'http://127.0.0.1:{port}{path}',headers={'X-Forwarded-Proto':'https'})
    try: r=urllib.request.urlopen(req); return r.status,r.read().decode('utf-8')
    except urllib.error.HTTPError as e: return e.code,e.read().decode('utf-8')
def meta(h,name):
    m=re.search(r'<meta (?:name|property)="%s" content="([^"]*)"'%re.escape(name),h); return m.group(1) if m else None
def show(port,path):
    st,h=get(port,path); print('\n=====',port,path,st)
    print('title      :',re.search(r'<title>(.*?)</title>',h).group(1))
    for n in ['description','robots','og:title','og:description','og:url','og:type','og:site_name','og:locale','og:image']: print(f'{n:11}:',meta(h,n))
    c=re.search(r'<link rel="canonical" href="([^"]*)"',h); print('canonical  :',c.group(1) if c else None)
    print('css/js     :',re.findall(r'site\.(?:css|js)\?v=\d+',h), 'data-theme:',re.search(r'data-theme="([^"]*)"',h).group(1))
    lds=re.findall(r'<script type="application/ld\+json">(.*?)</script>',h,re.S); print('json-ld blocks:',len(lds))
    for l in lds:
        d=json.loads(l); print(json.dumps(d,ensure_ascii=False,indent=1))
    print('hamza-form count in HTML:',h.count('أطلبني'),'| header/footer/chat present:', '<header class="site-header">' in h, '<footer>' in h, 'id="chat"' in h, 'id="mobile-nav"' in h)
    return h
h=show(8765,'/'); 
print('project labels:',re.findall(r'<div><p>(.*?)</p><h3>',h))
print('footer:',re.sub(r'<[^>]+>',' | ',re.search(r'<footer>.*?</footer>',h,re.S).group(0)))
print('header small:',re.search(r'<small>(.*?)</small>',h).group(1)); print('service titles:',re.findall(r'<span class="number">(\d+)</span><h3>(.*?)</h3>',h))
print('chat:',re.findall(r'<b>(مرشد[^<]*)</b>|<p class="assistant">(.*?)</p>',h))
print('imgs:',re.findall(r'<img [^>]*>',h)[:4])
h=show(8765,'/?service=contracting'); print('main:',re.sub(r'<[^>]+>','|',re.search(r'<main.*?</main>',h,re.S).group(0)))
show(8765,'/?service=landscaping'); h=show(8765,'/?service=zzzz'); print('main:',re.sub(r'<[^>]+>','|',re.search(r'<main.*?</main>',h,re.S).group(0)))
