#!/usr/bin/env python3
"""Derivatives for the company profile v01. Reads 06-profiles/assets/photos and
assets/mockups (copies; _originals is never touched); writes assets/derived/.
Only two operations: crop, and the blue duotone of art-direction.md 4.1."""
from pathlib import Path
import numpy as np
from PIL import Image
B = Path(__file__).resolve().parent.parent
PH, MK, OUT = B/'assets/photos', B/'assets/mockups', B/'assets/derived'
OUT.mkdir(exist_ok=True)
NAVY, BLUE, WHITE = np.array([31,49,98.]), np.array([55,88,176.]), np.array([255,255,255.])
def crop(im, f):
    w, h = im.size
    return im.crop((round(f[0]*w), round(f[1]*h), round(f[2]*w), round(f[3]*h)))
def duotone(im):
    g = np.asarray(im.convert('L')).astype(float)/255
    g = np.clip((g-0.5)*1.10+0.5, 0, 1)          # contrast +10%
    t = g[..., None]; mid = 0.55
    lo = NAVY + (BLUE-NAVY)*np.clip(t/mid, 0, 1)
    hi = BLUE + (WHITE-BLUE)*np.clip((t-mid)/(1-mid), 0, 1)
    return Image.fromarray(np.where(t <= mid, lo, hi).round().astype('uint8'))
JOBS = [  # out, src, crop, duotone, placed mm (w, h)
 ('cover_glass-facade_duotone.png', PH/'glass-facade-cleaners.png', (0.45,0,0.98,0.75), True, (110,110)),
 ('p08_electrical-panel_duotone.png', PH/'electrical-panel.png', (0.17,0,0.611,1), True, (83,132.5)),
 ('p11_office-cleaner_duotone.png', PH/'office-cleaner.png', (0.63,0,0.967,1), True, (83,132.5)),
 ('p12_team_duotone_candidate.png', MK/'mockup_cleaning-team.png', (0.385,0.04,0.719,0.84), True, (83,132.5)),
 ('p15_bus-shelter.png', PH/'bus-shelter.png', (0.44,0,0.989,1), False, (83,75)),
 ('p16_chamber-building.png', PH/'chamber-building.png', (0.21,0,0.99,1), False, (83,75)),
 ('p17_shahd-hotel.png', PH/'shahd-hotel.png', (0.20,0,0.979,1), False, (83,75)),
]
for out, src, f, duo, mm in JOBS:
    im = crop(Image.open(src).convert('RGB'), f)
    if duo: im = duotone(im)
    im.save(OUT/out)
    print(f'{out}\t{im.size[0]}x{im.size[1]}\tplaced {mm[0]}x{mm[1]} mm\t{im.size[0]/(mm[0]/25.4):.0f} ppi (w) / {im.size[1]/(mm[1]/25.4):.0f} ppi (h)')
