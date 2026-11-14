#!/usr/bin/env python3
"""Retouched working copies of the client's four mockup images — draft v03.

Same patch areas as v02 (imported from retouch_mockups_v02.py, plus EXTRA below), new fill method so the surface
is even (v02's stroke-only diffusion left mottled patches on the car door and a smudge on the facade):
  1. hole = the whole measured patch area grown by GROW px, minus the wordmark pixels (protected, never filled);
  2. a smooth quadratic surface (per channel, robust least squares) is fitted to a ring of clean surrounding panel;
  3. vertical structure (door gaps, hinges, panel seams) is carried through: per column, the residual of the panel
     just above and just below the patch is interpolated across, but only where above and below agree;
  4. fine grain matched to the high-frequency noise of the ring is added; the edge is feathered 2 px outward.
Sources are read from _originals/ and never written. Output: assets/derived/mockup_*_retouched_v03.png (+ truck crops)
and before/after 4x sheets in _work/retouch_v03/. Run: python3 _work/retouch_mockups_v03.py
"""
import importlib.util
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('r2', HERE / 'retouch_mockups_v02.py'); r2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r2)
CLIENT = r2.CLIENT; SRC = r2.SRC; OUT = r2.OUT
CHK = CLIENT / '06-profiles/_work/retouch_v03'; CHK.mkdir(parents=True, exist_ok=True)
R = r2.R

PATCHES = {k: list(v) for k, v in r2.PATCHES.items()}
EXTRA = {          # added after viewing the first v03 sheets
 'mockup_car-scooter-facade.png': [
  ([(236, 238), (318, 244), (318, 253), (236, 247)], 'f', 'facade sign: soft shadow line of the old Latin letters just below the v02 area'),
 ]}
ROBUST_OFF = {(453, 57), (1222, 683)}   # glossy helmet / scooter: highlights are part of the surface
# view 4 cab front: keep the area clear of the grille below it
PATCHES['mockup_logistics-trucks.png'] = [((R(850, 826, 933, 848), m, w) if p[0] == (850, 826) else (p, m, w)) for p, m, w in PATCHES['mockup_logistics-trucks.png']]
# cart panel: v02's area (1384,656-1470,671) also covered the lower bowl and dots of the white «اطلبني» on the cart and
# removed them (found in v03 at 6x). v03 limits the area to the descriptor letters only, right of and below the wordmark.
PATCHES['mockup_cleaning-team.png'] = [((R(1406, 660, 1468, 670), m, w + ' (v03: narrowed to spare the wordmark)') if p[0] == (1384, 656) else (p, m, w)) for p, m, w in PATCHES['mockup_cleaning-team.png']]
GROW_PATCH = {(1406, 660): 1, (528, 655): 1}       # car door: do not grow towards the sill crease
GRAIN_PATCH = {(1222, 683): 0.35}  # scooter side: glossy panel, very little grain
for k, v in EXTRA.items():
    PATCHES[k] += v
GROW = 2

def dil(m, px):
    return np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(2 * px + 1))) > 0

def fit_surface(sub, ring, shape):
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w]; xx = xx / w - .5; yy = yy / h - .5
    A = np.stack([np.ones_like(xx), xx, yy, xx * xx, xx * yy], -1)
    Ar = A[ring]; out = np.zeros((h, w, 3))
    for c in range(3):
        z = sub[..., c][ring]; keep = np.ones(len(z), bool)
        for _ in range(3):
            M = Ar[keep]
            coef = np.linalg.solve(M.T @ M + 1e-6 * np.eye(5), M.T @ z[keep])
            res = z - Ar @ coef; s = res[keep].std() + 1e-6
            keep = np.abs(res) < 2.2 * s
        out[..., c] = A @ coef
    return out

