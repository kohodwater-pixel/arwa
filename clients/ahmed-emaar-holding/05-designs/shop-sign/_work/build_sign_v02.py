"""Shop sign generator - Ahmed Emaar Holding - v02 (fabrication outlines).

Parametric: W and H are the real size in cm; every size is derived from H, so
the layout re-scales when the client measures the slab (edit W/H, re-run
build_sign_v02.py, export_v02.py, build_drawing_v02.py, build_mockup_v02.py).
SVG viewBox units = real centimetres, written at 1:10 (W mm x H mm).
Every gold element is ONE welded compound outline (skia-pathops): no live
text, no strokes, no clip paths, no overlapping contours.
The logo mark is the PROVISIONAL trace (04-identity/02-logo/_work/mark.py).
"""
import sys, json
LOGO_WORK = '/home/user/arwa/clients/ahmed-emaar-holding/04-identity/02-logo/_work'
sys.path.insert(0, LOGO_WORK)
from mark import BBOX
from textpath import shape
import weld

F = '/home/user/arwa/assets/fonts/'
AR_BOLD = (F + 'cairo/Cairo[slnt,wght].ttf', {'wght': 700})
AR_SEMI = (F + 'cairo/Cairo[slnt,wght].ttf', {'wght': 600})
LATIN = (F + 'inter/Inter[opsz,wght].ttf', {'wght': 600, 'opsz': 14})
NAVY, GOLD = '#102232', '#D4A95F'
NAME_AR = 'أحمد إعمار القابضة'
NAME_EN = 'AHMED EMAAR HOLDING'
TAG_AR = 'حلول متكاملة للبنية التحتية والخدمات'

W, H = 250.0, 60.0           # real size, cm (height = estimate, to be measured)
U = H / 60                   # layout unit: 1 cm at 60 cm high
MIN_MARGIN = 8 * U           # safe margin to lettering, all sides
LINE = 1.2                   # accent/rule width, cm (>= 1 cm to fabricate)
SLOPE = 0.86                 # the mark's roof diagonal (~41 deg)
LEGIBILITY_M_PER_CM = 3.0    # rule of thumb: ~3 m reading distance per 1 cm letter height

# mark stroke widths in board px (measured on the reference, see mark.py)
MARK_STROKES_PX = {'bars': (10.6, 12.0), 'crossbar': 10.0, 'arch': (8.3, 10.0), 'foot': 10.4, 'swoosh_max': 9.6}


def ar_metrics(font, size):
    s = size / 100
    _, _, a = shape(font[0], 'ا', 100, font[1])
    _, _, t = shape(font[0], 'ـ', 100, font[1])
    return {'alef_h': -a[1] * s, 'alef_stem': (a[2] - a[0]) * s, 'horiz_stroke': (t[3] - t[1]) * s}


def latin_metrics(size):
    s = size / 100
    _, _, h = shape(LATIN[0], 'H', 100, LATIN[1])
    _, _, i = shape(LATIN[0], 'I', 100, LATIN[1])
    _, _, d = shape(LATIN[0], '-', 100, LATIN[1])
    return {'cap': (h[3] - h[1]) * s, 'stem': (i[2] - i[0]) * s, 'bar': (d[3] - d[1]) * s}


def placed_text(font, text, size, x, baseline, anchor, tracking=0.0):
    p = weld.text_line(font[0], text, 100, font[1], tracking)
    s = size / 100
    x0, y0, x1, y1 = [v * s for v in p.bounds]
    tx = {'right': x - x1, 'center': x - (x0 + x1) / 2, 'left': x - x0}[anchor]
    q = weld.xform(p, (s, 0, 0, s, tx, baseline))
    return q, q.bounds


def placed_mark(x_right, top, height):
    x0, y0, x1, y1 = BBOX
    k = height / (y1 - y0)
    w = (x1 - x0) * k
    q = weld.xform(weld.mark_path(), (k, 0, 0, k, x_right - w - x0 * k, top - y0 * k))
    return q, w, k


