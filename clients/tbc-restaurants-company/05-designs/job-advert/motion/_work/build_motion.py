"""Generates the motion HTML source from the Direction A illustration fragments
in ../../_work/build_a.py (phone, burger, reactions), so the film and the
statics share one drawing. Run once; the HTML it writes is the editable source."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(HERE)
src = open(os.path.join(MOTION, '..', '_work', 'build_a.py'), encoding='utf-8').read()
DEFS = re.search(r"DEFS = r'''(.*?)'''", src, re.S).group(1)
ICONS = re.search(r"ICONS = r'''(.*?)'''", src, re.S).group(1)

# split the phone out of <defs> so its parts can be animated
i0 = DEFS.index('<!-- the phone, drawn in its own 360 x 700 box -->')
i1 = DEFS.index('</defs>')
phone = DEFS[i0:i1]
DEFS = DEFS[:i0]
phone = phone[phone.index('<g id="phone">') + len('<g id="phone">'):phone.rindex('</g>')]
b0 = phone.index('<!-- burger, drawn bottom-up -->')
b1 = phone.index('<use href="#spark" x="56"')
burger = phone[b0:b1]
phone = phone[:b0] + '<use id="phoneBurger" href="#burgerDef"/>\n      ' + phone[b1:]
old_heart = '<use href="#heart" x="268" y="462" width="40" height="40" fill="#E5412D"/>'
assert old_heart in phone
phone = phone.replace(old_heart, '<g id="likeHeart">' + old_heart + '</g>')
phone = phone.replace('<!-- glare -->', '<rect id="screenOff" x="34" y="34" width="292" height="632" fill="#241329"/>\n      <!-- glare -->')
DEFS += '  <g id="burgerDef">\n      ' + burger.strip() + '\n  </g>\n</defs>\n'

def use(i, ref): return f'<use id="{i}" href="#{ref}"/>'
def heart(i, fill): return f'<use id="{i}" href="#heart" x="-24" y="-24" width="48" height="48" fill="{fill}"/>'
def spark(i, fill): return f'<use id="{i}" href="#spark" x="-20" y="-20" width="40" height="40" fill="{fill}"/>'

STAGE = f'''<svg id="stage" viewBox="0 0 1080 1920" aria-hidden="true">
{DEFS}
  <g id="disc">
    <circle r="470" fill="url(#gDisc)"/><circle r="470" fill="url(#pDots)"/>
    <g id="ring"><circle r="498" fill="none" stroke="#FFB52E" stroke-width="4" stroke-dasharray="2 18" stroke-linecap="round"/></g>
  </g>
  <circle id="shock" r="330" fill="none" stroke="#FFB52E" stroke-width="12"/>

  <!-- food: plate, cutlery, burger, chef hat (origin = plate centre) -->
  <g id="food">
    <g id="fork" fill="#FFF3DC" stroke="#FFF3DC" stroke-width="8" stroke-linejoin="round">
      <path d="M-40 -250V-128Q-40 -84 -12 -76V246H12V-76Q40 -84 40 -128V-250H26V-136H7V-250H-7V-136H-26V-250Z"/>
    </g>
    <g id="knife" fill="#FFF3DC" stroke="#FFF3DC" stroke-width="8" stroke-linejoin="round">
      <path d="M-12 246H12V-20H24V-150Q24 -250 -20 -252V-20H-12Z"/>
    </g>
    <g id="plate">
      <ellipse cx="0" cy="196" rx="330" ry="70" fill="#12060F" opacity=".4"/>
      <ellipse cx="0" cy="164" rx="350" ry="112" fill="#DCC79D"/>
      <ellipse cx="0" cy="150" rx="350" ry="112" fill="#FFF8EA"/>
      <ellipse cx="0" cy="152" rx="252" ry="76" fill="#EFDFBE"/>
      <ellipse cx="0" cy="158" rx="240" ry="68" fill="#FFF8EA"/>
      <path d="M-322 128A350 112 0 0 1 -150 52" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity=".9"/>
    </g>
    <g transform="translate(0 150)"><ellipse id="burgerShadow" cx="0" cy="0" rx="226" ry="36" fill="#B58A4A" opacity=".5"/></g>
    <g id="foodBurger"><use href="#burgerDef" transform="translate(0 152) scale(2) translate(-180 -408)"/></g>
    <g id="hat"><g transform="scale(1.3)">
      <path d="M-78 -40C-132 -58 -130 -150 -70 -152C-66 -216 22 -234 46 -176C104 -196 142 -118 80 -42Z" fill="#FFF8EA"/>
      <path d="M-78 -40C-132 -58 -130 -150 -70 -152C-110 -140 -112 -80 -72 -62Z" fill="#EADBC0"/>
      <path d="M-38 -62V-112M2 -58V-124M42 -62V-114" stroke="#E2CFA8" stroke-width="7" stroke-linecap="round" fill="none"/>
      <path d="M-82 -46H84V-6Q84 6 72 6H-70Q-82 6 -82 -6Z" fill="#F4E6C8"/>
      <path d="M-82 -30H84" stroke="#E2CFA8" stroke-width="5"/>
    </g></g>
  </g>

  <!-- phone (inline so the screen, burger and like heart can be animated) -->
  <g id="phone"><g filter="url(#fPhone)">
    {phone.strip()}
  </g></g>

  <!-- reactions -->
  {use('r0', 'bLike')}{use('r1', 'bChat')}{use('r2', 'bShare')}{use('r3', 'bPlay')}{use('r4', 'bHash')}
  {heart('h0', '#E5412D')}{heart('h1x', '#FFB52E')}{heart('h2', '#FFF3DC')}{heart('h3', '#FF7A62')}{heart('h4', '#E5412D')}
  {spark('sp0', '#FFB52E')}{spark('sp1', '#FFF3DC')}{spark('sp2', '#FFB52E')}
</svg>'''

HTML = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>Job advert — motion graphic, direction A — 1080x1920 — ar — v01</title>
<meta name="viewport" content="width=1080">
<link rel="stylesheet" href="motion.css">
</head>
<body>
{ICONS}
<div id="frame">
{STAGE}

<!-- on-screen text: only strings from the advert copy in 01-brief/brief.md -->
<div class="it" id="kicker" data-copy><svg aria-hidden="true"><use href="#i-megaphone"/></svg><span>فرصة وظيفية</span></div>

<h1 class="it" id="h1" data-copy><span class="ln a"><span class="w" id="w0">موظف/ـة</span> <span class="w" id="w1">تسويق</span></span> <span class="ln b"><span class="w" id="w2">وإدارة</span> <span class="w" id="w3">حسابات</span></span> <span class="ln b"><span class="w" id="w4">التواصل</span> <span class="w" id="w5">الاجتماعي</span></span></h1>

<p class="it" id="sector" data-copy>لشركة متخصصة في قطاع المطاعم</p>

<div class="it" id="tag" data-copy><svg aria-hidden="true"><use href="#i-home"/></svg><span>العمل عن بُعد</span></div>

<div class="it" id="design">
  <svg viewBox="0 0 860 150" aria-hidden="true">
    <path d="M60 112L136 26M430 52L352 124" stroke="#2B1430" stroke-width="3" opacity=".45"/>
    <circle cx="136" cy="26" r="8" fill="#FFF3DC" stroke="#2B1430" stroke-width="4"/><circle cx="352" cy="124" r="8" fill="#FFF3DC" stroke="#2B1430" stroke-width="4"/>
    <path id="penPath" d="M60 112C170 -20 300 170 430 52" fill="none" stroke="#E5412D" stroke-width="8" stroke-linecap="round"/>
    <rect x="49" y="101" width="22" height="22" rx="4" fill="#FFF3DC" stroke="#2B1430" stroke-width="5"/><rect x="419" y="41" width="22" height="22" rx="4" fill="#FFF3DC" stroke="#2B1430" stroke-width="5"/>
    <g id="penNib"><path d="M0 0L-15 -34V-62H15V-34Z" fill="#2B1430" stroke="#2B1430" stroke-width="5" stroke-linejoin="round"/><path d="M0 -6V-30" stroke="#FFF3DC" stroke-width="3.500" stroke-linecap="round"/><circle cx="0" cy="-34" r="4.500" fill="#FFF3DC"/><rect x="-17" y="-76" width="34" height="12" rx="4" fill="#FFB52E"/></g>
    <g id="sw0"><rect x="-30" y="-30" width="60" height="60" rx="18" fill="#E5412D"/></g>
    <g id="sw1"><rect x="-30" y="-30" width="60" height="60" rx="18" fill="#FFB52E"/></g>
    <g id="sw2"><rect x="-30" y="-30" width="60" height="60" rx="18" fill="#6DBE45"/></g>
    <g id="sw3"><rect x="-30" y="-30" width="60" height="60" rx="18" fill="#5A2A62"/></g>
    <g id="sw4"><rect x="-30" y="-30" width="60" height="60" rx="18" fill="#2B1430"/></g>
  </svg>
  <p data-copy>خبرة في التصميم (شرط أساسي)</p>
</div>

<p class="it chip" id="chip0" data-copy>خبرة سابقة في التسويق وإدارة حسابات التواصل الاجتماعي</p>
<p class="it chip" id="chip1" data-copy>معرفة جيدة بمنصات إنستغرام وتيك توك وسناب شات وإكس</p>
<p class="it chip" id="chip2" data-copy>مهارة في كتابة المحتوى وحس إبداعي</p>
<p class="it chip" id="chip3" data-copy>يُفضَّل من لديه خبرة في قطاع المطاعم</p>

<p class="it" id="applyline" data-copy>للتقديم: أرسل/ي سيرتك الذاتية وسابقة أعمالك على البريد الإلكتروني</p>
<div class="it" id="pill"><div id="shine"></div><svg class="send" aria-hidden="true"><use href="#i-send"/></svg><bdi id="email" dir="ltr" data-copy>hr@otlobny.co</bdi></div>

</div>
<script src="motion.js"></script>
</body>
</html>
'''
name = 'tbc-restaurants-company_job-advert_motion-direction-a_ar_v01.html'
open(os.path.join(MOTION, name), 'w', encoding='utf-8').write(HTML)
print('wrote', name)
