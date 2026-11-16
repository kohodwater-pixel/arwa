#!/usr/bin/env python3
"""Single source for the Hedaya Nouman CV set (v01 drafts).

Generates, from one data structure, so that every file carries identical facts:
  - hedaya-nouman_cv_content_ar-en_v01.md
  - 4 ATS DOCX (python-docx)
  - 4 ATS HTML (single column)  -> exported to PDF with scripts/html2pdf.cjs
  - 4 Executive HTML (two-zone) -> exported to PDF with scripts/html2pdf.cjs

Facts come only from 01-brief/brief.md. Run: python3 _work/build_cv.py
"""
import html
import pathlib
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

OUT = pathlib.Path(__file__).resolve().parent.parent
V = "v01"
EMAIL = "hedayanouman@gmail.com"
PHONE = "+966 54 093 0121"
LRM = "‎"

# ----------------------------------------------------------------------------
# Shared facts
# ----------------------------------------------------------------------------
AR = dict(
    lang="ar",
    name="هداية فخري نعمان",
    city="المدينة المنورة، المملكة العربية السعودية",
    phone_label="الجوال",
    email_label="البريد الإلكتروني",
    contact_heading="بيانات التواصل",
    city_label="المدينة",
    H=dict(summary="الملخص المهني", comp="الكفاءات الأساسية", exp="الخبرة العملية",
           edu="التعليم", train="الدورات والشهادات", vol="العمل التطوعي", lang="اللغات"),
    hospital=("أخصائية خدمة عملاء", "مستشفى الدكتور حامد سليمان الأحمدي", "يونيو 2022 – ديسمبر 2026"),
    school=("العمل الإرشادي", "الابتدائية الثانية والتسعون", "2016 – 2017"),
    reception=("موظفة استقبال", "مجموعة الدكتور نزار إبراهيم غلام الطبية", "2015"),
    edu=[["بكالوريوس إدارة الأعمال", "جامعة طيبة", "2020"],
         ["دبلوم برمجة الحاسبات", "جامعة طيبة", "2014"]],
    train=[["دورة تطوير خدمات المستفيدين", "معهد الإدارة العامة"],
           ["دورة إدارة الوقت", "معهد الإدارة العامة"],
           ["دورة القيادة الإدارية", "معهد الإدارة العامة"],
           ["شهادة مبادئ السكرتارية الإدارية"]],
    vol=[["خدمة ضيوف الرحمن", "شهادة عمل تطوعي", "40 ساعة"],
         ["برنامج «نقطة استشارة»", "32 ساعة تطوعية، وشهادة شكر وتقدير من لجنة التنمية الاجتماعية (16 ساعة)"],
         ["حملة اليوم العالمي للسكري 2018", "لجنة التنمية الاجتماعية الأهلية وجمعية المدينة المنورة الخيرية للسكري"],
         ["فعاليات اليوم العالمي للكلى", "لجنة التنمية الاجتماعية", "10 ساعات"]],
    langs=["العربية: اللغة الأم", "الإنجليزية: مستوى أساسي"],
    school_bullets=["المشاركة في العمل الإرشادي بالمدرسة والتواصل المباشر مع الطلبة.",
                    "الاستماع إلى الاحتياجات وتقديم التوجيه المناسب ضمن فريق المدرسة."],
)
EN = dict(
    lang="en",
    name="Hedaya Fakhri Nouman",
    city="Madinah, Saudi Arabia",
    phone_label="Mobile",
    email_label="Email",
    contact_heading="Contact",
    city_label="Location",
    H=dict(summary="Professional Summary", comp="Core Competencies", exp="Professional Experience",
           edu="Education", train="Training & Certifications", vol="Volunteer Experience", lang="Languages"),
    hospital=("Customer Service Specialist", "Dr. Hamed Sulaiman Al-Ahmadi Hospital", "Jun 2022 – Dec 2026"),
    school=("Student Guidance Work", "92nd Primary School", "2016 – 2017"),
    reception=("Receptionist", "Dr. Nizar Ibrahim Ghulam Medical Group", "2015"),
    edu=[["Bachelor of Business Administration", "Taibah University", "2020"],
         ["Diploma in Computer Programming", "Taibah University", "2014"]],
    train=[["Developing Beneficiary (Customer) Services", "Institute of Public Administration (IPA)"],
           ["Time Management", "Institute of Public Administration (IPA)"],
           ["Administrative Leadership", "Institute of Public Administration (IPA)"],
           ["Certificate in Principles of Administrative Secretarial Work"]],
    vol=[["Serving Pilgrims (Guests of Allah)", "Volunteer work certificate", "40 hours"],
         ["“Consultation Point” Programme", "32 volunteer hours, plus a certificate of thanks and appreciation from the Social Development Committee (16 hours)"],
         ["World Diabetes Day Campaign 2018", "Community Social Development Committee and Madinah Charitable Diabetes Society"],
         ["World Kidney Day Activities", "Social Development Committee", "10 hours"]],
    langs=["Arabic: Native", "English: Basic"],
    school_bullets=["Supported the school’s student guidance work, communicating directly with students.",
                    "Listened to students’ needs and offered appropriate guidance as part of the school team."],
)

