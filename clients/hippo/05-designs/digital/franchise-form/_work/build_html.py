#!/usr/bin/env python3
"""Writes src/index.html (Arabic) and src/index-en.html (English) from one structure,
so the two languages cannot drift apart. The output is plain static HTML and can
also be edited by hand; re-running this script overwrites such edits.
Usage: python3 _work/build_html.py"""
import html, pathlib

SRC = pathlib.Path(__file__).resolve().parent.parent / "src"

AR = dict(
    lang="ar", dir="rtl", other_file="index-en.html", other_lang="en", other_dir="ltr", other_name="English",
    title="امتياز هيبو التجاري — استفسار", desc="نموذج الاستفسار عن امتياز هيبو التجاري.",
    skip="انتقل إلى النموذج",
    draft="<b>مسودة للعرض</b> — النموذج غير موصول بعد، ولن تُرسَل أي بيانات.",
    logo_alt="شعار هيبو — HIPPO Brioche Bread",
    masthead='<p class="label">امتياز هيبو التجاري</p>\n  <p class="label-en" lang="en" dir="ltr">Franchise</p>',
    photo_alt="ساندوتش بريوش من هيبو في حامله الأبيض",
    spot='<h1 id="campaign-line">حُطّ ثقلك.</h1>\n        <p class="support" lang="en" dir="ltr">Put your weight behind it.</p>',
    lead="كفّتنا مليانة، والكفّة الثانية ناقصها ثقلك. اترك بياناتك ونتواصل معك بخصوص امتياز هيبو التجاري.",
    h2="استفسار عن الامتياز", intro="ثلاث خطوات. كل الحقول مطلوبة، إلا ما كُتب بجانبه «اختياري».",
    noscript="هذا النموذج يحتاج إلى تفعيل JavaScript في متصفحك حتى يعمل.",
    step_word="الخطوة", of="من", s1="بياناتك", s2="خبرتك", s3="خطتك", optional="(اختياري)",
    full_name="الاسم الكامل", profession="المهنة", age="العمر", age_hint="بالسنوات، بالأرقام.",
    company_name="اسم شركتك", company_website="موقع شركتك الإلكتروني",
    mobile="رقم الجوال", mobile_hint='مثال: <span dir="ltr">05XXXXXXXX</span>. من خارج السعودية؟ اكتبه مع مفتاح الدولة.',
    email="البريد الإلكتروني", next="التالي", back="السابق", submit="أرسل الاستفسار",
    experience="ما خبرتك في المطاعم والمقاهي؟",
    experience_opts=[("owner", "أملك مطعمًا أو مقهى"), ("franchisee", "أشغّل امتيازًا لعلامة أخرى"), ("both", "الاثنان معًا"),
                     ("employee", "عملت موظفًا في القطاع"), ("none", "لا خبرة سابقة"), ("other", "غير ذلك")],
    other_label="اكتب إجابتك",
    own_brand="اسم علامتك التجارية، إن وُجدت", branches_operated="عدد الفروع التي تديرها حاليًا",
    why_hippo="لماذا امتياز هيبو؟",
    branches_wanted="كم فرعًا تنوي افتتاحه؟",
    branches_wanted_opts=[("one", "فرع واحد"), ("two-to-five", "من فرعين إلى خمسة"), ("six-to-ten", "من ستة إلى عشرة"), ("other", "غير ذلك")],
    investment_source="مصدر الاستثمار",
    investment_source_opts=[("savings", "مدّخرات شخصية"), ("investors", "مستثمرون أو شركاء"), ("bank", "تمويل بنكي"), ("other", "غير ذلك")],
    investment_amount="المبلغ الذي تنوي استثماره", amount_hint="بالأرقام، بالريال السعودي.", unit="ر.س",
    start_time="متى تتوقع أن تبدأ؟",
    start_time_opts=[("now", "فورًا"), ("within-6-months", "خلال 6 أشهر"), ("6-12-months", "خلال 6 إلى 12 شهرًا"), ("1-2-years", "خلال سنة إلى سنتين")],
    target_cities="المدن التي تستهدفها",
    has_location="هل لديك موقع للمحل؟",
    has_location_opts=[("yes", "نعم، لديّ موقع"), ("searching", "لا، أبحث عن موقع"), ("undecided", "لم أحدّد بعد")],
    heard_from="كيف سمعت عن امتياز هيبو؟", choose="اختر",
    heard_opts=[("video-ad", "من إعلان الفيديو"), ("social", "من حسابات هيبو في وسائل التواصل"), ("friend", "من صديق أو أحد المعارف"),
                ("customer", "جرّبت هيبو بنفسي"), ("other", "غير ذلك")],
    notes="ملاحظات", hp="اترك هذا الحقل فارغًا",
    consent="أوافق على استخدام بياناتي للتواصل معي بخصوص هذا الاستفسار.",
    privacy_gap="[رابط إشعار الخصوصية — يُضاف عند استلامه من هيبو]",
    box_alt="بوكس الجَمعات من هيبو", done_h="وصل استفسارك.", done_p="شكرًا لك. سيتواصل معك فريق هيبو عبر بيانات التواصل التي كتبتها.",
    wa_h="بقيت خطوة واحدة.", wa_p="فتحنا لك واتساب وفيه استفسارك مكتوبًا. اضغط «إرسال» هناك حتى يصلنا.", back_form="العودة إلى النموذج",
    demo_flag="<b>مسودة — النموذج غير موصول</b> لم يُرسَل أي شيء ولم تُحفَظ بياناتك. هذا عرض لشكل الصفحة فقط.",
    demo_label="بعد ربط النموذج ستظهر للزائر هذه الرسالة:", footer="امتياز هيبو التجاري",
)

