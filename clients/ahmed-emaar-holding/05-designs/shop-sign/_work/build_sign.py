"""Shop sign generator - Ahmed Emaar Holding - v01.

Parametric: change W and H (real size in cm) and re-run; every size below is
derived from H, so the layout re-scales when the client measures the slab.
SVG viewBox units = real centimetres; the SVG is written at 1:10
(width in mm = real cm), e.g. 250 x 60 cm sign -> 250 x 60 mm artboard.
All lettering is outlined (HarfBuzz shaping + font outlines), no live text.
The logo is the PROVISIONAL trace from 04-identity/02-logo/_work/mark.py.
"""
import sys, json
LOGO_WORK = '/home/user/arwa/clients/ahmed-emaar-holding/04-identity/02-logo/_work'
sys.path.insert(0, LOGO_WORK)
from mark import mark_paths, BBOX
from textpath import shape

F = '/home/user/arwa/assets/fonts/'
AR_BOLD = (F + 'cairo/Cairo[slnt,wght].ttf', {'wght': 700})
AR_SEMI = (F + 'cairo/Cairo[slnt,wght].ttf', {'wght': 600})
LATIN = (F + 'inter/Inter[opsz,wght].ttf', {'wght': 600, 'opsz': 14})
NAVY, GOLD = '#102232', '#D4A95F'
NAME_AR = 'أحمد إعمار القابضة'
NAME_EN = 'AHMED EMAAR HOLDING'
TAG_AR = 'حلول متكاملة للبنية التحتية والخدمات'

W, H = 250.0, 60.0          # real size, cm (height = estimate, to be measured)
MARGIN_TB = H * 7 / 60      # 7 cm at 60 cm high (>= 10 % of H)
MARGIN_LR = H * 10 / 60     # 10 cm at 60 cm high
LINE = 1.2                  # gold accent line width, cm (>= 1 cm to fabricate)


def text_el(font, text, size, x, baseline, anchor='left', tracking=0.0):
    """Outlined text. size in cm (font em). Returns (svg, bounds in cm)."""
    d, adv, b = shape(font[0], text, 100, font[1], tracking=tracking)
    s = size / 100
    bx0, by0, bx1, by1 = [v * s for v in b]
    w = bx1 - bx0
    if anchor == 'right':
        tx = x - bx1
    elif anchor == 'center':
        tx = x - (bx0 + bx1) / 2
    else:
        tx = x - bx0
    el = f'<path transform="translate({tx:.3f},{baseline:.3f}) scale({s:.6f})" d="{d}"/>'
    return el, (tx + bx0, baseline + by0, tx + bx1, baseline + by1)


def ar_metrics(font, size):
    """Heights for a size: alef height (baseline to top of ا), full extent."""
    _, _, b = shape(font[0], 'ا', 100, font[1])
    _, _, bf = shape(font[0], NAME_AR, 100, font[1])
    s = size / 100
    return {'alef': -b[1] * s, 'top': -bf[1] * s, 'bottom': bf[3] * s}


def size_for_width(font, text, width, tracking=0.0):
    _, _, b = shape(font[0], text, 100, font[1], tracking=tracking)
    return 100 * width / (b[2] - b[0])


def cap_size(font, cap_cm):
    _, _, b = shape(font[0], 'H', 100, font[1])
    return 100 * cap_cm / (b[3] - b[1])


def mark_el(x_right, top, height):
    x0, y0, x1, y1 = BBOX
    k = height / (y1 - y0)
    w = (x1 - x0) * k
    tx, ty = x_right - w - x0 * k, top - y0 * k
    ps = ''.join(f'<path d="{p}"/>' for p in mark_paths())
    return f'<g transform="translate({tx:.3f},{ty:.3f}) scale({k:.6f})">{ps}</g>', w


def lockup(x_right, top, mark_h, gap, ar_size_hint=None, latin_cap=None):
    """Horizontal lockup: mark at right (RTL start); Arabic name above Latin name,
    both justified to the same width, block spanning the mark height."""
    m, mw = mark_el(x_right, top, mark_h)
    text_right = x_right - mw - gap
    bottom = top + mark_h
    # Latin: cap height latin_cap, baseline on the mark's baseline
    lat_size = cap_size(LATIN, latin_cap)
    # Arabic: size so that its top (hamza of أ) sits on the mark top and its
    # lowest point (hamza of إ) leaves >= 0.55 x Latin cap above the Latin caps
    am = ar_metrics(AR_BOLD, 100)
    span = mark_h - latin_cap - 0.55 * latin_cap   # top of Arabic -> bottom of Arabic
    ar_size = 100 * span / (am['top'] + am['bottom'])
    if ar_size_hint:
        ar_size = min(ar_size, ar_size_hint)
    am = ar_metrics(AR_BOLD, ar_size)
    ar_base = top + am['top']
    ar, arb = text_el(AR_BOLD, NAME_AR, ar_size, text_right, ar_base, 'right')
    ar_w = arb[2] - arb[0]
    # tracking so the Latin line matches the Arabic width
    lo, hi = 0.0, 1.0
    for _ in range(40):
        tr = (lo + hi) / 2
        _, _, b = shape(LATIN[0], NAME_EN, lat_size, LATIN[1], tracking=tr)
        if b[2] - b[0] < ar_w: lo = tr
        else: hi = tr
    la, lab = text_el(LATIN, NAME_EN, lat_size, text_right, bottom, 'right', tracking=tr)
    left = min(arb[0], lab[0])
    info = {'mark_height_cm': round(mark_h, 1), 'mark_width_cm': round(mw, 1),
            'arabic_alef_height_cm': round(am['alef'], 1),
            'arabic_full_extent_cm': round(am['top'] + am['bottom'], 1),
            'arabic_width_cm': round(ar_w, 1),
            'latin_cap_height_cm': round(latin_cap, 1), 'latin_tracking_em': round(tr, 3),
            'latin_width_cm': round(lab[2] - lab[0], 1),
            'lockup_width_cm': round(x_right - left, 1),
            '_pos': {'top': top, 'bottom': bottom, 'x_right': x_right, 'mark_left': x_right - mw, 'text_right': text_right,
                     'left': left, 'ar_top': arb[1], 'ar_base': ar_base, 'ar_bottom': arb[3], 'lat_top': lab[1], 'lat_base': bottom}}
    return m + ar + la, left, info


