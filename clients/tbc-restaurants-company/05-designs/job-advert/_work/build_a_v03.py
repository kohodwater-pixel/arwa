"""Builds the two Direction A v03 HTML sources (post, story). The HTML files are
the editable sources; this keeps the shared markup in one place. Positions and
sizes per format live in direction-a.css."""
import os, sys

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHOTO = 'assets/tbc-restaurants-company_burger-photo_client-supplied.png'

HEART = ('<svg class="{cls}" viewBox="0 0 100 92" style="width:{w}px;height:{h}px" aria-hidden="true">'
         '<path d="M50 88C50 88 6 62 6 31A24 24 0 0 1 50 18A24 24 0 0 1 94 31C94 62 50 88 50 88Z" fill="url(#gH{g})"/>'
         '<path d="M50 88C50 88 6 62 6 31A24 24 0 0 1 50 18A24 24 0 0 1 94 31C94 62 50 88 50 88Z" fill="url(#gHs)"/>'
         '<path d="M20 34A14 14 0 0 1 33 20" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".75"/></svg>')


def heart(x, y, w, rot, g=1, cls='heart3d'):
    return (f'<div class="fx" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)">'
            + HEART.format(cls=cls, w=w, h=round(w * .92), g=g) + '</div>')


IC_HEART = '<svg viewBox="0 0 24 24"><path d="M12 20.500C12 20.500 3.500 15.300 3.500 9.300A4.600 4.600 0 0 1 12 6.800A4.600 4.600 0 0 1 20.500 9.300C20.500 15.300 12 20.500 12 20.500Z" fill="#fff"/></svg>'
IC_CHAT = '<svg viewBox="0 0 24 24"><path d="M5.500 4.500H18.500A2.500 2.500 0 0 1 21 7V14.500A2.500 2.500 0 0 1 18.500 17H12L7.500 20.500V17H5.500A2.500 2.500 0 0 1 3 14.500V7A2.500 2.500 0 0 1 5.500 4.500Z" fill="#3A1A08"/></svg>'


def card(x, y, rot, icon, w1, w2, cls='', scale=1):
    ic = f'<span class="ic{" s" if icon is IC_CHAT else ""}">{icon}</span>'
    return (f'<div class="fx card-g {cls}" style="left:{x}px;top:{y}px;transform:rotate({rot}deg) scale({scale})">{ic}'
            f'<span class="ln"><i style="width:{w1}px"></i><i style="width:{w2}px"></i></span></div>')


def fx(fmt):
    if fmt == 'post':
        return '\n'.join([
            heart(332, 26, 30, 14, 2, 'heart3d far'),
            card(366, 204, 5, IC_HEART, 70, 44, scale=.94),
            heart(6, 150, 46, -16, 1),
            card(8, 470, -5, IC_CHAT, 66, 40, scale=.92),
            heart(432, 398, 34, 16, 1),
            heart(440, 486, 20, -10, 2, 'heart3d far'),
            heart(1010, 520, 26, 14, 2, 'heart3d far'),
        ])
    return '\n'.join([
        heart(96, 60, 54, -14, 1, 'heart3d far'),
        card(690, 150, 5, IC_HEART, 96, 60, scale=1.2),
        heart(820, 40, 44, 14, 2, 'heart3d far'),
        card(48, 392, -5, IC_CHAT, 84, 52, scale=1.12),
        heart(770, 404, 70, 14, 1),
        heart(930, 500, 34, -10, 2),
        heart(40, 250, 40, -18, 2),
        # below the story safe area: soft depth only
        heart(120, 1700, 90, -14, 1, 'heart3d near'),
        heart(860, 1640, 56, 12, 2, 'heart3d far'),
        heart(520, 1790, 40, 6, 1, 'heart3d far'),
    ])


def page(fmt, extra_cls=''):
    size = '1080x1350' if fmt == 'post' else '1080x1920'
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>Job advert — direction A "Phone on the pass" — {fmt} {size} — ar — v03</title>
<meta name="viewport" content="width=1080">
<link rel="stylesheet" href="base.css">
<link rel="stylesheet" href="direction-a.css">
</head>
<body class="{fmt} dir-a{extra_cls}">

<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <defs>
    <linearGradient id="gH1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF8A6B"/><stop offset=".5" stop-color="#EE4A32"/><stop offset="1" stop-color="#B71F12"/></linearGradient>
    <linearGradient id="gH2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE08A"/><stop offset=".5" stop-color="#FFB52E"/><stop offset="1" stop-color="#E07F06"/></linearGradient>
    <radialGradient id="gHs" cx=".32" cy=".24" r=".7"><stop offset="0" stop-color="#fff" stop-opacity=".45"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <filter id="fGrain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" seed="11" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
  </defs>
  <symbol id="i-megaphone" viewBox="0 0 34 34"><path d="M6 13.500V20.500H10.500L21 26.500V7.500L10.500 13.500Z"/><path d="M11.500 21L13 27.500H16.500L15.200 22.500"/><path d="M25 13A5.500 5.500 0 0 1 25 21"/></symbol>
  <symbol id="i-home" viewBox="0 0 48 48"><path d="M6 23L24 7L42 23"/><path d="M11 21V40H37V21"/><path d="M18.500 33A8 8 0 0 1 29.500 33"/></symbol>
  <symbol id="i-send" viewBox="0 0 96 96"><circle cx="48" cy="48" r="48" fill="#2B1430"/><circle cx="48" cy="48" r="47" fill="none" stroke="#fff" stroke-opacity=".14" stroke-width="2"/><path d="M24 49L71 27L57 72L46 55Z" fill="#FFB52E"/><path d="M46 55L71 27L41 59L42 69Z" fill="#E58A0C"/></symbol>
