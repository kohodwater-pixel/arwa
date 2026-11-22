# HIPPO — box clip, franchise invitation card: notes

Date: 2026-11-22. By: graphic-designer. Status: v01, flat artwork, not reviewed, not composited.
Built to `../hippo_box-clip_direction_ar-en_v01.md`, section 3.

## Files
- `hippo_box-clip_invitation-card_ar_v01.png` — 1200 × 3120 px (W × 2.6 W), sRGB, opaque white.
- `_work/hippo_box-clip_invitation-card_480w_ar_v01.png` — 480 × 1248 px, the in-video size, legibility proof only.
- `src/card.html`, `src/card.css` — editable source; every size is a share of the card width (W = viewport width).
- `src/render.cjs` — `node render.cjs <W> <out.png>` (Playwright/Chromium); also prints boxes and the fonts actually used.
- `src/assets/logo.svg` — converted from the client's `hippo-logo-vector.pdf` with pdftocairo; same vector paths and colours; only the empty artboard around the mark was cropped (viewBox).
- `src/assets/qr.svg` — regenerated (segno 1.6.6), version 5, error correction M, 37 modules, #181717 on white, no centre logo.
- `src/assets/fonts/` — Tajawal Medium, Bold, ExtraBold + OFL.txt, from `assets/fonts/tajawal/`.

## Copy used (as briefed, unchanged)
امتياز هيبو التجاري · افتح هيبو / في مدينتك. · علامة سعودية منذ 2021 / 5 فروع في منطقتين · قدّم طلب الامتياز

## Layout, top to bottom (share of W)
margin 0.07 · logo box 0.34 × 0.5375 · gap 0.05 · label 0.085 Bold (line 0.10) · gap 0.05 · lime band 0.45, headline 0.15 ExtraBold, line height 1.25 · gap 0.05 · proof 0.068 Medium, line height 1.6 · gap 0.018 · QR white square 0.78 · gap 0.02 · black pill 0.78 × 0.15, text 0.08 ExtraBold lime · gap 0.057 · pink strip 0.05.

## Departures from the direction, and why
- Client's own QR image not used as is: it has a logo in the centre, navy modules and 49 modules per side; the direction forbids the first two. Regenerated from the same URL.
- Module = W/60 (not 0.78 W / 45), so modules are whole pixels at W = 480 (8 px) and W = 1200 (20 px). Quiet zone is therefore 4.9 modules inside the same 0.78 W white square.
- Gaps next to the QR square are 0.018 and 0.02 W, not 0.05: the elements at their stated sizes plus six 0.05 gaps come to 2.66 W, more than 2.6 W. The quiet zone already separates the code; clear white to the nearest ink is 7.1 modules above and 6.1 below.
- Logo artwork is 0.3375 W wide inside its 0.34 W box (2 pt of air kept in the SVG so no edge is shaved).
- Pill text lowered 0.006 W for optical centring.

## Assumptions
- "Full-width lime band" = edge to edge of the card.
- The logo's own lime (about #B3DB18 in the client's PDF) differs slightly from the palette lime #BBD032 of the band; the logo is left as supplied.
