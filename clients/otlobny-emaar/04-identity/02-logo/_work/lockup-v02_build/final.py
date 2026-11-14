import sys, re, json
sys.path.insert(0,'.')
from build import layout
import cairosvg
LOGO='/home/user/arwa/clients/otlobny-emaar/04-identity/02-logo/'
P=dict(ar_font='tajawal/Tajawal-Bold.ttf', en_font='ibmplexsans-static/IBMPlexSans-SemiBold.ttf',
       right=307.711, width=222.0, ar_top=103.258, gap=4.2, en_cap=8.8)
L=layout(P)
H=round(max(L['en_box'][3],124.597),3)
cols={'colour':'#525456','reversed':'#FFFFFF','white':'#FFFFFF','navy':'#1F3162'}
meta={k:(v if not isinstance(v,str) else None) for k,v in L.items() if not k.endswith('_d')}
meta['viewbox_h']=H; meta['params']=P
json.dump(meta,open('lockup_v02_metrics.json','w'),indent=1)
title='اطلبني — شركة اطلبني إعمار المحدودة — OTLOBNY EMAR COMPANY LTD.'
for v,c in cols.items():
    src=open(LOGO+f'otlobny-emaar_logo_wordmark-{v}_ar_v01.svg',encoding='utf-8').read()
    paths=re.findall(r'^  <path [^\n]*/>$',src,re.M)
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 307.711 {H}" width="307.711" height="{H}" role="img" aria-label="{title}">',
         f'  <title>{title}</title>',
         '  <!-- Wordmark: paths copied unchanged from otlobny-emaar_logo_wordmark-'+v+'_ar_v01.svg -->',
         '  <g id="wordmark">']
    out+=['  '+p for p in paths]
    out+=['  </g>',
          '  <!-- Descriptor: Tajawal Bold (Arabic, shaped with HarfBuzz, no tracking) and IBM Plex Sans SemiBold (caps, tracked), converted to outlines. Name strings: agency decision pending client confirmation. -->',
          f'  <g id="descriptor" fill="{c}">',
          f'    <path id="descriptor-ar" d="{L["ar_d"]}"/>',
          f'    <path id="descriptor-en" d="{L["en_d"]}"/>',
          '  </g>','</svg>','']
    fn=LOGO+f'otlobny-emaar_logo_lockup-{v}_ar-en_v02.svg'
    open(fn,'w',encoding='utf-8').write('\n'.join(out))
    cairosvg.svg2png(url=fn,write_to=LOGO+f'_work/otlobny-emaar_logo_lockup-{v}_ar-en_v02_transparent.png',output_width=2000)
print(json.dumps(meta,indent=1))
