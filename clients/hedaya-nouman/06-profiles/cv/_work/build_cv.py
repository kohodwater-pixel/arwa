#!/usr/bin/env python3
"""Single source for the Hedaya Nouman CV set — v02 drafts.

Generates, from one data structure, so that every file carries identical facts:
  - 4 ATS DOCX (python-docx)
  - 4 ATS HTML (single column)  -> exported to PDF with scripts/html2pdf.cjs
  - 4 Executive HTML (two zones) -> exported to PDF with scripts/html2pdf.cjs
(the content markdown is written by write_content.py from the same data)

Facts come only from 01-brief/brief.md, including the "Client answers" section.
Run: bash _work/export.sh
"""
import datetime
import html
import pathlib
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

OUT = pathlib.Path(__file__).resolve().parent.parent
V = "v02"
EMAIL = "hedayanouman@gmail.com"
PHONE = "+966 54 093 0121"
TEAL = "1F5A63"      # the one teal of the set
SAND = "C9A86A"      # warm accent: rules and small details only
SAND_LIGHT = "ECDCB6"  # title line on the teal band
PAGE_BREAK_BEFORE = {("cs", "ar"): "edu", ("cs", "en"): "edu", ("hs", "ar"): "vol", ("hs", "en"): "vol"}  # (model, lang) -> section key that starts page 2 in the ATS files

# ----------------------------------------------------------------------------
# Shared facts
# ----------------------------------------------------------------------------
AR = dict(
    lang="ar",
    name="هداية فخري نعمان",
    city="المدينة المنورة، المملكة العربية السعودية",
    nat_label="الجنسية", nat="سعودية",
    phone_label="الجوال", email_label="البريد الإلكتروني",
    contact_heading="بيانات التواصل", city_label="المدينة",
    H=dict(summary="الملخص المهني", comp="الكفاءات الأساسية", tech="المهارات التقنية", exp="الخبرة العملية",
           edu="التعليم", train="الدورات والشهادات", vol="العمل التطوعي", lang="اللغات"),
    hospital=("أخصائية خدمة عملاء – الخدمات الفندقية وخدمات الغرف", "مستشفى الدكتور حامد سليمان الأحمدي",
              "يونيو 2022 إلى ديسمبر 2026"),
    school=("منسقة إدارية", "الابتدائية الثانية والتسعون", "2016 إلى 2017"),
    reception=("موظفة استقبال", "مجموعة الدكتور نزار إبراهيم غلام الطبية", "2015"),
    school_bullets=["تنسيق الأعمال الإدارية في المدرسة ومتابعتها.",
                    "تقديم الدعم الإداري لإدارة المدرسة ومنسوبيها."],
    reception_bullets=["استقبال المراجعين والزوار عند وصولهم وتوجيههم إلى الخدمة المطلوبة.",
                       "الرد على الاستفسارات في مكتب الاستقبال بوصفه نقطة الاتصال الأولى."],
    tech=["نظام معلومات المستشفى", "Microsoft Excel"],
    edu=[["بكالوريوس إدارة الأعمال", "جامعة طيبة", "2020"],
         ["دبلوم برمجة الحاسبات", "جامعة طيبة", "2014"]],
    train=[["دورة تطوير خدمات المستفيدين", "معهد الإدارة العامة", "2020"],
           ["دورة إدارة الوقت", "معهد الإدارة العامة", "2020"],
           ["دورة القيادة الإدارية", "معهد الإدارة العامة", "2020"],
           ["شهادة مبادئ السكرتارية الإدارية", "2020"]],
    vol=[["خدمة ضيوف الرحمن", "شهادة عمل تطوعي", "40 ساعة"],
         ["برنامج «نقطة استشارة»", "32 ساعة تطوعية، وشهادة شكر وتقدير من لجنة التنمية الاجتماعية (16 ساعة)"],
         ["حملة اليوم العالمي للسكري 2018", "لجنة التنمية الاجتماعية الأهلية وجمعية المدينة المنورة الخيرية للسكري"],
         ["فعاليات اليوم العالمي للكلى", "لجنة التنمية الاجتماعية", "10 ساعات"]],
    langs=["العربية: اللغة الأم", "الإنجليزية: مستوى أساسي"],
)
EN = dict(
    lang="en",
    name="Hedaya Fakhri Nouman",
    city="Madinah, Saudi Arabia",
    nat_label="Nationality", nat="Saudi",
    phone_label="Mobile", email_label="Email",
    contact_heading="Contact", city_label="Location",
    H=dict(summary="Professional Summary", comp="Core Competencies", tech="Technical Skills",
           exp="Professional Experience", edu="Education", train="Training & Certifications",
           vol="Volunteer Experience", lang="Languages"),
    hospital=("Customer Service Specialist – Hospitality & Room Services", "Dr. Hamed Sulaiman Al-Ahmadi Hospital",
              "Jun 2022 – Dec 2026"),
    school=("Administrative Coordinator", "92nd Primary School", "2016 – 2017"),
    reception=("Receptionist", "Dr. Nizar Ibrahim Ghulam Medical Group", "2015"),
    school_bullets=["Coordinated and followed up the school’s administrative work.",
                    "Provided administrative support to the school’s management and staff."],
    reception_bullets=["Greeted patients and visitors on arrival and directed them to the service they needed.",
                       "Handled front-desk enquiries as the first point of contact."],
    tech=["Hospital information system", "Microsoft Excel"],
    edu=[["Bachelor of Business Administration", "Taibah University", "2020"],
         ["Diploma in Computer Programming", "Taibah University", "2014"]],
    train=[["Developing Beneficiary (Customer) Services", "Institute of Public Administration (IPA)", "2020"],
           ["Time Management", "Institute of Public Administration (IPA)", "2020"],
           ["Administrative Leadership", "Institute of Public Administration (IPA)", "2020"],
           ["Certificate in Principles of Administrative Secretarial Work", "2020"]],
    vol=[["Serving Pilgrims (Duyuf Al-Rahman)", "Volunteer work certificate", "40 hours"],
         ["“Consultation Point” Programme", "32 volunteer hours, plus a certificate of appreciation from the Social Development Committee (16 hours)"],
         ["World Diabetes Day Campaign 2018", "Community Social Development Committee and Madinah Charitable Diabetes Society"],
         ["World Kidney Day Activities", "Social Development Committee", "10 hours"]],
    langs=["Arabic: Native", "English: Basic"],
)

