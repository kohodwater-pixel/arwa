#!/usr/bin/env python3
"""Derive the guidelines v02 HTML and the v02 tokens from the v01 sources (round-2 rulings)."""
import json
import os

IDENT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(IDENT)
S = 'demo-sidra-coffee'
PW = 'waived for system test; required before print'


def sub(s, pairs):
    for a, b in pairs:
        assert a in s, a[:70]
        s = s.replace(a, b)
    return s


g = open(f'05-guidelines/{S}_brand-guidelines_mini_ar-en_v01.html').read()
g = g.replace('to be matched by printer', PW)
g = g.replace('Mini brand guidelines v01', 'Mini brand guidelines v02')
g = sub(g, [
 ('brand.css', 'brand-v02.css'), ('Version 01 · 2026-11-13', 'Version 02 · 2026-11-13'),
 ('  .pattern { margin: 0 -15mm 7mm; display: grid; row-gap: calc(210mm / 41); background: var(--crema); padding: calc(210mm / 41) 0; }\n  .pattern .bars { height: 13mm; }',
  '  /* cover pattern: three band rows. Block 82 mm wide: bar 10 mm, gap 2 mm, bar height 20 mm (1:2). */\n  .field { margin: 0 -15mm 7mm; background: var(--crema); padding: 6mm 15mm; display: flex; justify-content: space-between; align-items: flex-end; direction: ltr; }\n  .pattern { width: 82mm; display: grid; row-gap: 2mm; }\n  .pattern .bars { height: 20mm; }\n  .field .title-ar { margin-bottom: 0; max-width: 85mm; }'),
 ('  <div class="title-ar">دليل الهوية المختصر</div>\n  <div class="pattern">', '  <div class="field">\n  <div class="pattern">'),
 ('    <div class="bars"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>\n  </div>\n  <div class="bi">\n    <div class="en"><h3>01',
  '    <div class="bars"><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>\n  </div>\n  <div class="title-ar">دليل الهوية المختصر</div>\n  </div>\n  <div class="bi">\n    <div class="en"><h3>01'),
 ('logo_icon-colour_ar-en_v01.svg', 'logo_icon-colour_ar-en_v02.svg'),
 ('test_logo_16px-high_x10.png', 'test_logo_16px-high_x10_v02.png'),
 ('* CMYK values are approximate and uncalibrated. The printer matches each colour to the HEX value on a proof. No Pantone reference is licensed for this project.',
  '* CMYK values are approximate and uncalibrated. Pantone references and ICC-calibrated CMYK are waived for this system test and are required before print.'),
 ('Figures<br>AR 700 · EN 300, 85% width', 'Figures<br>AR 700 · EN Light 300'),
 ('preview_business-card_ar-en_v01.png', 'preview_business-card_ar-en_v02.png'),
 ('preview_bag-label_1kg_ar-en_v01.png', 'preview_bag-label_1kg_ar-en_v02.png'),
 ('Arabic side on Paper, English side on Crema. The phone number is a marked placeholder until the client supplies it.',
  'Arabic side on Paper, English side on Crema. Email is the only contact channel.'),
 ('بطاقة العمل، 90 × 50 مم. رقم الهاتف مؤقت ومعلَّم إلى أن يزوّدنا به العميل.', 'بطاقة العمل، 90 × 50 مم. البريد الإلكتروني هو قناة التواصل الوحيدة.'),
 ('<td>SVG, outlined. primary,', '<td>SVG, PDF, PNG at 1x, 2x, 4x; outlined. primary,'),
 ('<li>Print colours and minimum print sizes need a press proof.</li>',
  '<li>Pantone and calibrated CMYK values were waived for this test and are required before any print job. Minimum print sizes need a press proof.</li>\n      <li>The wordmark is outlined IBM Plex Sans Arabic Bold, accepted for this test. A redraw is required before real use.</li>'),
 ('<li>ألوان الطباعة والأحجام الدنيا المطبوعة تحتاج إلى تجربة طباعية.</li>',
  '<li>أُجّلت مراجع بانتون وقيم CMYK المعايَرة في هذا الاختبار، وهي لازمة قبل أي طباعة. والأحجام الدنيا المطبوعة تحتاج إلى تجربة طباعية.</li>\n      <li>الكلمة المرسومة مأخوذة من خط IBM Plex Sans Arabic Bold وقُبلت لهذا الاختبار، ويلزم إعادة رسمها قبل الاستعمال الفعلي.</li>'),
 ('<li>The logo and name have had a first check only. This is not a legal trademark clearance; a formal search is needed before registration.</li>',
  '<li>The name has had one web search only, and the mark itself has not been compared with other marks. This is not a legal trademark clearance; a formal search is needed before registration.</li>'),
 ('<li>فُحص الشعار والاسم فحصًا أوليًا فقط. هذا ليس فحصًا قانونيًا للعلامة التجارية، ويلزم بحث رسمي قبل التسجيل.</li>',
  '<li>أُجري للاسم بحث واحد على الإنترنت فقط، ولم يُقارَن الشعار نفسه بعلامات أخرى. هذا ليس فحصًا قانونيًا للعلامة التجارية، ويلزم بحث رسمي قبل التسجيل.</li>'),
])
assert g.count('<div class="pattern">') == 1 and '966' not in g and 'TBC' not in g
open(f'05-guidelines/{S}_brand-guidelines_mini_ar-en_v02.html', 'w').write(g)

t = json.load(open('03-system/_archive/tokens_v01.json'))
t = {'$version': 'v02 (2026-11-13). v01 is kept in _archive/tokens_v01.json', **t}
t['$description'] = ("Sidra Coffee design tokens. SYSTEM TEST, fictional client. Source: 04-identity/01-direction/creative-direction.md "
                     "(approved 2026-11-13). CMYK values are uncalibrated approximations. Pantone references and ICC-calibrated CMYK are "
                     "waived for system test; required before print (decision log 2026-11-13, ruling e).")
for k, v in t['color'].items():
    v['pantone'] = PW
    v['cmyk_status'] = 'approximate; ICC-calibrated CMYK ' + PW + ('; body text prints 100K' if k == 'ink' else '')
t['font']['figures'] = {'arabic': 'IBM Plex Sans Arabic Bold 700, unit in Arabic',
                        'latin': 'IBM Plex Sans Light 300, regular width (v02: the 85% width was dropped because it needs the variable font)'}
t['font']['files'] = {'arabic': 'assets/fonts/ibmplexsansarabic/ (static)', 'latin': 'assets/fonts/ibmplexsans-static/ (official static files)'}
t['logo']['icon'] = ('v02: three stacked band rows (bar 1:2.6) filling the square, lit bars in the centre column. '
                     'Seven bars count reliably from 41 px; switch size stays 48 px.')
t['logo']['status'] = ('ladder accepted for the test (decision log 2026-11-13, ruling g). Screen sizes from pixel tests in 02-logo/_work; '
                       'print sizes simulated at 600 dpi, not press-tested')
t['logo']['formats'] = 'SVG (source), vector PDF in 02-logo/pdf/, transparent PNG at 1x, 2x, 4x in 02-logo/png/'
json.dump(t, open('03-system/tokens.json', 'w'), indent=2, ensure_ascii=False)
print('ok')
