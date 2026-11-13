"""Transparent versions of the 27 partner logos. Reads assets/partners/, writes assets/partners-transparent/.
Method: measure each file's own background colour from its border; flood-fill from the border through
near-background pixels; optionally add enclosed background regions (letter counters) chosen per logo;
soft alpha in a 2 px band at the edge, with colours un-multiplied against the background.
No global white key (except ZERO: single-colour mark, coverage key). No redraw, sharpen or upscale."""
import numpy as np, os, shutil, sys
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
SRC='06-profiles/assets/partners/'; OUT='06-profiles/assets/partners-transparent/'; WORK='06-profiles/_work/'
ALL=lambda **h: True
NONE=lambda **h: False
SIMPLE=lambda **h: not h['annular']
# per logo: (t0 = background tolerance, policy for ENCLOSED background-coloured regions)
CFG={
 'existing-01':(12,NONE),
 'existing-02':(14,SIMPLE),
 'existing-03':(14,SIMPLE),
 'existing-04':(6,ALL),
 'existing-05':(14,lambda **h: h['area']>=40),
 'existing-06':(6,ALL),
 'existing-07':(14,NONE),
 'existing-08':(8,ALL),
 'existing-09':(14,SIMPLE),
 'existing-10':(14,lambda **h: h['cy']>0.62),
 'existing-11':(12,lambda **h: h['cy']>0.42),
 'existing-12':(10,ALL),
 'existing-13':(6,lambda **h: h['cy']>0.47),
 'existing-14':(6,lambda **h: h['cx']<0.78),
 'existing-15':(12,NONE),
 'existing-16':(6,lambda **h: h['cy']>0.80),
 'existing-17':(12,NONE),
 'existing-18':(14,ALL),
 'new-01':(18,lambda **h: h['cy']>0.66),
 'new-02':(18,ALL),
 'new-03':(36,ALL),
 'new-04':(18,SIMPLE),
 'new-05':(18,NONE),
 'new-06':(18,NONE),
 'new-07':(18,ALL),
 'new-08':(18,ALL),
 'new-09':(0,None),
}
exec(open(WORK+'transparent_overrides.py').read()) if os.path.exists(WORK+'transparent_overrides.py') else None
T1={k:44 for k in ['existing-01','existing-03','existing-05','existing-07','existing-10','existing-15','existing-17','existing-18','existing-02']}
T1.update({'existing-08':40,'existing-09':26,'existing-11':26,'new-01':40,'new-02':40,'new-04':40,'new-05':40,'new-06':40,'new-07':44,'new-08':40})
CFG['new-05']=(18,lambda **h: h['cy']>0.86)
WIN={'new-07':25,'existing-15':11}
T1.update({'new-07':110,'existing-15':100})
report=[]
def process(fn):
    key=fn.split('_')[0]; t0,pol=CFG[key]
    a=np.asarray(Image.open(SRC+fn).convert('RGB')).astype(float); H,W=a.shape[:2]
    ring=np.concatenate([a[:2].reshape(-1,3),a[-2:].reshape(-1,3),a[:,:2].reshape(-1,3),a[:,-2:].reshape(-1,3)])
    bg=np.median(ring,axis=0)
    if key=='new-09':   # ZERO: white single-colour mark on charcoal -> coverage, painted in the ground's own charcoal
        cov=np.clip((a.mean(2)-bg.mean())/(255-bg.mean()),0,1); cov[cov<0.06]=0
        out=np.zeros((H,W,4),np.uint8); out[...,:3]=np.round(bg).astype(np.uint8); out[...,3]=np.round(cov*255)
        Image.fromarray(out,'RGBA').save(OUT+fn); report.append((fn,tuple(int(v) for v in bg),'coverage key',0,0)); return
    d=np.abs(a-bg).max(2); low=d<=t0
    lab,n=ndi.label(low)
    bl=np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])); bl=bl[bl>0]
    B=np.isin(lab,bl); T=B.copy()
    hl,hn=ndi.label(low&~B); kept=0; cleared=0
    for i,sl in enumerate(ndi.find_objects(hl),1):
        comp=hl[sl]==i; area=int(comp.sum())
        ys,xs=np.nonzero(comp); cy=(ys.mean()+sl[0].start)/H; cx=(xs.mean()+sl[1].start)/W
        ann=ndi.binary_fill_holes(comp).sum()>area*1.02+2
        if area>=2 and pol(area=area,cx=cx,cy=cy,annular=ann,frac=area/(H*W)):
            T[sl]|=comp; cleared+=1
        else: kept+=1
    d1=ndi.binary_dilation(T,iterations=1)&~T; d2=ndi.binary_dilation(T,iterations=2)&~T&~d1
    dref=ndi.maximum_filter(d,size=5); ratio=np.clip(d/np.maximum(dref,1),0,1)
    alpha=np.ones((H,W)); alpha[T]=0; alpha[d1]=ratio[d1]
    m2=d2&(ratio<0.6); alpha[m2]=ratio[m2]
    # soft zone: near-background pixels (JPEG ringing, halos) connected to the removed background.
    t1=T1.get(key,t0); nS=0
    if t1>t0:
        l1,_=ndi.label((d<=t1)|T); tl=np.unique(l1[T]); S=np.isin(l1,tl[tl>0])&~T
        floor=0.5*np.percentile(d[~T],90) if (~T).any() else 255
        dref7=ndi.maximum_filter(d,size=WIN.get(key,7))
        sa=np.clip(d/np.maximum(dref7,floor),0,1); sa[dref7<=t1]=0   # nothing mark-like within 3 px: noise
        alpha[S]=np.minimum(alpha[S],sa[S]); nS=int(S.sum())
    alpha[alpha<0.04]=0
    rgb=a.copy(); e=(alpha>0)&(alpha<1)
    rgb[e]=np.clip(bg+(a[e]-bg)/alpha[e][:,None],0,255)
    out=np.dstack([np.round(rgb),np.round(alpha*255)]).astype(np.uint8)
    out[out[...,3]==0,:3]=np.round(bg).astype(np.uint8)   # hidden colour = background, avoids dark fringes when scaled
    Image.fromarray(out,'RGBA').save(OUT+fn); comp=out[...,:3].astype(float)*out[...,3:4]/255+bg*(1-out[...,3:4]/255.); df=np.abs(comp-a).max(2)
    report.append((fn,tuple(int(v) for v in bg),f't0={t0} t1={t1}',f'counters cleared {cleared} kept {kept}',f'soft px {nS}',f'vs original on own bg: max diff {df.max():.0f}, px>24: {(df>24).sum()}'))
