# Licences — Sidra Coffee identity

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS.

**Version:** v03  **Date:** 2026-11-13  **Previous versions:** `_archive/licences_v02.md`, `_archive/licences_v01.md`  **Prepared by:** Identity Designer

This is a record of what was used and under which licence, and of which originality checks have and have not been made. It is not legal advice.

**What changed in v03:** the section on name, mark and competitor checks was rewritten to match the facts now on file (`mark-check.md`, `01-direction/distinctiveness-check_v02.md`, decision log of 2026-11-13). The v02 sentences "no search of any kind has been run for the mark", "no look at the real identities" of the competitors and "no roastery or café of that name appeared" as the only name result are withdrawn. The note on the provenance of the static Latin font files was made more exact.

## Fonts

| Font | Used for | Source in repo | Licence | Copyright line in the licence file |
|---|---|---|---|---|
| IBM Plex Sans Arabic (Light, Regular, Medium, SemiBold, Bold; static TTF) | All Arabic text; source outlines of the Arabic wordmark (Bold) | `assets/fonts/ibmplexsansarabic/` | SIL Open Font License 1.1 (`OFL.txt` in the same folder) | Copyright © 2017 IBM Corp. with Reserved Font Name "Plex" |
| IBM Plex Sans (static TTF: Light, Regular, Medium, SemiBold, Bold) | All Latin text in v02 and v03 files | `assets/fonts/ibmplexsans-static/` | SIL Open Font License 1.1 (`OFL.txt` in the same folder) | Copyright © 2017 IBM Corp. with Reserved Font Name "Plex" |

What the OFL allows, as I read it: free use in print, web, apps and products, including commercial use; embedding in documents; bundling and redistribution with the licence file included. The fonts may not be sold on their own. Documents and artwork made with the fonts, including the outlined logo, are not themselves subject to the OFL.

### Latin font files

- All v02 and v03 files (`03-system/brand-v02.css`, business card v02, bag label v02, guidelines v02 and v03) use the static IBM Plex Sans files in `assets/fonts/ibmplexsans-static/` (Light, Regular, Medium, SemiBold, Bold, with `OFL.txt`).
- **Provenance of those static files (review r2, N11).** Read from the Regular file on 2026-11-13: version 3.006, vendor ID "IBM", designer "Bold Monday", copyright "2018 IBM Corp.", licence field SIL OFL 1.1. This metadata is what IBM's own release carries. Where the files were downloaded from is not recorded in the repo, and I have not compared them byte for byte with IBM's release. Earlier versions of this file called them "official"; the accurate statement is "IBM Plex Sans 3.006 by its own metadata, download source not recorded".
- The variable font and the six instances I cut from it in round 1 (`04-identity/_work/fonts/`) are not referenced by any v02 or v03 file. They are kept only because archived v01 HTML files link to them. **Do not ship `_work/fonts/` to the client:** those instances carry the Reserved Font Name "Plex".
- The 85% width figure style was dropped. Large Latin figures are IBM Plex Sans Light 300 at regular width.
- One exception to note: the Latin line "SIDRA COFFEE" inside the logo SVGs was outlined in round 1 from the SemiBold instance cut from the variable font, not from the static file. The logo contains outlines only, so no font file is distributed with it. I have not compared the two outlines; they should be identical at wght 600, wdth 100, but that is unverified.

## Logo

- Original work made for this client in this project. Arabic wordmark: outlines of IBM Plex Sans Arabic Bold with custom optical spacing. Latin line: outlines of IBM Plex Sans SemiBold with custom tracking. Seven-bar device: drawn from scratch.
- Icon v02: three stacked rows of the same seven-bar device, drawn from scratch. The single-row icon v01 is superseded and archived in `02-logo/_archive/`.

## Name, mark and competitor checks (review r1 issue 16; review r2 N4)

**None of this is a legal trademark clearance.** It is a record of what has and has not been looked at. The full records are `mark-check.md` (naming-specialist) and `01-direction/distinctiveness-check_v02.md` (art-director); where this summary and those files differ, those files win.

### What was checked

