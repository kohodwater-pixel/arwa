# Art-director geometry sketch for the v01 review. NOT a deliverable; checks that the review's numbers fit.
from PIL import Image
import glob, os
W = {'existing-01':14.7,'existing-02':30,'existing-03':29.5,'existing-04':28,'existing-05':33,'existing-06':36,'existing-07':32,'existing-08':20.3,'existing-09':42,'existing-10':24.2,'existing-11':38,'existing-12':34,'existing-13':31,'existing-14':38,'existing-15':19.9,'existing-16':16.6,'existing-17':28,'existing-18':30,'new-01':30.1,'new-02':38,'new-03':31,'new-04':28,'new-05':17.4,'new-06':32,'new-07':38,'new-08':28,'new-09':38}
order = list(W.keys())
def logo(key, cx, cy):
    f = [p for p in glob.glob('../assets/partners-transparent/'+key+'_*.png') if '_on-' not in os.path.basename(p)][0]
    im = Image.open(f).convert('RGBA'); bb = im.getchannel('A').point(lambda v:255 if v>24 else 0).getbbox()
    s = W[key]/(bb[2]-bb[0])  # mm per px
    x = cx - ((bb[0]+bb[2])/2)*s; y = cy - ((bb[1]+bb[3])/2)*s
    return f'<img class="abs" src="{f}" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{im.width*s:.2f}mm">'
def hdr(n, ar, en, folio):
    return f'''<div class="abs ar lbl" style="right:19mm;top:12mm">✦ {n} {ar}</div><div class="abs en lbl" style="left:19mm;top:12mm">{en}</div><div class="abs" style="left:19mm;width:259mm;top:19mm;border-top:var(--hair)"></div><div class="abs en" style="left:19mm;top:194mm;font-size:9pt;color:var(--navy)">{folio}</div>'''
def title(ar, en, ordn=None, size=(26,22)):
    o = f'<div class="abs ar lbl" style="right:19mm;top:26mm">{ordn}</div><div class="abs en lbl" style="left:19mm;top:26mm">{ordn}</div>' if ordn else ''
    return o + f'<div class="abs ar" style="right:19mm;top:31.5mm;font-weight:800;font-size:{size[0]}pt;line-height:1.3">{ar}</div><div class="abs en" style="left:19mm;top:31.5mm;font-weight:700;font-size:{size[1]}pt;line-height:1.15;color:var(--blue)">{en}</div>'
def partners(page, keys, cols, ordn):
    h = hdr('06','شركاء النجاح','PARTNERS IN SUCCESS', page) + title('شركاء النجاح','Partners in Success', ordn, (32,27))
    cw = 259/cols
    for r in range(4): h += f'<div class="abs" style="left:19mm;width:259mm;top:{56+42.5*r}mm;border-top:var(--hair)"></div>'
    for i,k in enumerate(keys):
        r, c = divmod(i, cols); cx = 278 - cw*(c+0.5); cy = 56+42.5*r+21.25
        h += logo(k, cx, cy)
    if page=='19': h += '<div class="abs ar lbl" style="right:19mm;top:186.5mm">جميع الشعارات ملك لأصحابها.</div><div class="abs en lbl" style="left:19mm;top:186.5mm">All logos are the property of their respective owners.</div>'
    return f'<div class="page">{h}</div>'
def rows_page(n, ordn, ar_t, en_t, ar_i, en_i, items, extra=None):
    h = hdr('03','خدماتنا','OUR SERVICES', n) + title(ar_t, en_t, ordn)
    h += '<div class="abs" style="left:141.5mm;top:28mm;width:14mm;height:14mm;border:.75pt solid var(--blue);border-radius:16%;transform:rotate(45deg)"></div>'
    h += f'<div class="abs flow" style="left:19mm;width:259mm;top:53.5mm"><div class="row3"><div class="ar lead">{ar_i}</div><div></div><div class="en lead">{en_i}</div></div><div style="height:8mm"></div>'
    for a,e in items: h += f'<div class="row3 hr"><div class="ar hd">{a}</div><div class="c"><i class="dia"></i></div><div class="en hd">{e}</div></div>'
    if extra: h += f'<div class="row3 hr" style="min-height:0"><div class="ar body">{extra[0]}</div><div></div><div class="en body">{extra[1]}</div></div>'
    return f'<div class="page">{h}</div></div>'
