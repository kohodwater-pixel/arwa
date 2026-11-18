"""Builds the two Direction B HTML sources (post, story). The generated HTML
files are the editable sources; this script keeps the sticker set in one place."""
import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFS = r'''
<defs>
  <!-- die-cut sticker: white outline + soft drop shadow -->
  <filter id="fSticker" x="-30%" y="-30%" width="160%" height="175%" color-interpolation-filters="sRGB">
    <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="b"/>
    <feColorMatrix in="b" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 60 -5" result="o"/>
    <feOffset in="o" dy="7" result="s0"/><feGaussianBlur in="s0" stdDeviation="5" result="s1"/>
    <feColorMatrix in="s1" type="matrix" values="0 0 0 0 0.03  0 0 0 0 0.12  0 0 0 0 0.08  0 0 0 .38 0" result="sh"/>
    <feMerge><feMergeNode in="sh"/><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <pattern id="pDotsB" width="26" height="26" patternUnits="userSpaceOnUse" patternTransform="rotate(28)"><circle cx="6" cy="6" r="3.500" fill="#FFF4DF" opacity=".13"/></pattern>
  <pattern id="pStripe" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)"><rect width="9" height="22" fill="#0C2E22" opacity=".1"/></pattern>

  <!-- stickers: each in a 100 x 100 box, flat fills, shared corner logic -->
  <g id="sBurger">
    <path d="M10 76H90V80A12 12 0 0 1 78 92H22A12 12 0 0 1 10 80Z" fill="#E8973A"/>
    <rect x="6" y="62" width="88" height="17" rx="8.500" fill="#5B2A19"/>
    <path d="M5 54H95V60H84L78 70Q75.500 73 73 70L67 60H40L36 66Q33.500 69 31 66L27 60H5Z" fill="#FFD23F" stroke="#FFD23F" stroke-width="3" stroke-linejoin="round"/>
    <rect x="9" y="46" width="82" height="10" rx="5" fill="#EF4B2F"/>
    <path d="M3 44Q4 37 12 38H88Q96 37 97 44Q97 51 90 50Q85 57 79 50Q73 57 67 50Q61 57 55 50Q49 57 43 50Q37 57 31 50Q25 57 19 50Q13 57 9 50Q3 51 3 44Z" fill="#59B947"/>
    <path d="M9 40C9 18 28 8 50 8C72 8 91 18 91 40Z" fill="#F2A545"/>
    <path d="M18 30C21 20 30 15 41 14" stroke="#FFDB9C" stroke-width="4" stroke-linecap="round" fill="none"/>
    <g fill="#FFF4DF"><ellipse cx="40" cy="22" rx="3.400" ry="1.900" transform="rotate(-22 40 22)"/><ellipse cx="55" cy="17" rx="3.400" ry="1.900" transform="rotate(8 55 17)"/><ellipse cx="69" cy="23" rx="3.400" ry="1.900" transform="rotate(26 69 23)"/><ellipse cx="50" cy="30" rx="3.400" ry="1.900" transform="rotate(-8 50 30)"/><ellipse cx="78" cy="32" rx="3.400" ry="1.900" transform="rotate(30 78 32)"/><ellipse cx="30" cy="33" rx="3.400" ry="1.900" transform="rotate(-28 30 33)"/></g>
  </g>
  <g id="sPizza">
    <path d="M10 26Q50 6 90 26L54 92Q50 97 46 92Z" fill="#FFD23F"/>
    <path d="M6 28Q50 2 94 28Q96 20 90 16Q50 -6 10 16Q4 20 6 28Z" fill="#E8973A"/>
    <path d="M14 19Q50 0 86 19" stroke="#F7C27A" stroke-width="3.500" stroke-linecap="round" fill="none"/>
    <circle cx="36" cy="38" r="8.500" fill="#EF4B2F"/><circle cx="62" cy="40" r="7.500" fill="#EF4B2F"/><circle cx="50" cy="62" r="7" fill="#EF4B2F"/>
    <circle cx="34" cy="36" r="2.200" fill="#FF8A73"/><circle cx="60" cy="38" r="2" fill="#FF8A73"/><circle cx="48" cy="60" r="1.900" fill="#FF8A73"/>
    <ellipse cx="50" cy="44" rx="4.500" ry="2.200" fill="#59B947" transform="rotate(-30 50 44)"/><ellipse cx="42" cy="54" rx="4" ry="2" fill="#59B947" transform="rotate(40 42 54)"/><ellipse cx="60" cy="54" rx="4" ry="2" fill="#59B947" transform="rotate(-50 60 54)"/>
  </g>
  <g id="sFries">
    <g fill="#FFD23F"><rect x="22" y="14" width="10" height="50" rx="3" transform="rotate(-12 27 39)"/><rect x="35" y="6" width="10" height="56" rx="3" transform="rotate(-4 40 34)"/><rect x="47" y="10" width="10" height="52" rx="3" transform="rotate(4 52 36)"/><rect x="59" y="4" width="10" height="58" rx="3" transform="rotate(9 64 33)"/><rect x="69" y="16" width="10" height="48" rx="3" transform="rotate(16 74 40)"/></g>
    <g fill="#F4B92A"><rect x="29" y="18" width="5" height="44" rx="2.500" transform="rotate(-12 27 39)"/><rect x="54" y="14" width="5" height="46" rx="2.500" transform="rotate(4 52 36)"/></g>
    <path d="M16 42Q50 54 84 42L76 90Q75 95 70 95H30Q25 95 24 90Z" fill="#EF4B2F"/>
    <path d="M16 42Q50 54 84 42L82.500 51Q50 62 17.500 51Z" fill="#FF7A5E"/>
    <circle cx="50" cy="74" r="9" fill="#FFF4DF"/>
  </g>
  <g id="sHeart">
    <path d="M50 90C50 90 8 64 8 35A23 23 0 0 1 50 21A23 23 0 0 1 92 35C92 64 50 90 50 90Z" fill="#FF4F7B"/>
    <path d="M22 36A13 13 0 0 1 35 23" stroke="#FFB3C8" stroke-width="6" stroke-linecap="round" fill="none"/>
  </g>
  <g id="sChat">
    <path d="M22 12H78A16 16 0 0 1 94 28V54A16 16 0 0 1 78 70H52L28 90V70H22A16 16 0 0 1 6 54V28A16 16 0 0 1 22 12Z" fill="#FFD23F"/>
    <circle cx="30" cy="41" r="6.500" fill="#0C2E22"/><circle cx="50" cy="41" r="6.500" fill="#0C2E22"/><circle cx="70" cy="41" r="6.500" fill="#0C2E22"/>
  </g>
  <g id="sMega">
    <path d="M44 62L50 88Q51 92 55 92H61Q66 92 65 87L59 62Z" fill="#0C2E22"/>
    <path d="M10 36H34L72 12Q78 9 78 16V84Q78 91 72 88L34 64H10Q6 64 6 60V40Q6 36 10 36Z" fill="#FF5A1F"/>
    <path d="M34 36V64H10Q6 64 6 60V40Q6 36 10 36Z" fill="#FFF4DF"/>
    <path d="M40 36L72 16" stroke="#FF9A70" stroke-width="5" stroke-linecap="round" fill="none"/>
    <path d="M86 38Q92 50 86 62" stroke="#FF8FB8" stroke-width="7" stroke-linecap="round" fill="none"/>
  </g>
  <g id="sHash">
    <rect x="8" y="8" width="84" height="84" rx="22" fill="#0C2E22"/>
    <path d="M40 26L33 74M67 26L60 74M24 40H78M22 60H76" stroke="#FFD23F" stroke-width="9" stroke-linecap="round" fill="none"/>
  </g>
  <g id="sPlay">
    <circle cx="50" cy="50" r="42" fill="#0C2E22"/>
    <circle cx="50" cy="50" r="33" fill="none" stroke="#FFF4DF" stroke-width="3" opacity=".35"/>
    <path d="M42 34L66 50L42 66Z" fill="#FFD23F" stroke="#FFD23F" stroke-width="7" stroke-linejoin="round"/>
  </g>
  <g id="sStar">
    <path d="M50 4L59 16L73 10L76 25L91 26L87 40L98 50L87 60L91 74L76 75L73 90L59 84L50 96L41 84L27 90L24 75L9 74L13 60L2 50L13 40L9 26L24 25L27 10L41 16Z" fill="#FFD23F"/>
    <path d="M50 78C50 78 28 64 28 49A12 12 0 0 1 50 42A12 12 0 0 1 72 49C72 64 50 78 50 78Z" fill="#EF4B2F"/>
  </g>
  <g id="sShare">
    <rect x="8" y="8" width="84" height="84" rx="24" fill="#FF8FB8"/>
    <path d="M27 72C27 50 41 40 57 40V27L81 49L57 71V57C45 57 35 61 27 72Z" fill="#0C2E22" stroke="#0C2E22" stroke-width="4" stroke-linejoin="round"/>
  </g>
</defs>
'''