def patch(a, poly, mode, rng, logo_kind='blue'):
    H, W, _ = a.shape
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    rect = np.array(m) > 0
    ys, xs = np.nonzero(rect); pad = 16
    T, B, L, Rr = max(0, ys.min() - pad), min(H, ys.max() + pad + 1), max(0, xs.min() - pad), min(W, xs.max() + pad + 1)
    sub = a[T:B, L:Rr].copy(); rc = rect[T:B, L:Rr]
    logo = dil(r2.logo_mask(sub, logo_kind), 1)
    if logo_kind == 'bright':      # white wordmark on the cart: protect its large shapes, the small descriptor letters go
        from scipy import ndimage as ndi
        br = sub.max(2) > 150; lb, _ = ndi.label(br); cnt = np.bincount(lb.ravel())
        logo = dil(np.isin(lb, [i for i, c in enumerate(cnt) if i and c > 150]), 1)
    if mode == 'f':
        logo |= dil((sub[..., 2] - sub[..., 0] > 14) & (sub[..., 2] > sub[..., 1]), 1)
    region = dil(rc, GROW_PATCH.get(tuple(poly[0]), GROW + (1 if mode == 'f' else 0)))
    hole = region & ~logo
    lum = sub.mean(2)
    med = np.array(Image.fromarray(lum.astype(np.uint8)).filter(ImageFilter.MedianFilter(9))).astype(float)
    ring = dil(region, 9) & ~dil(region, 1) & ~dil(logo, 3) & (np.abs(lum - med) < 14)
    if tuple(poly[0]) not in ROBUST_OFF and ring.sum() > 30:
        mv0 = np.median(lum[ring]); mad0 = 1.4826 * np.median(np.abs(lum[ring] - mv0))
        r2_ = ring & (np.abs(lum - mv0) < 2.5 * mad0 + 8)
        if r2_.sum() > 30:
            ring = r2_
        # columns where the panel ends (background beyond the object's edge) are not filled
        nr = dil(region, 4) & ~dil(region, 1)
        for x in range(sub.shape[1]):
            c = nr[:, x] & ~logo[:, x]
            if c.any() and np.all(np.abs(lum[c, x] - mv0) > 3 * mad0 + 40):
                region[:, x] = False
        hole = region & ~logo
    top = np.nonzero(region.any(1))[0].min()
    fr = ring.copy(); fr[:top] = False                 # the wordmark sits above every patch: fit from the sides and below
    if fr.sum() >= 60:
        ring_fit = fr
    else:
        ring_fit = ring
    if ring.sum() < 40:
        ring = dil(region, 9) & ~dil(region, 1) & ~dil(logo, 2)
    poly_fit = fit_surface(sub, ring_fit if ring.sum() >= 40 else ring, lum.shape)
    # membrane (Laplace) fill: the hole is a smooth surface that meets the surrounding panel everywhere; the boundary
    # values are a masked Gaussian average of CLEAN panel pixels (no wordmark, no remnant fringe), so nothing mottled
    # is propagated inward; wordmark pixels are a no-flux boundary (no blue bleeds in)
    clean = dil(region, 5) & ~region & ~dil(logo, 3) & (np.abs(lum - med) < 14)
    if clean.sum() > 30 and tuple(poly[0]) not in ROBUST_OFF:   # robust: drop grille edges, logo halo, shadows from the boundary
        mv = np.median(lum[clean]); mad = 1.4826 * np.median(np.abs(lum[clean] - mv))
        clean &= np.abs(lum - mv) < 2.5 * mad + 8
    def mblur(img, m, sg):
        num = np.stack([np.array(Image.fromarray(np.clip(img[..., c] * m, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sg))).astype(float) for c in range(3)], -1)
        den = np.array(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(sg))).astype(float)[..., None] / 255
        return np.where(den > 0.02, num / np.maximum(den, 1e-3), poly_fit)
    Cb = mblur(sub, clean, 2.0)
    surf = np.where(hole[..., None], poly_fit, Cb)
    fixed = ~hole & ~logo
    for _ in range(2500):
        acc = np.zeros_like(surf); wt = np.zeros(lum.shape)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ok = np.roll(np.roll(hole | fixed, dy, 0), dx, 1).astype(float)
            acc += np.roll(np.roll(surf, dy, 0), dx, 1) * ok[..., None]; wt += ok
        upd = acc / np.maximum(wt, 1e-6)[..., None]
        surf[hole] = upd[hole]
    fill = surf.copy()
    # vertical structure carried through where the panel above and below agree
    resid = sub - Cb
    near = dil(region, 6) & ~dil(region, 2) & ~dil(logo, 2)
    off = {}
    if mode in ('v', 'f', 'i'):
        for x in range(sub.shape[1]):
            col = np.nonzero(hole[:, x])[0]
            if not len(col):
                continue
            up = [y for y in range(0, col.min()) if near[y, x]]
            dn = [y for y in range(col.max() + 1, sub.shape[0]) if near[y, x]]
            if not up or not dn:
                continue
            off[x] = (resid[up, x].mean(0), resid[dn, x].mean(0), col)
        xs_ = sorted(off)
        if xs_:
            OA = np.array([off[x][0] for x in xs_]); OB = np.array([off[x][1] for x in xs_])
            k = np.ones(15) / 15
            sm = lambda M: np.stack([np.convolve(np.pad(M[:, c], 7, mode='edge'), k, 'valid') for c in range(3)], 1)
            OA, OB = OA - sm(OA), OB - sm(OB)
            for i, x in enumerate(xs_):
                oa, ob, col = OA[i], OB[i], off[x][2]
                la, lb = oa.mean(), ob.mean()
                if np.sign(la) == np.sign(lb) and min(abs(la), abs(lb)) > 6:
                    fill[col, x] += (oa if abs(la) < abs(lb) else ob)[None]   # constant per column: no gradient blocks
    # grain matched to the ring
    hp = sub - np.array(Image.fromarray(np.clip(sub, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(float)
    sd = np.clip(1.4826 * np.median(np.abs(hp[ring] - np.median(hp[ring], 0)), 0), 0.3, 3.0)
    n = rng.normal(0, 1, lum.shape)
    n = np.array(Image.fromarray(((n * 40) + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.7))).astype(float) - 128
    n /= (n.std() + 1e-6)
    fill += n[..., None] * sd.mean() * 0.6 * GRAIN_PATCH.get(tuple(poly[0]), 1.0) / 0.6 * 0.6
    alpha = np.array(Image.fromarray((hole * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(float) / 255
    alpha[hole] = 1.0; alpha[logo] = 0.0
    a = a.copy()
    a[T:B, L:Rr] = sub * (1 - alpha[..., None]) + fill * alpha[..., None]
    return a

def despeck(a, poly, logo_kind, log, fname):
    from scipy import ndimage as ndi
    xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
    L, T, Rr, B = max(0, min(xs) - 20), max(0, min(ys) - 14), min(a.shape[1], max(xs) + 20), min(a.shape[0], max(ys) + 14)
    sub = a[T:B, L:Rr]; lum = sub.mean(2)
    med = np.array(Image.fromarray(lum.clip(0, 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(11))).astype(float)
    lg = r2.logo_mask(sub, 'blue'); ll, _ = ndi.label(lg)
    big = np.isin(ll, [i for i, c in enumerate(np.bincount(ll.ravel())) if i and c > 40])
    pm = Image.new('L', (Rr - L, B - T), 0); ImageDraw.Draw(pm).polygon([(x - L, y - T) for x, y in poly], fill=255)
    zone = dil(np.array(pm) > 0, 6)                                   # only inside the patch area (+6 px)
    smooth = ndi.generic_filter(med, np.std, size=9) < 6               # on an even surface, not on detail
    cand = (np.abs(lum - med) > 18) & ~dil(big, 2) & zone & smooth
    lab, n = ndi.label(cand)
    boxes = []
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        hgt, wid = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        area = int((lab[sl] == i).sum())
        if area <= 30 and hgt <= 7 and wid <= 7:
            m = dil(lab == i, 2)
            medrgb = np.stack([np.array(Image.fromarray(sub[..., c].clip(0, 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(11))) for c in range(3)], -1).astype(float)
            sub[m] = medrgb[m]
            boxes.append((L + sl[1].start - 2, T + sl[0].start - 2, L + sl[1].stop + 2, T + sl[0].stop + 2))
    if boxes:
        log.append(f'  {fname}: {len(boxes)} isolated speck(s) near patch at {poly[0]} filled from local median: {boxes}')
    a[T:B, L:Rr] = sub
    return boxes

def zoom_sheet(before, after, polys, name, sc=4):
    tiles = []
    for poly in polys:
        xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
        box = (max(0, min(xs) - 30), max(0, min(ys) - 22), min(before.width, max(xs) + 30), min(before.height, max(ys) + 22))
        bw, bh = (box[2] - box[0]) * sc, (box[3] - box[1]) * sc
        t = Image.new('RGB', (bw * 2 + 10, bh), 'white')
        t.paste(before.crop(box).resize((bw, bh), Image.LANCZOS), (0, 0)); t.paste(after.crop(box).resize((bw, bh), Image.LANCZOS), (bw + 10, 0))
        tiles.append(t)
    Wd = max(t.width for t in tiles); Hd = sum(t.height + 10 for t in tiles)
    s = Image.new('RGB', (Wd, Hd), 'white'); y = 0
    for t in tiles:
        s.paste(t, (0, y)); y += t.height + 10
    s.save(CHK / f'zoom_{name}.png')

def main():
    rng = np.random.default_rng(11); done = {}; log = []
    for fname, patches in PATCHES.items():
        im = Image.open(SRC / fname).convert('RGB'); a = np.array(im).astype(float)
        for poly, mode, _ in patches:
            kind = 'bright' if (fname.startswith('mockup_cleaning') and poly[0][1] > 600) else 'blue'
            a = patch(a, poly, mode, rng, kind)
        specks = []
        for poly, mode, _ in patches:
            if fname.startswith('mockup_cleaning') and poly[0][1] > 600:
                continue
            specks += despeck(a, poly, 'blue', log, fname)
        res = Image.fromarray(np.clip(a, 0, 255).round().astype(np.uint8))
        stem = fname.rsplit('.', 1)[0]
        res.save(OUT / f'{stem}_retouched_v03.png', optimize=True)
        zoom_sheet(im, res, [p for p, _, _ in patches], stem)
        allow = Image.new('L', im.size, 0); dr = ImageDraw.Draw(allow)
        for poly, _, _ in patches:
            dr.polygon(poly, fill=255)
        for bx in specks:
            dr.rectangle(bx, fill=255)
        allow = np.array(allow.filter(ImageFilter.MaxFilter(2 * 6 + 1))) > 0
        diff = np.abs(np.array(res).astype(int) - np.array(im).astype(int)).max(2)
        logo_all = r2.logo_mask(np.array(im).astype(float), 'blue')
        line = (f'{fname}: {len(patches)} patches | px changed outside patch masks (+6 px): {int(((diff > 0) & ~allow).sum())} '
                f'| wordmark px changed: {int(((diff > 0) & logo_all & ~allow).sum())} outside masks, '
                f'{int(((diff > 2) & logo_all & allow).sum())} inside masks (>2 levels)')
        print(line); log.append(line); done[stem] = res
    trucks = done['mockup_logistics-trucks']
    crops = {'truck-front34': (0, 0, 700, 582), 'truck-rear34': (838, 0, 1536, 582),
             'truck-side': (0, 590, 668, 1024), 'truck-front': (672, 590, 1104, 1024), 'truck-rear': (1108, 590, 1536, 1024)}
    for k, box in crops.items():
        trucks.crop(box).save(OUT / f'mockup_{k}_retouched_v03.png', optimize=True)
    (CHK / 'run.log').write_text('\n'.join(log) + '\n')

if __name__ == '__main__':
    main()
