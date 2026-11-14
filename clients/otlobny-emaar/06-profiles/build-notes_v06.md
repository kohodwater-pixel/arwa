# Build notes — «اطلبني إعمار» / OTLOBNY Emaar company profile, draft v06

**Date:** 2026-11-14  **Author:** corporate-designer  **Status:** DRAFT v06. It answers `review_v05_r2.md` and the Creative Director rulings of 2026-11-14. Not approved by the client. Every v01–v05 file is untouched.

## Files
- `otlobny-emaar_company-profile_screen_ar-en_v06.pdf`: 20 pages, 297 × 210 mm, 10.9 MB
- `otlobny-emaar_company-profile_screen_ar-en_v06.html`: the editable source
- `_work/build_profile_v06.py`: the v05 generator with the r2 changes; writes `assets/derived/v06_*.jpg` (31 files, all used)
- `_work/finish_pdf_v06.py` and `_work/contact_v06.py`
- `_work/contact_v06_part1.png` and `_part2.png`, previews in `_work/preview_v06/`
- `_work/build_v06.log` and `_work/check_v06.log`

## Changes from v05
1. **Cover (M1):**
   - Hero changed from the abstract glass facade to the **steel erector on beams**. It shows building in progress, a literal reading of «إعمار». It is also sharper (202 ppi) and gives the cover a strong diagonal against the lattice.
   - The U.S. technician tile is replaced by the **Gulf site workforce**, which moved from p11.
   - The technician image is **no longer used anywhere**.
   - The glass facade moved to the contracting page (p7) as its large image, now at 416 ppi.
   - p11 lost the workforce image. The library has no unused non-demoted image, so that slot is a navy brand diamond.
2. **Works p16 (M2):**
   - Two balanced columns, one per work. Each runs image → caption → ≥ 8 mm → number → title; the Chamber column also has text and scope.
   - Chamber rendering: 88 mm wide, 186 ppi.
   - Dar Al Taqwa photo: 62 mm wide, 137 ppi, the largest size that stays above 130 ppi. It sits on a tint panel that fills its half of the page.
   - Still no scope for Dar Al Taqwa.
3. **Edge rule (m2):** every outer diamond on pp7–12 now bleeds past the trim by about 7 mm (cluster centre moved from 74.25 to 66 mm from the outer edge). No diamond stops just short of the edge.
4. **Lists (m3):** cells are aligned on the first baseline, and the columns are 0.86 / 1.14 so the Arabic has more room. The "Ajeer" lines use balanced wrapping, so «للمستشفيات» and «أجير» no longer sit alone on a line.
5. **Kickers (m1):** the separator is now a dash, «03 – خدماتنا – 01 / 06». Tajawal's raised middle dot is gone.
6. **p13 (m5):** the front three-quarter truck is reframed from the client's full image (`mockup_logistics-trucks_retouched_v03.png`, box 0,0,830,582). The logo on the truck body is now complete. Effective resolution 185 ppi.
7. **Contents (m8):** the Arabic-side section number is removed.
8. **Captions:** stacked, Arabic first then English, the same on p15 and p16.

## Image → page → effective ppi (checked by the build: no source on more than one page)

| Page | Image | ppi |
|---|---|---|
| p1 | steel erector (hero) | 202 |
| p1 | tower with palms | 281 |
| p1 | rope-access glass tower | 284 |
| p1 | Riyadh palm park | 319 |
| p1 | Gulf site workforce | 319 |
| p3 | Madinah plaza | 327 |
| p6 | Madinah panorama | 227 |
| p7 | glass facade | 416 |
| p7 | concrete screeding | 245 |
| p7 | surveyor | 246 |
| p8 | Doha palm walkway | 276 |
| p8 | San Diego dry planting | 276 |
| p9 | HVAC gauges | 333 |
| p9 | rooftop AC units | 245 |
| p9 | distribution board | 460 |
| p10 | rope-access window cleaner | 244 |
| p10 | mop and trolley | 245 |
| p11 | waiter | 245 |
| p11 | catering | 245 |
| p11 | client team mockup | 368 |
| p12 | racking aisle | 244 |
| p12 | client car/scooter mockup | 368 |
| p13 | client truck views: rear 3/4, side, front 3/4, front, rear | 184 / 138 / 185 / 152 / 151 |
| p13 | client rider | 276 |
| p15 | bus shelter | 133 |
| p16 | Chamber rendering | 186 |
| p16 | Dar Al Taqwa entrance | 137 |

## Checks
- **`check_arabic_pdf.py --expect "اطلبني إعمار"`:** PASS. Fonts are Tajawal and IBM Plex Sans, no fallback. 4,494 Arabic characters, no presentation forms.
- **Forbidden strings:** all 0. Shahd/«شهد», «الشركة المختارة», «رائدة», «أطلبني», lorem, TBC, WhatsApp, the old Dar Al Taqwa scope sentence, TAIBA, THERMO, COAST, "157th" / Air National Guard, and the names of the demoted photographers.
- **Text conventions:** no short-vowel marks, no Arabic-Indic digits. Contact details match `brand-context.md`.
- **Contrast:** unchanged from v05. p19 labels 8.96:1, values 12.55:1; p20 credits 7.61:1; footers 5.84:1 on white and 5.50:1 on the tint.
- **Visual check:** all 20 pages viewed on the final contact sheets; pp1, 7, 8, 10, 11, 13 and 16 also viewed at full preview size.

## Not changed, and why
- **m4 (p15 bus shelter):** the litter-free crop is only 550 px wide, so 105 mm (133 ppi) is already its sharpest useful size. The client's original file is needed.
- **m6 (non-Gulf stock):** the red-brick rope-access cleaner (p10) and the San Diego bay planting (p8) stay. The library has no unused, non-demoted Gulf-credible alternative.
- **m7 (faint partner logos), m9 (single-contract line):** these depend on the client.
