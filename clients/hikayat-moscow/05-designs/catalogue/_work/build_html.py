#!/usr/bin/env python3
"""Build the catalogue HTML from data/rates.json (via catalogue_lib), with measured pagination.

Pass 1 writes _work/measure.html with every block at content width; measure.cjs returns
block heights; pass 2 packs blocks into A4 pages and writes the final HTML.
Also writes _work/pagemap.json (page numbers per hotel / section) for the DOCX index.
"""
import json, subprocess, sys, pathlib, html as H
import catalogue_lib as L

WORK = pathlib.Path(__file__).resolve().parent
ROOT = WORK.parent
VERSION = sys.argv[1] if len(sys.argv) > 1 else "v01"
OUT_HTML = ROOT / f"hikayat-moscow_russia-hotel-collection_catalogue_ar-en_{VERSION}.html"
D = L.DATA
M = D["meta"]
CONTENT_H = 249.0   # mm available inside .content
GAP = 6.5           # mm between blocks

# Client rule (2026-11-15): no credits or captions printed; only CC0 / public-domain images.
PHOTOS = {}   # no CC0/PD photo of any specific hotel could be obtained -> typographic name cards
CITY_PHOTOS = {
    "moscow": {"src": "assets/photos/moscow_kremlin-domes_chuanann_cc0.jpg"},
    "spb": {"src": "assets/photos/spb_st-isaacs-dome_aljuarez_cc0.jpg"},
}

e = H.escape


def ltr(s, cls=""):
    return f'<bdi dir="ltr" class="{cls}">{e(str(s))}</bdi>'


def rub_html(rub):
    return f'<bdi dir="ltr" class="rub">{L.fmt_rub(rub)}<span class="cur"> RUB</span></bdi>'


def sar_html(sar):
    return f'<bdi dir="ltr" class="sar">{L.fmt_sar(sar)}<span class="cur"> SAR</span></bdi>'


STAR = '<svg class="star" viewBox="0 0 20 20"><path d="M10 1.5l2.6 5.6 6.1.7-4.5 4.2 1.2 6-5.4-3-5.4 3 1.2-6L1.3 7.8l6.1-.7z"/></svg>'


def stars(n):
    return f'<span class="stars" title="{n}">{STAR * n}</span>' if n else ""


def th2(ar, en, cls=""):
    return f'<th class="{cls}"><span class="th-ar">{e(ar)}</span><span class="th-en">{e(en)}</span></th>'


