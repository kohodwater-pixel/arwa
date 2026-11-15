#!/usr/bin/env python3
"""Transcribe the client's source file into data/rates.json.

No price is typed here. Every price row and every priced extra points to a line
number in _originals/client-brief-and-rates_2026-11-15.txt; the RUB value is
read from that line by regex, and the line text is stored as `source_line`.
Occupancy and breakfast classifications are asserted against the wording of the
line (or of the stated context line) so a mis-typed line number or a wrong
classification stops the build.

SAR = RUB / 21.4, Decimal, ROUND_HALF_UP, 2 dp.
"""
import json, re, pathlib, sys
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLIENT = ROOT.parents[1]
SRC = CLIENT / "_originals" / "client-brief-and-rates_2026-11-15.txt"
OUT = ROOT / "data" / "rates.json"
LINES = SRC.read_text(encoding="utf-8").split("\n")
RATE = Decimal("21.4")


def L(n):
    return LINES[n - 1]


def sar(rub):
    return str((Decimal(rub) / RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def rub_from(n):
    m = re.findall(r"(\d{1,3}(?:,\d{3})+|\d+)\s*روبل", L(n))
    if len(m) != 1:
        sys.exit(f"line {n}: expected exactly one RUB figure, got {m!r}: {L(n)}")
    return int(m[0].replace(",", ""))


# ---- vocab ---------------------------------------------------------------
OCC = {
    "1 person": ("شخص واحد", "1 person"),
    "2 persons": ("شخصان", "2 persons"),
    "3 persons": ("ثلاثة أشخاص", "3 persons"),
    "3 persons with extra bed": ("ثلاثة أشخاص مع سرير إضافي", "3 persons with extra bed"),
    "single": ("مفردة", "Single"),
    "double": ("مزدوجة", "Double"),
    "not stated": ("غير مذكور", "Not stated"),
}
BF = {
    "with": ("مع الإفطار", "With breakfast"),
    "without": ("بدون إفطار", "Without breakfast"),
    "with breakfast for 1": ("مع إفطار لشخص", "With breakfast for 1"),
    "with breakfast for 2": ("مع إفطار لشخصين", "With breakfast for 2"),
    "not stated": ("غير مذكور", "Not stated"),
}

# wording checks: (occupancy|breakfast) -> predicate on the line or context text
def check_occ(occ, text):
    t = text
    ok = {
        "1 person": "شخص واحد" in t,
        "2 persons": "شخصان" in t,
        "3 persons": "ثلاثة أشخاص" in t and "سرير إضافي" not in t,
        "3 persons with extra bed": "ثلاثة أشخاص مع سرير إضافي" in t,
        "single": "مفردة" in t,
        "double": "مزدوجة" in t,
        "not stated": not any(w in t for w in ["شخص واحد", "شخصان", "ثلاثة أشخاص", "مفردة", "مزدوجة"]),
    }[occ]
    return ok


def check_bf(bf, line, ctx):
    t = line + " || " + (ctx or "")
    return {
        "with": ("مع الإفطار" in line) or ("شاملة" in (ctx or "") and "إفطار" not in line and "الإفطار" in (ctx or "")),
        "without": "بدون إفطار" in line or ("بدون الإفطار" in (ctx or "") and "إفطار" not in line),
        "with breakfast for 1": "مع إفطار لشخص:" in line,
        "with breakfast for 2": "مع إفطار لشخصين" in line,
        "not stated": "إفطار" not in line and "الإفطار" not in (ctx or ""),
    }[bf]


def row(line_no, occ, bf, ctx=None):
    text = L(line_no)
    if not check_occ(occ, text):
        sys.exit(f"line {line_no}: occupancy '{occ}' does not match wording: {text}")
    ctx_text = L(ctx) if ctx else None
    if not check_bf(bf, text, ctx_text):
        sys.exit(f"line {line_no}: breakfast '{bf}' does not match wording: {text} | ctx: {ctx_text}")
    rub = rub_from(line_no)
    r = {
        "occupancy": occ, "occupancy_ar": OCC[occ][0], "occupancy_en": OCC[occ][1],
        "breakfast": bf, "breakfast_ar": BF[bf][0], "breakfast_en": BF[bf][1],
        "rub": rub, "sar": sar(rub),
        "source_line_no": line_no, "source_line": text,
    }
    if ctx:
        r["context_line_no"] = ctx
        r["context_line"] = ctx_text
    return r


def room(name, rows, heading_line, size=None, qualifier_ar=None, qualifier_en=None):
    h = L(heading_line)
    if name.split(" ")[0] not in h:
        sys.exit(f"room heading line {heading_line} does not contain '{name}': {h}")
    if size is not None:
        if f"{size} م²" not in h and not any(f"{size} م²" in L(heading_line + k) for k in (1, 2)):
            sys.exit(f"size {size} not found near line {heading_line}")
    return {"name": name, "qualifier_ar": qualifier_ar, "qualifier_en": qualifier_en,
            "size_m2": size, "heading_line_no": heading_line, "heading_line": h, "rows": rows}


def period(key, label_ar, label_en, dates_ar, dates_en, rooms, label_line=None, date_lines=(), end_iso=None, start_iso=None):
    for n in ([label_line] if label_line else []) + list(date_lines):
        pass
    return {"key": key, "label_ar": label_ar, "label_en": label_en,
            "dates_ar": dates_ar, "dates_en": dates_en,
            "dates_as_written": [L(n) for n in date_lines] if date_lines else None,
            "date_line_nos": list(date_lines) or None,
            "start_iso_derived": start_iso, "end_iso_derived": end_iso,
            "rooms": rooms}


def extra(kind, item_ar, item_en, cond_ar, cond_en, lines, priced=True, value_ar=None, value_en=None):
    rub = rub_from(lines[0]) if priced else None
    if priced:
        for n in lines[1:]:
            if rub_from(n) != rub:
                sys.exit(f"extra lines {lines} disagree")
    else:
        if re.search(r"\d{1,3},\d{3}\s*روبل", " ".join(L(n) for n in lines)):
            sys.exit(f"extra lines {lines} contain a price but marked unpriced")
    return {"kind": kind, "item_ar": item_ar, "item_en": item_en,
            "condition_ar": cond_ar, "condition_en": cond_en,
            "rub": rub, "sar": sar(rub) if priced else None,
            "value_ar": value_ar, "value_en": value_en,
            "source_line_nos": lines, "source_lines": [L(n) for n in lines]}


NODATES_AR = "لم تُحدَّد فترة الصلاحية في المصدر"
NODATES_EN = "No validity dates given in the source"
hotels = []

# 1 ---------------------------------------------------------------- St. Regis
hotels.append({
    "id": "st-regis", "city": "moscow", "order": 1,
    "name_en": "The St. Regis Moscow Nikolskaya", "name_ar": "فندق سانت ريجيس موسكو",
    "name_lines": [130, 132], "stars": 5, "stars_line": 132, "economy": False,
    "facts_ar": ["خمس نجوم (وفق المصدر)"], "facts_en": ["Five-star (as stated in the source)"],
    "booking_notes_ar": ["لم يُذكر عدد النزلاء لكل سعر.", "السرير الإضافي ورد ضمن بيانات غرفة Deluxe."],
    "booking_notes_en": ["Occupancy is not stated for these rates.", "The extra bed is listed under the Deluxe room."],
    "periods": [period("p1", "الأسعار", "Rates", NODATES_AR, NODATES_EN, [
        room("Superior", [row(137, "not stated", "without"), row(138, "not stated", "with")], 134, size=35),
        room("Deluxe", [row(143, "not stated", "without"), row(144, "not stated", "with")], 140, size=40),
    ])],
    "extras": [extra("extra_bed", "سرير إضافي", "Extra bed", "ورد ضمن بيانات غرفة Deluxe", "Listed under the Deluxe room", [145])],
})

# 2 ---------------------------------------------------------------- Garden Plaza
hotels.append({
    "id": "garden-plaza", "city": "moscow", "order": 2,
    "name_en": "Garden Plaza", "name_ar": "فندق جاردن بلازا",
    "name_lines": [147, 149], "stars": None, "economy": False,
    "facts_ar": ["لم يُذكر تصنيف النجوم في المصدر", "الأسعار مع الإفطار تشمل بوفيه الإفطار"],
    "facts_en": ["Star rating not stated in the source", "Rates with breakfast include buffet breakfast"],
    "booking_notes_ar": ["لا تتوفر بيانات أسعار بدون إفطار لبقية أنواع الغرف (Club Premium وClub Junior Suite).", "سعر Standard بدون إفطار لم يُذكر له نوع الإشغال."],
    "booking_notes_en": ["No room-only rates are given for the other room types (Club Premium, Club Junior Suite).", "Occupancy is not stated for the Standard room-only rate."],
    "periods": [period("p1", "الأسعار", "Rates", NODATES_AR, NODATES_EN, [
        room("Standard", [row(155, "double", "with", 151), row(156, "single", "with", 151), row(176, "not stated", "without", 174)], 153),
        room("Suite", [row(161, "single", "with", 151), row(162, "double", "with", 151), row(177, "single", "without", 174), row(178, "double", "without", 174)], 159),
        room("Club Premium", [row(166, "double", "with", 151), row(167, "single", "with", 151)], 164),
        room("Club Junior Suite", [row(171, "single", "with", 151), row(172, "double", "with", 151)], 169),
    ])],
    "extras": [extra("extra_bed", "سرير إضافي", "Extra bed", "لليلة — ورد ضمن بيانات غرفة Standard", "Per night — listed under the Standard room", [157])],
})

# 3 ---------------------------------------------------------------- Ararat Park
def ararat_rooms(k, cv, dl, st):
    return [
        room("Park King / Twin", [row(k + 2, "1 person", "without"), row(k + 3, "1 person", "with"), row(k + 4, "2 persons", "without"), row(k + 5, "2 persons", "with")], k),
        room("Park City View", [row(cv + 2, "1 person", "without"), row(cv + 3, "1 person", "with"), row(cv + 4, "2 persons", "without"), row(cv + 5, "2 persons", "with")], cv),
        room("Park Deluxe", [row(dl + 2, "1 person", "without"), row(dl + 3, "1 person", "with"), row(dl + 4, "2 persons", "without"), row(dl + 5, "2 persons", "with"), row(dl + 6, "3 persons", "without"), row(dl + 7, "3 persons", "with")], dl),
        room("Park Suite", [row(st + 2, "1 person", "without"), row(st + 3, "1 person", "with"), row(st + 4, "2 persons", "without"), row(st + 5, "2 persons", "with"), row(st + 6, "3 persons", "without"), row(st + 7, "3 persons", "with")], st),
    ]

hotels.append({
    "id": "ararat-park", "city": "moscow", "order": 3,
    "name_en": "Ararat Park Hotel", "name_ar": "فندق أرارات بارك",
    "name_lines": [182, 184], "stars": None, "economy": False,
    "facts_ar": ["موسكو", "لم يُذكر تصنيف النجوم في المصدر"],
    "facts_en": ["Moscow", "Star rating not stated in the source"],
    "booking_notes_ar": ["عرض الخريف يسري على فترتين منفصلتين.", "تاريخ 25 نوفمبر يرد في عرض الخريف والعرض الموسمي، وتاريخ 21 ديسمبر يرد في العرض الموسمي وعرض الشتاء — للتأكيد."],
    "booking_notes_en": ["The autumn offer covers two separate date ranges.", "25 November appears in both the autumn and seasonal offers, and 21 December in both the seasonal and winter offers — to be confirmed."],
    "periods": [
        period("autumn", "عرض الخريف", "Autumn offer", "7 سبتمبر – 23 أكتوبر 2026، و 30 أكتوبر – 25 نوفمبر 2026", "7 Sep – 23 Oct 2026 and 30 Oct – 25 Nov 2026",
               ararat_rooms(193, 200, 207, 216), 186, (190, 191), end_iso="2026-11-25", start_iso="2026-09-07"),
        period("seasonal", "العرض الموسمي", "Seasonal offer", "25 نوفمبر – 21 ديسمبر 2026", "25 Nov – 21 Dec 2026",
               ararat_rooms(229, 236, 243, 252), 225, (227,), end_iso="2026-12-21", start_iso="2026-11-25"),
        period("winter", "عرض الشتاء", "Winter offer", "21 – 30 ديسمبر 2026", "21 – 30 Dec 2026",
               ararat_rooms(265, 272, 279, 288), 261, (263,), end_iso="2026-12-30", start_iso="2026-12-21"),
    ],
    "extras": [
        extra("child", "إقامة طفل 0–5 سنوات", "Child 0–5 years", "دون سرير إضافي", "Without extra bed", [299], priced=False, value_ar="مجاناً", value_en="Free"),
        extra("child", "إقامة طفل 6–11 سنة", "Child 6–11 years", "بدون إفطار", "Without breakfast", [300]),
        extra("child", "إقامة طفل 6–11 سنة", "Child 6–11 years", "مع الإفطار", "With breakfast", [301]),
    ],
})

# 4 ---------------------------------------------------------------- Cosmos Arbat
hotels.append({
    "id": "cosmos-arbat", "city": "moscow", "order": 4,
    "name_en": "Cosmos Arbat Hotel", "name_ar": "فندق كوسموس أربات",
    "name_lines": [303, 305], "stars": None, "economy": False,
    "facts_ar": ["موسكو", "لم يُذكر تصنيف النجوم في المصدر"],
    "facts_en": ["Moscow", "Star rating not stated in the source"],
    "booking_notes_ar": ["لم يحدد المصدر ما إذا كانت أسعار Superior شاملة الإفطار.", "لم يُذكر الإفطار لسعر Deluxe في ديسمبر.", "لم يُذكر عدد النزلاء لكل سعر."],
    "booking_notes_en": ["The source does not state whether the Superior rates include breakfast.", "Breakfast is not stated for the December Deluxe rate.", "Occupancy is not stated for these rates."],
    "periods": [
        period("nov", "حتى نهاية نوفمبر", "Until the end of November", "حتى نهاية نوفمبر (تاريخ البداية غير مذكور)", "Until the end of November (start date not stated)", [
            room("Deluxe", [row(309, "not stated", "without")], 309, qualifier_ar="إطلالة داخلية", qualifier_en="Inner view"),
            room("Superior", [row(311, "not stated", "not stated")], 311, qualifier_ar="إطلالة على شارع أربات", qualifier_en="Arbat Street view"),
        ], 307, (307,), end_iso="2026-11-30"),
        period("dec", "أسعار ديسمبر", "December rates", "ديسمبر حتى 30 ديسمبر", "December, until 30 December", [
            room("Deluxe", [row(315, "not stated", "not stated")], 315, qualifier_ar="إطلالة داخلية", qualifier_en="Inner view"),
            room("Superior", [row(316, "not stated", "not stated")], 316, qualifier_ar="إطلالة على شارع أربات", qualifier_en="Arbat Street view"),
        ], 313, (313,), end_iso="2026-12-30", start_iso="2026-12-01"),
    ],
    "extras": [extra("breakfast", "إضافة الإفطار", "Breakfast supplement", "وردت ضمن أسعار «حتى نهاية نوفمبر»؛ لم يُذكر إن كانت للشخص", "Listed under 'until the end of November'; per person not stated", [310])],
})

# 5 ---------------------------------------------------------------- InterContinental
hotels.append({
    "id": "intercontinental", "city": "moscow", "order": 5,
    "name_en": "InterContinental Moscow", "name_ar": "فندق إنتركونتيننتال موسكو",
    "name_lines": [320, 322], "stars": 5, "stars_line": 322, "economy": False,
    "facts_ar": ["خمس نجوم (وفق المصدر)"], "facts_en": ["Five-star (as stated in the source)"],
    "booking_notes_ar": ["لم يُذكر ما إذا كان السعر الأساسي شاملاً الإفطار، ولا عدد النزلاء.", "«نهاية نوفمبر» حدّ غير محدد بتاريخ دقيق."],
    "booking_notes_en": ["The source does not state whether the base rate includes breakfast, nor the occupancy.", "'End of November' is not an exact date."],
    "periods": [
        period("nov", "حتى نهاية نوفمبر", "Until the end of November", "حتى نهاية نوفمبر (تاريخ البداية غير مذكور)", "Until the end of November (start date not stated)", [
            room("Deluxe King / Twin", [row(326, "not stated", "not stated")], 326)], 324, (324,), end_iso="2026-11-30"),
        period("dec", "من نهاية نوفمبر حتى 18 ديسمبر", "End of November to 18 December", "من نهاية نوفمبر حتى 18 ديسمبر", "From the end of November to 18 December", [
            room("Deluxe King / Twin", [row(330, "not stated", "not stated")], 330)], 328, (328,), end_iso="2026-12-18"),
    ],
    "extras": [
        extra("extra_bed", "سرير إضافي", "Extra bed", "لليلة", "Per night", [334]),
        extra("breakfast", "الإفطار", "Breakfast", "للشخص", "Per person", [335]),
    ],
})

# 6 ---------------------------------------------------------------- Marriott
def marriott_rooms(d, s, j, c):
    return [
        room("Deluxe King / Twin", [row(d + 2, "not stated", "without"), row(d + 3, "not stated", "with breakfast for 1"), row(d + 4, "not stated", "with breakfast for 2")], d),
        room("Superior", [row(s + 2, "not stated", "without"), row(s + 3, "not stated", "with breakfast for 1"), row(s + 4, "not stated", "with breakfast for 2")], s),
        room("Junior Suite", [row(j + 2, "not stated", "with breakfast for 1"), row(j + 3, "not stated", "with breakfast for 2")], j),
        room("Corner Suite", [row(c + 2, "not stated", "with breakfast for 1"), row(c + 3, "not stated", "with breakfast for 2")], c, size=65),
    ]

hotels.append({
    "id": "marriott-royal-aurora", "city": "moscow", "order": 6,
    "name_en": "Marriott Royal Aurora Moscow", "name_ar": "فندق ماريوت رويال أورورا",
    "name_lines": [337, 339], "stars": 5, "stars_line": 339, "economy": False,
    "facts_ar": ["خمس نجوم (وفق المصدر)"], "facts_en": ["Five-star (as stated in the source)"],
    "booking_notes_ar": ["يذكر المصدر «مع إفطار لشخص / لشخصين» دون ذكر عدد النزلاء صراحة.", "لا توجد أسعار بدون إفطار لـ Junior Suite وCorner Suite.", "من 30 ديسمبر إلى 8 يناير: الأسعار عند الطلب."],
    "booking_notes_en": ["The source gives 'with breakfast for 1 / for 2' without stating occupancy explicitly.", "No room-only rates for Junior Suite and Corner Suite.", "30 December to 8 January: rates on request."],
    "periods": [
        period("p1", "الفترة الأولى", "Period 1", "25 أغسطس – 19 سبتمبر 2026", "25 Aug – 19 Sep 2026", marriott_rooms(345, 351, 357, 362), 341, (343,), end_iso="2026-09-19", start_iso="2026-08-25"),
        period("p2", "الفترة الثانية", "Period 2", "20 سبتمبر – 19 نوفمبر 2026", "20 Sep – 19 Nov 2026", marriott_rooms(371, 377, 383, 388), 367, (369,), end_iso="2026-11-19", start_iso="2026-09-20"),
        period("p3", "الفترة الثالثة", "Period 3", "20 نوفمبر – 29 ديسمبر 2026", "20 Nov – 29 Dec 2026", marriott_rooms(397, 403, 409, 414), 393, (395,), end_iso="2026-12-29", start_iso="2026-11-20"),
    ],
    "extras": [
        extra("child", "الأطفال دون 5 سنوات", "Children under 5", "دون سرير إضافي", "Without extra bed", [421], priced=False, value_ar="مجاناً", value_en="Free"),
        extra("breakfast", "فطور الأطفال من 5 سنوات", "Children's breakfast from 5 years", "—", "—", [422]),
        extra("extra_bed", "سرير إضافي", "Extra bed", "حسب نوع الغرفة والتوفر؛ لم يُذكر سعر", "Depends on room type and availability; no fee stated", [423], priced=False, value_ar="غير مذكور", value_en="Not stated"),
        extra("on_request", "30 ديسمبر – 8 يناير", "30 Dec – 8 Jan", "الأسعار عند الطلب", "Rates on request", [424], priced=False, value_ar="عند الطلب", value_en="On request"),
    ],
})

# 7 ---------------------------------------------------------------- Safmar
hotels.append({
    "id": "safmar-grand", "city": "moscow", "order": 7,
    "name_en": "Safmar Grand Moscow", "name_ar": "فندق سافمار جراند",
    "name_lines": [426, 428], "stars": 5, "stars_line": 428, "economy": False,
    "facts_ar": ["خمس نجوم (وفق المصدر)", "أسعار Deluxe King / Twin شاملة الإفطار"],
    "facts_en": ["Five-star (as stated in the source)", "Deluxe King / Twin rates include breakfast"],
    "booking_notes_ar": ["من 29 ديسمبر إلى 10 يناير: الأسعار عند الطلب."],
    "booking_notes_en": ["29 December to 10 January: rates on request."],
    "periods": [period("p1", "الفترة", "Period", "25 أغسطس – 28 ديسمبر 2026", "25 Aug – 28 Dec 2026", [
        room("Deluxe King / Twin", [row(434, "1 person", "with", 432), row(435, "2 persons", "with", 432), row(436, "3 persons with extra bed", "with", 432)], 432),
    ], 430, (430,), end_iso="2026-12-28", start_iso="2026-08-25")],
    "extras": [
        extra("extra_bed", "سرير إضافي", "Extra bed", "لليلة", "Per night", [440]),
        extra("breakfast", "فطور الشخص الثالث", "Third person's breakfast", "لليلة", "Per night", [441]),
        extra("on_request", "29 ديسمبر – 10 يناير", "29 Dec – 10 Jan", "الأسعار عند الطلب", "Rates on request", [443], priced=False, value_ar="عند الطلب", value_en="On request"),
    ],
})

# 8 ---------------------------------------------------------------- National
def national_rooms(c, s, j, st, jt, rs, ks):
    return [
        room("Classic King / Twin", [row(c + 2, "not stated", "without"), row(c + 3, "not stated", "with breakfast for 1"), row(c + 4, "not stated", "with breakfast for 2")], c),
        room("Studio", [row(s + 2, "not stated", "without"), row(s + 3, "not stated", "with breakfast for 1"), row(s + 4, "not stated", "with breakfast for 2")], s),
        room("Junior Suite – No View", [row(j + 2, "not stated", "without"), row(j + 3, "not stated", "with breakfast for 1"), row(j + 4, "not stated", "with breakfast for 2")], j),
        room("Studio – Tverskaya View", [row(st + 2, "not stated", "with breakfast for 1"), row(st + 3, "not stated", "with breakfast for 2")], st),
        room("Junior Suite – Tverskaya View", [row(jt + 2, "not stated", "with breakfast for 1"), row(jt + 3, "not stated", "with breakfast for 2")], jt),
        room("Studio – Red Square / Kremlin View", [row(rs + 2, "not stated", "with breakfast for 1"), row(rs + 3, "not stated", "with breakfast for 2")], rs),
        room("Kremlin Suite", [row(ks + 2, "not stated", "with breakfast for 1"), row(ks + 3, "not stated", "with breakfast for 2")], ks),
    ]

hotels.append({
    "id": "national", "city": "moscow", "order": 8,
    "name_en": "Hotel National Moscow", "name_ar": "فندق ناشيونال موسكو",
    "name_lines": [445, 447], "stars": 5, "stars_line": 447, "economy": False,
    "facts_ar": ["خمس نجوم (وفق المصدر)"], "facts_en": ["Five-star (as stated in the source)"],
    "booking_notes_ar": ["يذكر المصدر «مع إفطار لشخص / لشخصين» دون ذكر عدد النزلاء صراحة.", "غرفة Classic لا تسمح بإضافة شخص ثالث.", "بعض الغرف غير متاحة في تواريخ محددة.", "لم تُذكر أسعار بعد 22 ديسمبر 2026."],
    "booking_notes_en": ["The source gives 'with breakfast for 1 / for 2' without stating occupancy explicitly.", "The Classic room does not allow a third person.", "Some rooms are unavailable on specific dates.", "No rates given after 22 December 2026."],
    "periods": [
        period("p1", "الفترة الأولى", "Period 1", "25 أغسطس – 24 سبتمبر 2026", "25 Aug – 24 Sep 2026", national_rooms(453, 459, 465, 471, 476, 481, 486), 449, (451,), end_iso="2026-09-24", start_iso="2026-08-25"),
        period("p2", "الفترة الثانية", "Period 2", "25 سبتمبر – 19 نوفمبر 2026", "25 Sep – 19 Nov 2026", national_rooms(495, 501, 507, 513, 518, 523, 528), 491, (493,), end_iso="2026-11-19", start_iso="2026-09-25"),
        period("p3", "الفترة الثالثة", "Period 3", "20 نوفمبر – 22 ديسمبر 2026", "20 Nov – 22 Dec 2026", national_rooms(537, 543, 549, 555, 560, 565, 570), 533, (535,), end_iso="2026-12-22", start_iso="2026-11-20"),
    ],
    "extras": [
        extra("extra_bed", "سرير إضافي", "Extra bed", "لليلة، حسب نوع الغرفة", "Per night, depending on room type", [577]),
        extra("breakfast", "فطور الأطفال من 5 سنوات", "Children's breakfast from 5 years", "—", "—", [578]),
        extra("child", "فطور الأطفال دون 5 سنوات", "Breakfast for children under 5", "—", "—", [579], priced=False, value_ar="مجاناً", value_en="Free"),
        extra("restriction", "غرفة Classic", "Classic room", "لا تسمح بإضافة شخص ثالث", "Does not allow a third person", [580], priced=False, value_ar="—", value_en="—"),
        extra("restriction", "توفر الغرف", "Room availability", "بعض الغرف غير متاحة في تواريخ محددة", "Some rooms unavailable on specific dates", [581], priced=False, value_ar="—", value_en="—"),
    ],
})

# 9 ---------------------------------------------------------------- Brosko
def brosko_room(name, h):
    return room(name, [row(h + 2, "not stated", "without"), row(h + 3, "not stated", "with breakfast for 1"), row(h + 4, "not stated", "with breakfast for 2")], h)

hotels.append({
    "id": "brosko", "city": "moscow", "order": 9,
    "name_en": "Brosko Hotels Group", "name_ar": "فندق بروسكو",
    "name_lines": [583, 585], "stars": 4, "stars_line": 585, "economy": True, "economy_line": 585,
    "facts_ar": ["فندق اقتصادي أربع نجوم في أربات (وفق المصدر)"], "facts_en": ["Economy four-star hotel in Arbat (as stated in the source)"],
    "booking_notes_ar": ["يذكر المصدر «مع إفطار لشخص / لشخصين» دون ذكر عدد النزلاء صراحة.", "السرير الإضافي متوفر في Deluxe وSuite حسب التوفر."],
    "booking_notes_en": ["The source gives 'with breakfast for 1 / for 2' without stating occupancy explicitly.", "Extra bed available in Deluxe and Suite, subject to availability."],
    "periods": [period("p1", "الأسعار", "Rates", NODATES_AR, NODATES_EN, [
        brosko_room("Standard Double", 587), brosko_room("Standard Twin", 593), brosko_room("Deluxe", 599), brosko_room("Suite", 605),
    ])],
    "extras": [
        extra("child", "الأطفال دون 6 سنوات", "Children under 6", "دون سرير إضافي", "Without extra bed", [613], priced=False, value_ar="مجاناً", value_en="Free"),
        extra("child", "سرير الأطفال دون 3 سنوات", "Cot for children under 3", "لليلة", "Per night", [614]),
        extra("extra_bed", "سرير إضافي", "Extra bed", "لليلة، متوفر في Deluxe وSuite حسب التوفر", "Per night, in Deluxe and Suite, subject to availability", [615]),
        extra("breakfast", "فطور الأطفال من 6 إلى 12 سنة", "Children's breakfast 6–12 years", "—", "—", [616]),
        extra("breakfast", "الفطور الإضافي للبالغين", "Additional adult breakfast", "—", "—", [617]),
    ],
})

# 10 --------------------------------------------------------------- Cosmos Royal Nevsky
hotels.append({
    "id": "cosmos-royal-nevsky", "city": "spb", "order": 10,
    "name_en": "Cosmos Royal Nevsky", "name_ar": "فندق كوسموس رويال نيفسكي",
    "name_lines": [623, 625], "stars": 5, "stars_line": 625, "economy": False,
    "facts_ar": ["خمس نجوم (وفق المصدر)", "جميع الأسعار شاملة الإفطار"],
    "facts_en": ["Five-star (as stated in the source)", "All rates include breakfast"],
    "booking_notes_ar": ["رسم الطفل حتى 5 سنوات (1,500 روبل) ورد مرتين في المصدر: تحت غرفة Standard وضمن الإقامة الإضافية؛ يُعرض هنا مرة واحدة."],
    "booking_notes_en": ["The child-up-to-5 charge (1,500 RUB) appears twice in the source: under the Standard room and under additional stay; shown once here."],
    "periods": [period("p1", "الفترة", "Period", "1 سبتمبر – 30 ديسمبر 2026", "1 Sep – 30 Dec 2026", [
        room("Standard", [row(633, "1 person", "with", 629), row(634, "2 persons", "with", 629)], 631),
        room("Premium", [row(639, "1 person", "with", 629), row(640, "2 persons", "with", 629)], 637, qualifier_ar="مع الإطلالة", qualifier_en="With view"),
    ], 627, (627,), end_iso="2026-12-30", start_iso="2026-09-01")],
    "extras": [
        extra("child", "طفل حتى 5 سنوات", "Child up to 5 years", "ورد تحت غرفة Standard وضمن الإقامة الإضافية", "Listed under the Standard room and under additional stay", [635, 644]),
        extra("child", "طفل من 6 إلى 12 سنة", "Child 6–12 years", "إقامة إضافية", "Additional stay", [645]),
        extra("adult", "بالغ من 13 سنة", "Adult from 13 years", "إقامة إضافية", "Additional stay", [646]),
    ],
})

# 11 --------------------------------------------------------------- Corinthia
hotels.append({
    "id": "corinthia", "city": "spb", "order": 11,
    "name_en": "Corinthia Hotel", "name_ar": "فندق كورنثيا",
    "name_lines": [648, 650], "stars": 5, "stars_line": 650, "economy": False,
    "facts_ar": ["سانت بطرسبرغ", "خمس نجوم (وفق المصدر)", "جميع الأسعار شاملة الإفطار"],
    "facts_en": ["Saint Petersburg", "Five-star (as stated in the source)", "All rates include breakfast"],
    "booking_notes_ar": ["لم يذكر المصدر إضافات أو أسعار سرير إضافي أو أطفال لهذا الفندق."],
    "booking_notes_en": ["The source gives no extras, extra-bed or child rates for this hotel."],
    "periods": [
        period("p1", "الفترة الأولى", "Period 1", "1 سبتمبر – 10 أكتوبر 2026", "1 Sep – 10 Oct 2026", [
            room("Superior", [row(660, "1 person", "with", 652), row(661, "2 persons", "with", 652)], 658),
            room("Deluxe Room", [row(665, "1 person", "with", 652), row(666, "2 persons", "with", 652)], 663),
        ], 654, (656,), end_iso="2026-10-10", start_iso="2026-09-01"),
        period("p2", "الفترة الثانية", "Period 2", "11 أكتوبر – 29 ديسمبر 2026", "11 Oct – 29 Dec 2026", [
            room("Superior", [row(674, "1 person", "with", 652), row(675, "2 persons", "with", 652)], 672),
            room("Deluxe Room", [row(679, "1 person", "with", 652), row(680, "2 persons", "with", 652)], 677),
        ], 668, (670,), end_iso="2026-12-29", start_iso="2026-10-11"),
    ],
    "extras": [],
})

# star / economy wording check
for h in hotels:
    if h["stars"] == 5 and "خمس نجوم" not in L(h["stars_line"]):
        sys.exit(f"{h['id']}: five-star not in line {h['stars_line']}")
    if h["stars"] == 4 and "أربع نجوم" not in L(h["stars_line"]):
        sys.exit(f"{h['id']}: four-star not in line")
    if h["stars"] is None and "نجوم" in L(h["name_lines"][1]):
        sys.exit(f"{h['id']}: stars present in source but not recorded")
    if h["name_en"].split(" ")[0].replace("The", "The") not in L(h["name_lines"][0]):
        sys.exit(f"{h['id']}: English name line mismatch")
    if h["name_ar"] not in L(h["name_lines"][1]):
        sys.exit(f"{h['id']}: Arabic name not found verbatim in line {h['name_lines'][1]}")

# ---- coverage check: every line in the hotel data block with a RUB figure must be used once
used = {}
for h in hotels:
    for p in h["periods"]:
        for r in p["rooms"]:
            for x in r["rows"]:
                used[x["source_line_no"]] = used.get(x["source_line_no"], 0) + 1
    for e in h["extras"]:
        for n in e["source_line_nos"]:
            used[n] = used.get(n, 0) + 1
price_lines = [i for i in range(124, 684) if re.search(r"\d\s*روبل", L(i))]
missing = [i for i in price_lines if i not in used]
dupes = [i for i, c in used.items() if c > 1]
if missing or dupes:
    sys.exit(f"coverage failure: unused price lines {missing}; used twice {dupes}")

# ---- anomalies / notes for confirmation -------------------------------------
anomalies = [
    {"id": "A01", "print": True, "hotels": ["marriott-royal-aurora", "national", "corinthia", "ararat-park"],
     "ar": "فترات انتهت قبل 15 نوفمبر 2026: ماريوت الفترة الأولى، ناشيونال الفترة الأولى، كورنثيا الفترة الأولى، والجزء الأول من عرض الخريف في أرارات بارك. تنتهي قريباً: ماريوت وناشيونال الفترة الثانية (19 نوفمبر)، عرض الخريف في أرارات (25 نوفمبر)، كوسموس أربات وإنتركونتيننتال («نهاية نوفمبر»).",
     "en": "Periods ended before 15 Nov 2026: Marriott period 1, National period 1, Corinthia period 1, first range of the Ararat autumn offer. Ending soon: Marriott and National period 2 (19 Nov), Ararat autumn (25 Nov), Cosmos Arbat and InterContinental ('end of November')."},
    {"id": "A02", "print": True, "hotels": ["marriott-royal-aurora"],
     "ar": "ماريوت، الفترة الثانية، Deluxe King / Twin مع إفطار لشخصين: 17,000 — أعلى بـ 3,000 من سعر الإفطار لشخص، والفرق 1,500 في بقية الصفوف.",
     "en": "Marriott period 2, Deluxe King / Twin with breakfast for 2: 17,000 — 3,000 above breakfast for 1; the step is 1,500 in all other rows."},
    {"id": "A03", "print": True, "hotels": ["national"],
     "ar": "ناشيونال، الفترة الثانية، Classic King / Twin مع إفطار لشخصين: 15,300 — أعلى بـ 1,000 من سعر الإفطار لشخص، والفرق 1,500 في بقية الصفوف.",
     "en": "National period 2, Classic King / Twin with breakfast for 2: 15,300 — 1,000 above breakfast for 1; the step is 1,500 in other rows."},
    {"id": "A04", "print": True, "hotels": ["national"],
     "ar": "ناشيونال، الفترة الثانية، Kremlin Suite مع إفطار لشخص: 54,300، مقابل 55,300 في الفترتين الأولى والثالثة.",
     "en": "National period 2, Kremlin Suite with breakfast for 1: 54,300, against 55,300 in periods 1 and 3."},
    {"id": "A05", "print": True, "hotels": ["ararat-park"],
     "ar": "أرارات بارك، عرض الخريف: فرق الإفطار في Park City View (شخص واحد وشخصان) وفي Park King / Twin لشخصين يختلف عن بقية الغرف والفترات.",
     "en": "Ararat autumn offer: the breakfast step for Park City View (1 and 2 persons) and Park King / Twin (2 persons) differs from the other rooms and periods."},
    {"id": "A06", "print": True, "hotels": ["ararat-park"],
     "ar": "أرارات بارك: 25 نوفمبر و21 ديسمبر يقع كلٌّ منهما في فترتين؛ و24 – 29 أكتوبر بلا سعر.",
     "en": "Ararat: 25 Nov and 21 Dec each fall in two periods; 24–29 Oct has no rate."},
    {"id": "A07", "print": True, "hotels": ["garden-plaza"],
     "ar": "جاردن بلازا: سعر Suite واحد مع الإفطار وبدونه؛ أسعار Club Junior Suite مطابقة لـ Suite؛ Standard بدون إفطار (10,000) بلا إشغال؛ لا أسعار بدون إفطار لـ Club Premium وClub Junior Suite.",
     "en": "Garden Plaza: Suite rate identical with and without breakfast; Club Junior Suite rates equal Suite; Standard without breakfast (10,000) has no occupancy; no room-only rates for Club Premium and Club Junior Suite."},
    {"id": "A08", "print": True, "hotels": ["cosmos-arbat"],
     "ar": "كوسموس أربات: الإفطار غير مذكور لـ Superior ولـ Deluxe في ديسمبر؛ إضافة الإفطار (1,800) لم يُذكر هل تسري في ديسمبر وهل هي للشخص؛ الإشغال وبداية الفترة الأولى غير مذكورين.",
     "en": "Cosmos Arbat: breakfast not stated for Superior or for December Deluxe; not stated whether the 1,800 breakfast supplement applies in December or per person; occupancy and first-period start not stated."},
    {"id": "A09", "print": True, "hotels": ["intercontinental"],
     "ar": "إنتركونتيننتال: الإفطار والإشغال غير مذكورين للسعر الأساسي؛ «نهاية نوفمبر» بلا تاريخ دقيق؛ لا أسعار بعد 18 ديسمبر.",
     "en": "InterContinental: breakfast and occupancy not stated for the base rate; 'end of November' has no exact date; no rates after 18 Dec."},
    {"id": "A10", "print": True, "hotels": ["safmar-grand"],
     "ar": "سافمار جراند: سعر ثلاثة أشخاص مع سرير إضافي (13,800) لا يساوي سعر شخصين (10,300) + السرير الإضافي (1,500) + فطور الشخص الثالث (1,500).",
     "en": "Safmar Grand: 3 persons with extra bed (13,800) does not equal 2 persons (10,300) + extra bed (1,500) + third-person breakfast (1,500)."},
    {"id": "A11", "print": True, "hotels": ["cosmos-royal-nevsky"],
     "ar": "كوسموس رويال نيفسكي: «طفل حتى 5 سنوات: 1,500» مذكور مرتين (تحت Standard وضمن الإقامة الإضافية) ويُعرض مرة واحدة؛ لم يُذكر هل ينطبق على Premium.",
     "en": "Cosmos Royal Nevsky: 'child up to 5: 1,500' is listed twice (under Standard and under additional stay) and shown once; not stated whether it applies to Premium."},
    {"id": "A12", "print": True, "hotels": ["st-regis", "garden-plaza", "brosko"],
     "ar": "بلا تواريخ صلاحية في المصدر: سانت ريجيس، جاردن بلازا، بروسكو.",
     "en": "No validity dates in the source: St. Regis, Garden Plaza, Brosko."},
    {"id": "A13", "print": True, "hotels": ["st-regis", "cosmos-arbat", "intercontinental", "marriott-royal-aurora", "national", "brosko"],
     "ar": "الإشغال غير مذكور: سانت ريجيس، كوسموس أربات، إنتركونتيننتال؛ وفي ماريوت وناشيونال وبروسكو يرد «مع إفطار لشخص / لشخصين» فقط.",
     "en": "Occupancy not stated: St. Regis, Cosmos Arbat, InterContinental; Marriott, National and Brosko give only 'with breakfast for 1 / for 2'."},
    {"id": "A14", "print": True, "hotels": ["st-regis"],
     "ar": "سانت ريجيس: السرير الإضافي (5,000) مذكور تحت Deluxe؛ لم يُذكر هل يشمل Superior وهل هو لليلة.",
     "en": "St. Regis: extra bed (5,000) listed under Deluxe; not stated whether it applies to Superior or is per night."},
    {"id": "A15", "print": True, "hotels": ["marriott-royal-aurora"],
     "ar": "ماريوت: لا أسعار بدون إفطار لـ Junior Suite وCorner Suite؛ السرير الإضافي بلا سعر؛ 30 ديسمبر – 8 يناير عند الطلب.",
     "en": "Marriott: no room-only rates for Junior Suite and Corner Suite; extra bed has no fee; 30 Dec – 8 Jan on request."},
    {"id": "A16", "print": True, "hotels": ["brosko"],
     "ar": "بروسكو: «Brosko Hotels Group» اسم مجموعة، والفندق المحدد غير مسمّى؛ أسعار Standard Double وStandard Twin متطابقة.",
     "en": "Brosko: 'Brosko Hotels Group' is a group name and the specific property is not named; Standard Double and Standard Twin rates are identical."},
    {"id": "A17", "print": True, "hotels": ["garden-plaza", "ararat-park", "cosmos-arbat"],
     "ar": "تصنيف النجوم غير مذكور: جاردن بلازا، أرارات بارك، كوسموس أربات (غير مشمولة في مقارنة الخمس نجوم).",
     "en": "Star rating not stated: Garden Plaza, Ararat Park, Cosmos Arbat (excluded from the five-star comparison)."},
    {"id": "A18", "print": True, "hotels": ["national", "safmar-grand"],
     "ar": "ناشيونال: لا أسعار بعد 22 ديسمبر. سافمار: 29 ديسمبر – 10 يناير عند الطلب.",
     "en": "National: no rates after 22 Dec. Safmar: 29 Dec – 10 Jan on request."},
    {"id": "A19", "print": False, "hotels": [],
     "ar": "اسم الوكالة كُتب في رسالة العميل «والسياحية»؛ اعتُمد «والسياحة» افتراضاً، والاسم الإنجليزي «Hikayat Moscow Travel & Tourism» افتراض؛ لا شعار ولا بيانات تواصل. (ملاحظة داخلية — لا تُطبع في الكتالوج.)",
     "en": "Agency name typed «والسياحية»; «والسياحة» assumed; English name 'Hikayat Moscow Travel & Tourism' assumed; no logo or contact details. (Internal — not printed in the catalogue.)"},
]

general_terms = {
    "ar": [
        "جميع الأسعار بالروبل الروسي كما وردت من العميل، ولليلة الواحدة ما لم يُذكر خلاف ذلك.",
        "السعر بالريال السعودي = السعر بالروبل ÷ 21.4، مقرّباً إلى منزلتين عشريتين؛ دون أي عمولة أو هامش ربح أو زيادة.",
        "الأسعار سارية خلال الفترات المذكورة لكل فندق فقط؛ وحيث لا تُذكر فترة يُشار إلى ذلك صراحة.",
        "رسوم السرير الإضافي والأطفال والإفطار الإضافي منفصلة عن سعر الغرفة وتظهر في جدول الإضافات.",
        "الأسعار المعلّمة «عند الطلب» تُؤكَّد عند الحجز.",
    ],
    "en": [
        "All prices are in Russian roubles as supplied by the client, per night unless stated otherwise.",
        "SAR = RUB ÷ 21.4, rounded to two decimals; no commission, margin or mark-up.",
        "Rates apply only within the periods stated for each hotel; where no period is stated, this is said explicitly.",
        "Extra-bed, child and additional-breakfast charges are separate from the room rate and shown in the extras table.",
        "Rates marked 'on request' are confirmed at booking.",
    ],
    "source_line_nos": [126, 38, 41, 46, 50],
}

data = {
    "meta": {
        "title_en": "RUSSIA HOTEL COLLECTION 2026",
        "title_ar": "دليل فنادق موسكو وسانت بطرسبرغ 2026",
        "subtitle_en": "Moscow & Saint Petersburg",
        "subtitle_ar": "دليل أسعار الفنادق والإقامة السياحية",
        "agency_ar": "حكايات موسكو للسفر والسياحة",
        "agency_ar_as_typed": L(1).replace("اعطيني كالتلوج اسمو ", ""),
        "agency_en_assumed": "Hikayat Moscow Travel & Tourism",
        "source_file": "_originals/client-brief-and-rates_2026-11-15.txt",
        "prepared": "2026-11-15",
        "rate_sar_to_rub": "21.4", "rate_line": L(38),
        "formula": "SAR = RUB / 21.4, ROUND_HALF_UP to 2 decimals",
        "currency_note": L(126),
        "cities": {"moscow": {"ar": "موسكو", "en": "Moscow", "line": 128}, "spb": {"ar": "سانت بطرسبرغ", "en": "Saint Petersburg", "line": 621}},
    },
    "hotels": hotels,
    "anomalies": anomalies,
    "general_terms": general_terms,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
n_rooms = sum(len(p["rooms"]) for h in hotels for p in h["periods"])
n_rows = sum(len(r["rows"]) for h in hotels for p in h["periods"] for r in p["rooms"])
n_per = sum(len(h["periods"]) for h in hotels)
n_ext = sum(len(h["extras"]) for h in hotels)
print(f"hotels={len(hotels)} periods={n_per} room-tables(room x period)={n_rooms} price_rows={n_rows} extras={n_ext} price_lines_in_source={len(price_lines)}")
