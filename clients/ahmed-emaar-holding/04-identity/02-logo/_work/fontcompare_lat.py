import sys; sys.path.insert(0,'.')
from textpath import shape
import cairosvg, io
from PIL import Image, ImageDraw
F='/home/user/arwa/assets/fonts/'
T='AHMED EMAAR HOLDING'
cands=[('IBM Plex Sans 500',F+'ibmplexsans/IBMPlexSans[wdth,wght].ttf',{'wght':500,'wdth':100}),
('IBM Plex Sans 600',F+'ibmplexsans/IBMPlexSans[wdth,wght].ttf',{'wght':600,'wdth':100}),
('Inter 500',F+'inter/Inter[opsz,wght].ttf',{'wght':500,'opsz':14}),
('Inter 600',F+'inter/Inter[opsz,wght].ttf',{'wght':600,'opsz':14}),
('Cairo 600 (Latin)',F+'cairo/Cairo[slnt,wght].ttf',{'wght':600}),
]
Z=4
im=Image.open('../../../_originals/ahmed-emaar-holding_identity-board_reference.webp').convert('RGB')
ref=im.crop((62,240,328,262)).resize((266*Z,22*Z),Image.LANCZOS)
tiles=[('REFERENCE',ref)]
for name,p,v in cands:
    # cap height: measure H
    _,_,bH=shape(p,'H',100,v); cap=bH[3]-bH[1]
    size=10.6/cap*100
    # solve tracking for width 243
    lo,hi=0,1
    for _ in range(40):
        tr=(lo+hi)/2; d,w,b=shape(p,T,size,v,tracking=tr)
        if b[2]-b[0]<243: lo=tr
        else: hi=tr
    print(name,'size',round(size,2),'tracking em',round(tr,3))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{266*Z}" height="{22*Z}"><rect width="100%" height="100%" fill="#14233b"/><g transform="scale({Z}) translate({74-62-b[0]},{256.5-240})"><path d="{d}" fill="#d4a650"/></g></svg>'
    tiles.append((name,Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert('RGB')))
W=266*Z; H=22*Z+30
sheet=Image.new('RGB',(W,H*len(tiles)),'white'); dr=ImageDraw.Draw(sheet)
for i,(n,t) in enumerate(tiles):
    dr.text((8,i*H+8),n,fill='black'); sheet.paste(t,(0,i*H+30))
sheet.save('font_compare_latin.png')
