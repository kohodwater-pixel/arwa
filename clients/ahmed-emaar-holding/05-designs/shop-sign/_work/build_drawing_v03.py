"""v03 technical drawing - individual raised letters on the wall. A3 landscape,
artwork at exactly 1:10. Arabic block and English block kept separate.
Numeric ranges inside Arabic text are isolated LTR (<span dir=ltr>) so they
do not reverse."""
import json, re
M = json.load(open('metrics_v03.json'))
LW, LH = M['overall_w'], M['overall_h']
p = M['pos']; mk, na, ne = M['mark'], M['name_ar'], M['name_en']
FONTS = '/home/user/arwa/assets/fonts'
LPM = 3.0
R = lambda s: f'<span dir="ltr" class="n">{s}</span>'   # isolated LTR number/range


def dim_h(x1, x2, y, label, tick=2.5):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" class="d"/><line x1="{x1}" y1="{y-tick}" x2="{x1}" y2="{y+tick}" class="d"/>'
            f'<line x1="{x2}" y1="{y-tick}" x2="{x2}" y2="{y+tick}" class="d"/><text x="{(x1+x2)/2}" y="{y-1.6}" class="t" text-anchor="middle">{label}</text>')


def dim_v(x, y1, y2, label, side='right', tick=2.5):
    tx, anc = (x + 2, 'start') if side == 'right' else (x - 2, 'end')
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="d"/><line x1="{x-tick}" y1="{y1}" x2="{x+tick}" y2="{y1}" class="d"/>'
            f'<line x1="{x-tick}" y1="{y2}" x2="{x+tick}" y2="{y2}" class="d"/><text x="{tx}" y="{(y1+y2)/2+1.2}" class="t" text-anchor="{anc}">{label}</text>')


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="e"/>'


art = open('v03_letters_full.svg').read()
art = re.sub(r'<svg[^>]*?>', f'<svg xmlns="http://www.w3.org/2000/svg" x="0" y="0" width="{LW}" height="{LH}" viewBox="0 0 {LW} {LH}">', art, count=1)
art = re.sub(r'<title>.*?</title>', '', art)
ar_body_top = p['ar_base'] - M['arabic_body_h']
g = [f'<rect x="0" y="0" width="{LW}" height="{LH}" fill="none" stroke="#999" stroke-width=".15" stroke-dasharray="1 1"/>',
     dim_h(0, LW, -10, f'[1] {LW:.0f}'), ext(0, -12, 0, 0), ext(LW, -12, LW, 0),
     dim_v(LW + 22, 0, LH, f'[2] {LH}'), ext(LW, 0, LW + 24, 0), ext(LW, LH, LW + 24, LH),
     dim_v(LW + 6, p['top'], p['bottom'], f'[3] {mk["h"]}'),
     dim_v(-24, p['ar_base'] - na['alef_h'], p['ar_base'], f'[4] {na["alef_h"]}', 'left'),
     dim_v(-10, ar_body_top, p['ar_base'], f'[5] {M["arabic_body_h"]}', 'left'),
     ext(-24, p['ar_base'], p['left'] + 3, p['ar_base']), ext(-10, ar_body_top, p['left'] + 3, ar_body_top),
     dim_v(-10, p['lat_top'], p['lat_base'], f'[6] {ne["cap"]}', 'left'),
     ext(-10, p['lat_top'], p['left'], p['lat_top']),
     dim_v(-34, p['ar_base'], p['lat_top'], f'[7] {M["gap_ar_base_to_en_top"]}', 'left'),
     ext(-34, p['lat_top'], -10, p['lat_top']),
     dim_h(p['mark_left'] - (p['mark_left'] - (p['left'] + na['width'])), p['mark_left'], LH + 7, f'[8] {p["mark_left"] - (p["left"] + na["width"]):.1f}'),
     ext(p['mark_left'], p['bottom'], p['mark_left'], LH + 9), ext(p['left'] + na['width'], p['lat_base'], p['left'] + na['width'], LH + 9)]
for i, sp in enumerate(M['small_pieces']):
    r = max(sp['w'], sp['h']) / 2 + 1.4
    g.append(f'<circle cx="{sp["x"]}" cy="{sp["y"]}" r="{r:.2f}" fill="none" stroke="#1a6fb3" stroke-width=".3"/>')
    g.append(f'<text x="{sp["x"]}" y="{sp["y"] - r - 0.8:.2f}" class="t b" text-anchor="middle">P{i+1}</text>')