# Competency sets: identical in both languages per model, same order, four per line.
COMP = {
    "cs": {
        "en": [["Customer Service", "Patient & Visitor Service", "Enquiry Handling", "Complaint Handling"],
               ["Team Leadership", "New Staff Training", "Hospitality Services in Healthcare", "Room Services"],
               ["Front Desk & Reception", "Administrative Coordination", "Communication Skills", "Time Management"],
               ["Working Under Pressure", "Teamwork", "Adaptability", "Computer Literacy"]],
        "ar": [["خدمة العملاء", "خدمة المرضى والمراجعين", "الرد على الاستفسارات", "التعامل مع الشكاوى"],
               ["قيادة الفريق", "تدريب الموظفات الجديدات", "الخدمات الفندقية في القطاع الصحي", "خدمات الغرف"],
               ["الاستقبال والمكتب الأمامي", "التنسيق الإداري", "مهارات التواصل", "إدارة الوقت"],
               ["العمل تحت الضغط", "العمل ضمن فريق", "المرونة والتكيف", "مهارات الحاسب الآلي"]],
    },
    "hs": {
        "en": [["Hospitality Services in Healthcare", "Room Services", "Guest Services", "Guest Reception & Welcome"],
               ["Team Leadership", "New Staff Training", "Service Etiquette", "Customer Service"],
               ["Enquiry Handling", "Complaint Handling", "Front Desk & Reception", "Communication Skills"],
               ["Time Management", "Working Under Pressure", "Teamwork", "Adaptability"]],
        "ar": [["الخدمات الفندقية في القطاع الصحي", "خدمات الغرف", "خدمة الضيوف", "استقبال الضيوف والترحيب بهم"],
               ["قيادة الفريق", "تدريب الموظفات الجديدات", "آداب الخدمة واللباقة", "خدمة العملاء"],
               ["الرد على الاستفسارات", "التعامل مع الشكاوى", "الاستقبال والمكتب الأمامي", "مهارات التواصل"],
               ["إدارة الوقت", "العمل تحت الضغط", "العمل ضمن فريق", "المرونة والتكيف"]],
    },
}

