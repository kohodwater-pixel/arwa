#!/usr/bin/env python3
"""Gathering box cut-out: the box is pink in front of a pink wall, so colour keying fails.
It is a straight-edged object: rough outline vertices are snapped to the strongest image edge
(per side, robust line fit), then the polygon is filled, feathered and edge-decontaminated.
Usage: python3 cutout_box.py <photo.jpg> <out-dir>   (vertices are in ORIGINAL photo pixels; rescale for HQ photos via SCALE)"""
import sys, os, json, numpy as np, cv2
sys.path.insert(0, os.path.dirname(__file__))
from cutout import finish, preview
SCALE=1.0
ROUGH=[(74,549),(713,418),(729,889),(758,901),(1129,1156),(1117,1313),(430,1543),(121,1230),(109,1066)]
SNAP=[12,10,0,0,6,6,7,8,10]
RETOUCH=[(173,537,7),(191,544,7)]   # white specks on the lid (photo px, radius): inpainted from the surrounding lid colour   # search half-width per side (side i = vertex i -> i+1)

def snap(img, P, R):
    g=cv2.cvtColor(img,cv2.COLOR_BGR2Lab).astype(np.float32)
    g=cv2.GaussianBlur(g,(0,0),1.2)
    lines=[]
    n=len(P)
    for i in range(n):
        a=np.array(P[i],np.float32); b=np.array(P[(i+1)%n],np.float32)
        d=b-a; L=np.linalg.norm(d); d/=L; nrm=np.array([-d[1],d[0]])
        pts=[]
        if R[i]<3: lines.append((a,d)); continue
        for t in np.linspace(0.12,0.88,60):
            c=a+d*L*t
            offs=np.arange(-R[i],R[i]+1)
            xs=c[0]+nrm[0]*offs; ys=c[1]+nrm[1]*offs
            prof=cv2.remap(g,xs.astype(np.float32).reshape(1,-1),ys.astype(np.float32).reshape(1,-1),cv2.INTER_LINEAR)[0]
            diff=np.linalg.norm(prof[4:]-prof[:-4],axis=1)
            k=int(diff.argmax()); 
            if diff[k]>6: pts.append(c+nrm*offs[k+2])
        pts=np.array(pts,np.float32)
        if len(pts)<10: lines.append((a,d)); continue
        vx,vy,x0,y0=cv2.fitLine(pts,cv2.DIST_HUBER,0,0.01,0.01).ravel()
        lines.append((np.array([x0,y0]),np.array([vx,vy])))
    out=[]
    for i in range(n):
        p1,d1=lines[i-1]; p2,d2=lines[i]
        A=np.array([d1,-d2]).T
        try:
            t=np.linalg.solve(A,p2-p1); v=p1+d1*t[0]
            if np.linalg.norm(v-np.array(P[i]))>30: v=np.array(P[i],np.float32)
        except np.linalg.LinAlgError: v=np.array(P[i],np.float32)
        out.append((float(v[0]),float(v[1])))
    return out

if __name__=='__main__':
    src,out=sys.argv[1],sys.argv[2]
    img=cv2.imread(src); H,W=img.shape[:2]
    rm=np.zeros((H,W),np.uint8)
    for x,y,r in RETOUCH: cv2.circle(rm,(round(x*SCALE),round(y*SCALE)),round(r*SCALE),255,-1)
    img=cv2.inpaint(img,rm,5,cv2.INPAINT_TELEA)
    P=[(x*SCALE,y*SCALE) for x,y in ROUGH]
    V=snap(img,P,SNAP)
    ov=img.copy()
    cv2.polylines(ov,[np.array(P,np.int32)],True,(255,255,255),1)
    cv2.polylines(ov,[np.array(V,np.int32)],True,(0,255,255),1)
    cv2.imwrite(os.path.join(out,'box_overlay.jpg'),ov)
    mask=np.zeros((H,W),np.uint8)
    cv2.fillPoly(mask,[np.round(np.array(V)*8).astype(np.int32)],1,cv2.LINE_8,3)
    rgba,box=finish(img,mask,erode=1,feather=1.0)
    cv2.imwrite(os.path.join(out,'box.png'),rgba)
    preview(rgba,os.path.join(out,'preview_box.jpg'))
    json.dump({'bbox':box,'verts':V},open(os.path.join(out,'box.json'),'w'))
    print(box,[(round(x),round(y)) for x,y in V])
