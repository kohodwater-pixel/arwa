# Arabic and bilingual design rules

Arabic is a first-class language in this agency, not a translation layer. Design the Arabic version with the same care as the Latin one, and design it first when the audience is primarily Arabic-speaking.

## Typography

- **Never add letter-spacing (tracking) to Arabic.** It breaks the connections between letters. Use kashida-aware justification or a wider typeface instead.
- **No faux bold, faux italic or forced all-caps styling.** Arabic has no capitals or italics; create emphasis with weight, size or colour.
- **Line height:** 1.6–1.9 for body text, more than Latin, to make room for diacritics and descenders.
- **Optical size matching:** Arabic usually looks smaller than Latin at the same point size. Scale the Arabic up (often 10–20%) until the two read as equal.
- **Pair by structure, not by name:** match stroke contrast, weight and tone between the Arabic and Latin typefaces. Prefer families designed with both scripts.
- **Use real Arabic typefaces** with full shaping, ligatures and diacritic support. Confirm the licence covers the client's use (print, web, app).
- **Diacritics (tashkeel):** only where needed for meaning or in Quranic and formal text; make sure they do not collide with the line above.

## Direction and layout

- Arabic layouts are **right to left**: reading order, grids, navigation, progress indicators, arrows, timelines and charts all mirror.
- Do **not** mirror: logos, photographs, clocks, media playback controls, phone numbers, and Latin words or numbers inside Arabic text.
- In bilingual layouts, give each language its own aligned block (Arabic right, Latin left). Do not interleave them line by line.
- Bullets, numbering and indents sit on the right. Tables read from the right-hand column.

## Text handling

- Use Arabic punctuation: ، ؛ ؟ and the correct quotation marks «».
- Decide per client whether numerals are Arabic-Indic (٠١٢٣) or Western (0123) and record it in `brand-context.md`. Never mix within a piece.
- Dates, currencies and units follow the client's market convention.
- Do not break a word across lines and never hyphenate Arabic.
- Translate meaning, not words. Headlines are written natively in Arabic by tone, not converted from English.

## Production checks

- Verify shaping in every export: letters must be connected and in the correct order. Disconnected or reversed letters mean the tool did not shape the text; fix it or outline the text from a tool that does.
- Embed or outline fonts in PDFs and check the result in a second viewer.
- Have the Arabic copy proofread by a native reader before delivery.
