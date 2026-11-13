#!/usr/bin/env python3
"""Round 2: icon v02 (three stacked band rows filling the square), bar-count re-test,
PNG 1x/2x/4x and vector PDF exports of the logo set."""
import glob
import io
import json
import os
import subprocess
import sys

import cairosvg
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_logo import SCHEMES, fmt, svg  # noqa: E402

LOGO = os.path.join(os.path.dirname(HERE), "02-logo")
WORK = os.path.join(LOGO, "_work")
SLUG = "demo-sidra-coffee"
PAPER, INK = "#F3ECE0", "#1F1B18"

# ---- icon v02: 205 x 205 units. Bar 25 wide, gap 5 (= 1/5 bar), 7 bars = 205.
# Three band rows, each 65 high (1:2.6), row gap 5: 3*65 + 2*5 = 205. Lit bars form the centre column.
SQ, BW, GAP, BH, ROWS = 205.0, 25.0, 5.0, 65.0, 3
for scheme, (_, cbar, clit) in SCHEMES.items():
    rects = []
    for r in range(ROWS):
        for i in range(7):
            c = clit if i == 3 else cbar
            rects.append(f'<rect x="{fmt(i * (BW + GAP))}" y="{fmt(r * (BH + GAP))}" width="{fmt(BW)}" height="{fmt(BH)}" fill="{c}"/>')
    fn = f"{SLUG}_logo_icon-{scheme}_ar-en_v02.svg"
    open(os.path.join(LOGO, fn), "w", encoding="utf-8").write(svg(SQ, SQ, "\n  ".join(rects), "Sidra Coffee — seven bars"))


def lum(px):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * c(px[0]) + 0.7152 * c(px[1]) + 0.0722 * c(px[2])


def render(path, size, bg=PAPER):
    im = Image.open(io.BytesIO(cairosvg.svg2png(url=path, output_width=size, output_height=size))).convert("RGBA")
    c = Image.new("RGBA", im.size, bg)
    c.alpha_composite(im)
    return c.convert("RGB")


def count(im, yf):
    y = min(im.height - 1, int(yf * im.height))
    row = [lum(im.getpixel((x, y))) for x in range(im.width)]
    bg, dark = max(row), min(row)
    thr = dark + 0.25 * (bg - dark)
    runs, inside = 0, False
    for v in row:
        if v < thr and not inside:
            runs, inside = runs + 1, True
        elif v >= thr:
            inside = False
    return runs


v1 = os.path.join(LOGO, f"{SLUG}_logo_icon-colour_ar-en_v01.svg")
v2 = os.path.join(LOGO, f"{SLUG}_logo_icon-colour_ar-en_v02.svg")
sm = os.path.join(LOGO, f"{SLUG}_logo_icon-small-colour_ar-en_v01.svg")
SIZES = [16, 24, 32, 41, 48, 64, 96]
report = {"method": "dark runs on one pixel row through the bars, Paper ground; a gap counts when it recovers 25% of the bar-to-ground range",
          "icon_v01_single_row_1to2": {}, "icon_v02_three_rows_1to2.6": {}}
for s in SIZES:
    report["icon_v01_single_row_1to2"][f"{s}px"] = count(render(v1, s), 0.5)
    report["icon_v02_three_rows_1to2.6"][f"{s}px"] = {"row1": count(render(v2, s), 0.16), "row2": count(render(v2, s), 0.5), "row3": count(render(v2, s), 0.84),
                                                      "gap_px": round(5 / 205 * s, 2)}
json.dump(report, open(os.path.join(WORK, "test_logo_icon-v02_bar-count.json"), "w"), indent=1)
print(json.dumps(report, indent=1))