ICONS = r'''
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-salary" viewBox="0 0 48 48"><rect x="4" y="11" width="40" height="26" rx="5" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round"/><circle cx="24" cy="24" r="6" fill="none" stroke="currentColor" stroke-width="5"/></symbol>
</svg>
'''

BODY = '''
<header class="head">
  <div class="kicker"><span>فرصة وظيفية</span></div>
  <h1><span class="a">موظف/ـة تسويق</span> <span class="b">وإدارة حسابات التواصل الاجتماعي</span></h1>
  <div class="meta">
    <p class="sector">لشركة متخصصة في قطاع المطاعم</p>
    <p class="tag"><svg aria-hidden="true"><use href="#i-salary"/></svg><span>راتب مجزٍ</span></p>
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
      <li>خبرة لا تقل عن 3 سنوات في التسويق وإدارة حسابات التواصل الاجتماعي</li>
      <li>خبرة في التصميم (شرط أساسي)</li>
      <li>معرفة جيدة بمنصات إنستغرام وتيك توك وسناب شات وإكس</li>
      <li>مهارة في كتابة المحتوى وحس إبداعي</li>
      <li>يُفضَّل من لديه خبرة في قطاع المطاعم</li>
    </ul>
  </div>
</section>

<footer class="apply">
  <p>للتقديم: أرسل/ي سيرتك الذاتية وسابقة أعمالك على البريد الإلكتروني</p>
  <div class="pill"><bdi class="email" dir="ltr">hr@otlobny.co</bdi></div>
</footer>
'''