# ----------------------------------------------------------------------------
# Model-specific copy
# ----------------------------------------------------------------------------
MODELS = {
    ("cs", "ar"): dict(
        base=AR, slug="customer-service", order=["summary", "comp", "exp", "edu", "train", "vol", "lang"],
        title="أخصائية خدمة عملاء",
        summary=("أخصائية خدمة عملاء بخبرة تزيد على أربع سنوات في خدمة المرضى والمراجعين بمستشفى الدكتور حامد "
                 "سليمان الأحمدي، وخبرة سابقة في الاستقبال بمجموعة طبية. حاصلة على بكالوريوس إدارة الأعمال من جامعة "
                 "طيبة، ودورات من معهد الإدارة العامة في تطوير خدمات المستفيدين وإدارة الوقت والقيادة الإدارية. "
                 "تتميز بوضوح التواصل والهدوء تحت ضغط العمل والالتزام بالمواعيد."),
        comp=["خدمة العملاء", "تجربة المريض والمراجع", "الرد على الاستفسارات", "التعامل مع الشكاوى والملاحظات",
              "الاستقبال والمكتب الأمامي", "مهارات التواصل", "إدارة الوقت", "العمل تحت الضغط", "العمل ضمن فريق",
              "المرونة والتكيف مع المتغيرات", "مهارات الحاسب الآلي", "الدعم الإداري"],
        hospital=["استقبال المرضى والمراجعين والإجابة عن استفساراتهم وتوجيههم إلى الجهة المختصة داخل المستشفى.",
                  "تلقي ملاحظات المراجعين وشكاواهم والتعامل معها أو رفعها إلى الجهة المعنية.",
                  "التنسيق مع أقسام المستشفى لإتمام خدمة المريض أو المراجع."],
        reception=["استقبال المراجعين والزوار عند وصولهم وتوجيههم إلى الخدمة المطلوبة.",
                   "الرد على الاستفسارات في مكتب الاستقبال بوصفه نقطة الاتصال الأولى."],
        vol_order=[0, 1, 2, 3],
    ),
    ("cs", "en"): dict(
        base=EN, slug="customer-service", order=["summary", "comp", "exp", "edu", "train", "vol", "lang"],
        title="Customer Service Specialist",
        summary=("Customer service specialist with more than four years of front-line experience serving patients and "
                 "visitors at Dr. Hamed Sulaiman Al-Ahmadi Hospital, and earlier front-desk experience as a medical group "
                 "receptionist. Holds a Bachelor of Business Administration from Taibah University and Institute of "
                 "Public Administration (IPA) training in beneficiary service development, time management and "
                 "administrative leadership. Brings clear communication, composure under pressure and dependable "
                 "punctuality to busy service environments."),
        comp=["Customer Service", "Patient & Visitor Experience", "Enquiry Handling", "Complaint Handling",
              "Front Desk & Reception", "Communication Skills", "Time Management", "Working Under Pressure",
              "Teamwork", "Adaptability", "Computer Literacy", "Administrative Support"],
        hospital=["Welcomed patients and visitors, answered their enquiries and directed them to the right department.",
                  "Received patient and visitor feedback and complaints, resolving them or referring them to the responsible team.",
                  "Coordinated with hospital departments to complete patient and visitor service requests."],
        reception=["Greeted patients and visitors on arrival and directed them to the service they needed.",
                   "Handled front-desk enquiries as the first point of contact."],
        vol_order=[0, 1, 2, 3],
    ),
    ("hs", "ar"): dict(
        base=AR, slug="hospitality", order=["summary", "comp", "exp", "vol", "train", "edu", "lang"],
        title="أخصائية خدمة ضيوف وعملاء | الهدف الوظيفي: أخصائية خدمات فندقية",
        summary=("أخصائية خدمة عملاء تتطلع إلى الانتقال إلى قطاع الضيافة والخدمات الفندقية، بخبرة تزيد على أربع سنوات "
                 "في خدمة المرضى والمراجعين بمستشفى الدكتور حامد سليمان الأحمدي، وخبرة سابقة في الاستقبال بمجموعة طبية. "
                 "أكملت 40 ساعة تطوعية في خدمة ضيوف الرحمن، ودورة تطوير خدمات المستفيدين من معهد الإدارة العامة، وتحمل "
                 "بكالوريوس إدارة الأعمال من جامعة طيبة. تنقل إلى العمل الفندقي حسن الاستقبال واللباقة في التعامل "
                 "والهدوء تحت ضغط العمل."),
        comp=["خدمة الضيوف والعملاء", "علاقات الضيوف", "استقبال الضيوف والترحيب بهم", "آداب الخدمة واللباقة",
              "الاستقبال والمكتب الأمامي", "الرد على الاستفسارات", "التعامل مع الشكاوى والملاحظات", "مهارات التواصل",
              "إدارة الوقت", "العمل تحت الضغط", "العمل ضمن فريق", "المرونة والتكيف مع المتغيرات",
              "مهارات الحاسب الآلي", "الدعم الإداري"],
        hospital=["استقبال المرضى والمراجعين والترحيب بهم وتوجيههم إلى الجهة المختصة داخل المستشفى.",
                  "الإجابة عن الاستفسارات وتقديم المعلومات اللازمة بوضوح ولباقة.",
                  "تلقي الملاحظات والشكاوى والتعامل معها أو رفعها إلى الجهة المعنية."],
        reception=["استقبال المراجعين والزوار عند وصولهم والترحيب بهم بوصفها نقطة الاتصال الأولى.",
                   "الرد على الاستفسارات في مكتب الاستقبال وتوجيه الزوار إلى الخدمة المطلوبة."],
        vol_order=[0, 1, 2, 3],
    ),
    ("hs", "en"): dict(
        base=EN, slug="hospitality", order=["summary", "comp", "exp", "vol", "train", "edu", "lang"],
        title="Guest Services Professional | Target Role: Hospitality Services Specialist",
        summary=("Guest-facing service professional seeking a first role in hospitality, with more than four years of "
                 "experience serving patients and visitors at Dr. Hamed Sulaiman Al-Ahmadi Hospital and earlier "
                 "front-desk experience as a medical group receptionist. Completed 40 volunteer hours serving pilgrims "
                 "(Guests of Allah), Institute of Public Administration (IPA) training in beneficiary service "
                 "development, and a Bachelor of Business Administration from Taibah University. Brings a warm "
                 "welcome, courteous service and composure under pressure to a hotel guest-services team."),
        comp=["Guest Services", "Guest Relations", "Guest Reception & Welcome", "Service Etiquette",
              "Front Desk & Reception", "Enquiry Handling", "Complaint Handling", "Customer Service",
              "Communication Skills", "Time Management", "Working Under Pressure", "Teamwork", "Adaptability",
              "Computer Literacy"],
        hospital=["Welcomed patients and visitors and directed them to the right department.",
                  "Answered enquiries and provided clear, courteous information.",
                  "Received feedback and complaints, resolving them or referring them to the responsible team."],
        reception=["Greeted patients and visitors on arrival as the first point of contact.",
                   "Handled front-desk enquiries and directed visitors to the service they needed."],
        vol_order=[0, 1, 2, 3],
    ),
}


