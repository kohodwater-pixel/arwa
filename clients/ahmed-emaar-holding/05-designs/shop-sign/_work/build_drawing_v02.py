"""v02 technical drawings: A3 landscape, artwork at exactly 1:10.
Arabic and English are given in separate blocks (Arabic first). Dimension
labels on the drawing are numbers with a [ref] keyed to the size table."""
import json, re
M = json.load(open('metrics_v02.json'))
W, H, LPM = M['W_cm'], M['H_cm'], M['legibility_m_per_cm']
FONTS = '/home/user/arwa/assets/fonts'


def dim_h(x1, x2, y, label, tick=2.5):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" class="d"/>'
            f'<line x1="{x1}" y1="{y-tick}" x2="{x1}" y2="{y+tick}" class="d"/><line x1="{x2}" y1="{y-tick}" x2="{x2}" y2="{y+tick}" class="d"/>'
            f'<text x="{(x1+x2)/2}" y="{y-1.6}" class="t" text-anchor="middle">{label}</text>')


def dim_v(x, y1, y2, label, side='right', tick=2.5):
    tx, anc = (x + 2, 'start') if side == 'right' else (x - 2, 'end')
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="d"/>'
            f'<line x1="{x-tick}" y1="{y1}" x2="{x+tick}" y2="{y1}" class="d"/><line x1="{x-tick}" y1="{y2}" x2="{x+tick}" y2="{y2}" class="d"/>'
            f'<text x="{tx}" y="{(y1+y2)/2+1.2}" class="t" text-anchor="{anc}">{label}</text>')


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="e"/>'


def row(ar_label, en_label, ar_val, en_val):
    return (f'<tr><td class="k"><div>{ar_label}</div><div class="en">{en_label}</div></td>'
            f'<td><div>{ar_val}</div><div class="en">{en_val}</div></td></tr>')


