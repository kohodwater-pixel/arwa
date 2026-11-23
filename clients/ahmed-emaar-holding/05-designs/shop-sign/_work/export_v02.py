import cairosvg, shutil, pymupdf, os, io, re
import numpy as np
from PIL import Image
P = '../ahmed-emaar-holding_shop-sign_option-{o}-{k}_ar-en_v02.{e}'
TITLE = ('Ahmed Emaar Holding shop sign option {O} v02 - cut-file artwork 1:10, RGB, not print-ready; '
         'logo PROVISIONAL trace, lettering typeface match (Cairo / Inter)')
for o in 'ab':
    src = f'v02_option-{o}_full.svg'
    s = open(src).read()
    assert 'stroke' not in s and 'clipPath' not in s and '<text' not in s, 'forbidden element'
    shutil.copy(src, P.format(o=o, k='artwork-1to10', e='svg'))
    pdf = P.format(o=o, k='artwork-1to10', e='pdf')
    cairosvg.svg2pdf(url=src, write_to=pdf)
    d = pymupdf.open(pdf); d.set_metadata({'title': TITLE.format(O=o.upper()), 'subject': 'v02 cut-file artwork, scale 1:10'}); d.save(pdf + '.tmp'); d.close(); os.replace(pdf + '.tmp', pdf)
    cairosvg.svg2png(url=src, write_to=P.format(o=o, k='preview', e='png'), output_width=2500, output_height=600)
    a = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(url=f'v02_option-{o}_fill-nonzero.svg', output_width=5000))))
    b = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(url=f'v02_option-{o}_fill-evenodd.svg', output_width=5000))))
    print(o, 'paths:', len(re.findall('<path', s)), 'fill-rule nonzero vs evenodd differing pixels:', int((a != b).any(-1).sum()))