drawing = (f'<svg xmlns="http://www.w3.org/2000/svg" width="345mm" height="78mm" viewBox="-55 -20 345 78" style="direction:ltr">'
           f'<style>.d{{stroke:#c0392b;stroke-width:.25;fill:none}}.e{{stroke:#c0392b;stroke-width:.15;stroke-dasharray:1 .8}}'
           f'.t{{font-family:"Plex Arabic";font-size:3.1px;fill:#222}}.b{{fill:#1a6fb3;font-weight:600}}</style>{art}{"".join(g)}</svg>')

# placement elevation (schematic, 1:50, wall frame from the photo estimate)
S = 0.2  # mm per cm (1:50)
def el(y):  # height above slab lower edge (cm) -> svg y (mm), top = 150 cm
    return (150 - y) * S
bot, top = 60.0, 60.0 + LH
elev = f'''<svg xmlns="http://www.w3.org/2000/svg" width="110mm" height="46mm" viewBox="-14 -2 86 36" style="direction:ltr">
<style>.t{{font-family:"Plex Arabic";font-size:2.1px;fill:#222}}.d{{stroke:#c0392b;stroke-width:.18}}</style>
<rect x="-6" y="{el(135)}" width="{310*S}" height="{(135-0)*S}" fill="#f2ece2" stroke="#999" stroke-width=".15"/>
<rect x="-6" y="{el(30)}" width="{310*S}" height="{30*S}" fill="#e6dccb"/>
<rect x="{-30*S}" y="{el(40)}" width="{12*S}" height="{40*S}" fill="#d8cfc0"/><rect x="{268*S}" y="{el(40)}" width="{12*S}" height="{40*S}" fill="#d8cfc0"/>
<line x1="{-27*S}" y1="{el(40)}" x2="{-27*S}" y2="{el(105)}" stroke="#555" stroke-width=".25"/><line x1="{-22*S}" y1="{el(40)}" x2="{-22*S}" y2="{el(95)}" stroke="#555" stroke-width=".25"/>
<line x1="{272*S}" y1="{el(40)}" x2="{272*S}" y2="{el(105)}" stroke="#555" stroke-width=".25"/><line x1="{277*S}" y1="{el(40)}" x2="{277*S}" y2="{el(95)}" stroke="#555" stroke-width=".25"/>
<polyline points="{-6},{el(27)} {10},{el(25)} {22},{el(29)} {35},{el(24)} {50},{el(29)} {62},{el(28)}" fill="none" stroke="#c0392b" stroke-width=".35"/>
<rect x="0" y="{el(top)}" width="{LW*S}" height="{LH*S}" fill="#D4A95F" opacity=".85"/>
<line x1="-6" y1="{el(0)}" x2="{304*S}" y2="{el(0)}" stroke="#333" stroke-width=".3"/>
<text x="-7" y="{el(0)+0.7}" class="t" text-anchor="end">0</text>
<text x="-7" y="{el(28)+0.7}" class="t" text-anchor="end">≈25</text>
<text x="-7" y="{el(bot)+0.7}" class="t" text-anchor="end">≈{bot:.0f}</text>
<text x="-7" y="{el(top)+0.7}" class="t" text-anchor="end">≈{top:.0f}</text>
<text x="-7" y="{el(135)+0.7}" class="t" text-anchor="end">≈135</text>
</svg>'''

leg = lambda h: f'{h * LPM:.0f}'
def row(ka, ke, va, ve):
    return f'<tr><td class="k"><div>{ka}</div><div class="en">{ke}</div></td><td><div>{va}</div><div class="en">{ve}</div></td></tr>'
def tbl(ta, te, rows):
    return f'<table><tr><th colspan="2"><div>{ta}</div><div class="en">{te}</div></th></tr>{"".join(rows)}</table>'

