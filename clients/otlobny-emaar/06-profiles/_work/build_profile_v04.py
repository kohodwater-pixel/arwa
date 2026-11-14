#!/usr/bin/env python3
"""otlobny-emaar — company profile v04 (NEW design, not a patch of v03).

Writes:
  06-profiles/otlobny-emaar_company-profile_screen_ar-en_v04.html   (editable source, assets linked from assets/)
  06-profiles/assets/derived/v04_*.jpg                               (cropped, retouched and graded photographs)

Copy: content-outline.md (+ status block), brand-context.md decision log (client rulings 2026-11-13/14).
Data reused from build_profile_v02/v03.py (texts, partner list and sizing); the layout is new.
Run:  python3 06-profiles/_work/build_profile_v04.py
"""
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np
import math, json

BASE = Path(__file__).resolve().parent.parent           # 06-profiles/
OUT = BASE / 'otlobny-emaar_company-profile_screen_ar-en_v04.html'
DER = BASE / 'assets/derived'
ST = 'assets/stock/'
LOG = []          # image log: page, file, source, crop px, size mm, effective ppi
CREDITS_USED = set()

# =============================================================== photo library: credits (CREDITS.md / stock README)
CREDIT = {
 'contracting_steel-erector-on-beams_flickr-132069821.jpg': ('Steel Worker', 'billjacobus1', 'CC BY 2.0', 'Flickr'),
 'contracting_rebar-worker_wikimedia-rebar-worker-j2.jpg': ('Rebar worker J2', 'Jamain', 'CC BY-SA 3.0', 'Wikimedia Commons'),
 'contracting_surveyor-theodolite_flickr-8756741875.jpg': ('A new generation of industrial leaders', 'DFID – UK Department for International Development', 'CC BY 2.0', 'Flickr'),
 'contracting_concrete-screeding-crew_flickr-4184357497.jpg': ('Concrete screeding', 'USACE Europe District', 'CC BY 2.0', 'Flickr'),
 'contracting_site-at-blue-hour_flickr-2146788503.jpg': ('BIG 06', 'seier+seier', 'CC BY 2.0', 'Flickr'),
 'landscaping_palm-promenade-lawn_flickr-19570930662.jpg': ('New Canary Island Date Palms – Torquay', 'Torquay Palms', 'CC BY-SA 2.0', 'Flickr'),
 'landscaping_palms-dry-planting_flickr-4968666077.jpg': ('Area 1', 'Port of San Diego', 'CC BY 2.0', 'Flickr'),
 'landscaping_gardener-trimmer_flickr-54576923958.jpg': ('Man using a trimmer', 'nenad53', 'CC BY 2.0', 'Flickr'),
 'cleaning_mop-and-trolley-floor_flickr-24978817211.jpg': ('Cleaner with mop and uniform', 'aqua.mech', 'CC BY 2.0', 'Flickr'),
 'cleaning_rope-access-window-cleaner_flickr-4797579546.jpg': ('Window Cleaner', 'Malte Sörensen', 'CC BY 2.0', 'Flickr'),
 'cleaning_floor-scrubbers-lobby_wikimedia-floor-scrubbers.jpg': ('Floor scrubbers', 'Z22', 'CC BY-SA 4.0', 'Wikimedia Commons'),
 'logistics_white-box-truck_flickr-51928284838.jpg': ('BV79175', 'Lav Ulv', 'CC BY 2.0', 'Flickr'),
 'logistics_warehouse-racking-aisle_flickr-4324416999.jpg': ('Sealey Warehouse', 'toolstop', 'CC BY 2.0', 'Flickr'),
 'logistics_forklift-in-motion_flickr-4325154436.jpg': ('Sealey Warehouse', 'toolstop', 'CC BY 2.0', 'Flickr'),
 'manpower_waiter-pouring-tea_flickr-38075436525.jpg': ('Waiter serving tea', 'www.ralfsteinberger.com', 'CC BY 2.0', 'Flickr'),
 'manpower_catering-table-setup-overhead_flickr-6160161346.jpg': ('Plano Cenital Catering', 'TEDxLasPalmas', 'CC BY-SA 2.0', 'Flickr'),
 'opener_madinah-haram-plaza-umbrellas_wikimedia-masjid-al-nabawi-2024-3.jpg': ('Masjid al-Nabawi 2024 (3)', 'Radosław Botev', 'CC BY 3.0 PL', 'Wikimedia Commons'),
 'opener_madinah-haram-panorama_wikimedia-mezquita-del-profeta-dd01.jpg': ('Prophet’s Mosque, Medina (DD 01)', 'Diego Delso', 'CC BY-SA 4.0', 'Wikimedia Commons'),
 # no attribution required (CC0 / US Gov public domain) — listed on the credits line as such
 'cover-hero_blue-glass-facade_wikimedia-glass-building-corner.jpg': ('Glass building corner', 'Jonathan Simcoe', 'CC0 1.0', 'Wikimedia Commons'),
 'maintenance_hvac-gauges_wikimedia-379th-eces-8502255.jpg': ('379th ECES HVAC technicians', 'U.S. Air Force, A1C Derrick Boleyn', 'Public domain', 'Wikimedia Commons'),
 'landscaping_date-palm_wikimedia-date-palm-tree-landscape.jpg': ('Date palm tree landscape', 'Srianix', 'CC0 1.0', 'Wikimedia Commons'),
 'contracting-electrical_distribution-board_wikimedia-small-house-distribution-panel-2.jpg': ('Small house distribution panel 2', 'Retired electrician', 'CC0 1.0', 'Wikimedia Commons'),
}

# =============================================================== retouches (on a copy in memory; sources are never written)
def _inpaint(a, mask, iters=600):
    """Fill masked pixels by repeated 4-neighbour averaging (membrane fill) — enough for small flat areas."""
    a = a.astype(float).copy()
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = ys.min() - 2, ys.max() + 3, xs.min() - 2, xs.max() + 3
    sub, m = a[y0:y1, x0:x1], mask[y0:y1, x0:x1]
    sub[m] = sub[~m].mean(axis=0)
    for _ in range(iters):
        avg = (np.roll(sub, 1, 0) + np.roll(sub, -1, 0) + np.roll(sub, 1, 1) + np.roll(sub, -1, 1)) / 4
        sub[m] = avg[m]
    rng = np.random.default_rng(4)
    noise = sub[~m].std(axis=0) * 0.35
    sub[m] += rng.normal(0, 1, (m.sum(), 3)) * noise
    a[y0:y1, x0:x1] = sub
    return np.clip(a, 0, 255).astype(np.uint8)

def retouch(fname, im):
    a = np.array(im)
    if fname.startswith('logistics_white-box-truck'):
        # Danish number plate and the operator's name on the sun visor: replaced by smooth local colour (not legible)
        for box in [(324, 520, 384, 544), (338, 271, 390, 291)]:
            l, t, r, b = box
            m = np.zeros(a.shape[:2], bool); m[t:b, l:r] = True
            a = _inpaint(a, m, 400)
    elif fname.startswith('contracting_rebar-worker'):
        # small white maker logo on the worker's black cap: letters filled with the cap colour
        l, t, r, b = 1700, 1105, 1790, 1215
        reg = a[t:b, l:r].astype(int)
        light = (reg.sum(axis=2) > 230) | (reg[..., 0] > reg[..., 2] + 4)
        m = np.zeros(a.shape[:2], bool); m[t:b, l:r] = light
        m = np.array(Image.fromarray(m.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(5))) > 0
        a = _inpaint(a, m, 800)
    elif fname.startswith('maintenance_hvac-gauges'):
        # maker name and logo on the blue manifold label: lettering filled with the label blue (label shape kept)
        from PIL import ImageDraw
        poly = [(1754, 1350), (2058, 1258), (2068, 1326), (1766, 1410)]
        pm = Image.new('L', (a.shape[1], a.shape[0]), 0); ImageDraw.Draw(pm).polygon(poly, fill=255)
        inside = np.array(pm) > 0
        r_, g_, b_ = [a[..., i].astype(int) for i in range(3)]
        dark_blue = (b_ > r_ + 35) & (r_ < 90) & ((r_ + g_ + b_) < 330)
        m = inside & ~dark_blue
        m = (np.array(Image.fromarray(m.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3))) > 0) & inside
        # normalised convolution from the label's own dark blue: keeps its shading, loses the lettering
        from scipy.ndimage import gaussian_filter
        w = (inside & dark_blue & ~m).astype(float)
        fill = np.stack([gaussian_filter(a[..., i] * w, 6) for i in range(3)], -1) / (gaussian_filter(w, 6)[..., None] + 1e-6)
        yy, xx = np.nonzero(m)
        rng = np.random.default_rng(7)
        a = a.copy()
        a[yy, xx] = np.clip(fill[yy, xx] + rng.normal(0, 2.0, (len(yy), 3)), 0, 255).astype(np.uint8)
        pm = Image.fromarray((m * 255).astype(np.uint8))
        soft = Image.fromarray(a).filter(ImageFilter.GaussianBlur(1.2))
        edge = np.array(pm.filter(ImageFilter.MaxFilter(5))) > 0
        edge &= ~(np.array(pm.filter(ImageFilter.MinFilter(5))) > 0)
        a[edge] = np.array(soft)[edge]
    elif fname.startswith('mockup_car-scooter-facade'):
        # banner slogan «خدمتك بجودة تهمنا» is not approved copy (content-gaps, new item d): filled with the banner's navy
        l, t, r, b = 1226, 176, 1336, 296
        reg = a[t:b, l:r].astype(int)
        m = np.zeros(a.shape[:2], bool); m[t:b, l:r] = reg.sum(axis=2) > 200
        m = np.array(Image.fromarray(m.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(7))) > 0
        a = _inpaint(a, m, 600)
    return Image.fromarray(a)