CSS = """
@font-face{font-family:'IBM Plex Sans Arabic';src:url('assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Regular.ttf');font-weight:400}
@font-face{font-family:'IBM Plex Sans Arabic';src:url('assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Medium.ttf');font-weight:500}
@font-face{font-family:'IBM Plex Sans Arabic';src:url('assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-SemiBold.ttf');font-weight:600}
@font-face{font-family:'IBM Plex Sans Arabic';src:url('assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Bold.ttf');font-weight:700}
@font-face{font-family:'IBM Plex Sans Arabic';src:url('assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Light.ttf');font-weight:300}
@font-face{font-family:'Montserrat';src:url('assets/fonts/montserrat/montserrat-latin-400-normal.ttf');font-weight:400}
@font-face{font-family:'Montserrat';src:url('assets/fonts/montserrat/montserrat-latin-500-normal.ttf');font-weight:500}
@font-face{font-family:'Montserrat';src:url('assets/fonts/montserrat/montserrat-latin-600-normal.ttf');font-weight:600}
@font-face{font-family:'Montserrat';src:url('assets/fonts/montserrat/montserrat-latin-700-normal.ttf');font-weight:700}
@font-face{font-family:'Montserrat';src:url('assets/fonts/montserrat/montserrat-latin-300-normal.ttf');font-weight:300}
@font-face{font-family:'Playfair Display';src:url('assets/fonts/playfair-display/playfair-display-latin-400-normal.ttf');font-weight:400}
@font-face{font-family:'Playfair Display';src:url('assets/fonts/playfair-display/playfair-display-latin-500-normal.ttf');font-weight:500}
@font-face{font-family:'Playfair Display';src:url('assets/fonts/playfair-display/playfair-display-latin-600-normal.ttf');font-weight:600}
@font-face{font-family:'Playfair Display';src:url('assets/fonts/playfair-display/playfair-display-latin-700-normal.ttf');font-weight:700}
@font-face{font-family:'HM';src:url('assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Regular.ttf');font-weight:400}
@font-face{font-family:'HM';src:url('assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Medium.ttf');font-weight:500}
@font-face{font-family:'HM';src:url('assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-SemiBold.ttf');font-weight:600}
@font-face{font-family:'HM';src:url('assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Bold.ttf');font-weight:700}
@font-face{font-family:'HM';src:url('assets/fonts/ibmplexsansarabic/IBMPlexSansArabic-Light.ttf');font-weight:300}
@font-face{font-family:'HM';src:url('assets/fonts/montserrat/montserrat-latin-300-normal.ttf');font-weight:300;unicode-range:U+0021-007E,U+00A1-00FF,U+2010-2027,U+2030-205E,U+20AC,U+2122}
@font-face{font-family:'HM';src:url('assets/fonts/montserrat/montserrat-latin-400-normal.ttf');font-weight:400;unicode-range:U+0021-007E,U+00A1-00FF,U+2010-2027,U+2030-205E,U+20AC,U+2122}
@font-face{font-family:'HM';src:url('assets/fonts/montserrat/montserrat-latin-500-normal.ttf');font-weight:500;unicode-range:U+0021-007E,U+00A1-00FF,U+2010-2027,U+2030-205E,U+20AC,U+2122}
@font-face{font-family:'HM';src:url('assets/fonts/montserrat/montserrat-latin-600-normal.ttf');font-weight:600;unicode-range:U+0021-007E,U+00A1-00FF,U+2010-2027,U+2030-205E,U+20AC,U+2122}
@font-face{font-family:'HM';src:url('assets/fonts/montserrat/montserrat-latin-700-normal.ttf');font-weight:700;unicode-range:U+0021-007E,U+00A1-00FF,U+2010-2027,U+2030-205E,U+20AC,U+2122}
:root{--navy:#14243A;--gold:#C6A66B;--ivory:#F7F4ED;--char:#292D32;--line:#E4DCCB;--muted:#5E6470;--goldtext:#8A6D32}
@page{size:210mm 297mm;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:'HM';color:var(--char);font-size:10pt;line-height:1.65;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.ar{font-family:'HM'}
bdi{unicode-bidi:isolate}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always;break-after:page;background:#fff}
.page:last-child{page-break-after:auto}
.content{position:absolute;top:24mm;bottom:22mm;right:18mm;left:18mm;overflow:hidden}
.rhead{position:absolute;top:11mm;right:18mm;left:18mm;height:7mm;border-bottom:0.3mm solid var(--gold);display:flex;justify-content:space-between;align-items:flex-end;padding-bottom:1.6mm}
.rhead .sec{font-size:9pt;color:var(--navy);font-weight:500}
.rhead .sec bdi{font-family:'Playfair Display';color:var(--goldtext);font-size:8.5pt;margin-right:2.5mm}
.rhead .brand{font-family:'Montserrat';font-size:7pt;letter-spacing:.24em;color:var(--muted);font-weight:500}
.rfoot{position:absolute;bottom:9mm;right:18mm;left:18mm;display:flex;justify-content:space-between;align-items:center;font-size:8.5pt;color:var(--muted)}
.rfoot .pn{font-family:'Playfair Display';font-size:11pt;color:var(--navy);border-top:0.3mm solid var(--gold);padding-top:1mm;min-width:10mm;text-align:center}
.block+.block{margin-top:6.5mm}
/* hotel header */
.hh{display:flex;background:var(--navy);color:var(--ivory);min-height:33mm;position:relative}
.hh .txt{flex:1;padding:4.5mm 7mm 4mm 7mm;display:flex;flex-direction:column;justify-content:center}
.hh .no{font-family:'Playfair Display';color:var(--gold);font-size:8.5pt;letter-spacing:.2em;margin-bottom:.5mm}
.hh .nar{font-size:19pt;font-weight:600;line-height:1.3}
.hh .nen{font-family:'Playfair Display';font-size:13pt;color:var(--gold);line-height:1.25}
.hh .rule{width:22mm;height:0.35mm;background:var(--gold);margin:2.5mm 0 1.8mm 0}
.hh .meta{font-size:9.5pt;line-height:1.4;color:#E9E3D6;display:flex;gap:4mm;align-items:center;flex-wrap:wrap}
.hh .side{width:44mm;border-inline-start:0.3mm solid rgba(198,166,107,.55);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2mm;padding:5mm}
.hh .side .city{font-family:'Playfair Display';font-size:10pt;letter-spacing:.16em;color:var(--gold);text-transform:uppercase}
.hh .side .cityar{font-size:11pt;color:var(--ivory)}
.hh .photo{width:62mm;position:relative;overflow:hidden}
.hh .photo img{width:100%;height:100%;object-fit:cover;display:block;position:absolute;inset:0}
.stars{display:inline-flex;gap:.9mm;vertical-align:middle}
.star{width:3.4mm;height:3.4mm;fill:var(--gold)}
.facts{margin-top:2.5mm;font-size:10pt;line-height:1.5;color:var(--char);display:flex;flex-wrap:wrap;gap:1.5mm 0}
.facts span+span:before{content:'';display:inline-block;width:1.2mm;height:1.2mm;background:var(--gold);transform:rotate(45deg);margin:0 3mm 0.6mm 3mm;vertical-align:middle}
.validity{margin-top:2mm;font-size:10pt;line-height:1.55;border-top:0.25mm solid var(--line);padding-top:2mm}
.validity b{color:var(--navy);font-weight:600}
.credit{font-size:8pt;color:var(--muted);margin-top:1.5mm}
/* continuation strip */
.hc{display:flex;justify-content:space-between;align-items:baseline;border-bottom:0.3mm solid var(--navy);padding-bottom:2mm}
.hc .nar{font-size:13pt;font-weight:600;color:var(--navy)}
.hc .nen{font-family:'Playfair Display';color:var(--goldtext);font-size:11pt}
.hc .cont{font-size:9pt;color:var(--muted);margin-inline-start:3mm;font-weight:400}
/* period block */
.ptitle{display:flex;align-items:baseline;gap:3mm;margin-bottom:2mm;line-height:1.4;flex-wrap:wrap}
.ptitle .pl{font-size:13pt;font-weight:600;color:var(--navy)}
.ptitle .pe{font-family:'Playfair Display';font-size:10.5pt;color:var(--goldtext)}
.ptitle .pd{font-size:10pt;color:var(--char);margin-inline-start:auto;border:0.25mm solid var(--gold);padding:0.4mm 3mm;border-radius:4mm;background:var(--ivory)}
.tag{font-size:8.5pt;color:#7A2E2E;border:0.25mm solid #C9A9A9;border-radius:3mm;padding:0 2.2mm;background:#FBF3F1}
table{width:100%;border-collapse:collapse;table-layout:fixed}
thead{display:table-header-group}
tr{break-inside:avoid}
th{background:var(--navy);color:var(--ivory);font-weight:600;text-align:right;padding:1.3mm 2.4mm 1.1mm;vertical-align:bottom;line-height:1.25}
th .th-ar{display:block;font-size:9.5pt}
th .th-en{display:block;font-family:'Montserrat';font-size:7pt;letter-spacing:.08em;color:var(--gold);font-weight:500;text-transform:uppercase;margin-top:.6mm}
th.c-sar{background:#0E1A2B;border-bottom:0.6mm solid var(--gold)}
th.c-num,td.c-num{text-align:left}
td{padding:0.9mm 2.4mm;border-bottom:0.2mm solid var(--line);vertical-align:middle;line-height:1.38;font-size:10pt}
td.room{border-bottom:0.3mm solid #CDBF9F;background:#FCFBF8}
tr.grp-end td{border-bottom:0.3mm solid #CDBF9F}
.rn{font-family:'Montserrat';font-weight:600;color:var(--navy);font-size:10pt;display:block;line-height:1.35}
.rs{display:block;font-size:9pt;color:var(--muted);line-height:1.4}
td.c-sar{background:var(--ivory);border-inline-end:0.6mm solid var(--gold)}
.rub{font-family:'Montserrat';font-size:10pt;color:#3B3F45;font-weight:400;white-space:nowrap}
.sar{font-family:'Montserrat';font-size:12pt;color:var(--navy);font-weight:600;white-space:nowrap}
.cur{font-size:7pt;letter-spacing:.06em;font-weight:500;color:var(--muted)}
.sar .cur{color:var(--goldtext);font-weight:600}
.ns{color:var(--muted)}
.val{font-size:10pt;color:var(--navy);font-weight:600;background:var(--ivory);border-inline-end:0.6mm solid var(--gold)}
.sect{font-size:12pt;line-height:1.4;font-weight:600;color:var(--navy);margin-bottom:2mm;display:flex;gap:3mm;align-items:baseline}
.sect bdi{font-family:'Playfair Display';color:var(--goldtext);font-size:10.5pt;font-weight:400}
ul.notes{list-style:none}
ul.notes li{position:relative;padding-inline-start:5mm;font-size:10pt;line-height:1.55;margin-bottom:.8mm}
ul.notes li:before{content:'';position:absolute;right:0;top:2.6mm;width:1.4mm;height:1.4mm;background:var(--gold);transform:rotate(45deg)}
.notesbox{background:var(--ivory);padding:3mm 4.5mm;border-inline-start:0.6mm solid var(--gold)}
/* cover */
.cover{background:var(--navy);color:var(--ivory)}
.cover .frame{position:absolute;inset:11mm;border:0.35mm solid rgba(198,166,107,.75)}
.cover .frame2{position:absolute;inset:13mm;border:0.2mm solid rgba(198,166,107,.35)}
.cover .inner{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 26mm}
.cover .kicker{font-family:'Montserrat';font-size:8.5pt;letter-spacing:.42em;color:var(--gold);font-weight:500}
.cover .t1{font-family:'Playfair Display';font-size:46pt;line-height:1.05;letter-spacing:.06em;margin-top:9mm}
.cover .t2{font-family:'Playfair Display';font-size:25pt;letter-spacing:.2em;line-height:1.2;margin-top:3mm}
.cover .yr{font-family:'Playfair Display';font-size:30pt;color:var(--gold);margin-top:6mm;letter-spacing:.2em}
.cover .rule{width:40mm;height:0.35mm;background:var(--gold);margin:9mm auto}
.cover .cities{font-family:'Playfair Display';font-size:15pt;letter-spacing:.06em}
.cover .tar{font-size:20pt;font-weight:600;margin-top:10mm;line-height:1.5}
.cover .sar_{font-size:13pt;color:var(--gold);margin-top:2mm;font-weight:400}
.cover .agency{position:absolute;bottom:26mm;left:0;right:0;text-align:center}
.cover .agency .a1{font-size:15pt;font-weight:600;color:var(--ivory)}
.cover .agency .a2{font-family:'Montserrat';font-size:8pt;letter-spacing:.3em;color:var(--gold);margin-top:1.5mm}
.cover .ed{position:absolute;top:24mm;left:0;right:0;text-align:center;font-size:9.5pt;color:#CFC6B4}
/* intro page */
.intro h1{font-size:19pt;font-weight:600;color:var(--navy);line-height:1.3}
.intro h1 bdi{display:block;text-align:right;font-family:'Playfair Display';font-size:13pt;color:var(--goldtext);font-weight:400}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:8mm}
.xbox{background:var(--navy);color:var(--ivory);padding:3.5mm 5mm}
.xbox .big{font-family:'Montserrat';font-size:21pt;font-weight:600;color:var(--gold);display:block;text-align:center;margin:1mm 0 2mm}
.xbox .f{font-size:10pt;line-height:1.6}
.xbox .f b{color:var(--gold);font-weight:600}
.h3{font-size:11.5pt;font-weight:600;color:var(--navy);border-bottom:0.3mm solid var(--gold);padding-bottom:1.2mm;margin-bottom:2mm;display:flex;justify-content:space-between;align-items:baseline}
.h3 bdi{font-family:'Playfair Display';font-weight:400;color:var(--goldtext);font-size:9.5pt}
table.legend td{font-size:9.5pt;padding:.7mm 1.6mm;line-height:1.3}
table.legend td.en{font-family:'Montserrat';font-size:8.5pt;color:var(--muted);text-align:left}
.idx{width:100%}
.idx .row{display:flex;align-items:baseline;gap:2mm;padding:.55mm 0;line-height:1.45;border-bottom:0.2mm dotted #CDBF9F;font-size:10pt}
.idx .row .n{font-family:'Playfair Display';color:var(--goldtext);width:6mm}
.idx .row .nm{flex:1}
.idx .row .nm bdi{font-family:'Montserrat';font-size:8pt;color:var(--muted);display:block;line-height:1.3}
.idx .row .pg{font-family:'Playfair Display';font-size:11pt;color:var(--navy)}
.idx .city{font-size:10.5pt;font-weight:600;color:var(--navy);margin:2mm 0 0;line-height:1.5}
.idx .city bdi{font-family:'Playfair Display';font-weight:400;color:var(--goldtext);font-size:9.5pt;margin-right:2.5mm}
/* section opener */
.opener .content{top:18mm}
.opener .ph{width:100%;height:84mm;overflow:hidden;position:relative}
.opener .ph img{width:100%;height:100%;object-fit:cover;display:block}
.opener .cap{font-size:8pt;color:var(--muted);margin-top:1.5mm;text-align:left;font-family:'Montserrat'}
.opener .num{font-family:'Playfair Display';color:var(--goldtext);letter-spacing:.3em;font-size:10pt;margin-top:9mm}
.opener .cn{font-size:40pt;font-weight:600;color:var(--navy);line-height:1.2;margin-top:1mm}
.opener .ce{font-family:'Playfair Display';font-size:22pt;color:var(--goldtext);letter-spacing:.18em;text-transform:uppercase}
.opener .rule{width:30mm;height:0.35mm;background:var(--gold);margin:5mm 0}
.opener .lst .row{display:flex;gap:3mm;align-items:baseline;padding:1.1mm 0;line-height:1.5;border-bottom:0.2mm solid var(--line);font-size:11pt}
.opener .lst .row bdi{font-family:'Playfair Display';color:var(--goldtext);font-size:10.5pt}
.opener .lst .row .pg{margin-inline-start:auto;font-family:'Playfair Display';color:var(--navy)}
/* analysis */
.ah .k{font-family:'Playfair Display';color:var(--goldtext);letter-spacing:.25em;font-size:9pt}
.ah h2{font-size:17pt;font-weight:600;color:var(--navy);line-height:1.35}
.ah h2 bdi{font-family:'Playfair Display';font-weight:400;font-size:12.5pt;color:var(--goldtext);margin-right:3.5mm}
.basis{margin-top:3mm;background:var(--ivory);border-inline-start:0.6mm solid var(--gold);padding:3mm 4.5mm}
.basis .lbl{font-size:9.5pt;font-weight:600;color:var(--navy);margin-bottom:.8mm}
.basis li{font-size:9.5pt;line-height:1.6;margin-inline-start:4mm}
.cap2{font-size:10.5pt;font-weight:600;color:var(--navy);margin-bottom:2mm;display:flex;gap:3mm;align-items:baseline}
.cap2 bdi{font-family:'Montserrat';font-size:8.5pt;color:var(--muted);font-weight:400}
.hn{font-size:10pt;font-weight:500;display:block;line-height:1.35}
.he{font-family:'Montserrat';font-size:8pt;color:var(--muted);display:block;line-height:1.3}
td.small{font-size:9.5pt}
.pp{display:block;font-weight:600;color:var(--navy);font-size:9.5pt}
/* notes page */
.nitem{display:flex;gap:3.5mm;font-size:10pt;line-height:1.7;padding:2mm 0;border-bottom:0.2mm solid var(--line)}
.nitem .id{font-family:'Playfair Display';color:var(--goldtext);min-width:9mm;font-size:10pt}
"""


