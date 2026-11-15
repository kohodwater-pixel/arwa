"""Shared data access, formatting and analysis for the Russia Hotel Collection 2026.

All three outputs (HTML/PDF, DOCX, XLSX) import this module so that every table,
every comparison and every number comes from data/rates.json through the same code.
No price is created here: analysis tables only select existing rows.
"""
import json, pathlib
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "rates.json").read_text(encoding="utf-8"))
RATE = Decimal(DATA["meta"]["rate_sar_to_rub"])
AS_OF = date(2026, 11, 15)
CITY_ORDER = ["moscow", "spb"]


def sar_of(rub):
    return str((Decimal(rub) / RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def fmt_rub(rub):
    return f"{rub:,}"


def fmt_sar(s):
    d = Decimal(s)
    return f"{d:,.2f}"


def hotels(city=None):
    hs = sorted(DATA["hotels"], key=lambda h: h["order"])
    return [h for h in hs if city is None or h["city"] == city]


def hotel(hid):
    return next(h for h in DATA["hotels"] if h["id"] == hid)


def all_rows():
    """Yield (hotel, period, room, row) in catalogue order."""
    for h in hotels():
        for p in h["periods"]:
            for r in p["rooms"]:
                for x in r["rows"]:
                    yield h, p, r, x


def room_label_ar(r):
    s = r["name"]
    return s


def room_sub_ar(r):
    parts = []
    if r.get("qualifier_ar"):
        parts.append(r["qualifier_ar"])
    if r.get("size_m2"):
        parts.append(f"{r['size_m2']} م²")
    return "، ".join(parts)


def room_full_en(r):
    s = r["name"]
    if r.get("qualifier_en"):
        s += f" ({r['qualifier_en']})"
    if r.get("size_m2"):
        s += f", {r['size_m2']} m²"
    return s


def room_full_ar(r):
    sub = room_sub_ar(r)
    return r["name"] + (f" — {sub}" if sub else "")


def period_status(p):
    e = p.get("end_iso_derived")
    if not e:
        return None
    if date.fromisoformat(e) < AS_OF:
        return "ended"
    return None


def covers(p, d):
    """True if the period's derived dates include day d. Unknown start = open start."""
    e = p.get("end_iso_derived")
    if not e:
        return False
    s = p.get("start_iso_derived")
    if s and date.fromisoformat(s) > d:
        return False
    return d <= date.fromisoformat(e)


def stars_ar(n):
    return {5: "خمس نجوم", 4: "أربع نجوم"}.get(n, "")


def stars_en(n):
    return {5: "Five-star", 4: "Four-star"}.get(n, "")


# ---- comparison bases ---------------------------------------------------
def is_two_with_bf(x):
    return (x["occupancy"] in ("2 persons", "double") and x["breakfast"] == "with") or x["breakfast"] == "with breakfast for 2"


def is_one_with_bf(x):
    return (x["occupancy"] in ("1 person", "single") and x["breakfast"] == "with") or x["breakfast"] == "with breakfast for 1"


def basis_text_ar(x):
    return f"{x['occupancy_ar']} · {x['breakfast_ar']}"


def basis_text_en(x):
    return f"{x['occupancy_en']} · {x['breakfast_en']}"


def _row(h, p, r, x, extra_ar=None, extra_en=None):
    return {
        "hotel_ar": h["name_ar"], "hotel_en": h["name_en"], "hotel_id": h["id"],
        "city_ar": DATA["meta"]["cities"][h["city"]]["ar"], "city_en": DATA["meta"]["cities"][h["city"]]["en"],
        "period_ar": p["label_ar"], "period_en": p["label_en"], "dates_ar": p["dates_ar"], "dates_en": p["dates_en"],
        "room": r["name"], "room_ar": room_full_ar(r), "room_en": room_full_en(r),
        "occupancy_ar": x["occupancy_ar"], "occupancy_en": x["occupancy_en"],
        "breakfast_ar": x["breakfast_ar"], "breakfast_en": x["breakfast_en"],
        "basis_ar": basis_text_ar(x), "basis_en": basis_text_en(x),
        "rub": x["rub"], "sar": x["sar"], "note_ar": extra_ar, "note_en": extra_en,
    }


def lowest(rows):
    """rows: list of (h,p,r,x). Return all rows sharing the minimum RUB."""
    if not rows:
        return []
    m = min(x["rub"] for _, _, _, x in rows)
    return [t for t in rows if t[3]["rub"] == m]


REF_A = date(2026, 11, 18)
REF_B = date(2026, 12, 10)
EQUIV_AR = "يُعامل «مع إفطار لشخصين» معاملة «شخصان مع الإفطار»، و«مع إفطار لشخص» معاملة «شخص واحد مع الإفطار»، لأن المصدر لا يذكر الإشغال صراحة في هذه الفنادق."
EQUIV_EN = "'With breakfast for 2' is treated as '2 persons with breakfast' and 'with breakfast for 1' as '1 person with breakfast', because the source does not state occupancy for those hotels."
DATE_AR = "حيث يقول المصدر «نهاية نوفمبر» اعتُبر 30 نوفمبر لأغراض المقارنة فقط."
DATE_EN = "Where the source says 'end of November', 30 November is used for comparison purposes only."


def ar_date(d):
    months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
    return f"{d.day} {months[d.month-1]} {d.year}"


def en_date(d):
    return d.strftime("%-d %b %Y")


def analyses():
    """Return a list of analysis sections. Each: key, title_ar/en, basis_ar/en (list), tables: [ {caption_ar, caption_en, columns, rows} ], notes_ar/en."""
    out = []

    # 1. Economy -----------------------------------------------------------
    eco = [h for h in hotels() if h.get("economy")]
    rows = []
    for h in eco:
        for p in h["periods"]:
            for r in p["rooms"]:
                for x in r["rows"]:
                    rows.append(_row(h, p, r, x))
    out.append({
        "key": "economy", "n": 1,
        "title_ar": "مقارنة الفنادق الاقتصادية", "title_en": "Economy hotels",
        "basis_ar": [f"الفنادق المشمولة: ما يصفه المصدر صراحةً بأنه «اقتصادي» فقط — {'، '.join(h['name_ar'] for h in eco)}.",
                     "لا يوجد في المصدر فندق اقتصادي ثانٍ، لذلك لا تُجرى مقارنة بين فنادق؛ يُعرض هنا سلّم أسعار غرف الفندق نفسه.",
                     "الفترة: لم تُحدَّد في المصدر. الإشغال: غير مذكور. الإفطار: كما هو في كل صف."],
        "basis_en": [f"Included: only hotels the source itself calls economy — {', '.join(h['name_en'] for h in eco)}.",
                     "The source names no second economy hotel, so no hotel-to-hotel comparison is possible; this table shows that hotel's own rate ladder.",
                     "Period: not stated in the source. Occupancy: not stated. Breakfast: as shown per row."],
        "tables": [{"caption_ar": eco[0]["name_ar"] if eco else "", "caption_en": eco[0]["name_en"] if eco else "",
                    "cols": ["room", "breakfast", "rub", "sar"], "rows": rows}],
    })

    # 2. Five-star ----------------------------------------------------------
    five = [h for h in hotels() if h.get("stars") == 5]
    t_two, t_one, excluded = [], [], []
    for h in five:
        cand2 = [(h, p, r, x) for p in h["periods"] if covers(p, REF_B) for r in p["rooms"] for x in r["rows"] if is_two_with_bf(x)]
        cand1 = [(h, p, r, x) for p in h["periods"] if covers(p, REF_B) for r in p["rooms"] for x in r["rows"] if is_one_with_bf(x)]
        if not cand2 and not cand1:
            excluded.append(h)
        for t in lowest(cand2):
            t_two.append(_row(*t))
        for t in lowest(cand1):
            t_one.append(_row(*t))
    t_two.sort(key=lambda r: Decimal(r["sar"]))
    t_one.sort(key=lambda r: Decimal(r["sar"]))
    excl_ar = "، ".join(h["name_ar"] for h in excluded)
    excl_en = ", ".join(h["name_en"] for h in excluded)
    out.append({
        "key": "five_star", "n": 2,
        "title_ar": "مقارنة فنادق الخمس نجوم", "title_en": "Five-star hotels",
        "basis_ar": [f"الفنادق المشمولة: ما يذكر المصدر أنه خمس نجوم فقط ({len(five)} فنادق).",
                     f"أساس المقارنة: أقل سعر مُدخل لكل فندق، صالح في تاريخ {ar_date(REF_B)}، مع الإفطار؛ جدول لشخصين وجدول لشخص واحد. الترتيب تصاعدي بالريال داخل الجدول الواحد فقط.",
                     EQUIV_AR,
                     f"غير مشمول: {excl_ar} — لا يوجد له سعر مع إفطار بإشغال محدد صالح في هذا التاريخ (أو لا تواريخ له في المصدر)." if excluded else ""],
        "basis_en": [f"Included: only hotels the source states as five-star ({len(five)}).",
                     f"Basis: lowest rate entered per hotel valid on {en_date(REF_B)}, with breakfast; one table for two guests, one for one guest. Sorted by SAR within each table only.",
                     EQUIV_EN,
                     f"Not included: {excl_en} — no breakfast rate with a stated occupancy valid on that date (or no dates in the source)." if excluded else ""],
        "tables": [
            {"caption_ar": f"شخصان مع الإفطار — صالح في {ar_date(REF_B)}", "caption_en": f"Two guests with breakfast — valid on {en_date(REF_B)}",
             "cols": ["hotel", "room", "basis", "rub", "sar"], "rows": t_two},
            {"caption_ar": f"شخص واحد مع الإفطار — صالح في {ar_date(REF_B)}", "caption_en": f"One guest with breakfast — valid on {en_date(REF_B)}",
             "cols": ["hotel", "room", "basis", "rub", "sar"], "rows": t_one},
        ],
    })

    # 3. Lowest entered price per hotel --------------------------------------
    rows = []
    for h in hotels():
        cand = [(h, p, r, x) for p in h["periods"] for r in p["rooms"] for x in r["rows"]]
        for t in lowest(cand):
            rows.append(_row(*t))
    out.append({
        "key": "lowest", "n": 3,
        "title_ar": "أقل سعر مُدخل في كل فندق", "title_en": "Lowest rate entered per hotel",
        "basis_ar": ["أقل رقم بالروبل ورد في المصدر لكل فندق، مع فترته ونوع غرفته وإشغاله وحالة الإفطار كما وردت.",
                     "الأسس مختلفة بين الفنادق (المواسم والإشغال والإفطار)، لذلك لا يصلح هذا الجدول لترتيب الفنادق أو للقول إن فندقاً هو الأرخص.",
                     "عند تساوي أكثر من غرفة في أقل سعر تُعرض جميعها."],
        "basis_en": ["The lowest RUB figure in the source for each hotel, with its period, room, occupancy and breakfast as written.",
                     "Bases differ between hotels (season, occupancy, breakfast), so this table must not be used to rank hotels or to call any hotel the cheapest.",
                     "Where several rooms share the lowest rate, all are shown."],
        "tables": [{"caption_ar": "حسب ترتيب الفنادق في الكتالوج", "caption_en": "In catalogue order",
                    "cols": ["hotel", "period", "room", "basis", "rub", "sar"], "rows": rows}],
    })

    # 4. Double / two persons with breakfast, grouped by reference date ------
    tables = []
    for d in (REF_A, REF_B):
        rows = []
        for h in hotels():
            cand = [(h, p, r, x) for p in h["periods"] if covers(p, d) for r in p["rooms"] for x in r["rows"] if is_two_with_bf(x)]
            for t in lowest(cand):
                rows.append(_row(*t))
        rows.sort(key=lambda r: Decimal(r["sar"]))
        tables.append({"caption_ar": f"أسعار صالحة في {ar_date(d)}", "caption_en": f"Rates valid on {en_date(d)}",
                       "cols": ["hotel", "period", "room", "basis", "rub", "sar"], "rows": rows})
    rows = []
    for h in hotels():
        nd = [p for p in h["periods"] if not p.get("end_iso_derived")]
        cand = [(h, p, r, x) for p in nd for r in p["rooms"] for x in r["rows"] if is_two_with_bf(x)]
        for t in lowest(cand):
            rows.append(_row(*t))
    rows.sort(key=lambda r: Decimal(r["sar"]))
    tables.append({"caption_ar": "فنادق بلا تواريخ صلاحية في المصدر (لا تُقارن بالجدولين أعلاه)", "caption_en": "Hotels with no validity dates in the source (not comparable with the tables above)",
                   "cols": ["hotel", "room", "basis", "rub", "sar"], "rows": rows})
    out.append({
        "key": "double_bf", "n": 4,
        "title_ar": "الغرف المزدوجة / شخصان مع الإفطار", "title_en": "Double rooms / two persons with breakfast",
        "basis_ar": ["لكل فندق: أقل سعر مُدخل لشخصين أو لغرفة مزدوجة مع الإفطار، ضمن الفترة التي تشمل التاريخ المرجعي.",
                     f"مجموعتان متداخلتان زمنياً: {ar_date(REF_A)} و{ar_date(REF_B)}؛ ثم الفنادق التي لا تواريخ لها. الترتيب تصاعدي داخل كل مجموعة فقط.",
                     EQUIV_AR + " " + DATE_AR,
                     "الفنادق التي لا يذكر المصدر لها سعراً لشخصين مع الإفطار (سانت ريجيس، كوسموس أربات، إنتركونتيننتال) لا تظهر هنا."],
        "basis_en": ["Per hotel: the lowest rate entered for two persons or a double room with breakfast, in the period covering the reference date.",
                     f"Two overlapping groups: {en_date(REF_A)} and {en_date(REF_B)}; then hotels with no dates. Sorted within each group only.",
                     EQUIV_EN + " " + DATE_EN,
                     "Hotels with no two-person breakfast rate in the source (St. Regis, Cosmos Arbat, InterContinental) do not appear."],
        "tables": tables,
    })

    # 5. Suites -------------------------------------------------------------
    rows = []
    for h in hotels():
        names = []
        for p in h["periods"]:
            for r in p["rooms"]:
                if "Suite" in r["name"] and r["name"] not in names:
                    names.append(r["name"])
        for n in names:
            cand = [(h, p, r, x) for p in h["periods"] for r in p["rooms"] if r["name"] == n for x in r["rows"]]
            lows = lowest(cand)
            lo = lows[0]
            np_ = len({p["key"] for (_, p, _, _) in cand})
            na = f"{len(cand)} أسعار في {np_} فترات" if np_ > 1 else f"{len(cand)} أسعار"
            ne = f"{len(cand)} rates in {np_} periods" if np_ > 1 else f"{len(cand)} rates"
            if len(lows) > 1:
                na += f"؛ السعر نفسه في {len(lows)} صفوف"
                ne += f"; same rate in {len(lows)} rows"
            rows.append(_row(*lo, extra_ar=na, extra_en=ne))
    out.append({
        "key": "suites", "n": 5,
        "title_ar": "الفنادق التي توفر أجنحة", "title_en": "Hotels offering suites",
        "basis_ar": ["الغرف التي يحمل اسمها في المصدر كلمة Suite. يُعرض لكل جناح أقل سعر مُدخل مع أساسه، وعدد أسعاره في الكتالوج.",
                     "هذا جرد للأجنحة وليس مقارنة؛ الأسس مختلفة."],
        "basis_en": ["Rooms whose name in the source contains 'Suite'. For each suite: the lowest rate entered with its basis, and how many rates it has in the catalogue.",
                     "This is an inventory, not a comparison; the bases differ."],
        "tables": [{"caption_ar": "حسب ترتيب الفنادق", "caption_en": "In catalogue order",
                    "cols": ["hotel", "room", "period", "basis", "rub", "sar", "note"], "rows": rows}],
    })

    # 6. Extra bed ----------------------------------------------------------
    rows = []
    for h in hotels():
        for e in h["extras"]:
            if e["kind"] == "extra_bed":
                rows.append({"hotel_ar": h["name_ar"], "hotel_en": h["name_en"], "item_ar": e["item_ar"], "item_en": e["item_en"],
                             "condition_ar": e["condition_ar"], "condition_en": e["condition_en"],
                             "rub": e["rub"], "sar": e["sar"], "value_ar": e["value_ar"], "value_en": e["value_en"]})
    out.append({
        "key": "extra_bed", "n": 6,
        "title_ar": "الفنادق التي تسمح بسرير إضافي", "title_en": "Hotels allowing an extra bed",
        "basis_ar": ["الفنادق التي يذكر المصدر لها «سريراً إضافياً»، مع الرسم وشروطه كما وردت.",
                     "أرارات بارك: يذكر أسعاراً لثلاثة أشخاص في Park Deluxe وPark Suite دون ذكر سرير إضافي. كوسموس رويال نيفسكي: يذكر «إقامة إضافية» للأطفال والبالغين دون ذكر سرير. كورنثيا وكوسموس أربات: لا ذكر للسرير الإضافي."],
        "basis_en": ["Hotels for which the source mentions an extra bed, with the fee and conditions as written.",
                     "Ararat Park gives 3-person rates for Park Deluxe and Park Suite without mentioning an extra bed. Cosmos Royal Nevsky gives 'additional stay' charges for children and adults without mentioning a bed. Corinthia and Cosmos Arbat: no extra bed mentioned."],
        "tables": [{"caption_ar": "حسب ترتيب الفنادق", "caption_en": "In catalogue order",
                    "cols": ["hotel", "condition", "rub", "sar"], "rows": rows, "kind": "extras"}],
    })

    # 7. Moscow vs Saint Petersburg -----------------------------------------
    tables = []
    for city in CITY_ORDER:
        rows = []
        for h in hotels(city):
            if h.get("stars") != 5:
                continue
            cand = [(h, p, r, x) for p in h["periods"] if covers(p, REF_B) for r in p["rooms"] for x in r["rows"] if is_two_with_bf(x)]
            for t in lowest(cand):
                rows.append(_row(*t))
        rows.sort(key=lambda r: Decimal(r["sar"]))
        c = DATA["meta"]["cities"][city]
        tables.append({"caption_ar": c["ar"], "caption_en": c["en"], "cols": ["hotel", "room", "basis", "rub", "sar"], "rows": rows})
    out.append({
        "key": "cities", "n": 7,
        "title_ar": "موسكو وسانت بطرسبرغ", "title_en": "Moscow and Saint Petersburg",
        "basis_ar": [f"أساس موحّد: فنادق خمس نجوم (وفق المصدر)، شخصان مع الإفطار، أقل سعر مُدخل لكل فندق صالح في {ar_date(REF_B)}.",
                     "لا يُحسب متوسط ولا فرق؛ تُعرض الأسعار كما هي جنباً إلى جنب. العيّنة صغيرة (فندقان فقط في سانت بطرسبرغ)، فلا تصلح لتعميم عن المدينتين.",
                     EQUIV_AR],
        "basis_en": [f"Common basis: five-star hotels (per the source), two persons with breakfast, lowest rate entered per hotel valid on {en_date(REF_B)}.",
                     "No averages or differences are computed; rates are shown side by side. The sample is small (two hotels in Saint Petersburg), so it does not support conclusions about the cities in general.",
                     EQUIV_EN],
        "tables": tables,
    })
    for a in out:
        a["basis_ar"] = [b for b in a["basis_ar"] if b]
        a["basis_en"] = [b for b in a["basis_en"] if b]
    return out


COLS = {
    "hotel": ("الفندق", "Hotel"), "period": ("الفترة", "Period"), "room": ("نوع الغرفة", "Room type"),
    "basis": ("الإشغال · الإفطار", "Occupancy · breakfast"), "breakfast": ("الإفطار", "Breakfast"),
    "rub": ("السعر بالروبل", "RUB"), "sar": ("السعر بالريال", "SAR"), "note": ("ملاحظة", "Note"),
    "condition": ("الشرط", "Condition"),
}