# =============================================================== one brand grade for every photograph
NAVY = np.array([31, 49, 98]) / 255
TINT = np.array([246, 248, 253]) / 255
def grade(im, s=1.0):
    s = s * 1.15
    """Soft cool editorial grade: slight desaturation, shadows drawn into the brand navy, highlights to the light tint,
    gentle contrast. The same function (strength s) for every photograph so they read as one family."""
    a = np.asarray(im).astype(float) / 255
    L = (a * [0.2126, 0.7152, 0.0722]).sum(axis=2, keepdims=True)
    a = L + (a - L) * (1 - 0.18 * s)                       # desaturate 18 %
    ws = 0.34 * s * (1 - L) ** 2.2                          # shadows -> navy
    a = a * (1 - ws) + NAVY * ws
    wh = 0.10 * s * L ** 2                                  # highlights -> light tint
    a = a * (1 - wh) + TINT * wh
    a = a * (1 - 0.04 * s) + np.array([0.0, 0.004, 0.02]) * s   # whisper of cool in the mid-tones
    a = 0.5 + (a - 0.5) * (1 + 0.06 * s)                    # gentle contrast
    return Image.fromarray((np.clip(a, 0, 1) * 255 + .5).astype(np.uint8))

_cache = {}
def load(src):
    if src not in _cache:
        im = Image.open(BASE / src).convert('RGB')
        _cache[src] = retouch(Path(src).name, im)
    return _cache[src]

def prep(name, src, w_mm, h_mm, cx=.5, cy=.5, zoom=1.0, box=None, page='', s=1.0, max_ppi=300):
    """Crop src to the frame's aspect around focus (cx, cy) (fractions), zoom>1 crops tighter; never upscales.
    Grades and saves assets/derived/v04_<name>.jpg; logs the effective ppi at the placed size."""
    im = load(src)
    W, H = im.size
    asp = w_mm / h_mm
    if box:
        l, t, r, b = box
        W2, H2 = r - l, b - t
        im = im.crop(box); W, H = W2, H2
        ox, oy = l, t
    else:
        ox = oy = 0
    cw = min(W, H * asp) / zoom; ch = cw / asp
    l = min(max(0, cx * W - cw / 2), W - cw); t = min(max(0, cy * H - ch / 2), H - ch)
    c = im.crop((round(l), round(t), round(l + cw), round(t + ch)))
    ppi = c.size[0] / (w_mm / 25.4)
    tw = min(c.size[0], round(w_mm / 25.4 * max_ppi))
    if tw < c.size[0]:
        c = c.resize((tw, round(tw / asp)), Image.LANCZOS)
    c = grade(c, s)
    if name == 'p13_rider':   # studio cut-out: lift the near-white ground to pure white so it merges with the page
        arr = np.asarray(c).copy(); arr[(arr > 238).all(axis=2)] = 255; c = Image.fromarray(arr)
    out = DER / f'v04_{name}.jpg'
    c.save(out, quality=86, optimize=True, progressive=True)
    fn = Path(src).name
    if fn in CREDIT:
        CREDITS_USED.add(fn)
    LOG.append((page, out.name, src, (round(ox + l), round(oy + t), round(ox + l + cw), round(oy + t + ch)), f'{w_mm:.1f} x {h_mm:.1f}', round(ppi)))
    return f'assets/derived/{out.name}'

def img(src, x, y, w, h, alt, cls=''):
    return f'<img class="a ph {cls}" src="{src}" alt="{alt}" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm">'

# =============================================================== shared type pieces
DM = '<i class="dm"></i>'
def kick(ar, en):
    return ar, en
def ar(html, cls='', style=''):
    return f'<div class="ar {cls}" lang="ar" dir="rtl" style="{style}">{html}</div>'
def en(html, cls='', style=''):
    return f'<div class="en {cls}" lang="en" dir="ltr" style="{style}">{html}</div>'
def at(x, y, w, inner, extra=''):
    return f'<div class="a" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;{extra}">{inner}</div>'
def N(s):
    return f'<span class="num" dir="ltr">{s}</span>'

def cols(x0, x1, y, ar_html, en_html, gap=7.0, extra=''):
    """The one bilingual structure: inside any text area, English column on the left, Arabic column on the right."""
    w = (x1 - x0 - gap) / 2
    return at(x0, y, w, en_html, extra) + at(x0 + w + gap, y, w, ar_html, extra)

def flow(x0, x1, y, inner):
    return f'<div class="a flow" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm">{inner}</div>'
def kpair(kar, ken):
    return f'<div class="pair">{en(ken, "k")}{ar(DM + kar, "k")}</div>'
def stack_title(tar, ten):
    """Half-page text areas: the Arabic title on its own line at the right, the English title under it at the left."""
    return f'<h2 class="ar t1 st" lang="ar" dir="rtl">{tar}</h2><h2 class="en t1 st" lang="en" dir="ltr">{ten}</h2>'
def fcols(ar_html, en_html, cls=''):
    return f'<div class="fcols {cls}">{en_html}{ar_html}</div>'

def head(x0, x1, y, kar, ken, tar, ten, big=False):
    """Kicker + title pair, shared baseline: Arabic on the right edge of the text area, English on the left edge."""
    c = 't1b' if big else 't1'
    k = (f'<div class="a pair" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm">'
         f'{en(ken, "k")}{ar(DM + kar, "k")}</div>')
    t = (f'<div class="a pair base" style="left:{x0}mm;top:{y+6.5}mm;width:{x1-x0}mm">'
         f'{en(ten, c)}{ar(tar, c)}</div>')
    return k + t

def foot(p, x0, x1, sar, sen, dark=False):
    folio = f'<b class="folio num" dir="ltr">{p:02d}</b>'
    return (f'<div class="a ft{" dk" if dark else ""}" style="left:{x0}mm;top:197mm;width:{x1-x0}mm">'
            f'{en(sen + " &nbsp;·&nbsp; OTLOBNY Emaar", "fl")}'
            f'{ar(f"<span>{sar} · اطلبني إعمار</span>{folio}", "fl")}</div>')

def page(p, body, cls=''):
    return f'<section class="page {cls}" id="p{p}" data-page="{p}">\n{body}\n</section>\n'

# =============================================================== copy (from content-outline.md; v02/v03 data)
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
      items=[('تشغيل وصيانة أنظمة التكييف المركزية', 'Operation and maintenance of central air-conditioning systems'),
             ('تشغيل وصيانة أنظمة المصاعد', 'Operation and maintenance of lift systems')]),
 dict(p=10, key='cleaning', ar='النظافة', en='Cleaning',
      sar='نظافة المباني ومكافحة الآفات للقطاعات الحكومية والتجارية والخاصة.',
      sen='Building cleaning and pest control for the government, commercial and private sectors.',
      iar='تقدم «اطلبني إعمار» خدمات نظافة عالية المستوى يمكن الوثوق بها، للقطاعات الحكومية والخاصة والتجارية.',
      ien='OTLOBNY Emaar provides high-standard, dependable cleaning services for the government, private and commercial sectors.',
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
      after=('تُبرم العقود شهرياً أو سنوياً على نظام «أجير».', 'Contracts are monthly or annual, through the Ajeer system.')),
 dict(p=12, key='logistics', ar='الخدمات اللوجستية', en='Logistics Services',
      sar='التوصيل ونقل البضائع والتخزين وتأجير المركبات.', sen='Delivery, goods transport, storage and vehicle rental.',
      iar='تقدّم «اطلبني إعمار» خدمات لوجستية تشمل التوصيل ونقل البضائع والتخزين وتأجير المركبات.',
      ien='OTLOBNY Emaar provides logistics services covering delivery, goods transport, storage and vehicle rental.',
      items=[('التوصيل', 'Delivery'), ('نقل البضائع', 'Goods transport'), ('التخزين', 'Storage'), ('تأجير المركبات', 'Vehicle rental')]),
]

