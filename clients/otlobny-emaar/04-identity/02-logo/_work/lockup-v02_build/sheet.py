import cairosvg, io
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
LOGO='/home/user/arwa/clients/otlobny-emaar/04-identity/02-logo/'
ORIG='/home/user/arwa/clients/otlobny-emaar/_originals/client-uploads_2026-11-14/photo_dar-al-taqwa-hotel-entrance.jpg'
fnt=ImageFont.truetype('/home/user/arwa/assets/fonts/ibmplexsans-static/IBMPlexSans-Medium.ttf',22)
fsm=ImageFont.truetype('/home/user/arwa/assets/fonts/ibmplexsans-static/IBMPlexSans-Regular.ttf',18)
def rend(v,w): return Image.open(io.BytesIO(cairosvg.svg2png(url=LOGO+f'otlobny-emaar_logo_lockup-{v}_ar-en_v02.svg',output_width=w))).convert('RGBA')
TW,TH=1000,620
def tile(bg,v,label,lc):
    t=bg.copy() if isinstance(bg,Image.Image) else Image.new('RGBA',(TW,TH),bg)
    lg=rend(v,760); t.alpha_composite(lg,((TW-lg.width)//2,(TH-lg.height)//2-10))
    ImageDraw.Draw(t).text((24,TH-40),label,font=fsm,fill=lc); return t
grad=Image.new('RGBA',(TW,TH)); d=ImageDraw.Draw(grad)
import numpy as np
for x in range(TW):
    f=x/(TW-1); 
    c=[(0x1F,0x31,0x62),(0x2B,0x45,0x8A),(0x37,0x58,0xB0)]
    if f<0.52: a,b,t=c[0],c[1],f/0.52
    else: a,b,t=c[1],c[2],(f-0.52)/0.48
    d.line([(x,0),(x,TH)],fill=tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3)))
ph=Image.open(ORIG).convert('RGBA'); s=max(TW/ph.width,TH/ph.height); ph=ph.resize((int(ph.width*s)+1,int(ph.height*s)+1)); ph=ph.crop((0,max(0,(ph.height-TH)//4),TW,max(0,(ph.height-TH)//4)+TH))
ph=ImageEnhance.Brightness(ph).enhance(0.8); ov=Image.new('RGBA',(TW,TH),(31,49,98,150)); ph.alpha_composite(ov)
tiles=[tile('#FFFFFF','colour','colour  |  on white','#525456'),tile('#F7F8FC','navy','navy (one colour)  |  on light tint #F7F8FC','#525456'),
       tile('#1F3162','reversed','reversed  |  on navy #1F3162','#FFFFFF'),tile(grad,'white','white  |  on brand gradient','#FFFFFF'),
       tile('#3758B0','white','white  |  on royal blue #3758B0','#FFFFFF'),tile(ph,'white','white  |  on photograph with navy overlay (test only)','#FFFFFF')]
# small size panel
SW=2*TW; SP=Image.new('RGBA',(SW,2000),'#FFFFFF'); d=ImageDraw.Draw(SP)
d.text((24,16),'Small-size test, colour version on white. Print renders at 300 dpi shown 1:1; screen renders at 1x; right column = descriptor of the same render enlarged (nearest neighbour), no smoothing added.',font=fnt,fill='#231F20')
rows=[('45 mm wide (300 dpi = 531 px)  - recommended minimum, print',531),('30 mm wide (300 dpi = 354 px) - below minimum: Latin line 3.5 pt; use wordmark alone',354),('20 mm wide (300 dpi = 236 px)  - descriptor not legible: use wordmark alone',236),
      ('screen 320 px wide - recommended minimum, screen',320),('screen 240 px wide - borderline: Latin caps 7 px high',240),('screen 160 px wide - too small: use wordmark alone',160)]
y=70
for lab,w in rows:
    im=rend('colour',w); d.text((24,y),lab,font=fsm,fill='#525456'); SP.alpha_composite(im,(24,y+30))
    crop=im.crop((int(im.width*0.25),int(im.height*0.72),im.width,im.height))
    k=min(4,1300//crop.width); big=crop.resize((crop.width*k,crop.height*k),Image.NEAREST)
    d.text((660,y),'descriptor enlarged %dx'%k,font=fsm,fill='#525456'); SP.alpha_composite(big,(660,y+30))
    y+=max(im.height,big.height)+70
SP=SP.crop((0,0,SW,y+10))
sheet=Image.new('RGBA',(SW,3*TH+SP.height),'#FFFFFF')
for i,t in enumerate(tiles): sheet.alpha_composite(t,((i%2)*TW,(i//2)*TH))
sheet.alpha_composite(SP,(0,3*TH))
sheet.convert('RGB').save(LOGO+'_work/sheet_lockup_v02_all-versions_small-size-test.png')
print(sheet.size)