def page(inner, sec_ar=None, sec_en=None, pn=None, cls=""):
    head = ""
    if sec_ar:
        head = f'<div class="rhead"><div class="sec">{e(sec_ar)}{ltr(sec_en) if sec_en else ""}</div><div class="brand">RUSSIA HOTEL COLLECTION 2026</div></div>'
    foot = ""
    if pn:
        foot = f'<div class="rfoot"><span>{e(M["agency_ar"])}</span><span class="pn">{pn}</span><span><bdi dir="ltr">1 SAR = 21.4 RUB</bdi></span></div>'
    return f'<section class="page {cls}">{head}<div class="content">{inner}</div>{foot}</section>'


# ---------------------------------------------------------------- blocks
def hotel_header(h, idx):
    city = M["cities"][h["city"]]
    meta = []
    if h.get("stars"):
        meta.append(f'{stars(h["stars"])}<span>{e(L.stars_ar(h["stars"]))}</span>')
    else:
        meta.append('<span>تصنيف النجوم غير مذكور في المصدر</span>')
    photo = PHOTOS.get(h["id"])
    side = (f'<div class="photo"><img src="{photo["src"]}" alt=""></div>' if photo else
            f'<div class="side"><span class="city">{e(city["en"])}</span><span class="cityar">{e(city["ar"])}</span></div>')
    head = (f'<div class="hh"><div class="txt"><div class="no">N° {idx:02d}</div>'
            f'<div class="nar">{e(h["name_ar"])}</div><div class="nen">{ltr(h["name_en"])}</div>'
            f'<div class="rule"></div><div class="meta">{"".join(meta)}</div></div>{side}</div>')
    facts = [f for f in h["facts_ar"] if "نجوم" not in f or "اقتصادي" in f]
    facts_html = f'<div class="facts">{"".join(f"<span>{e(f)}</span>" for f in facts)}</div>' if facts else ""
    vals = []
    for p in h["periods"]:
        if p.get("dates_as_written") is None and p["dates_ar"] == "لم تُحدَّد فترة الصلاحية في المصدر":
            vals.append(e(p["dates_ar"]))
        else:
            vals.append(f'{e(p["label_ar"])}: {e(p["dates_ar"])}')
    validity = f'<div class="validity"><b>الصلاحية:</b> {" · ".join(vals)}</div>'
    return head + facts_html + validity