# ----------------------------------------------------------------------------
# Model-specific copy
# ----------------------------------------------------------------------------
CS_ORDER = ["summary", "comp", "tech", "exp", "edu", "train", "vol", "lang"]
HS_ORDER = ["summary", "comp", "tech", "exp", "vol", "train", "edu", "lang"]
MODELS = {
    ("cs", "ar"): dict(
        base=AR, slug="customer-service", order=CS_ORDER, comp=COMP["cs"]["ar"],
        title=["أخصائية خدمة عملاء"],
        summary=("أخصائية خدمة عملاء بخبرة تزيد على أربع سنوات في مستشفى الدكتور حامد سليمان الأحمدي ضمن الخدمات "
                 "الفندقية وخدمات الغرف، شملت قيادة فريق العمل وتدريب الموظفات الجديدات وخدمة المرضى والمراجعين، مع خبرة "
                 "سابقة في التنسيق الإداري والاستقبال. حاصلة على بكالوريوس إدارة الأعمال من جامعة طيبة، ودورات من معهد "
                 "الإدارة العامة في تطوير خدمات المستفيدين وإدارة الوقت والقيادة الإدارية."),
        hospital=["قيادة فريق العمل في الخدمات الفندقية وخدمات الغرف بالمستشفى.",
                  "تدريب الموظفات الجديدات على مهام العمل.",
                  "استقبال استفسارات المرضى والمراجعين، وتسجيل ملاحظاتهم وشكاواهم وإحالتها إلى الجهة المعنية.",
                  "تقديم الخدمات الفندقية وخدمات الغرف للمرضى داخل المستشفى.",
                  "استخدام نظام معلومات المستشفى وبرنامج Microsoft Excel في إنجاز مهام العمل."],
    ),
    ("cs", "en"): dict(
        base=EN, slug="customer-service", order=CS_ORDER, comp=COMP["cs"]["en"],
        title=["Customer Service Specialist"],
        summary=("Customer service specialist with more than four years at Dr. Hamed Sulaiman Al-Ahmadi Hospital, "
                 "working in its hospitality and room services: leading the work team, training new staff and "
                 "serving patients and visitors. Earlier experience in administrative coordination and front-desk "
                 "reception. Holds a Bachelor of Business Administration from Taibah University and completed "
                 "Institute of Public Administration (IPA) courses in beneficiary service development, time "
                 "management and administrative leadership."),
        hospital=["Led the work team in the hospital’s hospitality and room services.",
                  "Trained new female employees in their duties.",
                  "Handled patient and visitor enquiries; recorded feedback and complaints and referred them to the responsible team.",
                  "Delivered hospitality and room services to hospital patients.",
                  "Used the hospital information system and Microsoft Excel to carry out work tasks."],
    ),
    ("hs", "ar"): dict(
        base=AR, slug="hospitality", order=HS_ORDER, comp=COMP["hs"]["ar"],
        title=["أخصائية خدمة عملاء – الخدمات الفندقية وخدمات الغرف", "الهدف الوظيفي: أخصائية خدمات فندقية"],
        summary=("أخصائية خدمة عملاء بخبرة تزيد على أربع سنوات في تقديم الخدمات الفندقية وخدمات الغرف داخل مستشفى "
                 "الدكتور حامد سليمان الأحمدي، شملت قيادة فريق العمل وتدريب الموظفات الجديدات. أكملت 40 ساعة تطوعية في "
                 "خدمة ضيوف الرحمن، ودورة تطوير خدمات المستفيدين من معهد الإدارة العامة، وتحمل بكالوريوس إدارة الأعمال "
                 "من جامعة طيبة. تتطلع إلى توظيف هذه الخبرة في قطاع الضيافة والفنادق."),
        hospital=["قيادة فريق العمل في الخدمات الفندقية وخدمات الغرف بالمستشفى.",
                  "تدريب الموظفات الجديدات على مهام العمل.",
                  "تقديم الخدمات الفندقية وخدمات الغرف للمرضى داخل المستشفى.",
                  "استقبال استفسارات المرضى والمراجعين، وتسجيل ملاحظاتهم وشكاواهم وإحالتها إلى الجهة المعنية.",
                  "استخدام نظام معلومات المستشفى وبرنامج Microsoft Excel في إنجاز مهام العمل."],
    ),
    ("hs", "en"): dict(
        base=EN, slug="hospitality", order=HS_ORDER, comp=COMP["hs"]["en"],
        title=["Customer Service Specialist – Hospitality & Room Services", "Target Role: Hospitality Services Specialist"],
        summary=("Customer service specialist with more than four years delivering hospitality and room services in "
                 "a hospital setting at Dr. Hamed Sulaiman Al-Ahmadi Hospital, including leading the work team and "
                 "training new staff. Completed 40 volunteer hours serving pilgrims (Duyuf Al-Rahman), an Institute "
                 "of Public Administration (IPA) course in beneficiary service development, and a Bachelor of "
                 "Business Administration at Taibah University. Seeking to bring this experience to a role in the "
                 "hospitality sector."),
        hospital=["Led the work team in the hospital’s hospitality and room services.",
                  "Trained new female employees in their duties.",
                  "Delivered hospitality and room services to hospital patients.",
                  "Handled patient and visitor enquiries; recorded feedback and complaints and referred them to the responsible team.",
                  "Used the hospital information system and Microsoft Excel to carry out work tasks."],
    ),
}
DOT = " · "


def roles(m):
    b = m["base"]
    return [(b["hospital"], m["hospital"]), (b["school"], b["school_bullets"]), (b["reception"], b["reception_bullets"])]


def contact_lines(b):
    """Arabic: one label, then e-mail and phone together. The e-mail's Latin letters make the phone that
    follows read left to right in any renderer, so no bidi control character is needed."""
    line1 = f'{b["city"]} | {b["nat_label"]}: {b["nat"]}'
    if b["lang"] == "ar":
        return [line1, f'{b["email_label"]} و{b["phone_label"]}: {EMAIL} | {PHONE}']
    return [line1, f'{b["phone_label"]}: {PHONE} | {b["email_label"]}: {EMAIL}']


