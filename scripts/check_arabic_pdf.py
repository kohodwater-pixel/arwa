#!/usr/bin/env python3
"""Pre-approval check for Arabic and bilingual PDFs.

Verifies, per page: fonts are embedded, no fallback font was substituted,
Arabic text is present and extractable, and renders PNG previews so the
shaping (connected letters, right-to-left order) can be inspected by eye.

Usage: python3 scripts/check_arabic_pdf.py <file.pdf> [--expect "نص متوقع" ...] [--png <dir>] [--dpi 110]
Exit code 0 = pass, 1 = fail.
"""
import argparse, pathlib, re, sys, unicodedata
import pymupdf

FALLBACK = re.compile(r"dejavu|freeserif|freesans|freemono|unifont|liberation|lastresort|notdef|times ?new|arial|helvetica|courier", re.I)
ARABIC = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
PRESENTATION = re.compile(r"[ﭐ-﷿ﹰ-﻿]")

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    return re.sub(r"[\sـً-ْ‎‏]+", "", s)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--expect", action="append", default=[], help="Arabic string that must be extractable (repeatable)")
    ap.add_argument("--png", help="directory for page previews")
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--allow-no-arabic", action="store_true")
    a = ap.parse_args()

    doc = pymupdf.open(a.pdf)
    problems, fonts_seen, all_text, arabic_chars = [], set(), "", 0
    type3_pages = set()
    for i, page in enumerate(doc, 1):
        for xref, ext, ftype, basefont, name, enc in page.get_fonts(full=False):
            clean = basefont.split("+")[-1]
            if ftype == "Type3":
                # Chromium embeds variable fonts as Type 3 glyph programs: embedded by definition, but unnamed.
                type3_pages.add(i)
                continue
            fonts_seen.add(clean)
            if ext == "n/a":
                problems.append(f"page {i}: font '{clean}' is not embedded")
            if FALLBACK.search(clean):
                problems.append(f"page {i}: fallback/system font '{clean}' in use - the intended font was not applied")
        text = page.get_text()
        all_text += text
        arabic_chars += len(ARABIC.findall(text))
        if a.png:
            out = pathlib.Path(a.png); out.mkdir(parents=True, exist_ok=True)
            page.get_pixmap(dpi=a.dpi).save(out / f"{pathlib.Path(a.pdf).stem}_p{i:02d}.png")

    if arabic_chars == 0 and not a.allow_no_arabic:
        problems.append("no extractable Arabic text found (text may be outlined, rasterised, or missing)")
    n_all = norm(all_text)
    for s in a.expect:
        t = norm(s)
        if t not in n_all and t[::-1] not in n_all:
            problems.append(f"expected text not found: {s}")
        elif t not in n_all:
            problems.append(f"expected text found only in REVERSED order (bidi not applied): {s}")
    pres = len(PRESENTATION.findall(all_text))

    print(f"file: {a.pdf}")
    print(f"pages: {doc.page_count}   page size (mm): {doc[0].rect.width/72*25.4:.0f} x {doc[0].rect.height/72*25.4:.0f}")
    print(f"fonts: {', '.join(sorted(fonts_seen)) or 'none'}")
    if type3_pages:
        print(f"note: Type 3 (variable-font) glyphs on {len(type3_pages)} page(s): fine for screen; for print prefer static font files")
    print(f"arabic characters extracted: {arabic_chars} (presentation forms: {pres})")
    if a.png:
        print(f"previews: {a.png}  <- open these and confirm letters are connected and read right to left")
    if problems:
        print("RESULT: FAIL")
        for p in problems: print("  - " + p)
        sys.exit(1)
    print("RESULT: PASS (automated checks). Visual check of the previews is still required.")

if __name__ == "__main__":
    main()
