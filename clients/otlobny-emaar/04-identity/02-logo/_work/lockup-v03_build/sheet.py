# v03 previews on their grounds, v02/v03 comparison, small-size test, clearance measurements.
import cairosvg, io, json, numpy as np, re
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
LOGO='/home/user/arwa/clients/otlobny-emaar/04-identity/02-logo/'; W_=LOGO+'_work/'
ORIG='/home/user/arwa/clients/otlobny-emaar/_originals/client-uploads_2026-11-14/photo_dar-al-taqwa-hotel-entrance.jpg'
fnt=ImageFont.truetype('/home/user/arwa/assets/fonts/ibmplexsans-static/IBMPlexSans-Medium.ttf',22)
fsm=ImageFont.truetype('/home/user/arwa/assets/fonts/ibmplexsans-static/IBMPlexSans-Regular.ttf',18)
def rend(v,w,ver='v03'): return Image.open(io.BytesIO(cairosvg.svg2png(url=LOGO+f'otlobny-emaar_logo_lockup-{v}_ar-en_{ver}.svg',output_width=w))).convert('RGBA')
VB=(307.711,141.848); X=21.34  # clear space = alef width
# 1. single previews on the correct ground, with the clear space as margin
for v,bg,name in [('colour','#FFFFFF','on-white'),('navy','#F7F8FC','on-tint'),('navy','#FFFFFF','on-white'),('reversed','#1F3162','on-navy'),('white','#3758B0','on-blue'),('white','#1F3162','on-navy')]:
    lg=rend(v,1600); m=int(round(X/VB[0]*1600))
    im=Image.new('RGBA',(lg.width+2*m,lg.height+2*m),bg); im.alpha_composite(lg,(m,m))
    im.convert('RGB').save(W_+f'otlobny-emaar_logo_lockup-{v}_ar-en_v03_{name}.png')
