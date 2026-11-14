"""v03: prepare the three TastySA partner logos (Shawarma Laila, Loomi, The End) for «شركاء النجاح».
Crop to artwork + even 8% transparent margin; The End downsampled to ~1400 px wide (premultiplied Lanczos);
Loomi: remove the 1-2 px bluish fringe on the OUTER edge only (opaque pixels touching transparency whose colour is
not the logo yellow). No redrawing, recolouring or sharpening. _originals are read only."""
from pathlib import Path
from PIL import Image
import numpy as np
from scipy import ndimage as ndi

C = Path(__file__).resolve().parents[2]
SRC = C / '_originals/partner-logos-tastysa_2026-11-14'
OUT = C / '06-profiles/assets/partners-transparent'
WK = C / '06-profiles/_work/partners_v03'; WK.mkdir(exist_ok=True)

def crop_margin(im, thr=8, m=0.08):
    a = np.array(im)[..., 3]
    ys, xs = np.where(a >= thr)
    l, t, r, b = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    art = im.crop((l, t, r, b))
    pad = round(m * max(art.size))
    can = Image.new('RGBA', (art.width + 2 * pad, art.height + 2 * pad), (0, 0, 0, 0))
    can.paste(art, (pad, pad))
    return can, (l, t, r, b), pad

def defringe_loomi(im, log):
    a = np.array(im).astype(np.int32)
    rgb, al = a[..., :3], a[..., 3]
    yellow = np.median(rgb[al == 255].reshape(-1, 3), 0)
    removed = 0
    for it in range(3):
        op = al > 0
        edge = op & ndi.binary_dilation(~op, structure=np.ones((3, 3)))     # opaque pixels touching transparency
        d = np.sqrt(((rgb - yellow) ** 2).sum(-1))
        blueish = (rgb[..., 2] > rgb[..., 0] - 40) & (d > 60)                 # fringe: blue-grey, far from the yellow
        kill = edge & blueish
        n = int(kill.sum())
        log.append(f'loomi defringe pass {it+1}: {n} edge pixels made transparent')
        if n == 0:
            break
        al[kill] = 0; removed += n
    # the 1-px boundary left after removal still carries a slight green-grey mix: soften those to half alpha (no colour change)
    op = al > 0
    edge = op & ndi.binary_dilation(~op, structure=np.ones((3, 3)))
    d = np.sqrt(((rgb - yellow) ** 2).sum(-1))
    soft = edge & (d > 35)
    al[soft] = 128
    log.append(f'loomi: {removed} fringe pixels removed in total; {int(soft.sum())} remaining off-colour boundary pixels set to 50% alpha; '
               f'interior (blue counters, letter edges against the counters) untouched; yellow ref {yellow.tolist()}')
    a[..., 3] = al
    return Image.fromarray(a.astype(np.uint8), 'RGBA')

log = []
jobs = [('layla-shawarma-logo-transparent', 'new-10_shawarma-laila'), ('loomi-logo-transparent', 'new-11_loomi'),
        ('the-end-logo-transparent', 'new-12_the-end')]
outs = []
for src, dst in jobs:
    im = Image.open(SRC / f'{src}.png').convert('RGBA')
    if src.startswith('loomi'):
        im = defringe_loomi(im, log)
    if src.startswith('the-end'):
        art, box, _ = crop_margin(im)
        art = art.crop((round(.08 * max(art.size)),) * 2 + (art.width - round(.08 * max(art.size)), art.height - round(.08 * max(art.size))))
        k = 1400 / art.width
        art = art.convert('RGBa').resize((1400, round(art.height * k)), Image.LANCZOS).convert('RGBA')
        im = art
        log.append(f'the-end: artwork bbox {box} in source, downsampled x{k:.3f} to {art.size}')
    out, box, pad = crop_margin(im)
    out.save(OUT / f'{dst}.png', optimize=True)
    log.append(f'{dst}.png <- {src}.png: artwork bbox {box}, margin {pad} px, final {out.size}')
    outs.append(out)

# check sheets: on white and on navy, plus 4x zooms of edges
for bg, name in (((255, 255, 255), 'white'), ((31, 49, 98), 'navy')):
    W = sum(o.width for o in outs) + 40 * 4; H = max(o.height for o in outs) + 80
    sh = Image.new('RGB', (W, H), bg); x = 40
    for o in outs:
        t = Image.new('RGBA', o.size, bg + (255,)); t.alpha_composite(o); sh.paste(t.convert('RGB'), (x, 40)); x += o.width + 40
    sh.save(WK / f'new-10-12_on-{name}.png')
for o, (src, dst) in zip(outs, jobs):
    t = Image.new('RGBA', o.size, (255, 255, 255, 255)); t.alpha_composite(o)
    w, h = o.size
    t.convert('RGB').crop((0, 0, min(w, 320), min(h, 220))).resize((min(w, 320) * 4, min(h, 220) * 4), Image.NEAREST).save(WK / f'{dst}_zoom4x_on-white.png')
(WK / 'prepare.log').write_text('\n'.join(log) + '\n')
print('\n'.join(log))