def roles(m):
    b = m["base"]
    return [(b["hospital"], m["hospital"]), (b["school"], b["school_bullets"]), (b["reception"], m["reception"])]


def contact_plain(b):
    return f'{b["city"]} | {b["phone_label"]}: {PHONE} | {b["email_label"]}: {EMAIL}'


def fname(m, design, ext):
    return f'hedaya-nouman_cv_{m["slug"]}-{design}_{m["base"]["lang"]}_{V}.{ext}'


# ----------------------------------------------------------------------------
# Plain-text lines (used for the markdown and as the expected text in checks)
# ----------------------------------------------------------------------------
def md_cv(m):
    b = m["base"]
    o = [f'**{b["name"]}**  ', f'{m["title"]}  ', contact_plain(b), ""]
    for k in m["order"]:
        o.append(f'**{b["H"][k]}**')
        o.append("")
        if k == "summary":
            o.append(m["summary"])
        elif k == "comp":
            o.append(" | ".join(m["comp"]))
        elif k == "exp":
            for (t, e, d), bl in roles(m):
                o.append(f"*{t}*  ")
                o.append(f"{e} | {d}")
                o.append("")
                o += [f"- {x}" for x in bl]
                o.append("")
            o.pop()
        elif k == "edu":
            o += [f'- {" | ".join(x)}' for x in b["edu"]]
        elif k == "train":
            o += [f'- {" | ".join(x)}' for x in b["train"]]
        elif k == "vol":
            o += [f'- {" | ".join(b["vol"][i])}' for i in m["vol_order"]]
        elif k == "lang":
            o.append(" | ".join(b["langs"]))
        o.append("")
    return "\n".join(o)