files=sorted(f for f in os.listdir(SRC) if f.endswith('.png'))
assert len(files)==27
for f in files: process(f)
shutil.copyfile(SRC+'new-03_keeta.png',OUT+'new-03_keeta_on-yellow.png'); shutil.copyfile(SRC+'new-09_zero.png',OUT+'new-09_zero_on-dark.png')
for r in report: print(*r)
def sheet(color,name,sel=None,cols=6,cw=640,ch=480):
    fs=files+['new-03_keeta_on-yellow.png','new-09_zero_on-dark.png'] if sel is None else sel
    rows=-(-len(fs)//cols); s=Image.new('RGB',(cols*cw,rows*ch),color); dr=ImageDraw.Draw(s)
    for k,f in enumerate(fs):
        im=Image.open(OUT+f).convert('RGBA'); r=min((cw-40)/im.width,(ch-50)/im.height,4.0)
        th=im.resize((max(1,int(im.width*r)),max(1,int(im.height*r))),Image.LANCZOS if r<1 else Image.BICUBIC)
        s.paste(th,((k%cols)*cw+(cw-th.width)//2,(k//cols)*ch+(ch-40-th.height)//2),th)
        dr.text(((k%cols)*cw+6,(k//cols)*ch+ch-16),f[:-4]+(' (variant)' if k>=27 and sel is None else ''),fill=(128,128,128))
    s.save(name); return s
sheet((255,255,255),WORK+'partners-transparent_on-white.png')
s=sheet((0x1F,0x31,0x62),WORK+'partners-transparent_on-navy.png')
# viewing pieces (preview scaling only)
w,h=s.size
for j in range(5): s.crop((0,j*480,w,(j+1)*480)).save(WORK+f'partners-src/navy_row{j+1}.png')