# test sheet: v01, v02, small at each size, actual size and enlarged x6
Z = 6
sheet = Image.new("RGB", (sum(s * Z + 24 for s in SIZES) + 24, 3 * (96 * Z // 2 + 30) + 400), PAPER)
y = 16
for src in (v1, v2, sm):
    x = 24
    rowh = 0
    for s in SIZES:
        im = render(src, s)
        z = Z if s <= 48 else 3
        big = im.resize((s * z, s * z), Image.NEAREST)
        sheet.paste(big, (x, y))
        x += big.width + 24
        rowh = max(rowh, big.height)
    y += rowh + 24
sheet = sheet.crop((0, 0, sheet.width, y))
sheet.save(os.path.join(WORK, "test_logo_icon-v02_sizes.png"))

# ---- exports: PNG 1x/2x/4x (transparent) and vector PDF
PNG, PDF = os.path.join(LOGO, "png"), os.path.join(LOGO, "pdf")
os.makedirs(PNG, exist_ok=True)
os.makedirs(PDF, exist_ok=True)
superseded = {f"{SLUG}_logo_icon-{s}_ar-en_v01.svg" for s in SCHEMES}
n_png = n_pdf = 0
problems = []
for path in sorted(glob.glob(os.path.join(LOGO, "*.svg"))):
    base = os.path.basename(path)
    if base in superseded:
        continue
    head, lang, ver = base[:-4].rsplit("_", 2)
    for k in (1, 2, 4):
        out = os.path.join(PNG, f"{head}-{k}x_{lang}_{ver}.png")
        cairosvg.svg2png(url=path, write_to=out, scale=k)
        im = Image.open(out)
        if im.mode != "RGBA" or im.getchannel("A").getextrema()[0] != 0:
            problems.append(("not transparent", out))
        n_png += 1
    out = os.path.join(PDF, base[:-4] + ".pdf")
    cairosvg.svg2pdf(url=path, write_to=out)
    fonts = subprocess.run(["pdffonts", out], capture_output=True, text=True).stdout.strip().splitlines()[2:]
    imgs = subprocess.run(["pdfimages", "-list", out], capture_output=True, text=True).stdout.strip().splitlines()[2:]
    if fonts or imgs:
        problems.append(("pdf has fonts or raster images", out))
    n_pdf += 1
print("png:", n_png, "pdf:", n_pdf, "problems:", problems)

# spot-check sheet: a few PNG exports on a checkerboard plus PDFs rendered with pdftoppm
def checker(w, h, a=(200, 200, 200), b=(240, 240, 240), n=12):
    im = Image.new("RGB", (w, h), b)
    px = im.load()
    for yy in range(h):
        for xx in range(w):
            if (xx // n + yy // n) % 2:
                px[xx, yy] = a
    return im

picks = [f"{SLUG}_logo_primary-colour-2x_ar_v01.png", f"{SLUG}_logo_bilingual-white-2x_ar-en_v01.png",
         f"{SLUG}_logo_icon-colour-1x_ar-en_v02.png", f"{SLUG}_logo_latin-small-colour-reversed-1x_en_v01.png"]
tiles = []
for p in picks:
    im = Image.open(os.path.join(PNG, p)).convert("RGBA")
    c = checker(im.width + 40, im.height + 40).convert("RGBA")
    c.alpha_composite(im, (20, 20))
    tiles.append(c.convert("RGB"))
for p in [f"{SLUG}_logo_bilingual-colour_ar-en_v01.pdf", f"{SLUG}_logo_icon-colour-on-ember_ar-en_v02.pdf"]:
    stem = os.path.join(WORK, "_pdfcheck")
    subprocess.run(["pdftoppm", "-png", "-r", "144", "-singlefile", os.path.join(PDF, p), stem], check=True)
    im = Image.open(stem + ".png").convert("RGB")
    c = Image.new("RGB", (im.width + 40, im.height + 40), "#C23A20" if "ember" in p else "white")
    c.paste(im, (20, 20))
    tiles.append(c)
    os.remove(stem + ".png")
out = Image.new("RGB", (sum(t.width for t in tiles) + 10 * len(tiles), max(t.height for t in tiles)), "white")
x = 0
for t in tiles:
    out.paste(t, (x, 0))
    x += t.width + 10
out.save(os.path.join(WORK, "check_logo_exports_png-pdf.png"))
