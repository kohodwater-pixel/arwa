"""Round 3: system.md v03, tokens.json v03, PNG re-export at whole-pixel sizes.
Run from 04-identity/. v02 copies are already in the _archive folders."""
import json, os, re, glob, io
import cairosvg
from PIL import Image

# ---------------------------------------------------------------- system.md
p = "03-system/system.md"
L = open(p, encoding="utf-8").read().split("\n")

def rep(prefix, new, count=1):
    hits = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(hits) == count, (prefix, len(hits))
    for i in hits:
        L[i] = new

def after(prefix, new_lines):
    hits = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(hits) == 1, (prefix, len(hits))
    L[hits[0] + 1:hits[0] + 1] = new_lines

rep("**Version:** v02", "**Version:** v03  **Date:** 2026-11-13  **Prepared by:** Identity Designer  **Status:** revised after quality review r2; for re-review, not yet approved")
rep("**Previous version:**", "**Previous versions:** `_archive/system_v02.md`, `_archive/system_v01.md`. What changed in v03 is listed in section 12; v02 changes are in section 9.")
rep("**Built from:**", "**Built from:** `01-direction/creative-direction.md` (Direction A \"Weekly Beat\", approved 2026-11-13) as amended by `creative-direction-amendment-01.md` and `creative-direction-amendment-02.md`; where they differ, the later amendment wins. Machine-readable values: `tokens.json`. Shared CSS: `brand-v02.css` (unchanged in v03; `brand.css` is the v01 file, kept because archived v01 HTML files link to it).")
rep("| Ember — جمر | `#C23A20`", "| Ember — جمر | `#C23A20` | 194 58 32 | 15 90 100 5 | waived for system test; required before print | The lit bar; one headline or one field per layout; the 1 kg bag; on web, the one primary action button per screenful (section 10) | 10% |")
rep("| **Ink on Ember** |", "| **Ink on Ember** | **3.19:1** | Bars and rules (graphics). Text only at 24 px / 18 pt and above, or 19 px / 14 pt Bold and above; prefer Paper on Ember for any text |")
rep("**Correction to the direction:**", "**Ink on Ember is 3.19:1, not 3.9:1.** `creative-direction.md` section 2 gives 3.9:1; that figure is wrong and was corrected by the art-director in amendment 01 section 1 (the approved direction file itself is left unchanged). 3.19 clears the 3:1 threshold for large text and graphics with very little margin, so the rule was tightened as in the table above. Wherever 3.9:1 still appears in an older file, 3.19:1 is the value to use. All other figures in the direction match to one decimal.")

after("- Small pieces (business card, label)", [
"",
"### 3.1 A4 document ladder (amendment 01 section 9; review r2 N8)",
"",
"The four-step scale (0.65 / 1 / 1.6 / 5) stays the identity scale. On A4 documents the Latin block is held to three columns and the display step does not fit, so two steps are added **for A4 documents only** (company profile, proposals, reports).",
"",
"| Level | Scale | Latin | Arabic | Line height EN / AR |",
"|---|---|---|---|---|",
"| Caption | 0.65 | 6.5 pt SemiBold, uppercase, +12% | 7.5 pt Regular | 1.4 / 1.6 |",
"| Body | 1 | 10 pt Regular | 11.5 pt Regular | 1.45 / 1.75 |",
"| Sub-head | 1.6 | 16 pt Medium | 18.5 pt Medium | 1.3 / 1.5 |",
"| **Section title** | 2.8 | **28 pt** Bold, -1.5% | **32 pt** Bold | 1.1 / 1.3 |",
"| **Cover title** | 4 | **40 pt** Bold, -1.5% | **46 pt** Bold | 1.05 / 1.3 |",
"",
"- One section title per page; the cover title appears on the cover only.",
"- Tracking applies to the Latin only; Arabic is never tracked.",
"- These two steps are not used on social, presentation or packaging formats.",
"",
"### 3.2 Social ladder, formats 1080 px wide (amendment 02 section 4; review r2 N12)",
"",
"For 1080 × 1080, 1080 × 1350 and 1080 × 1920 only. It is the screen ladder × 1.15, because a 1080 px canvas is seen on a phone at about a third of its pixel size.",
"",
"| Level | Arabic | Latin beside it |",
"|---|---|---|",
"| Display headline | **132 px** Bold, line height 1.3 | 115 px Bold, -1.5%, 1.05 |",
"| Sub-head | **42 px** Medium, 1.5 | 37 px Medium, 1.3 |",
"| Body and call to action | **27 px** Regular, 1.75 | 23.5 px Regular, 1.45 |",
"| Caption | **17.5 px** Regular, Ash on Paper only | 15 px SemiBold, uppercase, +12% |",
"",
"- 132 px is the maximum, not a starting point. A longer headline drops to the sub-head step or is rewritten shorter; no sizes in between and nothing above 132 px.",
"- One display headline per post.",
"- Web, slides, documents and packaging keep their own ladders.",
"",
"### 3.3 Caption floor on screen",
"",
"On screen-only pieces no caption or other text is set below **9 px** (decision log 2026-11-13, art-director rulings). The screen caption step is 15 / 13 px, so the floor matters only where a small piece scales the whole ladder down: stop at 9 px. Print captions stay at 7.5 / 6.5 pt.",
])