EN = dict(
    lang="en", dir="ltr", other_file="index.html", other_lang="ar", other_dir="rtl", other_name="العربية",
    title="HIPPO Franchise — Enquiry", desc="Enquiry form for the HIPPO franchise.",
    skip="Skip to the form",
    draft="<b>Draft for review</b> — the form is not connected yet. Nothing will be sent.",
    logo_alt="HIPPO Brioche Bread logo",
    masthead='<p class="label">Franchise</p>',
    photo_alt="A HIPPO brioche sandwich in its white holder",
    spot='<p class="support" lang="ar" dir="rtl">حُطّ ثقلك.</p>\n        <h1 id="campaign-line">Put your weight behind it.</h1>',
    lead="Our side of the scale is full. The other side is missing your weight. Leave your details and we'll get in touch about the HIPPO franchise.",
    h2="Franchise enquiry", intro="Three steps. Every field is required unless it says “optional”.",
    noscript="This form needs JavaScript switched on in your browser.",
    step_word="Step", of="of", s1="About you", s2="Your experience", s3="Your plan", optional="(optional)",
    full_name="Full name", profession="Profession", age="Age", age_hint="In years, in digits.",
    company_name="Your company's name", company_website="Your company's website",
    mobile="Mobile number", mobile_hint="Example: 05XXXXXXXX. Outside Saudi Arabia, include your country code.",
    email="Email", next="Next", back="Back", submit="Send enquiry",
    experience="What's your restaurant or café experience?",
    experience_opts=[("owner", "I own a restaurant or café"), ("franchisee", "I run another brand's franchise"), ("both", "Both"),
                     ("employee", "I've worked in the sector as an employee"), ("none", "No experience yet"), ("other", "Something else")],
    other_label="Tell us more",
    own_brand="Your own brand's name, if you have one", branches_operated="Branches you currently run",
    why_hippo="Why the HIPPO franchise?",
    branches_wanted="How many branches do you plan to open?",
    branches_wanted_opts=[("one", "One"), ("two-to-five", "Two to five"), ("six-to-ten", "Six to ten"), ("other", "Something else")],
    investment_source="Source of investment",
    investment_source_opts=[("savings", "Personal savings"), ("investors", "Investors or partners"), ("bank", "Bank financing"), ("other", "Something else")],
    investment_amount="Amount you plan to invest", amount_hint="In digits, in Saudi riyals.", unit="SAR",
    start_time="When do you expect to start?",
    start_time_opts=[("now", "Right away"), ("within-6-months", "Within 6 months"), ("6-12-months", "In 6 to 12 months"), ("1-2-years", "In 1 to 2 years")],
    target_cities="Cities you're targeting",
    has_location="Do you have a location for the branch?",
    has_location_opts=[("yes", "Yes, I have one"), ("searching", "No, I'm looking"), ("undecided", "Not decided yet")],
    heard_from="How did you hear about the HIPPO franchise?", choose="Choose",
    heard_opts=[("video-ad", "The video ad"), ("social", "HIPPO's social media accounts"), ("friend", "A friend or contact"),
                ("customer", "I've eaten at HIPPO"), ("other", "Somewhere else")],
    notes="Notes", hp="Leave this field empty",
    consent="I agree to my details being used to contact me about this enquiry.",
    privacy_gap="[Privacy notice link — to be added once HIPPO supplies it]",
    box_alt="A HIPPO gathering box", done_h="Your enquiry is in.", done_p="Thank you. The HIPPO team will contact you using the contact details you gave.",
    wa_h="One step left.", wa_p="We've opened WhatsApp with your enquiry written out. Press send there so it reaches us.", back_form="Back to the form",
    demo_flag="<b>Draft — form not connected</b> Nothing was sent and your details were not saved. This only shows how the page will look.",
    demo_label="Once the form is connected, visitors will see this message:", footer="Franchise",
)