def lockup(x_right, top, mark_h, gap, latin_cap):
    """Mark at right (RTL start); Arabic over Latin, justified to one width,
    Arabic top on the mark top, Latin baseline on the mark baseline."""
    els = {}
    els['mark'], mw, k = placed_mark(x_right, top, mark_h)
    text_right = x_right - mw - gap
    bottom = top + mark_h
    _, _, bf = shape(AR_BOLD[0], NAME_AR, 100, AR_BOLD[1])
    span = mark_h - latin_cap * 1.55
    ar_size = 100 * span / (bf[3] - bf[1])
    ar_base = top + -bf[1] * ar_size / 100
    els['name-ar'], arb = placed_text(AR_BOLD, NAME_AR, ar_size, text_right, ar_base, 'right')
    ar_w = arb[2] - arb[0]
    _, _, bh = shape(LATIN[0], 'H', 100, LATIN[1])
    lat_size = 100 * latin_cap / (bh[3] - bh[1])
    lo, hi = 0.0, 1.0
    for _ in range(40):
        tr = (lo + hi) / 2
        _, _, b = shape(LATIN[0], NAME_EN, lat_size, LATIN[1], tracking=tr)
        (lo, hi) = (tr, hi) if b[2] - b[0] < ar_w else (lo, tr)
    els['name-en'], lab = placed_text(LATIN, NAME_EN, lat_size, text_right, bottom, 'right', tr)
    am, lm = ar_metrics(AR_BOLD, ar_size), latin_metrics(lat_size)
    left = min(arb[0], lab[0])
    info = {
        'mark': {'h': mark_h, 'w': mw, 'stroke_min': MARK_STROKES_PX['arch'][0] * k,
                 'stroke_bars': [v * k for v in MARK_STROKES_PX['bars']], 'swoosh_max': MARK_STROKES_PX['swoosh_max'] * k},
        'name_ar': {'alef_h': am['alef_h'], 'full_extent': arb[3] - arb[1], 'width': ar_w,
                    'stem': am['alef_stem'], 'horiz_stroke': am['horiz_stroke']},
        'name_en': {'cap': lm['cap'], 'tracking_em': tr, 'width': lab[2] - lab[0], 'stem': lm['stem'], 'bar': lm['bar']},
        'pos': {'top': top, 'bottom': bottom, 'x_right': x_right, 'mark_left': x_right - mw, 'left': left,
                'ar_top': arb[1], 'ar_base': ar_base, 'ar_bottom': arb[3], 'lat_top': lab[1], 'lat_base': bottom},
    }
    return els, info


def accents():
    """Corner cuts parallel to the mark's roof diagonal: two at top-left (end
    of the RTL line), one at bottom-right. Expanded to filled bands and
    trimmed exactly at the panel edge (boolean intersection)."""
    panel = weld.rect(0, 0, W, H)
    bands = []
    for h in (10 * U, 16 * U):           # top-left: (0,h) -> (h/SLOPE, 0)
        bands.append(weld.band(-5, h + 5 * SLOPE, h / SLOPE + 5, -5 * SLOPE, LINE))
    h = 12 * U                           # bottom-right: (W-h/SLOPE, H) -> (W, H-h)
    bands.append(weld.band(W - h / SLOPE - 5, H + 5 * SLOPE, W + 5, H - h - 5 * SLOPE, LINE))
    return weld.intersect(weld.union(bands), panel)


def centred(fn_build):
    els, info = fn_build(0)
    lw = -info['pos']['left']
    return fn_build((W + lw) / 2)


def option_a():
    mark_h, gap, cap = 38 * U, 7.5 * U, 7.0 * U
    top = (H - mark_h) / 2
    els, info = centred(lambda xr: lockup(xr, top, mark_h, gap, cap))
    els['accents'] = accents()
    p = info['pos']
    info['margins'] = {'top': p['top'], 'bottom': H - p['bottom'], 'right': W - p['x_right'], 'left': p['left']}
    return els, info