sizes = [
    row('[1] العرض الكلي للكتابة', '[1] Overall lettering width', f'{R(f"{LW:.0f}")} سم (يشمل الشعار)', f'{LW:.0f} cm (mark included)'),
    row('[2] الارتفاع الكلي', '[2] Overall height', f'{R(LH)} سم', f'{LH} cm'),
    row('[3] الشعار', '[3] Mark', f'{R(mk["h"])} × {R(mk["w"])} سم', f'{mk["h"]} × {mk["w"]} cm'),
    row('[4] [5] الاسم العربي', '[4] [5] Arabic name', f'ارتفاع الألف {R(na["alef_h"])} سم؛ ارتفاع جسم الحروف {R(M["arabic_body_h"])} سم؛ الامتداد الكلي {R(na["full_extent"])} سم؛ العرض {R(na["width"])} سم',
        f'alef {na["alef_h"]} cm; letter-body height {M["arabic_body_h"]} cm; full extent {na["full_extent"]} cm; width {na["width"]} cm'),
    row('[6] الاسم الإنجليزي', '[6] English name', f'ارتفاع الحرف الكبير {R(ne["cap"])} سم؛ العرض {R(ne["width"])} سم؛ خط Inter ExtraBold', f'cap height {ne["cap"]} cm; width {ne["width"]} cm; Inter ExtraBold (800), tracking {ne["tracking_em"]} em'),
    row('[7] [8] المسافات', '[7] [8] Spacing', f'من خط قاعدة العربي إلى أعلى الإنجليزي {R(M["gap_ar_base_to_en_top"])} سم (وأدنى نقطة في الهمزة {R(M["gap_ar_bottom_to_en_top"])} سم)؛ بين الشعار والكتابة {R(round(p["mark_left"] - (p["left"] + na["width"]), 1))} سم',
        f'Arabic baseline to English cap top {M["gap_ar_base_to_en_top"]} cm (lowest hamza {M["gap_ar_bottom_to_en_top"]} cm); mark to lettering {p["mark_left"] - (p["left"] + na["width"]):.1f} cm'),
]
pieces_ar = '، '.join(f'P{i+1}' for i in range(len(M['small_pieces'])))
strokes = [
    row('الشعار', 'Mark', f'الأعمدة {R("4.2–4.7")} سم؛ أنحف جزء في القوس {R(mk["stroke_min"])} سم؛ طرف الذيل مقطوع عند نحو {R("1.5")} سم', f'bars 4.2–4.7 cm; thinnest arch {mk["stroke_min"]} cm; swoosh tip blunted at ≈ 1.5 cm'),
    row('الاسم العربي', 'Arabic name', f'الجذع {R(na["stem"])} سم؛ الخط الأفقي {R(na["horiz_stroke"])} سم؛ النقاط {R("3.1 × 2.7")} سم؛ الهمزات {R("5.8 × 5.2")} سم', f'stem {na["stem"]} cm; horizontal {na["horiz_stroke"]} cm; dots 3.1 × 2.7 cm; hamzas 5.8 × 5.2 cm'),
    row('الاسم الإنجليزي', 'English name', f'الجذع {R(ne["stem"])} سم؛ الخط الأفقي نحو {R(ne["bar"])} سم', f'stem {ne["stem"]} cm; horizontal bar ≈ {ne["bar"]} cm'),
    row('الحدّ الأدنى', 'Minimum', f'كل الخطوط ≥ {R("1.5")} سم', 'every stroke ≥ 1.5 cm'),
]
fab = [
    row('القطع', 'Pieces', f'الشعار {M["n_pieces_mark"]} قطع؛ العربي {M["n_pieces_ar"]} قطعة منها {len(M["small_pieces"])} قطع صغيرة ({pieces_ar}: همزتان و6 نقاط) تُثبّت كل منها بمسمار مستقل؛ الإنجليزي {M["n_pieces_en"]} حرفًا',
        f'mark {M["n_pieces_mark"]} pieces; Arabic {M["n_pieces_ar"]} pieces incl. {len(M["small_pieces"])} small parts (P1–P{len(M["small_pieces"])}: 2 hamzas, 6 dots), each pinned separately; English {M["n_pieces_en"]} letters'),
    row('العمق المقترح', 'Suggested depth', f'الشعار والعربي {R("5")} سم؛ الإنجليزي {R("3")} سم؛ مع فراغ عن الجدار {R("15–20")} مم', 'mark and Arabic 5 cm; English 3 cm; stand-off from the wall 15–20 mm'),
    row('المادة', 'Material', 'حروف ألمنيوم مشكّلة أو أكريليك سميك؛ لون الوجه والجوانب حسب الصيغة المختارة', 'fabricated aluminium or thick acrylic letters; face and return colours per the chosen variant'),
    row('التثبيت', 'Fixing', 'مسامير ملولبة (ستاد) مع مثبّت كيميائي في خرسانة سليمة فقط، وقالب ثقب بمقاس 1:1 من المصنّع', 'threaded stand-off studs with chemical anchors into sound concrete only, using a 1:1 drilling template from the fabricator'),
    row('ارتفاع التركيب', 'Mounting height', f'أسفل الحروف نحو {R(f"{bot:.0f}")} سم فوق الحافة السفلية لبلاطة السقف (نحو {R("30")} سم فوق خط التشقق)، وأعلاها نحو {R(f"{top:.0f}")} سم — تقدير من الصورة',
        f'letter bottoms ≈ {bot:.0f} cm above the slab\'s lower front edge (≈ 30 cm above the crack line), tops ≈ {top:.0f} cm — estimate from the photo'),
]
contrast = [
    row(f'ذهبي {R("#D4A95F")}', 'Gold #D4A95F', f'{R("1.9")} على الجدار المشمس؛ {R("1.0")} على الزخرفة الوردية — ضعيف', '1.9 on sunlit wall; 1.0 on the rose motif — weak'),
    row(f'كحلي {R("#102232")}', 'Navy #102232', f'{R("14.2")} على الجدار المشمس؛ {R("7.2")} على الزخرفة — ممتاز', '14.2 on sunlit wall; 7.2 on the motif — excellent'),
    row(f'برونزي داكن {R("#4A3A28")}', 'Dark bronze #4A3A28', f'{R("9.6")} و{R("4.8")} — جيد', '9.6 and 4.8 — good'),
    row('ذهبي بحافة كحلية', 'Gold with navy edge', f'الحافة على الجدار {R("14.2")}؛ الذهبي على الكحلي {R("7.4")}', 'edge on wall 14.2; gold on navy 7.4'),
]
legr = [row('مسافة المشاهدة المقصودة', 'Intended viewing distance', f'{R("20–30")} م', '20–30 m'),
        row('الاسم العربي (على ارتفاع جسم الحروف)', 'Arabic name (on letter-body height)', f'حتى نحو {R(leg(M["arabic_body_h"]))} م', f'up to ≈ {leg(M["arabic_body_h"])} m'),
        row('الاسم الإنجليزي', 'English name', f'حتى نحو {R(leg(ne["cap"]))} م', f'up to ≈ {leg(ne["cap"])} m')]
