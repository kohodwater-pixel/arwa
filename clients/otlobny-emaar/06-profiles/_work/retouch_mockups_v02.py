#!/usr/bin/env python3
"""Retouched working copies of the client's four mockup images (draft v02).

Covers ONLY the small descriptor line under each «اطلبني» logo (old activity name, misspelt
"OTLOBY"/"OTLOBIY"/"OTLOBHY", garbled Arabic). The wordmark and everything else stay as supplied.
Method: each patch is a polygon; every pixel column inside it is re-filled by interpolating between
the surface just above and just below the patch (mode 'v'), or from the surface below only ('b'),
or along the row from left to right ('h'); fine grain matched to the neighbouring surface is added;
the patch is feathered into the image over 3 px. Vertical modes keep vertical seams (door gaps,
rear-door hinges) intact.

Sources are read from _originals/ and never written. Output: 06-profiles/assets/derived/mockup_*_retouched_v02.png
plus the truck-collage crops, and before/after zoom sheets in _work/retouch_v02/.
Run: python3 _work/retouch_mockups_v02.py
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

CLIENT = Path(__file__).resolve().parents[2]
SRC = CLIENT / '_originals'
OUT = CLIENT / '06-profiles/assets/derived'
CHK = CLIENT / '06-profiles/_work/retouch_v02'
OUT.mkdir(parents=True, exist_ok=True); CHK.mkdir(parents=True, exist_ok=True)

def R(l, t, r, b):
    return [(l, t), (r, t), (r, b), (l, b)]

# (polygon in source pixels, mode, where / reason) — coordinates measured on 3-4x zooms of each source
PATCHES = {
 'mockup_cleaning-team.png': [
  (R(323, 329, 356, 339), 'v', 'chest logo, worker 1: garbled descriptor line'),
  (R(532, 314, 579, 325), 'v', 'chest logo, worker 2: garbled descriptor line'),
  (R(752, 313, 804, 325), 'v', 'chest logo, worker 3: garbled descriptor line'),
  (R(958, 318, 999, 331), 'v', 'chest logo, worker 4: garbled descriptor line'),
  (R(1197, 324, 1250, 336), 'v', 'chest logo, worker 5: garbled descriptor line'),
  (R(1384, 656, 1470, 671), 'v', 'cleaning cart panel: garbled Arabic descriptor line'),
 ],
 'mockup_delivery-rider.png': [
  (R(453, 57, 496, 68), 'v', 'helmet logo: garbled descriptor line'),
  (R(499, 251, 540, 265), 'v', 'jacket chest logo: garbled descriptor lines'),
  (R(661, 297, 710, 320), 'v', 'delivery bag: garbled Arabic line and misspelt "OTLOBY ... Co." line'),
 ],
 'mockup_car-scooter-facade.png': [
  (R(160, 185, 352, 228), 'v', 'facade sign: «شركة لطليني اللصابة والنظافة» and "OTLOBIY Maintenance & Cleaning Co." (misspelt, old activity)'),
  (R(1253, 144, 1325, 159), 'v', 'street banner: descriptor line under the logo (garbled); the slogan «خدمتك بجودة تهمنا» is correct Arabic and kept'),
  (R(528, 660, 682, 695), 'v', 'car door: «شركة اطلبني اللصيانة والنظافة» and "OTLOBHY Maintenance & Cleaning Co." (misspelt, old activity)'),
  (R(1361, 514, 1459, 537), 'v', 'scooter top box: garbled Arabic line and "OTLOBHY Maintenance & Cleaning Co."'),
  ([(1222, 683), (1286, 663), (1288, 675), (1224, 696)], 'v', 'scooter side panel: slanted garbled descriptor lines'),
 ],
 'mockup_logistics-trucks.png': [
  (R(143, 355, 223, 378), 'v', 'view 1 cab front: «شركة اطلبني الخدمات اللوجستية» (garbled) and "OTLOBY Logistics Services Co."'),
  (R(357, 352, 402, 370), 'v', 'view 1 cab door: garbled descriptor lines'),
  (R(580, 292, 696, 335), 'v', 'view 1 box side: «شركة اطلبني الخدمات اللوجستية» and "OTLOBY Logistics Services Co." (misspelt)'),
  (R(986, 315, 1089, 359), 'v', 'view 2 box side: garbled Arabic and "OTLOBY Logistics Services Co."'),
  (R(1228, 293, 1383, 336), 'v', 'view 2 rear doors: descriptor lines (misspelt)'),
  (R(321, 795, 462, 831), 'v', 'view 3 box side: descriptor lines (misspelt)'),
  (R(64, 840, 111, 855), 'v', 'view 3 cab door: garbled descriptor line'),
  (R(850, 826, 933, 851), 'v', 'view 4 cab front: garbled descriptor lines'),
  (R(1234, 760, 1392, 798), 'v', 'view 5 rear doors: descriptor lines (misspelt)'),
 ],
}

FEATHER = 2

def logo_mask(a, kind):
    """Pixels that belong to the wordmark and must never be filled or used as a fill source."""
    rgb = a / 255.0
    mx, mn = rgb.max(2), rgb.min(2)
    sat = (mx - mn) / np.maximum(mx, 1e-3)
    blueish = (sat > 0.3) & (mx > 0.5) & (rgb[:, :, 2] + rgb[:, :, 1] > rgb[:, :, 0] * 1.6)
    if kind == 'bright':   # white wordmark on a dark panel
        return blueish | (mx > 0.62)
    return blueish

def patch(a, poly, mode, rng, logo_kind='blue'):
    h, w, _ = a.shape
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).polygon(poly, fill=255)
    rect = np.array(m) > 0
    ys, xs = np.nonzero(rect)
    pad = 12
    T, B, L, Rr = max(0, ys.min() - pad), min(h, ys.max() + pad + 1), max(0, xs.min() - pad), min(w, xs.max() + pad + 1)
    sub = a[T:B, L:Rr].copy()
    logo = logo_mask(sub, logo_kind)
    # protect only logo pixels connected to the area above/inside: grow by 1 px so its anti-aliased edge stays
    logo = np.array(Image.fromarray((logo * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))) > 0
    hole = rect[T:B, L:Rr] & ~logo
    hole = (np.array(Image.fromarray((hole * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3))) > 0) & ~logo
    usable = ~hole & ~logo
    wv, wh = (1.0, 0.12) if mode == 'v' else (1.0, 1.0)
    f = sub.copy()
    # start from the surface just below each column, then relax (masked anisotropic diffusion)
    for x in range(f.shape[1]):
        col = np.nonzero(hole[:, x])[0]
        if len(col):
            below = [y for y in range(col.max() + 1, min(f.shape[0], col.max() + 5)) if usable[y, x]]
            f[col, x] = sub[below, x].mean(0) if below else sub[usable].mean(0)
    src = usable.astype(float)
    for _ in range(600):
        acc = np.zeros_like(f); wt = np.zeros(f.shape[:2])
        for dy, dx, ww in ((1, 0, wv), (-1, 0, wv), (0, 1, wh), (0, -1, wh)):
            nb_ok = np.roll(np.roll(usable | hole, dy, 0), dx, 1).astype(float) * ww
            acc += np.roll(np.roll(f, dy, 0), dx, 1) * nb_ok[:, :, None]; wt += nb_ok
        upd = acc / np.maximum(wt, 1e-6)[:, :, None]
        f[hole] = upd[hole]
    ring = sub[usable].reshape(-1, 3)
    loc = np.array(Image.fromarray(sub.astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(float)
    sd = float(np.clip((sub - loc)[usable].std(), 0, 5))
    f[hole] += rng.normal(0, sd * .7, (hole.sum(), 1))
    alpha = np.array(Image.fromarray((hole * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(FEATHER * .5))).astype(float) / 255
    alpha[hole] = 1.0; alpha[logo] = 0.0
    a = a.copy()
    a[T:B, L:Rr] = sub * (1 - alpha[:, :, None]) + f * alpha[:, :, None]
    return a

def zoom_sheet(before, after, polys, name):
    tiles = []
    for poly in polys:
        xs = [p[0] for p in poly]; ys = [p[1] for p in poly]
        box = (max(0, min(xs) - 40), max(0, min(ys) - 30), min(before.width, max(xs) + 40), min(before.height, max(ys) + 30))
        sc = 4
        bw, bh = (box[2] - box[0]) * sc, (box[3] - box[1]) * sc
        t = Image.new('RGB', (bw * 2 + 10, bh), 'white')
        t.paste(before.crop(box).resize((bw, bh), Image.LANCZOS), (0, 0))
        t.paste(after.crop(box).resize((bw, bh), Image.LANCZOS), (bw + 10, 0))
        tiles.append(t)
    W = max(t.width for t in tiles); H = sum(t.height + 10 for t in tiles)
    s = Image.new('RGB', (W, H), 'white'); y = 0
    for t in tiles:
        s.paste(t, (0, y)); y += t.height + 10
    s.save(CHK / f'zoom_{name}.png')

def main():
    rng = np.random.default_rng(7)
    done = {}
    for fname, patches in PATCHES.items():
        im = Image.open(SRC / fname).convert('RGB')
        a = np.array(im).astype(float)
        for poly, mode, _ in patches:
            kind = 'bright' if (fname.startswith('mockup_cleaning') and poly[0][1] > 600) else 'blue'
            a = patch(a, poly, mode, rng, kind)
        res = Image.fromarray(np.clip(a, 0, 255).round().astype(np.uint8))
        stem = fname.rsplit('.', 1)[0]
        res.save(OUT / f'{stem}_retouched_v02.png', optimize=True)
        zoom_sheet(im, res, [p for p, _, _ in patches], stem)
        done[stem] = res
        print('retouched', fname, len(patches), 'patches')
    # truck collage: separate views; view 1 is cropped at x 700 so the Riyadh tower (x >= 703) is excluded
    trucks = done['mockup_logistics-trucks']
    crops = {'truck-front34': (0, 0, 700, 582), 'truck-rear34': (838, 0, 1536, 582),
             'truck-side': (0, 590, 668, 1024), 'truck-front': (672, 590, 1104, 1024), 'truck-rear': (1108, 590, 1536, 1024)}
    for k, box in crops.items():
        trucks.crop(box).save(OUT / f'mockup_{k}_retouched_v02.png', optimize=True)
        print('crop', k, box)

if __name__ == '__main__':
    main()