def hotel_cont(h):
    return f'<div class="hc"><div><span class="nar">{e(h["name_ar"])}</span><span class="cont">— تابع</span></div><span class="nen">{ltr(h["name_en"])}</span></div>'


def rate_table(h, p):
    status = L.period_status(p)
    tag = '<span class="tag">فترة منتهية — تُعرض كما وردت</span>' if status == "ended" else ""
    title = (f'<div class="ptitle"><span class="pl">{e(p["label_ar"])}</span><span class="pe">{ltr(p["label_en"])}</span>{tag}'
             f'<span class="pd">{e(p["dates_ar"])}</span></div>')
    rows = []
    for r in p["rooms"]:
        n = len(r["rows"])
        sub = L.room_sub_ar(r)
        for i, x in enumerate(r["rows"]):
            cls = ' class="grp-end"' if i == n - 1 else ""
            tds = ""
            if i == 0:
                tds += f'<td class="room" rowspan="{n}"><span class="rn">{ltr(r["name"])}</span>' + (f'<span class="rs">{e(sub)}</span>' if sub else "") + "</td>"
            oc = "ns" if x["occupancy"] == "not stated" else ""
            bc = "ns" if x["breakfast"] == "not stated" else ""
            tds += f'<td class="{oc}">{e(x["occupancy_ar"])}</td><td class="{bc}">{e(x["breakfast_ar"])}</td>'
            tds += f'<td class="c-num">{rub_html(x["rub"])}</td><td class="c-num c-sar">{sar_html(x["sar"])}</td>'
            rows.append(f"<tr{cls}>{tds}</tr>")
    t = ('<table class="rates"><colgroup><col style="width:30%"><col style="width:17%"><col style="width:19%"><col style="width:16%"><col style="width:18%"></colgroup>'
         f'<thead><tr>{th2("نوع الغرفة","Room type")}{th2("الإشغال","Occupancy")}{th2("الإفطار","Breakfast")}{th2("السعر بالروبل","RUB","c-num")}{th2("السعر بالريال","SAR","c-num c-sar")}</tr></thead>'
         f'<tbody>{"".join(rows)}</tbody></table>')
    return title + t