def option_b():
    """Lockup row on top; tagline (alef >= 8 cm) centred below between two
    gold rules (the rule-and-text device of the reference cover)."""
    top = MIN_MARGIN
    tag_alef = 8.0 * U
    tm = ar_metrics(AR_SEMI, 100)
    tsize = 100 * tag_alef / tm['alef_h']
    _, _, bt = shape(AR_SEMI[0], TAG_AR, tsize, AR_SEMI[1])
    t_base = H - MIN_MARGIN - bt[3]
    t_top = t_base + bt[1]
    gap_rows = 4.5 * U
    mark_h = t_top - gap_rows - top
    els, info = centred(lambda xr: lockup(xr, top, mark_h, 6 * U, 5.6 * U))
    els['tagline'], tb = placed_text(AR_SEMI, TAG_AR, tsize, W / 2, t_base, 'center')
    ry = t_base - tag_alef * 0.38
    pad = 4 * U
    x_in = 20 * U
    els['rules'] = weld.union([weld.rect(x_in, ry - LINE / 2, tb[0] - pad - x_in, LINE),
                               weld.rect(tb[2] + pad, ry - LINE / 2, W - x_in - tb[2] - pad, LINE)])
    els['accents'] = accents()
    tmm = ar_metrics(AR_SEMI, tsize)
    info['tagline'] = {'alef_h': tmm['alef_h'], 'full_extent': tb[3] - tb[1], 'width': tb[2] - tb[0],
                       'stem': tmm['alef_stem'], 'horiz_stroke': tmm['horiz_stroke'],
                       'top': tb[1], 'base': t_base, 'bottom': tb[3], 'x0': tb[0], 'x1': tb[2],
                       'gap_above': tb[1] - info['pos']['bottom']}
    p = info['pos']
    info['margins'] = {'top': p['top'], 'bottom': H - tb[3], 'right': W - min(p['x_right'], tb[2]) if False else W - max(p['x_right'], tb[2]),
                       'left': min(p['left'], tb[0])}
    return els, info


ORDER = ['mark', 'name-ar', 'name-en', 'tagline', 'rules', 'accents']


def svg(els, mode='full', fill_rule='nonzero', only=None):
    title = ('Ahmed Emaar Holding - shop sign v02 - cut-file artwork at 1:10 (1 mm = 1 cm real), RGB, not print-ready. '
             'Logo is a PROVISIONAL trace pending the original file; lettering is a typeface match (Cairo / Inter). '
             'Each gold element is one welded outline; no live text.')
    panel = f'<rect id="panel-navy" width="{W}" height="{H}" fill="{NAVY}"/>' if mode in ('full', 'panel') else ''
    gold = ''
    if mode in ('full', 'letters'):
        gold = ''.join(f'<path id="{n}" fill="{GOLD}" fill-rule="{fill_rule}" d="{weld.to_d(els[n])}"/>'
                       for n in ORDER if n in els and (only is None or n in only))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">'
            f'<title>{title}</title>{panel}{gold}</svg>')


def r1(v):
    if isinstance(v, dict): return {k: r1(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)): return [r1(x) for x in v]
    return round(v, 1) if isinstance(v, float) else v


if __name__ == '__main__':
    out = {'W_cm': W, 'H_cm': H, 'legibility_m_per_cm': LEGIBILITY_M_PER_CM}
    for name, fn in (('a', option_a), ('b', option_b)):
        els, info = fn()
        out[name] = r1(info)
        for mode in ('full', 'panel', 'letters'):
            open(f'v02_option-{name}_{mode}.svg', 'w').write(svg(els, mode))
        for rule in ('nonzero', 'evenodd'):
            open(f'v02_option-{name}_fill-{rule}.svg', 'w').write(svg(els, 'full', rule))
        for grp, members in (('channel', ['mark', 'name-ar']), ('flat', ['name-en', 'tagline', 'rules', 'accents'])):
            open(f'v02_option-{name}_{grp}.svg', 'w').write(svg(els, 'letters', only=members))
    json.dump(out, open('metrics_v02.json', 'w'), indent=1, ensure_ascii=False)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != 'pos'} if isinstance(v, dict) else v for k, v in out.items()}, indent=1, ensure_ascii=False))