def page(t):
    e = html.escape

    def lab(key, opt):
        return e(t[key]) + (f' <span class="optional">{t["optional"]}</span>' if opt else "")

    def text(name, opt=False, hint=None, cls="", attrs="", tag="input", label_key=None, wrap_id=None, hidden=False):
        d = [f"{name}-hint"] if hint else []
        d.append(f"{name}-error")
        c = f' class="{cls}"' if cls else ""
        req = "" if opt else " required"
        ctl = (f'<textarea id="{name}" name="{name}"{req} {attrs} aria-describedby="{" ".join(d)}"></textarea>' if tag == "textarea"
               else f'<input{c} type="text" id="{name}" name="{name}"{req} {attrs} aria-describedby="{" ".join(d)}">')
        if name == "investment_amount":
            ctl = f'<div class="with-unit">{ctl}<span class="unit" aria-hidden="true">{e(t["unit"])}</span></div>'
        h = f'\n          <p class="hint" id="{name}-hint">{t[hint]}</p>' if hint else ""
        wid = f' id="{wrap_id}"' if wrap_id else ""
        hid = " hidden" if hidden else ""
        return f'''        <div class="field"{wid}{hid}>
          <label for="{name}">{lab(label_key or name, opt)}</label>{h}
          {ctl}
          <p class="error" id="{name}-error" hidden></p>
        </div>
'''

    def radios(name, opt=False, other=False):
        rows = "\n".join(
            f'            <label class="choice"><input type="radio" name="{name}" value="{v}"{"" if opt or i else " required"}><span>{e(l)}</span></label>'
            for i, (v, l) in enumerate(t[name + "_opts"]))
        o = text(name + "_other", label_key="other_label", attrs='maxlength="200"', wrap_id=name + "_other-wrap", hidden=True).replace("        <div", "          <div", 1) if other else ""
        return f'''        <fieldset class="field" id="{name}-group">
          <legend id="{name}-legend">{lab(name, opt)}</legend>
          <div class="choices" role="radiogroup" id="{name}-choices" aria-labelledby="{name}-legend" aria-describedby="{name}-error"{"" if opt else ' aria-required="true"'}>
{rows}
          </div>
          <p class="error" id="{name}-error" hidden></p>
{o}        </fieldset>
'''

    heard = "\n".join(f'            <option value="{v}">{e(l)}</option>' for v, l in t["heard_opts"])
    num = 'inputmode="numeric" autocomplete="off"'

    def done(live):
        return f'''      <img class="box" src="assets/box.webp" width="640" height="680" alt="{e(t["box_alt"])}">
      <h2>{e(t["done_h"])}</h2>
      <p>{e(t["done_p"])}</p>'''

    return f'''<!DOCTYPE html>
<html lang="{t["lang"]}" dir="{t["dir"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<meta name="format-detection" content="telephone=no">
<link rel="alternate" hreflang="{t["other_lang"]}" href="{t["other_file"]}">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<a class="skip" href="#form-title">{e(t["skip"])}</a>

<p class="draft-strip" id="draft-strip">{t["draft"]}</p>

<header class="masthead">
  <a class="lang-switch" href="{t["other_file"]}" lang="{t["other_lang"]}" dir="{t["other_dir"]}" hreflang="{t["other_lang"]}">{t["other_name"]}</a>
  <img class="logo" src="assets/hippo-logo.png" width="1343" height="2127" alt="{e(t["logo_alt"])}">
  {t["masthead"]}
</header>

<main>
  <section class="stage" aria-labelledby="campaign-line">
    <div class="wall">
      <div class="hero-photo"><img src="assets/sandwich.webp" width="760" height="549" alt="{e(t["photo_alt"])}"></div>
    </div>
    <div class="floor">
      <div class="spot">
        {t["spot"]}
      </div>
      <p class="lead">{e(t["lead"])}</p>
    </div>
  </section>

  <section class="sheet" aria-labelledby="form-title">
    <div id="form-panel">
      <h2 id="form-title">{e(t["h2"])}</h2>
      <p class="intro">{e(t["intro"])}</p>
      <noscript><p>{e(t["noscript"])}</p></noscript>

      <div class="steps" id="steps" data-step="1">
        <p class="steps-text" id="steps-text" tabindex="-1"><span class="steps-count">{e(t["step_word"])} <span id="step-now">1</span> {e(t["of"])} 3</span> <span class="steps-name" id="step-name" data-s1="{e(t["s1"])}" data-s2="{e(t["s2"])}" data-s3="{e(t["s3"])}">{e(t["s1"])}</span></p>
        <div class="steps-bar" aria-hidden="true"><span></span><span></span><span></span></div>
      </div>

      <form id="enquiry-form" novalidate>
       <div class="step" id="step-1" role="group" aria-labelledby="steps-text">
{text("full_name", attrs='autocomplete="name" maxlength="120"')}{text("profession", attrs='autocomplete="organization-title" maxlength="120"')}{text("age", hint="age_hint", cls="ltr-value short", attrs=num + ' maxlength="3"')}{text("company_name", opt=True, attrs='autocomplete="organization" maxlength="160"')}{text("company_website", opt=True, cls="ltr-value", attrs='inputmode="url" autocomplete="url" autocapitalize="none" spellcheck="false" maxlength="200"')}{text("mobile", hint="mobile_hint", cls="ltr-value", attrs='inputmode="tel" autocomplete="tel" maxlength="24"').replace('type="text" id="mobile"', 'type="tel" id="mobile"')}{text("email", cls="ltr-value", attrs='inputmode="email" autocomplete="email" autocapitalize="none" spellcheck="false" maxlength="160"').replace('type="text" id="email"', 'type="email" id="email"')}
        <p class="form-alert" id="alert-1" role="alert" tabindex="-1" hidden></p>
        <div class="actions">
          <button class="submit" id="next-1" type="button" data-next="2">{e(t["next"])}</button>
        </div>
       </div>

       <div class="step" id="step-2" role="group" aria-labelledby="steps-text" hidden>
{radios("experience", other=True)}{text("own_brand", opt=True, attrs='autocomplete="off" maxlength="160"')}{text("branches_operated", opt=True, cls="ltr-value short", attrs=num + ' maxlength="5"')}{text("why_hippo", tag="textarea", attrs='rows="4" maxlength="1500"')}
        <p class="form-alert" id="alert-2" role="alert" tabindex="-1" hidden></p>
        <div class="actions">
          <button class="again back" type="button" data-prev="1">{e(t["back"])}</button>
          <button class="submit" id="next-2" type="button" data-next="3">{e(t["next"])}</button>
        </div>
       </div>

       <div class="step" id="step-3" role="group" aria-labelledby="steps-text" hidden>
{radios("branches_wanted", other=True)}{radios("investment_source", other=True)}{text("investment_amount", hint="amount_hint", cls="ltr-value", attrs=num + ' maxlength="20"')}{radios("start_time")}{text("target_cities", attrs='autocomplete="off" maxlength="300"')}{radios("has_location", opt=True)}
        <div class="field">
          <label for="heard_from">{lab("heard_from", True)}</label>
          <select id="heard_from" name="heard_from">
            <option value="">{e(t["choose"])}</option>
{heard}
          </select>
        </div>
{text("notes", opt=True, tag="textarea", attrs='rows="3" maxlength="1500"')}
        <div class="hp" aria-hidden="true">
          <label for="f-check">{e(t["hp"])}</label>
          <input type="text" id="f-check" name="f_check" tabindex="-1" autocomplete="off">
        </div>

        <div class="field">
          <div class="consent">
            <input type="checkbox" id="consent" name="consent" value="yes" required aria-describedby="consent-error">
            <label for="consent">{e(t["consent"])}</label>
          </div>
          <p class="privacy" id="privacy-slot"><span class="to-supply">{e(t["privacy_gap"])}</span></p>
          <p class="error" id="consent-error" hidden></p>
        </div>

        <p class="form-alert" id="alert-3" role="alert" tabindex="-1" hidden></p>
        <div class="actions">
          <button class="again back" id="back-btn" type="button" data-prev="2">{e(t["back"])}</button>
          <button class="submit" id="submit-btn" type="submit">{e(t["submit"])}</button>
        </div>
       </div>
      </form>
    </div>

    <!-- State: sent (only when FORM_ENDPOINT is set and the server confirmed) -->
    <div class="done" id="done-live" tabindex="-1" role="status" hidden>
{done(True)}
    </div>

    <!-- State: WhatsApp opened (only when WHATSAPP_NUMBER is set) -->
    <div class="done" id="done-whatsapp" tabindex="-1" role="status" hidden>
      <h2>{e(t["wa_h"])}</h2>
      <p>{e(t["wa_p"])}</p>
      <button class="again" type="button" data-back>{e(t["back_form"])}</button>
    </div>

    <!-- State: draft (nothing connected). Says plainly that nothing was sent. -->
    <div class="done" id="done-draft" tabindex="-1" role="status" hidden>
      <p class="demo-flag">{t["demo_flag"]}</p>
      <p class="demo-preview-label">{e(t["demo_label"])}</p>
{done(False)}
      <button class="again" type="button" data-back>{e(t["back_form"])}</button>
    </div>
  </section>
</main>

<footer class="site-footer">
  <img class="logo" src="assets/hippo-logo.png" width="1343" height="2127" alt="{e(t["logo_alt"])}" loading="lazy">
  <p>{e(t["footer"])}</p>
</footer>

<script src="js/config.js"></script>
<script src="js/form.js"></script>
</body>
</html>
'''


(SRC / "index.html").write_text(page(AR), encoding="utf-8")
(SRC / "index-en.html").write_text(page(EN), encoding="utf-8")
print("written: index.html, index-en.html")
