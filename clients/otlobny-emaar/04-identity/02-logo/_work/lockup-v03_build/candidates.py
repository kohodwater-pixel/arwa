# v03 descriptor: candidate widths/sizes, rendered next to v02 for an optical decision.
import sys, re, io, json
sys.path.insert(0,'../lockup-v02_build')
import build
import cairosvg
from PIL import Image, ImageDraw, ImageFont
LOGO='/home/user/arwa/clients/otlobny-emaar/04-identity/02-logo/'
build.AR='شركة اطلبني اعمار'; build.EN='OTLOBNY EMAR COMPANY'
base=dict(ar_font='tajawal/Tajawal-Bold.ttf', en_font='ibmplexsans-static/IBMPlexSans-SemiBold.ttf', right=307.711, ar_top=103.258, gap=4.2)
C=[('B  Latin exactly as v02 (cap 8.8, +0.127 em); Arabic scaled to match',186.80,8.8),
   ('F  Latin cap 8.8, tracking reduced',170.65,8.8),
   ('E  between',165.0,8.3),
   ('D  Arabic exactly as v02 (18.05); Latin reduced',147.13,7.6)]
src=open(LOGO+'otlobny-emaar_logo_wordmark-colour_ar_v01.svg',encoding='utf-8').read()
paths=re.findall(r'^  <path [^\n]*/>$',src,re.M)
fnt=ImageFont.truetype('/home/user/arwa/assets/fonts/ibmplexsans-static/IBMPlexSans-Regular.ttf',20)
ims=[('v02 (superseded)',Image.open(io.BytesIO(cairosvg.svg2png(url=LOGO+'otlobny-emaar_logo_lockup-colour_ar-en_v02.svg',output_width=900,background_color='#fff'))))]
for lab,w,cap in C:
    L=build.layout(dict(base,width=w,en_cap=cap))
    H=max(L['en_box'][3],124.597)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 307.711 {H:.3f}">'+''.join(paths)+f'<path fill="#525456" d="{L["ar_d"]}"/><path fill="#525456" d="{L["en_d"]}"/></svg>'
    ims.append((f'{lab} | W {w} | AR {L["size_ar"]:.2f} | EN cap {cap} tr {L["tracking_em"]:+.3f} | H {H:.2f}',Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(),output_width=900,background_color='#fff')))))
    print(lab,{k:(round(v,3) if isinstance(v,float) else [round(x,2) for x in v]) for k,v in L.items() if not k.endswith('_d')})
W=2000; rows=(len(ims)+1)//2; S=Image.new('RGB',(W,rows*500),'#fff'); d=ImageDraw.Draw(S)
for i,(lab,im) in enumerate(ims):
    x=(i%2)*1000+50; y=(i//2)*500+20; d.text((x,y),lab,font=fnt,fill='#231F20'); S.paste(im.convert('RGB'),(x,y+40))
S.save('candidates_v03_width.png')
