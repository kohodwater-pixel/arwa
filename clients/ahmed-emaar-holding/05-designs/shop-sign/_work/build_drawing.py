"""Technical drawing (A3 landscape, artwork at exactly 1:10) for each option.
HTML -> PDF with scripts/html2pdf.cjs. Labels are live text (Arabic + English)."""
import json, re, sys
M = json.load(open('metrics.json'))
W, H = M['W_cm'], M['H_cm']
FONTS = '/home/user/arwa/assets/fonts'


def dim_h(x1, x2, y, label, tick=2.5):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" class="d"/>'
            f'<line x1="{x1}" y1="{y-tick}" x2="{x1}" y2="{y+tick}" class="d"/><line x1="{x2}" y1="{y-tick}" x2="{x2}" y2="{y+tick}" class="d"/>'
            f'<text x="{(x1+x2)/2}" y="{y-1.6}" class="t" text-anchor="middle">{label}</text>')


def dim_v(x, y1, y2, label, side='right', tick=2.5):
    tx = x + 2 if side == 'right' else x - 2
    anc = 'start' if side == 'right' else 'end'
    return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="d"/>'
            f'<line x1="{x-tick}" y1="{y1}" x2="{x+tick}" y2="{y1}" class="d"/><line x1="{x-tick}" y1="{y2}" x2="{x+tick}" y2="{y2}" class="d"/>'
            f'<text x="{tx}" y="{(y1+y2)/2+1.2}" class="t" text-anchor="{anc}">{label}</text>')


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="e"/>'


def build(opt):
    info = M[opt]; p = info['_pos']
    art = open(f'option-{opt}_full.svg').read()
    art = re.sub(r'<svg[^>]*?>', '<svg xmlns="http://www.w3.org/2000/svg" x="0" y="0" width="250" height="60" viewBox="0 0 250 60">', art, count=1)
    art = re.sub(r'<title>.*?</title>', '', art)
    f = lambda v: f'{v:.1f}'
    g = []
    # overall
    g.append(dim_h(0, W, -12, f'{W:.0f} سم (cm) — العرض الكلي (overall width)'))
    g += [ext(0, -14, 0, 0), ext(W, -14, W, 0)]
    g.append(dim_v(W + 26, 0, H, f'{H:.0f} *'))
    g += [ext(W, 0, W + 28, 0), ext(W, H, W + 28, H)]
    # margins
    g.append(dim_h(p['x_right'], W, H + 9, f'{W - p["x_right"]:.1f}'))
    g.append(dim_h(0, p['left'], H + 9, f'{p["left"]:.1f}'))
    g += [ext(p['x_right'], p['bottom'], p['x_right'], H + 11), ext(p['left'], p['lat_base'], p['left'], H + 11)]
    g.append(dim_v(-8, 0, p['top'], f'{p["top"]:.1f}', 'left'))
    # mark height
    g.append(dim_v(W + 4, p['top'], p['bottom'], f'{info["mark_height_cm"]} (mark)'))
    # Arabic alef height and Latin cap height (left side)
    g.append(dim_v(-20, p['ar_base'] - info['arabic_alef_height_cm'], p['ar_base'], f'(alef) {info["arabic_alef_height_cm"]}', 'left'))
    g.append(ext(-20, p['ar_base'], p['left'], p['ar_base']))
    g.append(dim_v(-8, p['lat_top'], p['lat_base'], f'(cap) {info["latin_cap_height_cm"]}', 'left'))
    g.append(ext(-8, p['lat_top'], p['left'], p['lat_top']))
    if opt == 'b':
        t = info['_tag']
        g.append(dim_v(-8, t['base'] - info['tagline_alef_height_cm'], t['base'], f'(tagline) {info["tagline_alef_height_cm"]}', 'left'))
        g.append(dim_v(-30, H - 7, H, '7.0', 'left'))
    else:
        g.append(dim_v(-8, p['bottom'], H, f'{H - p["bottom"]:.1f}', 'left'))
    g.append(f'<text x="{W/2}" y="{H + 20}" class="t" text-anchor="middle">الأبعاد بالسنتيمتر بالمقاس الحقيقي (dimensions in cm, real size) — المقياس 1:10 على ورق A3 (scale 1:10 on A3)</text>')
    drawing = (f'<svg xmlns="http://www.w3.org/2000/svg" width="360mm" height="110mm" viewBox="-60 -22 360 110" direction="ltr" style="direction:ltr">'
               f'<style>.d{{stroke:#c0392b;stroke-width:.25;fill:none}}.e{{stroke:#c0392b;stroke-width:.15;stroke-dasharray:1 .8}}'
               f'.t{{font-family:"Plex Arabic";font-size:3.1px;fill:#222}}</style>{art}{"".join(g)}</svg>')
    lbl = 'أ' if opt == 'a' else 'ب'
    tag_row = (f'<tr><td>الشعار النصي (tagline): «حلول متكاملة للبنية التحتية والخدمات»</td><td>ارتفاع الألف {info["tagline_alef_height_cm"]} سم (alef height), العرض {info["tagline_width_cm"]} سم</td></tr>' if opt == 'b' else '')
    html = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><style>