def extras_table(h):
    if not h["extras"]:
        return '<div class="sect">الإضافات <bdi dir="ltr">Extras</bdi></div><div class="notesbox">لم يذكر المصدر أي إضافات لهذا الفندق.</div>'
    rows = []
    for x in h["extras"]:
        if x["rub"] is not None:
            price = f'<td class="c-num">{rub_html(x["rub"])}</td><td class="c-num c-sar">{sar_html(x["sar"])}</td>'
        else:
            price = f'<td colspan="2" class="val" style="text-align:center">{e(x["value_ar"])}</td>'
        rows.append(f'<tr><td>{e(x["item_ar"])}</td><td class="small">{e(x["condition_ar"])}</td>{price}</tr>')
    return ('<div class="sect">الإضافات ورسوم الأطفال <bdi dir="ltr">Extras &amp; children</bdi></div>'
            '<table class="extras"><colgroup><col style="width:27%"><col style="width:39%"><col style="width:16%"><col style="width:18%"></colgroup>'
            f'<thead><tr>{th2("البند","Item")}{th2("الشرط","Condition")}{th2("السعر بالروبل","RUB","c-num")}{th2("السعر بالريال","SAR","c-num c-sar")}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>')


def booking_notes(h):
    items = "".join(f"<li>{e(n)}</li>" for n in h["booking_notes_ar"])
    return f'<div class="sect">ملاحظات الحجز <bdi dir="ltr">Booking notes</bdi></div><div class="notesbox"><ul class="notes">{items}</ul></div>'


def analysis_head(a):
    lis = "".join(f"<li>{e(b)}</li>" for b in a["basis_ar"])
    return (f'<div class="ah"><div class="k">ANALYSIS {a["n"]:02d}</div><h2>{e(a["title_ar"])}{ltr(a["title_en"])}</h2>'
            f'<div class="basis"><div class="lbl">أساس المقارنة</div><ul>{lis}</ul></div></div>')


def hotel_cell(r):
    return f'<td><span class="hn">{e(r["hotel_ar"])}</span><span class="he">{ltr(r["hotel_en"])}</span></td>'


