#!/usr/bin/env python3
"""Local cut-outs of HIPPO menu photos (flat pink wall / violet floor studio).
Usage: python3 cutout.py <photo-dir> <out-dir> [name ...]
Nothing leaves the machine. Output: <name>.png (RGBA, cropped) + preview_<name>.jpg on pink/violet.
To swap in HQ photos: put them in <photo-dir> with the same names and re-run; tune CFG if needed."""
import sys, os, json
import numpy as np, cv2

PINK_SMAX=[1.01]
WALL=(0xE6,0x3C,0x7C); FLOOR=(0x69,0x6B,0xC6)

def bg_rule(img):
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV_FULL).astype(np.float32)
    h=hsv[...,0]*360/255; s=hsv[...,1]/255; v=hsv[...,2]/255
    violet=(h>212)&(h<278)&(s>0.26)&(v>0.10)
    pink=((h>318)|(h<4))&(s>0.38)&(s<PINK_SMAX[0])&(v>0.45)
    return violet,pink

def fill(m):
    p=cv2.copyMakeBorder(m,2,2,2,2,cv2.BORDER_CONSTANT,value=0)
    ff=p.copy(); mm=np.zeros((p.shape[0]+2,p.shape[1]+2),np.uint8); cv2.floodFill(ff,mm,(0,0),2)
    p[ff!=2]=1
    return p[2:-2,2:-2].copy()

def cut(img, cfg):
    PINK_SMAX[0]=cfg.get('pink_smax',1.01)
    H,W=img.shape[:2]
    violet,pink=bg_rule(img)
    bg=violet|pink
    if cfg.get('pink_is_fg'):  # cartons: pink object in front of pink wall -> handled by polygon/extra rule
        bg=violet
    fg0=(~bg).astype(np.uint8)
    x0,y0,x1,y1=cfg.get('roi',(0,0,W,H))
    roi=np.zeros((H,W),np.uint8); roi[y0:y1,x0:x1]=1
    if 'poly' in cfg:
        roi[:]=0; cv2.fillPoly(roi,[np.array(cfg['poly'],np.int32)],1)
    fg0&=roi
    fg0=cv2.morphologyEx(fg0,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    n,lab,stats,_=cv2.connectedComponentsWithStats(fg0,8)
    keep=np.zeros_like(fg0)
    areas=stats[1:,cv2.CC_STAT_AREA]
    big=areas.max()
    for i in range(1,n):
        if stats[i,cv2.CC_STAT_AREA]>=cfg.get('minfrac',0.03)*big and stats[i,cv2.CC_STAT_HEIGHT]>12: keep[lab==i]=1
    # fill holes
    keep=fill(keep)
    k=cfg.get('band',7)
    sure_fg=cv2.erode(keep,np.ones((k,k),np.uint8))
    sure_bg=1-cv2.dilate(keep,np.ones((k,k),np.uint8))
    gm=np.where(sure_fg==1,cv2.GC_FGD,np.where(sure_bg==1,cv2.GC_BGD,np.where(keep==1,cv2.GC_PR_FGD,cv2.GC_PR_BGD))).astype(np.uint8)
    if cfg.get('grabcut',True):
        bm=np.zeros((1,65),np.float64); fm=np.zeros((1,65),np.float64)
        cv2.grabCut(img,gm,None,bm,fm,4,cv2.GC_INIT_WITH_MASK)
        mask=((gm==cv2.GC_FGD)|(gm==cv2.GC_PR_FGD)).astype(np.uint8)
    else: mask=keep
    # never keep clearly-background coloured pixels at the rim
    if not cfg.get('pink_is_fg'):
        rim=mask-cv2.erode(mask,np.ones((5,5),np.uint8))
        mask[(rim==1)&bg]=0
    else:
        rim=mask-cv2.erode(mask,np.ones((5,5),np.uint8))
        mask[(rim==1)&violet]=0
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    n,lab,stats,_=cv2.connectedComponentsWithStats(mask,8)
    if n>2:
        big=stats[1:,cv2.CC_STAT_AREA].max()
        for i in range(1,n):
            if stats[i,cv2.CC_STAT_AREA]<cfg.get('minfrac',0.03)*big: mask[lab==i]=0
    mask=fill(mask)
    return mask

def finish(img, mask, erode=1, feather=1.2):
    """shrink 1px, feather, and pull edge colours from the interior (kills pink/violet fringe)."""
    m=cv2.erode(mask,np.ones((3,3),np.uint8),iterations=erode) if erode else mask
    a=cv2.GaussianBlur(m.astype(np.float32),(0,0),feather)
    a=np.clip((a-0.15)/0.7,0,1)
    core=cv2.erode(m,np.ones((3,3),np.uint8),iterations=3)
    # inpaint colours outward from the core
    inp=cv2.inpaint(img,(1-core).astype(np.uint8)*255,6,cv2.INPAINT_TELEA) if True else img
    edge=(a>0)&(core==0)
    out=img.copy()
    # blend: on edge pixels use 65% interior-extended colour
    w=np.where(edge,0.7,0.0)[...,None]
    out=(out*(1-w)+inp*w).astype(np.uint8)
    rgba=np.dstack([out,(a*255).astype(np.uint8)])
    ys,xs=np.where(a>0.01)
    pad=6
    y0,y1=max(ys.min()-pad,0),min(ys.max()+pad,img.shape[0]); x0,x1=max(xs.min()-pad,0),min(xs.max()+pad,img.shape[1])
    return rgba[y0:y1,x0:x1],(int(x0),int(y0),int(x1),int(y1))

def preview(rgba,path):
    h,w=rgba.shape[:2]
    a=rgba[...,3:4].astype(np.float32)/255
    tiles=[]
    for col in (WALL,FLOOR,(255,255,255)):
        bgc=np.zeros((h,w,3),np.float32); bgc[:]=col[::-1]
        tiles.append((rgba[...,:3]*a+bgc*(1-a)).astype(np.uint8))
    cv2.imwrite(path,np.hstack(tiles),[cv2.IMWRITE_JPEG_QUALITY,90])

CFG={
 'crispy-chicken':{'roi':(0,745,1202,1600)},
 'box-breakfast-89':{'pink_smax':0.86,'grabcut':False},
}
if __name__=='__main__':
    src,out=sys.argv[1],sys.argv[2]; names=sys.argv[3:] or list(CFG)
    os.makedirs(out,exist_ok=True); meta={}
    for nme in names:
        img=cv2.imread(os.path.join(src,nme+'.jpg'))
        mask=cut(img,CFG.get(nme,{}))
        rgba,box=finish(img,mask)
        cv2.imwrite(os.path.join(out,nme+'.png'),rgba)
        preview(rgba,os.path.join(out,'preview_'+nme+'.jpg'))
        meta[nme]=box; print(nme,box,rgba.shape)
