"""Builds the PROVISIONAL logo trace (outlined SVG + PDF) and the comparison sheet.
Geometry in reference-board px; see mark.py. Lettering: Cairo 700 (Arabic), Inter 600 +0.24em tracking (Latin), outlined."""
import sys, io; sys.path.insert(0, '.')
from mark import mark_paths
from textpath import shape
import cairosvg
from PIL import Image, ImageDraw, ImageFont

F = '/home/user/arwa/assets/fonts/'
AR_FONT = (F + 'cairo/Cairo[slnt,wght].ttf', {'wght': 700})
LA_FONT = (F + 'inter/Inter[opsz,wght].ttf', {'wght': 600, 'opsz': 14})
NAVY, GOLD = '#102232', '#D4A95F'
OUT = '/home/user/arwa/clients/ahmed-emaar-holding/04-identity/02-logo/'

def fit_text(font, text, x_left, width, baseline, tracking=0.0):
    d, w, b = shape(font[0], text, 100, font[1], tracking=tracking)
    s = width / (b[2] - b[0])
    return f'<path transform="translate({x_left - b[0]*s:.3f},{baseline:.3f}) scale({s:.5f})" d="{d}"/>'

def lockup_group():
    m = ''.join(f'<path d="{p}"/>' for p in mark_paths())
    ar = fit_text(AR_FONT, 'أحمد إعمار القابضة', 72, 245, 229.5)
    la = fit_text(LA_FONT, 'AHMED EMAAR HOLDING', 74, 243, 256.5, tracking=0.24)
    return m, ar, la

# lockup bbox in ref px (with a little clear space)
X0, Y0, X1, Y1 = 62, 68, 327, 266

def svg(bg, scale=1, title=''):
    m, ar, la = lockup_group()
    w, h = (X1-X0), (Y1-Y0)
    rect = f'<rect x="{X0}" y="{Y0}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*scale}" height="{h*scale}" viewBox="{X0} {Y0} {w} {h}">'
            f'<title>{title}</title>{rect}<g fill="{GOLD}" fill-rule="nonzero">{m}{ar}{la}</g></svg>')

if __name__ == '__main__':
    t = 'Ahmed Emaar Holding - PROVISIONAL logo reconstruction traced from the client identity board, pending the original vector file. Not a master artwork.'
    base = OUT + 'ahmed-emaar-holding_logo_provisional-trace'
    for suffix, bg in [('', None), ('-on-navy', NAVY)]:
        s = svg(bg, 4, t)
        open(f'{base}{suffix}_ar-en_v01.svg', 'w').write(s)
        cairosvg.svg2pdf(bytestring=s.encode(), write_to=f'{base}{suffix}_ar-en_v01.pdf')
    # comparison: reference crop | vector, same size, at 1x and 4x
    ref = Image.open('/home/user/arwa/clients/ahmed-emaar-holding/_originals/ahmed-emaar-holding_identity-board_reference.webp').convert('RGB').crop((X0, Y0, X1, Y1))
    rows = []
    for Z in (1, 4):
        r = ref.resize((ref.width*Z, ref.height*Z), Image.LANCZOS)
        v = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg(NAVY, Z).encode()))).convert('RGB')
        row = Image.new('RGB', (r.width*2 + 20, r.height + 40), 'white')
        row.paste(r, (0, 40)); row.paste(v, (r.width + 20, 40))
        d = ImageDraw.Draw(row)
        d.text((6, 10), f'REFERENCE (board crop) x{Z}', fill='black'); d.text((r.width + 26, 10), f'PROVISIONAL VECTOR TRACE x{Z}', fill='black')
        rows.append(row)
    W = max(r.width for r in rows); H = sum(r.height for r in rows)
    sheet = Image.new('RGB', (W, H), 'white'); y = 0
    for r in rows: sheet.paste(r, (0, y)); y += r.height
    sheet.save('ahmed-emaar-holding_logo_provisional-trace_comparison_v01.png')