</svg>

<!-- atmosphere -->
<div class="glow"></div>
<svg class="grain" aria-hidden="true"><rect width="100%" height="100%" filter="url(#fGrain)"/></svg>
<div class="vignette"></div>

<!-- phone mock: CSS only -->
<div class="phone" aria-hidden="true">
  <span class="btn r"></span><span class="btn l1"></span><span class="btn l2"></span>
  <div class="glass"><div class="screen">
    <div class="island"></div>
    <div class="ui">
      <div class="ui-prev"><i></i><i></i><i></i></div>
      <div class="ui-head"><span class="av"></span><span class="n1"></span><span class="n2"></span><span class="dots"></span></div>
      <div class="ui-photo"></div>
      <div class="ui-actions">
        <svg class="a1" viewBox="0 0 28 28"><path d="M14 24C14 24 4 18 4 11A5.400 5.400 0 0 1 14 8A5.400 5.400 0 0 1 24 11C24 18 14 24 14 24Z" fill="#E5412D" stroke="#E5412D"/></svg>
        <svg class="a2" viewBox="0 0 28 28"><path d="M7 5H21A3 3 0 0 1 24 8V16.500A3 3 0 0 1 21 19.500H14L9 23.500V19.500H7A3 3 0 0 1 4 16.500V8A3 3 0 0 1 7 5Z"/></svg>
        <svg class="a3" viewBox="0 0 28 28"><path d="M4 13.500L24 4.500L18 24L13.500 16Z"/><path d="M13.500 16L24 4.500"/></svg>
        <svg class="a4" viewBox="0 0 28 28"><path d="M7 4.500H21V24L14 18.500L7 24Z"/></svg>
      </div>
      <div class="ui-cap"><i></i><i></i><i></i></div>
      <div class="ui-next"></div>
    </div>
    <div class="sheen"></div>
  </div></div>
</div>

<!-- client-supplied burger photograph (unaltered; scaled proportionally) -->
<img class="burger" src="{PHOTO}" alt="">

<!-- floating reactions -->
{fx(fmt)}

<main>
<div class="kicker"><svg aria-hidden="true"><use href="#i-megaphone"/></svg><span>فرصة وظيفية</span></div>

<header class="head">
  <h1><span class="a">موظف/ـة تسويق</span> <span class="b"><span class="b1">وإدارة حسابات</span> <span class="b2">التواصل الاجتماعي</span></span></h1>
  <div class="meta">
    <p class="sector">لشركة متخصصة في قطاع المطاعم</p>
    <p class="tag"><svg aria-hidden="true"><use href="#i-home"/></svg><span>العمل عن بُعد</span></p>
  </div>
</header>

<section class="cards">
  <div class="block">
    <h2>المهام</h2>
    <ul>
      <li>إعداد خطة المحتوى الشهرية وتنفيذها</li>
      <li>إدارة حسابات التواصل الاجتماعي والنشر والتفاعل مع العملاء</li>
      <li>كتابة المحتوى الإعلاني والتنسيق مع المصممين والمصورين</li>
      <li>إدارة الحملات الإعلانية المدفوعة ومتابعة نتائجها</li>
      <li>إعداد تقارير الأداء الدورية</li>
    </ul>
  </div>
  <div class="block">
    <h2>المتطلبات</h2>
    <ul>
      <li>خبرة سابقة في التسويق وإدارة حسابات التواصل الاجتماعي</li>
      <li>خبرة في التصميم (شرط أساسي)</li>
      <li>معرفة جيدة بمنصات إنستغرام وتيك توك وسناب شات وإكس</li>
      <li>مهارة في كتابة المحتوى وحس إبداعي</li>
      <li>يُفضَّل من لديه خبرة في قطاع المطاعم</li>
    </ul>
  </div>
</section>

<footer class="apply">
  <p>للتقديم: أرسل/ي سيرتك الذاتية وسابقة أعمالك على البريد الإلكتروني</p>
  <div class="pill"><svg class="send" aria-hidden="true"><use href="#i-send"/></svg><bdi class="email" dir="ltr">hr@otlobny.co</bdi></div>
</footer>
</main>
</body>
</html>
'''


for fmt in ('post', 'story'):
    name = f'tbc-restaurants-company_job-advert_{fmt}-direction-a_ar_v03.html'
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(page(fmt))
    print('wrote', name)
if '--plex' in sys.argv:  # typeface comparison render, kept in _work only
    html = page('post', ' plex').replace('href="base.css"', 'href="../base.css"').replace('href="direction-a.css"', 'href="../direction-a.css"').replace('src="assets/', 'src="../assets/')
    open(os.path.join(OUT, '_work', 'compare_post-direction-a_plex.html'), 'w', encoding='utf-8').write(html)