# ----------------------------------------------------------------------------
# DOCX (ATS)
# ----------------------------------------------------------------------------
FONT = "Arial"
ACCENT = RGBColor(0x1F, 0x4E, 0x5F)
INK = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x40, 0x40, 0x40)
YEAR_RANGE = r"\d{4} – \d{4}"
LATIN_CHUNK = re.compile(re.escape(PHONE) + "|" + YEAR_RANGE + r"|[A-Za-z0-9][A-Za-z0-9@._]*")


def _el(parent, tag, **attrs):
    e = parent.find(qn(tag))
    if e is None:
        e = OxmlElement(tag)
        parent.append(e)
    for k, v in attrs.items():
        e.set(qn(k), v)
    return e


def style_run(run, size, bold=False, color=INK, rtl=False):
    rpr = run._r.get_or_add_rPr()
    for child in list(rpr):
        rpr.remove(child)
    # children appended in schema order: rFonts, b, bCs, i, iCs, color, sz, szCs, rtl, lang
    f = OxmlElement("w:rFonts")
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        f.set(qn(a), FONT)
    rpr.append(f)
    for tag in ("w:b", "w:bCs"):
        e = OxmlElement(tag); e.set(qn("w:val"), "1" if bold else "0"); rpr.append(e)
    for tag in ("w:i", "w:iCs"):
        e = OxmlElement(tag); e.set(qn("w:val"), "0"); rpr.append(e)
    c = OxmlElement("w:color"); c.set(qn("w:val"), str(color)); rpr.append(c)
    for tag in ("w:sz", "w:szCs"):
        e = OxmlElement(tag); e.set(qn("w:val"), str(int(size * 2))); rpr.append(e)
    if rtl:
        rpr.append(OxmlElement("w:rtl"))
        lang = OxmlElement("w:lang"); lang.set(qn("w:val"), "ar-SA"); lang.set(qn("w:bidi"), "ar-SA"); rpr.append(lang)
    else:
        lang = OxmlElement("w:lang"); lang.set(qn("w:val"), "en-GB"); rpr.append(lang)


