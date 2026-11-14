#!/usr/bin/env python3
"""otlobny-emaar — company profile v06 (answers review_v05_r2 and the CD rulings of 2026-11-14; v05 files untouched).

Writes:
  06-profiles/otlobny-emaar_company-profile_screen_ar-en_v06.html   (editable source, assets linked from assets/)
  06-profiles/assets/derived/v06_*.jpg                               (cropped, retouched, graded photographs)

Copy: content-outline.md (+ status blocks), brand-context.md decision log (CD rulings 2026-11-14 for v06),
review_v04_r1.md (m14 English edits). Photography: assets/stock/README.md round 3 (page plan, grade recipe, demotions).
Run:  python3 06-profiles/_work/build_profile_v06.py
"""
from pathlib import Path
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
import math, re

BASE = Path(__file__).resolve().parent.parent           # 06-profiles/
OUT = BASE / 'otlobny-emaar_company-profile_screen_ar-en_v06.html'
DER = BASE / 'assets/derived'
ST = 'assets/stock/'
LOG = []                 # (page, derived file, source, crop px, size mm, effective ppi)
USED = {}                # source file -> set of pages (no image may appear on two pages)
CREDITS_USED = set()

# =============================================================== credits (CREDITS.md, round 3; original titles)
CREDIT = {
 'cover-hero_blue-glass-facade_wikimedia-glass-building-corner.jpg': ('Glass building corner', 'Jonathan Simcoe', 'CC0 1.0', 'Wikimedia Commons', False),
 'contracting_tower-construction-with-palms_flickr-3384156664.jpg': ('Construction.', 'ianmunroe', 'CC BY 2.0', 'Flickr', False),
 'cleaning_rope-access-blue-glass-tower_flickr-16633802875.jpg': ('Clean windows everyday', 'waitscm', 'CC BY 2.0', 'Flickr', False),
 'landscaping_palm-park-riyadh-museum_flickr-51949716085.jpg': ('Stones and Grass, National Museum Park Riyadh', 'amanderson2', 'CC BY 2.0', 'Flickr', False),
 'maintenance_technician-headlamp-tools_flickr-51315198261.jpg': ('157th Airmen', 'S.C. Air National Guard', 'Public Domain Mark 1.0', 'Flickr', False),
 'opener_madinah-haram-plaza-umbrellas_wikimedia-masjid-al-nabawi-2024-3.jpg': ('Masjid al-Nabawi 2024 (3)', 'Radosław Botev', 'CC BY 3.0 PL', 'Wikimedia Commons', False),
 'opener_madinah-haram-panorama_wikimedia-mezquita-del-profeta-dd01.jpg': ('Mezquita del Profeta, Medina, Arabia Saudita, 2025-05-22, DD 01', 'Diego Delso', 'CC BY-SA 4.0', 'Wikimedia Commons', True),
 'contracting_steel-erector-on-beams_flickr-132069821.jpg': ('Steel Worker', 'billjacobus1', 'CC BY 2.0', 'Flickr', False),
 'contracting_concrete-screeding-crew_flickr-4184357497.jpg': ('Concrete screeding (Army engineers)', 'USACE Europe District', 'CC BY 2.0', 'Flickr', False),
 'contracting_surveyor-theodolite_flickr-8756741875.jpg': ('A new generation of industrial leaders', 'DFID – UK Department for International Development', 'CC BY 2.0', 'Flickr', False),
 'landscaping_date-palm-walkway-doha_flickr-7631829614.jpg': ('Doha, Qatar', 'Studio Sarah Lou', 'CC BY 2.0', 'Flickr', False),
 'landscaping_palms-dry-planting_flickr-4968666077.jpg': ('Area 1', 'Port of San Diego', 'CC BY 2.0', 'Flickr', False),
 'maintenance_hvac-gauges_wikimedia-379th-eces-8502255.jpg': ('379th ECES HVAC technicians combat rising temperatures', 'U.S. Air Force, A1C Derrick Boleyn', 'Public domain', 'Wikimedia Commons', False),
 'maintenance_rooftop-ac-units-technician_flickr-54752357237.jpg': ('Air Conditioners', 'chooyutshing', 'Public Domain Mark 1.0', 'Flickr', False),
 'contracting-electrical_distribution-board_wikimedia-small-house-distribution-panel-2.jpg': ('Small house distribution panel 2', 'Retired electrician', 'CC0 1.0', 'Wikimedia Commons', False),
 'cleaning_mop-and-trolley-floor_flickr-24978817211.jpg': ('Cleaner with mop and uniform', 'aqua.mech', 'CC BY 2.0', 'Flickr', False),
 'cleaning_rope-access-window-cleaner_flickr-4797579546.jpg': ('Window Cleaner', 'Malte Sörensen', 'CC BY 2.0', 'Flickr', False),
 'manpower_gulf-site-workforce_flickr-9836421046.jpg': ('Workers on Building Site', 'mikecogh', 'CC BY-SA 2.0', 'Flickr', True),
 'manpower_waiter-pouring-tea_flickr-38075436525.jpg': ('Waiter serving tea', 'www.ralfsteinberger.com', 'CC BY 2.0', 'Flickr', False),
 'manpower_catering-table-setup-overhead_flickr-6160161346.jpg': ('Plano Cenital Catering', 'TEDxLasPalmas', 'CC BY-SA 2.0', 'Flickr', True),
 'logistics_warehouse-racking-aisle_flickr-4324416999.jpg': ('Sealey Warehouse (racking aisle)', 'toolstop', 'CC BY 2.0', 'Flickr', False),
}
FREE = ('CC0 1.0', 'Public domain', 'Public Domain Mark 1.0')
DEMOTED = {'contracting_rebar-worker_wikimedia-rebar-worker-j2.jpg', 'landscaping_palm-promenade-lawn_flickr-19570930662.jpg',
           'landscaping_gardener-trimmer_flickr-54576923958.jpg', 'landscaping_date-palm_wikimedia-date-palm-tree-landscape.jpg',
           'cleaning_floor-scrubbers-lobby_wikimedia-floor-scrubbers.jpg', 'logistics_white-box-truck_flickr-51928284838.jpg',
           'logistics_forklift-in-motion_flickr-4325154436.jpg', 'contracting_site-at-blue-hour_flickr-2146788503.jpg'}

# =============================================================== retouches (in memory; no source file is written)
def _inpaint(a, mask, iters=600):
    a = a.astype(float).copy()
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = max(ys.min() - 2, 0), ys.max() + 3, max(xs.min() - 2, 0), xs.max() + 3
    sub, m = a[y0:y1, x0:x1], mask[y0:y1, x0:x1]
    sub[m] = sub[~m].mean(axis=0)
    for _ in range(iters):
        avg = (np.roll(sub, 1, 0) + np.roll(sub, -1, 0) + np.roll(sub, 1, 1) + np.roll(sub, -1, 1)) / 4
        sub[m] = avg[m]
    rng = np.random.default_rng(4)
    sub[m] += rng.normal(0, 1, (m.sum(), 3)) * sub[~m].std(axis=0) * 0.3
    a[y0:y1, x0:x1] = sub
    return np.clip(a, 0, 255).astype(np.uint8)

def _dilate(m, k=3):
    return np.array(Image.fromarray(m.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(k))) > 0

def retouch(fname, im):
    a = np.array(im)
    r_, g_, b_ = [a[..., i].astype(int) for i in range(3)]
    if fname.startswith('maintenance_hvac-gauges'):
        # maker name and logo on the blue manifold label: lettering only, rebuilt from the label's own blue (v04 method)
        from scipy.ndimage import gaussian_filter
        pm = Image.new('L', (a.shape[1], a.shape[0]), 0)
        ImageDraw.Draw(pm).polygon([(1754, 1350), (2058, 1258), (2068, 1326), (1766, 1410)], fill=255)
        inside = np.array(pm) > 0
        dark_blue = (b_ > r_ + 35) & (r_ < 90) & ((r_ + g_ + b_) < 330)
        m = _dilate(inside & ~dark_blue) & inside
        w = (inside & dark_blue & ~m).astype(float)
        fill = np.stack([gaussian_filter(a[..., i] * w, 6) for i in range(3)], -1) / (gaussian_filter(w, 6)[..., None] + 1e-6)
        yy, xx = np.nonzero(m)
        a = a.copy()
        a[yy, xx] = np.clip(fill[yy, xx] + np.random.default_rng(7).normal(0, 2.0, (len(yy), 3)), 0, 255).astype(np.uint8)
    elif fname.startswith('mockup_car-scooter-facade'):
        # banner slogan «خدمتك بجودة تهمنا» is not approved copy: filled with the banner navy (logo on the banner kept)
        l, t, r, b = 1226, 176, 1336, 296
        m = np.zeros(a.shape[:2], bool); m[t:b, l:r] = (r_ + g_ + b_)[t:b, l:r] > 200
        a = _inpaint(a, _dilate(m, 7), 600)
    elif fname.startswith('maintenance_technician-headlamp'):
        # maker name printed in grey on the black head strap ("COAST"): letters filled with the strap colour.
        # Mask = light, neutral (not skin-toned) pixels inside the strap area.
        l, t, r, b = 672, 206, 762, 225
        sub = np.zeros(a.shape[:2], bool); sub[t:b, l:r] = True
        m = sub & ((r_ + g_ + b_) > 100) & ~(r_ > b_ + 25)
        a = _inpaint(a, _dilate(m, 3), 500)
    return Image.fromarray(a)