WORKS = [
 dict(p=15, ar='تصميم وتركيب محطات انتظار الحافلات', en='Design and installation of bus waiting shelters',
      sar='صممت «اطلبني إعمار» محطات انتظار الحافلات وركبتها، وهي محطات تنظم حركة الركاب وسير الحافلات، بجودة عالية واحترافية في التنفيذ.',
      sen='OTLOBNY Emaar designed and installed bus waiting shelters, which help organise passengers and bus movement, to a high standard of execution.',
      chips=[('تصميم', 'Design'), ('تركيب', 'Installation')]),
 dict(p=16, ar='الغرفة التجارية والصناعية في المدينة المنورة', en='Madinah Chamber of Commerce and Industry',
      sar='قدمت «اطلبني إعمار» خدمات التشغيل والصيانة والنظافة للغرفة التجارية والصناعية في المدينة المنورة.',
      sen='OTLOBNY Emaar provided operation, maintenance and cleaning services for the Madinah Chamber of Commerce and Industry.',
      chips=[('تشغيل', 'Operation'), ('صيانة', 'Maintenance'), ('نظافة', 'Cleaning')]),
 # client ruling 2026-11-14: Dar Al Taqwa Hotel replaces the earlier hotel; scope ASSUMED (same pattern), to be confirmed
 dict(p=17, ar='فندق دار التقوى', en='Dar Al Taqwa Hotel',
      sar='قدمت «اطلبني إعمار» خدمات الصيانة والنظافة لفندق دار التقوى.',
      sen='OTLOBNY Emaar provided maintenance and cleaning services for Dar Al Taqwa Hotel.',
      chips=[('صيانة', 'Maintenance'), ('نظافة', 'Cleaning')]),
]

# =============================================================== page 1 — cover: one large image, several small (diamond lattice)
def diamond_svg(cells, defs_id):
    """cells: list of (cx, cy, half_diag, fill_or_src, kind, alt). Rounded squares turned 45 degrees, clipped images."""
    defs, body = '', ''
    for n, (cx, cy, r, f, kind, alt) in enumerate(cells):
        side = r * math.sqrt(2)
        rx = side * .12
        rect = (f'<rect x="{cx-side/2:.3f}" y="{cy-side/2:.3f}" width="{side:.3f}" height="{side:.3f}" rx="{rx:.3f}" '
                f'transform="rotate(45 {cx:.3f} {cy:.3f})"')
        if kind == 'img':
            defs += f'<clipPath id="{defs_id}{n}">{rect}/></clipPath>'
            body += (f'<image href="{f}" x="{cx-r:.3f}" y="{cy-r:.3f}" width="{2*r:.3f}" height="{2*r:.3f}" '
                     f'preserveAspectRatio="xMidYMid slice" clip-path="url(#{defs_id}{n})"><title>{alt}</title></image>')
        else:
            body += f'{rect} fill="{f}"/>'
    return (f'<svg class="a" style="left:0;top:0" width="297mm" height="210mm" viewBox="0 0 297 210" role="img" aria-label="Photographs of the six service fields, illustrative">'
            f'<defs><linearGradient id="gC" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1F3162"/><stop offset="1" stop-color="#3758B0"/></linearGradient>{defs}</defs>{body}</svg>')

def p01():
    a, g = 43.2, 3.6
    s = (a + g) / math.sqrt(2)
    r1 = a / math.sqrt(2)
    rH = (3 * a + 2 * g) / math.sqrt(2)
    Hc = (236.0, 96.0)
    O = (Hc[0], Hc[1] - 2 * s)
    def C(i, j):
        return (O[0] + (i - j) * s, O[1] + (i + j) * s)
    d = lambda name: 2 * r1   # mm size of the bounding square of a small cell
    hero = prep('cover_hero_steel-frame', ST + 'contracting_steel-erector-on-beams_flickr-132069821.jpg', 2 * rH, 2 * rH, cx=.62, cy=.47, page='1')
    t_hvac = prep('cover_t_hvac', ST + 'maintenance_hvac-gauges_wikimedia-379th-eces-8502255.jpg', d(0), d(0), cx=.66, cy=.52, zoom=1.7, page='1')
    t_palm = prep('cover_t_palms', ST + 'landscaping_palm-promenade-lawn_flickr-19570930662.jpg', d(0), d(0), cx=.70, cy=.52, page='1')
    t_mop = prep('cover_t_mop', ST + 'cleaning_mop-and-trolley-floor_flickr-24978817211.jpg', d(0), d(0), cx=.62, cy=.55, page='1')
    t_aisle = prep('cover_t_aisle', ST + 'logistics_warehouse-racking-aisle_flickr-4324416999.jpg', d(0), d(0), cx=.5, cy=.55, page='1')
    cells = [
        (*Hc, rH, hero, 'img', 'Steel frame under construction'),
        (*C(-1, 0), r1, 'url(#gC)', 'fill', ''),
        (*C(-1, 1), r1, t_hvac, 'img', 'Technician reading air-conditioning gauges'),
        (*C(-1, 2), r1, t_palm, 'img', 'Landscaped grounds with palms'),
        (*C(0, 3), r1, t_mop, 'img', 'Floor cleaning with mop and trolley'),
        (*C(1, 3), r1, t_aisle, 'img', 'Warehouse racking aisle'),
        (*C(2, 3), r1, '#3758B0', 'fill', ''),
    ]
    notch = (C(-1, 2)[0] - 16.5, Hc[1], 7.2, '#5AC584', 'fill', '')
    cells.append(notch)
    svg = diamond_svg(cells, 'cv')
    return page(1, svg + f'''
<img class="a" src="assets/logo/otlobny-emaar_logo_wordmark-colour_ar_v01.svg" alt="اطلبني" style="left:18mm;top:22mm;width:76mm;height:{76*124.597/307.711:.2f}mm">
<div class="a" style="left:18mm;top:126mm;width:86mm">{ar('اطلبني إعمار', 'cv-k')}{ar('الملف التعريفي', 'cv-t')}</div>
<div class="a" style="left:18mm;top:157mm;width:86mm">{en('OTLOBNY Emaar', 'cv-ke')}{en('Company Profile', 'cv-te')}</div>
<div class="a cvline" style="left:18mm;top:184mm;width:86mm"></div>
<div class="a" style="left:18mm;top:187.5mm;width:86mm;display:flex;justify-content:space-between;direction:ltr">{en('otlobny.net', 'cv-f')}{ar('المدينة المنورة', 'cv-fa')}</div>
''', 'cover')

# =============================================================== page 2 — contents
def p02():
    im = prep('p02_glass', ST + 'cover-hero_blue-glass-facade_wikimedia-glass-building-corner.jpg', 118, 210, cx=.62, cy=.5, page='2')
    rows = [('من نحن', 'About Us', 3), ('رؤيتنا ورسالتنا', 'Vision and Mission', 4), ('أهدافنا', 'Our Goals', 5), ('خدماتنا', 'Our Services', 6),
            ('لماذا «اطلبني إعمار»', 'Why OTLOBNY Emaar', 14), ('أعمالنا', 'Our Work', 15), ('شركاء النجاح', 'Partners in Success', 18), ('تواصل معنا', 'Contact', 20)]
    x0, x1 = 136, 279
    r = ''
    for n, (a_, e_, pg) in enumerate(rows):
        y = 58 + n * 16.4
        r += (f'<a class="a toc" href="#p{pg}" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm">'
              f'{en(e_, "toc-e")}<span class="toc-n num">{pg:02d}</span>{ar(a_, "toc-a")}</a>')
    return page(2, img(im, 0, 0, 118, 210, 'Glass facade') +
                f'<img class="a" src="assets/logo/otlobny-emaar_logo_wordmark-white_ar_v01.svg" alt="اطلبني" style="left:18mm;top:178mm;width:34mm;height:{34*124.597/307.711:.2f}mm">' +
                head(x0, x1, 20, 'الملف التعريفي', 'Company Profile', 'المحتويات', 'Contents') +
                f'<div class="a hr" style="left:{x0}mm;top:{58-0.1}mm;width:{x1-x0}mm"></div>' + r +
                foot(2, x0, x1, 'المحتويات', 'Contents'))