def fname(m, design, ext):
    return f'hedaya-nouman_cv_{m["slug"]}-{design}_{m["base"]["lang"]}_{V}.{ext}'


def key_of(m):
    return next(k for k, v in MODELS.items() if v is m)


# ----------------------------------------------------------------------------
# Plain text (markdown) — also the expected text in verify.py
# ----------------------------------------------------------------------------
def md_cv(m):
    b = m["base"]
    o = [f'**{b["name"]}**  '] + [f"{t}  " for t in m["title"]] + [f"{c}  " for c in contact_lines(b)]
    o[-1] = o[-1].rstrip()
    o.append("")
    for k in m["order"]:
        o += [f'**{b["H"][k]}**', ""]
        if k == "summary":
            o.append(m["summary"])
        elif k == "comp":
            o += [DOT.join(row) + "  " for row in m["comp"]]
            o[-1] = o[-1].rstrip()
        elif k == "tech":
            o.append(DOT.join(b["tech"]))
        elif k == "exp":
            for (t, e, d), bl in roles(m):
                o += [f"*{t}*  ", f"{e} | {d}", ""] + [f"- {x}" for x in bl] + [""]
            o.pop()
        elif k in ("edu", "train", "vol"):
            o += [f'- {" | ".join(x)}' for x in b[k]]
        elif k == "lang":
            o.append(" | ".join(b["langs"]))
        o.append("")
    return "\n".join(o)


# ----------------------------------------------------------------------------
# DOCX (ATS): single column, real headings and bullets; polish = paragraph shading and borders only
# ----------------------------------------------------------------------------
FONT = "Arial"
C_TEAL, C_INK, C_GREY = RGBColor.from_string(TEAL), RGBColor(0x1A, 0x1A, 0x1A), RGBColor(0x40, 0x40, 0x40)
C_WHITE, C_SANDL = RGBColor(0xFF, 0xFF, 0xFF), RGBColor.from_string(SAND_LIGHT)
# Latin chunk inside Arabic text: the phone, or Latin words/digits (words joined by single spaces: "Microsoft Excel")
LATIN_CHUNK = re.compile(re.escape(f"{EMAIL} | {PHONE}") + "|" + re.escape(PHONE) + r"|[A-Za-z0-9][A-Za-z0-9@._]*(?: [A-Za-z][A-Za-z0-9@._]*)*")
PPR_ORDER = ["w:pStyle", "w:keepNext", "w:keepLines", "w:pageBreakBefore", "w:framePr", "w:widowControl", "w:numPr",
             "w:suppressLineNumbers", "w:pBdr", "w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
             "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN", "w:bidi", "w:adjustRightInd",
             "w:snapToGrid", "w:spacing", "w:ind", "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap",
             "w:jc", "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl", "w:divId",
             "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange"]


def ppr_add(p, el):
    """Insert a pPr child at its schema position."""
    ppr = p._p.get_or_add_pPr()
    for old in ppr.findall(qn(el.tag.replace("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}", "w:"))):
        ppr.remove(old)
    tag = "w:" + el.tag.split("}")[1]
    ppr.insert_element_before(el, *PPR_ORDER[PPR_ORDER.index(tag) + 1:])


def border(sides):
    """sides: {side: (size_eighths_pt, space_pt, colour)}"""
    bdr = OxmlElement("w:pBdr")
    for side in ("top", "left", "bottom", "right"):
        if side in sides:
            sz, space, colour = sides[side]
            e = OxmlElement(f"w:{side}")
            for a, v in (("w:val", "single"), ("w:sz", str(sz)), ("w:space", str(space)), ("w:color", colour)):
                e.set(qn(a), v)
            bdr.append(e)
    return bdr


def shade(colour):
    s = OxmlElement("w:shd")
    for a, v in (("w:val", "clear"), ("w:color", "auto"), ("w:fill", colour)):
        s.set(qn(a), v)
    return s


def style_run(run, size, bold=False, color=C_INK, rtl=False):
    rpr = run._r.get_or_add_rPr()
    for child in list(rpr):
        rpr.remove(child)
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
        e = OxmlElement(tag); e.set(qn("w:val"), str(int(round(size * 2)))); rpr.append(e)
    if rtl:
        rpr.append(OxmlElement("w:rtl"))
        lang = OxmlElement("w:lang"); lang.set(qn("w:val"), "ar-SA"); lang.set(qn("w:bidi"), "ar-SA"); rpr.append(lang)
    else:
        lang = OxmlElement("w:lang"); lang.set(qn("w:val"), "en-GB"); rpr.append(lang)