# =============================================================== the art-director's grade recipe (round 3), identical for every photo
NAVY = np.array([31, 49, 98]) / 255
WARM = {'manpower_waiter-pouring-tea_flickr-38075436525.jpg', 'manpower_catering-table-setup-overhead_flickr-6160161346.jpg'}
def grade(im, fname):
    a = np.asarray(im).astype(float) / 255
    if fname in WARM:                                        # 0. warm interiors: temperature -5 (approximation: R -3 %, B +3 %)
        a = a * np.array([0.97, 1.0, 1.03])
    L = (a * [0.2126, 0.7152, 0.0722]).sum(axis=2, keepdims=True)
    a = L + (a - L) * 0.80                                   # 1. saturation -20
    a = np.interp(a, [0, 64 / 255, 192 / 255, 1], [10 / 255, 56 / 255, 200 / 255, 1])   # 2. curves 64->56, 192->200, black out 10
    a = np.clip(a, 0, 1)
    sl = a - (1 - 2 * NAVY) * a * (1 - a)                    # 3. navy #1F3162, soft light (all channels < .5)
    a = a * 0.85 + sl * 0.15                                 #    at 15 % opacity
    return Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))

_cache = {}
def load(src):
    if src not in _cache:
        _cache[src] = retouch(Path(src).name, Image.open(BASE / src).convert('RGB'))
    return _cache[src]

def prep(name, src, w_mm, h_mm, cx=.5, cy=.5, zoom=1.0, box=None, page='', graded=True, whiten=False):
    """Crop to the frame's aspect around (cx, cy), never upscale; grade; save assets/derived/v06_<name>.jpg; log ppi."""
    fn = Path(src).name
    assert fn not in DEMOTED, fn
    im = load(src)
    ox = oy = 0
    if box:
        ox, oy = box[0], box[1]
        im = im.crop(box)
    W, H = im.size
    asp = w_mm / h_mm
    cw = min(W, H * asp) / zoom; ch = cw / asp
    l = min(max(0, cx * W - cw / 2), W - cw); t = min(max(0, cy * H - ch / 2), H - ch)
    c = im.crop((round(l), round(t), round(l + cw), round(t + ch)))
    ppi = c.size[0] / (w_mm / 25.4)
    tw = min(c.size[0], round(w_mm / 25.4 * 300))
    if tw < c.size[0]:
        c = c.resize((tw, round(tw / asp)), Image.LANCZOS)
    if graded:
        c = grade(c, fn)
    if whiten:
        arr = np.asarray(c).copy(); arr[(arr > 238).all(axis=2)] = 255; c = Image.fromarray(arr)
    out = DER / f'v06_{name}.jpg'
    c.save(out, quality=86, optimize=True, progressive=True)
    if fn in CREDIT:
        CREDITS_USED.add(fn)
    USED.setdefault(src, set()).add(page)
    LOG.append((page, out.name, src, (round(ox + l), round(oy + t), round(ox + l + cw), round(oy + t + ch)), f'{w_mm:.1f} x {h_mm:.1f}', round(ppi), 'graded' if graded else 'not graded'))
    return f'assets/derived/{out.name}'

def img(src, x, y, w, h, alt, cls=''):
    return f'<img class="a ph {cls}" src="{src}" alt="{alt}" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm">'

# =============================================================== type helpers
DM = '<i class="dm"></i>'
def ar(html, cls='', style=''):
    return f'<div class="ar {cls}" lang="ar" dir="rtl" style="{style}">{html}</div>'
def en(html, cls='', style=''):
    return f'<div class="en {cls}" lang="en" dir="ltr" style="{style}">{html}</div>'
def at(x, y, w, inner, extra=''):
    return f'<div class="a" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;{extra}">{inner}</div>'
def N(s):
    return f'<span class="num" dir="ltr">{s}</span>'
def flow(x0, x1, y, inner, cls=''):
    return f'<div class="a flow {cls}" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm">{inner}</div>'
def fcols(ar_html, en_html, cls=''):
    return f'<div class="fcols {cls}">{en_html}{ar_html}</div>'

# one numbering scheme, same format in both languages (m1)
SEC = {1: ('من نحن', 'About Us'), 2: ('الرؤية والرسالة والأهداف', 'Vision, Mission and Goals'), 3: ('خدماتنا', 'Our Services'),
       4: ('لماذا نحن', 'Why Us'), 5: ('أعمالنا', 'Our Work'), 6: ('شركاء النجاح', 'Partners in Success'), 7: ('تواصل معنا', 'Contact')}
def kicker(n, sub=None):
    a_, e_ = SEC[n]
    s = f' — {N(sub)}' if sub else ''
    return (f'<div class="pair kick">{en(f"{n:02d} — {e_}" + (f" — {sub}" if sub else ""), "k")}'
            f'{ar(DM + N(f"{n:02d}") + f" — {a_}" + s, "k")}</div>')
def stack_title(tar, ten, cls=''):
    return f'<h2 class="ar t1 st {cls}" lang="ar" dir="rtl">{tar}</h2><h2 class="en t1 st {cls}" lang="en" dir="ltr">{ten}</h2>'
def pair_title(tar, ten):
    return f'<div class="pair base">{en(ten, "t1")}{ar(tar, "t1")}</div>'

def foot(p, x0, x1, n, dark=False):
    a_, e_ = SEC[n] if n else ('المحتويات', 'Contents')
    folio = f'<b class="folio num" dir="ltr">{p:02d}</b>'
    return (f'<div class="a ft{" dk" if dark else ""}" style="left:{x0}mm;top:197mm;width:{x1-x0}mm">'
            f'{en(e_ + " &nbsp;·&nbsp; OTLOBNY Emaar", "fl")}{ar(f"<span>{a_} · اطلبني إعمار</span>{folio}", "fl")}</div>')

def page(p, body, cls=''):
    return f'<section class="page {cls}" id="p{p}" data-page="{p}">\n{body}\n</section>\n'

def lgrid(items, after=None):
    """M2: one shared grid row per item — English cell left, Arabic cell right, one rule across both."""
    rows = ''.join(f'<div class="lr">{en(DM + f"<span>{e_}</span>", "li")}{ar(DM + f"<span>{a_}</span>", "li")}</div>' for a_, e_ in items)
    if after:
        rows += f'<div class="lr last">{en(after[1], "after")}{ar(after[0], "after")}</div>'
    return f'<div class="lg">{rows}</div>'

# =============================================================== diamonds (cover and service master share one lattice idea)
def diamond_svg(cells, did, w=297, h=210, x=0, y=0, label='Photographs, illustrative'):
    defs, body = '', ''
    for n, c in enumerate(cells):
        cx, cy, r, f, kind = c[:5]
        alt = c[5] if len(c) > 5 else ''
        side = r * math.sqrt(2); rx = side * .12
        rect = (f'<rect x="{cx-side/2:.3f}" y="{cy-side/2:.3f}" width="{side:.3f}" height="{side:.3f}" rx="{rx:.3f}" '
                f'transform="rotate(45 {cx:.3f} {cy:.3f})"')
        if kind == 'img':
            defs += f'<clipPath id="{did}{n}">{rect}/></clipPath>'
            body += (f'<image href="{f}" x="{cx-r:.3f}" y="{cy-r:.3f}" width="{2*r:.3f}" height="{2*r:.3f}" '
                     f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{did}{n})"><title>{alt}</title></image>')
        elif kind == 'line':
            body += f'{rect} fill="none" stroke="{f}" stroke-width=".3"/>'
        else:
            body += f'{rect} fill="{f}"/>'
    return (f'<svg class="a" style="left:{x}mm;top:{y}mm" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
            f'<defs><linearGradient id="g{did}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1F3162"/><stop offset="1" stop-color="#3758B0"/></linearGradient>{defs}</defs>{body}</svg>')

def lattice(w, h, step, color, op, did, filled=()):
    """Outline diamond lattice (decorative ground), optional filled cells [(i, j, colour)]."""
    r = step / 2 - .9
    cells = []
    for j in range(-1, int(h / step * 2) + 3):
        for i in range(-1, int(w / step) + 2):
            cx = i * step + (step / 2 if j % 2 else 0); cy = j * step / 2
            cells.append((cx, cy, r, color, 'line'))
    for (i, j, col) in filled:
        cx = i * step + (step / 2 if j % 2 else 0); cy = j * step / 2
        cells.append((cx, cy, r, col, 'fill'))
    return diamond_svg(cells, did, w, h, label='Decorative pattern').replace('<svg class="a"', f'<svg class="a" opacity="{op}"', 1) if op < 1 else diamond_svg(cells, did, w, h, label='Decorative pattern')