# =============================================================== page 3 — about
def p03():
    im = prep('p03_madinah-plaza', ST + 'opener_madinah-haram-plaza-umbrellas_wikimedia-masjid-al-nabawi-2024-3.jpg', 148.5, 210, cx=.42, cy=.5, page='3', s=.8)
    x0, x1 = 18, 134
    a_ = ('«اطلبني إعمار» شركة ذات مسؤولية محدودة، تأسست عام 2021 في المدينة المنورة، وتعمل بالسجل التجاري رقم 4650245200.'
          '<br>تقدم الشركة خدماتها في ستة مجالات: المقاولات العامة، والزراعة والتشجير، والصيانة، والنظافة، وتأمين الكوادر، والخدمات اللوجستية. وتخدم المنشآت الحكومية والتجارية والخاصة.')
    e_ = ('OTLOBNY Emaar is a limited liability company founded in 2021 in Al Madinah Al Munawwarah, Saudi Arabia, operating under Commercial Registration No. 4650245200.'
          '<br>The company works in six fields: general contracting, landscaping, maintenance, cleaning, manpower supply and logistics services. It serves government, commercial and private facilities.')
    facts = [('سنة التأسيس', 'Founded', N('2021'), N('2021'), True),
             ('المقر', 'Based in', 'المدينة المنورة', 'Al Madinah Al Munawwarah', False),
             ('الشكل القانوني', 'Legal form', 'شركة ذات مسؤولية محدودة', 'Limited liability company', False),
             ('السجل التجاري', 'Commercial Registration', N('4650245200'), N('4650245200'), True)]
    f = ''
    for n, (la, le, va, ve, isnum) in enumerate(facts):
        y = 140 + n * 13.2
        f += (f'<div class="a hr" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm"></div>' +
              cols(x0, x1, y + 2.2, ar(f'<div class="fl2">{la}</div><div class="fv{" fvn" if isnum else ""}">{va}</div>'),
                   en(f'<div class="fl2">{le}</div><div class="fv{" fvn" if isnum else ""}">{ve}</div>')))
    return page(3, img(im, 148.5, 0, 148.5, 210, 'The Prophet’s Mosque plaza, Al Madinah Al Munawwarah') +
                flow(x0, x1, 20, kpair(N('01'), '01') + stack_title('من نحن', 'About Us') +
                     '<div class="rule-g" style="margin:5mm 0 5mm auto"></div>' + fcols(ar(a_, 'body'), en(e_, 'body'))) + f +
                f'<div class="a hr" style="left:{x0}mm;top:{140+4*13.2}mm;width:{x1-x0}mm"></div>' +
                foot(3, x0, x1, 'من نحن', 'About Us'))

# =============================================================== page 4 — vision and mission
def p04():
    im = prep('p04_madinah-panorama', ST + 'opener_madinah-haram-panorama_wikimedia-mezquita-del-profeta-dd01.jpg', 297, 96, cx=.395, cy=.5, zoom=1.42, page='4', s=.8)
    va = 'تنطلق رؤيتنا في «اطلبني إعمار» نحو التوسع والتطور المستمر لتحقيق المنافسة في الأسواق المحلية في جميع مجالات عملنا، تماشياً مع رؤية المملكة العربية السعودية 2030.'
    ve = 'At OTLOBNY Emaar, our vision is continuous expansion and development, so that we compete in local markets across all our fields of work, in line with Saudi Vision 2030.'
    ma = 'نسعى في «اطلبني إعمار» إلى تزويد سوق العمل بالقوى العاملة الوطنية والأجنبية التي تتمتع بالكفاءات العالية في كثير من المهن الحرفية والفنية في مجالات خدماتنا، وفق أحدث المعايير المتبعة في المملكة العربية السعودية.'
    me = 'At OTLOBNY Emaar, we work to supply the labour market with highly competent national and expatriate manpower in a wide range of skilled trades and technical occupations across our fields of service, to the latest standards applied in the Kingdom of Saudi Arabia.'
    x0, x1 = 18, 279
    blk = lambda t, b, lang: (f'<div class="vm-t">{t}</div><div class="vm-b">{b}</div>')
    body = (head(x0, x1, 104, N('02'), '02', 'رؤيتنا', 'Our Vision') +
            cols(x0, x1, 125, ar(va, 'lead'), en(ve, 'lead'), gap=24) +
            f'<div class="a hr" style="left:{x0}mm;top:153mm;width:{x1-x0}mm"></div>' +
            f'<div class="a pair base" style="left:{x0}mm;top:157mm;width:{x1-x0}mm">{en("Our Mission", "t2")}{ar("رسالتنا", "t2")}</div>' +
            cols(x0, x1, 167, ar(ma, 'body'), en(me, 'body'), gap=24))
    return page(4, img(im, 0, 0, 297, 96, 'The Prophet’s Mosque, Al Madinah Al Munawwarah') + body + foot(4, x0, x1, 'رؤيتنا ورسالتنا', 'Vision and Mission'))

# =============================================================== page 5 — goals (dark page)
def p05():
    goals = [
     ('تقديم أفضل الخدمات بجودة عالية لعملائنا الكرام رغبة في كسب رضاهم واستحسانهم.',
      'To deliver the best service, at high quality, and so earn our clients’ satisfaction and approval.'),
     ('السعي لعقد شراكات استراتيجية مع عدة جهات محلية ومؤسسات إقليمية وعالمية في مجالات الشركة المتخصصة وغيرها من المجالات الأخرى.',
      'To seek strategic partnerships with local bodies and with regional and international institutions, in the company’s specialist fields and beyond.'),
     ('التطوير الدائم والمتابعة المستمرة لمشاريع الشركة لتقديم أفضل الخدمات.',
      'To keep developing, and to follow up the company’s projects closely, so that we deliver the best service.'),
     ('توفير بيئة عمل جذابة لإطلاق كوادر من الخبرات البشرية للإبداع والتميز.',
      'To provide an attractive working environment in which experienced people can create and excel.')]
    x0, x1 = 18, 279
    out = head(x0, x1, 20, N('02'), '02', 'أهدافنا', 'Our Goals')
    for n, (ga, ge) in enumerate(goals):
        y = 58 + n * 33
        out += f'<div class="a hr dkhr" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm"></div>'
        out += at(x0, y + 4, 112, en(ge, 'lead'))
        out += at(x0 + 149, y + 4, 112, ar(ga, 'lead'))
        out += at(130.5 + 3, y + 3.2, 30, f'<div class="gnum num">{n+1:02d}</div>')
    out += f'<div class="a hr dkhr" style="left:{x0}mm;top:{58+4*33}mm;width:{x1-x0}mm"></div>'
    return page(5, out + foot(5, x0, x1, 'أهدافنا', 'Our Goals', dark=True), 'dark')

# =============================================================== page 6 — services overview (six photographs)
OVER = {}
def p06():
    x0, x1 = 18, 279
    tw, th, gx = (261 - 2 * 6) / 3, 50.0, 6.0
    out = head(x0, x1, 20, f'{N("03")} خدماتنا', 'Our Services &nbsp;03', 'جهة واحدة لستة مجالات', 'One company, six fields')
    for n, s in enumerate(SERVICES):
        col, row = n % 3, n // 3
        x = x1 - (col + 1) * tw - col * gx          # first tile at the top right (Arabic reading order)
        y = 52 + row * 72
        src, alt = OVER[s['key']]
        out += f'<a href="#p{s["p"]}">' + img(src, x, y, tw, th, alt) + '</a>'
        out += (f'<div class="a pair" style="left:{x}mm;top:{y+th+3}mm;width:{tw}mm">'
                f'{en(s["en"], "ov-e")}{ar(s["ar"], "ov-a")}</div>')
        out += (f'<div class="a pair" style="left:{x}mm;top:{y+th+11.3}mm;width:{tw}mm">'
                f'{en(N(f"{s["p"]:02d}"), "ov-n")}{ar(N(f"{n+1:02d} / 06"), "ov-n")}</div>')
    return page(6, out + foot(6, x0, x1, 'خدماتنا', 'Our Services'))