def add_par(doc, text, style, size, rtl, bold=False, color=C_INK, before=0, after=0, keep=False, line=None):
    p = doc.add_paragraph(style=style)
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(before), Pt(after)
    pf.line_spacing = line or (1.2 if rtl else 1.12)
    if keep:
        pf.keep_with_next = True
    if rtl:
        # True RTL paragraph. No w:jc on purpose: in a bidi paragraph the start edge is the right.
        ppr_add(p, OxmlElement("w:bidi"))
        pos = 0
        for mt in LATIN_CHUNK.finditer(text):
            if mt.start() > pos:
                style_run(p.add_run(text[pos:mt.start()]), size, bold, color, rtl=True)
            # digits, Latin words, e-mail and phone are left-to-right runs (Western digits, no bidi marks)
            style_run(p.add_run(mt.group(0)), size, bold, color, rtl=False)
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
    sec.top_margin = sec.bottom_margin = Mm(15)
    if rtl:
        sec._sectPr.append(OxmlElement("w:bidi"))
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(body)
    rpr = normal.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), FONT)
    szcs = OxmlElement("w:szCs"); szcs.set(qn("w:val"), str(int(body * 2))); rpr.append(szcs)

    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0, tzinfo=None)
    cp = doc.core_properties
    cp.title = f'{b["name"]} | {m["title"][0]}'
    cp.author = cp.last_modified_by = b["name"]
    cp.comments = ""
    cp.subject = cp.keywords = cp.category = ""
    cp.created = cp.modified = now
    cp.revision = 1
    cp.language = "ar-SA" if rtl else "en-GB"

    # ---- header band: shaded paragraphs with one shared teal border, so the group reads as one block
    band = []
    band.append(add_par(doc, b["name"], "Heading 1", 22, rtl, bold=True, color=C_WHITE, line=1.15))
    for t in m["title"]:
        band.append(add_par(doc, t, "Normal", 11.5, rtl, bold=True, color=C_SANDL, line=1.25))
    for c in contact_lines(b):
        band.append(add_par(doc, c, "Normal", body, rtl, color=C_WHITE, line=1.3))
    for p in band:
        ppr_add(p, border({s: (24, 9, TEAL) for s in ("top", "left", "bottom", "right")}))
        ppr_add(p, shade(TEAL))
        p.paragraph_format.keep_with_next = True
    # contact lines sit a little apart from the title: done with line spacing only (no white gaps in the band)

    def h2(k, first=False):
        p = add_par(doc, b["H"][k], "Heading 2", 12.5, rtl, bold=True, color=C_TEAL, before=14 if first else 11,
                    after=4, keep=True)
        ppr_add(p, border({"bottom": (6, 2, SAND)}))
        if PAGE_BREAK_BEFORE.get(key_of(m)) == k:
            p.paragraph_format.page_break_before = True
            p.paragraph_format.space_before = Pt(0)

    def bullets(items):
        for x in items:
            add_par(doc, x, "List Bullet", body, rtl, after=1.5)

    for i, k in enumerate(m["order"]):
        h2(k, first=(i == 0))
        if k == "summary":
            add_par(doc, m["summary"], "Normal", body, rtl, line=1.3 if rtl else 1.2)
        elif k == "comp":
            for row in m["comp"]:
                add_par(doc, DOT.join(row), "Normal", body, rtl, after=1.5)
        elif k == "tech":
            add_par(doc, DOT.join(b["tech"]), "Normal", body, rtl)
        elif k == "exp":
            for j, ((t, e, d), bl) in enumerate(roles(m)):
                add_par(doc, t, "Heading 3", body + 0.5, rtl, bold=True, before=7 if j else 1, keep=True)
                add_par(doc, f"{e} | {d}", "Normal", body, rtl, color=C_TEAL, after=2.5, keep=True)
                bullets(bl)
        elif k in ("edu", "train", "vol"):
            bullets([" | ".join(x) for x in b[k]])
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
ESC = html.escape


def E(t):
    """Escape, and keep hyphenated Latin words (Al-Ahmadi, front-desk) on one line so that a line break
    at the hyphen cannot make a text extractor join the two halves."""
    return re.sub(r"[A-Za-z]+(?:-[A-Za-z]+)+", lambda mt: f'<span class="nb">{mt.group(0)}</span>', ESC(t))


MAIL = f'<a class="ltr" dir="ltr" href="mailto:{EMAIL}">{EMAIL}</a>'
TEL = f'<span class="ltr" dir="ltr">{PHONE}</span>'


def head(m, css):
    b = m["base"]
    rtl = b["lang"] == "ar"
    return (f'<!DOCTYPE html>\n<html lang="{b["lang"]}" dir="{"rtl" if rtl else "ltr"}">\n<head>\n<meta charset="utf-8">\n'
            f'<title>{ESC(b["name"])} | {ESC(m["title"][0])}</title>\n<style>\n{FACES}{css}</style>\n</head>\n')


