"""v02: PROVISIONAL logo trace, welded outlines (one compound path per element)."""
import sys, io; sys.path.insert(0, '.')
import cairosvg, pymupdf
from PIL import Image, ImageDraw
from weld import mark_path, text_line, xform, to_d
F = '/home/user/arwa/assets/fonts/'
NAVY, GOLD = '#102232', '#D4A95F'
OUT = '/home/user/arwa/clients/ahmed-emaar-holding/04-identity/02-logo/'
TITLE = ('Ahmed Emaar Holding logo - PROVISIONAL reconstruction from the client identity board, pending the original vector file. '
         'Mark redrawn geometrically; lettering is a typeface match (Cairo / Inter), not traced.')

def fit(p, x_left, width, baseline):
    x0, y0, x1, y1 = p.bounds
    s = width / (x1 - x0)
    return xform(p, (s, 0, 0, s, x_left - x0 * s, baseline))

def elements():
    m = mark_path()
    ar = fit(text_line(F + 'cairo/Cairo[slnt,wght].ttf', 'أحمد إعمار القابضة', 100, {'wght': 700}), 72, 245, 229.5)
    la = fit(text_line(F + 'inter/Inter[opsz,wght].ttf', 'AHMED EMAAR HOLDING', 100, {'wght': 600, 'opsz': 14}, 0.24), 74, 243, 256.5)
    return [('mark', m), ('name-ar', ar), ('name-en', la)]

X0, Y0, X1, Y1 = 62, 68, 327, 266

def svg(bg, scale=1, fill_rule='nonzero'):
    w, h = X1 - X0, Y1 - Y0
    rect = f'<rect x="{X0}" y="{Y0}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    ps = ''.join(f'<path id="{n}" fill-rule="{fill_rule}" d="{to_d(p)}"/>' for n, p in elements())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*scale}" height="{h*scale}" viewBox="{X0} {Y0} {w} {h}">'
            f'<title>{TITLE}</title>{rect}<g fill="{GOLD}">{ps}</g></svg>')

def set_title(pdf):
    d = pymupdf.open(pdf); d.set_metadata({'title': TITLE, 'author': 'Agency (provisional)', 'subject': 'PROVISIONAL logo trace v02'})
    d.saveIncr() if False else d.save(pdf + '.tmp'); d.close()
    import os; os.replace(pdf + '.tmp', pdf)

if __name__ == '__main__':
    base = OUT + 'ahmed-emaar-holding_logo_provisional-trace'
    for suffix, bg in [('', None), ('-on-navy', NAVY)]:
        s = svg(bg, 4)
        open(f'{base}{suffix}_ar-en_v02.svg', 'w').write(s)
        cairosvg.svg2pdf(bytestring=s.encode(), write_to=f'{base}{suffix}_ar-en_v02.pdf')
        set_title(f'{base}{suffix}_ar-en_v02.pdf')
    # fill-rule invariance check
    import numpy as np
    a = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg(NAVY, 6, 'nonzero').encode()))))
    b = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg(NAVY, 6, 'evenodd').encode()))))
    print('fill-rule pixel diff (max, count):', int(np.abs(a.astype(int) - b).max()), int((a != b).any(-1).sum()))
    ref = Image.open('/home/user/arwa/clients/ahmed-emaar-holding/_originals/ahmed-emaar-holding_identity-board_reference.webp').convert('RGB').crop((X0, Y0, X1, Y1))
    rows = []
    for Z in (1, 4):
        r = ref.resize((ref.width * Z, ref.height * Z), Image.LANCZOS)
        v = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg(NAVY, Z).encode()))).convert('RGB')
        row = Image.new('RGB', (r.width * 2 + 20, r.height + 40), 'white'); row.paste(r, (0, 40)); row.paste(v, (r.width + 20, 40))
        d = ImageDraw.Draw(row); d.text((6, 10), f'REFERENCE (board crop) x{Z}', fill='black'); d.text((r.width + 26, 10), f'PROVISIONAL VECTOR TRACE v02 x{Z}', fill='black')
        rows.append(row)
    sheet = Image.new('RGB', (max(r.width for r in rows), sum(r.height for r in rows)), 'white'); y = 0
    for r in rows: sheet.paste(r, (0, y)); y += r.height
    sheet.save('ahmed-emaar-holding_logo_provisional-trace_comparison_v02.png')

# welded vs unwelded (v01-style overlapping parts) raster check: nothing lost or added
def unwelded_svg(Z):
    from mark import mark_paths
    import build_logo as v1
    m, ar, la = v1.lockup_group()
    w, h = X1 - X0, Y1 - Y0
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*Z}" height="{h*Z}" viewBox="{X0} {Y0} {w} {h}">'
            f'<rect x="{X0}" y="{Y0}" width="{w}" height="{h}" fill="{NAVY}"/><g fill="{GOLD}">{m}{ar}{la}</g></svg>')
if __name__ == '__main__':
    import numpy as np
    a = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg(NAVY, 6).encode()))).convert('L')).astype(int)
    b = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=unwelded_svg(6).encode()))).convert('L')).astype(int)
    print('welded vs unwelded: pixels differing by >64 levels:', int((np.abs(a - b) > 64).sum()), 'of', a.size)