def add_par(doc, text, style, size, rtl, bold=False, color=INK, before=0, after=0, keep=False):
    p = doc.add_paragraph(style=style)
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(before), Pt(after)
    pf.line_spacing = 1.15 if rtl else 1.1
    if keep:
        pf.keep_with_next = True
    ppr = p._p.get_or_add_pPr()
    if rtl:
        # True RTL paragraph. No w:jc on purpose: in a bidi paragraph Word treats "left" as the
        # leading (right) edge, so an explicit jc=right would flip the text to the LEFT margin.
        bidi = OxmlElement("w:bidi")
        ppr.insert_element_before(bidi, "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind", "w:contextualSpacing",
                                  "w:mirrorIndents", "w:suppressOverlap", "w:jc", "w:textDirection", "w:textAlignment",
                                  "w:textboxTightWrap", "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr",
                                  "w:pPrChange")
        pos = 0
        for mt in LATIN_CHUNK.finditer(text):
            if mt.start() > pos:
                style_run(p.add_run(text[pos:mt.start()]), size, bold, color, rtl=True)
            chunk = mt.group(0)
            # digits, e-mail and phone stay left-to-right runs with Western digits; LRM keeps "+" in front
            style_run(p.add_run((LRM + chunk) if (chunk == PHONE or " " in chunk) else chunk), size, bold, color, rtl=False)
            pos = mt.end()
        if pos < len(text):
            style_run(p.add_run(text[pos:]), size, bold, color, rtl=True)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        style_run(p.add_run(text), size, bold, color)
    return p


def build_docx(m, path):
    b = m["base"]
    rtl = b["lang"] == "ar"
    body = 10.5 if rtl else 10
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(18)
    sec.top_margin = sec.bottom_margin = Mm(13)
    if rtl:
        sec._sectPr.append(OxmlElement("w:bidi"))
    # document defaults / Normal: same font for Latin and complex script
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(body)
    rpr = normal.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), FONT)
    _el(rpr, "w:szCs", **{"w:val": str(int(body * 2))})
    doc.core_properties.title = f'{b["name"]} | {m["title"]}'
    doc.core_properties.author = b["name"]
    doc.core_properties.language = "ar-SA" if rtl else "en-GB"

    add_par(doc, b["name"], "Heading 1", 20, rtl, bold=True, color=ACCENT, after=2)
    add_par(doc, m["title"], "Normal", 12, rtl, bold=True, color=GREY, after=2)
    add_par(doc, contact_plain(b), "Normal", body, rtl, after=4)

    def h2(k):
        add_par(doc, b["H"][k], "Heading 2", 12.5, rtl, bold=True, color=ACCENT, before=7, after=2, keep=True)

    def bullets(items):
        for x in items:
            add_par(doc, x, "List Bullet", body, rtl, after=1)

    for k in m["order"]:
        h2(k)
        if k == "summary":
            add_par(doc, m["summary"], "Normal", body, rtl)
        elif k == "comp":
            add_par(doc, " | ".join(m["comp"]), "Normal", body, rtl)
        elif k == "exp":
            for i, ((t, e, d), bl) in enumerate(roles(m)):
                add_par(doc, t, "Heading 3", body + 0.5, rtl, bold=True, before=4 if i else 1, keep=True)
                add_par(doc, f"{e} | {d}", "Normal", body, rtl, color=GREY, after=2, keep=True)
                bullets(bl)
        elif k == "edu":
            bullets([" | ".join(x) for x in b["edu"]])
        elif k == "train":
            bullets([" | ".join(x) for x in b["train"]])
        elif k == "vol":
            bullets([" | ".join(b["vol"][i]) for i in m["vol_order"]])
        elif k == "lang":
            add_par(doc, " | ".join(b["langs"]), "Normal", body, rtl)
    doc.save(path)