def joined(parts):
    return E(" | ".join(parts))


def dots(items, cls="dot"):
    return f' <span class="{cls}">·</span> '.join(E(x) for x in items)


# ----------------------------------------------------------------------------
# ATS HTML: same template as the DOCX (band = CSS background, rules = borders)
# ----------------------------------------------------------------------------
ATS_CSS = f"""@page{{size:A4;margin:15mm 18mm 14mm;}}
*{{box-sizing:border-box;}}
html,body{{margin:0;padding:0;}}
:root{{--teal:#{TEAL};--sand:#{SAND};--sandl:#{SAND_LIGHT};--ink:#1a1a1a;}}
body{{font-family:'IBM Plex Sans',sans-serif;font-size:10pt;line-height:1.45;color:var(--ink);}}
html[lang=ar] body{{font-family:'Tajawal',sans-serif;font-size:10.6pt;line-height:1.65;}}
.ltr{{unicode-bidi:isolate;}}
.nb{{white-space:nowrap;}}
a{{color:inherit;text-decoration:none;}}
header{{background:var(--teal);color:#fff;padding:12pt 15pt 11pt;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
h1{{font-size:23pt;font-weight:600;margin:0;line-height:1.2;}}
html[lang=ar] h1{{font-size:24pt;font-weight:700;line-height:1.4;}}
.title{{font-size:11.5pt;font-weight:500;color:var(--sandl);margin:1.5pt 0 0;}}
html[lang=ar] .title{{font-size:12pt;margin:0;}}
.contact{{margin:0;}}
.title + .contact{{margin-top:5pt;}}
h2{{font-size:12pt;font-weight:600;color:var(--teal);margin:13pt 0 5pt;padding-bottom:2pt;border-bottom:.75pt solid var(--sand);break-after:avoid;}}
html[lang=ar] h2{{font-size:13pt;font-weight:700;margin:11pt 0 4pt;padding-bottom:0;}}
h3{{font-size:10.6pt;font-weight:600;margin:7pt 0 0;break-after:avoid;}}
html[lang=ar] h3{{font-size:11.4pt;font-weight:700;margin-top:5pt;}}
h2 + h3{{margin-top:0;}}
p{{margin:0;}}
p,li{{text-wrap:pretty;}}
.meta{{color:var(--teal);font-weight:500;margin-bottom:2pt;break-after:avoid;}}
.dot{{color:#a8873f;font-weight:600;padding:0 1pt;}}
ul{{margin:0;padding-inline-start:14pt;}}
li{{margin:0 0 1.5pt;break-inside:avoid;}}
li::marker{{color:var(--teal);}}
.pb{{break-before:page;margin-top:0;}}
"""


def build_ats_html(m, path):
    b = m["base"]
    o = [head(m, ATS_CSS), "<body>", "<header>", f'<h1>{E(b["name"])}</h1>']
    o += [f'<p class="title">{E(t)}</p>' for t in m["title"]]
    o.append(f'<p class="contact">{E(b["city"])} | {E(b["nat_label"])}: {E(b["nat"])}</p>')
    if b["lang"] == "ar":
        o.append(f'<p class="contact">{E(b["email_label"])} و{E(b["phone_label"])}: <span class="ltr" dir="ltr">{MAIL} | {PHONE}</span></p>')
    else:
        o.append(f'<p class="contact">{E(b["phone_label"])}: {TEL} | {E(b["email_label"])}: {MAIL}</p>')
    o.append("</header>")

    def ul(items):
        o.append("<ul>")
        o.extend(f"<li>{x}</li>" for x in items)
        o.append("</ul>")

    for k in m["order"]:
        pb = ' class="pb"' if PAGE_BREAK_BEFORE.get(key_of(m)) == k else ""
        o.append(f'<h2{pb}>{E(b["H"][k])}</h2>')
        if k == "summary":
            o.append(f'<p>{E(m["summary"])}</p>')
        elif k == "comp":
            o += [f"<p>{dots(row)}</p>" for row in m["comp"]]
        elif k == "tech":
            o.append(f'<p>{dots(b["tech"])}</p>')
        elif k == "exp":
            for (t, e, d), bl in roles(m):
                o.append(f"<h3>{E(t)}</h3>")
                o.append(f'<p class="meta">{E(e)} | {E(d)}</p>')
                ul([E(x) for x in bl])
        elif k in ("edu", "train", "vol"):
            ul([joined(x) for x in b[k]])
        elif k == "lang":
            o.append(f'<p>{joined(b["langs"])}</p>')
    o.append("</body>\n</html>\n")
    path.write_text("\n".join(o), encoding="utf-8")


