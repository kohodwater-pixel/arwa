#!/usr/bin/env python3
"""Generates otlobny-emaar_company-profile_screen_ar-en_v02.html (company profile, draft v02).

v02 = the v01 generator (kept below unchanged where still used) plus the "v02" section at the end, which
redefines the pages that changed and writes the derived JPEGs. Client answers and rulings: brand-context.md.

The HTML it writes is the editable source and is self-contained next to its assets/ folder.
Copy comes from content-outline.md; layout from art-direction.md and the Creative Director's
rulings in brand-context.md (decision log, last row). Nothing here invents content.
Run: python3 _work/build_profile_v01.py
"""
from pathlib import Path
from PIL import Image
import math

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / 'otlobny-emaar_company-profile_screen_ar-en_v02.html'

# ------------------------------------------------------------------ shared pieces
SPARK = 'M0 -1 Q.16 -.16 1 0 Q.16 .16 0 1 Q-.16 .16 -1 0 Q-.16 -.16 0 -1Z'

def spark(size_mm, color, cls=''):
    return (f'<svg class="sp {cls}" width="{size_mm}mm" height="{size_mm}mm" viewBox="-1 -1 2 2" aria-hidden="true">'
            f'<path d="{SPARK}" fill="{color}"/></svg>')

def band(cols, x, y, color, opacity=1.0, rows=3):
    w, h = (cols - 1) * 5 + 2, (rows - 1) * 5 + 2
    marks = ''.join(f'<path transform="translate({c*5+1} {r*5+1})" d="{SPARK}"/>' for r in range(rows) for c in range(cols))
    return (f'<svg class="abs" style="left:{x}mm;top:{y}mm" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" aria-hidden="true">'
            f'<g fill="{color}" opacity="{opacity}">{marks}</g></svg>')

ICONS = {  # drawn for this document: 24-unit grid, line only, round caps and joins
 'contracting': '<path d="M3 21h18"/><path d="M5 21V10l6-3v14"/><path d="M11 21V4h8v17"/><path d="M14 8h2M14 12h2M14 16h2"/><path d="M8 12v1.5M8 16v1.5"/>',
 'landscaping': '<circle cx="12" cy="9" r="6"/><path d="M12 21V9"/><path d="M12 13.5l3-3M12 11l-2.5-2.5"/><path d="M6 21h12"/>',
 'maintenance': '<path d="M20.73 6.38A5 5 0 0 1 14.29 12.7L7.93 19.06A2.11 2.11 0 0 1 4.94 16.07L11.3 9.71A5 5 0 0 1 17.62 3.27L15.01 5.88L18.12 8.99Z"/>',
 'cleaning': '<path d="M6 21v-7a3 3 0 0 1 3-3h3a3 3 0 0 1 3 3v7Z"/><path d="M9 11V8h3v3"/><path d="M7 8h7.5l1.5-2.5H9a2 2 0 0 0-2 2Z"/><path d="M12.5 8l1.5 2.5"/><path d="M19 3.5l1.2-1.2M19.6 6h1.9M19 8.5l1.2 1.2"/><path d="M6 16h9"/>',
 'manpower': '<circle cx="9" cy="7" r="3.2"/><path d="M3 20v-1a6 6 0 0 1 12 0v1"/><path d="M15.5 4.1a3.2 3.2 0 0 1 0 5.8"/><path d="M18 13.6a6 6 0 0 1 3 5.4v1"/>',
 'logistics': '<path d="M4.5 17H2V6h11v11H8.5"/><path d="M13 9h4.5L21 12.5V17h-2.5"/><path d="M14.5 17H13"/><circle cx="6.5" cy="17.5" r="2"/><circle cx="16.5" cy="17.5" r="2"/>',
}