# =============================================================== copy (content-outline.md; m14 English edits)
SERVICES = [
 dict(p=7, key='contracting', ar='المقاولات العامة', en='General Contracting',
      sar='تنفيذ المشاريع الإنشائية بجميع مراحلها، من الدراسة الفنية إلى التنفيذ.',
      sen='Construction projects at every stage, from technical study to execution.',
      iar='تنفذ «اطلبني إعمار» المشاريع الإنشائية بجميع مراحلها، ابتداءً من الدراسة الفنية والمخططات التصميمية حتى التنفيذ، لكافة أنواع المباني والمنشآت السكنية والحكومية والتجارية.',
      ien='OTLOBNY Emaar carries out construction projects at every stage, from the technical study and design drawings through to execution, for all types of residential, government and commercial buildings and facilities.',
      items=[('مشاريع الإنشاء', 'Construction projects'), ('الأعمال الكهربائية', 'Electrical works'), ('الأعمال الميكانيكية', 'Mechanical works'),
             ('أعمال السباكة والصرف', 'Plumbing and drainage works'), ('مشاريع أنظمة الحريق', 'Fire systems projects')]),
 dict(p=8, key='landscaping', ar='الزراعة والتشجير', en='Landscaping',
      sar='التشجير وتنسيق الحدائق وصيانة المنتزهات وأنظمة الري.',
      sen='Tree planting, garden landscaping, and maintenance of parks and irrigation equipment.',
      iar='تنفذ «اطلبني إعمار» أعمال التشجير وتنسيق الحدائق، وتتولى صيانة المنتزهات وأشجار الشوارع وما يتصل بها من أجهزة الري.',
      ien='OTLOBNY Emaar carries out tree planting and garden landscaping, and maintains parks, street trees and the irrigation equipment that serves them.',
      items=[('أعمال التشجير', 'Tree planting'), ('تنسيق الحدائق المزروعة', 'Landscaping of planted gardens'),
             ('صيانة المنتزهات وأشجار الشوارع', 'Maintenance of parks and street trees'), ('صيانة أجهزة الري', 'Maintenance of irrigation equipment')]),
 dict(p=9, key='maintenance', ar='الصيانة', en='Maintenance',
      sar='خدمات صيانة شاملة للمنشآت بفريق من الكوادر المؤهلة.',
      sen='Comprehensive facility maintenance by a qualified team.',
      iar='تقدم «اطلبني إعمار» خدمات صيانة شاملة للمنشآت، عن طريق فريق احترافي من الكوادر المؤهلة.',
      ien='OTLOBNY Emaar provides comprehensive maintenance services for facilities, delivered by a professional team of qualified staff.',
      items=[('تشغيل وصيانة أنظمة التكييف المركزية', 'Operation and maintenance of central air&#8209;conditioning systems'),
             ('تشغيل وصيانة أنظمة المصاعد', 'Operation and maintenance of lift systems')]),
 dict(p=10, key='cleaning', ar='النظافة', en='Cleaning',
      sar='نظافة المباني ومكافحة الآفات للقطاعات الحكومية والتجارية والخاصة.',
      sen='Building cleaning and pest control for the government, commercial and private sectors.',
      iar='تقدم «اطلبني إعمار» خدمات نظافة عالية المستوى يمكن الوثوق بها، للقطاعات الحكومية والخاصة والتجارية.',
      ien='OTLOBNY Emaar provides <span class="nw">high-standard,</span> dependable cleaning services for the government, private and commercial sectors.',
      items=[('نظافة المباني الحكومية والتجارية والمباني الخاصة', 'Cleaning of government, commercial and private buildings'),
             ('مكافحة الآفات والحشرات لجميع المنشآت الحكومية والخاصة', 'Pest and insect control for all government and private facilities')]),
 dict(p=11, key='manpower', ar='تأمين الكوادر', en='Manpower Supply',
      sar='كوادر نظامية مؤهلة للمنشآت الحكومية والتجارية والخاصة، بعقود شهرية وسنوية على نظام «أجير».',
      sen='Qualified, legally compliant staff for government, commercial and private facilities, on monthly and annual contracts through the Ajeer system.',
      iar='توفر «اطلبني إعمار» الكوادر النظامية المؤهلة لسوق العمل في مجالات الضيافة والخدمات، للمرافق الحكومية والتجارية والخاصة، وفقاً لمعايير الصحة المهنية.',
      ien='OTLOBNY Emaar supplies qualified, legally compliant staff for hospitality and services roles in government, commercial and private facilities, in line with occupational health standards.',
      items=[('تأجير عمال نظافة للمستشفيات والفنادق والمطارات', 'Cleaning staff for hospitals, hotels and airports'),
             ('تأجير خدمات عمال للفعاليات والمناسبات', 'Staff for events and functions'),
             ('توفير عمال المقاهي والمطاعم والإعاشة', 'Staff for cafés, restaurants and catering')],
      after=('تبرم العقود شهرياً أو سنوياً على نظام «أجير».', 'Contracts are monthly or annual, through the Ajeer system.')),
 dict(p=12, key='logistics', ar='الخدمات اللوجستية', en='Logistics Services',
      sar='التوصيل ونقل البضائع والتخزين وتأجير المركبات.', sen='Delivery, goods transport, storage and vehicle rental.',
      iar='تقدم «اطلبني إعمار» خدمات لوجستية تشمل التوصيل ونقل البضائع والتخزين وتأجير المركبات.',
      ien='OTLOBNY Emaar provides logistics services covering delivery, goods transport, storage and vehicle rental.',
      items=[('التوصيل', 'Delivery'), ('نقل البضائع', 'Goods transport'), ('التخزين', 'Storage'), ('تأجير المركبات', 'Vehicle rental')]),
]

# =============================================================== p1 cover
def p01():
    a, g = 43.2, 3.6
    s = (a + g) / math.sqrt(2); r1 = a / math.sqrt(2); rH = (3 * a + 2 * g) / math.sqrt(2)
    Hc = (236.0, 96.0); O = (Hc[0], Hc[1] - 2 * s)
    C = lambda i, j: (O[0] + (i - j) * s, O[1] + (i + j) * s)
    d = 2 * r1
    hero = prep('p01_hero_steel-erector', ST + 'contracting_steel-erector-on-beams_flickr-132069821.jpg', 2 * rH, 2 * rH, cx=.62, cy=.47, page='1')
    t1 = prep('p01_t_tower', ST + 'contracting_tower-construction-with-palms_flickr-3384156664.jpg', d, d, cx=.80, cy=.62, page='1')
    t2 = prep('p01_t_rope-access', ST + 'cleaning_rope-access-blue-glass-tower_flickr-16633802875.jpg', d, d, cx=.55, cy=.5, page='1')
    t3 = prep('p01_t_palm-park', ST + 'landscaping_palm-park-riyadh-museum_flickr-51949716085.jpg', d, d, cx=.45, cy=.42, page='1')
    t4 = prep('p01_t_workforce', ST + 'manpower_gulf-site-workforce_flickr-9836421046.jpg', d, d, cx=.52, cy=.62, page='1')
    cells = [(*Hc, rH, hero, 'img', 'Steel erector on a building frame under construction'),
             (*C(-1, 0), r1, 'url(#gcv)', 'fill'),
             (*C(-1, 1), r1, t1, 'img', 'Tower under construction with palms'),
             (*C(-1, 2), r1, t2, 'img', 'Rope-access team cleaning a glass tower'),
             (*C(0, 3), r1, t3, 'img', 'Palm park with stone landscaping'),
             (*C(1, 3), r1, t4, 'img', 'Site workforce in hard hats'),
             (*C(2, 3), r1, '#3758B0', 'fill'),
             (C(-1, 2)[0] - 16.5, Hc[1], 7.2, '#5AC584', 'fill')]
    X0, X1 = 18, 104            # m5: one text column; logo, Arabic title, rule and English all sit on it
    lw = X1 - X0
    return page(1, diamond_svg(cells, 'cv') + f'''
<img class="a" src="assets/logo/otlobny-emaar_logo_wordmark-colour_ar_v01.svg" alt="اطلبني" style="left:{X0}mm;top:22mm;width:{lw}mm;height:{lw*124.597/307.711:.2f}mm">
<div class="a" style="left:{X0}mm;top:124mm;width:{lw}mm">{ar('اطلبني إعمار', 'cv-k')}{ar('الملف التعريفي', 'cv-t')}</div>
<div class="a" style="left:{X0}mm;top:156mm;width:{lw}mm">{en('OTLOBNY Emaar', 'cv-ke')}{en('Company Profile', 'cv-te')}</div>
<div class="a cvline" style="left:{X0}mm;top:184mm;width:{lw}mm"></div>
<div class="a pair" style="left:{X0}mm;top:187.5mm;width:{lw}mm">{en('otlobny.net', 'cv-f')}{ar('المدينة المنورة', 'cv-fa')}</div>''', 'cover')

# =============================================================== p2 contents (type only; navy panel with the lattice)
def p02():
    rows = [(1, 3), (2, 4), (3, 6), (4, 14), (5, 15), (6, 17), (7, 19)]
    x0, x1 = 140, 279
    r = ''
    for k, (n, pg) in enumerate(rows):
        y = 60 + k * 18.5
        a_, e_ = SEC[n]
        r += (f'<a class="a toc" href="#p{pg}" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm">'
              f'{en(f"<span class=tn>{n:02d}</span>{e_}", "toc-e")}<span class="toc-n num">{pg:02d}</span>{ar(a_, "toc-a")}</a>')
    panel = (f'<div class="a dark-panel" style="left:0;top:0;width:118mm;height:210mm"></div>'
             + lattice(118, 210, 22, '#9BABD7', .35, 'lt2', filled=[(3, 7, '#5AC584'), (1, 10, '#3758B0'), (4, 12, '#3758B0')]))
    return page(2, panel +
                f'<img class="a" src="assets/logo/otlobny-emaar_logo_wordmark-white_ar_v01.svg" alt="اطلبني" style="left:18mm;top:170mm;width:40mm;height:{40*124.597/307.711:.2f}mm">' +
                flow(x0, x1, 20, f'<div class="pair">{en("Company Profile", "k")}{ar(DM + "الملف التعريفي", "k")}</div>' + pair_title('المحتويات', 'Contents')) +
                f'<div class="a hr" style="left:{x0}mm;top:60mm;width:{x1-x0}mm"></div>' + r +
                foot(2, x0, x1, 0))

# =============================================================== p3 about (Madinah plaza)
def p03():
    im = prep('p03_madinah-plaza', ST + 'opener_madinah-haram-plaza-umbrellas_wikimedia-masjid-al-nabawi-2024-3.jpg', 148.5, 210, cx=.42, cy=.5, page='3')
    x0, x1 = 18, 134
    a_ = ('«اطلبني إعمار» شركة ذات مسؤولية محدودة، تأسست عام 2021 في المدينة المنورة، وتعمل بالسجل التجاري رقم 4650245200. '
          'تقدم الشركة خدماتها في ستة مجالات: المقاولات العامة، والزراعة والتشجير، والصيانة، والنظافة، وتأمين الكوادر، والخدمات اللوجستية. وتخدم المنشآت الحكومية والتجارية والخاصة.')
    e_ = ('OTLOBNY Emaar is a limited liability company founded in 2021 in Al Madinah Al Munawwarah, Saudi Arabia, operating under Commercial Registration No. 4650245200. '
          'The company works in six fields: general contracting, landscaping, maintenance, cleaning, manpower supply and logistics services. It serves government, commercial and private facilities.')
    facts = [('سنة التأسيس', 'Founded', N('2021'), N('2021'), True),
             ('المقر', 'Based in', 'المدينة المنورة', 'Al Madinah Al Munawwarah', False),
             ('الشكل القانوني', 'Legal form', 'شركة ذات مسؤولية محدودة', 'Limited liability company', False),
             ('السجل التجاري', 'Commercial Registration', N('4650245200'), N('4650245200'), True)]
    rows = ''.join(f'<div class="fr">{en(f"<div class=fl2>{le}</div><div class=fv>{ve}</div>")}{ar(f"<div class=fl2>{la}</div><div class=fv>{va}</div>")}</div>'
                   for la, le, va, ve, _ in facts)
    return page(3, img(im, 148.5, 0, 148.5, 210, 'The Prophet’s Mosque plaza, Al Madinah Al Munawwarah') +
                flow(x0, x1, 20, kicker(1) + stack_title('من نحن', 'About Us') + '<div class="rule-g"></div>' + fcols(ar(a_, 'body'), en(e_, 'body'))) +
                f'<div class="a facts" style="left:{x0}mm;top:136mm;width:{x1-x0}mm">{rows}</div>' + foot(3, x0, x1, 1))

