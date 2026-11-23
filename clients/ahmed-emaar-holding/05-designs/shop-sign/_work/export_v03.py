import cairosvg, shutil, pymupdf, os, io, re
import numpy as np
from PIL import Image
base = '../ahmed-emaar-holding_shop-sign_letters-on-wall-artwork-1to10_ar-en_v03'
s = open('v03_letters_full.svg').read()
assert 'stroke' not in s and 'clipPath' not in s and '<text' not in s
shutil.copy('v03_letters_full.svg', base + '.svg')
cairosvg.svg2pdf(url='v03_letters_full.svg', write_to=base + '.pdf')
d = pymupdf.open(base + '.pdf'); d.set_metadata({'title': open('v03_title.txt').read(), 'subject': 'v03 cut-file artwork, letters on wall, scale 1:10'}); d.save(base + '.tmp'); d.close(); os.replace(base + '.tmp', base + '.pdf')
a = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(url='v03_letters_fill-nonzero.svg', output_width=6000))))
b = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(url='v03_letters_fill-evenodd.svg', output_width=6000))))
print('paths', len(re.findall('<path', s)), 'nonzero vs evenodd differing px:', int((a != b).any(-1).sum()))
d = pymupdf.open(base + '.pdf'); p = d[0]
print('pdf mm', round(p.rect.width / 72 * 25.4, 1), round(p.rect.height / 72 * 25.4, 1), 'fonts', p.get_fonts(), 'text', repr(p.get_text()))
p.get_pixmap(dpi=200).save('v03_pdfcheck.png')