def accents(depth_left=None, depth_right=None):
    """Restrained gold corner cuts parallel to the mark's roof diagonal
    (rising to the right, slope 0.86 ~ 41 deg): two at the top-left corner
    (end of the RTL reading line), one at the bottom-right corner. They stay
    inside the free end fields and never cross the lettering."""
    slope = 0.86
    els = []
    for h in depth_left:                       # top-left corner: (0,h) -> (h/slope,0)
        els.append(f'<line x1="{-2}" y1="{h + 2*slope:.2f}" x2="{h / slope:.2f}" y2="0"/>')
    for h in depth_right:                      # bottom-right corner: (W-h/slope,H) -> (W,H-h)
        els.append(f'<line x1="{W - h / slope:.2f}" y1="{H}" x2="{W + 2}" y2="{H - h - 2*slope:.2f}"/>')
    return (f'<g clip-path="url(#panel)" stroke="{GOLD}" stroke-width="{LINE}" '
            f'stroke-linecap="butt" fill="none">{"".join(els)}</g>')


def option_a():
    mark_h = H * 32 / 60
    top = (H - mark_h) / 2
    # compute width first to centre the lockup
    _, left, info = lockup(0, top, mark_h, H * 7 / 60, latin_cap=H * 6 / 60)
    lw = -left
    x_right = (W + lw) / 2
    body, left, info = lockup(x_right, top, mark_h, H * 7 / 60, latin_cap=H * 6 / 60)
    acc = accents([H * 10 / 60, H * 16 / 60], [H * 12 / 60])
    info['margins_cm'] = {'top': round(top, 1), 'bottom': round(H - top - mark_h, 1),
                          'right': round(W - x_right, 1), 'left': round(left, 1)}
    return body, acc, info


def option_b():
    """Lockup row on top, tagline centred below between two gold rules
    (the rule-and-text device of the reference cover)."""
    mark_h = H * 27 / 60
    top = MARGIN_TB
    gap = H * 5.5 / 60
    cap = H * 5.3 / 60
    _, left, _ = lockup(0, top, mark_h, gap, latin_cap=cap)
    lw = -left
    x_right = (W + lw) / 2
    body, left, info = lockup(x_right, top, mark_h, gap, latin_cap=cap)
    # tagline
    tag_alef = H * 5.0 / 60
    _, _, ba = shape(AR_SEMI[0], 'ا', 100, AR_SEMI[1])
    tsize = 100 * tag_alef / -ba[1]
    _, _, bt = shape(AR_SEMI[0], TAG_AR, tsize, AR_SEMI[1])
    t_base = H - MARGIN_TB - bt[3]
    tag, tb = text_el(AR_SEMI, TAG_AR, tsize, W / 2, t_base, 'center')
    # rules either side of the tagline, vertically at the middle of the letters' body
    ry = t_base - tag_alef * 0.38
    pad = H * 4 / 60
    rules = (f'<rect x="{left:.2f}" y="{ry - LINE / 2:.2f}" width="{tb[0] - pad - left:.2f}" height="{LINE}"/>'
             f'<rect x="{tb[2] + pad:.2f}" y="{ry - LINE / 2:.2f}" width="{x_right - tb[2] - pad:.2f}" height="{LINE}"/>')
    acc = accents([H * 10 / 60, H * 16 / 60], [H * 12 / 60])
    info.update({'tagline_alef_height_cm': round(tag_alef, 1),
                 'tagline_full_extent_cm': round(tb[3] - tb[1], 1),
                 'tagline_width_cm': round(tb[2] - tb[0], 1),
                 '_tag': {'top': tb[1], 'base': t_base, 'bottom': tb[3], 'x0': tb[0], 'x1': tb[2]},
                 'gap_lockup_to_tagline_cm': round(tb[1] - (top + mark_h), 1),
                 'margins_cm': {'top': round(top, 1), 'bottom': round(H - tb[3], 1),
                                'right': round(W - x_right, 1), 'left': round(left, 1)}})
    return body + tag + rules, acc, info


def svg(body, acc, mode='full', scale_note=True):
    """mode: full | panel (navy only) | letters (gold only, transparent)."""
    title = ('Ahmed Emaar Holding - shop sign v01 - artwork at 1:10 (1 mm = 1 cm real). '
             'Logo is a PROVISIONAL trace pending the original file. All text outlined.')
    panel = f'<rect width="{W}" height="{H}" fill="{NAVY}"/>' if mode in ('full', 'panel') else ''
    gold = f'<g fill="{GOLD}">{body}</g>{acc}' if mode in ('full', 'letters') else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">'
            f'<title>{title}</title><defs><clipPath id="panel"><rect width="{W}" height="{H}"/></clipPath></defs>'
            f'{panel}{gold}</svg>')


if __name__ == '__main__':
    out = {}
    for name, fn in (('a', option_a), ('b', option_b)):
        body, acc, info = fn()
        out[name] = info
        for mode in ('full', 'panel', 'letters'):
            open(f'option-{name}_{mode}.svg', 'w').write(svg(body, acc, mode))
    json.dump({'W_cm': W, 'H_cm': H, **out}, open('metrics.json', 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(out, indent=1, ensure_ascii=False))