# =============================================================== p4 vision and mission (type only; lattice band)
def p04():
    va = 'تنطلق رؤيتنا في «اطلبني إعمار» نحو التوسع والتطور المستمر لتحقيق المنافسة في الأسواق المحلية في جميع مجالات عملنا، تماشياً مع رؤية المملكة العربية السعودية 2030.'
    ve = 'At OTLOBNY Emaar, our vision is continuous expansion and development, so that we compete in local markets across all our fields of work, in line with Saudi Vision 2030.'
    ma = 'نسعى في «اطلبني إعمار» إلى تزويد سوق العمل بالقوى العاملة الوطنية والأجنبية التي تتمتع بالكفاءات العالية في كثير من المهن الحرفية والفنية في مجالات خدماتنا، وفق أحدث المعايير المتبعة في المملكة العربية السعودية.'
    me = ('At OTLOBNY Emaar, we work to supply the labour market with highly competent national and expatriate manpower in a wide range of skilled trades '
          'and technical occupations across our fields of service, in line with the latest standards in the Kingdom of Saudi Arabia.')
    x0, x1 = 18, 279
    band = (f'<div class="a" style="left:0;top:0;width:297mm;height:62mm;background:var(--tint)"></div>'
            + lattice(297, 62, 20, '#9BABD7', .55, 'lt4', filled=[(10, 3, '#5AC584'), (11, 4, '#3758B0'), (12, 3, '#1F3162'), (12, 5, '#9BABD7')]))
    body = (flow(x0, x1, 72, kicker(2) + pair_title('رؤيتنا', 'Our Vision') + fcols(ar(va, 'lead vm'), en(ve, 'lead vm'), 'g24')) +
            f'<div class="a hr" style="left:{x0}mm;top:142mm;width:{x1-x0}mm"></div>' +
            flow(x0, x1, 147, f'<div class="pair base">{en("Our Mission", "t2")}{ar("رسالتنا", "t2")}</div>' + fcols(ar(ma, 'body'), en(me, 'body'), 'g24 mt3')))
    return page(4, band + body + foot(4, x0, x1, 2))

# =============================================================== p5 goals (navy)
def p05():
    goals = [
     ('تقديم أفضل الخدمات بجودة عالية لعملائنا الكرام رغبة في كسب رضاهم واستحسانهم.',
      'To deliver the best service, at high quality, and so earn our clients’ satisfaction and approval.'),
     ('السعي لعقد شراكات استراتيجية مع عدة جهات محلية ومؤسسات إقليمية وعالمية في مجالات الشركة المتخصصة وغيرها من المجالات الأخرى.',
      'To seek strategic partnerships with local bodies and with regional and international institutions, in the company’s specialist fields and beyond.'),
     ('التطوير الدائم والمتابعة المستمرة لمشاريع الشركة لتقديم أفضل الخدمات.',
      'To keep developing, and to monitor the company’s projects closely, so that we deliver the best service.'),
     ('توفير بيئة عمل جذابة لإطلاق كوادر من الخبرات البشرية للإبداع والتميز.',
      'To provide an attractive working environment in which experienced people can create and excel.')]
    x0, x1 = 18, 279
    out = flow(x0, x1, 20, kicker(2) + pair_title('أهدافنا', 'Our Goals'))
    for n, (ga, ge) in enumerate(goals):
        y = 58 + n * 33
        out += f'<div class="a hr dkhr" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm"></div>'
        out += at(x0, y + 4, 112, en(ge, 'lead'))
        out += at(x0 + 149, y + 4, 112, ar(ga, 'lead'))
        out += at(133.5, y + 3.2, 30, f'<div class="gnum num">{n+1:02d}</div>')
    out += f'<div class="a hr dkhr" style="left:{x0}mm;top:{58+4*33}mm;width:{x1-x0}mm"></div>'
    return page(5, out + foot(5, x0, x1, 2, dark=True), 'dark')

# =============================================================== p6 services overview (panorama band + typographic index)
def p06():
    # panorama cropped above the "TAIBA FRONT HOTEL" sign and left of the toilets sign (M5)
    im = prep('p06_madinah-panorama', ST + 'opener_madinah-haram-panorama_wikimedia-mezquita-del-profeta-dd01.jpg', 297, 68, box=(0, 340, 2660, 1240), cx=.5, cy=.62, page='6')
    x0, x1 = 18, 279
    out = img(im, 0, 0, 297, 68, 'The Prophet’s Mosque, Al Madinah Al Munawwarah')
    out += flow(x0, x1, 78, kicker(3) + pair_title('جهة واحدة لستة مجالات', 'One company, six fields'))
    cw, gx = (261 - 2 * 8) / 3, 8
    for n, s in enumerate(SERVICES):
        col, row = n % 3, n // 3
        x = x1 - (col + 1) * cw - col * gx
        y = 110 + row * 41
        out += (f'<a class="a ov" href="#p{s["p"]}" style="left:{x:.2f}mm;top:{y}mm;width:{cw:.2f}mm">'
                f'<div class="pair ovh">{en(f"Page {s["p"]:02d}", "ov-p")}{ar(f"<span class=ov-no>{N(f"{n+1:02d}")}</span>", "")}</div>'
                + fcols(ar(f'<div class="ov-a">{s["ar"]}</div><div class="ov-d">{s["sar"]}</div>'),
                        en(f'<div class="ov-e">{s["en"]}</div><div class="ov-d">{s["sen"]}</div>'), 'g5') + '</a>')
    return page(6, out + foot(6, x0, x1, 3))

# =============================================================== pp7–12 service master: diamond cluster + text
S_A, S_G = 50.0, 3.6
S_STEP = (S_A + S_G) / math.sqrt(2); S_R1 = S_A / math.sqrt(2); S_R2 = (2 * S_A + S_G) / math.sqrt(2)
def cell(hx, i, j, top=98.0):
    O = (hx, top - S_STEP)
    return (O[0] + (i - j) * S_STEP, O[1] + (i + j) * S_STEP)

PLAN = {   # (source, cx, cy, zoom, alt, illustrative?) — README round 3 page plan, no repeats
 'contracting': dict(hero=(ST + 'cover-hero_blue-glass-facade_wikimedia-glass-building-corner.jpg', .55, .55, 1.0, 'Glass facade of a completed building'),
                     cells={(1, 2): (ST + 'contracting_concrete-screeding-crew_flickr-4184357497.jpg', .62, .6, 1.0, 'Crew screeding a concrete slab'),
                            (2, 1): (ST + 'contracting_surveyor-theodolite_flickr-8756741875.jpg', .5, .42, 1.0, 'Surveyor with a theodolite')},
                     fills={(2, 2): 'navy'}),
 'landscaping': dict(cells={(0, 0): (ST + 'landscaping_date-palm-walkway-doha_flickr-7631829614.jpg', .5, .45, 1.0, 'Date palms along a walkway'),
                            (1, 1): (ST + 'landscaping_palms-dry-planting_flickr-4968666077.jpg', .45, .55, 1.0, 'Water-wise planting with palms')},
                     fills={(0, 1): 'navy', (1, 0): 'green', (2, 1): 'tint', (2, 2): 'blue'}),
 'maintenance': dict(hero=(ST + 'maintenance_hvac-gauges_wikimedia-379th-eces-8502255.jpg', .55, .5, 1.25, 'Technicians reading air-conditioning gauges'),
                     cells={(1, 2): (ST + 'maintenance_rooftop-ac-units-technician_flickr-54752357237.jpg', .3335, .5, 1.0, 'Technician among rooftop air-conditioning units'),
                            (2, 1): (ST + 'contracting-electrical_distribution-board_wikimedia-small-house-distribution-panel-2.jpg', .5, .5, 1.5, 'Electrical distribution board')},
                     fills={(2, 2): 'navy'}),
 'cleaning':    dict(cells={(0, 0): (ST + 'cleaning_rope-access-window-cleaner_flickr-4797579546.jpg', .72, .45, 1.0, 'Rope-access window cleaning'),
                            (1, 1): (ST + 'cleaning_mop-and-trolley-floor_flickr-24978817211.jpg', .55, .6, 1.0, 'Floor cleaning with mop and trolley')},
                     fills={(1, 0): 'navy', (0, 1): 'green', (1, 2): 'tint', (2, 2): 'blue'}),
 'manpower':    dict(cells={(1, 0): (ST + 'manpower_waiter-pouring-tea_flickr-38075436525.jpg', .42, .45, 1.0, 'Waiter pouring tea'),
                            (0, 1): (ST + 'manpower_catering-table-setup-overhead_flickr-6160161346.jpg', .55, .5, 1.0, 'Staff setting a catering table'),
                            (1, 1): ('assets/derived/mockup_cleaning-team_retouched_v03.png', .5, .32, 1.0, 'Service team in branded uniforms, illustrative image', True)},
                     fills={(0, 0): 'navy', (0, -1): 'tint'}),
 'logistics':   dict(cells={(0, 0): (ST + 'logistics_warehouse-racking-aisle_flickr-4324416999.jpg', .5, .55, 1.0, 'Warehouse racking aisle'),
                            (1, 1): ('assets/derived/mockup_car-scooter-facade_retouched_v03.png', .74, .52, 1.0, 'Branded delivery scooter, illustrative image', True)},
                     fills={(0, 1): 'navy', (1, 0): 'green', (0, -1): 'tint'}),
}
BOX = {ST + 'manpower_catering-table-setup-overhead_flickr-6160161346.jpg': (190, 0, 1024, 682),     # event banner cropped off
       ST + 'landscaping_palm-park-riyadh-museum_flickr-51949716085.jpg': (0, 0, 1024, 640),        # figure on the lawn cropped off
       'assets/derived/mockup_cleaning-team_retouched_v03.png': (192, 0, 1344, 1024)}