site = [row('1', '1', 'ارتفاع وجه حافة السقف (من خط التشقق إلى الحافة السفلية)', 'Height of the slab-edge face (crack line to lower edge)'),
        row('2', '2', 'ارتفاع الجدار فوق خط التشقق حتى أعلى الجدار', 'Wall height from the crack line to the top of the wall'),
        row('3', '3', 'العرض الصافي بين رقبتي العمودين وحديد التسليح البارز', 'Clear width between the column stubs and their exposed rebar')]

html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Plex Arabic";src:url("file://{FONTS}/ibmplexsansarabic/IBMPlexSansArabic-Regular.ttf");font-weight:400}}
@font-face{{font-family:"Plex Arabic";src:url("file://{FONTS}/ibmplexsansarabic/IBMPlexSansArabic-SemiBold.ttf");font-weight:600}}
@page{{size:420mm 297mm;margin:0}}
body{{margin:0;font-family:"Plex Arabic";color:#222;font-size:6.9pt;line-height:1.5}}
.page{{width:420mm;height:297mm;box-sizing:border-box;padding:8mm 11mm;position:relative}}
.en{{direction:ltr;text-align:left;color:#444}} .n{{unicode-bidi:isolate}}
.head{{display:flex;gap:10mm}} .head>div{{flex:1}} h1{{font-size:12.5pt;margin:0;font-weight:600;line-height:1.45}} .sub{{font-size:7.8pt}}
.top{{display:flex;direction:ltr;align-items:flex-start;gap:4mm;margin-top:2mm}}
.cap{{text-align:center;font-size:7.6pt}} .cap .en{{text-align:center}}
.elev{{direction:rtl;font-size:6.6pt;border:0.3pt solid #999;padding:1.5mm}} .elev svg{{display:block;margin:0 auto}} .elev .en{{font-size:6.4pt}}
.cols{{display:flex;gap:4mm;margin-top:2mm}} .cols>div{{flex:1;display:flex;flex-direction:column;gap:2.5mm}}
table{{border-collapse:collapse;width:100%}} td,th{{border:0.3pt solid #999;padding:0.5mm 1.4mm;text-align:right;vertical-align:top}}
th{{background:#eee;font-weight:600}} td.k{{width:25%;font-weight:600}}
.warn{{border:1pt solid #c0392b;color:#c0392b;padding:1.5mm 2.5mm;font-weight:600;font-size:7.6pt}} .warn .en{{color:#c0392b}}
.note{{font-size:6.5pt;color:#555}}
</style></head><body><div class="page">
<div class="head">
<div><h1>لافتة بحروف بارزة على الجدار — رسم فني — الإصدار 03</h1>
<div class="sub">أحمد إعمار القابضة · {R("2026-11-23")} · بدون لوحة خلفية: الشعار والاسمان حروف بارزة مستقلة تُثبَّت على الجدار مباشرة فوق خط التشقق، بعرض كلي {R("250")} سم.</div></div>
<div class="en"><h1>Raised letters on the wall — technical drawing — v03</h1>
<div class="sub">Ahmed Emaar Holding · 2026-11-23 · No panel: the mark and both names are individual raised letters fixed directly to the wall above the crack line, 250 cm overall width.</div></div></div>
<div class="top"><div>{drawing}
<div class="cap"><div>الأبعاد بالسنتيمتر بالمقاس الحقيقي — المقياس {R("1:10")} على ورق {R("A3")} — ملف قصّ، ألوان {R("RGB")}، غير جاهز للطباعة — {R("P1–P8")} قطع صغيرة تُثبّت منفصلة</div>
<div class="en">Dimensions in cm, real size — scale 1:10 on A3 — cut-file artwork, RGB, not print-ready — P1–P8 small separately pinned parts</div></div></div>
</div>
<div class="cols">
<div>{tbl('المقاسات (المقاس الحقيقي)', 'Sizes (real)', sizes)}{tbl('سماكة الخطوط (المقاس الحقيقي)', 'Stroke widths (real size)', strokes)}</div>
<div>{tbl('التنفيذ والتثبيت — اقتراحات للتأكيد مع المصنّع', 'Fabrication and fixing — suggestions to confirm with the sign maker', fab)}<div class="elev">{elev}<div>مخطط الموقع (تقريبي، {R("1:50")}): الارتفاعات بالسنتيمتر فوق الحافة السفلية للبلاطة. الكتابة كلها على الجدار فوق خط التشقق (الأحمر) وبعيدًا عن الشريط المتضرر وحديد التسليح البارز بنحو {R("20")} سم من كل جانب.</div>
<div class="en">Site elevation (approximate, 1:50): heights in cm above the slab's lower front edge. The whole lockup sits on the wall above the crack line (red), clear of the damaged strip and ≈ 20 cm from the exposed rebar on each side.</div></div></div>
<div>{tbl('التباين مع الجدار (مقاس من صورة الموقع)', 'Contrast against the wall (measured on the site photo)', contrast)}
{tbl('مسافة القراءة — قاعدة تقريبية: نحو 3 م لكل 1 سم', 'Reading distance — rule of thumb: ≈ 3 m per 1 cm', legr)}
{tbl('قياسات مطلوبة من الموقع', 'Site measurements requested', site)}</div></div>
<div class="warn" style="margin-top:2.5mm"><div>تحذير: مسامير التثبيت تدخل في حافة السقف والجدار المتشققين. يُشترط أن يفحص مقاول إنشائي حافة السقف والجدار ويرمّمهما (تشققات وحديد مكشوف وتساقط في الخرسانة) قبل أي ثقب أو تركيب، وألا تُثبّت أي قطعة في خرسانة متضررة.</div>
<div class="en">Warning: the fixings go into the cracked slab edge and wall. A structural contractor must inspect and repair the slab edge and wall (cracks, exposed rebar, spalling) before any drilling or installation; no piece is to be fixed into damaged concrete.</div></div>
<div class="note" style="margin-top:1.5mm"><div>المقاسات والمواضع تقديرية من صورة واحدة (وجه حافة السقف نحو {R("30–40")} سم بافتراض عرض للباب الدرج {R("2.5–3.0")} م). الشعار إعادة رسم مؤقتة بانتظار الملف الأصلي؛ طرف الذيل مقطوع لأغراض التصنيع. الحروف مطابقة بخطوط Cairo وInter (الإنجليزي بوزن أثقل لأغراض التصنيع). التباين محسوب بين ألوان العيّنة وبكسلات الصورة، وهو مؤشر لا قياس مخبري.</div>
<div class="en">Sizes and positions are estimates from one photo (slab-edge face ≈ 30–40 cm, assuming a 2.5–3.0 m shutter). Logo is a PROVISIONAL trace pending the original file; swoosh tip blunted for fabrication. Lettering is a typeface match (Cairo / Inter; English set heavier for fabrication). Contrast is computed between swatch colours and photo pixels — an indicator, not a lab measurement.</div></div>
</div></body></html>'''
open('v03_drawing.html', 'w').write(html)