def st(ref, cx, cy, size, rot=0):
    """A sticker centred on (cx, cy), `size` px wide, tilted `rot` degrees."""
    k = size / 100
    return (f'<g transform="translate({cx} {cy}) rotate({rot}) scale({k}) translate(-50 -50)">'
            f'<use href="#{ref}" filter="url(#fSticker)"/></g>')


def scene(fmt):
    if fmt == 'post':
        w, h = 1080, 1350
        fields = '''
  <path d="M0 0H1080V452Q560 548 0 470Z" fill="#0F3D2E"/>
  <path d="M0 0H1080V452Q560 548 0 470Z" fill="url(#pDotsB)"/>
  <circle cx="36" cy="20" r="132" fill="#FFD23F"/>
  <circle cx="150" cy="506" r="128" fill="#FF5A1F"/>
  <circle cx="1076" cy="548" r="74" fill="#FF8FB8"/>
  <path d="M0 1122Q540 1076 1080 1112V1350H0Z" fill="#FF5A1F"/>
  <circle cx="1050" cy="1350" r="84" fill="#FFD23F"/>'''
        stickers = [
            st('sPizza', 86, 78, 132, -14), st('sHeart', 234, 58, 64, 12), st('sChat', 368, 90, 94, -8),
            st('sHash', 508, 54, 56, 10), st('sPlay', 640, 84, 78, -6),
            st('sBurger', 146, 480, 196, -8), st('sFries', 290, 520, 100, 10),
            st('sHeart', 1030, 1300, 72, 12), st('sShare', 50, 1302, 70, -10),
        ]
    else:
        w, h = 1080, 1920
        fields = '''
  <path d="M0 0H1080V716Q560 812 0 734Z" fill="#0F3D2E"/>
  <path d="M0 0H1080V716Q560 812 0 734Z" fill="url(#pDotsB)"/>
  <circle cx="60" cy="40" r="210" fill="#FFD23F"/>
  <circle cx="1010" cy="150" r="150" fill="#FF5A1F"/>
  <circle cx="150" cy="772" r="128" fill="#FF5A1F"/>
  <circle cx="1076" cy="812" r="74" fill="#FF8FB8"/>
  <path d="M0 1386Q540 1340 1080 1376V1920H0Z" fill="#FF5A1F"/>
  <circle cx="1000" cy="1880" r="230" fill="#FFD23F"/>
  <circle cx="90" cy="1900" r="170" fill="#0F3D2E"/>'''
        stickers = [
            # top zone hero cluster (above the story safe area: no text there)
            st('sPizza', 150, 138, 230, -14), st('sMega', 420, 150, 170, -10), st('sChat', 640, 110, 130, 8),
            st('sHeart', 800, 214, 104, 12), st('sHash', 300, 44, 70, 10), st('sPlay', 964, 120, 130, -8), st('sShare', 548, 236, 72, -10),
            # boundary cluster
            st('sBurger', 146, 746, 196, -8), st('sFries', 290, 788, 100, 10),
            # bottom zone
            st('sBurger', 300, 1744, 300, 8), st('sFries', 640, 1752, 210, -8), st('sStar', 930, 1776, 190, 12),
            st('sHeart', 494, 1640, 84, -12), st('sChat', 800, 1640, 96, 8), st('sPizza', 90, 1650, 130, -20), st('sHash', 500, 1868, 70, 10),
        ]
    return f'''<svg class="scene" viewBox="0 0 {w} {h}" aria-hidden="true">
{DEFS}
  <!-- colour fields -->{fields}
  <!-- stickers -->
  {chr(10).join('  ' + s for s in stickers)}
</svg>'''


def page(fmt):
    size = '1080x1350' if fmt == 'post' else '1080x1920'
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>Job advert — direction B "Menu board" — {fmt} {size} — ar — v03</title>
<meta name="viewport" content="width=1080">
<link rel="stylesheet" href="base.css">
<link rel="stylesheet" href="direction-b.css">
</head>
<body class="{fmt} dir-b">
{ICONS}
<!-- colour fields and stickers: everything is inline vector, drawn for this piece -->
{scene(fmt)}
<main>
{BODY}
</main>
</body>
</html>
'''


for fmt in ('post', 'story'):
    name = f'tbc-restaurants-company_job-advert_{fmt}-direction-b_ar_v03.html'
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(page(fmt))
    print('wrote', name)