rep("- Bar row: always seven equal bars", "- Bar row: always seven equal bars, the fourth lit, gap = 1/5 bar width. **Rule** proportion 2:1 (logo, dividers); **band** proportion 1:2 to 1:4 (packaging, large fields). Pattern: three or more band rows stacked with the same gap, lit bars in one column. **\"Always seven\" and \"one lit bar\" are counted per row:** the stacked pattern and the icon therefore show more than seven bars and more than one lit bar in total, which is correct, provided the lit bars line up in one centre column. Never light two bars in one row, never stagger the lit bars from row to row, never stack fewer than three rows (amendment 02 section 2).")
rep("- Lit bar colour:", "- Lit bar colour: Ember on Paper, Crema and Ink. **On Ember: Ink bars with a Paper lit bar** (see section 7, point 2). The bar row is a device, never a chart: nothing is labelled by, numbered by or tied to an individual bar (ruling f).")

rep("Files in `../02-logo/`, named", "Files in `../02-logo/`, named `demo-sidra-coffee_logo_<lockup>-<colour>_<lang>_v01.svg` (icon with bars: `_v02`). All text is converted to outlines; the SVGs contain only `path` and `rect` and need no fonts.")
rep("**Icon v02 (review issue 19).**", "**Icon v02 (review issue 19).** The v01 icon (one row of 1:2 bars with a margin) still read as a barcode and its bar count was unstable. v02 uses the system's own pattern rule: three band rows (bar 1:2.6, inside the 1:2 to 1:4 band range), row gap equal to the bar gap, lit bars in one column, filling a 205-unit square so that bar = 25, gap = 5. It reads as a grid of weeks, not a barcode. **Confirmed by the art-director in amendment 02 section 2**, in place of the direction's one-row wording, together with the per-row reading of the misuse rules (section 4).")
rep("v02 is stable from 41 px up;", "v02 is stable from 41 px up; v01 was not stable until 48 px. Below 41 px the gap is under one pixel and seven bars cannot hold in any proportion while the 1/5 gap rule stands, so `icon-small` is still required from 16 to 47 px. The 48 px switch size (ruling g) is unchanged. The five superseded v01 icon files (`icon-<colour>_ar-en_v01.svg`) are now in `../02-logo/_archive/` with the reason (review r2 N10); no current file links to them. The `icon-small` v01 files are current and stay in `../02-logo/`.")
rep("**Export formats (review issue 18).**", "**Export formats (review issue 18; r2 N10).** `../02-logo/png/`: transparent PNG at 1x, 2x and 4x for every current lockup and colour version (135 files). Re-exported in v03 at whole-pixel sizes, so 2x and 4x are exact multiples of 1x: lockups 204 / 408 / 816 px wide, icon 205 / 410 / 820, icon-small 200 / 400 / 800. The lockup artwork is 203.6 units wide, so each PNG is scaled up by 0.2% to reach 204 px, with the height rounded to a whole pixel at 1x; the PNGs are for screen use and the SVG stays the master. `../02-logo/pdf/`: vector PDF of each (45 files; checked with pdffonts and pdfimages: no fonts, no raster images). The superseded v01 icon was never exported. PDFs are RGB, straight from the SVG; no CMYK or spot-colour PDFs exist (print colour is waived for the test).")
rep("**Difference from competitors.**", "**Difference from competitors.** Compared on 2026-11-13 with the home pages of Camel Step, Elixir Bunn and Brew92: distinct from all three. Home pages only; not a trademark search. (Art-director, `../01-direction/distinctiveness-check_v02.md`, which is the record.) Camel Step: a line-drawn symbol in dark teal-blue on white, against Sidra's heavy Arabic wordmark on seven bars in Ember, Ink and warm Paper. Elixir Bunn: a thin calligraphic Arabic and serif Latin wordmark, black on white with green and gold and ornament, against a low-contrast sans wordmark, a counted bar device and no ornament; its red `#D92C20` is a sale label, not a brand colour, so Ember stays. Brew92: a thin Latin wordmark in electric blue on cool grey, English-led, against an Arabic-led mark. One overlap: Camel Step sets its site text in IBM Plex Sans Arabic, so the wordmark redraw is required before real use (section 7, point 1). \"Arabic-first\" is not claimed as a differentiator: two of the three are Arabic-led. Not seen: packaging, social accounts, signage, other roasters.")
rep("**Conflict check (review issue 16).**", "**Conflict check (review issue 16).** A preliminary web search was run by the naming-specialist on 2026-11-13 (`../mark-check.md`; summary in `../licences.md`). **Name: HIGH risk**: search results report a \"Sidra\" dining complex in Riyadh operated by Alshaya (same word, same city, food and beverage). **Medium risk:** \"Sidra\" is a coffee variety already sold by Riyadh roasters. **Device:** the seven-bar row could not be checked by text search; its status is unknown, not clear. A row of bars is a generic device and similar marks may exist. No trademark register was searched. **This is not a legal trademark clearance; a formal search and opinion by a trademark attorney is required before any real use.** For the system test the check is recorded and work continues (decision log).")