def analysis_table(a, t):
    cols = t["cols"]
    widths = {"hotel": 24, "room": 21, "basis": 20, "pbasis": 23, "breakfast": 22, "rub": 17, "sar": 20, "note": 14, "condition": 40}
    if t.get("kind") == "extras":
        widths = {"hotel": 30, "condition": 40, "rub": 17, "sar": 20}
    tot = sum(widths[c] for c in cols)
    colg = "".join(f'<col style="width:{widths[c]*100/tot:.1f}%">' for c in cols)
    hdr = "".join(th2(*L.COLS[c], cls=("c-num c-sar" if c == "sar" else "c-num" if c == "rub" else "")) for c in cols)
    body = []
    for r in t["rows"]:
        tds = ""
        for c in cols:
            if c == "hotel":
                tds += hotel_cell(r)
            elif c == "period":
                tds += f'<td class="small">{e(r["period_ar"])}</td>'
            elif c == "room":
                rs = r["room_ar"].split(" — ", 1)
                tds += f'<td><span class="rn">{ltr(rs[0])}</span>' + (f'<span class="rs">{e(rs[1])}</span>' if len(rs) > 1 else "") + "</td>"
            elif c == "basis":
                tds += f'<td class="small">{e(r["occupancy_ar"])}<br>{e(r["breakfast_ar"])}</td>'
            elif c == "pbasis":
                tds += f'<td class="small"><span class="pp">{e(r["period_short_ar"])}</span>{e(r["occupancy_ar"])} · {e(r["breakfast_ar"])}</td>'
            elif c == "breakfast":
                tds += f'<td>{e(r["breakfast_ar"])}</td>'
            elif c == "note":
                tds += f'<td class="small">{e(r.get("note_ar") or "")}</td>'
            elif c == "condition":
                tds += f'<td class="small">{e(r["condition_ar"])}</td>'
            elif c == "rub":
                tds += f'<td class="c-num">{rub_html(r["rub"])}</td>' if r["rub"] is not None else ""
            elif c == "sar":
                tds += f'<td class="c-num c-sar">{sar_html(r["sar"])}</td>' if r["sar"] is not None else f'<td colspan="2" class="val" style="text-align:center">{e(r.get("value_ar") or "")}</td>'
        body.append(f"<tr>{tds}</tr>")
    if not t["rows"]:
        body.append(f'<tr><td colspan="{len(cols)}">لا توجد صفوف تطابق هذا الأساس.</td></tr>')
    cap = f'<div class="cap2">{e(t["caption_ar"])}{ltr(t["caption_en"])}</div>'
    return cap + f'<table class="an"><colgroup>{colg}</colgroup><thead><tr>{hdr}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def note_item(a):
    return f'<div class="nitem"><span class="id">{a["id"]}</span><span>{e(a["ar"])}</span></div>'


def notes_head():
    return ('<div class="ah"><div class="k">NOTES FOR CONFIRMATION</div><h2>ملاحظات للتأكيد<bdi dir="ltr">Notes for confirmation</bdi></h2>'
            '<p style="margin-top:2mm;font-size:10pt;color:var(--muted)">نقاط في بيانات المصدر عُرضت كما وردت وتحتاج إلى تأكيد.</p></div>')


def terms_block():
    lis = "".join(f"<li>{e(t)}</li>" for t in D["general_terms"]["ar"])
    return f'<div class="sect">الشروط العامة <bdi dir="ltr">General terms</bdi></div><div class="notesbox"><ul class="notes">{lis}</ul></div>'


def credits_block():
    rows = "".join(f'<li>{ltr(v["credit"])}</li>' for v in list(PHOTOS.values()) + list(CITY_PHOTOS.values()))
    return ('<div class="sect">مصادر الصور والخطوط <bdi dir="ltr">Photo and font credits</bdi></div>'
            f'<div class="notesbox"><ul class="notes">{rows}'
            '<li>الصور مرخّصة برخص المشاع الإبداعي ومأخوذة عبر Openverse؛ الفنادق التي لم تتوفر لها صورة موثوقة تظهر ببطاقة اسم.</li>'
            '<li>الخطوط: IBM Plex Sans Arabic وMontserrat وPlayfair Display — جميعها برخصة SIL Open Font License 1.1.</li>'
            f'<li>المصدر الوحيد للأسعار: رسالة العميل بتاريخ 15 نوفمبر 2026. أُعدّ هذا الإصدار في 15 نوفمبر 2026.</li></ul></div>')


# ---------------------------------------------------------------- blocks registry
blocks = {}
order_hotels = L.hotels()
for i, h in enumerate(order_hotels, 1):
    blocks[f"hh:{h['id']}"] = hotel_header(h, i)
    blocks[f"hc:{h['id']}"] = hotel_cont(h)
    for p in h["periods"]:
        blocks[f"pt:{h['id']}:{p['key']}"] = rate_table(h, p)
    blocks[f"ex:{h['id']}"] = extras_table(h)
    blocks[f"bn:{h['id']}"] = booking_notes(h)
ANA = L.analyses()
for a in ANA:
    blocks[f"ah:{a['key']}"] = analysis_head(a)
    for j, t in enumerate(a["tables"]):
        blocks[f"at:{a['key']}:{j}"] = analysis_table(a, t)
blocks["nh"] = notes_head()
PRINTED_NOTES = [a for a in D["anomalies"] if a.get("print", True)]
for a in PRINTED_NOTES:
    blocks[f"nt:{a['id']}"] = note_item(a)
blocks["gt"] = terms_block()


