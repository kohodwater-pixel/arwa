import cv2,numpy as np,json
R=lambda i: cv2.rotate(cv2.imread(f'B/{i:03d}.png'),cv2.ROTATE_90_CLOCKWISE)
HX=704
def fit_env(t,v,sign,iters=6):
    # robust line v=a*t+b keeping the outer envelope (sign=+1 keep larger v)
    t=np.asarray(t,float); v=np.asarray(v,float); keep=np.ones(len(t),bool)
    for _ in range(iters):
        a,b=np.polyfit(t[keep],v[keep],1); r=(v-(a*t+b))*sign
        keep=(r>-2.0)&(r<6)
        if keep.sum()<10: break
    return a,b
def detect(f):
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    w=((hsv[...,1]<45)&(hsv[...,2]>150)).astype(np.uint8)
    w[:, :HX+3]=0
    n,lab,st,_=cv2.connectedComponentsWithStats(w)
    if n<2: return None
    k=1+np.argmax(st[1:,4]); m=(lab==k)
    if st[k,4]<1500: return None
    ys=np.arange(115,640); right=np.array([ (np.where(m[y])[0].max() if m[y].any() else 0) for y in ys])
    ok=right>0
    if ok.sum()<50: return None
    a,b=fit_env(ys[ok],right[ok],+1)
    xr=int(np.median(right[ok]))
    xs=np.arange(HX+8,max(HX+12,int(a*380+b)-6))
    if len(xs)<8: return None
    top=np.array([np.where(m[:,x])[0].min() if m[:,x].any() else 9999 for x in xs]); bot=np.array([np.where(m[:,x])[0].max() if m[:,x].any() else -1 for x in xs])
    at,bt=fit_env(xs[top<9999],top[top<9999],-1); ab,bb=fit_env(xs[bot>=0],bot[bot>=0],+1)
    def inter(al,bl,ae,be): # y=al*x+bl ; x=ae*y+be
        y=(al*be+bl)/(1-al*ae); return [ae*y+be,y]
    return dict(ft=inter(at,bt,a,b),fb=inter(ab,bb,a,b),ht=[HX,at*HX+bt],hb=[HX,ab*HX+bb],area=int(st[k,4]))
res={}
tiles=[]
for i in range(40,72):
    f=R(i); d=detect(f); res[i]=d
    if i%2==0:
        g=f.copy()
        if d:
            q=np.array([d['ht'],d['ft'],d['fb'],d['hb']],np.int32); cv2.polylines(g,[q],True,(0,200,0),2)
        cv2.putText(g,str(i),(10,40),0,1.2,(0,255,255),2); tiles.append(g[:,420:1100])
    print(i, None if d is None else [[round(v) for v in d[k]] for k in ('ht','ft','fb','hb')])
cv2.imwrite('lid_dbg.png',np.vstack([np.hstack(tiles[k:k+4]) for k in range(0,16,4)]))