rep("| Distinct from every competitor |", "| Distinct from every competitor | **Pass within home-page evidence**: art-director's check v02, three competitors, home pages only |")
rep("| Preliminary conflict check; trademark notice |", "| Preliminary conflict check; trademark notice | **Done as a preliminary check, with a HIGH name risk found** (Alshaya \"Sidra\", Riyadh); device not checkable by text search; no register searched; not-legal-clearance notice in `licences.md`, `mark-check.md` and guidelines v03 p6. Counsel's opinion required before real use |")
rep("| Misuse examples |", "| Misuse examples | Pass (8 drawn, 5 written, plus the per-row note for the stacked pattern and icon in guidelines v03) |")
rep("## 7. Decisions and deviations", "## 7. Decisions and deviations (status after round 3)")
rep("7. **Latin line reads \"SIDRA COFFEE\"**", "7. **Latin line reads \"SIDRA COFFEE\"** as the direction specifies, although naming.md warns that \"Sidra coffee\" reads as a variety in English. **Closed: the Latin line stays \"SIDRA COFFEE\"** (decision log 2026-11-13; amendment 02 section 7). \"Roastery\" is used in running copy.")

# section 8: replace the proposed block (now written into brand-context by the Creative Director)
s8 = next(i for i, l in enumerate(L) if l.startswith("## 8. Proposed text"))
s9 = next(i for i, l in enumerate(L) if l.startswith("## 9. What changed in v02"))
L[s8:s9] = [
"## 8. `brand-context.md` section 5",
"",
"The text proposed here in v02 has been written into `brand-context.md` section 5 by the Creative Director (the v02 wording is kept in `_archive/system_v02.md`). One addition is still outstanding there, which amendment 02 section 2 asks for and which is the Creative Director's to make. Proposed wording for the \"Do not\" line:",
"",
"> The rules \"always seven\" and \"one lit bar\" count per row: the stacked pattern and the icon repeat three or more identical rows, with the lit bars in one centre column. Never light two bars in one row, stagger the lit bars, or stack fewer than three rows.",
"",
"Also for that section when it is next updated: Ember may fill the one primary action button per screenful on web (section 10); the A4 and social ladders and the 9 px screen caption floor are in section 3 of this file and in `tokens.json`.",
"",
]

