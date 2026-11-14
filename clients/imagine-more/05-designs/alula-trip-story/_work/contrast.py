import json,sys,numpy as np
from PIL import Image
W='/home/user/arwa/clients/imagine-more/05-designs/alula-trip-story/_work/'
rects=json.load(open(W+'rects.json'))
def lum(a):
    a=a/255.0; a=np.where(a<=0.03928,a/12.92,((a+0.055)/1.055)**2.4); return 0.2126*a[...,0]+0.7152*a[...,1]+0.0722*a[...,2]
for L,rs in rects.items():
    im=np.asarray(Image.open(W+f'bgonly_{L}.png').convert('RGB')).astype(float); Lm=lum(im)
    row=[]
    for k,lst in rs.items():
        vals=np.concatenate([Lm[int(y0):int(y1)+1,int(x0):int(x1)+1].ravel() for x0,y0,x1,y1 in lst])
        med=1.05/(np.median(vals)+0.05); worst=1.05/(np.percentile(vals,95)+0.05)
        row.append(f'{k} {med:.1f} (worst {worst:.1f})')
    print(L.upper()+': '+' | '.join(row))
