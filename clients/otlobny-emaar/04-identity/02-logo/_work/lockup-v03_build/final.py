# Lockup v03: same method as v02 (../lockup-v02_build/shape.py + build.layout), only the strings and the block width change.
# Arabic = registered name (commercial registration certificate shown by the client 2026-11-27).
import sys, re, json
sys.path.insert(0,'../lockup-v02_build')
import build
import cairosvg
LOGO='/home/user/arwa/clients/otlobny-emaar/04-identity/02-logo/'
AR='شركة اطلبني اعمار'   # شركة اطلبني اعمار — plain alef U+0627, no hamza
EN='OTLOBNY EMAR COMPANY'
assert AR=='شركة اطلبني اعمار' and 'إ' not in AR and 'أ' not in AR
build.AR=AR; build.EN=EN
# right, ar_top, gap, en_cap: unchanged from v02. width: 222.0 -> 171.363 (left ink edge on x = 136.348,
# the right edge of the stem to the left of the lam), see system.md section 1b.
P=dict(ar_font='tajawal/Tajawal-Bold.ttf', en_font='ibmplexsans-static/IBMPlexSans-SemiBold.ttf',
       right=307.711, width=307.711-136.348, ar_top=103.258, gap=4.2, en_cap=8.8)
L=build.layout(P)
H=round(max(L['en_box'][3],124.597),3)
cols={'colour':'#525456','reversed':'#FFFFFF','white':'#FFFFFF','navy':'#1F3162'}
meta={k:(v if not isinstance(v,str) else None) for k,v in L.items() if not k.endswith('_d')}
meta['viewbox_h']=H; meta['params']=P; meta['strings']={'ar':AR,'en':EN}
json.dump(meta,open('lockup_v03_metrics.json','w',encoding='utf-8'),indent=1,ensure_ascii=False)
title=f'اطلبني — {AR} — {EN}'
for v,c in cols.items():
    src=open(LOGO+f'otlobny-emaar_logo_wordmark-{v}_ar_v01.svg',encoding='utf-8').read()
    paths=re.findall(r'^  <path [^\n]*/>$',src,re.M)
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 307.711 {H}" width="307.711" height="{H}" role="img" aria-label="{title}">',
         f'  <title>{title}</title>',
         '  <!-- Wordmark: paths copied unchanged from otlobny-emaar_logo_wordmark-'+v+'_ar_v01.svg -->',
         '  <g id="wordmark">']
    out+=['  '+p for p in paths]
    out+=['  </g>',
          '  <!-- Descriptor v03: Tajawal Bold (Arabic, shaped with HarfBuzz, no tracking) and IBM Plex Sans SemiBold (caps, tracked), converted to outlines. Arabic string is the registered company name (commercial registration certificate shown by the client 2026-11-27); Latin string approved by the client 2026-11-27 (no registered Latin name). Supersedes v02. -->',
          f'  <g id="descriptor" fill="{c}">',
          f'    <path id="descriptor-ar" d="{L["ar_d"]}"/>',
          f'    <path id="descriptor-en" d="{L["en_d"]}"/>',
          '  </g>','</svg>','']
    fn=LOGO+f'otlobny-emaar_logo_lockup-{v}_ar-en_v03.svg'
    import os
    assert not os.path.exists(fn) or '--rebuild' in sys.argv, fn+' exists'
    open(fn,'w',encoding='utf-8').write('\n'.join(out))
    cairosvg.svg2png(url=fn,write_to=LOGO+f'_work/otlobny-emaar_logo_lockup-{v}_ar-en_v03_transparent.png',output_width=2000)
print(json.dumps(meta,indent=1,ensure_ascii=False))
