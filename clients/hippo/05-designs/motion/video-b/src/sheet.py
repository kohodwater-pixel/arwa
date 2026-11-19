#!/usr/bin/env python3
"""Contact sheet with time-code labels. Usage: python3 sheet.py <out.jpg> <cols> <png> [<png> ...]  (label = time parsed from the file name)"""
import sys, re, os
from PIL import Image, ImageDraw, ImageFont
out, cols, files = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
fw, fh, gap, lab, pad = 360, 640, 16, 34, 24
rows = (len(files) + cols - 1) // cols
W, H = pad * 2 + cols * fw + (cols - 1) * gap, pad * 2 + rows * (fh + lab) + (rows - 1) * gap
sheet = Image.new('RGB', (W, H), '#F3F3F1'); dr = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
except Exception: font = ImageFont.load_default()
for i, f in enumerate(files):
    x, y = pad + (i % cols) * (fw + gap), pad + (i // cols) * (fh + lab + gap)
    m = re.search(r'(\d+\.\d+)', os.path.basename(f)); t = float(m.group(1)) if m else 0
    dr.text((x, y + 4), 't = %.2f s  (frame %d)' % (t, round(t * 30)), fill='#333', font=font)
    sheet.paste(Image.open(f).convert('RGB').resize((fw, fh), Image.LANCZOS), (x, y + lab))
sheet.save(out, quality=88); print(out, sheet.size)
