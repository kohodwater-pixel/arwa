#!/usr/bin/env python3
"""Contact sheet from still PNGs: python3 sheet.py <out.jpg> <cols> <thumb-width> <png> [<png> ...]  (label = time from file name)"""
import sys, os, re
from PIL import Image, ImageDraw, ImageFont
out, cols, tw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); files = sys.argv[4:]
th = round(tw * 1920 / 1080); pad = 14; lab = 34
rows = -(-len(files) // cols)
sheet = Image.new('RGB', (cols * (tw + pad) + pad, rows * (th + lab + pad) + pad), (245, 245, 245))
d = ImageDraw.Draw(sheet)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
except Exception: f = ImageFont.load_default()
for i, p in enumerate(files):
    im = Image.open(p).convert('RGB').resize((tw, th), Image.LANCZOS)
    x = pad + (i % cols) * (tw + pad); y = pad + (i // cols) * (th + lab + pad)
    sheet.paste(im, (x, y + lab)); d.rectangle([x, y + lab, x + tw - 1, y + lab + th - 1], outline=(120, 120, 120))
    m = re.search(r'(\d+\.\d+)', os.path.basename(p)); t = float(m.group(1)) if m else 0
    d.text((x, y + 4), f't = {t:.2f} s  (frame {round(t*30)})', fill=(20, 20, 20), font=f)
sheet.save(out, quality=88)