| Check | By whom, when | Result |
|---|---|---|
| Visual comparison with three competitors | art-director, 2026-11-13, countersigning the Creative Director's earlier addendum (`01-direction/distinctiveness-check_v02.md`) | Compared with the home pages of Camel Step, Elixir Bunn and Brew92: **distinct from all three.** Home pages only (first 900 px of each); not a trademark search. One overlap: Camel Step sets its site text in IBM Plex Sans Arabic, which is why the wordmark redraw is required before real use. |
| Preliminary web search of the name | naming-specialist, 2026-11-13, 14 web searches in Arabic and English (`mark-check.md`). Search-result summaries were read; no linked page was opened. | **HIGH risk found:** search results report a dining complex named "Sidra" in Riyadh (and one in Kuwait), operated by Alshaya: the same word, in the same city, in food and beverage. Whether it still trades under that name, and whether the name is registered, is not known. |
| "Sidra" as a coffee variety | naming-specialist, same searches | **MEDIUM risk:** "Sidra" is a coffee variety name and search results show it already on sale by Riyadh roasters. Possible descriptiveness problem in class 30; a question for counsel. |
| Other uses of the word | naming-specialist, same searches | "Sidra" convenience stores with a café counter in Qatar (medium in Qatar, low in Saudi Arabia). Sidra / Sedra / Sidr names in other categories: low each, medium together as a sign of a crowded word. No café or roastery named Sidra / Sedra / سدرة / سدره was found in the GCC, which is weak evidence: the search does not see social-only shops, maps or the commercial register. |
| Preliminary web search of the mark | naming-specialist, 2026-11-13, two text searches (one English, one Arabic) | No coffee or food brand was described in text as using a row of bars or a seven-part week device. **Not rateable:** logos are rarely described in words. The status of the seven-bar device is **unknown, not clear.** |

### What was not checked

- **No trademark register was searched:** not SAIP (Saudi Arabia), not the GCC system, not the WIPO Global Brand Database, in class 30, 43, 35 or any other class.
- **The bar device could not be checked by text search.** No image search, reverse-image search or logo-similarity search was run. The only visual check on file is the comparison with three competitor home pages.
- Competitors beyond their home pages: packaging, social accounts, cafés, signage and print. Any other Saudi or GCC roaster.
- Google Maps, delivery apps, Instagram, Snapchat, TikTok, the Saudi commercial register, domains and social handles.

### Known risks to pass to counsel

- The Alshaya "Sidra" dining complex in Riyadh: check registrations for Sidra / سدرة / سدره in classes 43, 35 and 30, Saudi Arabia first, then Kuwait and Qatar.
- "Sidra" as a variety name: descriptiveness in class 30.
- A row of equal bars is a generic graphic device and resembles a barcode, a progress indicator or a calendar strip; similar marks may well exist in other categories. Distinctiveness rests on the combination with the wordmark.
- The Arabic wordmark is unmodified IBM Plex Sans Arabic Bold with custom spacing (accepted for the test, redraw required before real use). A typeset word in a freely available font is weak as a distinctive mark, and a competitor uses the same typeface for text.

### Status

For the system test the check is recorded and work continues (decision log, 2026-11-13). **For any real use: a formal search and written opinion by a trademark attorney, covering the name and the device, is required before the name or the mark is used, printed or filed.** Usage rule kept in the meantime: always the full name «سدرة للقهوة» / "Sidra Coffee", with "roastery" in running English copy; never "Sidra" alone.

## Colour references

- Pantone references and ICC-calibrated CMYK are waived for system test; required before print (decision log 2026-11-13, ruling e). No Pantone licence or swatch reference is available in this project. CMYK values in `tokens.json` are uncalibrated approximations.

## Images, icons, illustrations

- None used. No stock photography, icon set or third-party artwork appears in any file in `04-identity/`.

## Tools (no licence passes to the client)

- uharfbuzz 0.57 (shaping), fontTools (outlines, instancing), CairoSVG and Pillow (PNG previews and exports), Chromium via Playwright (HTML to PDF and PNG). Open-source build tools; they leave no licensed content in the deliverables.