cover = '''<div class="page">
<div class="abs" style="inset:0;background:var(--grad);clip-path:polygon(0 0,163.5mm 0,0 163.5mm)"></div>
<div class="abs" style="left:83.5mm;top:27mm;width:130mm;height:130mm"><div style="position:absolute;left:19.04mm;top:19.04mm;width:91.92mm;height:91.92mm;border-radius:16%;transform:rotate(45deg);overflow:hidden"><div style="position:absolute;left:-19.04mm;top:-19.04mm;width:130mm;height:130mm;transform:rotate(-45deg);background:url(../assets/derived/cover_glass-facade_duotone.png) center/cover"></div></div></div>
<div class="abs" style="left:185.14mm;top:128.64mm;width:12.73mm;height:12.73mm;background:var(--green);border-radius:16%;transform:rotate(45deg)"></div>
<div class="abs" style="left:19mm;top:26mm;width:59mm;height:12mm;background:radial-gradient(circle,rgba(255,255,255,.3) .5mm,transparent .6mm) 0 0/5mm 5mm"></div><img class="abs" src="../assets/logo/otlobny-emaar_logo_lockup-proposal-colour_ar-en_v01.svg" style="right:19mm;top:22mm;height:36mm">
<div class="abs ar" style="right:19mm;top:164mm;font-weight:800;font-size:46pt;line-height:1.25">الملف التعريفي</div>
<div class="abs en" style="left:19mm;top:170mm;font-weight:700;font-size:38pt;line-height:1.1;color:var(--blue)">Company Profile</div>
</div>'''
vision = '<div class="page">' + hdr('02','رؤيتنا ورسالتنا وأهدافنا','VISION, MISSION AND GOALS','05') + title('رسالتنا','Our Mission') + '''<div class="abs" style="left:148.5mm;top:53.5mm;height:132.5mm;border-left:var(--hair)"></div>
<div class="abs ar" style="right:19mm;width:105mm;top:53.5mm;font-weight:700;font-size:24pt;line-height:1.5">نسعى في «اطلبني إعمار» إلى تزويد سوق العمل بالقوى العاملة الوطنية والأجنبية التي تتمتع بالكفاءات العالية في كثير من المهن الحرفية والفنية في مجالات خدماتنا، وفق أحدث المعايير المتبعة في المملكة العربية السعودية.</div>
<div class="abs en" style="left:19mm;width:105mm;top:55mm;font-weight:600;font-size:19pt;line-height:1.35;color:var(--grey)">At OTLOBNY Emaar, we work to supply the labour market with highly competent national and expatriate manpower in a wide range of skilled trades and technical occupations across our fields of service, to the latest standards applied in the Kingdom of Saudi Arabia.</div></div>'''
proj = '<div class="page">' + hdr('05','أعمالنا','OUR WORK','16') + title('أعمالنا','Our Work','02 / 03') + '''<div class="abs" style="left:85mm;top:53.5mm;width:127mm;height:105mm;background:url(../assets/photos/chamber-building.png) center/cover"></div>
<div class="abs ar" style="right:19mm;width:61mm;top:53.5mm"><div class="hd" style="line-height:1.6">الغرفة التجارية والصناعية في المدينة المنورة</div><div class="body" style="margin-top:4mm">قدمت «اطلبني إعمار» خدمات التشغيل والصيانة والنظافة للغرفة التجارية والصناعية في المدينة المنورة.</div></div>
<div class="abs en" style="left:19mm;width:61mm;top:53.5mm"><div class="hd" style="line-height:1.35">Madinah Chamber of Commerce and Industry</div><div class="body" style="margin-top:4mm">OTLOBNY Emaar provided operation, maintenance and cleaning services for the Madinah Chamber of Commerce and Industry.</div></div>
<div class="abs ar" style="right:19mm;top:152mm"><span class="chip ar">تشغيل</span> <span class="chip ar">صيانة</span> <span class="chip ar">نظافة</span></div>
<div class="abs en" style="left:19mm;top:152mm;width:61mm"><span class="chip">OPERATION</span> <span class="chip">MAINTENANCE</span> <span class="chip">CLEANING</span></div></div>'''
css = open('../otlobny-emaar_company-profile_screen_ar-en_v01.html',encoding='utf8').read().split('<style>')[1].split('.page{')[0].replace('assets/fonts','../../assets/fonts')
css += '''.page{position:relative;width:297mm;height:210mm;overflow:hidden;background:#fff;margin-bottom:4mm}.abs{position:absolute}
.ar{font-family:"Tajawal";direction:rtl;text-align:right;color:var(--navy)}.en{font-family:"IBM Plex Sans";direction:ltr;text-align:left;color:var(--grey)}
.ar.lbl{font-size:9.5pt;font-weight:500}.en.lbl{font-size:8.5pt;font-weight:500;text-transform:uppercase;letter-spacing:.06em}
.ar.lead,.ar .lead{font-size:14pt;font-weight:500;line-height:1.7}.en.lead{font-size:12.5pt;line-height:1.5}
.ar.hd,.ar .hd{font-size:20pt;font-weight:700;line-height:1.6}.en.hd,.en .hd{font-size:17pt;font-weight:600;line-height:1.35}
.ar.body,.ar .body{font-size:11.5pt;line-height:1.75}.en.body,.en .body{font-size:10pt;line-height:1.5}
.row3{display:grid;grid-template-columns:105mm 39mm 105mm;column-gap:5mm;direction:rtl}.row3.hr{border-top:var(--hair);padding-top:4mm;min-height:22.5mm;padding-bottom:3mm}
.c{text-align:center;padding-top:3.4mm}.dia{display:inline-block;width:2.6mm;height:2.6mm;background:var(--green);transform:rotate(45deg);border-radius:16%}
.chip{display:inline-flex;align-items:center;height:6.5mm;padding:0 3mm;border:.5pt solid var(--blue);border-radius:4mm;font-size:8.5pt;font-weight:500;letter-spacing:.06em;color:var(--navy);margin:0 0 1.5mm 0}.chip.ar{font-size:9.5pt;letter-spacing:0;font-family:"Tajawal";padding-top:.6mm}
'''
pages = [cover, vision,
 rows_page('10','03 / 06','الصيانة','Maintenance','تقدم «اطلبني إعمار» خدمات صيانة شاملة للمنشآت، عن طريق فريق احترافي من الكوادر المؤهلة.','OTLOBNY Emaar provides comprehensive maintenance services for facilities, delivered by a professional team of qualified staff.',[('تشغيل وصيانة أنظمة التكييف المركزية','Operation and maintenance of central air-conditioning systems'),('تشغيل وصيانة أنظمة المصاعد','Operation and maintenance of lift systems')]),
 rows_page('12','05 / 06','تأمين الكوادر','Manpower Supply','توفر «اطلبني إعمار» الكوادر النظامية المؤهلة لسوق العمل في مجالات الضيافة والخدمات، للمرافق الحكومية والتجارية والخاصة، وفقاً لمعايير الصحة المهنية.','OTLOBNY Emaar supplies qualified, legally compliant staff for hospitality and services roles in government, commercial and private facilities, in line with occupational health standards.',[('تأجير عمال نظافة للمستشفيات والفنادق والمطارات','Cleaning staff for hospitals, hotels and airports'),('تأجير خدمات عمال للفعاليات والمناسبات','Staff for events and functions'),('توفير عمال المقاهي والمطاعم والإعاشة','Staff for cafés, restaurants and catering')],('تُبرم العقود شهرياً أو سنوياً على نظام «أجير».','Contracts are monthly or annual, through the Ajeer system.')),
 proj, partners('18', order[:15], 5, '01 / 02'), partners('19', order[15:], 4, '02 / 02')]
open('ad-sketch_v01/ad-sketch_v01.html','w',encoding='utf8').write('<!DOCTYPE html><html><head><meta charset="utf-8"><style>'+css.replace('../assets','../../assets')+'</style></head><body>'+''.join(pages).replace('../assets','../../assets')+'</body></html>')