def build(opt):
    I = M[opt]; p = I['pos']; mk, na, ne = I['mark'], I['name_ar'], I['name_en']
    tg = I.get('tagline'); mg = I['margins']
    art = open(f'v02_option-{opt}_full.svg').read()
    art = re.sub(r'<svg[^>]*?>', '<svg xmlns="http://www.w3.org/2000/svg" x="0" y="0" width="250" height="60" viewBox="0 0 250 60">', art, count=1)
    art = re.sub(r'<title>.*?</title>', '', art)
    xl = min(p['left'], tg['x0']) if tg else p['left']
    xr = max(p['x_right'], tg['x1']) if tg else p['x_right']
    g = [dim_h(0, W, -12, f'[1] {W:.0f}'), ext(0, -14, 0, 0), ext(W, -14, W, 0),
         dim_v(W + 26, 0, H, f'[2] {H:.0f} *'), ext(W, 0, W + 28, 0), ext(W, H, W + 28, H),
         dim_v(W + 6, p['top'], p['bottom'], f'[3] {mk["h"]}'),
         dim_h(xr, W, H + 9, f'{mg["right"]}'), dim_h(0, xl, H + 9, f'{mg["left"]}'),
         ext(xr, p['bottom'], xr, H + 11), ext(xl, p['lat_base'], xl, H + 11),
         dim_v(-8, 0, p['top'], f'{mg["top"]}', 'left'),
         dim_v(-22, p['ar_base'] - na['alef_h'], p['ar_base'], f'[4] {na["alef_h"]}', 'left'),
         ext(-22, p['ar_base'], p['left'], p['ar_base']),
         dim_v(-8, p['lat_top'], p['lat_base'], f'[5] {ne["cap"]}', 'left'),
         ext(-8, p['lat_top'], p['left'], p['lat_top'])]
    if tg:
        g += [dim_v(-22, tg['base'] - tg['alef_h'], tg['base'], f'[6] {tg["alef_h"]}', 'left'),
              ext(-22, tg['base'], tg['x0'], tg['base']),
              dim_v(-8, tg['bottom'], H, f'{mg["bottom"]}', 'left')]
    else:
        g.append(dim_v(-8, p['bottom'], H, f'{mg["bottom"]}', 'left'))
    drawing = (f'<svg xmlns="http://www.w3.org/2000/svg" width="360mm" height="96mm" viewBox="-60 -22 360 96" style="direction:ltr">'
               f'<style>.d{{stroke:#c0392b;stroke-width:.25;fill:none}}.e{{stroke:#c0392b;stroke-width:.15;stroke-dasharray:1 .8}}'
               f'.t{{font-family:"Plex Arabic";font-size:3.1px;fill:#222}}</style>{art}{"".join(g)}</svg>')
    L = 'أ' if opt == 'a' else 'ب'
    leg = lambda h: f'{h * LPM:.0f}'
    sizes = [
        row('[1] العرض الكلي', '[1] Overall width', f'{W:.0f} سم', f'{W:.0f} cm'),
        row('[2] الارتفاع', '[2] Height', f'{H:.0f} سم — تقديري، يُقاس في الموقع *', f'{H:.0f} cm — estimate, to be measured on site *'),
        row('[3] الشعار (ارتفاع × عرض)', '[3] Mark (h × w)', f'{mk["h"]} × {mk["w"]} سم', f'{mk["h"]} × {mk["w"]} cm'),
        row('[4] الاسم العربي', '[4] Arabic name', f'ارتفاع الألف {na["alef_h"]} سم؛ الامتداد الكلي مع الهمزتين {na["full_extent"]} سم؛ العرض {na["width"]} سم',
            f'alef height {na["alef_h"]} cm; full extent incl. hamzas {na["full_extent"]} cm; width {na["width"]} cm'),
        row('[5] الاسم الإنجليزي', '[5] English name', f'ارتفاع الحرف الكبير {ne["cap"]} سم؛ العرض {ne["width"]} سم', f'cap height {ne["cap"]} cm; tracking {ne["tracking_em"]} em; width {ne["width"]} cm'),
    ]
    if tg:
        sizes.append(row('[6] الشعار النصي', '[6] Tagline', f'«حلول متكاملة للبنية التحتية والخدمات» — ارتفاع الألف {tg["alef_h"]} سم؛ العرض {tg["width"]} سم',
                         f'alef height {tg["alef_h"]} cm; width {tg["width"]} cm'))
    sizes.append(row('الهوامش إلى الحروف', 'Margins to lettering', f'أعلى {mg["top"]}، أسفل {mg["bottom"]}، يمين {mg["right"]}، يسار {mg["left"]} سم. الخطوط الذهبية الزخرفية وحدها تصل إلى الحافة.',
                     f'top {mg["top"]}, bottom {mg["bottom"]}, right {mg["right"]}, left {mg["left"]} cm. Only the decorative gold lines reach the edge.'))
    strokes = [
        row('الشعار', 'Mark', f'الأعمدة {mk["stroke_bars"][0]}–{mk["stroke_bars"][1]} سم؛ أنحف جزء في القوس {mk["stroke_min"]} سم؛ الذيل المنحني حتى {mk["swoosh_max"]} سم ويضيق إلى رأس حاد',
            f'bars {mk["stroke_bars"][0]}–{mk["stroke_bars"][1]} cm; thinnest arch {mk["stroke_min"]} cm; swoosh up to {mk["swoosh_max"]} cm, tapering to a sharp tip'),
        row('الاسم العربي', 'Arabic name', f'الجذع الرأسي {na["stem"]} سم؛ الخط الأفقي {na["horiz_stroke"]} سم', f'vertical stem {na["stem"]} cm; horizontal stroke {na["horiz_stroke"]} cm'),
        row('الاسم الإنجليزي', 'English name', f'الجذع {ne["stem"]} سم؛ الخط الأفقي نحو {ne["bar"]} سم', f'stem {ne["stem"]} cm; horizontal bar ≈ {ne["bar"]} cm'),
    ]
    if tg:
        strokes.append(row('الشعار النصي', 'Tagline', f'الجذع {tg["stem"]} سم؛ الخط الأفقي {tg["horiz_stroke"]} سم', f'stem {tg["stem"]} cm; horizontal stroke {tg["horiz_stroke"]} cm'))
    strokes.append(row('الخطوط الذهبية', 'Gold lines', '1.2 سم، بزاوية 41° مثل قطع الشعار', '1.2 cm, at 41° like the cut of the mark'))
    fab = [
        row('حروف مجسّمة مضيئة', 'Channel letters (lit)', 'الشعار والاسم العربي: يمكن تنفيذهما حروفًا مجسّمة بإضاءة خلفية (هالة)، عمق 5–8 سم. يُقترح تثخين طرف الذيل المنحني قليلًا.',
            'Mark and Arabic name: can be built as halo-lit channel letters, 5–8 cm deep. Suggest blunting the swoosh tip slightly.'),
        row('قصّ مسطّح', 'Flat-cut (unlit)', 'الاسم الإنجليزي' + ('، الشعار النصي' if tg else '') + ' والخطوط الذهبية: خطوطها أنحف من أن تُنفَّذ حروفًا مضيئة؛ تُقصّ مسطّحة 5–10 مم (أكريليك ذهبي مرآة أو ستانلس ذهبي) وتُثبّت بفواصل.',
            'English name' + (', tagline' if tg else '') + ' and gold lines: strokes too thin for lit letters; flat-cut 5–10 mm (gold mirror acrylic or gold-finish stainless), stud-mounted.'),
        row('اللوح', 'Panel', 'ألمنيوم مركّب ACP أو صينية ألمنيوم مدهونة بالفرن، كحلي، وجه واحد', 'Navy ACP or powder-coated aluminium tray, single sided'),
    ]
    colours = [
        row('<span class="sw" style="background:#102232"></span>كحلي', 'Navy', 'HEX #102232 · CMYK تقريبًا 100/78/45/55 · RAL 5011 أو 5004 (يُطابَق مع عيّنة)', 'HEX #102232 · CMYK ≈ 100/78/45/55 · RAL 5011 or 5004 (match to sample)'),
        row('<span class="sw" style="background:#D4A95F"></span>ذهبي', 'Gold', 'HEX #D4A95F · CMYK تقريبًا 12/32/72/2 · Pantone 7562 C أو 871 C معدني', 'HEX #D4A95F · CMYK ≈ 12/32/72/2 · Pantone 7562 C or 871 C metallic'),
    ]
    legr = [row('مسافة المشاهدة المقصودة', 'Intended viewing distance', '20–30 م (من الشارع والسيارة)', '20–30 m (from the street / a car)'),
            row('الاسم العربي', 'Arabic name', f'حتى نحو {leg(na["alef_h"])} م', f'up to ≈ {leg(na["alef_h"])} m'),
            row('الاسم الإنجليزي', 'English name', f'حتى نحو {leg(ne["cap"])} م', f'up to ≈ {leg(ne["cap"])} m')]
    if tg:
        legr.append(row('الشعار النصي', 'Tagline', f'حتى نحو {leg(tg["alef_h"])} م', f'up to ≈ {leg(tg["alef_h"])} m'))
    site = [row('1', '1', 'ارتفاع وجه حافة السقف (من خط التشقق إلى الحافة السفلية)', 'Height of the slab-edge face (crack line to underside edge)'),
            row('2', '2', 'ارتفاع الجدار المتاح فوق خط التشقق', 'Usable wall height above the crack line'),
            row('3', '3', 'العرض الصافي بين رقبتي العمودين', 'Clear width between the two column stubs')]
    tbl = lambda title_ar, title_en, rows: (f'<table><tr><th colspan="2"><div>{title_ar}</div><div class="en">{title_en}</div></th></tr>{"".join(rows)}</table>')
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Plex Arabic";src:url("file://{FONTS}/ibmplexsansarabic/IBMPlexSansArabic-Regular.ttf");font-weight:400}}
@font-face{{font-family:"Plex Arabic";src:url("file://{FONTS}/ibmplexsansarabic/IBMPlexSansArabic-SemiBold.ttf");font-weight:600}}
@page{{size:420mm 297mm;margin:0}}
body{{margin:0;font-family:"Plex Arabic";color:#222;font-size:7pt;line-height:1.55}}
.page{{width:420mm;height:297mm;box-sizing:border-box;padding:9mm 12mm;position:relative}}
.en{{direction:ltr;text-align:left;color:#444}}
.head{{display:flex;gap:10mm;align-items:flex-start}} .head>div{{flex:1}}
h1{{font-size:13pt;margin:0;font-weight:600;line-height:1.5}} .sub{{font-size:8pt}}
.draw{{margin:3mm 0 0 13mm;direction:ltr}}
.cap{{text-align:center;font-size:8pt;margin-top:-4mm}} .cap .en{{text-align:center}}
.cols{{display:flex;gap:5mm;margin-top:3mm}} .cols>div{{flex:1;display:flex;flex-direction:column;gap:3mm}}
table{{border-collapse:collapse;width:100%}} td,th{{border:0.3pt solid #999;padding:0.6mm 1.5mm;text-align:right;vertical-align:top}}
th{{background:#eee;font-weight:600}} td.k{{width:24%;font-weight:600}}
.sw{{display:inline-block;width:6mm;height:3mm;vertical-align:middle;border:0.3pt solid #999;margin-left:1.5mm}}
.warn{{border:0.8pt solid #c0392b;color:#c0392b;padding:1.5mm 2.5mm;font-weight:600}} .warn .en{{color:#c0392b}}
.note{{font-size:6.8pt;color:#555}}
</style></head><body><div class="page">
<div class="head">
<div><h1>لوحة محل — الخيار {L} — رسم فني — الإصدار 02</h1>
<div class="sub">أحمد إعمار القابضة · 2026-11-23 · لوحة 250 × 60 سم، وجه واحد، تُثبَّت على واجهة حافة السقف فوق الباب الدرج. تغطي اللوحة حافة السقف (نحو 30–40 سم) ونحو 20–30 سم من الجدار فوقها، وتعبر خط التشقق.</div></div>
<div class="en"><h1>Shop sign — option {opt.upper()} — technical drawing — v02</h1>
<div class="sub">Ahmed Emaar Holding · 2026-11-23 · 250 × 60 cm single-sided panel fixed to the front of the slab above the rolling shutter. It covers the slab edge (≈ 30–40 cm) plus ≈ 20–30 cm of wall above it, and crosses the crack line.</div></div>
</div>
<div class="draw">{drawing}</div>
<div class="cap"><div>الأبعاد بالسنتيمتر بالمقاس الحقيقي — المقياس 1:10 على ورق A3 — الرسم: ملف قصّ، ألوان RGB، غير جاهز للطباعة</div>
<div class="en">Dimensions in cm, real size — scale 1:10 on A3 — artwork shown is cut-file artwork, RGB, not print-ready</div></div>
<div class="cols">
<div>{tbl('المقاسات (المقاس الحقيقي)', 'Sizes (real)', sizes)}</div>
<div>{tbl('التنفيذ — اقتراحات للتأكيد مع المصنّع', 'Fabrication — suggestions to confirm with the sign maker', fab)}{tbl('الألوان والتشطيب — اقتراحات', 'Colours & finishes — suggestions', colours)}{tbl('سماكة الخطوط (المقاس الحقيقي)', 'Stroke widths (real size)', strokes)}</div>
<div>{tbl('مسافة القراءة — قاعدة تقريبية: نحو 3 م لكل 1 سم من ارتفاع الحرف', 'Reading distance — rule of thumb: ≈ 3 m per 1 cm of letter height', legr)}
{tbl('قياسات مطلوبة من الموقع', 'Site measurements requested', site)}
<div class="warn"><div>يُشترط فحص وترميم حافة السقف قبل التركيب (تشققات وحديد مكشوف)</div><div class="en">Slab edge to be inspected and repaired before installation (cracks and exposed rebar).</div></div>
<div class="note"><div>* الارتفاع 60 سم افتراض: وجه حافة السقف يُقدَّر بنحو 30–40 سم من الصورة (زاوية تصوير مائلة لأعلى)، والتقدير يعتمد على عرض مفترض للباب الدرج 2.5–3.0 م. التصميم يُعاد تحجيمه بعد القياس. الشعار إعادة رسم مؤقتة بانتظار الملف الأصلي، والحروف مطابقة بخطوط Cairo وInter. ألوان CMYK وRAL وPantone تقريبية.</div>
<div class="en">* The 60 cm height is an assumption: the slab-edge face is estimated at ≈ 30–40 cm from the photo (steep upward camera angle), based on an assumed shutter width of 2.5–3.0 m. The layout re-scales once measured. Logo is a PROVISIONAL trace pending the original file; lettering is a typeface match (Cairo / Inter). CMYK, RAL and Pantone values are approximate.</div></div>
</div></div></div></body></html>'''
    open(f'v02_drawing-{opt}.html', 'w').write(html)


for o in 'ab':
    build(o)