# ----------------------------------------------------------------------------
# HTML helpers
# ----------------------------------------------------------------------------
FONTS = "../../../../assets/fonts"
FACES = "".join(
    f"@font-face{{font-family:'IBM Plex Sans';font-weight:{w};src:url('{FONTS}/ibmplexsans-static/IBMPlexSans-{n}.ttf') format('truetype');}}\n"
    for w, n in ((400, "Regular"), (500, "Medium"), (600, "SemiBold"))
) + "".join(
    f"@font-face{{font-family:'Tajawal';font-weight:{w};src:url('{FONTS}/tajawal/Tajawal-{n}.ttf') format('truetype');}}\n"
    for w, n in ((400, "Regular"), (500, "Medium"), (700, "Bold"))
)
E = html.escape


def phone_html():
    return f'<span class="ltr" dir="ltr">{PHONE}</span>'


def head(m, css):
    b = m["base"]
    rtl = b["lang"] == "ar"
    return (f'<!DOCTYPE html>\n<html lang="{b["lang"]}" dir="{"rtl" if rtl else "ltr"}">\n<head>\n<meta charset="utf-8">\n'
            f'<title>{E(b["name"])} | {E(m["title"])}</title>\n<style>\n{FACES}{css}</style>\n</head>\n')


def D(d):
    """Dates: a pure year range is isolated left-to-right so it shows and extracts as 2016 – 2017."""
    return re.sub("(" + YEAR_RANGE + ")", r'<span class="ltr" dir="ltr">\1</span>', E(d))


def joined(parts):
    return E(" | ".join(parts))


# ----------------------------------------------------------------------------
# ATS HTML (single column, no tables, no graphics)
# ----------------------------------------------------------------------------
ATS_CSS = """@page{size:A4;margin:12mm 18mm 11mm;}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{font-family:'IBM Plex Sans',sans-serif;font-size:9.9pt;line-height:1.37;color:#1a1a1a;}
html[lang=ar] body{font-family:'Tajawal',sans-serif;font-size:10.1pt;line-height:1.6;}
html[lang=ar] li{margin-bottom:.5pt;}
html[lang=ar] h1,html[lang=ar] h2,html[lang=ar] h3,html[lang=ar] .title{font-weight:700;}
.ltr{unicode-bidi:isolate;}
h1{font-size:20pt;font-weight:600;color:#1f4e5f;margin:0;line-height:1.25;}
html[lang=ar] h1{font-size:20pt;line-height:1.45;}
.title{font-size:12pt;font-weight:600;color:#404040;margin:1pt 0 2pt;}
.contact{margin:0 0 4pt;}
h2{font-size:12pt;font-weight:600;color:#1f4e5f;margin:8pt 0 2pt;break-after:avoid;}
html[lang=ar] h2{margin:5pt 0 0;}
h3{font-size:10.5pt;font-weight:600;margin:5pt 0 0;break-after:avoid;}
html[lang=ar] h3{font-size:11pt;margin-top:3pt;}
h2 + h3{margin-top:1pt;}
p{margin:0;}
p,li{text-wrap:pretty;}
.meta{color:#404040;margin-bottom:2pt;break-after:avoid;}
ul{margin:0;padding-inline-start:15pt;}
li{margin:0 0 1.5pt;break-inside:avoid;}
"""


