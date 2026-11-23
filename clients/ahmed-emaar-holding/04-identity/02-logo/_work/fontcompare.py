import sys; sys.path.insert(0,'.')
from textpath import shape
import cairosvg, io
from PIL import Image, ImageDraw
F='/home/user/arwa/assets/fonts/'
AR='أحمد إعمار القابضة'
cands=[('Cairo 700',F+'cairo/Cairo[slnt,wght].ttf',{'wght':700}),
('Cairo 800',F+'cairo/Cairo[slnt,wght].ttf',{'wght':800}),
('Tajawal Bold',F+'tajawal/Tajawal-Bold.ttf',None),
('Tajawal ExtraBold',F+'tajawal/Tajawal-ExtraBold.ttf',None),
('IBM Plex Sans Arabic Bold',F+'ibmplexsansarabic/IBMPlexSansArabic-Bold.ttf',None),
('Noto Kufi Arabic 700',F+'notokufiarabic/NotoKufiArabic[wght].ttf',{'wght':700}),
('Noto Kufi Arabic 600',F+'notokufiarabic/NotoKufiArabic[wght].ttf',{'wght':600}),
('Noto Sans Arabic 700',F+'notosansarabic/NotoSansArabic[wdth,wght].ttf',{'wght':700,'wdth':100}),
]
Z=4
im=Image.open('../../../_originals/ahmed-emaar-holding_identity-board_reference.webp').convert('RGB')
ref=im.crop((62,196,328,240)).resize((266*Z,44*Z),Image.LANCZOS)
tiles=[('REFERENCE',ref)]
for name,p,v in cands:
    d,w,b=shape(p,AR,100,v)
    x0,y0,x1,y1=b; sc=245/(x1-x0)
    # baseline in ref crop at y=229.5-196 = 33.5
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{266*Z}" height="{44*Z}"><rect width="100%" height="100%" fill="#14233b"/><g transform="scale({Z}) translate({72-62-x0*sc},{33.5}) scale({sc})"><path d="{d}" fill="#d4a650"/></g></svg>'
    png=cairosvg.svg2png(bytestring=svg.encode())
    tiles.append((name,Image.open(io.BytesIO(png)).convert('RGB')))
W=266*Z; H=44*Z+30
sheet=Image.new('RGB',(W,H*len(tiles)),'white'); dr=ImageDraw.Draw(sheet)
for i,(n,t) in enumerate(tiles):
    dr.text((8,i*H+8),n,fill='black'); sheet.paste(t,(0,i*H+30))
sheet.save('font_compare_arabic.png')
