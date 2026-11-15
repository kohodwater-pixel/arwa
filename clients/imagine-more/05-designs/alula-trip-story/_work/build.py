#!/usr/bin/env python3
"""Generates the three option HTML files from one template (same layout, different photo)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
HL = (int(os.environ.get('HLW', 600)), float(os.environ.get('HLS', 62)))
OPTS = json.load(open(os.path.join(HERE, 'options.json'), encoding='utf8'))

SAR = '<path fill="currentColor" d="M699.62,1113.02h0c-20.06,44.48-33.32,92.75-38.4,143.37l424.51-90.24c20.06-44.47,33.31-92.75,38.4-143.37l-424.51,90.24Z"/><path fill="currentColor" d="M1085.73,895.8c20.06-44.47,33.32-92.75,38.4-143.37l-330.68,70.33v-135.2l292.27-62.11c20.06-44.47,33.32-92.75,38.4-143.37l-330.68,70.27V66.13c-50.67,28.45-95.67,66.32-132.25,110.99v403.35l-132.25,28.11V0c-50.67,28.44-95.67,66.32-132.25,110.99v525.69l-295.91,62.88c-20.06,44.47-33.33,92.75-38.42,143.37l334.33-71.05v170.26l-358.3,76.14c-20.06,44.47-33.32,92.75-38.4,143.37l375.04-79.7c30.53-6.35,56.77-24.4,73.83-49.24l68.78-101.97v-.02c7.14-10.55,11.3-23.27,11.3-36.97v-149.98l132.25-28.11v270.4l424.53-90.28Z"/>'
STAR = '<svg class="abs star {c}" viewBox="0 0 24 24"><path fill="#fff" d="M12 0c.9 6.9 4.2 10.6 12 12-7.8 1.4-11.1 5.1-12 12-.9-6.9-4.2-10.6-12-12C7.8 10.6 11.1 6.9 12 0Z"/></svg>'

ICONS = {
 # cup with steam
 'cup': '<svg viewBox="0 0 54 48"><path d="M19 3v7M26 3v7M33 3v7"/><path d="M10 16h30v12a13 13 0 0 1-13 13h-4a13 13 0 0 1-13-13Z"/><path d="M40 19h3.500a5.5 5.5 0 0 1 0 11H39.6"/></svg>',
 # croissant with a steaming cup behind it
 'breakfast': '<svg viewBox="0 0 54 48"><defs><mask id="bk" maskUnits="userSpaceOnUse" x="0" y="0" width="54" height="48"><rect width="54" height="48" fill="#fff"/><g fill="#000" stroke="#000" stroke-width="3.6"><ellipse cx="16" cy="35" rx="5" ry="7.6"/><ellipse cx="8.6" cy="37.6" rx="3.8" ry="6.2" transform="rotate(26 8.6 37.6)"/><ellipse cx="23.4" cy="37.6" rx="3.8" ry="6.2" transform="rotate(-26 23.4 37.6)"/><ellipse cx="3.6" cy="42" rx="2.3" ry="4.2" transform="rotate(52 3.6 42)"/><ellipse cx="28.4" cy="42" rx="2.3" ry="4.2" transform="rotate(-52 28.4 42)"/></g></mask></defs><g stroke-width="2" ><path d="M29 14c-1.6-1.8 1.6-3.2 0-5s1.6-3.2 0-5"/><path d="M34.5 13c-1.6-1.8 1.6-3.4 0-5.400s1.6-3.6 0-5.6"/><path d="M40 14c-1.6-1.8 1.6-3.2 0-5s1.6-3.2 0-5"/></g><g mask="url(#bk)"><path fill="#fff" stroke="none" d="M22 17.500h25c.6 0 1 .4 1 1 0 8.5-3.6 15.5-9 17.500h-9c-5.4-2-9-9-9-17.5 0-.6.4-1 1-1Z"/><path d="M47.5 20.500h1.700a3.6 3.6 0 0 1 0 7.200h-3.4" stroke-width="2.6"/></g><g fill="#fff" stroke="none"><ellipse cx="16" cy="35" rx="5" ry="7.6"/><ellipse cx="8.6" cy="37.6" rx="3.8" ry="6.2" transform="rotate(26 8.6 37.6)"/><ellipse cx="23.4" cy="37.6" rx="3.8" ry="6.2" transform="rotate(-26 23.4 37.6)"/><ellipse cx="3.6" cy="42" rx="2.3" ry="4.2" transform="rotate(52 3.6 42)"/><ellipse cx="28.4" cy="42" rx="2.3" ry="4.2" transform="rotate(-52 28.4 42)"/></g></svg>',
 # plate with fork and knife
 'dinner': '<svg viewBox="0 0 54 48"><circle cx="27" cy="25" r="12.5"/><circle cx="27" cy="25" r="6"/><path d="M5 4v10a4 4 0 0 0 8 0V4M9 4v40"/><path d="M47 44V4c-4.5 3.5-6 10-6 20h6"/></svg>',
 # bus
 'bus': '<svg viewBox="0 0 54 48"><rect x="6" y="5" width="42" height="31" rx="7"/><path d="M6 22h42M20.5 6v16M33.5 6v16"/><circle cx="15.5" cy="38" r="4.5" fill="none"/><circle cx="38.5" cy="38" r="4.5"/><path d="M20 36h14"/></svg>',
 # ticket, tilted
 'ticket': '<svg viewBox="0 0 54 48"><g transform="rotate(-17 27 24)"><path d="M5 12h44v7.500a4.5 4.5 0 0 0 0 9V36H5v-7.500a4.5 4.5 0 0 0 0-9Z"/><path d="M31 13v22" stroke-dasharray="3.5 4"/></g></svg>',
}
GROUP = '<svg viewBox="0 0 50 30"><g fill="#fff"><circle cx="25" cy="6.5" r="6.5"/><circle cx="9.5" cy="10" r="4.8"/><circle cx="40.5" cy="10" r="4.8"/><path d="M12.5 30c0-8 5-13.5 12.5-13.500S37.5 22 37.5 30Z"/><path d="M0 30c0-6.5 3.8-11 9.5-11 1.6 0 3 .4 4.3 1-2.6 2.6-4 6-4.3 10Z"/><path d="M50 30c0-6.5-3.8-11-9.5-11-1.6 0-3 .4-4.3 1 2.6 2.6 4 6 4.3 10Z"/></g></svg>'

INC = [(702, 'cup', 'ضيافة', 'على الرحلة'), (579, 'breakfast', 'وجبة إفطار', 'من هيبو'), (457, 'dinner', 'وجبة غداء', 'لذيذة'), (334, 'bus', 'تنقلات', 'مريحة'), (212, 'ticket', 'رسوم الدخول', 'للمواقع')]

TPL = '''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1080">
<title>Imagine More × Hippo — AlUla trip story — option {L} (1080×1920)</title>
<link rel="stylesheet" href="story.css">
<style>
/* option {L}: {subject} */
:root{{--photo:url("assets/photos/{photo}");--bg-size:{size};--bg-pos:{pos};--top-a:{top};{toprgb}--bot-a:{bot};--glass-a:{glass};--under-a:{under};--chip-under:{chip};--hl-w:{hlw};--hl-s:{hls}px}}
</style>
</head>
<body>
<main class="story">
  <div class="bg"></div>
  <div class="shade-top"></div>
  <div class="shade-bottom"></div>

  <img class="abs logo-hippo" src="assets/img/logo-hippo.png" alt="HIPPO">

  {star_r}
  {star_l}
  <h1 class="abs headline">مـــن المـــديـــنـــة إلـــى العُـــلا</h1>
  <p class="abs sub">يــوم كــامــل فــي ســحــر العُــلا</p>

  <div class="abs chips glass">
    <div class="cell date"><b>كل يوم جمعة</b>من 20 نوفمبر حتى 5 فبراير</div>
    <div class="rule"></div>
    <div class="cell">رحلات .. تجارب استثنائية</div>
  </div>

  <section class="abs price glass">
    <div class="abs label">سعر الرحلة<br>للشخص</div>
    <div class="abs now ltr">299</div>
    <div class="abs was"><svg viewBox="0 0 1124.14 1256.39" aria-hidden="true">{sar}</svg><span>320</span></div>
    <svg class="abs sar" viewBox="0 0 1124.14 1256.39" role="img" aria-label="ريال سعودي">{sar}</svg>
    <div class="abs rule"></div>
    <div class="abs group">{group}خصم خاص<br>للمجموعات</div>
  </section>

  <div class="abs inc-label glass">تشمل<br>الرحلة</div>
{inc}

  <div class="abs cta"><span>احجز الآن</span><span class="dot"><svg viewBox="0 0 16 16"><path d="M10.5 2.5 5 8l5.5 5.5"/></svg></span></div>

  <div class="abs phone"><span class="t">للحجـز والاستفسار</span><span class="n ltr" dir="ltr">+966 50 814 7381</span></div>

  <img class="abs social" src="assets/img/icons-social.png" alt="Instagram, Snapchat, X, TikTok">
  <div class="abs foot handle" dir="ltr"><i>|</i>Imaginemore_sa</div>
  <img class="abs wa" src="assets/img/icon-whatsapp.png" alt="WhatsApp">
  <div class="abs foot wanum" dir="ltr"><i>|</i>014 834 6811</div>
  <div class="abs foot ln" dir="ltr">LN 73103653</div>

  <img class="abs logo-im" src="assets/img/logo-imagine-more.png" alt="Imagine More — Tourism | Media | Events">
</main>
</body>
</html>
'''

for o in OPTS:
    inc = '\n'.join(f'  <div class="abs inc" style="left:{x}px">{ICONS[k]}{a}<br>{b}</div>' for x, k, a, b in INC)
    html = TPL.format(L=o['letter'].upper(), subject=o['subject'], photo=o['photo'], size=o.get('size', 'cover'), pos=o.get('pos', '50% 50%'),
                      top=o.get('top', .62), toprgb=o.get('toprgb',''), bot=o.get('bot', 1), glass=o.get('glass', .2), under=o.get('under', .5), chip=o.get('chip', .25), hlw=HL[0], hls=HL[1], sar=SAR, group=GROUP, inc=inc,
                      star_r=STAR.format(c='r'), star_l=STAR.format(c='l'))
    p = os.path.join(OUT, f"imagine-more_alula-trip-story_option-{o['letter']}_ar_{o['ver']}.html")
    open(p, 'w', encoding='utf8').write(html)
    print('wrote', p)