def measure():
    mh = WORK / "measure.html"
    body = "".join(f'<div style="width:174mm;margin-bottom:20mm"><div class="block" data-block="{k}">{v}</div></div>' for k, v in blocks.items())
    mh.write_text(f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><base href="../"><style>{CSS}</style></head><body>{body}</body></html>', encoding="utf-8")
    subprocess.run(["node", str(WORK / "measure.cjs"), "measure", str(mh), str(WORK / "heights.json")], check=True)
    return json.loads((WORK / "heights.json").read_text())


HT = measure()


def pack(seq, cont_id=None):
    """seq: list of (block_id, keep_with_next). Returns list of pages (lists of ids)."""
    pages, cur, used = [], [], 0.0
    i = 0
    while i < len(seq):
        bid, kwn = seq[i]
        need = HT[bid] + (GAP if cur else 0)
        if kwn and i + 1 < len(seq):
            need += GAP + HT[seq[i + 1][0]]
        if HT[bid] > CONTENT_H - 20:
            sys.exit(f"block {bid} too tall: {HT[bid]:.1f} mm")
        if cur and used + need > CONTENT_H:
            pages.append(cur)
            cur, used = [], 0.0
            if cont_id:
                cur.append(cont_id); used = HT[cont_id]
            continue
        cur.append(bid); used += HT[bid] + (GAP if len(cur) > 1 else 0)
        i += 1
    if cur:
        pages.append(cur)
    return pages


# ---------------------------------------------------------------- page plan
plan = []  # list of dicts: kind, blocks, sec
plan.append({"kind": "cover"})
plan.append({"kind": "intro"})
for city in L.CITY_ORDER:
    plan.append({"kind": "opener", "city": city})
    for h in L.hotels(city):
        # master order for every hotel: header -> booking notes -> extras -> one table per period
        seq = [(f"hh:{h['id']}", False), (f"bn:{h['id']}", False), (f"ex:{h['id']}", False)] + [(f"pt:{h['id']}:{p['key']}", False) for p in h["periods"]]
        for pg in pack(seq, cont_id=f"hc:{h['id']}"):
            plan.append({"kind": "flow", "blocks": pg, "hotel": h["id"], "city": city})
for a in ANA:
    seq = [(f"ah:{a['key']}", True)] + [(f"at:{a['key']}:{j}", False) for j in range(len(a["tables"]))]
    for pg in pack(seq):
        plan.append({"kind": "flow", "blocks": pg, "analysis": a["key"]})
seq = [("nh", True)] + [(f"nt:{a['id']}", False) for a in PRINTED_NOTES] + [("gt", False)]
for pg in pack(seq):
    plan.append({"kind": "flow", "blocks": pg, "notes": True})

# page numbers
pagemap = {"hotels": {}, "analysis": {}, "openers": {}, "notes": None, "total": len(plan)}
for n, p in enumerate(plan, 1):
    p["pn"] = n
    if p.get("hotel") and p["hotel"] not in pagemap["hotels"]:
        pagemap["hotels"][p["hotel"]] = n
    if p.get("analysis") and p["analysis"] not in pagemap["analysis"]:
        pagemap["analysis"][p["analysis"]] = n
    if p["kind"] == "opener":
        pagemap["openers"][p["city"]] = n
    if p.get("notes") and not pagemap["notes"]:
        pagemap["notes"] = n
pagemap["plan"] = [{k: v for k, v in p.items()} for p in plan]
(WORK / "pagemap.json").write_text(json.dumps(pagemap, ensure_ascii=False, indent=1), encoding="utf-8")


# ---------------------------------------------------------------- special pages
def cover():
    return ('<section class="page cover"><div class="frame"></div><div class="frame2"></div>'
            '<div class="ed">إصدار 15 نوفمبر 2026</div>'
            '<div class="inner"><div class="kicker">MOSCOW · SAINT PETERSBURG</div>'
            '<div class="t1">RUSSIA</div><div class="t2">HOTEL COLLECTION</div><div class="yr">2026</div>'
            '<div class="rule"></div>'
            f'<div class="cities">{ltr(M["subtitle_en"])}</div>'
            f'<div class="tar">{e(M["title_ar"])}</div><div class="sar_">{e(M["subtitle_ar"])}</div></div>'
            f'<div class="agency"><div class="a1">{e(M["agency_ar"])}</div><div class="a2">PRICES IN RUB · SAR CONVERSION AT 21.4</div></div></section>')


def intro():
    bf = [("مع الإفطار", "With breakfast", "السعر يشمل الإفطار"), ("بدون إفطار", "Without breakfast", "سعر الغرفة فقط"),
          ("مع إفطار لشخص", "With breakfast for 1", "يشمل إفطار شخص واحد"), ("مع إفطار لشخصين", "With breakfast for 2", "يشمل إفطار شخصين"),
          ("غير مذكور", "Not stated", "لم يذكر المصدر ذلك")]
    oc = [("شخص واحد / مفردة", "1 person / Single"), ("شخصان / مزدوجة", "2 persons / Double"), ("ثلاثة أشخاص", "3 persons"),
          ("غير مذكور", "Not stated in the source")]
    lg1 = "".join(f'<tr><td><b style="font-weight:600;color:var(--navy)">{e(a)}</b></td><td>{e(c)}</td><td class="en">{ltr(b)}</td></tr>' for a, b, c in bf)
    lg2 = "".join(f'<tr><td><b style="font-weight:600;color:var(--navy)">{e(a)}</b></td><td class="en">{ltr(b)}</td></tr>' for a, b in oc)
    idx = ""
    k = 0
    for city in L.CITY_ORDER:
        c = M["cities"][city]
        idx += f'<div class="city">{e(c["ar"])}{ltr(c["en"])}</div>'
        for h in L.hotels(city):
            k += 1
            idx += f'<div class="row"><span class="n">{k:02d}</span><span class="nm">{e(h["name_ar"])}{ltr(h["name_en"])}</span><span class="pg">{pagemap["hotels"][h["id"]]}</span></div>'
    idx += '<div class="city">التحليل والملاحظات<bdi dir="ltr">Analysis &amp; notes</bdi></div>'
    for a in ANA:
        idx += f'<div class="row"><span class="n">A{a["n"]}</span><span class="nm">{e(a["title_ar"])}</span><span class="pg">{pagemap["analysis"][a["key"]]}</span></div>'
    idx += f'<div class="row"><span class="n">N</span><span class="nm">ملاحظات للتأكيد والشروط العامة</span><span class="pg">{pagemap["notes"]}</span></div>'
    right = (f'<div class="h3">سعر الصرف وطريقة التحويل<bdi dir="ltr">Exchange rate</bdi></div>'
             f'<div class="xbox"><span class="big"><bdi dir="ltr">1 SAR = 21.4 RUB</bdi></span>'
             '<div class="f">السعر بالريال = السعر بالروبل ÷ <b>21.4</b><br>تُقرَّب النتيجة إلى منزلتين عشريتين.<br>'
             'سعر الصرف ثابت كما حدده العميل.<br>لا عمولة ولا هامش ربح ولا أي زيادة.<br>السعر الأصلي بالروبل معروض للمراجعة.</div></div>'
             '<div style="height:3.5mm"></div>'
             f'<div class="h3">حالة الإفطار<bdi dir="ltr">Breakfast</bdi></div><table class="legend">{lg1}</table>'
             '<div style="height:3mm"></div>'
             f'<div class="h3">الإشغال<bdi dir="ltr">Occupancy</bdi></div><table class="legend">{lg2}</table>'
             '<div style="height:3mm"></div>'
             f'<div class="h3">الرموز<bdi dir="ltr">Symbols</bdi></div><table class="legend">'
             f'<tr><td>{stars(5)}</td><td>تصنيف النجوم كما ورد في المصدر فقط</td></tr>'
             '<tr><td><span class="tag">فترة منتهية</span></td><td>فترة انتهت قبل 15 نوفمبر 2026، معروضة كما وردت</td></tr>'
             '<tr><td><span class="ns">غير مذكور</span></td><td>معلومة لم يذكرها المصدر</td></tr></table>')
    left = f'<div class="h3">فهرس الفنادق<bdi dir="ltr">Index</bdi></div><div class="idx">{idx}</div>'
    inner = (f'<div class="intro"><h1>قبل أن تبدأ<bdi dir="ltr">About this catalogue</bdi></h1>'
             '<p style="margin:2mm 0 4.5mm;font-size:10pt;line-height:1.6">جميع الأسعار مأخوذة كما وردت من العميل بالروبل الروسي، ولليلة الواحدة ما لم يُذكر خلاف ذلك، ومحوّلة إلى الريال السعودي آلياً. السعر بالريال هو الرقم الأبرز في كل صف، والسعر بالروبل بجانبه للمراجعة.</p>'
             f'<div class="grid2"><div>{right}</div><div>{left}</div></div></div>')
    return page(inner, "دليل الكتالوج", "About", 2)


def opener(city):
    c = M["cities"][city]
    ph = CITY_PHOTOS.get(city)
    lst = "".join(f'<div class="row"><span>{e(h["name_ar"])}</span>{ltr(h["name_en"])}<span class="pg">{pagemap["hotels"][h["id"]]}</span></div>' for h in L.hotels(city))
    n = {"moscow": "01", "spb": "02"}[city]
    img = f'<div class="ph"><img src="{ph["src"]}" alt=""></div>' if ph else ""
    cnt = len(L.hotels(city))
    inner = (f'{img}<div class="num">SECTION {n}</div><div class="cn">{e(c["ar"])}</div><div class="ce">{e(c["en"])}</div>'
             f'<div class="rule"></div><div class="lst">{lst}</div>'
             f'<p style="margin-top:5mm;font-size:9.5pt;color:var(--muted)">{L.ar_count(cnt, "فنادق", "فندقاً", "فندقان")} في هذا القسم، بترتيب ورودها في المصدر.</p>')
    return page(inner, None, None, None, cls="opener").replace('<section class="page opener">', '<section class="page opener">') \
        .replace('</div></section>', f'</div><div class="rfoot"><span>{e(M["agency_ar"])}</span><span class="pn">{pagemap["openers"][city]}</span><span></span></div></section>')


def flow(p):
    inner = "".join(f'<div class="block" data-b="{b}">{blocks[b]}</div>' for b in p["blocks"])
    if p.get("hotel"):
        c = M["cities"][p["city"]]
        return page(inner, c["ar"], c["en"], p["pn"])
    if p.get("analysis"):
        return page(inner, "التحليل", "Analysis", p["pn"])
    return page(inner, "ملاحظات وشروط", "Notes & terms", p["pn"])


pages = []
for p in plan:
    if p["kind"] == "cover":
        pages.append(cover())
    elif p["kind"] == "intro":
        pages.append(intro())
    elif p["kind"] == "opener":
        pages.append(opener(p["city"]))
    else:
        pages.append(flow(p))

doc = (f'<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">'
       f'<title>RUSSIA HOTEL COLLECTION 2026 — {e(M["title_ar"])}</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>')
OUT_HTML.write_text(doc, encoding="utf-8")
print(f"wrote {OUT_HTML.name}: {len(plan)} pages")
for p in plan:
    if p["kind"] == "flow":
        used = sum(HT[b] for b in p["blocks"]) + GAP * (len(p["blocks"]) - 1)
        print(f"  p{p['pn']:02d} {used:6.1f}mm  {', '.join(p['blocks'])}")
