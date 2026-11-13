# Licences — Sidra Coffee identity

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS.

**Version:** v02  **Date:** 2026-11-13  **Previous version:** `_archive/licences_v01.md`  **Prepared by:** Identity Designer

This is a record of what was used and under which licence. It is not legal advice.

## Fonts

| Font | Used for | Source in repo | Licence | Copyright line in the licence file |
|---|---|---|---|---|
| IBM Plex Sans Arabic (Light, Regular, Medium, SemiBold, Bold; static TTF) | All Arabic text; source outlines of the Arabic wordmark (Bold) | `assets/fonts/ibmplexsansarabic/` | SIL Open Font License 1.1 (`OFL.txt` in the same folder) | Copyright © 2017 IBM Corp. with Reserved Font Name "Plex" |
| IBM Plex Sans (official static TTF: Light, Regular, Medium, SemiBold, Bold) | All Latin text in v02 files | `assets/fonts/ibmplexsans-static/` | SIL Open Font License 1.1 (`OFL.txt` in the same folder) | Copyright © 2017 IBM Corp. with Reserved Font Name "Plex" |

What the OFL allows, as I read it: free use in print, web, apps and products, including commercial use; embedding in documents; bundling and redistribution with the licence file included. The fonts may not be sold on their own. Documents and artwork made with the fonts, including the outlined logo, are not themselves subject to the OFL.

### Latin font files (changed in v02)

- All v02 files (`03-system/brand-v02.css`, business card v02, bag label v02, guidelines v02) use the **official static IBM Plex Sans files** in `assets/fonts/ibmplexsans-static/` (Light, Regular, Medium, SemiBold, Bold, with `OFL.txt`). The guidelines v02 PDF embeds IBMPlexSans, -Light, -Medm, -SmBld and -Bold plus four IBM Plex Sans Arabic weights, and nothing else.
- The variable font and the six instances I cut from it in round 1 (`04-identity/_work/fonts/`) are no longer referenced by any v02 file. They are kept only because the v01 HTML files link to them. **Do not ship `_work/fonts/` to the client:** those instances carry the Reserved Font Name "Plex".
- The 85% width figure style was dropped. Large Latin figures are IBM Plex Sans Light 300 at regular width.
- One exception to note: the Latin line "SIDRA COFFEE" inside the logo SVGs was outlined in round 1 from the SemiBold instance cut from the variable font, not from the official static file. The logo contains outlines only, so no font file is distributed with it. I have not compared the two outlines; they should be identical at wght 600, wdth 100, but that is unverified.

## Logo

- Original work made for this client in this project. Arabic wordmark: outlines of IBM Plex Sans Arabic Bold with custom optical spacing. Latin line: outlines of IBM Plex Sans SemiBold with custom tracking. Seven-bar device: drawn from scratch.
- Icon v02: three stacked rows of the same seven-bar device, drawn from scratch.

## Preliminary mark conflict check (review issue 16)

**This is not a legal trademark clearance.** It is a record of what has and has not been looked at.

What was checked:

| Check | By whom | Result |
|---|---|---|
| The name "Sidra" / «سدرة» as a roastery or coffee brand in Saudi Arabia | naming-specialist, one web search in English and Arabic, 2026-11-13 (`03-strategy/naming.md` section 2.3) | No roastery or café of that name appeared. One search is weak evidence. |
| "Sidra" as a coffee variety name | naming-specialist, same date | Confirmed: it is a variety name in the specialty trade. Possible descriptiveness problem in class 30; a question for counsel. |
| The mark against my own knowledge | identity-designer, from memory only | I do not know of a coffee brand using a row of seven bars with one lit under an Arabic wordmark. This is recall, not a search, and proves nothing. |

What was **not** checked:

- **No search of any kind has been run for the mark itself** (the seven-bar device, the wordmark, the lockups). The identity-designer agent has no web or image-search tools in this environment.
- No trademark register: SAIP (Saudi Arabia), GCC, WIPO Global Brand Database, in class 30 (coffee), class 43 (café services) or any other class.
- No reverse-image or logo-similarity search.
- No look at the real identities of Camel Step, Elixir Bunn or Brew92: their websites could not be opened during research, and the audit's visual notes are unverified recall. The Creative Director will add the competitor comparison from research.
- No check of other "Sidra" brands in the region outside coffee, of GCC cafés named Sidra, of domains or of social handles.

Known risks to pass to counsel:

- A row of equal bars is a generic graphic device and resembles a barcode, a progress indicator or a calendar strip; similar marks may well exist in other categories. Distinctiveness rests on the combination with the wordmark.
- The Arabic wordmark is unmodified IBM Plex Sans Arabic Bold with custom spacing (accepted for the test, redraw required before real use). A typeset word in a freely available font is weak as a distinctive mark.

Required before registration or launch: a formal search and opinion by trademark counsel.

## Colour references

- Pantone references and ICC-calibrated CMYK are waived for system test; required before print (decision log 2026-11-13, ruling e). No Pantone licence or swatch reference is available in this project. CMYK values in `tokens.json` are uncalibrated approximations.

## Images, icons, illustrations

- None used. No stock photography, icon set or third-party artwork appears in any file in `04-identity/`.

## Tools (no licence passes to the client)

- uharfbuzz 0.57 (shaping), fontTools (outlines, instancing), CairoSVG and Pillow (PNG previews), Chromium via Playwright (HTML to PDF and PNG). Open-source build tools; they leave no licensed content in the deliverables.
