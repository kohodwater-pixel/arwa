# Licences — Sidra Coffee identity

> **SYSTEM TEST — FICTIONAL CLIENT.** Invented data for testing Creative Agency OS.

**Version:** v01  **Date:** 2026-11-13  **Prepared by:** Identity Designer

This is a record of what was used and under which licence. It is not legal advice.

## Fonts

| Font | Used for | Source in repo | Licence | Copyright line in the licence file |
|---|---|---|---|---|
| IBM Plex Sans Arabic (Light, Regular, Medium, SemiBold, Bold; static TTF) | All Arabic text; source outlines of the Arabic wordmark (Bold) | `assets/fonts/ibmplexsansarabic/` | SIL Open Font License 1.1 (`OFL.txt` in the same folder) | Copyright © 2017 IBM Corp. with Reserved Font Name "Plex" |
| IBM Plex Sans (variable font, wdth and wght axes) | All Latin text; source outlines of "SIDRA COFFEE" in the logo (SemiBold 600, width 100) | `assets/fonts/ibmplexsans/` | SIL Open Font License 1.1 (`OFL.txt` in the same folder) | Copyright © 2017 IBM Corp. with Reserved Font Name "Plex" |

What the OFL allows, as I read it: free use in print, web, apps and products, including commercial use; embedding in documents; bundling and redistribution with the licence file included. The fonts may not be sold on their own. Documents and artwork made with the fonts, including the outlined logo, are not themselves subject to the OFL.

### Static Latin instances: open point

- The repo holds IBM Plex Sans only as a variable font. For outlining the logo and for PDF embedding by name, six static instances were cut with fontTools (`varLib.instancer`): Light, Regular, Medium, SemiBold, Bold, and Light at 85% width. They are in `04-identity/_work/fonts/` and are **work files**.
- These instances still carry the name "IBM Plex Sans". "Plex" is a Reserved Font Name, and the OFL does not allow a modified version to be distributed under a reserved name. Whether an unaltered instance of a variable font counts as a modified version is not something I can settle.
- **Therefore: do not ship the files in `_work/fonts/` to the client.** For the delivery package, obtain IBM's own static IBM Plex Sans files (official IBM Plex release) and include them with `OFL.txt`. Not done in this task.
- IBM's static release has a Condensed family rather than an 85% width. The "Light 300, width 85%" figure style in the direction therefore depends on the variable font; for print, either use the variable font or agree IBM Plex Sans Condensed Light as the substitute. Decision for the art-director.

## Logo

- Original work made for this client in this project. Arabic wordmark: outlines of IBM Plex Sans Arabic Bold with custom optical spacing. Latin line: outlines of IBM Plex Sans SemiBold with custom tracking. Seven-bar device: drawn from scratch.
- **No trademark search has been made for the mark.** The name check in `03-strategy/naming.md` was a single web search and did not cover SAIP, GCC or WIPO registers. This is not a legal trademark clearance; a formal search by counsel is needed before registration or launch.

## Colour references

- No Pantone licence or swatch reference is available in this project. Pantone values are recorded as "to be matched by printer". CMYK values are uncalibrated approximations.

## Images, icons, illustrations

- None used. No stock photography, icon set or third-party artwork appears in any file in `04-identity/`.

## Tools (no licence passes to the client)

- uharfbuzz 0.57 (shaping), fontTools (outlines, instancing), CairoSVG and Pillow (PNG previews), Chromium via Playwright (HTML to PDF and PNG). Open-source build tools; they leave no licensed content in the deliverables.