FILL = {'navy': 'url(#gS)', 'green': '#5AC584', 'blue': '#3758B0', 'tint': '#E8ECF7'}

def service(i, s):
    p, k = s['p'], s['key']
    pl = PLAN[k]
    img_left = (i % 2 == 0)
    x_half = 0 if img_left else 148.5
    hx = 66.0 if img_left else 148.5 - 66.0      # m2: outer diamonds bleed (about 7 mm past the trim)
    cells, caps = [], ''
    if 'hero' in pl:
        src, cx, cy, z, alt = pl['hero']
        f = prep(f'p{p:02d}_{k}_hero', src, 2 * S_R2, 2 * S_R2, cx, cy, zoom=z, box=BOX.get(src), page=str(p))
        c = cell(hx, 0, 0); cells.append((hx, c[1] + S_STEP, S_R2, f, 'img', alt))
    for (ij, spec) in pl['cells'].items():
        src, cx, cy, z, alt = spec[:5]
        illus = len(spec) > 5
        f = prep(f'p{p:02d}_{k}_{ij[0]}{ij[1]}', src, 2 * S_R1, 2 * S_R1, cx, cy, zoom=z, box=BOX.get(src), page=str(p), graded=not illus)
        c = cell(hx, *ij); cells.append((c[0], c[1], S_R1, f, 'img', alt))
        if illus:   # m3: every client mockup carries the label, directly under its diamond
            caps += (f'<div class="a pair illus" style="left:{x_half + c[0] - 30:.2f}mm;top:{c[1] + S_R1 + 1.6:.2f}mm;width:60mm">'
                     f'{en("Illustrative image", "cap")}{ar("صورة توضيحية", "cap")}</div>')
    for ij, col in pl['fills'].items():
        c = cell(hx, *ij); cells.append((c[0], c[1], S_R1, f'url(#gs{p})' if col == 'navy' else FILL[col], 'fill'))
    # small green accent in the left notch of the 2x2 block (same device as the cover)
    svg = diamond_svg(cells, f's{p}', 148.5, 210, x_half, 0, label=f'{s["en"]}: photographs')
    x0, x1 = (148.5 + 14, 279) if img_left else (18, 148.5 - 14)
    inner = (kicker(3, f'{i+1:02d} / 06') + stack_title(s['ar'], s['en']) + '<div class="rule-g"></div>' +
             fcols(ar(s['iar'], 'lead sv'), en(s['ien'], 'lead sv')) + lgrid(s['items'], s.get('after')))
    return page(p, svg + caps + flow(x0, x1, 20, inner) + foot(p, x0, x1, 3))

# =============================================================== p13 fleet in pictures (purely pictorial, M3)
def p13():
    R = lambda n: f'assets/derived/mockup_{n}_retouched_v03.png'
    G, BH = 3.6, 80.0
    W3 = (297 - 2 * G) / 3
    a = prep('p13_truck-rear34', R('truck-rear34'), W3, BH, .5, .55, page='13', graded=False)
    b = prep('p13_truck-side', R('truck-side'), W3, BH, .5, .5, page='13', graded=False)
    c = prep('p13_truck-front34', R('logistics-trucks'), W3, BH, cx=.577, cy=.5, box=(0, 0, 830, 582), page='13', graded=False)
    f = prep('p13_truck-front', R('truck-front'), 72, 72, .5, .5, page='13', graded=False)
    r = prep('p13_truck-rear', R('truck-rear'), 72, 72, .5, .5, page='13', graded=False)
    rider = prep('p13_rider', R('delivery-rider'), 46, 94.2, box=(290, 0, 790, 1024), page='13', graded=False, whiten=True)
    out = img(a, 0, 0, W3, BH, 'Branded box truck, rear three-quarter view, illustrative image')
    out += img(b, W3 + G, 0, W3, BH, 'Branded box truck, side view, illustrative image')
    out += img(c, 2 * (W3 + G), 0, W3, BH, 'Branded box truck, front three-quarter view, illustrative image')
    out += img(r, 207, 98, 72, 72, 'Branded box truck, rear view, illustrative image')
    out += img(rider, 125.5, 92, 46, 94.2, 'Delivery rider with branded bag, illustrative image', 'mult')
    out += img(f, 18, 98, 72, 72, 'Branded box truck, front view, illustrative image')
    out += f'<div class="a pair" style="left:18mm;top:{BH+3}mm;width:261mm">{en("03 — Our Services · Logistics", "k")}{ar(DM + N("03") + " — خدماتنا · الخدمات اللوجستية", "k")}</div>'
    out += f'<div class="a pair" style="left:18mm;top:174mm;width:261mm">{en("Illustrative images", "cap")}{ar("صور توضيحية", "cap")}</div>'
    return page(13, out + foot(13, 18, 279, 3))

# =============================================================== p14 why
def p14():
    pts = [
     ('جهة واحدة لستة مجالات', 'المقاولات العامة، والزراعة والتشجير، والصيانة، والنظافة، وتأمين الكوادر، والخدمات اللوجستية، في عقد مع شركة واحدة.',
      'One company, six fields', 'General contracting, landscaping, maintenance, cleaning, manpower supply and logistics, under a contract with a single company.'),
     ('كوادر نظامية على نظام «أجير»', 'نوفر كوادر نظامية مؤهلة، بعقود على نظام «أجير».',
      'Compliant manpower through Ajeer', 'Qualified, legally compliant staff, contracted through the Ajeer system.'),
     ('عقود شهرية وسنوية', 'يختار العميل مدة التعاقد المناسبة في خدمة تأمين الكوادر.',
      'Monthly and annual contracts', 'In manpower supply, the client chooses the contract term that suits.'),
     ('خدمة للقطاعات الثلاثة', 'نخدم المنشآت الحكومية والتجارية والخاصة.',
      'Three sectors served', 'Government, commercial and private facilities.'),
     ('من الدراسة إلى التنفيذ', 'ننفذ المشاريع الإنشائية بجميع مراحلها، ابتداءً من الدراسة الفنية والمخططات التصميمية.',
      'From study to execution', 'Construction projects at every stage, starting with the technical study and design drawings.'),
     ('فريق مؤهل ومعايير الصحة المهنية', 'فريق احترافي من الكوادر المؤهلة، ويجري تأمين الكوادر وفقاً لمعايير الصحة المهنية.',
      'A qualified team and occupational health standards', 'A professional team of qualified staff; manpower is supplied in line with occupational health standards.')]
    x0, x1 = 18, 279
    out = flow(x0, x1, 20, kicker(4) + pair_title('لماذا «اطلبني إعمار»', 'Why OTLOBNY Emaar'))
    for n, (ta, da, te, de) in enumerate(pts):
        y = 52 + n * 23.4
        out += f'<div class="a hr" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm"></div>'
        out += at(x0, y + 3, 112, en(f'<div class="wt">{te}</div><div class="wd">{de}</div>'))
        out += at(x0 + 149, y + 3, 112, ar(f'<div class="wt">{ta}</div><div class="wd">{da}</div>'))
        out += at(133.5, y + 3.2, 30, f'<div class="wnum num">{n+1:02d}</div>')
    out += f'<div class="a hr" style="left:{x0}mm;top:{52+6*23.4}mm;width:{x1-x0}mm"></div>'
    return page(14, out + foot(14, x0, x1, 4), 'tint')

# =============================================================== pp15–16 works: one block master, three works (M6)
WORKS = [
 dict(n=1, ar='تصميم وتركيب محطات انتظار الحافلات', en='Design and installation of bus waiting shelters',
      sar='صممت «اطلبني إعمار» محطات انتظار الحافلات وركبتها، وهي محطات تنظم حركة الركاب وسير الحافلات، بجودة عالية واحترافية في التنفيذ.',
      sen='OTLOBNY Emaar designed and installed bus waiting shelters. Built to a high standard, they help organise passenger flow and bus movement.',
      chips=[('تصميم', 'Design'), ('تركيب', 'Installation')],
      cap=('صورة مقدمة من العميل', 'Photograph supplied by the client')),
 dict(n=2, ar='الغرفة التجارية والصناعية في المدينة المنورة', en='Madinah Chamber of Commerce and Industry',
      sar='قدمت «اطلبني إعمار» خدمات التشغيل والصيانة والنظافة للغرفة التجارية والصناعية في المدينة المنورة.',
      sen='OTLOBNY Emaar provided operation, maintenance and cleaning services for the Madinah Chamber of Commerce and Industry.',
      chips=[('تشغيل', 'Operation'), ('صيانة', 'Maintenance'), ('نظافة', 'Cleaning')],
      cap=('تصور معماري مقدم من العميل', 'Architectural rendering supplied by the client')),
 # C1 (CD ruling): the hotel as a work, no stated scope, no body text, no chips
 dict(n=3, ar='فندق دار التقوى', en='Dar Al Taqwa Hotel', sar=None, sen=None, chips=None,
      cap=('صورة مقدمة من العميل', 'Photograph supplied by the client')),
]
def chips(lst, lang):
    return ''.join(f'<span class="chip">{a_ if lang == "ar" else e_}</span>' for a_, e_ in lst)

