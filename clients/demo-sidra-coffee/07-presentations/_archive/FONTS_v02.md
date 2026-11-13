# Fonts for the Sidra Coffee presentation

> **SYSTEM TEST — FICTIONAL CLIENT.**

Applies to `demo-sidra-coffee_presentation_cafe-owners_ar_v02.pptx`. Date: 2026-11-13.

The PPTX does **not** embed its fonts (python-pptx cannot embed fonts in a PowerPoint file). Install the two families below on any machine that opens or presents the deck; otherwise PowerPoint, Keynote or LibreOffice will substitute another typeface and the line breaks will change. The PDF export has its fonts embedded and needs nothing installed.

| Family | Used for | Weights used in the deck | Files in this repository | Licence |
|---|---|---|---|---|
| IBM Plex Sans Arabic | All Arabic text (theme complex-script font, major and minor) | Regular 400, Bold 700 | `assets/fonts/ibmplexsansarabic/` (static TTF: Light, Regular, Medium, SemiBold, Bold) | SIL Open Font License 1.1, `OFL.txt` in the same folder |
| IBM Plex Sans | Latin text and numerals: the email address, 250, 1, step numbers, slide counter (theme Latin font, major and minor) | Regular 400, Bold 700 | `assets/fonts/ibmplexsans-static/` (static TTF: Light, Regular, Medium, SemiBold, Bold) and `assets/fonts/ibmplexsans/` (variable font) | SIL Open Font License 1.1, `OFL.txt` in `assets/fonts/ibmplexsans-static/` |

Copyright © 2017 IBM Corp. with Reserved Font Name "Plex". The OFL allows use, embedding and redistribution with the licence file; the fonts may not be sold on their own. Full licence notes for this client: `04-identity/licences.md`.

## How to install

- This repository: `bash scripts/setup.sh` installs both families for the current user.
- Windows or macOS: open each `.ttf` file from the folders above and choose Install. Use the static files (`ibmplexsans-static/`), not the variable font, for PowerPoint.

## How the fonts are set in the file

- Theme font scheme "Sidra Coffee": Latin = IBM Plex Sans, complex script and Arabic script = IBM Plex Sans Arabic, for both headings and body. New slides made from the four layouts pick these up without manual formatting.
- Latin letters and numerals inside Arabic text are separate runs set explicitly in IBM Plex Sans.
- No other typeface is used. Bullets take IBM Plex Sans.

## Known limits

- For the delivery package, the font files and both `OFL.txt` files must be copied to `08-final-delivery/07-fonts-and-licences/`. Not done here; this is a working folder.
- `04-identity/licences.md` warns that static IBM Plex Sans instances cut from the variable font must not be shipped. I have not verified whether the files in `assets/fonts/ibmplexsans-static/` are IBM's own release or cut instances; confirm before they go to a client.
- On this machine both the variable and the static IBM Plex Sans are installed under the same family name. LibreOffice drew the bold Latin text from the variable font, so in the PDF those glyphs are embedded as Type 3 outlines. They look correct on screen; for print, export on a machine with only the static files installed.
