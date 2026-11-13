"""Prepare the 27 partner logos. Reads _originals/ only; writes to 06-profiles/assets/partners/.
No redraw, recolour, sharpen or upscale: embedded rasters are taken at native pixels,
vector logos are rasterised from the PDF's own vector data."""
import pymupdf, numpy as np, json, os
from PIL import Image
PDF='_originals/otlobny_company-profile_original_2026-11-13.pdf'
OUT='06-profiles/assets/partners/'; WORK='06-profiles/_work/partners-src/'
doc=pymupdf.open(PDF); page=doc[18]
meta=[]

def trim_white(im, thr=235, mfrac=0.08, keep_full=False):
    a=np.asarray(im.convert('RGB')).astype(int)
    if keep_full: return im.convert('RGB'), 'full embedded image kept (own tinted tile)'
    m=(a.min(axis=2)<thr)
    ys,xs=np.where(m.any(1))[0],np.where(m.any(0))[0]
    x0,x1,y0,y1=xs[0],xs[-1]+1,ys[0],ys[-1]+1
    mg=max(6,int(round(mfrac*max(x1-x0,y1-y0))))
    W,H=im.size
    canvas=Image.new('RGB',(x1-x0+2*mg,y1-y0+2*mg),(255,255,255))
    sx0,sy0,sx1,sy1=max(0,x0-mg),max(0,y0-mg),min(W,x1+mg),min(H,y1+mg)
    canvas.paste(im.convert('RGB').crop((sx0,sy0,sx1,sy1)),(sx0-(x0-mg),sy0-(y0-mg)))
    touch=[s for s,c in zip('LTRB',(x0==0,y0==0,x1==W,y1==H)) if c]
    return canvas,(f'content {x1-x0}x{y1-y0}px'+(f'; content reaches source edge {"".join(touch)}' if touch else ''))

def embedded(xref):
    pix=pymupdf.Pixmap(doc,xref)
    sm=doc.extract_image(xref).get('smask',0)
    if pix.colorspace and pix.colorspace.n!=3 or pix.alpha: pix=pymupdf.Pixmap(pymupdf.csRGB,pix)
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    if sm:
        mp=pymupdf.Pixmap(doc,sm); mask=Image.frombytes('L',(mp.width,mp.height),mp.samples)
        assert mask.size==im.size
        im=Image.composite(im,Image.new('RGB',im.size,(255,255,255)),mask)
    return im

def render(clip,dpi):
    pix=page.get_pixmap(clip=pymupdf.Rect(*clip),dpi=dpi,colorspace=pymupdf.csRGB,alpha=False)
    return Image.frombytes('RGB',(pix.width,pix.height),pix.samples)

# (short-name, kind, arg) in reading order of the original page, right to left, row by row
E18=[
 ('madinah-award-foundation','emb',537),
 ('al-madinah-region-development-authority','ren',((578,216,660,268),400)),
 ('al-maqar','emb',539),
 ('we-ar-spa','vec',(365,200,465,280)),
 ('mawaddah','emb',540),
 ('imagine-more','vec',(140,215,243,270)),
 ('hsh','emb',548),
 ('taibah-cooperative','emb',541),
 ('dar-al-taqwa-hotel','emb',531),
 ('dallah-taibah-hotel','emb',532),
 ('al-madinah-harmony','emb',535),
 ('tiny-house','emb',542),
 ('platinum','vec',(672,392,792,478)),
 ('madinah-chamber','vec',(465,388,665,482)),
 ('manarat-taba-hotel','emb',534),
 ('hippo','vec',(290,388,372,478)),
 ('taza','ren',((175,403,272,466),400)),
 ('arabic-calligraphic-mark','emb',547),
]
for i,(name,kind,arg) in enumerate(E18,1):
    if kind=='emb':
        im=embedded(arg); info=doc.extract_image(arg)
        a=np.asarray(im).astype(int); corners=[a[1,1].min(),a[1,-2].min(),a[-2,1].min(),a[-2,-2].min()]
        keep=min(corners)<250 and max(corners)<252 and name=='taibah-cooperative'
        src=f'embedded image xref {arg}, native {im.size[0]}x{im.size[1]} px (CMYK/indexed -> sRGB)'
        out,note=trim_white(im,keep_full=keep); note+=f'; corners min-channel {corners}'
    elif kind=='ren':
        clip,dpi=arg; im=render(clip,dpi); src=f'page 19 render at {dpi} dpi (image with a soft mask of different resolution)'
        out,note=trim_white(im)
    else:
        im=render(arg,800); src='page 19 vector artwork rasterised at 800 dpi'
        out,note=trim_white(im)
    fn=f'existing-{i:02d}_{name}.png'; out.save(OUT+fn)
    meta.append(dict(file=fn,size=out.size,source=src,note=note)); print(fn,out.size,src,'|',note)