def work_text(w):
    t = (f'<div class="pair wkno">{en(f"{w["n"]:02d} / 03", "k")}{ar(N(f"{w["n"]:02d} / 03"), "k")}</div>' +
         stack_title(w['ar'], w['en'], 'tw'))
    if w['sar']:
        t += '<div class="rule-g"></div>' + fcols(ar(w['sar'], 'body'), en(w['sen'], 'body'))
        t += fcols(ar(f'<div class="scl">نطاق العمل</div><div class="chips">{chips(w["chips"], "ar")}</div>'),
                   en(f'<div class="scl">Scope</div><div class="chips">{chips(w["chips"], "en")}</div>'), 'mt6')
    return t

def caption(w, x, y, wd):
    return f'<div class="a pair capr" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{wd:.2f}mm">{en(w["cap"][1], "cap")}{ar(w["cap"][0], "cap")}</div>'

def p15():
    w = WORKS[0]
    # m10: litter cropped out (crop, not retouch): x from 400 px; 550 x 471 px at 105 mm = 133 ppi
    iw = 105.0; ih = iw * 471 / 550
    im = prep('p15_bus-shelter', 'assets/photos/bus-shelter.png', iw, ih, box=(400, 0, 950, 471), page='15')
    out = f'<div class="a panel" style="left:0;top:0;width:141mm;height:210mm"></div>'
    iy = 105 - ih / 2 + 4                       # image block centred on the page's optical middle
    out += img(im, 18, iy, iw, ih, 'Bus waiting shelter installed by the company') + caption(w, 18, iy + ih + 3, iw)
    out += flow(155, 279, 20, kicker(5))
    out += flow(155, 279, 105 - ih / 2 + 4, work_text(w))
    return page(15, out + foot(15, 155, 279, 5))

def p16():
    """M2: two balanced columns, one per work, each image -> caption -> (8 mm) -> number -> title (-> text, scope)."""
    a_, b_ = WORKS[1], WORKS[2]
    top = 32.0
    xr0, xr1, xl0, xl1 = 156.5, 279, 18, 140.5
    # right column (read first): Chamber rendering 644 x 454 px at 88 mm = 186 ppi
    cw = 88.0; chh = cw * 454 / 644
    im1 = prep('p16_chamber', 'assets/photos/chamber-building.png', cw, chh, box=(0, 0, 644, 454), page='16')
    # left column: Dar Al Taqwa entrance 335 x 597 px at 62 mm = 137 ppi (largest size that stays above 130 ppi)
    dw = 62.0; dh = dw * 597 / 335
    im2 = prep('p16_dar-al-taqwa_entrance', 'assets/photos/dar-al-taqwa-hotel-entrance.jpg', dw, dh, page='16')
    out = f'<div class="a panel" style="left:0;top:0;width:148.5mm;height:210mm"></div>' + flow(18, 279, 20, kicker(5))
    out += img(im1, xr1 - cw, top, cw, chh, 'Madinah Chamber of Commerce building, architectural rendering')
    out += caption(a_, xr1 - cw, top + chh + 2.2, cw)
    out += flow(xr0, xr1, top + chh + 2.2 + 8 + 8, work_text(a_), 'sm')
    out += img(im2, xl1 - dw, top, dw, dh, 'Entrance of Dar Al Taqwa Hotel')
    out += caption(b_, xl1 - dw, top + dh + 2.2, dw)
    out += flow(xl0, xl1, top + dh + 2.2 + 8 + 8, work_text(b_), 'dt')
    return page(16, out + foot(16, 18, 279, 5))

# =============================================================== pp17–18 partners
PARTNERS = [
 ('existing-01_madinah-award-foundation', 'Partner logo: green dome emblem'), ('existing-02_al-madinah-region-development-authority', 'Al Madinah Region Development Authority'),
 ('existing-03_al-maqar', 'Al Maqar'), ('existing-04_we-ar-spa', 'Partner logo: AR Spa mark'), ('existing-05_mawaddah', 'Mawaddah'),
 ('existing-06_imagine-more', 'Imagine More Travel Agency'), ('existing-07_hsh', 'Partner logo: HSH mark'), ('existing-08_taibah-cooperative', 'Cooperative Taibah'),
 ('existing-09_dar-al-taqwa-hotel', 'Dar Al Taqwa Hotel'), ('existing-10_dallah-taibah-hotel', 'Dallah Taibah Hotel'), ('existing-11_al-madinah-harmony', 'Al Madinah Harmony'),
 ('existing-12_tiny-house', 'Tiny House'), ('existing-13_platinum', 'Platinum'), ('existing-14_madinah-chamber', 'Almadinah Almunawarah Chamber'),
 ('existing-15_manarat-taba-hotel', 'Partner logo: column emblem'), ('existing-16_hippo', 'Hippo'), ('existing-17_taza', 'Taza'),
 ('existing-18_arabic-calligraphic-mark', 'Partner logo: Arabic calligraphic mark'),
 ('new-01_manazil-al-mukhtara', 'Manazil Al-Mukhtara Company'), ('new-02_novotel', 'Novotel Hotels & Resorts'), ('new-03_keeta', 'Keeta'), ('new-04_jahez', 'Jahez'),
 ('new-05_medina-dates-festival', 'International Medina Festival Dates'), ('new-06_hungerstation', 'HungerStation'), ('new-07_rotana', 'Rotana'),
 ('new-08_chop-and-co', 'Chop & Co'), ('new-09_zero', 'ZERO'), ('new-10_shawarma-laila', 'Shawarma Laila'), ('new-11_loomi', 'Loomi'),
 ('new-12_the-end', 'The End Burgers / Fries'), ('new-13_le-meridien', 'Le Méridien'), ('new-14_al-esra-cabin', 'Al Esra Cabin'),
]
assert len(PARTNERS) == 32 and len({s for s, _ in PARTNERS}) == 32
AD_W = {'existing-01': 40.0, 'existing-02': 40.0, 'existing-03': 29.5, 'existing-04': 28.0, 'existing-05': 33.0, 'existing-06': 36.0,
        'existing-07': 32.0, 'existing-08': 26.0, 'existing-09': 66.0, 'existing-10': 40.0, 'existing-11': 56.0, 'existing-12': 34.0,
        'existing-13': 31.0, 'existing-14': 38.0, 'existing-15': 40.0, 'existing-16': 16.6, 'existing-17': 28.0, 'existing-18': 30.0,
        'new-01': 30.1, 'new-02': 38.0, 'new-03': 31.0, 'new-04': 28.0, 'new-05': 17.4, 'new-06': 32.0, 'new-07': 38.0, 'new-08': 28.0,
        'new-09': 38.0, 'new-10': 34.6, 'new-11': 31.5, 'new-12': 31.0, 'new-13': 44.0, 'new-14': 24.0}
HEAVY = {'existing-12': .87, 'new-03': .87, 'new-06': .87, 'new-12': .87, 'new-11': .87, 'new-09': .9}   # m8: heavy black marks -13 %
FAINT_H = {'existing-01': 24.0, 'existing-08': 22.0, 'existing-11': 22.0, 'existing-09': 22.0}            # m8: faint marks get more room
SCALE, H_MAX = 0.86, 19.5
TIER_B = {f'existing-{n:02d}' for n in (1, 2, 3, 5, 8, 9, 10, 11, 15, 17)}
TIER_C = {'existing-07', 'existing-18'}
EFFECTIVE_W = {'existing-02_al-madinah-region-development-authority': 121 / 0.86, 'existing-17_taza': 143 / 0.87}
PLOG = []

def logo(stem, alt, cx, cy):
    im = Image.open(BASE / 'assets/partners-transparent' / f'{stem}.png'); W, H = im.size
    A = np.array(im.getchannel('A')).astype(float)
    bb = im.getchannel('A').getbbox(); w, h = bb[2] - bb[0], bb[3] - bb[1]
    key = stem.split('_')[0]
    sc = SCALE * HEAVY.get(key, 1.0)
    k = min(AD_W[key] * sc / w, FAINT_H.get(key, H_MAX) * HEAVY.get(key, 1.0) / h)
    eff = (EFFECTIVE_W[stem] / W) if stem in EFFECTIVE_W else 1.0
    floor = 100 if key in TIER_B else 80 if key in TIER_C else 0
    if floor:
        k = min(k, 25.4 / floor * eff)
    ppi = 25.4 / k * eff
    ys, xs = np.mgrid[0:H, 0:W]; m = A.sum() or 1
    gx, gy = (A * xs).sum() / m, (A * ys).sum() / m
    bx, by = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    ox = bx + float(np.clip((gx - bx) / 2, -.12 * w, .12 * w)); oy = by + float(np.clip((gy - by) / 2, -.12 * h, .12 * h))
    PLOG.append((stem, round(w * k, 1), round(h * k, 1), round(ppi)))
    if stem == 'new-13_le-meridien':
        wmm = w * k; hmm = wmm * 78 / 540
        return f'<img class="a" src="assets/partners-transparent/new-13_le-meridien.svg" alt="{alt}" style="left:{cx-wmm/2:.2f}mm;top:{cy-hmm/2:.2f}mm;width:{wmm:.2f}mm;height:{hmm:.2f}mm">'
    return f'<img class="a" src="assets/partners-transparent/{stem}.png" alt="{alt}" style="left:{cx-ox*k:.2f}mm;top:{cy-oy*k:.2f}mm;width:{W*k:.2f}mm;height:{H*k:.2f}mm">'

