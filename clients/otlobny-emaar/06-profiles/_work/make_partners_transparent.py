#!/usr/bin/env python3
"""Partner logos -> transparent background (graphic-designer, 2026-11-13).
Border-measured background colour, flood fill from the borders, soft un-premultiplied edge.
Sources are read only. No redrawing, sharpening or upscaling."""
import glob, os, shutil, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

P = '/home/user/arwa/clients/otlobny-emaar/06-profiles'
SRC, OUT, WORK = P + '/assets/partners', P + '/assets/partners-transparent', P + '/_work'
S8 = np.ones((3, 3), bool)

# per-logo settings. counters: 'all' | 'none' | dict(min_area=, simple=True, box=(x0,y0,x1,y1) fractions)
D = dict(tol=14, lo=4, k=2, floor=50, counters='none')
LOW = dict(tol=18, t2=70)
KEEP = dict(t2=40)             # white belongs to the mark: cautious soft flood
VEC = dict(tol=8, t2=30, speck=0)
CFG = {
 'existing-01': dict(KEEP, tol=18, t2=30), 'existing-02': dict(counters='all', k=3, r=7, t2=70),
 'existing-03': dict(LOW, counters='all', tol=24),
 'existing-04': dict(VEC, counters='all'), 'existing-05': dict(LOW, counters=dict(min_area=60)),
 'existing-06': dict(VEC, counters='all'), 'existing-07': dict(KEEP, tol=18),
 'existing-08': dict(KEEP, tol=10, lo=3, t2=30, counters=dict(min_area=40)),
 'existing-09': dict(LOW, counters='all'), 'existing-10': dict(LOW, counters='all'), 'existing-11': dict(LOW, counters='all'),
 'existing-12': dict(counters='all'), 'existing-13': dict(VEC, hull=[(0.30, 0.0, 0.70, 0.47)]),
 'existing-14': dict(VEC, counters='all'),
 'existing-15': dict(KEEP, tol=18, shadow=1), 'existing-16': dict(VEC, counters=dict(box=(0, .76, 1, 1))),
 'existing-17': dict(KEEP, t2=70), 'existing-18': dict(LOW, counters='all'),
 'new-01': dict(counters='all', tol=18, t2=70), 'new-02': dict(counters='all', tol=18),
 'new-04': dict(KEEP, counters=dict(simple=True), tol=18, k=3), 'new-05': dict(KEEP, tol=26, k=3, counters=dict(box=(0, .84, 1, 1))),
 'new-06': dict(KEEP, tol=18, k=3),
 'new-07': dict(counters='all', tol=16, t2=70), 'new-08': dict(counters='all', tol=18),
}
try:
    sys.path.insert(0, WORK); from partners_overrides import OV  # optional per-logo overrides
    for k_, v_ in OV.items(): CFG.setdefault(k_, {}).update(v_)
except ImportError:
    pass

def bgcol(a):
    b = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]]).astype(float)
    return np.median(b, 0)

def cut(a, c):
    cfg = dict(D); cfg.update(c)
    a = a.astype(float); bg = bgcol(a)
    d = np.abs(a - bg).max(2)
    near = d <= cfg['tol']; prot = np.zeros_like(near)
    chroma = a.max(2) - a.min(2); shm = (chroma <= 28) & (a.min(2) >= 110) & ~near if cfg.get('shadow') else np.zeros_like(near)
    if cfg.get('protect') is not None:      # boxes (fractions) where near-bg pixels are never background
        h, w = d.shape
        for x0, y0, x1, y1 in cfg['protect']:
            near[int(y0*h):int(y1*h), int(x0*w):int(x1*w)] = False
    if cfg.get('hull'):                     # white inside the convex outline of the mark in this box stays
        from scipy.spatial import ConvexHull
        h, w = d.shape
        for x0, y0, x1, y1 in cfg['hull']:
            sub = np.zeros_like(near); sub[int(y0*h):int(y1*h), int(x0*w):int(x1*w)] = True
            ys, xs = np.nonzero(sub & (d > 60)); pts = np.c_[xs, ys]
            hv = pts[ConvexHull(pts).vertices]
            m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).polygon([tuple(map(int, q)) for q in hv], fill=1)
            near[np.array(m, bool)] = False; prot |= np.array(m, bool)
    lab, n = ndi.label(near | shm, S8)      # a soft grey shadow is passable, and is given its own alpha below
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    Bx = np.isin(lab, edge[edge > 0]); B = Bx & near; SH = Bx & shm
    cnt = cfg['counters']; cleared = 0
    if cnt != 'none':
        h, w = d.shape
        enc = near & ~B
        lab2, n2 = ndi.label(enc, S8)
        if cnt == 'all':
            B |= enc; cleared = n2
        else:
            objs = ndi.find_objects(lab2)
            for i, sl in enumerate(objs, 1):
                comp = lab2 == i; area = comp.sum()
                if area < cnt.get('min_area', 0): continue
                if 'box' in cnt:
                    x0, y0, x1, y1 = cnt['box']; ys, xs = np.nonzero(comp)
                    if not (xs.min() >= x0*w and xs.max() <= x1*w and ys.min() >= y0*h and ys.max() <= y1*h): continue
                if cnt.get('simple') and (ndi.binary_fill_holes(comp).sum() - area) > 20: continue
                B |= comp; cleared += 1
    k = cfg['k']
    dmax = ndi.maximum_filter(d, size=2*k + 3)
    ref = np.maximum(dmax, cfg['floor'])
    soft = np.clip((d - cfg['lo']) / (ref - cfg['lo']), 0, 1)
    band = ndi.binary_dilation(B, S8, iterations=k) & ~B          # mark side of the boundary
    inner = B & ndi.binary_dilation(~B, S8, iterations=k)          # background side of the boundary
    alpha = np.ones_like(d); alpha[B] = 0
    alpha[band] = soft[band]; alpha[inner] = soft[inner]
    # soft flood: weak (light) pixels reachable from the background get alpha = their distance from the
    # background colour relative to the strongest mark pixel nearby. Composited on the old ground this is exact.
    t2, R = cfg.get('t2', 60), cfg.get('r', 4)
    weak = ((d <= t2) & ~prot) | B
    lab3, _ = ndi.label(weak, S8)
    S = np.isin(lab3, np.unique(lab3[B])) & ~B
    ref2 = np.maximum(ndi.maximum_filter(d, size=2*R + 1), cfg['floor'])
    s2 = np.clip((d - cfg['lo']) / (ref2 - cfg['lo']), 0, 1)
    alpha[S] = np.minimum(alpha, s2)[S]
    if SH.any():
        alpha[SH] = np.minimum(alpha, d / 255.0)[SH]
    sp = cfg.get('speck', 45)                                      # isolated compression specks off the mark
    if sp:
        lab4, n4 = ndi.label(alpha > 0, S8)
        if n4:
            mx = ndi.maximum(d, lab4, index=np.arange(1, n4 + 1))
            alpha[np.isin(lab4, np.nonzero(mx < sp)[0] + 1)] = 0
    alpha[alpha < 0.03] = 0
    aa = np.maximum(alpha, 1e-6)[..., None]
    rgb = np.clip(bg + (a - bg) / aa, 0, 255)                      # un-premultiply against the background colour
    rgb[alpha == 0] = 0
    return np.dstack([rgb, alpha * 255]).round().astype(np.uint8), cleared, bg

