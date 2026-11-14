#!/usr/bin/env python3
"""Contact sheets of the v07 previews: part1 = pages 1-10, part2 = pages 11-20 (2 columns, labelled)."""
from PIL import Image, ImageDraw
from pathlib import Path
import sys
d = Path(__file__).parent / 'preview_v07'
files = sorted(d.glob('*_p[0-9][0-9].png'))
W = 900
for part, sel in ((1, files[:10]), (2, files[10:20])):
    ims = [Image.open(f).convert('RGB') for f in sel]
    h = round(W * ims[0].height / ims[0].width)
    S = Image.new('RGB', (2 * W + 60, 5 * (h + 40) + 20), (90, 92, 98))
    dr = ImageDraw.Draw(S)
    for n, (f, im) in enumerate(zip(sel, ims)):
        x, y = 20 + (n % 2) * (W + 20), 20 + (n // 2) * (h + 40)
        S.paste(im.resize((W, h), Image.LANCZOS), (x, y))
        dr.text((x, y + h + 6), f.stem[-3:], fill='white')
    S.save(d.parent / f'contact_v07_part{part}.png')
    print('wrote', f'contact_v07_part{part}.png')