# ----------------------------------------------------------------------------
# Executive Modern HTML: teal name band, tinted full-height side column, timeline, tags
# Geometry is fixed (band 42mm, side column 66mm) so verify.py can read the page zone by zone.
# ----------------------------------------------------------------------------
BAND_MM, SIDE_MM, SIDE_AR_MM = 33, 58, 58
EXEC_CSS = f"""@page{{size:A4;margin:0;}}
*{{box-sizing:border-box;}}
html,body{{margin:0;padding:0;-webkit-print-color-adjust:exact;print-color-adjust:exact;}}
:root{{--teal:#{TEAL};--sand:#{SAND};--sandl:#{SAND_LIGHT};--tint:#f5f1e8;--ink:#20282b;--muted:#566266;--line:#d6ccb8;}}
body{{font-family:'IBM Plex Sans',sans-serif;font-size:9.5pt;line-height:1.45;color:var(--ink);}}
html[lang=ar] body{{font-family:'Tajawal',sans-serif;font-size:10pt;line-height:1.6;}}
.ltr{{unicode-bidi:isolate;}}
.nb{{white-space:nowrap;}}
a{{color:inherit;text-decoration:none;}}
.page{{width:210mm;height:296.6mm;display:grid;grid-template-rows:{BAND_MM}mm 1fr;break-inside:avoid;overflow:hidden;}}
header{{background:var(--teal);color:#fff;padding:0 13mm;display:flex;flex-direction:column;justify-content:center;border-bottom:1.6pt solid var(--sand);}}
h1{{font-size:27pt;font-weight:600;margin:0;line-height:1.12;letter-spacing:.01em;}}
html[lang=ar] h1{{font-size:28pt;font-weight:700;line-height:1.3;letter-spacing:0;}}
.title{{font-size:11.5pt;font-weight:500;color:var(--sandl);margin:1.6mm 0 0;}}
html[lang=ar] .title{{font-size:12.2pt;margin-top:.2mm;line-height:1.5;}}
.title + .title{{margin-top:0;color:#fff;font-weight:400;font-size:10.5pt;}}
html[lang=ar] .title + .title{{font-size:11pt;}}
.grid{{display:grid;grid-template-columns:{SIDE_MM}mm 1fr;min-height:0;}}
html[lang=ar] .grid{{grid-template-columns:{SIDE_AR_MM}mm 1fr;}}
aside{{background:var(--tint);padding:6.5mm 6mm 5mm;padding-inline-start:13mm;}}
main{{padding:6.5mm 7mm 5mm;padding-inline-end:13mm;}}
section{{margin:0 0 4.3mm;}}
section:last-child{{margin-bottom:0;}}
h2{{font-size:8.8pt;font-weight:600;color:var(--teal);text-transform:uppercase;letter-spacing:.08em;margin:0 0 2.2mm;break-after:avoid;}}
h2::after{{content:"";display:block;width:9mm;height:1.5pt;background:var(--sand);margin-top:1.1mm;}}
html[lang=ar] h2{{font-size:11.8pt;font-weight:700;letter-spacing:0;text-transform:none;margin-bottom:1.7mm;line-height:1.45;}}
html[lang=ar] section{{margin-bottom:3.9mm;}}
html[lang=ar] ul.rows li{{margin-bottom:1.1mm;}}
html[lang=ar] .role{{margin-bottom:2mm;}}
html[lang=ar] h2::after{{margin-top:.3mm;}}
p{{margin:0;}}
p,li{{text-wrap:pretty;}}
ul{{margin:0;padding:0;list-style:none;}}
.cap{{display:block;font-size:8.5pt;color:var(--muted);line-height:1.35;}}
html[lang=ar] .cap{{font-size:9pt;line-height:1.5;}}
aside li{{margin:0 0 1.9mm;}}
aside li:last-child{{margin-bottom:0;}}
aside .stack li{{margin-bottom:2.3mm;}}
aside .stack .a{{display:block;font-weight:500;}}
html[lang=ar] aside .stack .a{{font-weight:500;}}
aside .stack .b{{display:block;color:var(--muted);font-size:8.8pt;}}
html[lang=ar] aside .stack .b{{font-size:9.2pt;}}
.sep{{color:var(--muted);}}
aside .sep{{display:none;}}
.tags{{display:flex;flex-wrap:wrap;gap:1.2mm 1.3mm;}}
.tags li{{border:.6pt solid #9db7ba;border-radius:9pt;padding:.5mm 2.6mm;font-size:8.7pt;line-height:1.45;color:#184a52;white-space:nowrap;background:#fff;}}
html[lang=ar] .tags li{{font-size:9pt;line-height:1.55;padding:.3mm 2.2mm .1mm;}}
html[lang=ar] .tags{{gap:1.1mm 1mm;}}
.tl{{border-inline-start:.8pt solid var(--line);margin-inline-start:1.2mm;padding-inline-start:5mm;}}
.role{{position:relative;margin:0 0 2.5mm;break-inside:avoid;}}
.role:last-child{{margin-bottom:0;}}
.role::before{{content:"";position:absolute;inset-inline-start:-6.45mm;top:1.25mm;width:2.1mm;height:2.1mm;border-radius:50%;background:var(--teal);border:.8mm solid #fff;box-sizing:content-box;margin-top:-.8mm;}}
html[lang=ar] .role::before{{top:1.9mm;}}
.rh{{display:flex;justify-content:space-between;align-items:baseline;gap:4mm;margin-bottom:.9mm;}}
h3{{font-size:10.5pt;font-weight:600;margin:0;}}
html[lang=ar] h3{{font-size:11pt;font-weight:700;}}
.date{{font-size:8.8pt;color:var(--muted);white-space:nowrap;}}
html[lang=ar] .date{{font-size:9.2pt;}}
.org{{color:var(--teal);font-weight:500;}}
ul.b{{padding-inline-start:3.6mm;list-style:disc;}}
ul.b li{{margin:0 0 .4mm;padding-inline-start:.4mm;}}
ul.b li::marker{{color:var(--sand);font-size:.85em;}}
ul.rows li{{margin:0 0 1.7mm;}}
ul.rows li:last-child{{margin-bottom:0;}}
ul.rows .a{{font-weight:600;}}
html[lang=ar] ul.rows .a{{font-weight:700;}}
ul.rows .b{{color:var(--muted);}}
"""


