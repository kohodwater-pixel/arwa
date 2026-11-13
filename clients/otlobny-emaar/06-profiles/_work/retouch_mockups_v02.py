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
  (R(958, 318, 1004, 332), 'v', 'chest logo, worker 4: garbled descriptor line'),
  (R(1197, 324, 1250, 336), 'v', 'chest logo, worker 5: garbled descriptor line'),
  (R(1384, 656, 1470, 671), 'v', 'cleaning cart panel: garbled Arabic descriptor line'),
 ],
 'mockup_delivery-rider.png': [
  (R(453, 57, 496, 68), 'v', 'helmet logo: garbled descriptor line'),
  (R(499, 251, 540, 265), 'v', 'jacket chest logo: garbled descriptor lines'),
  (R(661, 297, 710, 320), 'v', 'delivery bag: garbled Arabic line and misspelt "OTLOBY ... Co." line'),
 ],
 'mockup_car-scooter-facade.png': [
  ([(160, 185), (352, 200), (354, 246), (160, 230)], 'v', 'facade sign: «شركة لطليني اللصابة والنظافة» and "OTLOBIY Maintenance & Cleaning Co." (misspelt, old activity)'),
  (R(316, 234, 358, 252), 'i', 'facade sign: tail of the old Latin line ("...ing Co.") under the perspective'),
  (R(1253, 144, 1325, 159), 'v', 'street banner: descriptor line under the logo (garbled); the slogan «خدمتك بجودة تهمنا» is correct Arabic and kept'),
  (R(528, 655, 682, 696), 'i', 'car door: «شركة اطلبني اللصيانة والنظافة» and "OTLOBHY Maintenance & Cleaning Co." (misspelt, old activity)'),
  (R(1361, 514, 1459, 537), 'v', 'scooter top box: garbled Arabic line and "OTLOBHY Maintenance & Cleaning Co."'),
  ([(1222, 683), (1286, 663), (1288, 675), (1224, 696)], 'v', 'scooter side panel: slanted garbled descriptor lines'),
 ],
 'mockup_logistics-trucks.png': [
  (R(143, 355, 223, 378), 'v', 'view 1 cab front: «شركة اطلبني الخدمات اللوجستية» (garbled) and "OTLOBY Logistics Services Co."'),
  (R(357, 352, 402, 370), 'v', 'view 1 cab door: garbled descriptor lines'),
  (R(580, 292, 696, 335), 'v', 'view 1 box side: «شركة اطلبني الخدمات اللوجستية» and "OTLOBY Logistics Services Co." (misspelt)'),
  (R(986, 315, 1089, 364), 'v', 'view 2 box side: garbled Arabic and "OTLOBY Logistics Services Co."'),
  (R(1040, 344, 1066, 362), 'i', 'view 2 box side: two leftover dots of the old Latin line'),
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
    if logo_kind == 'bright':   # the wrong line is white too: inside the patch nothing is protected
        logo &= ~rect[T:B, L:Rr]
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
    f[hole] += rng.normal(0, sd * .35, (hole.sum(), 1))
    alpha = np.array(Image.fromarray((hole * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(FEATHER * .5))).astype(float) / 255
    alpha[hole] = 1.0; alpha[logo] = 0.0
    a = a.copy()
    a[T:B, L:Rr] = sub * (1 - alpha[:, :, None]) + f * alpha[:, :, None]
    return a

# Correct descriptor composited where the old line sat on a flat surface (Creative Director, client answer 3).
# Taken from the proposed lockup (04-identity/02-logo, white version): «شركة اطلبني إعمار» over "OTLOBNY Emaar Co.",
# shaped Arabic as vector paths, rendered with cairosvg. Box = (left, top, right, bottom) the new descriptor is fitted into,
# right-aligned and top-aligned as the old line was; colour matched to the scene.
LOCKUP = CLIENT / '04-identity/02-logo/otlobny-emaar_logo_lockup-proposal-white_ar-en_v01.svg'
WHITE, NAVYGREY = (226, 230, 238), (52, 60, 82)
COMPOSITES = {
 'mockup_cleaning-team.png': [((1388, 657, 1463, 671), WHITE, 'cleaning cart panel')],
 'mockup_delivery-rider.png': [((664, 299, 709, 320), WHITE, 'delivery bag side panel')],
 'mockup_car-scooter-facade.png': [((166, 188, 338, 226), WHITE, 'facade sign', 0.085), ((536, 663, 676, 694), NAVYGREY, 'car door'),
                                   ((1366, 517, 1454, 537), WHITE, 'scooter top box')],
 'mockup_logistics-trucks.png': [((586, 296, 692, 334), WHITE, 'view 1 box side'), ((988, 318, 1086, 358), WHITE, 'view 2 box side'),
                                 ((1233, 296, 1380, 334), WHITE, 'view 2 rear doors'), ((326, 798, 458, 830), WHITE, 'view 3 box side'),
                                 ((1238, 763, 1388, 797), WHITE, 'view 5 rear doors')],
}

def descriptor_alpha():
    import cairosvg, io
    W = 4924   # 4x the 1231 px test render; the descriptor block is x 600-1231, y 395-520 there
    im = Image.open(io.BytesIO(cairosvg.svg2png(url=str(LOCKUP), output_width=W))).getchannel('A')
    k = W / 1231
    crop = im.crop((int(600 * k), int(394 * k), W, im.height))
    return crop.crop(crop.getbbox())

def composite(res, box, colour, alpha_hi, shear=0.0):
    l, t, r, b = box
    s = min((r - l) / alpha_hi.width, (b - t) / alpha_hi.height)
    w, h = max(1, round(alpha_hi.width * s)), max(1, round(alpha_hi.height * s))
    al = alpha_hi.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.35))
    al = al.point(lambda v: int(v * 0.94))
    if shear:   # follow the sign's perspective: the line drops towards the right
        h2 = h + int(round(shear * w)) + 1
        al = al.transform((w, h2), Image.AFFINE, (1, 0, 0, -shear, 1, 0), resample=Image.BICUBIC)
        h = h2
    layer = Image.new('RGB', (w, h), colour)
    res.paste(layer, (r - w, t), al)
    return (r - w, t, r, t + h)

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
    global ALPHA
    ALPHA = descriptor_alpha()
    rng = np.random.default_rng(7)
    done = {}
    for fname, patches in PATCHES.items():
        im = Image.open(SRC / fname).convert('RGB')
        a = np.array(im).astype(float)
        for poly, mode, _ in patches:
            kind = 'bright' if (fname.startswith('mockup_cleaning') and poly[0][1] > 600) else 'blue'
            a = patch(a, poly, mode, rng, kind)
        res = Image.fromarray(np.clip(a, 0, 255).round().astype(np.uint8))
        for c in COMPOSITES.get(fname, []):
            box, colour, where = c[:3]
            got = composite(res, box, colour, ALPHA, c[3] if len(c) > 3 else 0.0)
            print('  composite', where, 'at', got)
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