def build_ats_html(m, path):
    b = m["base"]
    o = [head(m, ATS_CSS), "<body>",
         f'<h1>{E(b["name"])}</h1>',
         f'<p class="title">{E(m["title"])}</p>',
         f'<p class="contact">{E(b["city"])} | {E(b["phone_label"])}: {phone_html()} | {E(b["email_label"])}: <span class="ltr" dir="ltr">{EMAIL}</span></p>']

    def ul(items):
        o.append("<ul>")
        o.extend(f"<li>{x}</li>" for x in items)
        o.append("</ul>")

    for k in m["order"]:
        o.append(f'<h2>{E(b["H"][k])}</h2>')
        if k == "summary":
            o.append(f'<p>{E(m["summary"])}</p>')
        elif k == "comp":
            o.append(f'<p>{joined(m["comp"])}</p>')
        elif k == "exp":
            for (t, e, d), bl in roles(m):
                o.append(f"<h3>{E(t)}</h3>")
                o.append(f'<p class="meta">{E(e)} | {D(d)}</p>')
                ul([E(x) for x in bl])
        elif k == "edu":
            ul([joined(x) for x in b["edu"]])
        elif k == "train":
            ul([joined(x) for x in b["train"]])
        elif k == "vol":
            ul([joined(b["vol"][i]) for i in m["vol_order"]])
        elif k == "lang":
            o.append(f'<p>{joined(b["langs"])}</p>')
    o.append("</body>\n</html>\n")
    path.write_text("\n".join(o), encoding="utf-8")


# ----------------------------------------------------------------------------
# Executive Modern HTML (two zones: side column at the start edge, main column)
# ----------------------------------------------------------------------------
EXEC_CSS = """@page{size:A4;margin:0;}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
:root{--accent:#1f5a63;--ink:#20282b;--muted:#5a666a;--line:#cfd9db;}
body{font-family:'IBM Plex Sans',sans-serif;font-size:9.2pt;line-height:1.48;color:var(--ink);}
html[lang=ar] body{font-family:'Tajawal',sans-serif;font-size:9.7pt;line-height:1.6;}
html[lang=ar] h1,html[lang=ar] h2,html[lang=ar] h3{font-weight:700;}
html[lang=ar] main ul.rows .a{font-weight:700;}
.ltr{unicode-bidi:isolate;}
.page{width:210mm;height:296.6mm;padding:15mm 17mm 12mm;display:grid;grid-template-rows:auto 1fr;break-inside:avoid;}
header{padding-bottom:5mm;border-bottom:.6pt solid var(--accent);margin-bottom:6.5mm;}
h1{font-size:25pt;font-weight:600;color:var(--accent);margin:0;line-height:1.15;}
html[lang=ar] h1{font-size:26pt;line-height:1.4;}
.title{font-size:11.5pt;font-weight:500;color:var(--muted);margin:1.6mm 0 0;}
html[lang=ar] .title{font-size:12pt;margin-top:0;}
.grid{display:grid;grid-template-columns:58mm 1fr;column-gap:9mm;min-height:0;}
aside{border-inline-end:.6pt solid var(--line);padding-inline-end:7mm;}
section{margin:0 0 5.4mm;}
section:last-child{margin-bottom:0;}
h2{font-size:8.3pt;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:.07em;margin:0 0 2.4mm;break-after:avoid;}
html[lang=ar] h2{font-size:11.2pt;letter-spacing:0;text-transform:none;margin-bottom:1.2mm;}
html[lang=ar] aside li{margin-bottom:.9mm;}
html[lang=ar] aside .contact li{margin-bottom:1.4mm;}
html[lang=ar] aside .stack li{margin-bottom:1.8mm;}
p{margin:0;}
p,li{text-wrap:pretty;}
ul{margin:0;padding:0;list-style:none;}
.cap{display:block;font-size:.86em;color:var(--muted);}
aside li{margin:0 0 1.5mm;}
aside li:last-child{margin-bottom:0;}
aside .contact li{margin-bottom:2mm;}
aside .stack li{margin-bottom:2.4mm;}
aside .stack .a{display:block;font-weight:500;}
aside .stack .b{display:block;color:var(--muted);font-size:.93em;}
.sep{color:var(--muted);}
aside .sep{display:none;}
main .role{margin:0 0 3.4mm;break-inside:avoid;}
main .role:last-child{margin-bottom:0;}
.rh{display:flex;justify-content:space-between;align-items:baseline;gap:5mm;}
h3{font-size:10.6pt;font-weight:600;margin:0;}
html[lang=ar] h3{font-size:10.8pt;}
.date{font-size:.92em;color:var(--muted);white-space:nowrap;}
.org{color:var(--accent);font-weight:500;margin-bottom:1.1mm;}
main ul.b{padding-inline-start:4mm;list-style:disc;}
main ul.b li{margin:0 0 .9mm;padding-inline-start:.6mm;}
main ul.b li::marker{color:var(--accent);font-size:.8em;}
main ul.rows li{margin:0 0 1.9mm;}
main ul.rows li:last-child{margin-bottom:0;}
main ul.rows .a{font-weight:600;}
main ul.rows .b{color:var(--muted);}
"""