# =============================================================== pages 7–12 — services (one master, mirrored for rhythm)
PW = 132.0            # service master: photo panel width (hero square + two tiles)
def service(i, s, pics):
    p = s['p']
    img_left = (i % 2 == 0)
    ix = 0 if img_left else 297 - PW
    hero, t1, t2 = pics
    HH, G = 132.0, 3.6
    tw2 = (PW - G) / 2
    th2 = 210 - HH - G
    out = img(hero[0], ix, 0, PW, HH, hero[1])
    out += img(t1[0], ix, HH + G, tw2, th2, t1[1]) + img(t2[0], ix + tw2 + G, HH + G, tw2, th2, t2[1])
    x0, x1 = (PW + 14, 279) if img_left else (18, 297 - PW - 14)
    li_a = ''.join(f'<div class="li">{DM}<span>{a_}</span></div>' for a_, _ in s['items'])
    li_e = ''.join(f'<div class="li">{DM}<span>{e_}</span></div>' for _, e_ in s['items'])
    if s.get('after'):
        li_a += f'<p class="after">{s["after"][0]}</p>'
        li_e += f'<p class="after">{s["after"][1]}</p>'
    inner = (kpair(f'خدماتنا {N(f"{i+1:02d} / 06")}', f'Our Services &nbsp;{i+1:02d} / 06') + stack_title(s['ar'], s['en']) +
             '<div class="rule-g" style="margin:5mm 0 6mm auto"></div>' +
             fcols(ar(s['iar'], 'lead sv'), en(s['ien'], 'lead sv')) +
             fcols(ar(li_a, 'lst'), en(li_e, 'lst'), 'mt8'))
    out += flow(x0, x1, 20, inner)
    return page(p, out + foot(p, x0, x1, 'خدماتنا', 'Our Services'))

def service_pics():
    P = {}
    W, H, G = PW, 132.0, 3.6
    tw2, th2 = (PW - G) / 2, 210 - 132 - G
    # explicit, readable list: (source, cx, cy, zoom, alt)
    spec = {
     'contracting': [(ST + 'contracting_rebar-worker_wikimedia-rebar-worker-j2.jpg', .58, .52, 1.25, 'Worker tying reinforcement steel'),
                     (ST + 'contracting_surveyor-theodolite_flickr-8756741875.jpg', .5, .45, 1.15, 'Surveyor with a theodolite'),
                     (ST + 'contracting-electrical_distribution-board_wikimedia-small-house-distribution-panel-2.jpg', .5, .52, 1.6, 'Electrical distribution board')],
     'landscaping': [(ST + 'landscaping_date-palm_wikimedia-date-palm-tree-landscape.jpg', .47, .40, 1.2, 'Date palm'),
                     (ST + 'landscaping_palm-promenade-lawn_flickr-19570930662.jpg', .72, .55, 1.0, 'Landscaped promenade with palms and lawn'),
                     (ST + 'landscaping_gardener-trimmer_flickr-54576923958.jpg', .5, .48, 1.0, 'Grounds maintenance with a trimmer')],
     'maintenance': [(ST + 'maintenance_hvac-gauges_wikimedia-379th-eces-8502255.jpg', .62, .50, 1.15, 'Technicians reading air-conditioning gauges'),
                     (ST + 'maintenance_hvac-gauges_wikimedia-379th-eces-8502255.jpg', .55, .42, 3.2, 'Air-conditioning service gauges, detail'),
                     (ST + 'contracting_site-at-blue-hour_flickr-2146788503.jpg', .45, .5, 1.0, 'Building at blue hour')],
     'cleaning':    [(ST + 'cleaning_floor-scrubbers-lobby_wikimedia-floor-scrubbers.jpg', .70, .55, 1.0, 'Floor-cleaning machine in a lobby'),
                     (ST + 'cleaning_mop-and-trolley-floor_flickr-24978817211.jpg', .55, .6, 1.0, 'Floor cleaning with mop and trolley'),
                     (ST + 'cleaning_rope-access-window-cleaner_flickr-4797579546.jpg', .72, .45, 1.0, 'Rope-access window cleaning')],
     'manpower':    [('assets/derived/mockup_cleaning-team_retouched_v03.png', .5, .42, 1.0, 'Service team in branded uniforms, illustrative image'),
                     (ST + 'manpower_waiter-pouring-tea_flickr-38075436525.jpg', .45, .45, 1.0, 'Waiter pouring tea'),
                     (ST + 'manpower_catering-table-setup-overhead_flickr-6160161346.jpg', .62, .5, 1.0, 'Staff setting a catering table')],
     'logistics':   [('assets/derived/mockup_car-scooter-facade_retouched_v03.png', .625, .5, 1.0, 'Branded car and delivery scooter, illustrative image'),
                     (ST + 'logistics_white-box-truck_flickr-51928284838.jpg', .55, .55, 1.0, 'Box truck on the road'),
                     (ST + 'logistics_forklift-in-motion_flickr-4325154436.jpg', .62, .5, 1.0, 'Forklift in a warehouse')],
    }
    BOX = {ST + 'cleaning_floor-scrubbers-lobby_wikimedia-floor-scrubbers.jpg': (1060, 0, 2655, 1991),        # right 60 %: no maker mark
           ST + 'manpower_catering-table-setup-overhead_flickr-6160161346.jpg': (190, 0, 1024, 682)}         # banner cropped off
    for n, s in enumerate(SERVICES):
        k = s['key']
        out = []
        for m, (src, cx, cy, z, alt) in enumerate(spec[k]):
            w, h = (W, H) if m == 0 else (tw2, th2)
            sv = .55 if src.startswith('assets/derived/mockup') else 1.0
            out.append((prep(f'p{s["p"]:02d}_{k}_{["hero","t1","t2"][m]}', src, w, h, cx, cy, zoom=z, box=BOX.get(src), page=str(s['p']), s=sv), alt))
        P[k] = out
        # overview tile: the same hero photograph, a different crop
        src, cx, cy, z, alt = spec[k][0]
        sv = .55 if src.startswith('assets/derived/mockup') else 1.0
        OVER[k] = (prep(f'p06_{k}', src, (261 - 12) / 3, 50, cx, cy, zoom=z * 1.08, box=BOX.get(src), page='6', s=sv), alt)
    return P

# =============================================================== page 13 — logistics in pictures (client images)
def p13():
    R = lambda n: f'assets/derived/mockup_{n}_retouched_v03.png'
    G, BH = 3.6, 92.0
    W3 = (297 - 2 * G) / 3
    a = prep('p13_truck-front34', R('truck-front34'), W3, BH, .5, .55, page='13', s=.55)
    b = prep('p13_truck-side', R('truck-side'), W3, BH, .5, .5, page='13', s=.55)
    c = prep('p13_truck-rear34', R('truck-rear34'), W3, BH, .5, .55, page='13', s=.55)
    rider = prep('p13_rider', R('delivery-rider'), 46, 94.2, box=(290, 0, 790, 1024), page='13', s=0)
    out = img(c, 0, 0, W3, BH, 'Branded box truck, rear view, illustrative image') + img(b, W3 + G, 0, W3, BH, 'Branded box truck, side view, illustrative image') + \
          img(a, 2 * (W3 + G), 0, W3, BH, 'Branded box truck, front view, illustrative image')
    out += img(rider, 125.5, 100, 46, 94.2, 'Delivery rider with branded bag, illustrative image', 'mult')
    items = [('التوصيل', 'Delivery'), ('نقل البضائع', 'Goods transport'), ('التخزين', 'Storage'), ('تأجير المركبات', 'Vehicle rental')]
    la = ''.join(f'<div class="li">{DM}<span>{x}</span></div>' for x, _ in items)
    le = ''.join(f'<div class="li">{DM}<span>{y}</span></div>' for _, y in items)
    out += flow(184, 279, 104, ar(f'<div class="k">{DM}خدماتنا {N("06 / 06")}</div><div class="t1">الخدمات اللوجستية</div>'
                                 f'<div class="lst" style="margin-top:6mm">{la}</div>'))
    out += flow(18, 113, 104, en(f'<div class="k">Our Services &nbsp;06 / 06</div><div class="t1">Logistics Services</div>'
                                 f'<div class="lst" style="margin-top:6mm">{le}</div>'))
    out += f'<div class="a pair" style="left:18mm;top:{BH+3}mm;width:261mm">{en("Illustrative images", "cap")}{ar("صور توضيحية", "cap")}</div>'
    return page(13, out + foot(13, 18, 279, 'خدماتنا', 'Our Services'))