N9=['manazil-al-mukhtara','novotel','keeta','jahez','medina-dates-festival','hungerstation','rotana','chop-and-co','zero']
SRC='_originals/partner-logos-client_2026-11-13/'
for i,name in enumerate(N9,1):
    f=sorted(x for x in os.listdir(SRC) if x.startswith(f'{i:02d}_'))[0]
    im=Image.open(SRC+f).convert('RGB'); a=np.asarray(im).astype(int); H,W=a.shape[:2]
    rows=a.mean(axis=(1,2)); t=0
    # black bars: leading/trailing rows darker than the background, only when background is light
    light_bg=a[H//2,3].mean()>150
    b=H
    if light_bg:
        while rows[t]<128: t+=1
        while rows[b-1]<128: b-=1
        if t: t+=2
        if b<H: b-=2
    a2=a[t:b]; bg=np.median(np.concatenate([a2[:,:4].reshape(-1,3),a2[:,-4:].reshape(-1,3)]),axis=0)
    m=(np.abs(a2-bg).max(axis=2)>40)
    ys,xs=np.where(m.any(1))[0],np.where(m.any(0))[0]
    x0,x1,y0,y1=xs[0],xs[-1]+1,ys[0]+t,ys[-1]+1+t
    mg=int(round(0.08*max(x1-x0,y1-y0)))
    canvas=Image.new('RGB',(x1-x0+2*mg,y1-y0+2*mg),tuple(int(round(v)) for v in bg))
    sx0,sy0,sx1,sy1=max(0,x0-mg),max(t,y0-mg),min(W,x1+mg),min(b,y1+mg)
    canvas.paste(im.crop((sx0,sy0,sx1,sy1)),(sx0-(x0-mg),sy0-(y0-mg)))
    touch=[s for s,c in zip('LTRB',(x0==0,y0==t,x1==W,y1==b)) if c]
    pad=[s for s,c in zip('LTRB',(x0-mg<0,y0-mg<t,x1+mg>W,y1+mg>b)) if c]
    fn=f'new-{i:02d}_{name}.png'; canvas.save(OUT+fn)
    note=f'content {x1-x0}x{y1-y0}px; bars removed top {t}px bottom {H-b}px; bg {tuple(int(v) for v in bg)}; canvas padded with bg on {"".join(pad) or "none"}; content reaches source edge {"".join(touch) or "none"}'
    meta.append(dict(file=fn,size=canvas.size,source=SRC+f+f' ({W}x{H} px JPEG)',note=note)); print(fn,canvas.size,'|',note)
json.dump(meta,open(WORK+'meta.json','w'),ensure_ascii=False,indent=1)

# contact sheet
cols=6; cw,ch=420,330; rows_=-(-len(meta)//cols)
sheet=Image.new('RGB',(cols*cw,rows_*ch),(225,227,230))
from PIL import ImageDraw
d=ImageDraw.Draw(sheet)
for k,mt in enumerate(meta):
    im=Image.open(OUT+mt['file']); r=min((cw-30)/im.width,(ch-60)/im.height,2.0)
    th=im.resize((max(1,int(im.width*r)),max(1,int(im.height*r))),Image.LANCZOS)
    x=(k%cols)*cw+(cw-th.width)//2; y=(k//cols)*ch+10+(ch-60-th.height)//2
    sheet.paste(th,(x,y)); d.text(((k%cols)*cw+8,(k//cols)*ch+ch-40),mt['file'][:-4]+f"\n{im.width}x{im.height}",fill=(0,0,0))
sheet.save('06-profiles/_work/partners_contact-sheet.png'); print(len(meta),'logos on sheet',sheet.size)