L += [
"",
"## 10. Ember on web: the button rule (ruling l; amendment 02 section 3)",
"",
"- On a web or app screen, Ember may fill **the single primary action button in each screenful**, in addition to the lit bar. A screenful is what is visible without scrolling at 1440 × 900 and at 390 × 844; check both.",
"- Within one screenful the Ember button **takes the place of** the Ember field or headline: the lit bar plus either one Ember button or one Ember field or headline, never both (confirmed, decision log 2026-11-13).",
"- Button: Ember fill, Paper label (4.56:1), Medium 500 or heavier, square corners, no shadow.",
"- Every other button in the same screenful is Ink: Ink fill with Paper label, or a 2 px Ink outline with Ink label on Paper or Crema.",
"- **A header button that stays on screen while scrolling is always Ink.**",
"- States use solid colours only: hover and pressed = Ink fill with Paper label; focus = 2 px Ink outline set 2 px outside the button.",
"- Ember is never a body-text or link colour.",
"- Web and app screens only. Documents, slides, social and print keep \"once per layout\".",
"",
"## 11. Motion rules, summary (amendment 02 section 1, which is the full text)",
"",
"The static rules describe resting states. In any film, animated slide or web animation:",
"",
"| Subject | Rule |",
"|---|---|",
"| Bar build | Bars may build in. Each appears in its final place and size by a hard-edged wipe or a hard cut; bars never slide, scale, bounce, rotate, swap or fade. Order follows the lockup's reading direction (right to left for Arabic and bilingual, left to right for Latin-led). Seven bars in 1.0 s at most. |",
"| Partial counts | No hold on a partial count: any moment where nothing moves for 0.1 s or more shows seven bars or none. Bars do not build out. |",
"| Lit bar | Ember appears only after all seven bars are present, only on the fourth, by a bottom-up hard-edged fill or a hard cut in 0.3 s at most. No blend, glow, pulse or flash. No other bar lights at any moment and the light never travels along the row. |",
"| Wordmark and Arabic text | Arrive whole: an opacity fade of the complete word or line in 0.5 s at most, or a hard cut. Never letter by letter, never by a wipe. This fade is the only exception to \"no tints\" and applies to transitions only; nothing is held part-way through it. |",
"| Ending | A film ends on the complete, static logo held for at least 1.0 s, with no fade-out. An empty Paper lead-in of up to 0.1 s is allowed. |",
"| Poster frame | Every film ships with a poster frame taken from the final hold. Stills and thumbnails are never taken from a build or a fade. |",
"| General | One easing, cubic ease-out. Flat colour and square corners; no blur, shadow, gradient or texture. Films work silent; sound only with a recorded licence. Web and app motion honours `prefers-reduced-motion` by showing the final state only. |",
"",
"## 12. What changed in v03 (after quality review r2)",
"",
"| Review issue | Action |",
"|---|---|",
"| N8 A4 ladder | Recorded in section 3.1 and in `tokens.json` (`font.ladder_a4_document_pt`). |",
"| N12 social ladder | The approved 1080-wide ladder (132 / 42 / 27 / 17.5 px Arabic) recorded in section 3.2 and in `tokens.json` (`font.ladder_social_1080_px`). |",
"| Caption floor | 9 px floor for screen-only pieces recorded in section 3.3 and in `tokens.json`. |",
"| Ruling (l) Ember button | Section 10 and `tokens.json` (`color.ember.web_button`, `button`). |",
"| Motion | Summary in section 11 and `tokens.json` (`motion`). |",
"| r1 21 Ink on Ember | 3.19:1 with the tightened text rule from amendment 01, in section 2 and `tokens.json`. |",
"| N4, r1 16 | Competitor and conflict-check paragraphs in section 5 and the self-check rows in section 6 rewritten to match `distinctiveness-check_v02.md` and `mark-check.md`. `licences.md` v03 and guidelines v03 p6 say the same. |",
"| N13 misuse exemption | Per-row counting stated in section 4 and on the guidelines v03 misuse page. |",
"| N10 | Icon v01 SVGs moved to `02-logo/_archive/`; PNGs re-exported at whole-pixel sizes (section 5). |",
"",
"Not changed in v03: the logo SVGs and PDFs, `brand-v02.css`, the applications, the palette and every measured value.",
]
open(p, "w", encoding="utf-8").write("\n".join(L))