# 2. comparison v02 | v03, all four versions
TW,TH=1000,560
def tile(bg,v,ver,label,lc):
    t=Image.new('RGBA',(TW,TH),bg); lg=rend(v,760,ver); t.alpha_composite(lg,((TW-760)//2,60))
    ImageDraw.Draw(t).text((24,TH-40),label,font=fsm,fill=lc); return t
rows=[('colour','#FFFFFF','on white','#525456'),('navy','#F7F8FC','on light tint #F7F8FC','#525456'),('reversed','#1F3162','on navy #1F3162','#FFFFFF'),('white','#3758B0','on royal blue #3758B0','#FFFFFF')]
cmp=Image.new('RGBA',(2*TW,len(rows)*TH),'#fff')
for i,(v,bg,g,lc) in enumerate(rows):
    cmp.alpha_composite(tile(bg,v,'v02',f'v02 (superseded)  |  {v}  |  {g}',lc),(0,i*TH))
    cmp.alpha_composite(tile(bg,v,'v03',f'v03 (current)  |  {v}  |  {g}',lc),(TW,i*TH))
cmp.convert('RGB').save(W_+'compare_lockup_v02-left_v03-right.png')
# 3. sheet: grounds + small sizes (same layout as the v02 sheet)
TH=620
def tile2(bg,v,label,lc):
    t=bg.copy() if isinstance(bg,Image.Image) else Image.new('RGBA',(TW,TH),bg)
    lg=rend(v,760); t.alpha_composite(lg,((TW-lg.width)//2,(TH-lg.height)//2-10))
    ImageDraw.Draw(t).text((24,TH-40),label,font=fsm,fill=lc); return t
grad=Image.new('RGBA',(TW,TH)); d=ImageDraw.Draw(grad)
for x in range(TW):
    f=x/(TW-1); c=[(0x1F,0x31,0x62),(0x2B,0x45,0x8A),(0x37,0x58,0xB0)]
    if f<0.52: a,b,t=c[0],c[1],f/0.52
    else: a,b,t=c[1],c[2],(f-0.52)/0.48
    d.line([(x,0),(x,TH)],fill=tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3)))
ph=Image.open(ORIG).convert('RGBA'); s=max(TW/ph.width,TH/ph.height); ph=ph.resize((int(ph.width*s)+1,int(ph.height*s)+1)); ph=ph.crop((0,max(0,(ph.height-TH)//4),TW,max(0,(ph.height-TH)//4)+TH))
ph=ImageEnhance.Brightness(ph).enhance(0.8); ph.alpha_composite(Image.new('RGBA',(TW,TH),(31,49,98,150)))
tiles=[tile2('#FFFFFF','colour','colour  |  on white','#525456'),tile2('#F7F8FC','navy','navy (one colour)  |  on light tint #F7F8FC','#525456'),
       tile2('#1F3162','reversed','reversed  |  on navy #1F3162','#FFFFFF'),tile2(grad,'white','white  |  on brand gradient','#FFFFFF'),
       tile2('#3758B0','white','white  |  on royal blue #3758B0','#FFFFFF'),tile2(ph,'white','white  |  on photograph with navy overlay (test only)','#FFFFFF')]
SW=2*TW; SP=Image.new('RGBA',(SW,2400),'#FFFFFF'); d=ImageDraw.Draw(SP)
d.text((24,16),'Small-size test v03, colour version on white. Print renders at 300 dpi shown 1:1; screen renders at 1x; right = descriptor of the same render enlarged (nearest neighbour).',font=fnt,fill='#231F20')
R=[('45 mm wide (300 dpi = 531 px)  - minimum, print (unchanged from v02)',531),('30 mm wide (300 dpi = 354 px) - below minimum: use wordmark alone',354),('20 mm wide (300 dpi = 236 px)  - below minimum: use wordmark alone',236),
   ('screen 320 px wide - minimum, screen (unchanged from v02)',320),('screen 240 px wide - below minimum',240),('screen 160 px wide - below minimum: use wordmark alone',160)]
y=70
for lab,w in R:
    im=rend('colour',w); d.text((24,y),lab,font=fsm,fill='#525456'); SP.alpha_composite(im,(24,y+30))
    crop=im.crop((int(im.width*0.42),int(im.height*0.71),im.width,im.height))
    k=min(4,1300//crop.width); big=crop.resize((crop.width*k,crop.height*k),Image.NEAREST)
    d.text((660,y),'descriptor enlarged %dx'%k,font=fsm,fill='#525456'); SP.alpha_composite(big,(660,y+30))
    y+=max(im.height,big.height)+70
SP=SP.crop((0,0,SW,y+10))
sheet=Image.new('RGBA',(SW,3*TH+SP.height),'#FFFFFF')
for i,t in enumerate(tiles): sheet.alpha_composite(t,((i%2)*TW,(i//2)*TH))
sheet.alpha_composite(SP,(0,3*TH))
sheet.convert('RGB').save(W_+'sheet_lockup_v03_all-versions_small-size-test.png')
# small-size crops saved separately at 3x for close viewing
for w,n in [(531,'45mm-300dpi'),(320,'320px')]:
    a=rend('colour',w,'v02'); b=rend('colour',w); c=Image.new('RGBA',(w*2+60,max(a.height,b.height)+20),'#fff'); c.alpha_composite(a,(10,10)); c.alpha_composite(b,(w+50,10))
    c=c.resize((c.width*3,c.height*3),Image.NEAREST); c.convert('RGB').save(f'small_{n}_v02-left_v03-right_3x.png')
# 4. measurements: ink bounds, clipping, clearance descriptor <-> wordmark
def mask(ver,gid):
    s=open(LOGO+f'otlobny-emaar_logo_lockup-navy_ar-en_{ver}.svg',encoding='utf-8').read()
    other='descriptor' if gid=='wordmark' else 'wordmark'
    s=re.sub(rf'<g id="{other}".*?</g>','',s,flags=re.S)
    h=float(re.search(r'viewBox="0 0 307.711 ([\d.]+)"',s).group(1)); pad=10
    s=s.replace(f'viewBox="0 0 307.711 {h}"',f'viewBox="{-pad} {-pad} {307.711+2*pad} {h+2*pad}"').replace(f'width="307.711" height="{h}"','')
    sc=8; im=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(),output_width=int((307.711+2*pad)*sc))))
    return np.array(im)[:,:,3]>127, sc, pad, h
for ver in ('v02','v03'):
    wm,sc,pad,h=mask(ver,'wordmark'); ds,_,_,_=mask(ver,'descriptor')
    ys,xs=np.nonzero(ds); bb=[xs.min()/sc-pad,ys.min()/sc-pad,(xs.max()+1)/sc-pad,(ys.max()+1)/sc-pad]
    def edge(m):
        e=m.copy(); e[1:-1,1:-1]=m[1:-1,1:-1]&~(m[:-2,1:-1]&m[2:,1:-1]&m[1:-1,:-2]&m[1:-1,2:]); return e
    wm2=wm.copy(); wm2[:int((60+pad)*sc)]=False
    a=np.argwhere(edge(wm2)).astype(np.float32); b=np.argwhere(edge(ds)).astype(np.float32)
    dist=min(float(np.sqrt(((a[None,:,:]-b[i:i+500,None,:])**2).sum(-1)).min()) for i in range(0,len(b),500))/sc
    ys2,xs2=np.nonzero(wm|ds); allb=[xs2.min()/sc-pad,ys2.min()/sc-pad,(xs2.max()+1)/sc-pad,(ys2.max()+1)/sc-pad]
    print(ver,'viewBox h',h,'| descriptor ink',[round(float(x),2) for x in bb],'| whole ink',[round(float(x),2) for x in allb],'| min distance descriptor-wordmark %.2f'%dist,'| gap to pill (x) %.1f'%(bb[0]-67.395))