def parts_html(parts):
    a = f'<span class="a">{E(parts[0])}</span>'
    if len(parts) == 1:
        return a
    return a + ' <span class="sep">|</span> ' + f'<span class="b">{E(" | ".join(parts[1:]))}</span>'


def build_exec_html(m, path):
    b = m["base"]
    H = b["H"]
    side_keys = ["comp", "train", "lang"]
    o = [head(m, EXEC_CSS), '<body>\n<div class="page">',
         f'<header>\n<h1>{E(b["name"])}</h1>\n<p class="title">{E(m["title"])}</p>\n</header>',
         '<div class="grid">', "<aside>",
         f'<section>\n<h2>{E(b["contact_heading"])}</h2>\n<ul class="contact">',
         f'<li><span class="cap">{E(b["city_label"])}</span>{E(b["city"])}</li>',
         f'<li><span class="cap">{E(b["phone_label"])}</span>{phone_html()}</li>',
         f'<li><span class="cap">{E(b["email_label"])}</span><span class="ltr" dir="ltr">{EMAIL}</span></li>',
         "</ul>\n</section>"]
    for k in [x for x in m["order"] if x in side_keys]:
        o.append(f"<section>\n<h2>{E(H[k])}</h2>")
        if k == "comp":
            o.append("<ul>" + "".join(f"<li>{E(x)}</li>" for x in m["comp"]) + "</ul>")
        elif k == "train":
            o.append('<ul class="stack">' + "".join(f"<li>{parts_html(x)}</li>" for x in b["train"]) + "</ul>")
        elif k == "lang":
            o.append("<ul>" + "".join(f"<li>{E(x)}</li>" for x in b["langs"]) + "</ul>")
        o.append("</section>")
    o.append("</aside>\n<main>")
    for k in [x for x in m["order"] if x not in side_keys]:
        o.append(f"<section>\n<h2>{E(H[k])}</h2>")
        if k == "summary":
            o.append(f'<p>{E(m["summary"])}</p>')
        elif k == "exp":
            for (t, e, d), bl in roles(m):
                o.append('<div class="role">')
                o.append(f'<div class="rh"><h3>{E(t)}</h3><span class="date">{D(d)}</span></div>')
                o.append(f'<p class="org">{E(e)}</p>')
                o.append('<ul class="b">' + "".join(f"<li>{E(x)}</li>" for x in bl) + "</ul>")
                o.append("</div>")
        elif k == "edu":
            o.append('<ul class="rows">' + "".join(f"<li>{parts_html(x)}</li>" for x in b["edu"]) + "</ul>")
        elif k == "vol":
            o.append('<ul class="rows">' + "".join(f"<li>{parts_html(b['vol'][i])}</li>" for i in m["vol_order"]) + "</ul>")
        o.append("</section>")
    o.append("</main>\n</div>\n</div>\n</body>\n</html>\n")
    path.write_text("\n".join(o), encoding="utf-8")


# ----------------------------------------------------------------------------
if __name__ == "__main__":
    for key, m in MODELS.items():
        build_docx(m, OUT / fname(m, "ats", "docx"))
        build_ats_html(m, OUT / fname(m, "ats", "html"))
        build_exec_html(m, OUT / fname(m, "executive", "html"))
        (OUT / "_work" / f"cvtext_{key[0]}_{key[1]}.md").write_text(md_cv(m), encoding="utf-8")
        print("built", key)