# =============================================================== page 14 — why (light, typographic)
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
    out = head(x0, x1, 20, f'{N("04")} لماذا نحن', 'Why us &nbsp;04', 'لماذا «اطلبني إعمار»', 'Why OTLOBNY Emaar')
    for n, (ta, da, te, de) in enumerate(pts):
        y = 52 + n * 23.4
        out += f'<div class="a hr" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm"></div>'
        out += at(x0, y + 3, 112, en(f'<div class="wt">{te}</div><div class="wd">{de}</div>'))
        out += at(x0 + 149, y + 3, 112, ar(f'<div class="wt">{ta}</div><div class="wd">{da}</div>'))
        out += at(133.5, y + 3.2, 30, f'<div class="wnum num">{n+1:02d}</div>')
    out += f'<div class="a hr" style="left:{x0}mm;top:{52+6*23.4}mm;width:{x1-x0}mm"></div>'
    return page(14, out + foot(14, x0, x1, 'لماذا «اطلبني إعمار»', 'Why OTLOBNY Emaar'), 'tint')

# =============================================================== pages 15–17 — works
def chips(lst, lang):
    return ''.join(f'<span class="chip">{a_ if lang == "ar" else e_}</span>' for a_, e_ in lst)

def work_flow(w, i, x0, x1):
    return flow(x0, x1, 20, kpair(f'أعمالنا {N(f"{i:02d} / 03")}', f'Our Work &nbsp;{i:02d} / 03') +
                stack_title(w['ar'], w['en']).replace('t1 st', 't1 st tw') + '<div class="rule-g" style="margin:5mm 0 6mm auto"></div>' +
                fcols(ar(w['sar'], 'lead'), en(w['sen'], 'lead')))

def scope(w, x0, x1, y):
    return (f'<div class="a fcols" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm">'
            f'{en("<div class=scl>Scope</div><div class=chips style=margin-top:2mm>" + chips(w["chips"], "en") + "</div>")}'
            f'{ar("<div class=scl>نطاق العمل</div><div class=chips style=margin-top:2mm>" + chips(w["chips"], "ar") + "</div>")}</div>')

def work_image(w, n, src, px, iw, ih, alt, cap_en, cap_ar):
    """Works master: a light tint panel fills the image half; photograph, caption and scope sit centred in it."""
    total = ih + 3 + 6 + 10 + 16
    y = 105 - total / 2
    x = px + (148.5 - iw) / 2
    out = f'<div class="a panel" style="left:{px}mm;top:0;width:148.5mm;height:210mm"></div>'
    out += img(src, x, y, iw, ih, alt)
    out += f'<div class="a pair" style="left:{x}mm;top:{y+ih+3}mm;width:{iw}mm">{en(cap_en, "cap")}{ar(cap_ar, "cap")}</div>'
    out += scope(w, x, x + iw, y + ih + 14)
    return out

def p15():
    w = WORKS[0]
    iw = 118.0; ih = iw * 471 / 950            # whole photograph, 204 ppi
    im = prep('p15_bus-shelter', 'assets/photos/bus-shelter.png', iw, ih, box=(0, 0, 950, 471), page='15', s=.7)
    out = work_image(w, 1, im, 148.5, iw, ih, 'Bus waiting shelter installed by the company', 'Project photograph', 'صورة من أعمال الشركة')
    out += work_flow(w, 1, 18, 134.5)
    return page(15, out + foot(15, 18, 134.5, 'أعمالنا', 'Our Work'))

def p16():
    w = WORKS[1]
    iw = 118.0; ih = iw * 454 / 644            # 139 ppi
    im = prep('p16_chamber', 'assets/photos/chamber-building.png', iw, ih, box=(0, 0, 644, 454), page='16', s=.7)
    out = work_image(w, 2, im, 0, iw, ih, 'Madinah Chamber of Commerce building, architectural image', 'Image supplied by the client', 'صورة من العميل')
    out += work_flow(w, 2, 162.5, 279)
    return page(16, out + foot(16, 162.5, 279, 'أعمالنا', 'Our Work'))

def p17():
    w = WORKS[2]
    # 335 x 597 px source: placed 40 mm wide = 213 ppi; light grade only
    im = prep('p17_dar-al-taqwa_entrance', 'assets/photos/dar-al-taqwa-hotel-entrance.jpg', 40, 71.3, page='17', s=.5)
    x0, x1 = 18, 279
    out = head(x0, x1, 20, f'أعمالنا {N("03 / 03")}', 'Our Work &nbsp;03 / 03', 'أعمالنا', 'Our Work')
    px = 148.5 - 20
    dy = 12
    out += f'<div class="a panel" style="left:{148.5-34}mm;top:0;width:68mm;height:210mm"></div>'
    out += at(190, 62 + dy, 89, ar(w['ar'], 'huge'))
    out += at(190, 94 + dy, 89, ar(w['sar'], 'lead'))
    out += at(190, 124 + dy, 89, ar(f'<div class="chips" style="margin-top:0">{chips(w["chips"], "ar")}</div>'))
    out += at(18, 66.5 + dy, 89, en(w['en'], 'huge-e'))
    out += at(18, 94 + dy, 89, en(w['sen'], 'lead'))
    out += at(18, 124 + dy, 89, en(f'<div class="chips" style="margin-top:0">{chips(w["chips"], "en")}</div>'))
    out += img(im, px, 58 + dy, 40, 71.3, 'Entrance of Dar Al Taqwa Hotel')
    out += f'<div class="a" style="left:{px-10}mm;top:{134+dy}mm;width:60mm;text-align:center">{ar("مدخل الفندق", "cap", "text-align:center")}{en("Hotel entrance", "cap", "text-align:center")}</div>'
    return page(17, out + foot(17, x0, x1, 'أعمالنا', 'Our Work'))

# =============================================================== pages 18–19 — partners (32 logos, 16 + 16)
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
# optical widths (mm) — v03 values (art-director + v03 corrections), scaled to the v04 cell; new-13/14 added
AD_W = {'existing-01': 40.0, 'existing-02': 40.0, 'existing-03': 29.5, 'existing-04': 28.0, 'existing-05': 33.0, 'existing-06': 36.0,
        'existing-07': 32.0, 'existing-08': 20.3, 'existing-09': 58.0, 'existing-10': 40.0, 'existing-11': 50.0, 'existing-12': 34.0,
        'existing-13': 31.0, 'existing-14': 38.0, 'existing-15': 40.0, 'existing-16': 16.6, 'existing-17': 28.0, 'existing-18': 30.0,
        'new-01': 30.1, 'new-02': 38.0, 'new-03': 31.0, 'new-04': 28.0, 'new-05': 17.4, 'new-06': 32.0, 'new-07': 38.0, 'new-08': 28.0,
        'new-09': 38.0, 'new-10': 34.6, 'new-11': 31.5, 'new-12': 31.0,
        'new-13': 44.0,   # Le Méridien: very wide, thin black wordmark (aspect 7:1) -> widest box
        'new-14': 24.0}   # Al Esra Cabin: compact square mark
SCALE = 0.86            # v04 cells are 65 x 33 mm (v03: 52 x 42.5 mm)
H_MAX = 19.5
TIER_B = {f'existing-{n:02d}' for n in (1, 2, 3, 5, 8, 9, 10, 11, 15, 17)}
TIER_C = {'existing-07', 'existing-18'}
EFFECTIVE_W = {'existing-02_al-madinah-region-development-authority': 121 / 0.86, 'existing-17_taza': 143 / 0.87}
PLOG = []

def logo(stem, alt, cx, cy):
    d = BASE / 'assets/partners-transparent'
    im = Image.open(d / f'{stem}.png'); W, H = im.size
    A = np.array(im.getchannel('A')).astype(float)
    bb = im.getchannel('A').getbbox()
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    key = stem.split('_')[0]
    k = min(AD_W[key] * SCALE / w, H_MAX / h)
    eff = (EFFECTIVE_W[stem] / W) if stem in EFFECTIVE_W else 1.0
    floor = 100 if key in TIER_B else 80 if key in TIER_C else 0
    if floor:
        k = min(k, 25.4 / floor * eff)
    ppi = 25.4 / k * eff
    ys, xs = np.mgrid[0:H, 0:W]; m = A.sum() or 1
    gx, gy = (A * xs).sum() / m, (A * ys).sum() / m
    bx, by = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    ox_px = bx + float(np.clip((gx - bx) / 2, -.12 * w, .12 * w)); oy_px = by + float(np.clip((gy - by) / 2, -.12 * h, .12 * h))
    PLOG.append((stem, round(w * k, 1), round(h * k, 1), round(ppi)))
    src = f'assets/partners-transparent/{stem}.png'
    if stem == 'new-13_le-meridien':     # the client's vector file: same artwork, sharper
        src = 'assets/partners-transparent/new-13_le-meridien.svg'
        # SVG viewBox 540 x 78 is the artwork itself; size it to the PNG's ink box
        wmm = w * k; hmm = wmm * 78 / 540
        return f'<img class="a" src="{src}" alt="{alt}" style="left:{cx-wmm/2:.2f}mm;top:{cy-hmm/2:.2f}mm;width:{wmm:.2f}mm;height:{hmm:.2f}mm">'
    return f'<img class="a" src="{src}" alt="{alt}" style="left:{cx-ox_px*k:.2f}mm;top:{cy-oy_px*k:.2f}mm;width:{W*k:.2f}mm;height:{H*k:.2f}mm">'