@font-face{{font-family:"Plex Arabic";src:url("file://{FONTS}/ibmplexsansarabic/IBMPlexSansArabic-Regular.ttf");font-weight:400}}
@font-face{{font-family:"Plex Arabic";src:url("file://{FONTS}/ibmplexsansarabic/IBMPlexSansArabic-SemiBold.ttf");font-weight:600}}
@page{{size:420mm 297mm;margin:0}}
body{{margin:0;font-family:"Plex Arabic";color:#222;font-size:9pt;line-height:1.6}}
.page{{width:420mm;height:297mm;box-sizing:border-box;padding:12mm 14mm;position:relative}}
h1{{font-size:16pt;margin:0 0 1mm;font-weight:600}} .en{{direction:ltr;unicode-bidi:isolate}}
.sub{{color:#555;font-size:9.5pt}}
.draw{{position:absolute;top:34mm;left:25mm;direction:ltr}}
.cols{{position:absolute;top:148mm;right:14mm;left:14mm;display:flex;gap:8mm}}
.cols>div{{flex:1}}
table{{border-collapse:collapse;width:100%;font-size:8.3pt}} td,th{{border:0.3pt solid #999;padding:1.2mm 2mm;text-align:right;vertical-align:top}} th{{background:#eee;font-weight:600}}
.sw{{display:inline-block;width:9mm;height:4mm;vertical-align:middle;border:0.3pt solid #999;margin-left:2mm}}
.warn{{border:0.8pt solid #c0392b;color:#c0392b;padding:2mm 3mm;font-weight:600;margin-top:3mm}}
.foot{{position:absolute;bottom:8mm;right:14mm;left:14mm;font-size:7.5pt;color:#666;border-top:0.3pt solid #999;padding-top:1.5mm}}
</style></head><body><div class="page">
<h1>لوحة محل — الخيار {lbl} — رسم فني <span class="en">(Shop sign — option {opt.upper()} — technical drawing)</span></h1>
<div class="sub">أحمد إعمار القابضة <span class="en">(Ahmed Emaar Holding)</span> · الإصدار 01 <span class="en">(v01)</span> · 2026-11-23 · لوحة واجهة على حافة السقف فوق الباب الدرج <span class="en">(fascia on the slab edge above the rolling shutter)</span> · وجه واحد <span class="en">(single sided)</span></div>
<div class="draw">{drawing}</div>
<div class="cols">
<div><table>
<tr><th colspan="2">المقاسات (sizes, real)</th></tr>
<tr><td>اللوحة (panel)</td><td>{W:.0f} × {H:.0f} سم (cm) — الارتفاع تقديري *</td></tr>
<tr><td>الشعار (mark)</td><td>{info["mark_height_cm"]} × {info["mark_width_cm"]} سم</td></tr>
<tr><td>الاسم العربي (Arabic name)</td><td>ارتفاع الألف {info["arabic_alef_height_cm"]} سم (alef height) · الامتداد الكلي مع الهمزات {info["arabic_full_extent_cm"]} سم (full extent) · العرض {info["arabic_width_cm"]} سم</td></tr>
<tr><td>الاسم الإنجليزي (English name)</td><td>ارتفاع الحرف الكبير {info["latin_cap_height_cm"]} سم (cap height) · العرض {info["latin_width_cm"]} سم</td></tr>
{tag_row}
<tr><td>الهوامش الآمنة (safe margins)</td><td>أعلى {info["margins_cm"]["top"]} · أسفل {info["margins_cm"]["bottom"]} · يمين {info["margins_cm"]["right"]} · يسار {info["margins_cm"]["left"]} سم — الخطوط الذهبية الزخرفية فقط تصل إلى الحافة (decorative gold lines only run to the edge)</td></tr>
<tr><td>الخطوط الذهبية (gold lines)</td><td>عرض 1.2 سم (1.2 cm wide), بزاوية 41° مثل قطع الشعار</td></tr>
</table></div>
<div><table>
<tr><th colspan="2">الألوان والتشطيب — اقتراحات للتأكيد مع المصنّع (colours &amp; finishes — suggestions, confirm with sign maker)</th></tr>
<tr><td><span class="sw" style="background:#102232"></span>كحلي (navy)</td><td><span class="en">HEX #102232 · CMYK ≈ 100 / 78 / 45 / 55 · suggested RAL 5011 (Steel blue) or RAL 5004 — match to sample</span><br>لوح ألمنيوم مركّب ACP أو ألمنيوم مدهون فرن <span class="en">(navy ACP or powder-coated aluminium tray)</span></td></tr>
<tr><td><span class="sw" style="background:#D4A95F"></span>ذهبي (gold)</td><td><span class="en">HEX #D4A95F · CMYK ≈ 12 / 32 / 72 / 2 · ref. Pantone 7562 C (flat) / 871 C (metallic)</span><br>حروف بارزة ثلاثية الأبعاد 3–5 سم: أكريليك ذهبي مرآة أو ستانلس ستيل ذهبي مصقول/مخدوش <span class="en">(3–5 cm raised letters: gold mirror acrylic or brushed gold-finish stainless / ACP)</span></td></tr>
<tr><td>الإضاءة (lighting)</td><td>اختياري: إضاءة LED خلفية (هالة) أو أمامية للحروف — غير محددة من العميل <span class="en">(optional halo- or face-lit LED; not specified by the client)</span></td></tr>
</table>
<div class="warn">يُشترط فحص وترميم حافة السقف قبل التركيب (تشققات وحديد مكشوف)<br><span class="en">Slab edge to be inspected and repaired before installation (cracks and exposed rebar).</span></div>
</div>
</div>
<div class="foot">* الارتفاع 60 سم تقديري من صورة الموقع ويجب قياسه في الموقع؛ التصميم قابل لإعادة التحجيم <span class="en">(60 cm height is an estimate from the site photo — measure on site; layout re-scales).</span>
 الشعار إعادة رسم مؤقتة من لوحة الهوية بانتظار الملف الأصلي من العميل <span class="en">(logo is a PROVISIONAL trace pending the client's original file)</span>. كل النصوص في ملف التصنيع محوّلة إلى مسارات <span class="en">(all lettering in the artwork files is outlined)</span>. ألوان CMYK و RAL و Pantone تقريبية <span class="en">(CMYK/RAL/Pantone values approximate)</span>.</div>
</div></body></html>'''
    head, rest = html.split('<div class="draw">', 1)
    dr, tail = rest.split('</svg></div>', 1)
    wrap = lambda t: re.sub(r'(?<!class="en">)(\([A-Za-z0-9][^()<]*\))', r'<span class="en">\1</span>', t)
    html = wrap(head) + '<div class="draw">' + dr + '</svg></div>' + wrap(tail)
    open(f'drawing-{opt}.html', 'w').write(html)


for o in 'ab':
    build(o)
