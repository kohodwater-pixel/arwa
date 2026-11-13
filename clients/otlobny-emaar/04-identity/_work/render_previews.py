#!/usr/bin/env python3
"""Render PNG previews of the logo SVGs into 02-logo/_work/ (work files, not deliverables)."""
import glob, io, os
import cairosvg
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); LOGO = os.path.join(HERE, "..", "02-logo"); W = os.path.join(LOGO, "_work")
os.makedirs(W, exist_ok=True)
NAVY, BLUE = (0x1F, 0x31, 0x62), (0x37, 0x58, 0xB0)
def render(svg, width, bg):
    im = Image.open(io.BytesIO(cairosvg.svg2png(url=svg, output_width=width))).convert("RGBA")
    pad = int(width * 0.09)
    c = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), bg + (255,)); c.alpha_composite(im, (pad, pad))
    return c.convert("RGB")
tiles = {}
for f in sorted(glob.glob(os.path.join(LOGO, "*.svg"))):
    base = os.path.basename(f)[:-4]
    scheme = base.split("_")[2].split("-")[-1]
    bgs = {"colour": [("white", (255, 255, 255))], "navy": [("white", (255, 255, 255))],
           "reversed": [("navy", NAVY)], "white": [("navy", NAVY), ("blue", BLUE)]}[scheme]
    for name, bg in bgs:
        im = render(f, 1400, bg); im.save(os.path.join(W, f"{base}_on-{name}.png")); tiles[(base, name)] = im
for kind in ("wordmark", "lockup-proposal"):
    sel = [(k, v) for k, v in tiles.items() if f"_{kind}-" in k[0]]
    w = 700; ims = [v.resize((w, int(v.height * w / v.width))) for _, v in sel]
    h = max(i.height for i in ims); cols = 2; rows = (len(ims) + 1) // 2
    sheet = Image.new("RGB", (cols * w, rows * h), (200, 200, 200))
    for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(os.path.join(W, f"sheet_{kind}_all-versions.png"))
small = Image.new("RGB", (1700, 520), (255, 255, 255)); x = 20
for kind in ("wordmark-colour_ar", "lockup-proposal-colour_ar-en", "wordmark-navy_ar"):
    f = glob.glob(os.path.join(LOGO, f"*_{kind}_v01.svg"))[0]
    for hpx in (16, 28, 57, 113):   # 10 mm high = 28 px at 72 dpi, 57 px at 144 dpi, 113 px at 288 dpi
        im = Image.open(io.BytesIO(cairosvg.svg2png(url=f, output_height=hpx))).convert("RGBA")
        bgim = Image.new("RGBA", im.size, (255, 255, 255, 255)); bgim.alpha_composite(im); bgim = bgim.convert("RGB")
        small.paste(bgim, (x, 20))
        z = bgim.resize((im.width * 4, im.height * 4), Image.NEAREST) if hpx <= 28 else None
        if z: small.paste(z, (x, 160))
        x += max(im.width, z.width if z else 0) + 20
small.save(os.path.join(W, "test_small-sizes_16px-and-10mm.png"))
o1 = Image.open(os.path.join(HERE, "p01-logo-crop-01.png")).convert("RGB"); o20 = Image.open(os.path.join(HERE, "p20-logo-crop-20.png")).convert("RGB")
def fit(im, w): return im.resize((w, int(im.height * w / im.width)))
def tile(s): return tiles[[k for k in tiles if s in k[0]][0]]
a = fit(o1, 950); b = fit(tile("wordmark-colour"), 950); c = fit(o20, 950); d = fit(tile("wordmark-reversed"), 950)
r1 = max(a.height, b.height)
sheet = Image.new("RGB", (1900, r1 + max(c.height, d.height)), (128, 128, 128))
sheet.paste(a, (0, 0)); sheet.paste(b, (950, 0)); sheet.paste(c, (0, r1)); sheet.paste(d, (950, r1))
sheet.save(os.path.join(W, "compare_original-left_extracted-right.png"))
print("ok", len(tiles))