def partners(p):
    items = PARTNERS[:16] if p == 18 else PARTNERS[16:]
    x0, x1 = 18, 279
    cw, ch, top = (x1 - x0) / 4, 33.0, 56.0
    out = head(x0, x1, 20, f'{N("05")} شركاء النجاح {N(f"{p-17:02d} / 02")}', f'Partners in Success &nbsp;{p-17:02d} / 02', 'شركاء النجاح', 'Partners in Success')
    for r in range(5):
        out += f'<div class="a hr" style="left:{x0}mm;top:{top + r*ch}mm;width:{x1-x0}mm"></div>'
    for c in range(1, 4):
        out += f'<div class="a vr" style="left:{x0 + c*cw}mm;top:{top + 5}mm;height:{4*ch - 10}mm"></div>'
    for n, (s, a_) in enumerate(items):
        col, row = n % 4, n // 4
        cx = x1 - (col + .5) * cw            # right to left
        cy = top + (row + .5) * ch
        out += logo(s, a_, cx, cy)
    if p == 19:
        out += f'<div class="a pair" style="left:{x0}mm;top:{top+4*ch+2.5}mm;width:{x1-x0}mm">{en("All logos are the property of their respective owners.", "cap")}{ar("جميع الشعارات ملك لأصحابها.", "cap")}</div>'
    return page(p, out + foot(p, x0, x1, 'شركاء النجاح', 'Partners in Success'))

