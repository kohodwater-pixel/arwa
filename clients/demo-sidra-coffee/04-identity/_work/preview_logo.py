#!/usr/bin/env python3
"""PNG previews and the 16 px / 10 mm tests for the logo set."""
import io
import json
import os

import cairosvg
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(os.path.dirname(HERE), "02-logo")
WORK = os.path.join(LOGO, "_work")
os.makedirs(WORK, exist_ok=True)
M = json.load(open(os.path.join(HERE, "logo-metrics.json")))
F, MT = M["files"], M["metrics"]
PAPER, CREMA, INK, EMBER = "#F3ECE0", "#E3C9A0", "#1F1B18", "#C23A20"


def render(key, height=None, width=None):
    kw = {}
    if height:
        kw["output_height"] = height
    if width:
        kw["output_width"] = width
    png = cairosvg.svg2png(url=os.path.join(LOGO, F[key]), **kw)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def on(bg, im, pad):
    c = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), bg)
    c.alpha_composite(im, (pad, pad))
    return c


def sheet(name, rows, bgs, h=150, pad=60):
    """rows: list of lists of keys; each row drawn on its background."""
    tiles = []
    for keys, bg in zip(rows, bgs):
        ims = [on(bg, render(k, height=h), pad) for k in keys]
        row = Image.new("RGBA", (sum(i.width for i in ims), max(i.height for i in ims)), bg)
        x = 0
        for i in ims:
            row.paste(i, (x, 0))
            x += i.width
        tiles.append(row)
    W = max(t.width for t in tiles)
    out = Image.new("RGB", (W, sum(t.height for t in tiles)), "white")
    y = 0
    for t, bg in zip(tiles, bgs):
        out.paste(Image.new("RGB", (W, t.height), bg), (0, y))
        out.paste(t.convert("RGB"), (0, y))
        y += t.height
    out.save(os.path.join(WORK, name))
    return out


L = ["primary", "bilingual", "latin", "icon"]
LANG = {"primary": "ar", "bilingual": "ar-en", "latin": "en", "icon": "ar-en"}
k = lambda l, s, small="": f"{l}{small}-{s}_{LANG[l]}"

sheet("preview_logo_all-versions.png",
      [[k(l, "colour") for l in L], [k(l, "colour") for l in L], [k(l, "colour-reversed") for l in L],
       [k(l, "colour-on-ember") for l in L], [k(l, "black") for l in L], [k(l, "white") for l in L]],
      [PAPER, CREMA, INK, EMBER, "#FFFFFF", "#000000"])
sheet("preview_logo_small-fallback.png",
      [[k(l, "colour", "-small") for l in L], [k(l, "colour-reversed", "-small") for l in L],
       [k(l, "black", "-small") for l in L]], [PAPER, INK, "#FFFFFF"])
sheet("preview_logo_primary-large.png", [[k("primary", "colour")], [k("bilingual", "colour")]], [PAPER, CREMA], h=420, pad=120)


def lum(px):
    def c(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * c(px[0]) + 0.7152 * c(px[1]) + 0.0722 * c(px[2])


def count_bars(im_rgb, y_frac):
    """Count dark runs along the pixel row at y_frac of the image height.
    A gap counts when it recovers at least 25% of the way from bar to background."""
    y = min(im_rgb.height - 1, int(y_frac * im_rgb.height))
    row = [lum(im_rgb.getpixel((x, y))) for x in range(im_rgb.width)]
    bg, dark = max(row), min(row)
    thr = dark + 0.25 * (bg - dark)
    runs, inside = 0, False
    for v in row:
        if v < thr and not inside:
            runs, inside = runs + 1, True
        elif v >= thr:
            inside = False
    return runs


report = {}
tests = []
for label, px_h in [("16px-high", 16), ("24px-high", 24), ("32px-high", 32), ("48px-high", 48)]:
    for l in L:
        for small in ("", "-small"):
            for scheme, bg in (("colour", PAPER), ("colour-reversed", INK)):
                im = render(k(l, scheme, small), height=px_h)
                flat = on(bg, im, 0).convert("RGB")
                if l == "icon":
                    yf = 0.5
                elif l == "primary":
                    yf = (MT["bars_y"] + MT["bar_h"] / 2) / MT["primary_height"]
                elif l == "bilingual":
                    yf = (MT["bars_y"] + MT["bar_h"] / 2) / MT["bilingual_height"]
                else:
                    yf = 1 - (MT["bar_h"] / 2) / MT["latin_height"]
                n = count_bars(flat, yf) if not small and scheme == "colour" else None
                if n is not None:
                    report[f"{l} {label} ({flat.width}x{flat.height}px)"] = n
                if scheme == "colour" or small == "":
                    tests.append((label, l, small, scheme, bg, flat))

# 16 px test sheet: actual size and 10x nearest-neighbour enlargement
for label in ("16px-high", "24px-high", "32px-high"):
    sel = [t for t in tests if t[0] == label and t[3] == "colour"]
    Z = 10
    Wt = sum(t[5].width * Z + 30 for t in sel) + 30
    Ht = max(t[5].height for t in sel) * Z + 90
    out = Image.new("RGB", (Wt, Ht), PAPER)
    x = 30
    for t in sel:
        im = t[5]
        out.paste(im, (x, 20))
        out.paste(im.resize((im.width * Z, im.height * Z), Image.NEAREST), (x, 60))
        x += im.width * Z + 30
    out.save(os.path.join(WORK, f"test_logo_{label}_x10.png"))

# reversed at 16 px
sel = [t for t in tests if t[0] == "16px-high" and t[3] == "colour-reversed"]
Z = 10
out = Image.new("RGB", (sum(t[5].width * Z + 30 for t in sel) + 30, 16 * Z + 60), INK)
x = 30
for t in sel:
    out.paste(t[5].resize((t[5].width * Z, t[5].height * Z), Image.NEAREST), (x, 30))
    x += t[5].width * Z + 30
out.save(os.path.join(WORK, "test_logo_16px-high_reversed_x10.png"))

# 10 mm wide in print, simulated at 600 dpi (236 px), shown enlarged x4; black and reversed
mm10 = round(10 / 25.4 * 600)
ims = [on("#FFFFFF", render(k("primary", "black"), width=mm10), 40),
       on("#FFFFFF", render(k("bilingual", "black"), width=mm10), 40),
       on("#000000", render(k("primary", "white"), width=mm10), 40),
       on(PAPER, render(k("primary", "colour"), width=mm10), 40),
       on(PAPER, render(k("icon", "colour"), width=mm10), 40)]
out = Image.new("RGB", (sum(i.width for i in ims), max(i.height for i in ims)), "white")
x = 0
for i in ims:
    out.paste(i.convert("RGB"), (x, 0))
    x += i.width
out = out.resize((out.width * 3, out.height * 3), Image.NEAREST)
out.save(os.path.join(WORK, "test_logo_10mm-wide_600dpi_x3.png"))

json.dump(report, open(os.path.join(WORK, "test_logo_bar-count.json"), "w"), indent=1)
print(json.dumps(report, indent=1))
print("bar gap px at 16px-high primary:", round(MT["bar_gap"] * 16 / MT["primary_height"], 2))