def parts_html(parts):
    a = f'<span class="a">{E(parts[0])}</span>'
    if len(parts) == 1:
        return a
    return a + ' <span class="sep">|</span> ' + f'<span class="b">{E(" | ".join(parts[1:]))}</span>'


SIDE_KEYS = ["tech", "edu", "train", "lang"]


def build_exec_html(m, path):
    b = m["base"]
    H = b["H"]
    o = [head(m, EXEC_CSS), '<body>\n<div class="page">', "<header>", f'<h1>{E(b["name"])}</h1>']
    o += [f'<p class="title">{E(t)}</p>' for t in m["title"]]
    o += ["</header>", '<div class="grid">', "<aside>",
          f'<section>\n<h2>{E(b["contact_heading"])}</h2>\n<ul class="contact">',
          f'<li><span class="cap">{E(b["city_label"])}</span>{E(b["city"])}</li>',
          f'<li><span class="cap">{E(b["nat_label"])}</span>{E(b["nat"])}</li>',
          f'<li><span class="cap">{E(b["phone_label"])}</span>{TEL}</li>',
          f'<li><span class="cap">{E(b["email_label"])}</span>{MAIL}</li>',
          "</ul>\n</section>"]
    for k in [x for x in m["order"] if x in SIDE_KEYS]:
        o.append(f"<section>\n<h2>{E(H[k])}</h2>")
        if k == "tech":
            o.append("<ul>" + "".join(f"<li>{E(x)}</li>" for x in b["tech"]) + "</ul>")
        elif k in ("edu", "train"):
            o.append('<ul class="stack">' + "".join(f"<li>{parts_html(x)}</li>" for x in b[k]) + "</ul>")
        elif k == "lang":
            o.append("<ul>" + "".join(f"<li>{E(x)}</li>" for x in b["langs"]) + "</ul>")
        o.append("</section>")
    o.append("</aside>\n<main>")
    for k in [x for x in m["order"] if x not in SIDE_KEYS]:
        o.append(f"<section>\n<h2>{E(H[k])}</h2>")
        if k == "summary":
            o.append(f'<p>{E(m["summary"])}</p>')
        elif k == "comp":
            o.append('<ul class="tags">' + "".join(f"<li>{E(x)}</li>" for row in m["comp"] for x in row) + "</ul>")
        elif k == "exp":
            o.append('<div class="tl">')
            for (t, e, d), bl in roles(m):
                o.append('<div class="role">')
                o.append(f"<h3>{E(t)}</h3>")
                o.append(f'<div class="rh"><p class="org">{E(e)}</p><span class="date">{E(d)}</span></div>')
                o.append('<ul class="b">' + "".join(f"<li>{E(x)}</li>" for x in bl) + "</ul>")
                o.append("</div>")
            o.append("</div>")
        elif k == "vol":
            o.append('<ul class="rows">' + "".join(f"<li>{parts_html(x)}</li>" for x in b["vol"]) + "</ul>")
        o.append("</section>")
    o.append("</main>\n</div>\n</div>\n</body>\n</html>\n")
    path.write_text("\n".join(o), encoding="utf-8")


# ----------------------------------------------------------------------------
if __name__ == "__main__":
    for key, m in MODELS.items():
        build_docx(m, OUT / fname(m, "ats", "docx"))
        build_ats_html(m, OUT / fname(m, "ats", "html"))
        build_exec_html(m, OUT / fname(m, "executive", "html"))
        print("built", key)