# =============================================================== page 20 — contact, credits, back cover
def p20():
    rows = [('الهاتف', 'Tel', '<a href="tel:+966549555514">054 955 5514</a>'),
            ('البريد الإلكتروني', 'Email', '<a href="mailto:info@otlobny.co">info@otlobny.co</a>'),
            ('الموقع الإلكتروني', 'Website', '<a href="https://otlobny.net">otlobny.net</a>'),
            ('السجل التجاري', 'Commercial Registration', '4650245200')]
    x0, x1 = 48, 249
    out = f'<img class="a" src="assets/logo/otlobny-emaar_logo_wordmark-reversed_ar_v01.svg" alt="اطلبني" style="left:{148.5-34}mm;top:20mm;width:68mm;height:{68*124.597/307.711:.2f}mm">'
    out += f'<div class="a pair base" style="left:{x0}mm;top:62mm;width:{x1-x0}mm">{en("Contact", "t2")}{ar("تواصل معنا", "t2")}</div>'
    for n, (la, le, v) in enumerate(rows):
        y = 76 + n * 13
        out += f'<div class="a hr dkhr" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm"></div>'
        out += (f'<div class="a crow" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm">{en(le, "cl")}<div class="cv num">{v}</div>{ar(la, "cl")}</div>')
    y = 76 + 4 * 13
    out += f'<div class="a hr dkhr" style="left:{x0}mm;top:{y}mm;width:{x1-x0}mm"></div>'
    out += cols(x0, x1, y + 4, ar('<div class="cl">العنوان</div><div class="ca">طريق الأمير عبدالمجيد بن عبدالعزيز، المدينة المنورة، المملكة العربية السعودية</div>'),
                en('<div class="cl">Address</div><div class="ca">Prince Abdulmajeed bin Abdulaziz Road, Al Madinah Al Munawwarah, Saudi Arabia</div>'), gap=30)
    # photo credits: only the photographs actually used (CREDITS_USED is complete once every other page is built)
    att, free = [], []
    for fn in sorted(CREDITS_USED, key=lambda f: CREDIT[f][1].lower()):
        t, a_, lic, src = CREDIT[fn]
        (free if lic in ('CC0 1.0', 'Public domain') else att).append(f'“{t}”, {a_}, {lic} ({src})')
    att = sorted(set(att)); free = sorted(set(free))
    cr_en = ('<b>Photo credits.</b> ' + '; '.join(att) + '. All modified (cropped, colour-graded; logo or number plate removed where present). '
             'No attribution required: ' + '; '.join(free) + '. Licences: creativecommons.org/licenses. '
             'Project photographs, vehicle and team images: the client. Service photographs are illustrative.')
    cr_ar = ('<b>حقوق الصور.</b> صور الخدمات توضيحية، مرخّصة بتراخيص المشاع الإبداعي أو ملكية عامة، ومنسوبة لأصحابها في القائمة الإنجليزية المجاورة، '
             'وقد عُدّلت (قصّ ومعالجة لونية). صور الأعمال وصور المركبات والفريق من العميل.')
    out += f'<div class="a hr dkhr" style="left:18mm;top:170mm;width:261mm"></div>'
    out += at(18, 173, 180, en(cr_en, 'credit'))
    out += at(207, 173, 72, ar(cr_ar, 'credit'))
    return page(20, out, 'dark')

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
:root{--blue:#3758B0;--green:#5AC584;--navy:#1F3162;--tint:#F7F8FC;--peri:#9BABD7;--grey:#525456;--hair:.3pt solid #C9D1EA}
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:"IBM Plex Sans",sans-serif;font-synthesis:none;hyphens:none;-webkit-hyphens:none;font-kerning:normal}
a{color:inherit;text-decoration:none}
.page{position:relative;width:297mm;height:210mm;overflow:hidden;background:#fff;break-after:page;page-break-after:always}
.page:last-child{break-after:auto;page-break-after:auto}
.page.tint{background:var(--tint)}
.page.dark{background:linear-gradient(115deg,#1F3162 0%,#22386F 55%,#2B458A 100%)}
.a{position:absolute}
img.ph{display:block;object-fit:cover}
img.mult{mix-blend-mode:multiply}
.tw.ar{font-size:25pt !important;line-height:1.4 !important} .tw.en{font-size:17pt !important}
.panel{background:var(--tint)}
/* language blocks — Arabic: Tajawal, right to left, never tracked; English: IBM Plex Sans, left to right */
.ar{font-family:"Tajawal",sans-serif;direction:rtl;text-align:right;color:var(--navy);letter-spacing:0}
.en{font-family:"IBM Plex Sans",sans-serif;direction:ltr;text-align:left;color:var(--grey)}
.num{font-family:"IBM Plex Sans",sans-serif;direction:ltr;unicode-bidi:isolate;letter-spacing:0;font-feature-settings:"tnum" 0}
.dark .ar,.dark .en{color:#fff}
p,.body,.lead,.wd,.ca{text-wrap:pretty}
.pair{display:flex;direction:ltr;justify-content:space-between;align-items:flex-start}
.pair.base{align-items:baseline}
.pair>.en{flex:0 1 auto}.pair>.ar{flex:0 1 auto}
/* type scale v04 (pt) — Arabic about 18-25 % larger than the English beside it */
.ar.k,.ar .k{font-weight:700;font-size:9.5pt;line-height:1.6;color:var(--blue);display:flex;align-items:center;gap:1.8mm}
.en.k,.en .k{font-weight:600;font-size:6.8pt;line-height:1.6;color:var(--blue);text-transform:uppercase;letter-spacing:.14em}
.dark .k{color:var(--green) !important}
.ar.t1,.ar .t1{font-weight:800;font-size:31pt;line-height:1.3;color:var(--navy)}
.en.t1,.en .t1{font-weight:600;font-size:21pt;line-height:1.15;color:var(--blue)}
.ar.t1b{font-weight:800;font-size:38pt;line-height:1.25}
.en.t1b{font-weight:600;font-size:26pt;line-height:1.1;color:var(--blue)}
.dark .t1,.dark .en.t1,.dark .ar.t1{color:#fff}
.ar.t2,.ar .t2{font-weight:700;font-size:17pt;line-height:1.5;color:var(--navy)}
.en.t2,.en .t2{font-weight:600;font-size:13pt;line-height:1.3;color:var(--navy)}
.ar.lead,.ar .lead{font-weight:500;font-size:13pt;line-height:1.75}
.en.lead,.en .lead{font-weight:400;font-size:10.5pt;line-height:1.55}
.ar.body,.ar .body{font-weight:400;font-size:11pt;line-height:1.8}
.en.body,.en .body{font-weight:400;font-size:9pt;line-height:1.6}
.ar.cap,.ar .cap{font-weight:500;font-size:8pt;line-height:1.6;color:var(--grey)}
.en.cap,.en .cap{font-weight:500;font-size:6.5pt;line-height:1.5;color:var(--grey);text-transform:uppercase;letter-spacing:.1em}
.dkc{color:rgba(255,255,255,.85) !important}
/* devices */
.dm{display:inline-block;flex:none;width:1.5mm;height:1.5mm;margin:.3mm;background:var(--green);border-radius:16%;transform:rotate(45deg)}
.hr{border-top:var(--hair);height:0}
.dkhr{border-top:.3pt solid rgba(255,255,255,.28)}
.vr{border-left:var(--hair);width:0}
.rule-g{width:14mm;border-top:1.2pt solid var(--green)}
.ar .rule-g{margin-left:0}
/* footer */
.ft{display:flex;direction:ltr;justify-content:space-between;align-items:baseline}
.ft .fl{font-size:6.5pt;font-weight:500;color:#5F6573}
.ft .en.fl{text-transform:uppercase;letter-spacing:.1em}
.ft .ar.fl{font-size:8pt;display:flex;gap:3mm;align-items:baseline}
.ft .folio{font-family:"IBM Plex Sans";font-weight:600;font-size:7.5pt;color:var(--navy)}
.ft.dk .fl{color:rgba(255,255,255,.7)} .ft.dk .folio{color:#fff}
/* cover */
.cv-k{font-weight:700;font-size:15pt;line-height:1.5;color:var(--blue)}
.cv-t{font-weight:800;font-size:33pt;line-height:1.3;color:var(--navy);margin-top:.5mm;white-space:nowrap}
.cv-ke{font-weight:600;font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase;color:var(--blue)}
.cv-te{font-weight:500;font-size:23pt;line-height:1.15;color:var(--navy);margin-top:1.2mm}
.cvline{border-top:.6pt solid var(--green);height:0}
.cv-f{font-weight:500;font-size:8pt;color:var(--grey)} .cv-fa{font-weight:500;font-size:9.5pt;color:var(--grey)}
/* contents */
.toc{display:flex;direction:ltr;justify-content:space-between;align-items:center;height:16.4mm;border-bottom:var(--hair)}
.toc-e{font-weight:500;font-size:9.5pt;color:var(--grey);width:55mm}
.toc-a{font-weight:700;font-size:14pt;color:var(--navy);width:62mm}
.toc-n{font-weight:600;font-size:15pt;color:var(--blue);width:20mm;text-align:center}
/* about facts */
.fl2{font-weight:500;font-size:6.5pt;letter-spacing:.1em;text-transform:uppercase;color:#5F6573;line-height:1.4}
.ar .fl2{font-size:8pt;letter-spacing:0;text-transform:none;line-height:1.5}
.fv{font-weight:700;font-size:11.5pt;color:var(--navy);line-height:1.35;margin-top:.4mm}
.en .fv{font-weight:600;font-size:9.5pt}
.fvn{font-family:"IBM Plex Sans";font-weight:600 !important;font-size:12pt !important;color:var(--blue)}
/* goals and why */
.gnum{font-family:"IBM Plex Sans";font-weight:400;font-size:30pt;line-height:1;color:var(--green);text-align:center}
.wnum{font-family:"IBM Plex Sans";font-weight:600;font-size:15pt;line-height:1;color:var(--blue);text-align:center}
.ar .wt{font-weight:700;font-size:13pt;line-height:1.5;color:var(--navy)}
.en .wt{font-weight:600;font-size:10pt;line-height:1.35;color:var(--navy)}
.ar .wd{font-weight:400;font-size:10.5pt;line-height:1.7;margin-top:.6mm}
.en .wd{font-size:8.6pt;line-height:1.5;margin-top:.8mm}
/* overview */
.ov-a{font-weight:700;font-size:13pt;line-height:1.4;color:var(--navy)}
.ov-e{font-weight:600;font-size:9pt;line-height:1.5;color:var(--navy);padding-top:1.2mm}
.ov-n{font-size:7pt;font-weight:600;color:var(--blue)} .en.ov-n{letter-spacing:.06em}
/* lists */
.lst .li{display:flex;align-items:flex-start;gap:2.4mm;padding:2mm 0 2.1mm;border-top:var(--hair)}
.lst .li:last-of-type{border-bottom:var(--hair)}
.ar .lst .li,.ar.lst .li{font-weight:500;font-size:11pt;line-height:1.55;color:var(--navy)}
.en .lst .li,.en.lst .li{font-weight:500;font-size:8.8pt;line-height:1.5;color:var(--navy)}
.ar.lst .dm,.ar .lst .dm{margin-top:2.05mm} .en.lst .dm,.en .lst .dm{margin-top:1.55mm}
.after{margin-top:3.5mm}
.ar .after{font-size:10.5pt;line-height:1.7} .en .after{font-size:8.6pt;line-height:1.5}
/* works */
.chips{display:flex;flex-wrap:wrap;gap:1.6mm;margin-top:5mm}
.chip{display:inline-flex;align-items:center;height:6.4mm;padding:0 3mm;border:.5pt solid var(--blue);border-radius:3.2mm;color:var(--navy);white-space:nowrap}
.ar .chip{font-weight:500;font-size:9.5pt;padding-top:.6mm}
.en .chip{font-weight:500;font-size:7.4pt;letter-spacing:.04em}
.bigno{font-family:"IBM Plex Sans";font-weight:400;font-size:44pt;line-height:1;color:#fff;text-align:right}
.ar.huge{font-weight:800;font-size:36pt;line-height:1.3;color:var(--navy);white-space:nowrap}
.en.huge-e{font-weight:600;font-size:21pt;white-space:nowrap;line-height:1.15;color:var(--blue)}
.stamp{outline:.3pt solid #C9D1EA;outline-offset:2.4mm}
/* flow text areas */
.flow{display:flex;flex-direction:column}
.flow .pair{margin-bottom:3mm}
h2.st{display:block;width:100%}
.ar.t1.st{margin-top:1mm} .en.t1.st{margin-top:1.5mm}
.fcols{display:grid;direction:ltr;grid-template-columns:1fr 1fr;column-gap:7mm;align-items:start}
.mt8{margin-top:8mm}
.ar.lead.sv{font-size:12pt;line-height:1.75} .en.lead.sv{font-size:10pt;line-height:1.55}
.en .scl{font-size:6.5pt;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--blue)}
.ar .scl{font-size:9pt;font-weight:700;color:var(--blue)}
.en.scope{font-size:6.5pt;letter-spacing:.1em;text-transform:uppercase;color:var(--grey)}
.ar.scope{font-size:8.5pt;color:var(--grey)}
.dark .t2{color:#fff !important}
/* contact */
.crow{display:flex;direction:ltr;justify-content:space-between;align-items:center;height:13mm}
.cl{font-size:7pt !important;font-weight:500;letter-spacing:.1em;text-transform:uppercase;color:var(--peri) !important}
.ar.cl,.ar .cl{font-size:9pt !important;letter-spacing:0;text-transform:none}
.crow>.en,.crow>.ar{width:60mm}
.cv{font-weight:500;font-size:16pt;color:#fff;text-align:center}
.ca{font-size:9pt;line-height:1.6;margin-top:1mm}
.ar .ca{font-size:10.5pt;line-height:1.8}
.credit{font-size:6pt;line-height:1.5;color:var(--peri) !important}
.ar.credit{font-size:7pt;line-height:1.7}
.credit b{font-weight:600;color:#fff}
'''

def build():
    pics = service_pics()
    pages = [p01(), p02(), p03(), p04(), p05(), p06()]
    pages += [service(i, s, pics[s['key']]) for i, s in enumerate(SERVICES)]
    pages += [p13(), p14(), p15(), p16(), p17(), partners(18), partners(19)]
    pages += [p20()]   # last: credits list needs every photograph registered
    html = ('<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
            '<title>اطلبني إعمار — الملف التعريفي | OTLOBNY Emaar — Company Profile (draft v04)</title>\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<style>{CSS}</style>\n</head>\n<body>\n' + ''.join(pages) + '</body>\n</html>\n')
    OUT.write_text(html, encoding='utf-8')
    print('wrote', OUT.name, len(pages), 'pages')
    for r in LOG:
        print('  img p%-3s %-40s %-90s crop %s -> %s mm, %d ppi' % r)
    for r in PLOG:
        print('  logo %-48s %5.1f x %4.1f mm  %4d ppi' % r)
    print('credits used:', len(CREDITS_USED))

if __name__ == '__main__':
    build()