# ---------------------------------------------------------------- tokens.json
tp = "03-system/tokens.json"
t = json.load(open(tp, encoding="utf-8"))
t["$version"] = "v03 (2026-11-13). v02 and v01 are kept in _archive/"
t["$description"] = t["$description"].replace("Source: 04-identity/01-direction/creative-direction.md (approved 2026-11-13).", "Source: 04-identity/01-direction/creative-direction.md (approved 2026-11-13) as amended by creative-direction-amendment-01.md and -02.md.")
assert "amendment-01" in t["$description"]
t["color"]["ember"]["role"] = "The lit bar; one headline or one field per layout; the 1 kg bag; on web, the one primary action button per screenful"
t["color"]["ember"]["web_button"] = "Web and app only: Ember may fill the single primary action button in each screenful, in addition to the lit bar. Within a screenful the button replaces the Ember field or headline. See 'button'."
t["contrast"]["not_for_text"]["ink-on-ember"] = {
    "ratio": 3.19,
    "rule": "graphics (bars, rules); text only at 24 px / 18 pt and above, or 19 px / 14 pt Bold and above; prefer paper-on-ember for any text",
    "note": "creative-direction.md section 2 gives 3.9; corrected to 3.19 in amendment 01 section 1"
}
f = t["font"]
f["size_px_screen_min"] = {"value": 9, "rule": "Floor for captions and any other text on screen-only pieces (decision log 2026-11-13). Applies when a small piece scales the ladder down."}
f["ladder_a4_document_pt"] = {
    "$description": "A4 documents only (amendment 01 section 9). Adds section_title and cover_title to the identity scale. One section title per page; cover title on the cover only. Latin tracking only; Arabic is never tracked. Not for social, presentation or packaging formats.",
    "caption": {"scale": 0.65, "latin": 6.5, "arabic": 7.5, "latin_weight": 600, "arabic_weight": 400, "latin_letter_spacing": "0.12em", "latin_transform": "uppercase", "line_height_latin": 1.4, "line_height_arabic": 1.6},
    "body": {"scale": 1, "latin": 10, "arabic": 11.5, "latin_weight": 400, "arabic_weight": 400, "line_height_latin": 1.45, "line_height_arabic": 1.75},
    "subhead": {"scale": 1.6, "latin": 16, "arabic": 18.5, "latin_weight": 500, "arabic_weight": 500, "line_height_latin": 1.3, "line_height_arabic": 1.5},
    "section_title": {"scale": 2.8, "latin": 28, "arabic": 32, "latin_weight": 700, "arabic_weight": 700, "latin_letter_spacing": "-0.015em", "line_height_latin": 1.1, "line_height_arabic": 1.3},
    "cover_title": {"scale": 4, "latin": 40, "arabic": 46, "latin_weight": 700, "arabic_weight": 700, "latin_letter_spacing": "-0.015em", "line_height_latin": 1.05, "line_height_arabic": 1.3}
}
f["ladder_social_1080_px"] = {
    "$description": "Social formats 1080 px wide only: 1080x1080, 1080x1350, 1080x1920 (amendment 02 section 4). Screen ladder x 1.15. Display is a maximum: a longer headline drops to subhead or is rewritten; no sizes in between; one display headline per post.",
    "display": {"arabic": 132, "latin": 115, "arabic_weight": 700, "latin_weight": 700, "latin_letter_spacing": "-0.015em", "line_height_arabic": 1.3, "line_height_latin": 1.05, "max": True},
    "subhead": {"arabic": 42, "latin": 37, "arabic_weight": 500, "latin_weight": 500, "line_height_arabic": 1.5, "line_height_latin": 1.3},
    "body": {"arabic": 27, "latin": 23.5, "arabic_weight": 400, "latin_weight": 400, "line_height_arabic": 1.75, "line_height_latin": 1.45},
    "caption": {"arabic": 17.5, "latin": 15, "arabic_weight": 400, "latin_weight": 600, "latin_letter_spacing": "0.12em", "latin_transform": "uppercase", "line_height_arabic": 1.6, "line_height_latin": 1.4, "colour": "ash, on paper only"}
}
t["bar_row"]["count_rule"] = "Seven bars and one lit bar (the fourth) per row. The stacked pattern and the icon repeat three or more identical rows, so they show more than seven bars and more than one lit bar in total; the lit bars line up in one centre column. Never two lit bars in one row, never staggered, never fewer than three rows."
t["bar_row"]["not_a_chart"] = "Nothing is labelled by, numbered by or tied to an individual bar (ruling f)."
t["button"] = {
    "$description": "Web and app screens only (ruling l; amendment 02 section 3). A screenful is what is visible without scrolling at 1440x900 and at 390x844.",
    "primary": {"background": "{color.ember}", "label": "{color.paper}", "contrast": 4.56, "min_font_weight": 500, "corner_radius": 0, "shadow": "none", "limit": "one per screenful; replaces the Ember field or headline in that screenful"},
    "secondary": {"background": "{color.ink}", "label": "{color.paper}", "alternative": "2 px ink outline with ink label on paper or crema"},
    "persistent_header": "always ink, never ember",
    "hover_pressed": {"background": "{color.ink}", "label": "{color.paper}"},
    "focus": "2 px ink outline, offset 2 px outside the button",
    "never": "ember as body-text or link colour; tints for states"
}
t["motion"] = {
    "$description": "Summary of amendment 02 section 1, which is the full text.",
    "easing": "cubic ease-out, one easing for every move",
    "bar_build": {"allowed": "hard-edged wipe or hard cut, each bar in its final position and size", "forbidden": "slide, scale, bounce, rotate, swap, fade, build-out", "order": "reading order of the lockup: right to left for Arabic and bilingual, left to right for Latin-led", "max_duration_s": 1.0},
    "partial_count_max_hold_s": 0.1,
    "lit_bar": {"after": "all seven bars present", "index": 4, "transition": "bottom-up hard-edged fill or hard cut", "max_duration_s": 0.3, "forbidden": "colour blend, glow, pulse, flash, any other bar lit, light travelling along the row"},
    "wordmark_and_arabic_text": {"transition": "opacity fade of the whole word or line, or hard cut", "max_duration_s": 0.5, "forbidden": "letter by letter, wipe, holding part-way through a fade"},
    "end_hold_min_s": 1.0,
    "end": "complete static logo, no fade-out",
    "lead_in_max_s": 0.1,
    "poster_frame": "required; taken from the final hold, never from a build or a fade",
    "style": "flat colour, square corners; no blur, shadow, gradient or texture",
    "sound": "films work silent; sound only with a recorded licence",
    "reduced_motion": "prefers-reduced-motion shows the final state only"
}
t["logo"]["icon"] = "v02, confirmed by the art-director (amendment 02 section 2): three stacked band rows (bar 1:2.6) filling the square, lit bars in the centre column. Seven bars count reliably from 41 px; switch size stays 48 px. Icon v01 is archived in 02-logo/_archive/."
t["logo"]["formats"] = "SVG (source), vector PDF in 02-logo/pdf/, transparent PNG at 1x, 2x, 4x in 02-logo/png/"
t["logo"]["png_px_wide"] = {"lockups": [204, 408, 816], "icon": [205, 410, 820], "icon_small": [200, 400, 800]}
json.dump(t, open(tp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
open(tp, "a").write("\n")
json.load(open(tp, encoding="utf-8"))
print("system.md lines:", len(L), "| tokens keys:", list(t.keys()))

# ---------------------------------------------------------------- PNG re-export
import math
n = 0; sizes = {}
for svg in sorted(glob.glob("02-logo/*.svg")):
    b = os.path.basename(svg)[:-4]
    m = re.match(r"(.*)_((?:ar-en|ar|en)_v\d\d)$", b)
    head, tail = m.group(1), m.group(2)
    src = open(svg, encoding="utf-8").read()
    w, h = [float(x) for x in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', src).groups()]
    W1 = math.ceil(w - 1e-9); H1 = max(1, round(h * W1 / w))
    for k in (1, 2, 4):
        out = f"02-logo/png/{head}-{k}x_{tail}.png"
        assert os.path.exists(out), out   # only replace files of the existing set
        cairosvg.svg2png(url=svg, write_to=out, output_width=W1 * k, output_height=H1 * k)
        im = Image.open(out)
        assert im.mode == "RGBA" and im.size == (W1 * k, H1 * k), (out, im.mode, im.size)
        n += 1
    sizes.setdefault((W1, H1), []).append(head)
print("png written:", n, "| files in png/:", len(glob.glob("02-logo/png/*.png")))
for k, v in sizes.items(): print(k, len(v), "lockups, e.g.", v[0].split("logo_")[1])