def icon(name, size_mm, color='#fff', cls=''):
    return (f'<svg class="{cls}" width="{size_mm}mm" height="{size_mm}mm" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

def holder(name, box=14):
    s = box / math.sqrt(2)
    ic = box * 0.5
    return (f'<span class="holder" style="width:{box}mm;height:{box}mm">'
            f'<svg width="{box}mm" height="{box}mm" viewBox="0 0 {box} {box}" aria-hidden="true"><rect x="{(box-s)/2+.15:.3f}" y="{(box-s)/2+.15:.3f}" '
            f'width="{s-.3:.3f}" height="{s-.3:.3f}" rx="{s*.16:.3f}" transform="rotate(45 {box/2} {box/2})" fill="none" stroke="#fff" stroke-width=".265"/></svg>'
            f'{icon(name, round(ic, 2), "#fff", "holder-ic")}</span>')

DM = '<i class="dm"></i>'
AR_DOC, EN_DOC = 'اطلبني إعمار · الملف التعريفي', 'OTLOBNY Emaar · Company Profile'

SECTIONS = {  # page -> (number, Arabic, English)
 2: ('', 'المحتويات', 'Contents'), 3: ('01', 'من نحن', 'About Us'),
 **{p: ('02', 'رؤيتنا ورسالتنا وأهدافنا', 'Vision, Mission and Goals') for p in (4, 5, 6)},
 **{p: ('03', 'خدماتنا', 'Our Services') for p in range(7, 14)},
 14: ('04', 'لماذا اطلبني إعمار', 'Why OTLOBNY Emaar'),
 **{p: ('05', 'أعمالنا', 'Our Work') for p in (15, 16, 17)},
 **{p: ('06', 'شركاء النجاح', 'Partners in Success') for p in (18, 19)},
}

def chrome(p, extra_footer=''):
    num, ar, en = SECTIONS[p]
    n = f'<span class="num" dir="ltr">{num}</span>' if num else ''
    head = (f'<div class="hd"><div class="en lbl" lang="en" dir="ltr">{en}</div>'
            f'<div class="ar lbl hd-ar" lang="ar" dir="rtl">{spark(2.4, "#5AC584")}{n}<span>{ar}</span></div></div><div class="hd-line"></div>')
    folio = f'<span class="folio num" dir="ltr">{p:02d}</span>'
    if p % 2 == 0:   # even page: folio on the right, English document name on the left
        foot = f'<div class="ft"><div class="en lbl" lang="en" dir="ltr">{EN_DOC}</div>{folio}</div>'
    else:            # odd page: folio on the left, Arabic document name on the right
        foot = f'<div class="ft">{folio}<div class="ar lbl" lang="ar" dir="rtl">{AR_DOC}</div></div>'
    return head + foot + extra_footer

def page(p, body, cls='', with_chrome=True, extra_footer=''):
    ch = chrome(p, extra_footer) if with_chrome else ''
    return f'<section class="page {cls}" id="p{p}" data-page="{p}">\n{ch}\n{body}\n</section>\n'

def titles(ar, en, size='ttl-p', label_ar=None, label_en=None, top=31.5, wide=False):
    """Page title pair, baselines aligned, Arabic right / English left."""
    w = 'w105' if wide else 'w83'
    lab = ''
    if label_ar:
        lab = (f'<div class="pair abs" style="top:26mm"><div class="en lbl {w}" lang="en" dir="ltr">{label_en}</div>'
               f'<div class="ar lbl {w}" lang="ar" dir="rtl">{label_ar}</div></div>')
    return lab + (f'<div class="pair abs" style="top:{top}mm"><h2 class="en {size} {w}" lang="en" dir="ltr">{en}</h2>'
                  f'<h2 class="ar {size} {w}" lang="ar" dir="rtl">{ar}</h2></div>')

# ------------------------------------------------------------------ page 1, cover
def p1():
    s1, s2, s3 = 100 / math.sqrt(2), 110 / math.sqrt(2), 18 / math.sqrt(2)
    svg = f'''<svg class="abs" style="left:0;top:0" width="297mm" height="210mm" viewBox="0 0 297 210" role="img" aria-label="Glass facade, illustrative image">
<defs><linearGradient id="g1" gradientUnits="userSpaceOnUse" x1="-30" y1="0" x2="70" y2="0"><stop offset="0" stop-color="#1F3162"/><stop offset=".52" stop-color="#2B458A"/><stop offset="1" stop-color="#3758B0"/></linearGradient>
<clipPath id="c2"><rect x="{95-s2/2:.3f}" y="{85-s2/2:.3f}" width="{s2:.3f}" height="{s2:.3f}" rx="{s2*.16:.3f}" transform="rotate(45 95 85)"/></clipPath></defs>
<rect x="{20-s1/2:.3f}" y="{20-s1/2:.3f}" width="{s1:.3f}" height="{s1:.3f}" rx="{s1*.16:.3f}" transform="rotate(45 20 20)" fill="url(#g1)"/>
<image href="assets/derived/cover_glass-facade_duotone.png" x="40" y="30" width="110" height="110" preserveAspectRatio="xMidYMid slice" clip-path="url(#c2)"/>
<rect x="{160-s3/2:.3f}" y="{150-s3/2:.3f}" width="{s3:.3f}" height="{s3:.3f}" rx="{s3*.16:.3f}" transform="rotate(45 160 150)" fill="#5AC584"/>
</svg>'''
    return page(1, svg + f'''
<img class="abs" style="left:178.6mm;top:26mm;width:99.4mm;height:42mm" src="assets/logo/otlobny-emaar_logo_lockup-proposal-colour_ar-en_v01.svg" alt="اطلبني — شركة اطلبني إعمار — OTLOBNY Emaar Co.">
{band(12, 221, 76, "#9BABD7")}
<div class="pair abs" style="top:160mm"><h1 class="en ttl-c" lang="en" dir="ltr">Company Profile</h1><h1 class="ar ttl-c" lang="ar" dir="rtl">الملف التعريفي</h1></div>
''', with_chrome=False)

# ------------------------------------------------------------------ page 2, contents
def p2():
    rows = [('من نحن', 'About Us', 3), ('رؤيتنا ورسالتنا وأهدافنا', 'Vision, Mission and Goals', 4), ('خدماتنا', 'Our Services', 7),
            ('لماذا اطلبني إعمار', 'Why OTLOBNY Emaar', 14), ('أعمالنا', 'Our Work', 15), ('شركاء النجاح', 'Partners in Success', 18),
            ('تواصل معنا', 'Contact', 20)]
    r = ''.join(f'<a class="row5 toc" href="#p{n}"><div class="en hdg" lang="en" dir="ltr">{en}</div><div class="mid tocn num" dir="ltr">{n:02d}</div>'
                f'<div class="ar hdg" lang="ar" dir="rtl">{ar}</div></a>' for ar, en, n in rows)
    return page(2, titles('المحتويات', 'Contents', 'ttl-s', top=28, wide=True) + f'<div class="rows abs" style="top:56mm">{r}</div>', 'tint')

# ------------------------------------------------------------------ page 3, about
def p3():
    ar = ('«اطلبني إعمار» شركة ذات مسؤولية محدودة، تأسست عام 2021 في المدينة المنورة، وتعمل بالسجل التجاري رقم 4650245200. '
          'تقدم الشركة خدماتها في ستة مجالات: المقاولات العامة، والزراعة والتشجير، والصيانة، والنظافة، وتأمين الكوادر، والخدمات اللوجستية. '
          'وتخدم المنشآت الحكومية والتجارية والخاصة.')
    en = ('OTLOBNY Emaar is a limited liability company founded in 2021 in Al Madinah Al Munawwarah, Saudi Arabia, operating under Commercial Registration No. 4650245200. '
          'The company works in six fields: general contracting, landscaping, maintenance, cleaning, manpower supply and logistics services. '
          'It serves government, commercial and private facilities.')
    def fact(lar, len_, var=None, ven=None, mid=None):
        a = f'<div class="ar" lang="ar" dir="rtl"><div class="lbl">{lar}</div>' + (f'<div class="hdg">{var}</div>' if var else '') + '</div>'
        e = f'<div class="en" lang="en" dir="ltr"><div class="lbl">{len_}</div>' + (f'<div class="hdg">{ven}</div>' if ven else '') + '</div>'
        return f'<div class="row5 fact">{e}<div class="mid">{mid or DM}</div>{a}</div>'
    facts = (fact('سنة التأسيس', 'Founded', mid='<span class="bignum num" dir="ltr">2021</span>')
             + fact('المقر', 'Based in', 'المدينة المنورة', 'Al Madinah Al Munawwarah')
             + fact('الشكل القانوني', 'Legal form', 'شركة ذات مسؤولية محدودة', 'Limited liability company')
             + fact('السجل التجاري', 'Commercial Registration', mid='<span class="crnum num" dir="ltr">4650245200</span>'))
    return page(3, titles('من نحن', 'About Us', wide=True) + f'''
<p class="abs en lead w105" lang="en" dir="ltr" style="left:19mm;top:53.5mm">{en}</p>
<p class="abs ar lead w105" lang="ar" dir="rtl" style="left:173mm;top:53.5mm">{ar}</p>
<div class="vline abs" style="left:148.5mm;top:53.5mm;height:57.5mm"></div>
<div class="rows abs" style="top:118mm">{facts}</div>''')

# ------------------------------------------------------------------ pages 4-5, statements
def statement(p, tar, ten, ar, en, extra=''):
    return page(p, titles(tar, ten, wide=True) + f'''
<p class="abs en hdg long w105" lang="en" dir="ltr" style="left:19mm;top:58mm">{en}</p>
<p class="abs ar hdg long w105" lang="ar" dir="rtl" style="left:173mm;top:58mm">{ar}</p>
<div class="vline abs" style="left:148.5mm;top:53.5mm;height:105mm"></div>{extra}''')

def p4():
    return statement(4, 'رؤيتنا', 'Our Vision',
        'تنطلق رؤيتنا في «اطلبني إعمار» نحو التوسع والتطور المستمر لتحقيق المنافسة في الأسواق المحلية في جميع مجالات عملنا، تماشياً مع رؤية المملكة العربية السعودية 2030.',
        'At OTLOBNY Emaar, our vision is continuous expansion and development, so that we compete in local markets across all our fields of work, in line with Saudi Vision 2030.',
        band(7, 132.5, 166, '#9BABD7'))

def p5():
    return statement(5, 'رسالتنا', 'Our Mission',
        'نسعى في «اطلبني إعمار» إلى تزويد سوق العمل بالقوى العاملة الوطنية والأجنبية التي تتمتع بالكفاءات العالية في كثير من المهن الحرفية والفنية في مجالات خدماتنا، وفق أحدث المعايير المتبعة في المملكة العربية السعودية.',
        'At OTLOBNY Emaar, we work to supply the labour market with highly competent national and expatriate manpower in a wide range of skilled trades and technical occupations across our fields of service, to the latest standards applied in the Kingdom of Saudi Arabia.')

# ------------------------------------------------------------------ page 6, goals
def p6():
    goals = [
     ('تقديم أفضل الخدمات بجودة عالية لعملائنا الكرام رغبة في كسب رضاهم واستحسانهم.',
      'To deliver the best service, at high quality, and so earn our clients’ satisfaction and approval.'),
     ('السعي لعقد شراكات استراتيجية مع عدة جهات محلية ومؤسسات إقليمية وعالمية في مجالات الشركة المتخصصة وغيرها من المجالات الأخرى.',
      'To seek strategic partnerships with local bodies and with regional and international institutions, in the company’s specialist fields and beyond.'),
     ('التطوير الدائم والمتابعة المستمرة لمشاريع الشركة لتقديم أفضل الخدمات.',
      'To keep developing, and to follow up the company’s projects closely, so that we deliver the best service.'),
     ('توفير بيئة عمل جذابة لإطلاق كوادر من الخبرات البشرية للإبداع والتميز.',
      'To provide an attractive working environment in which experienced people can create and excel.')]
    r = ''.join(f'<div class="row5 goal fit"><p class="en lead" lang="en" dir="ltr">{en}</p><div class="mid"><span class="bignum num" dir="ltr">{i:02d}</span></div>'
                f'<p class="ar lead" lang="ar" dir="rtl">{ar}</p></div>' for i, (ar, en) in enumerate(goals, 1))
    return page(5, titles('أهدافنا', 'Our Goals', wide=True) + f'<div class="rows abs" style="top:56mm">{r}</div>')

# ------------------------------------------------------------------ services data
SERVICES = [
 dict(p=8, key='contracting', ar='المقاولات العامة', en='General Contracting',
      sar='تنفيذ المشاريع الإنشائية بجميع مراحلها، من الدراسة الفنية إلى التنفيذ.',
      sen='Construction projects at every stage, from technical study to execution.',
      iar='تنفذ «اطلبني إعمار» المشاريع الإنشائية بجميع مراحلها، ابتداءً من الدراسة الفنية والمخططات التصميمية حتى التنفيذ، لكافة أنواع المباني والمنشآت السكنية والحكومية والتجارية.',
      ien='OTLOBNY Emaar carries out construction projects at every stage, from the technical study and design drawings through to execution, for all types of residential, government and commercial buildings and facilities.',
      items=[('مشاريع الإنشاء', 'Construction projects'), ('الأعمال الكهربائية', 'Electrical works'), ('الأعمال الميكانيكية', 'Mechanical works'),
             ('أعمال السباكة والصرف', 'Plumbing and drainage works'), ('مشاريع أنظمة الحريق', 'Fire systems projects')],
      photo=('assets/derived/p08_electrical-panel_duotone.png', 'Electrician at a distribution board, illustrative image')),
 dict(p=9, key='landscaping', ar='الزراعة والتشجير', en='Landscaping',
      sar='التشجير وتنسيق الحدائق وصيانة المنتزهات وأنظمة الري.',
      sen='Tree planting, garden landscaping, and maintenance of parks and irrigation equipment.',
      iar='تنفذ «اطلبني إعمار» أعمال التشجير وتنسيق الحدائق، وتتولى صيانة المنتزهات وأشجار الشوارع وما يتصل بها من أجهزة الري.',
      ien='OTLOBNY Emaar carries out tree planting and garden landscaping, and maintains parks, street trees and the irrigation equipment that serves them.',
      items=[('أعمال التشجير', 'Tree planting'), ('تنسيق الحدائق المزروعة', 'Landscaping of planted gardens'),
             ('صيانة المنتزهات وأشجار الشوارع', 'Maintenance of parks and street trees'), ('صيانة أجهزة الري', 'Maintenance of irrigation equipment')]),
 dict(p=10, key='maintenance', ar='الصيانة', en='Maintenance',
      sar='خدمات صيانة شاملة للمنشآت بفريق من الكوادر المؤهلة.',
      sen='Comprehensive facility maintenance by a qualified team.',
      iar='تقدم «اطلبني إعمار» خدمات صيانة شاملة للمنشآت، عن طريق فريق احترافي من الكوادر المؤهلة.',
      ien='OTLOBNY Emaar provides comprehensive maintenance services for facilities, delivered by a professional team of qualified staff.',
      items=[('تشغيل وصيانة أنظمة التكييف المركزية', 'Operation and maintenance of central <span class="nw">air-conditioning</span> systems'),
             ('تشغيل وصيانة أنظمة المصاعد', 'Operation and maintenance of lift systems')]),
 dict(p=11, key='cleaning', ar='النظافة', en='Cleaning',
      sar='نظافة المباني ومكافحة الآفات للقطاعات الحكومية والتجارية والخاصة.',
      sen='Building cleaning and pest control for the government, commercial and private sectors.',
      iar='تقدم «اطلبني إعمار» خدمات نظافة عالية المستوى يمكن الوثوق بها، للقطاعات الحكومية والخاصة والتجارية.',
      ien='OTLOBNY Emaar provides <span class="nw">high-standard,</span> dependable cleaning services for the government, private and commercial sectors.',
      items=[('نظافة المباني الحكومية والتجارية والمباني الخاصة', 'Cleaning of government, commercial and private buildings'),
             ('مكافحة الآفات والحشرات لجميع المنشآت الحكومية والخاصة', 'Pest and insect control for all government and private facilities')],
      photo=('assets/derived/p11_office-cleaner_duotone.png', 'Cleaner wiping a glass partition, illustrative image')),
 dict(p=12, key='manpower', ar='تأمين الكوادر', en='Manpower Supply',
      sar='كوادر نظامية مؤهلة للمنشآت الحكومية والتجارية والخاصة، بعقود شهرية وسنوية على نظام «أجير».',
      sen='Qualified, legally compliant staff for government, commercial and private facilities, on monthly and annual contracts through the Ajeer system.',
      iar='توفر «اطلبني إعمار» الكوادر النظامية المؤهلة لسوق العمل في مجالات الضيافة والخدمات، للمرافق الحكومية والتجارية والخاصة، وفقاً لمعايير الصحة المهنية.',
      ien='OTLOBNY Emaar supplies qualified, legally compliant staff for hospitality and services roles in government, commercial and private facilities, in line with occupational health standards.',
      items=[('تأجير عمال نظافة للمستشفيات والفنادق والمطارات', 'Cleaning staff for hospitals, hotels and airports'),
             ('تأجير خدمات عمال للفعاليات والمناسبات', 'Staff for events and functions'),
             ('توفير عمال المقاهي والمطاعم والإعاشة', 'Staff for cafés, restaurants and catering')],
      after=('تُبرم العقود شهرياً أو سنوياً على نظام «أجير».', 'Contracts are monthly or annual, through the Ajeer system.')),
 dict(p=13, key='logistics', ar='الخدمات اللوجستية', en='Logistics Services',
      sar='التوصيل بالدراجات النارية ونقل البضائع بشاحنات الصندوق.',
      sen='Motorcycle delivery and goods transport by box truck.',
      iar='تضيف «اطلبني إعمار» الخدمات اللوجستية إلى مجالات عملها.',
      ien='OTLOBNY Emaar is adding logistics services to its fields of work.',
      items=[('التوصيل بالدراجات النارية', 'Delivery by motorcycle'), ('نقل البضائع بشاحنات الصندوق', 'Goods transport by box truck'),
             ('أسطول مركبات لخدمة أعمال التوصيل والنقل', 'A vehicle fleet serving delivery and transport')],
      draft=True),
]

# ------------------------------------------------------------------ page 7, services overview
def p7():
    rows = ''
    for s in SERVICES:
        rows += (f'<a class="row5 svc" href="#p{s["p"]}"><div class="en" lang="en" dir="ltr"><div class="hdg">{s["en"]}</div><div class="body">{s["sen"]}</div></div>'
                 f'<div class="mid col">{holder(s["key"])}<span class="lbl num pg" dir="ltr">{s["p"]:02d}</span></div>'
                 f'<div class="ar" lang="ar" dir="rtl"><div class="hdg">{s["ar"]}</div><div class="body">{s["sar"]}</div></div></a>')
    return page(6, titles('خدماتنا', 'Our Services', 'ttl-s', top=26, wide=True) + f'''
<img class="abs" style="left:133.68mm;top:28mm;width:29.64mm;height:12mm" src="assets/logo/otlobny-emaar_logo_wordmark-white_ar_v01.svg" alt="اطلبني">
<div class="rows svcs abs" style="top:46mm;height:141mm">{rows}</div>''', 'grad dk')

# ------------------------------------------------------------------ pages 8-13, service pages
PILL13 = ('<div class="pill draft abs"><span class="en lbl" lang="en" dir="ltr">Draft — details to be confirmed</span>' + DM +
          '<span class="ar lbl" lang="ar" dir="rtl">مسودة — بانتظار تأكيد التفاصيل</span></div>')

def service(i, s):
    lab_ar = f'خدماتنا <span class="num" dir="ltr">{i:02d} / 06</span>'
    lab_en = f'Our Services <span class="num">{i:02d} / 06</span>'
    bal = ' style="text-wrap:balance"' if s['p'] == 11 else ''   # avoids a one-word last line on p11
    cells = (f'<p class="en lead c1" lang="en" dir="ltr"{bal}>{s["ien"]}</p><p class="ar lead c5" lang="ar" dir="rtl">{s["iar"]}</p><div class="gap6"></div>')
    for ar, en in s['items']:
        cells += (f'<div class="li en body c1" lang="en" dir="ltr">{DM}<span>{en}</span></div>'
                  f'<div class="li ar body c5" lang="ar" dir="rtl">{DM}<span>{ar}</span></div>')
    if s.get('after'):
        cells += (f'<p class="en body c1 after" lang="en" dir="ltr">{s["after"][1]}</p><p class="ar body c5 after" lang="ar" dir="rtl">{s["after"][0]}</p>')
    if s.get('photo'):
        panel = (f'<div class="panel abs"><img src="{s["photo"][0]}" alt="{s["photo"][1]}"></div>'
                 f'<div class="cap abs"><span class="en lbl" lang="en" dir="ltr">Illustrative image</span><span class="ar lbl" lang="ar" dir="rtl">صورة توضيحية</span></div>')
    else:
        panel = (f'<div class="panel grad abs">{icon(s["key"], 46, "#fff", "abs big-ic")}'
                 f'{band(7, 6, 114, "#fff", .3)}</div>')
    return page(s['p'], titles(s['ar'], s['en'], label_ar=lab_ar, label_en=lab_en) + panel + f'<div class="trip abs" style="top:53.5mm">{cells}</div>',
                extra_footer=PILL13 if s.get('draft') else '')

# ------------------------------------------------------------------ page 14, why
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
    r = ''.join(f'<div class="row5 why"><div class="en" lang="en" dir="ltr"><div class="lead b">{ten}</div><div class="body">{den}</div></div>'
                f'<div class="mid"><span class="tocn num" dir="ltr">{i:02d}</span></div>'
                f'<div class="ar" lang="ar" dir="rtl"><div class="lead b">{tar}</div><div class="body">{dar}</div></div></div>'
                for i, (tar, dar, ten, den) in enumerate(pts, 1))
    return page(14, titles('لماذا «اطلبني إعمار»', 'Why OTLOBNY Emaar', wide=True) + f'<div class="rows whys abs" style="top:47mm;height:139mm">{r}</div>', 'tint')

# ------------------------------------------------------------------ pages 15-17, projects
PROJECTS = [
 dict(p=15, ar='تصميم وتركيب محطات انتظار الحافلات', en='Design and installation of bus waiting shelters',
      sar='صممت «اطلبني إعمار» محطات انتظار الحافلات وركبتها، وهي محطات تنظم حركة الركاب وسير الحافلات، بجودة عالية واحترافية في التنفيذ.',
      sen='OTLOBNY Emaar designed and installed bus waiting shelters, which help organise passengers and bus movement, to a high standard of execution.',
      chips=[('تصميم', 'Design'), ('تركيب', 'Installation')], img='assets/derived/p15_bus-shelter.png', alt='Bus waiting shelter'),
 dict(p=16, ar='الغرفة التجارية والصناعية في المدينة المنورة', en='Madinah Chamber of Commerce and Industry',
      sar='قدمت «اطلبني إعمار» خدمات التشغيل والصيانة والنظافة للغرفة التجارية والصناعية في المدينة المنورة.',
      sen='OTLOBNY Emaar provided operation, maintenance and cleaning services for the Madinah Chamber of Commerce and Industry.',
      chips=[('تشغيل', 'Operation'), ('صيانة', 'Maintenance'), ('نظافة', 'Cleaning')], img='assets/derived/p16_chamber-building.png', alt='Madinah Chamber building'),
 dict(p=17, ar='فندق شهد المدينة', en='Shahd Al Madinah Hotel',
      sar='قدمت «اطلبني إعمار» خدمات الصيانة والنظافة لفندق شهد المدينة.',
      sen='OTLOBNY Emaar provided maintenance and cleaning services for Shahd Al Madinah Hotel.',
      chips=[('صيانة', 'Maintenance'), ('نظافة', 'Cleaning')], img='assets/derived/p17_shahd-hotel.png', alt='Shahd Al Madinah Hotel'),
]

def project(i, pr):
    lab_ar = f'<span class="num" dir="ltr">{i:02d} / 03</span>'
    lab_en = f'<span class="num">{i:02d} / 03</span>'
    chips_ar = ''.join(f'<span class="pill ar lbl">{a}</span>' for a, _ in pr['chips'])
    chips_en = ''.join(f'<span class="pill en lbl">{e}</span>' for _, e in pr['chips'])
    idx_ar = ''.join(f'<div class="ar lbl {"cur" if q is pr else ""}" lang="ar" dir="rtl">{DM if q is pr else ""}<span>{q["ar"]}</span></div>' for q in reversed(PROJECTS))
    idx_en = ''.join(f'<div class="en lbl {"cur" if q is pr else ""}" lang="en" dir="ltr">{DM if q is pr else ""}<span>{q["en"]}</span></div>' for q in PROJECTS)
    return page(pr['p'], titles('أعمالنا', 'Our Work', label_ar=lab_ar, label_en=lab_en) + f'''
<img class="abs frame" src="{pr["img"]}" alt="{pr["alt"]}">
<div class="abs w83 en" lang="en" dir="ltr" style="left:19mm;top:53.5mm"><h3 class="hdg">{pr["en"]}</h3><p class="body pj">{pr["sen"]}</p></div>
<div class="abs w83 ar" lang="ar" dir="rtl" style="left:195mm;top:53.5mm"><h3 class="hdg">{pr["ar"]}</h3><p class="body pj">{pr["sar"]}</p></div>
<div class="chips abs en" lang="en" dir="ltr" style="left:19mm;top:136mm">{chips_en}</div>
<div class="chips abs ar" lang="ar" dir="rtl" style="right:19mm;top:136mm">{chips_ar}</div>
<div class="pindex abs"><div class="r3">{idx_ar}</div><div class="r3">{idx_en}</div></div>''')

# ------------------------------------------------------------------ pages 18-19, partners
PARTNERS = [  # file stem, alternative text (as the logo reads; unconfirmed owners described, not named)
 ('existing-01_madinah-award-foundation', 'Partner logo: green dome emblem'), ('existing-02_al-madinah-region-development-authority', 'Al Madinah Region Development Authority'),
 ('existing-03_al-maqar', 'Al Maqar'), ('existing-04_we-ar-spa', 'Partner logo: AR Spa mark'), ('existing-05_mawaddah', 'Mawaddah'),
 ('existing-06_imagine-more', 'Imagine More Travel Agency'), ('existing-07_hsh', 'Partner logo: HSH mark'), ('existing-08_taibah-cooperative', 'Cooperative Taibah'),
 ('existing-09_dar-al-taqwa-hotel', 'Dar Al Taqwa Hotel'), ('existing-10_dallah-taibah-hotel', 'Dallah Taibah Hotel'), ('existing-11_al-madinah-harmony', 'Al Madinah Harmony'),
 ('existing-12_tiny-house', 'Tiny House'), ('existing-13_platinum', 'Platinum'), ('existing-14_madinah-chamber', 'Almadinah Almunawarah Chamber'),
 ('existing-15_manarat-taba-hotel', 'Partner logo: column emblem'), ('existing-16_hippo', 'Hippo'), ('existing-17_taza', 'Taza'),
 ('existing-18_arabic-calligraphic-mark', 'Partner logo: Arabic calligraphic mark'),
 ('new-01_manazil-al-mukhtara', 'Manazil Al-Mukhtara Company'), ('new-02_novotel', 'Novotel Hotels & Resorts'), ('new-03_keeta', 'Keeta'), ('new-04_jahez', 'Jahez'),
 ('new-05_medina-dates-festival', 'International Medina Festival Dates'), ('new-06_hungerstation', 'HungerStation'), ('new-07_rotana', 'Rotana'),
 ('new-08_chop-and-co', 'Chop & Co'), ('new-09_zero', 'ZERO'),
]
# Effective detail width in px where it is lower than the file's pixels (partners/README.md): soft-masked renders.
EFFECTIVE_W = {'existing-02_al-madinah-region-development-authority': 121 / 0.86, 'existing-17_taza': 143 / 0.87}
VECTOR_OK = {'existing-04_we-ar-spa', 'existing-06_imagine-more', 'existing-13_platinum', 'existing-14_madinah-chamber', 'existing-16_hippo'}
CELL_W, CELL_H, MAX_W, MAX_H, AREA = 51.8, 44.0, 34.0, 21.0, 400.0
PARTNER_LOG = []

def partner_dir():
    t = BASE / 'assets/partners-transparent'
    if t.is_dir() and all((t / f'{s}.png').exists() for s, _ in PARTNERS):
        return t, 'assets/partners-transparent'
    return BASE / 'assets/partners', 'assets/partners'

def logo_cell(stem, alt, first=False):
    d, rel = partner_dir()
    im = Image.open(d / f'{stem}.png')
    W, H = im.size
    bb = im.getchannel('A').getbbox() if im.mode == 'RGBA' else (0, 0, W, H)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    k = min(MAX_W / w, MAX_H / h, math.sqrt(AREA / (w * h)))        # mm per px: optical levelling by area, capped both ways
    if stem.startswith('existing') and stem not in VECTOR_OK:        # never above native pixels at 150 ppi
        eff = EFFECTIVE_W.get(stem)
        k = min(k, 25.4 / 150 * ((eff / W) if eff else 1.0))
    ppi = 25.4 / k * ((EFFECTIVE_W[stem] / W) if stem in EFFECTIVE_W else 1)
    PARTNER_LOG.append((stem, w, h, round(w * k, 1), round(h * k, 1), round(ppi)))
    cx, cy = (bb[0] + bb[2]) / 2 * k, (bb[1] + bb[3]) / 2 * k        # centre the visible mark, not the file
    return (f'<div class="pc{" c0" if first else ""}"><img src="{rel}/{stem}.png" alt="{alt}" style="width:{W*k:.2f}mm;height:{H*k:.2f}mm;'
            f'left:{CELL_W/2-cx:.2f}mm;top:{CELL_H/2-cy:.2f}mm"></div>')

def partners(p):
    if p == 18:
        cells = (f'<div class="pc ptitle">{spark(2.4, "#5AC584", "pmark")}<div class="pair"><h2 class="en ttl-p" lang="en" dir="ltr">Partners in Success</h2>'
                 f'<h2 class="ar ttl-p" lang="ar" dir="rtl">شركاء النجاح</h2></div></div>')
        cells += ''.join(logo_cell(s, a, first=(i >= 2 and (i - 2) % 5 == 0)) for i, (s, a) in enumerate(PARTNERS[:12]))
        note = ''
    else:
        cells = ''.join(logo_cell(s, a, first=(i % 5 == 0)) for i, (s, a) in enumerate(PARTNERS[12:]))
        note = ('<div class="pair abs pnote" style="top:176.5mm"><div class="en lbl" lang="en" dir="ltr">All logos are the property of their respective owners.</div>'
                '<div class="ar lbl" lang="ar" dir="rtl">جميع الشعارات ملك لأصحابها.</div></div>')
    return page(p, f'<div class="pgrid abs">{cells}</div>{note}')

# ------------------------------------------------------------------ page 20, contact and back cover
def p20():
    def row(lar, len_, val):
        return (f'<div class="crow"><div class="en lbl" lang="en" dir="ltr">{len_}</div><div class="cval num" dir="ltr">{val}</div>'
                f'<div class="ar lbl" lang="ar" dir="rtl">{lar}</div></div>')
    rows = (row('الهاتف', 'Tel', '<a href="tel:0549555514">054 955 5514</a>')
            + row('البريد الإلكتروني', 'Email', '<a href="mailto:info@otlobny.co">info@otlobny.co</a>')
            + row('الموقع الإلكتروني — يحدده العميل', 'Website — client to confirm', '<span class="pill wpill">otlobny.co&ensp;/&ensp;otlobny.com</span>')
            + row('السجل التجاري', 'Commercial Registration', '4650245200'))
    return page(20, f'''
<img class="abs" style="left:108.3mm;top:26mm;width:80.4mm;height:34mm" src="assets/logo/otlobny-emaar_logo_lockup-proposal-white_ar-en_v01.svg" alt="اطلبني — شركة اطلبني إعمار — OTLOBNY Emaar Co.">
<div class="pair abs" style="top:71mm;left:60mm;width:177mm"><h2 class="en ttl-s" lang="en" dir="ltr">Contact</h2><h2 class="ar ttl-s" lang="ar" dir="rtl">تواصل معنا</h2></div>
<div class="crows abs">{rows}</div>
<div class="abs en" lang="en" dir="ltr" style="left:60mm;top:153mm;width:72mm"><div class="lbl">Address</div><div class="body">Prince Abdulmajeed bin Abdulaziz Road,<br>Al Madinah Al Munawwarah, Saudi Arabia</div></div>
<div class="abs ar" lang="ar" dir="rtl" style="left:165mm;top:153mm;width:72mm"><div class="lbl">العنوان</div><div class="body">طريق الأمير عبدالمجيد بن عبدالعزيز،<br>المدينة المنورة، المملكة العربية السعودية</div></div>
<div class="abs" style="left:147.4mm;top:160mm">{DM}</div>
{band(12, 19, 180, "#fff", .3)}''', 'grad dk', with_chrome=False)

# ------------------------------------------------------------------ CSS
CSS = r'''
@font-face{font-family:"Tajawal";font-weight:400;src:url("assets/fonts/Tajawal-Regular.ttf") format("truetype")}
@font-face{font-family:"Tajawal";font-weight:500;src:url("assets/fonts/Tajawal-Medium.ttf") format("truetype")}
@font-face{font-family:"Tajawal";font-weight:700;src:url("assets/fonts/Tajawal-Bold.ttf") format("truetype")}
@font-face{font-family:"Tajawal";font-weight:800;src:url("assets/fonts/Tajawal-ExtraBold.ttf") format("truetype")}
@font-face{font-family:"IBM Plex Sans";font-weight:400;src:url("assets/fonts/IBMPlexSans-Regular.ttf") format("truetype")}
@font-face{font-family:"IBM Plex Sans";font-weight:500;src:url("assets/fonts/IBMPlexSans-Medium.ttf") format("truetype")}
@font-face{font-family:"IBM Plex Sans";font-weight:600;src:url("assets/fonts/IBMPlexSans-SemiBold.ttf") format("truetype")}
@font-face{font-family:"IBM Plex Sans";font-weight:700;src:url("assets/fonts/IBMPlexSans-Bold.ttf") format("truetype")}
:root{--blue:#3758B0;--green:#5AC584;--navy:#1F3162;--tint:#F7F8FC;--peri:#9BABD7;--grey:#525456;
  --grad:linear-gradient(90deg,#1F3162 0%,#2B458A 52%,#3758B0 100%);--hair:.25pt solid #9BABD7}
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:"IBM Plex Sans",sans-serif;font-synthesis:none;hyphens:none;-webkit-hyphens:none}
a{color:inherit;text-decoration:none}
.page{position:relative;width:297mm;height:210mm;overflow:hidden;background:#fff;break-after:page;page-break-after:always}
.page:last-child{break-after:auto;page-break-after:auto}
.page.tint{background:var(--tint)} .grad{background:var(--grad)}
.abs{position:absolute}
/* languages: Arabic right to left in Tajawal, never tracked; English left to right in IBM Plex Sans */
.ar{font-family:"Tajawal","IBM Plex Sans",sans-serif;direction:rtl;text-align:right;color:var(--navy);letter-spacing:0}
.en{font-family:"IBM Plex Sans",sans-serif;direction:ltr;text-align:left;color:var(--grey)}
.num{font-family:"IBM Plex Sans",sans-serif;direction:ltr;unicode-bidi:isolate;letter-spacing:0}
.dk,.dk .ar,.dk .en{color:#fff}
/* type scale (art-direction.md 2.4) */
.ar.ttl-c{font-weight:800;font-size:46pt;line-height:1.25}        .en.ttl-c{font-weight:700;font-size:38pt;line-height:1.1;letter-spacing:-.01em;color:var(--blue)}
.ar.ttl-s{font-weight:800;font-size:32pt;line-height:1.3}         .en.ttl-s{font-weight:700;font-size:27pt;line-height:1.15;color:var(--blue)}
.ar.ttl-p{font-weight:800;font-size:26pt;line-height:1.3}         .en.ttl-p{font-weight:700;font-size:22pt;line-height:1.15;color:var(--blue)}
.ar.hdg,.ar .hdg{font-weight:700;font-size:20pt;line-height:1.4}  .en.hdg,.en .hdg{font-weight:600;font-size:17pt;line-height:1.25}
.ar.hdg.long{line-height:1.6}                                     .en.hdg.long{line-height:1.35}
.ar.lead,.ar .lead{font-weight:500;font-size:14pt;line-height:1.7} .en.lead,.en .lead{font-weight:400;font-size:12.5pt;line-height:1.5}
.ar .lead.b{font-weight:700;line-height:1.5}                      .en .lead.b{font-weight:600;line-height:1.5}
.ar.body,.ar .body{font-weight:400;font-size:11.5pt;line-height:1.75} .en.body,.en .body{font-weight:400;font-size:10pt;line-height:1.5}
.ar.lbl,.ar .lbl{font-weight:500;font-size:9.5pt;line-height:1.6}  .en.lbl,.en .lbl{font-weight:500;font-size:8.5pt;line-height:1.4;text-transform:uppercase;letter-spacing:.06em}
.dk .en.ttl-s,.dk .en.ttl-p{color:#fff}
p,h1,h2,h3,.body,.lead{text-wrap:pretty}
.nw{white-space:nowrap} .w83{width:83mm} .w105{width:105mm}
.pair h1,.pair h2{white-space:nowrap}
.pair{left:19mm;width:259mm;display:flex;flex-direction:row;direction:ltr;justify-content:space-between;align-items:baseline}
/* running header and folio */
.hd{position:absolute;left:19mm;top:11.2mm;width:259mm;height:5.6mm;display:flex;direction:ltr;justify-content:space-between;align-items:baseline}
.hd-ar .sp{margin-inline-end:1.8mm;vertical-align:-.15mm} .hd-ar .num{font-weight:500;font-size:9pt;margin-left:1.8mm}
.hd-line{position:absolute;left:19mm;top:19mm;width:259mm;border-top:var(--hair)}
.ft{position:absolute;left:19mm;top:193.6mm;width:259mm;display:flex;direction:ltr;justify-content:space-between;align-items:baseline}
.folio{font-weight:500;font-size:9pt;color:var(--navy)}
.dk .hd-line{border-top-color:rgba(255,255,255,.35)} .dk .folio{color:#fff}
/* small devices */
.dm{display:inline-block;flex:none;width:1.56mm;height:1.56mm;margin:.32mm;background:var(--green);border-radius:16%;transform:rotate(45deg)}
.vline{border-left:var(--hair);width:0}
.pill{display:inline-flex;align-items:center;height:6.5mm;padding:0 3.2mm;border:.5pt solid var(--blue);border-radius:3.25mm;color:var(--navy);white-space:nowrap}
.pill.draft{left:50%;transform:translateX(-50%);top:191.6mm;gap:2.4mm;direction:ltr;background:#fff}
.pill.draft .en,.pill.draft .ar{color:var(--navy)}
/* five-column rows: English | gutter | centre | gutter | Arabic */
.rows{left:19mm;width:259mm}
.row5{display:grid;direction:ltr;grid-template-columns:105mm 39mm 105mm;column-gap:5mm;border-top:var(--hair)}
.dk .row5{border-top-color:rgba(255,255,255,.35)}
.row5>.mid{display:flex;justify-content:center;white-space:nowrap}
.toc{height:18mm;align-items:center} .tocn{font-weight:700;font-size:26pt;line-height:1;color:var(--blue)}
.fact{height:16mm;align-items:center} .fact .hdg{line-height:1.3 !important} .fact>.mid{align-items:center}
.bignum{font-weight:700;font-size:40pt;line-height:1;color:var(--blue)} .crnum{font-weight:700;font-size:20pt;line-height:1;color:var(--blue)}
.goal{height:31mm;padding-top:3.6mm;align-items:start} .goal>.mid{margin-top:-.4mm}
.whys{display:flex;flex-direction:column} .why{flex:1 1 auto;padding:2mm 0 1mm;align-items:start} .why>.mid{padding-top:.5mm} .why .ar .body{line-height:1.65}
.svcs{display:flex;flex-direction:column}
.svc{flex:1 1 auto;align-items:center;padding:1mm 0} .svc .ar .hdg{line-height:1.25} .svc .en .hdg{line-height:1.2}
.svc .ar .body{line-height:1.6} .svc .en .body,.why .en .body{margin-top:.5mm}
.mid.col{flex-direction:column;align-items:center;justify-content:center;gap:.4mm}
.holder{position:relative;display:block} .holder>svg:first-child{position:absolute;left:0;top:0}
.holder-ic{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)}
.pg{font-size:9pt;font-weight:500;line-height:1.2;color:#fff}
/* service triptych */
.trip{left:19mm;width:259mm;display:grid;direction:ltr;grid-template-columns:83mm 83mm 83mm;column-gap:5mm;align-items:start}
.c1{grid-column:1} .c5{grid-column:3} .gap6{grid-column:1/-1;height:6mm}
.li{display:flex;align-items:flex-start;gap:2.2mm;min-height:10mm;padding:2mm 0;border-top:var(--hair);align-self:stretch;font-weight:500 !important}
.li.ar{line-height:1.5} .li.en{line-height:1.5} .li.ar .dm{margin-top:1.95mm} .li.en .dm{margin-top:1.86mm}
.li.ar{color:var(--navy)} .after{margin-top:6mm;padding-top:0}
.panel{left:107mm;top:26mm;width:83mm;height:132.5mm;overflow:hidden;clip-path:polygon(0 0,100% 0,100% calc(100% - 27.5mm),calc(100% - 27.5mm) 100%,0 100%)}
.panel img{display:block;width:100%;height:100%;object-fit:cover}
.big-ic{left:18.5mm;top:35mm}
.cap{left:107mm;top:164.6mm;width:83mm;display:flex;direction:ltr;justify-content:space-between;align-items:baseline}
/* project pages */
.frame{left:107mm;top:53.5mm;width:83mm;height:75mm;object-fit:cover;display:block}
.pj{margin-top:4mm}
.chips{display:flex;gap:2mm}
.pindex{left:19mm;top:168mm;width:259mm;border-top:var(--hair);padding-top:2.2mm}
.r3{display:grid;direction:ltr;grid-template-columns:83mm 83mm 83mm;column-gap:5mm;align-items:start} .r3+.r3{margin-top:1.2mm}
.r3>div{display:flex;align-items:flex-start;gap:1.6mm;color:var(--grey)} .r3>.ar{color:var(--grey)}
.r3>.cur{color:var(--navy);font-weight:700} .r3 .dm{margin-top:1.75mm} .r3 .en .dm,.r3>.en .dm{margin-top:1.05mm}
/* partners: logos straight on white, hairline grid, no tiles */
.pgrid{left:19mm;top:40mm;width:259mm;height:132mm;display:grid;direction:rtl;grid-template-columns:repeat(5,51.8mm);grid-template-rows:repeat(3,44mm)}
.pc{position:relative;overflow:hidden;border-inline-start:var(--hair);border-top:var(--hair)}
.pc img{position:absolute;display:block}
.pgrid{border-bottom:var(--hair)}
.ptitle{grid-column:span 3;border-inline-start:0} .pc.c0{border-inline-start:0}
.ptitle .pair{position:absolute;left:3mm;right:0;width:auto;bottom:3.2mm}
.pmark{position:absolute;right:0;top:4mm}
.pnote .ar,.pnote .en{color:var(--grey)}
/* contact */
.crows{left:60mm;top:92mm;width:177mm}
.crow{display:grid;direction:ltr;grid-template-columns:56mm 65mm 56mm;height:14mm;align-items:center;border-top:.25pt solid rgba(255,255,255,.35)}
.crow:last-child{border-bottom:.25pt solid rgba(255,255,255,.35)}
.cval{font-weight:500;font-size:17pt;line-height:1;color:#fff;text-align:center;white-space:nowrap}
.wpill{border-color:rgba(255,255,255,.8);color:#fff;font-size:10pt;font-weight:500}
.dk .lbl{color:#fff}
'''

def grid_overlay():
    cols = ''.join(f'<i style="left:{278-22*(n-1)-17}mm;top:0;width:17mm;height:210mm;background:rgba(255,0,120,.10)"></i>' for n in range(1, 13))
    rows = ''.join(f'<i style="left:19mm;top:{26+27.5*r}mm;width:259mm;height:22.5mm;border-top:.2mm solid rgba(0,160,255,.7);border-bottom:.2mm solid rgba(0,160,255,.7)"></i>' for r in range(6))
    return f'<div class="gridov">{cols}{rows}</div>'

def build():
    pages = [p1(), p2(), p3(), p4(), p5(), p6(), p7()]
    pages += [service(i, s) for i, s in enumerate(SERVICES, 1)]
    pages += [p14()] + [project(i, pr) for i, pr in enumerate(PROJECTS, 1)]
    pages += [partners(18), partners(19), p20()]
    html = ('<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
            '<title>اطلبني إعمار — الملف التعريفي | OTLOBNY Emaar — Company Profile (draft v01)</title>\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<style>{CSS}</style>\n</head>\n<body>\n' + ''.join(pages) + '</body>\n</html>\n')
    OUT.write_text(html, encoding='utf-8')
    g = html.replace('</section>', grid_overlay() + '</section>').replace('"assets/', '"../assets/').replace('url("../assets/', 'url("../assets/')
    g = g.replace('</style>', '.gridov i{position:absolute;display:block}</style>')
    (BASE / '_work' / 'otlobny-emaar_company-profile_grid-proof_v01.html').write_text(g, encoding='utf-8')
    print('wrote', OUT.name, len(pages), 'pages; partner logos from', partner_dir()[1])
    for row in PARTNER_LOG:
        print('  logo %-55s mark %4dx%-4d px -> %5.1f x %4.1f mm, %d ppi' % row)


# ====================================================================== v02
# Client feedback on v01 ("use the images I sent; a visual pleasure"), client answers (logistics confirmed,
# website otlobny.net, nothing from the website), art-director review of v01 (adopted points listed in build-notes_v02.md).
SECTIONS.clear()
SECTIONS.update({2: ('', 'المحتويات', 'Contents'), 3: ('01', 'من نحن', 'About Us'),
 **{p: ('02', 'رؤيتنا ورسالتنا وأهدافنا', 'Vision, Mission and Goals') for p in (4, 5)},
 **{p: ('03', 'خدماتنا', 'Our Services') for p in range(6, 14)},
 14: ('04', 'لماذا اطلبني إعمار', 'Why OTLOBNY Emaar'),
 **{p: ('05', 'أعمالنا', 'Our Work') for p in (15, 16, 17)},
 **{p: ('06', 'شركاء النجاح', 'Partners in Success') for p in (18, 19)}})

DER = BASE / 'assets/derived'
IMG_LOG = []

def prep(name, src, aspect, cx=.5, cy=.5, max_w=None, box=None, page_='', w_mm=None, colour='full colour'):
    """Crop a source to an exact aspect (w/h) around (cx, cy) as fractions, never upscaled; save JPEG; log ppi."""
    im = Image.open(BASE / src).convert('RGB')
    W, H = im.size
    if box:
        l, t, r, b = box
    else:
        w = min(W, H * aspect, max_w or W); h = w / aspect
        l = min(max(0, cx * W - w / 2), W - w); t = min(max(0, cy * H - h / 2), H - h)
        r, b = l + w, t + h
    c = im.crop((round(l), round(t), round(r), round(b)))
    out = DER / f'v02_{name}.jpg'
    c.save(out, quality=86, optimize=True, progressive=True)
    if w_mm:
        IMG_LOG.append((page_, out.name, src, (round(l), round(t), round(r), round(b)), c.size, w_mm, round(c.size[0] / (w_mm / 25.4)), colour))
    return f'assets/derived/{out.name}'

CAP = ('<div class="pair abs capv2" style="top:{top}mm"><span class="en lbl" lang="en" dir="ltr">Illustrative image</span>'
       '<span class="ar lbl" lang="ar" dir="rtl">صورة توضيحية</span></div>')
RET = '06-profiles/assets/derived/'   # retouched mockups (made by retouch_mockups_v02.py), relative to BASE.parent
def R(n):
    return f'assets/derived/mockup_{n}_retouched_v02.png'

def foot(p, light=False):
    folio = f'<span class="folio num" dir="ltr">{p:02d}</span>'
    if p % 2 == 0:
        f = f'<div class="ft{" lt" if light else ""}"><div class="en lbl" lang="en" dir="ltr">{EN_DOC}</div>{folio}</div>'
    else:
        f = f'<div class="ft{" lt" if light else ""}">{folio}<div class="ar lbl" lang="ar" dir="rtl">{AR_DOC}</div></div>'
    return f

# ------------------------------------------------------------------ cover
def v2_cover():
    img = prep('cover_car-scooter-facade', R('car-scooter-facade'), 297 / 210, cx=.49, cy=.5, page_='1', w_mm=297)
    return page(1, f'''
<img class="abs bleed" style="left:0;top:0;width:297mm;height:210mm" src="{img}" alt="Brand vehicles and building sign, illustrative image">
<div class="abs" style="left:0;top:104mm;width:297mm;height:106mm;background:linear-gradient(180deg,rgba(31,49,98,0) 0%,rgba(31,49,98,.78) 42%,rgba(31,49,98,.95) 100%)"></div>
<div class="abs lockpanel"></div>
<img class="abs" style="left:192.8mm;top:15mm;width:85.2mm;height:36mm" src="assets/logo/otlobny-emaar_logo_lockup-proposal-colour_ar-en_v01.svg" alt="اطلبني — شركة اطلبني إعمار — OTLOBNY Emaar Co.">
<div class="pair abs dk" style="top:166mm"><h1 class="en ttl-c" lang="en" dir="ltr">Company Profile</h1><h1 class="ar ttl-c" lang="ar" dir="rtl">الملف التعريفي</h1></div>
{band(12, 119, 193, "#fff", .35)}
{CAP.format(top=199)}''', 'dk', with_chrome=False)

# ------------------------------------------------------------------ contents
def v2_contents():
    rows = [('من نحن', 'About Us', 3), ('رؤيتنا ورسالتنا وأهدافنا', 'Vision, Mission and Goals', 4), ('خدماتنا', 'Our Services', 6),
            ('لماذا اطلبني إعمار', 'Why OTLOBNY Emaar', 14), ('أعمالنا', 'Our Work', 15), ('شركاء النجاح', 'Partners in Success', 18),
            ('تواصل معنا', 'Contact', 20)]
    r = ''.join(f'<a class="toc3" href="#p{n}"><div class="en hdg" lang="en" dir="ltr">{en}</div><div class="tocn num" dir="ltr">{n:02d}</div>'
                f'<div class="ar hdg" lang="ar" dir="rtl">{ar}</div></a>' for ar, en, n in rows)
    img = prep('contents_glass-facade', 'assets/photos/glass-facade-cleaners.png', 107 / 210, cx=.42, cy=.5, page_='2', w_mm=107)
    return page(2, f'''
<img class="abs" style="left:0;top:0;width:107mm;height:210mm" src="{img}" alt="Rope-access cleaners on a glass tower, illustrative image">
<div class="abs" style="left:0;top:0;width:107mm;height:210mm;background:linear-gradient(180deg,rgba(31,49,98,.15) 0%,rgba(31,49,98,.25) 55%,rgba(31,49,98,.9) 100%)"></div>
<img class="abs" style="left:19mm;top:166mm;width:37mm;height:15mm" src="assets/logo/otlobny-emaar_logo_wordmark-white_ar_v01.svg" alt="اطلبني">
<div class="abs capv2 cap-l" style="left:19mm;top:186mm;width:69mm"><span class="en lbl" lang="en" dir="ltr">Illustrative image</span><span class="ar lbl" lang="ar" dir="rtl">صورة توضيحية</span></div>
<div class="abs" style="left:117mm;top:26mm;width:161mm;display:flex;direction:ltr;justify-content:space-between;align-items:baseline">
<h2 class="en ttl-s" lang="en" dir="ltr">Contents</h2><h2 class="ar ttl-s" lang="ar" dir="rtl">المحتويات</h2></div>
<div class="abs" style="left:117mm;top:52mm;width:161mm">{r}</div>{foot(2)}''', 'tint', with_chrome=False)

# ------------------------------------------------------------------ vision and mission, one page, centre image
def v2_vismis():
    img = prep('vismis_office-cleaner', 'assets/photos/office-cleaner.png', 83 / 210, cx=.815, cy=.5, page_='4', w_mm=83)
    va = 'تنطلق رؤيتنا في «اطلبني إعمار» نحو التوسع والتطور المستمر لتحقيق المنافسة في الأسواق المحلية في جميع مجالات عملنا، تماشياً مع رؤية المملكة العربية السعودية 2030.'
    ve = 'At OTLOBNY Emaar, our vision is continuous expansion and development, so that we compete in local markets across all our fields of work, in line with Saudi Vision 2030.'
    ma = 'نسعى في «اطلبني إعمار» إلى تزويد سوق العمل بالقوى العاملة الوطنية والأجنبية التي تتمتع بالكفاءات العالية في كثير من المهن الحرفية والفنية في مجالات خدماتنا، وفق أحدث المعايير المتبعة في المملكة العربية السعودية.'
    me = 'At OTLOBNY Emaar, we work to supply the labour market with highly competent national and expatriate manpower in a wide range of skilled trades and technical occupations across our fields of service, to the latest standards applied in the Kingdom of Saudi Arabia.'
    def col(lang, x, t1, s1, t2, s2):
        d = 'rtl' if lang == 'ar' else 'ltr'
        return (f'<div class="abs {lang} vm" lang="{lang}" dir="{d}" style="left:{x}mm;top:28mm;width:83mm">'
                f'<h2 class="ttl-p">{t1}</h2><p class="stmt">{s1}</p><div class="vmrule"></div><h2 class="ttl-p">{t2}</h2><p class="stmt">{s2}</p></div>')
    return page(4, f'''
<img class="abs" style="left:107mm;top:0;width:83mm;height:210mm" src="{img}" alt="Cleaner at work behind office glass, illustrative image">
<div class="abs capv2 capc" style="left:107mm;top:199mm;width:83mm"><span class="en lbl" lang="en" dir="ltr">Illustrative image</span><span class="ar lbl" lang="ar" dir="rtl">صورة توضيحية</span></div>
{col('en', 19, 'Our Vision', ve, 'Our Mission', me)}{col('ar', 195, 'رؤيتنا', va, 'رسالتنا', ma)}''', 'nohl')

# ------------------------------------------------------------------ services: band master
for s_ in SERVICES:
    s_['p'] -= 1
LOG = SERVICES[5]
LOG.update(sar='التوصيل ونقل البضائع والتخزين وتأجير المركبات.', sen='Delivery, goods transport, storage and vehicle rental.',
           iar='تقدّم «اطلبني إعمار» خدمات لوجستية تشمل التوصيل ونقل البضائع والتخزين وتأجير المركبات.',
           ien='OTLOBNY Emaar provides logistics services covering delivery, goods transport, storage and vehicle rental.',
           items=[('التوصيل', 'Delivery'), ('نقل البضائع', 'Goods transport'), ('التخزين', 'Storage'), ('تأجير المركبات', 'Vehicle rental')])
LOG.pop('draft', None)

BAND_H = 96
BANDS = {'contracting': 100, 'landscaping': 112, 'maintenance': 128, 'cleaning': 126, 'manpower': 100, 'logistics': 128}
def band_imgs():
    a = 0
    return {
     'contracting': [(prep('svc_electrical-panel', 'assets/photos/electrical-panel.png', 297 / BANDS['contracting'], cy=.42, page_='7', w_mm=297), 297, 'Electrician at a distribution board')],
     'landscaping': [(prep('svc_nursery-worker', 'assets/photos/nursery-worker.png', 222 / BANDS['landscaping'], cy=.56, page_='8', w_mm=222), 222, 'Workers tending plants in a greenhouse')],
     'maintenance': [(prep('svc_glass-facade', 'assets/photos/glass-facade-cleaners.png', 297 / BANDS['maintenance'], cy=.45, page_='9', w_mm=297), 297, 'Rope-access team working on a glass facade')],
     'cleaning': [(prep('svc_cleaning-team', R('cleaning-team'), 297 / BANDS['cleaning'], cy=.45, page_='10', w_mm=297), 297, 'Cleaning team in branded uniforms')],
     'manpower': [(prep('svc_waiter', 'assets/photos/waiter.png', 222 / BANDS['manpower'], cy=.42, page_='11', w_mm=222), 222, 'Waiter serving in a restaurant')],
     'logistics': [(prep('svc_truck-front34', R('truck-front34'), 148 / BANDS['logistics'], cx=.5, cy=.55, page_='12', w_mm=148), 148, 'Branded box truck'),
                   (prep('svc_truck-rear34', R('truck-rear34'), 148 / BANDS['logistics'], cx=.5, cy=.55, page_='12', w_mm=148), 148, 'Branded box truck at a warehouse')],
    }

def v2_service(i, s, imgs):
    p = s['p']
    BAND_H = BANDS[s['key']]
    x, parts = 0, ''
    for src, w, alt in imgs[s['key']]:
        parts += f'<img class="abs" style="left:{x}mm;top:0;width:{w}mm;height:{BAND_H}mm" src="{src}" alt="{alt}, illustrative image">'
        x += w + (1 if w < 200 else 0)
    if x < 290:   # modest-resolution photograph: the rest of the band is a brand panel with the service icon
        parts += (f'<div class="abs grad" style="left:{x}mm;top:0;width:{297-x}mm;height:{BAND_H}mm"></div>'
                  f'<div class="abs" style="left:{x + (297-x)/2 - 14}mm;top:14mm">{icon(s["key"], 28, "#fff")}</div>')
    over = f'<div class="abs" style="left:0;top:{BAND_H-50}mm;width:297mm;height:50mm;background:linear-gradient(180deg,rgba(31,49,98,0),rgba(31,49,98,.9))"></div>'
    lab = (f'<div class="pair abs dk" style="top:{BAND_H-25}mm"><div class="en lbl" lang="en" dir="ltr">Our Services <span class="num">{i:02d} / 06</span></div>'
           f'<div class="ar lbl" lang="ar" dir="rtl">خدماتنا <span class="num" dir="ltr">{i:02d} / 06</span></div></div>'
           f'<div class="pair abs dk" style="top:{BAND_H-19.5}mm"><h2 class="en ttl-s" lang="en" dir="ltr">{s["en"]}</h2><h2 class="ar ttl-s" lang="ar" dir="rtl">{s["ar"]}</h2></div>')
    li_en = ''.join(f'<div class="li en body" lang="en" dir="ltr">{DM}<span>{en}</span></div>' for ar, en in s['items'])
    li_ar = ''.join(f'<div class="li ar body" lang="ar" dir="rtl">{DM}<span>{ar}</span></div>' for ar, en in s['items'])
    if s.get('after'):
        li_en += f'<p class="en body after2" lang="en" dir="ltr">{s["after"][1]}</p>'
        li_ar += f'<p class="ar body after2" lang="ar" dir="rtl">{s["after"][0]}</p>'
    T = BAND_H + 11
    body = (f'<p class="abs en lead sv" lang="en" dir="ltr" style="left:19mm;top:{T}mm;width:61mm">{s["ien"]}</p>'
            f'<div class="abs lst" style="left:85mm;top:{T}mm;width:61mm">{li_en}</div>'
            f'<div class="abs lst" style="left:151mm;top:{T}mm;width:61mm">{li_ar}</div>'
            f'<p class="abs ar lead sv" lang="ar" dir="rtl" style="left:217mm;top:{T}mm;width:61mm">{s["iar"]}</p>')
    return page(p, parts + over + lab + CAP.format(top=BAND_H + 2.5) + body + foot(p), with_chrome=False)

# ------------------------------------------------------------------ logistics in pictures
def v2_logistics_gallery():
    h = 83
    views = [('truck-front', 432, 'front'), ('truck-side', 668, 'side'), ('truck-rear', 428, 'rear')]
    k = (297 - 2 * 1.5) / sum(w for _, w, _ in views)
    x, imgs = 0, ''
    for n, w, v in views:
        wm = w * k
        src = prep(f'gal_{n}', R(n), wm / h, cy=.5, page_='13', w_mm=round(wm, 1))
        imgs += f'<img class="abs" style="left:{x:.2f}mm;top:0;width:{wm:.2f}mm;height:{h}mm" src="{src}" alt="Branded box truck, {v} view, illustrative image">'
        x += wm + 1.5
    rider = prep('gal_rider', R('delivery-rider'), 0.47, box=(300, 10, 770, 1010), page_='13', w_mm=52.6)
    return page(13, imgs + f'''
<img class="abs" style="left:122.2mm;top:89mm;width:52.6mm;height:112mm" src="{rider}" alt="Delivery rider with branded jacket and bag, illustrative image">
<div class="abs en" lang="en" dir="ltr" style="left:19mm;top:100mm;width:83mm"><div class="lbl">Our Services <span class="num">06 / 06</span></div>
<h2 class="ttl-s" style="margin-top:2mm">{LOG["en"]}</h2><p class="stmt2">{LOG["sen"]}</p></div>
<div class="abs ar" lang="ar" dir="rtl" style="left:195mm;top:100mm;width:83mm"><div class="lbl">خدماتنا <span class="num" dir="ltr">06 / 06</span></div>
<h2 class="ttl-s" style="margin-top:2mm">{LOG["ar"]}</h2><p class="stmt2">{LOG["sar"]}</p></div>
{CAP.format(top=181)}{foot(13)}''', with_chrome=False)

# ------------------------------------------------------------------ works: bigger frame, no index (AD review change 2)
WORK_CROPS = {15: ('assets/photos/bus-shelter.png', (0.41, 0.0, 0.989, 1.0)), 16: ('assets/photos/chamber-building.png', (0.137, 0.0, 0.99, 1.0)),
              17: ('assets/photos/shahd-hotel.png', (0.20, 0.085, 0.979, 1.0))}
def v2_project(i, pr):
    src, (fl, ft, fr, fb) = WORK_CROPS[pr['p']]
    W, H = Image.open(BASE / src).size
    l, r, t, b = fl * W, fr * W, ft * H, fb * H
    asp = 127 / 105
    if (r - l) / (b - t) > asp:      # too wide: trim both sides evenly
        d = ((r - l) - (b - t) * asp) / 2; l, r = l + d, r - d
    else:                            # too tall: trim the top
        t = b - (r - l) / asp
    img = prep(f'work_{pr["p"]}', src, asp, box=(l, t, r, b), page_=str(pr['p']), w_mm=127)
    lab_ar = f'<span class="num" dir="ltr">{i:02d} / 03</span>'; lab_en = f'<span class="num">{i:02d} / 03</span>'
    chips_ar = ''.join(f'<span class="pill ar lbl">{a}</span>' for a, _ in pr['chips'])
    chips_en = ''.join(f'<span class="pill en lbl">{e}</span>' for _, e in pr['chips'])
    return page(pr['p'], titles('أعمالنا', 'Our Work', label_ar=lab_ar, label_en=lab_en) + f'''
<img class="abs" style="left:85mm;top:53.5mm;width:127mm;height:105mm;object-fit:cover" src="{img}" alt="{pr["alt"]}">
<div class="abs en" lang="en" dir="ltr" style="left:19mm;top:53.5mm;width:61mm"><h3 class="hdg">{pr["en"]}</h3><p class="body pj">{pr["sen"]}</p></div>
<div class="abs ar" lang="ar" dir="rtl" style="left:217mm;top:53.5mm;width:61mm"><h3 class="hdg">{pr["ar"]}</h3><p class="body pj">{pr["sar"]}</p></div>
<div class="chips2 abs en" lang="en" dir="ltr" style="left:19mm;bottom:{210-158.5}mm;width:61mm">{chips_en}</div>
<div class="chips2 abs ar" lang="ar" dir="rtl" style="left:217mm;bottom:{210-158.5}mm;width:61mm">{chips_ar}</div>''')

# ------------------------------------------------------------------ partners (AD review section 3)
AD_W = {'existing-01': 14.7, 'existing-02': 30.0, 'existing-03': 29.5, 'existing-04': 28.0, 'existing-05': 33.0, 'existing-06': 36.0,
        'existing-07': 32.0, 'existing-08': 20.3, 'existing-09': 42.0, 'existing-10': 24.2, 'existing-11': 38.0, 'existing-12': 34.0,
        'existing-13': 31.0, 'existing-14': 38.0, 'existing-15': 19.9, 'existing-16': 16.6, 'existing-17': 28.0, 'existing-18': 30.0,
        'new-01': 30.1, 'new-02': 38.0, 'new-03': 31.0, 'new-04': 28.0, 'new-05': 17.4, 'new-06': 32.0, 'new-07': 38.0, 'new-08': 28.0, 'new-09': 38.0}
TIER_B = {f'existing-{n:02d}' for n in (1, 2, 3, 5, 8, 9, 10, 11, 15, 17)}
TIER_C = {'existing-07', 'existing-18'}
PLOG2 = []
def v2_logo(stem, alt, cx, cy):
    d, rel = partner_dir()
    im = Image.open(d / f'{stem}.png'); W, H = im.size
    bb = im.getchannel('A').getbbox() if im.mode == 'RGBA' else (0, 0, W, H)
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    key = stem.split('_')[0]
    k = AD_W[key] / w                                       # mm per px
    eff = (EFFECTIVE_W[stem] / W) if stem in EFFECTIVE_W else 1.0
    floor = 100 if key in TIER_B else 80 if key in TIER_C else 0
    if floor:
        k = min(k, 25.4 / floor * eff)
    ppi = 25.4 / k * eff
    PLOG2.append((stem, round(w * k, 1), round(h * k, 1), round(ppi)))
    ox, oy = cx - (bb[0] + bb[2]) / 2 * k, cy - (bb[1] + bb[3]) / 2 * k
    return f'<img class="abs" src="{rel}/{stem}.png" alt="{alt}" style="left:{ox:.2f}mm;top:{oy:.2f}mm;width:{W*k:.2f}mm;height:{H*k:.2f}mm">'

def v2_partners(p):
    if p == 18:
        items, xs = PARTNERS[:15], [252.1, 200.3, 148.5, 96.7, 44.9]
    else:
        items, xs = PARTNERS[15:], [245.6, 180.9, 116.1, 51.4]
    ys = [77.25, 119.75, 162.25]
    logos = ''.join(v2_logo(s, a, xs[n % len(xs)], ys[n // len(xs)]) for n, (s, a) in enumerate(items))
    rules = ''.join(f'<div class="abs" style="left:19mm;top:{y}mm;width:259mm;border-top:var(--hair)"></div>' for y in (56, 98.5, 141, 183.5))
    o = f'{p-17:02d} / 02'
    note = ('<div class="pair abs pnote" style="top:186.5mm"><div class="en lbl" lang="en" dir="ltr">All logos are the property of their respective owners.</div>'
            '<div class="ar lbl" lang="ar" dir="rtl">جميع الشعارات ملك لأصحابها.</div></div>') if p == 19 else ''
    return page(p, titles('شركاء النجاح', 'Partners in Success', 'ttl-s', label_ar=f'<span class="num" dir="ltr">{o}</span>',
                          label_en=f'<span class="num">{o}</span>', wide=True) + rules + logos + note)

# ------------------------------------------------------------------ contact and back cover (AD review change 6; client answer: otlobny.net)
def v2_contact():
    def row(lar, len_, val):
        return (f'<div class="crow2"><div class="en lbl" lang="en" dir="ltr">{len_}</div><div class="cval2 num" dir="ltr">{val}</div>'
                f'<div class="ar lbl" lang="ar" dir="rtl">{lar}</div></div>')
    rows = (row('الهاتف', 'Tel', '<a href="tel:+966549555514">054 955 5514</a>')
            + row('البريد الإلكتروني', 'Email', '<a href="mailto:info@otlobny.co">info@otlobny.co</a>')
            + row('الموقع الإلكتروني', 'Website', '<a href="https://otlobny.net">otlobny.net</a>')
            + row('السجل التجاري', 'Commercial Registration', '4650245200'))
    return page(20, f'''
<img class="abs" style="left:101.15mm;top:22mm;width:94.7mm;height:40mm" src="assets/logo/otlobny-emaar_logo_lockup-proposal-white_ar-en_v01.svg" alt="اطلبني — شركة اطلبني إعمار — OTLOBNY Emaar Co.">
<div class="abs" style="left:41mm;top:74mm;width:215mm;display:flex;direction:ltr;justify-content:space-between;align-items:baseline"><h2 class="en ttl-p" lang="en" dir="ltr">Contact</h2><h2 class="ar ttl-p" lang="ar" dir="rtl">تواصل معنا</h2></div>
<div class="abs" style="left:41mm;top:94mm;width:215mm">{rows}</div>
<div class="abs" style="left:41mm;top:158mm;width:215mm;display:flex;direction:ltr;justify-content:space-between;align-items:flex-start">
<div class="en" lang="en" dir="ltr"><div class="lbl">Address</div><div class="body">Prince Abdulmajeed bin Abdulaziz Road,<br>Al Madinah Al Munawwarah, Saudi Arabia</div></div>
<div class="ar" lang="ar" dir="rtl"><div class="lbl">العنوان</div><div class="body">طريق الأمير عبدالمجيد بن عبدالعزيز،<br>المدينة المنورة، المملكة العربية السعودية</div></div></div>
{band(12, 119, 184, "#fff", .3)}''', 'grad dk', with_chrome=False)

CSS += r'''
.bleed{object-fit:cover;display:block}
img.abs{display:block;object-fit:cover}
.lockpanel{left:183mm;top:0;width:114mm;height:64mm;background:#fff;clip-path:polygon(0 0,100% 0,100% 100%,22mm 100%,0 calc(100% - 22mm))}
.dk .en.ttl-c{color:#fff}
.capv2{left:19mm;width:259mm;display:flex;direction:ltr;justify-content:space-between}
.capv2 .lbl{font-size:7pt !important;color:var(--grey)} .dk .capv2 .lbl,.capv2.lt .lbl{color:rgba(255,255,255,.85)}
.cap-l .lbl,.capc .lbl{color:rgba(255,255,255,.9) !important}
.capc{padding:0 3mm}
.ft.lt .lbl,.ft.lt .folio{color:#fff}
.toc3{display:grid;direction:ltr;grid-template-columns:64mm 23mm 64mm;column-gap:5mm;height:18.5mm;align-items:center;border-top:var(--hair)}
.toc3 .tocn{text-align:center}
.nohl .hd-line{display:none} .nohl .hd .en.lbl{width:83mm} .nohl .hd .ar.lbl{width:83mm;justify-content:flex-start}
.vm .ttl-p{white-space:nowrap}
.ar .stmt{font-weight:700;font-size:16.5pt;line-height:1.6;margin-top:3mm;color:var(--navy)}
.en .stmt{font-weight:500;font-size:13.5pt;line-height:1.42;margin-top:3.6mm;color:var(--navy)}
.vmrule{border-top:.75pt solid var(--green);width:17mm;margin:7mm 0 6mm}
.ar .vmrule{margin-right:0;margin-left:auto}
.ar.lead.sv{font-size:13pt;line-height:1.7} .en.lead.sv{font-size:11.5pt;line-height:1.5}
.lst .li{min-height:9mm;padding:1.8mm 0}
.lst .li:last-of-type{border-bottom:var(--hair)}
.after2{margin-top:4mm}
.dk .lbl{color:#fff}
.stmt2{margin-top:5mm}
.en .stmt2{font-weight:500;font-size:15pt;line-height:1.4;color:var(--navy)}
.ar .stmt2{font-weight:700;font-size:18pt;line-height:1.6;color:var(--navy)}
.chips2{display:flex;flex-wrap:wrap;gap:1.5mm 2mm}
.pill.ar{padding-top:.9mm}
.pnote .ar,.pnote .en{color:var(--grey)}
.crow2{display:grid;direction:ltr;grid-template-columns:70mm 75mm 70mm;height:15mm;align-items:center;border-top:.25pt solid rgba(255,255,255,.35)}
.crow2:last-child{border-bottom:.25pt solid rgba(255,255,255,.35)}
.cval2{font-weight:500;font-size:20pt;line-height:1;color:#fff;text-align:center;white-space:nowrap}
.fact .bignum{font-size:28pt} .crnum{font-size:22pt !important}
.rows>.row5:first-child{border-top:var(--hair)}
'''

def build_v2():
    imgs = band_imgs()
    pages = [v2_cover(), v2_contents(), p3(), v2_vismis(), p6(), p7()]
    pages += [v2_service(i, s, imgs) for i, s in enumerate(SERVICES, 1)]
    pages += [v2_logistics_gallery(), p14()] + [v2_project(i, pr) for i, pr in enumerate(PROJECTS, 1)]
    pages += [v2_partners(18), v2_partners(19), v2_contact()]
    html = ('<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
            '<title>اطلبني إعمار — الملف التعريفي | OTLOBNY Emaar — Company Profile (draft v02)</title>\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<style>{CSS}</style>\n</head>\n<body>\n' + ''.join(pages) + '</body>\n</html>\n')
    OUT.write_text(html, encoding='utf-8')
    print('wrote', OUT.name, len(pages), 'pages')
    for r in IMG_LOG:
        print('  img p%-3s %-34s %-48s crop %s px %s -> %s mm wide, %d ppi, %s' % r)
    for r in PLOG2:
        print('  logo %-55s %5.1f x %4.1f mm, %d ppi' % r)

if __name__ == '__main__':
    build_v2()