def partners(p):
    items = PARTNERS[:16] if p == 17 else PARTNERS[16:]
    x0, x1 = 18, 279
    cw, ch, top = (x1 - x0) / 4, 33.0, 56.0
    out = flow(x0, x1, 20, kicker(6, f'{p-16:02d} / 02') + pair_title('شركاء النجاح', 'Partners in Success'))
    for r in range(5):
        out += f'<div class="a hr" style="left:{x0}mm;top:{top + r*ch}mm;width:{x1-x0}mm"></div>'
    for c in range(1, 4):   # m8: vertical rules run the full height of the grid, top rule to bottom rule
        out += f'<div class="a vr" style="left:{x0 + c*cw}mm;top:{top}mm;height:{4*ch}mm"></div>'
    for n, (s, a_) in enumerate(items):
        out += logo(s, a_, x1 - (n % 4 + .5) * cw, top + (n // 4 + .5) * ch)
    if p == 18:
        out += f'<div class="a pair" style="left:{x0}mm;top:{top+4*ch+2.5}mm;width:{x1-x0}mm">{en("All logos are the property of their respective owners.", "cap")}{ar("جميع الشعارات ملك لأصحابها.", "cap")}</div>'
    return page(p, out + foot(p, x0, x1, 6))

# =============================================================== p19 contact (navy), p20 back cover with photo credits
def p19():
    rows = [('الهاتف', 'Tel', '<a href="tel:+966549555514">054 955 5514</a>'),
            ('البريد الإلكتروني', 'Email', '<a href="mailto:info@otlobny.co">info@otlobny.co</a>'),
            ('الموقع الإلكتروني', 'Website', '<a href="https://otlobny.net">otlobny.net</a>'),
            ('السجل التجاري', 'Commercial Registration', '4650245200')]
    x0, x1 = 48, 249
    out = f'<img class="a" src="assets/logo/otlobny-emaar_logo_wordmark-reversed_ar_v01.svg" alt="اطلبني" style="left:{148.5-34}mm;top:20mm;width:68mm;height:{68*124.597/307.711:.2f}mm">'
    out += flow(x0, x1, 58, kicker(7) + f'<div class="pair base">{en("Contact", "t2")}{ar("تواصل معنا", "t2")}</div>')
    for n, (la, le, v) in enumerate(rows):
        y = 80 + n * 14
        out += f'<div class="a hr dkhr" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm"></div>'
        out += f'<div class="a crow" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm">{en(le, "cl")}<div class="cv num">{v}</div>{ar(la, "cl")}</div>'
    y = 80 + 4 * 14
    out += f'<div class="a hr dkhr" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm"></div>'
    out += flow(x0, x1, y + 5, fcols(ar('<div class="cl">العنوان</div><div class="ca">طريق الأمير عبدالمجيد بن عبدالعزيز، المدينة المنورة، المملكة العربية السعودية</div>'),
                                   en('<div class="cl">Address</div><div class="ca">Prince Abdulmajeed bin Abdulaziz Road, Al Madinah Al Munawwarah, Saudi Arabia</div>'), 'g30'))
    return page(19, out + foot(19, 18, 279, 7, dark=True), 'dark flat')

def p20():
    att, free = [], []
    for fn in sorted(CREDITS_USED, key=lambda f: CREDIT[f][1].lower()):
        t, a_, lic, src, sa = CREDIT[fn]
        s = f'“{t}”, {a_}, {lic}, {src}' + (' — modified version shared under the same licence' if sa else '')
        (free if lic in FREE else att).append(s)
    cr_en = ('<p><b>Photo credits.</b> ' + '; '.join(att) + '.</p>'
             '<p>All photographs above are modified (cropped and colour-graded; small third-party marks removed where present). '
             'Licences: creativecommons.org/licenses.</p>'
             '<p><b>No attribution required:</b> ' + '; '.join(free) + '.</p>'
             '<p><b>Client images.</b> Project photographs and the architectural rendering were supplied by the client. '
             'Images marked “Illustrative image” are illustrative visuals supplied by the client; they do not show actual vehicles or staff.</p>')
    cr_ar = ('<p><b>حقوق الصور.</b> الصور الفوتوغرافية للخدمات صور توضيحية مرخصة بتراخيص المشاع الإبداعي أو ملكية عامة، '
             'ومنسوبة إلى أصحابها في القائمة الإنجليزية المجاورة، وقد عدلت بالقص والمعالجة اللونية.</p>'
             '<p><b>صور العميل.</b> صور الأعمال والتصور المعماري مقدمة من العميل. '
             'الصور الموسومة «صورة توضيحية» تصاميم توضيحية مقدمة من العميل، ولا تمثل مركبات أو فرق عمل فعلية.</p>')
    out = (f'<img class="a" src="assets/logo/otlobny-emaar_logo_wordmark-colour_ar_v01.svg" alt="اطلبني" style="left:{148.5-40}mm;top:42mm;width:80mm;height:{80*124.597/307.711:.2f}mm">'
           f'<div class="a pair" style="left:{148.5-40}mm;top:{42+80*124.597/307.711+8}mm;width:80mm">{en("otlobny.net", "cv-f")}{ar("المدينة المنورة", "cv-fa")}</div>'
           f'<div class="a hr" style="left:18mm;top:132mm;width:261mm"></div>'
           + at(18, 136, 168, en(cr_en, 'credit')) + at(196, 136, 83, ar(cr_ar, 'credit')))
    return page(20, out, 'back')

# =============================================================== CSS
CSS = r'''
@font-face{font-family:"Tajawal";font-weight:400;src:url("assets/fonts/Tajawal-Regular.ttf") format("truetype")}
@font-face{font-family:"Tajawal";font-weight:500;src:url("assets/fonts/Tajawal-Medium.ttf") format("truetype")}
@font-face{font-family:"Tajawal";font-weight:700;src:url("assets/fonts/Tajawal-Bold.ttf") format("truetype")}
@font-face{font-family:"Tajawal";font-weight:800;src:url("assets/fonts/Tajawal-ExtraBold.ttf") format("truetype")}
@font-face{font-family:"IBM Plex Sans";font-weight:400;src:url("assets/fonts/IBMPlexSans-Regular.ttf") format("truetype")}
@font-face{font-family:"IBM Plex Sans";font-weight:500;src:url("assets/fonts/IBMPlexSans-Medium.ttf") format("truetype")}
@font-face{font-family:"IBM Plex Sans";font-weight:600;src:url("assets/fonts/IBMPlexSans-SemiBold.ttf") format("truetype")}
@font-face{font-family:"IBM Plex Sans";font-weight:700;src:url("assets/fonts/IBMPlexSans-Bold.ttf") format("truetype")}
:root{--blue:#3758B0;--green:#5AC584;--navy:#1F3162;--tint:#F7F8FC;--peri:#9BABD7;--grey:#525456;--mute:#5F6573;--hair:.3pt solid #C9D1EA}
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:"IBM Plex Sans",sans-serif;font-synthesis:none;hyphens:none;-webkit-hyphens:none;font-kerning:normal}
a{color:inherit;text-decoration:none}
.page{position:relative;width:297mm;height:210mm;overflow:hidden;background:#fff;break-after:page;page-break-after:always}
.page:last-child{break-after:auto;page-break-after:auto}
.page.tint{background:var(--tint)}
.page.dark{background:linear-gradient(115deg,#1F3162 0%,#22386F 55%,#2B458A 100%)}
.page.dark.flat{background:#1F3162}
.dark-panel{background:#1F3162}
.panel{background:var(--tint)}
.a{position:absolute}
img.ph{display:block;object-fit:cover}
img.mult{mix-blend-mode:multiply}
.ar{font-family:"Tajawal",sans-serif;direction:rtl;text-align:right;color:var(--navy);letter-spacing:0}
.en{font-family:"IBM Plex Sans",sans-serif;direction:ltr;text-align:left;color:var(--grey)}
.num{font-family:"IBM Plex Sans",sans-serif;direction:ltr;unicode-bidi:isolate;letter-spacing:0}
.dark .ar,.dark .en{color:#fff}
p,.body,.lead,.wd,.ca,.ov-d{text-wrap:pretty}
h2,.t1,.t2,.wt,.li span,.ov-a,.ov-e{text-wrap:balance}
.nw{white-space:nowrap}
.pair{display:flex;direction:ltr;justify-content:space-between;align-items:flex-start;gap:6mm}
.pair.base{align-items:baseline}
.ar.k,.ar .k{font-weight:700;font-size:9.5pt;line-height:1.6;color:var(--blue);display:flex;align-items:center;gap:1.6mm}
.en.k,.en .k{font-weight:600;font-size:6.8pt;line-height:2.1;color:var(--blue);text-transform:uppercase;letter-spacing:.14em}
.dark .k{color:var(--green) !important}
.kick{margin-bottom:3mm}
.ar.t1,.ar .t1{font-weight:800;font-size:31pt;line-height:1.3;color:var(--navy)}
.en.t1,.en .t1{font-weight:600;font-size:21pt;line-height:1.15;color:var(--blue)}
.dark .t1{color:#fff !important}
.ar.t2,.ar .t2{font-weight:700;font-size:17pt;line-height:1.5;color:var(--navy)}
.en.t2,.en .t2{font-weight:600;font-size:13pt;line-height:1.3;color:var(--navy)}
.dark .t2{color:#fff !important}
.ar.lead,.ar .lead{font-weight:500;font-size:13pt;line-height:1.75}
.en.lead,.en .lead{font-weight:400;font-size:10.5pt;line-height:1.55}
.ar.lead.sv{font-size:12pt;line-height:1.75} .en.lead.sv{font-size:10pt;line-height:1.55}
.ar.lead.vm{font-weight:700;font-size:16pt;line-height:1.7} .en.lead.vm{font-weight:500;font-size:12.5pt;line-height:1.45;color:var(--navy)}
.ar.body,.ar .body{font-weight:400;font-size:11pt;line-height:1.8}
.en.body,.en .body{font-weight:400;font-size:9pt;line-height:1.6}
.ar.cap,.ar .cap{font-weight:500;font-size:8pt;line-height:1.6;color:var(--grey)}
.en.cap,.en .cap{font-weight:500;font-size:6.5pt;line-height:2;color:var(--grey);text-transform:uppercase;letter-spacing:.1em}
.dm{display:inline-block;flex:none;width:1.5mm;height:1.5mm;margin:.3mm;background:var(--green);border-radius:16%;transform:rotate(45deg)}
.hr{border-top:var(--hair);height:0}
.dkhr{border-top:.3pt solid rgba(255,255,255,.35)}
.vr{border-left:var(--hair);width:0}
.rule-g{width:14mm;border-top:1.2pt solid var(--green);margin:5mm 0 6mm auto}
/* flow text areas */
.flow{display:flex;flex-direction:column}
h2.st{display:block;width:100%}
.ar.t1.st{margin-top:0} .en.t1.st{margin-top:1.5mm}
.fcols{display:grid;direction:ltr;grid-template-columns:1fr 1fr;column-gap:7mm;align-items:start}
.fcols.g24{column-gap:24mm} .fcols.g30{column-gap:30mm} .fcols.g5{column-gap:5mm}
.mt3{margin-top:3mm} .mt6{margin-top:6mm}
/* M2: bilingual list, one grid row per item */
.lg{margin-top:8mm;border-bottom:var(--hair)}
.lr{display:grid;direction:ltr;grid-template-columns:.86fr 1.14fr;column-gap:6mm;align-items:baseline;border-top:var(--hair);padding:2.2mm 0 2.3mm;min-height:10mm}
.lr.last{border-top:0;align-items:start;padding-top:3.5mm}
.lr>.li{display:flex;align-items:baseline;gap:2.4mm}
.li .dm{align-self:flex-start}
.ar.li{font-weight:500;font-size:11pt;line-height:1.55;color:var(--navy)} .ar.li .dm{margin-top:2.05mm}
.en.li{font-weight:500;font-size:8.8pt;line-height:1.5;color:var(--navy)} .en.li .dm{margin-top:1.55mm}
.ar.after{font-size:10.5pt;line-height:1.7;text-wrap:balance} .en.after{font-size:8.6pt;line-height:1.5}
/* footer */
.ft{display:flex;direction:ltr;justify-content:space-between;align-items:baseline}
.ft .fl{font-size:6.5pt;font-weight:500;color:var(--mute)}
.ft .en.fl{text-transform:uppercase;letter-spacing:.1em}
.ft .ar.fl{font-size:8pt;display:flex;gap:3mm;align-items:baseline}
.ft .folio{font-family:"IBM Plex Sans";font-weight:600;font-size:7.5pt;color:var(--navy)}
.ft.dk .fl{color:rgba(255,255,255,.82)} .ft.dk .folio{color:#fff}
/* cover */
.cv-k{font-weight:700;font-size:15pt;line-height:1.5;color:var(--blue)}
.cv-t{font-weight:800;font-size:33pt;line-height:1.3;color:var(--navy);margin-top:.5mm;white-space:nowrap}
.cv-ke{font-weight:600;font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;color:var(--blue)}
.cv-te{font-weight:500;font-size:23pt;line-height:1.15;color:var(--navy);margin-top:1.2mm}
.cvline{border-top:.6pt solid var(--green);height:0}
.cv-f{font-weight:500;font-size:8pt;color:var(--grey)} .cv-fa{font-weight:500;font-size:9.5pt;color:var(--grey)}
/* contents */
.toc{display:flex;direction:ltr;justify-content:space-between;align-items:center;height:18.5mm;border-bottom:var(--hair)}
.toc-e{font-weight:500;font-size:9.5pt;color:var(--grey);width:52mm}
.toc-a{font-weight:700;font-size:14pt;color:var(--navy);width:70mm;white-space:nowrap}
.toc-n{font-weight:600;font-size:15pt;color:var(--blue);width:16mm;text-align:center}
.tn{display:inline-block;font-family:"IBM Plex Sans";font-weight:600;color:var(--blue);font-size:8pt;width:8mm}
.ar .tn{text-align:right;margin-left:2mm}
/* about facts: m6 — fixed label and value heights in both languages, so the values share a baseline */
.facts{border-bottom:var(--hair)}
.fr{display:grid;direction:ltr;grid-template-columns:1fr 1fr;column-gap:7mm;border-top:var(--hair);padding:1.6mm 0 1.2mm}
.fl2{height:4.2mm;line-height:4.2mm;font-weight:500;color:var(--mute)}
.en .fl2{font-size:6.5pt;letter-spacing:.1em;text-transform:uppercase} .ar .fl2{font-size:8pt}
.fv{height:6.2mm;line-height:6.2mm;font-weight:700;color:var(--navy);white-space:nowrap}
.ar .fv{font-size:11.5pt} .en .fv{font-size:9.5pt;font-weight:600}
.fv .num{font-weight:600;font-size:12pt;color:var(--blue)}
/* goals and why */
.gnum{font-family:"IBM Plex Sans";font-weight:400;font-size:30pt;line-height:1;color:var(--green);text-align:center}
.wnum{font-family:"IBM Plex Sans";font-weight:600;font-size:15pt;line-height:1;color:var(--blue);text-align:center}
.ar .wt{font-weight:700;font-size:13pt;line-height:1.5;color:var(--navy)} .en .wt{font-weight:600;font-size:10pt;line-height:1.35;color:var(--navy)}
.ar .wd{font-weight:400;font-size:10.5pt;line-height:1.7;margin-top:.6mm} .en .wd{font-size:8.6pt;line-height:1.5;margin-top:.8mm}
/* overview */
.ov{display:block;border-top:1pt solid var(--navy);padding-top:2.4mm}
.ovh{margin-bottom:1.8mm;align-items:center}
.ov-no{font-family:"IBM Plex Sans";font-weight:600;font-size:13pt;color:var(--blue)}
.ov-p{font-size:6.5pt;font-weight:600;color:var(--blue);letter-spacing:.1em;text-transform:uppercase}
.ov-a{font-weight:700;font-size:12.5pt;line-height:1.45;color:var(--navy)}
.ov-e{font-weight:600;font-size:9pt;line-height:1.35;color:var(--navy);padding-top:.8mm}
.ar .ov-d{font-size:9.5pt;line-height:1.65;margin-top:1mm;color:var(--navy)} .en .ov-d{font-size:7.8pt;line-height:1.45;margin-top:1.2mm}
/* works */
.wkno{margin-bottom:1mm}
.capr{flex-direction:column;align-items:stretch;gap:0} .capr .ar{order:-1}
.ar.t1.tw{font-size:25pt;line-height:1.4} .en.t1.tw{font-size:16pt;line-height:1.2}
.dt .ar.t1.tw{font-size:22pt;line-height:1.35} .dt .en.t1.tw{font-size:14pt}
.sm .ar.t1.tw{font-size:17pt;line-height:1.35;white-space:nowrap} .sm .en.t1.tw{font-size:12pt} .sm .rule-g{margin:3mm 0 3.5mm auto} .sm .mt6{margin-top:3.5mm} .sm .ar.body{font-size:10.5pt;line-height:1.7}
.scl{font-weight:600;color:var(--blue)} .en .scl{font-size:6.5pt;letter-spacing:.1em;text-transform:uppercase} .ar .scl{font-size:9pt;font-weight:700}
.chips{display:flex;flex-wrap:nowrap;gap:1.6mm;margin-top:2mm}
.ar .chips{justify-content:flex-start}
.chip{display:inline-flex;align-items:center;height:6.2mm;padding:0 2.6mm;border:.5pt solid var(--blue);border-radius:3.1mm;color:var(--navy);white-space:nowrap}
.ar .chip{font-weight:500;font-size:9.5pt;padding-top:.6mm} .en .chip{font-weight:500;font-size:7.2pt;letter-spacing:.03em}
/* contact: M1 — labels white at 82 % on flat navy (about 9:1) */
.crow{display:flex;direction:ltr;justify-content:space-between;align-items:center;height:14mm}
.cl{font-weight:500;color:rgba(255,255,255,.82) !important}
.en.cl,.en .cl{font-size:7.5pt;letter-spacing:.1em;text-transform:uppercase}
.ar.cl,.ar .cl{font-size:10pt}
.crow>.en,.crow>.ar{width:60mm}
.cv{font-weight:500;font-size:16pt;color:#fff;text-align:center}
.ca{font-size:9.5pt;line-height:1.6;margin-top:1mm} .ar .ca{font-size:11pt;line-height:1.8}
/* back cover credits: M1 — grey on white 7.6:1; English 7 pt, Arabic 8.5 pt */
.credit{color:var(--grey)}
.en.credit{font-size:7pt;line-height:1.5} .ar.credit{font-size:8.5pt;line-height:1.75}
.credit p+p{margin-top:1.6mm}
.credit b{font-weight:600;color:var(--navy)}
'''

def build():
    pages = [p01(), p02(), p03(), p04(), p05(), p06()]
    pages += [service(i, s) for i, s in enumerate(SERVICES)]
    pages += [p13(), p14(), p15(), p16(), partners(17), partners(18), p19(), p20()]
    html = ('<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
            '<title>اطلبني إعمار — الملف التعريفي | OTLOBNY Emaar — Company Profile (draft v06)</title>\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<style>{CSS}</style>\n</head>\n<body>\n' + ''.join(pages) + '</body>\n</html>\n')
    # m13: one diacritics convention — none in running text (fatha/damma/kasra/shadda/sukun/tanwin are stripped
    # except tanwin fath on «ـاً», which the outline uses as part of the spelling)
    body = re.sub(r'[ٌ-ْ]', '', html.replace('اً', '')).replace('', 'اً')
    OUT.write_text(body, encoding='utf-8')
    print('wrote', OUT.name, len(pages), 'pages')
    for r in LOG:
        print('  img p%-3s %-44s %-92s crop %s -> %s mm, %d ppi, %s' % r)
    rep = {s: sorted(p) for s, p in USED.items() if len(p) > 1}
    print('sources on more than one page:', rep or 'none')
    for r in PLOG:
        print('  logo %-48s %5.1f x %4.1f mm  %4d ppi' % r)
    print('credits used:', len(CREDITS_USED))

if __name__ == '__main__':
    build()
