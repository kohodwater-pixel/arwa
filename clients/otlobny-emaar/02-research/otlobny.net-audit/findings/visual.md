# Visual / mobile audit: otlobny.net (home, ?service=cleaning)
Tested with system Playwright (plugin runtime rejects non-bundled scripts). Desktop 1440x900, mobile 390x844 (touch). Screenshots in ../screenshots/: home|cleaning _ desktop|mobile _ fold|full.png, home_mobile_menu_open.png. sandbox:false was not reported (default chromium.launch()).

Font note: page loads IBM Plex Sans Arabic from fonts.googleapis.com / fonts.gstatic.com; it rendered correctly here, so no font fallback was seen. Blocked/failed here only: img1.wsimg.com tccl.min.js (GoDaddy monitor) and static.cloudflareinsights.com beacon (environment, not a design issue).

## Findings
1. HIGH - Both project images return HTTP 403: /assets/images/project-01.png and project-02.png. Section "المشاريع" shows two broken-image icons with alt text over empty 390px-tall boxes (home_mobile_full.png). Fix: restore files/permissions; add width/height; replace "cleaning" English category label with Arabic.
2. HIGH - Mobile menu button (☰, 34x44) does nothing: nav is display:none under the mobile breakpoint and tapping leaves it hidden (home_mobile_menu_open.png). The header "اطلب عرض سعر" CTA also vanishes on mobile (0x0). Fix: JS toggle / drawer including the quote link.
3. MEDIUM - Quote path on mobile: hero CTA is visible above the fold (133x48 at y=561, home_mobile_fold.png), good. But the quote form is at the very bottom of a 7,793px page; there is no tap-to-call (0 tel: links) and WhatsApp exists only in the footer text link. Fix: sticky WhatsApp/call buttons; add tel:+966549555514.
4. MEDIUM - Service pages (?service=cleaning) have no hero image, thin content (two lists, three steps), no inline form; CTA is at the bottom only (cleaning_mobile_full.png). The floating "اسأل مرشدك" FAB overlaps heading text ("كيف ننفذ العمل") on scroll. Fix: add bottom padding/z-order, move FAB, add inline CTA.
5. MEDIUM - Tap targets under 44px: "استكشف التفاصيل ←" links 297x19 (x9), FAQ summaries 351x33, footer email/WhatsApp links 19px high, "العودة للرئيسية" 110x24, FAB 41px high. Fix: min-height 44px padding.
6. LOW - Hero video: preload=none, no poster; mobile falls back to a plain dark gradient, so the above-the-fold mobile hero has no imagery (logo only) while desktop shows the video frame. Add poster and a still image.
7. LOW - Hero text over video on desktop: subtitle contrast is moderate over bright glass; the overlay is light on the left only. Body contrast on dark theme is fine (text rgb 236,245,248 on rgb 8,19,28, about 17:1); small grey card text (~13px) looks lower contrast, verify ≥4.5:1.
8. LOW - Arrows "←" in links are correctly pointing left for RTL. The "← العودة للرئيسية" back link places the arrow on the left of the label, which is acceptable in RTL, but the link is ~24px high.

## Passes
Viewport meta correct (width=device-width,initial-scale=1). No horizontal overflow (scrollWidth = 390 / 1440 on both pages). RTL alignment, letter joining and order correct; base font 16px. H1 visible above the fold on mobile.

## Images (HTML in _work/crawl/page_01.html)
36 imgs: logo x2, project x2, partners x32.
- Alt: logo alt fine; project alts descriptive but generic; ALL 32 partner logos use identical alt "شريك نجاح" (no brand names) - poor.
- Formats: all PNG, no WebP/AVIF, no srcset. logo.png is 1.47 MB at 2048x1104 shown at 57px (header) and 300px: severe over-delivery and the LCP-adjacent asset.
- width/height attributes: none on any image (CLS risk). Dimensions: partner logos 360x180 shown at 108x54 (ok).
- Lazy loading: partners lazy (good); project images, logo not lazy (project images are below the fold, should be). Hero logo should be eager.
- Broken: project-01/02 403.
- No OG image or image sitemap checked in this pass.

Images score: 38/100
(alt 8/25, formats/size 5/25, dimensions 0/15, lazy 10/15, delivery/broken 5/20, relevance 10/0 rounded.)