def keeta(a):
    a = a.astype(float); bg = bgcol(a); d = np.abs(a - bg).max(2)
    ink = np.median(a[d > 0.8 * d.max()], 0)                        # the wordmark's own black
    ref = np.abs(ink - bg).max()
    alpha = np.clip((d - 22) / (ref * 0.92 - 22), 0, 1)
    rgb = np.clip(bg + (a - bg) / np.maximum(alpha, 1e-6)[..., None], 0, 255)
    rgb[alpha > 0.5] = np.minimum(rgb[alpha > 0.5], a[alpha > 0.5] + 0)  # never lighter than source inside
    rgb[alpha == 0] = 0
    return np.dstack([rgb, alpha * 255]).round().astype(np.uint8), bg

def zero(a):
    a = a.astype(float); bg = bgcol(a)
    lum = a @ np.array([.2126, .7152, .0722]); l0 = bg @ np.array([.2126, .7152, .0722])
    l1 = np.percentile(lum, 99.9)
    alpha = np.clip((lum - l0 - 10) / (l1 - l0 - 14), 0, 1)
    out = np.zeros(a.shape[:2] + (4,), np.uint8); out[..., :3] = bg.round(); out[..., 3] = (alpha * 255).round()
    out[alpha == 0, :3] = 0
    return out, bg

def sheet(files, colour, path, cw=640, ch=470, pad=34, cols=6):
    rows = -(-len(files) // cols)
    S = Image.new('RGB', (cols * cw, rows * ch), colour); dr = ImageDraw.Draw(S)
    for i, f in enumerate(files):
        im = Image.open(f).convert('RGBA')
        s = min((cw - 2*pad) / im.width, (ch - 2*pad - 16) / im.height)
        im = im.convert('RGBa').resize((max(1, round(im.width*s)), max(1, round(im.height*s))),
                                       Image.LANCZOS if s < 1 else Image.BICUBIC).convert('RGBA')
        x = (i % cols) * cw + (cw - im.width) // 2; y = (i // cols) * ch + (ch - 16 - im.height) // 2
        S.paste(im, (x, y), im)
        dr.text(((i % cols) * cw + 6, (i // cols) * ch + ch - 14), os.path.basename(f)[:-4],
                fill=(128, 128, 128))
    S.save(path)

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for f in sorted(glob.glob(SRC + '/*.png')):
        name = os.path.basename(f); key = name.split('_')[0]
        a = np.array(Image.open(f).convert('RGB'))
        if key == 'new-03':
            o, bg = keeta(a); shutil.copyfile(f, OUT + '/new-03_keeta_on-yellow.png'); info = 'keyed against yellow'
        elif key == 'new-09':
            o, bg = zero(a); shutil.copyfile(f, OUT + '/new-09_zero_on-dark.png'); info = 'luminance -> alpha'
        else:
            o, n, bg = cut(a, CFG[key]); info = f'counters cleared: {n}'
        assert o.shape[:2] == a.shape[:2]
        Image.fromarray(o, 'RGBA').save(OUT + '/' + name, optimize=True)
        al = o[..., 3]
        print(f'{name:58s} bg={bg.round().astype(int)} transp={100*(al==0).mean():5.1f}% semi={100*((al>0)&(al<255)).mean():4.1f}% {info}')
    files = [f for f in sorted(glob.glob(OUT + '/*.png')) if '_on-' not in f]
    assert len(files) == 27
    sheet(files, (255, 255, 255), WORK + '/partners-transparent_on-white.png')
    sheet(files, (0x1F, 0x31, 0x62), WORK + '/partners-transparent_on-navy.png')
    for nm, sel in (('a', files[:9]), ('b', files[9:18]), ('c', files[18:])):   # enlarged checks, 3 per row
        sheet(sel, (0x1F, 0x31, 0x62), WORK + f'/partners-transparent_zoom-{nm}_on-navy.png', cw=660, ch=520, pad=20, cols=3)
