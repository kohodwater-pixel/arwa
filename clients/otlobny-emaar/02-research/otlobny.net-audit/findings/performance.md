# Performance / Core Web Vitals (LAB ONLY) - otlobny.net, 2026-11-27

NO FIELD DATA. PSI, CrUX and Google APIs were blocked, so there is no CrUX/p75 data. All figures are single-run lab measurements from a cloud container (system Playwright Chromium, plugin renderer not used; no sandbox warning was raised). INP cannot be measured in the lab; TBT is the proxy. Mobile profile: 412px, 4x CPU slowdown, 1.6 Mbps / 150 ms RTT. Desktop profile: 1350px, unthrottled.
Third-party hosts requested: fonts.googleapis.com and fonts.gstatic.com (loaded OK here, so the allowlist passed them), img1.wsimg.com/traffic-assets/js/tccl.min.js (GoDaddy tracker, blocked), static.cloudflareinsights.com beacon (blocked). Blocked hosts mean real-user timings are likely slightly worse. wa.me is a link only.

## Measured
| Page / profile | TTFB | FCP | LCP (element) | CLS | TBT | Requests | Transfer |
|---|---|---|---|---|---|---|---|
| Home mobile | 648 ms | 2.1 s | 16.3 s (logo.png 1.47 MB) | 0.003 | 0 ms | 15 | 5.7 MB (incl. 4 MB hero video) |
| Home desktop | 547 ms | 1.2 s | 1.3 s (hero video poster/frame) | 0.007 | 0 ms | 47 | 6.5 MB |
| Service mobile | 235 ms | 0.9 s | 0.9 s (text) | 0.052 | 0 ms | 12 | 1.6 MB |
| Service desktop | 551 ms | 0.86 s | 0.86 s (H1) | 0.011 | 0 ms | 12 | 1.7 MB |

Home DOM: 295 elements. Service page DOM: 70 elements. Longest main-thread task: 383 ms (home mobile, 4x CPU). Mobile LCP is inflated by throttling and by the video and logo competing for bandwidth, but the direction is real.

## Score: 62/100 (lab estimate, my judgement, not a Lighthouse score)
Desktop is fast and CLS and TBT are clean. Mobile homepage LCP is poor, and page weight is large. The service page is good.

## Findings
1. HIGH - 1.47 MB logo.png (2048x1104) displayed at 48x26 and 268x144, used twice on every page. It is the mobile home LCP element at 16.3 s (lab) and the only image on the service page. No width/height, no srcset. Fix: export SVG, or WebP/AVIF at 2x display size (about 5-15 KB), add width/height, add `fetchpriority="high"` on the header logo.
2. HIGH - Hero video background-one.mp4 is 4.0 MB (preload="none", but on desktop it is the LCP element and loaded in the first 3 s). Mobile transferred it too. Fix: use a poster image, serve a compressed 720p version of 1 MB or less, skip the video on mobile or when Save-Data is on, and don't make it the LCP.
3. MEDIUM - 36 images, all PNG, no srcset. 32 partner logos are 360x180 PNGs displayed at 108x54, 20-38 KB each, about 1 MB total (desktop images 2.28 MB). 4 images are not lazy, so the partner logos are lazy-loaded correctly. Fix: WebP/AVIF or SVG at 216x108, and explicit dimensions.
4. MEDIUM - /assets/images/project-01.png and project-02.png return 403 (both through curl and the browser). These are broken images in the "projects" section, 412x430 on mobile. They also cause a visible empty box and a risk of layout shift. Fix: check permissions or upload paths. This is a functional bug, not only performance.
5. MEDIUM - Google Fonts is loaded through `@import` inside site.css, a chained request that delays font discovery. It uses 6 woff2 files (about 146-192 KB), and `display=swap` is present. Fix: self-host IBM Plex Sans Arabic (subset, 2-3 weights), preload the main one, or use `<link rel=preconnect>` plus a `<link>` instead of `@import`. Self-hosting also removes the third-party dependency.
6. LOW/MEDIUM - HTML is `Cache-Control: no-store, no-cache, must-revalidate`, `cf-cache-status: DYNAMIC`, with a PHP session cookie on every anonymous request. Cloudflare cannot cache it. TTFB is 0.55-0.65 s on home, which is under the 0.8 s guideline but not edge-fast. Fix: stop `session_start()` on public pages, send `s-maxage` plus a Cloudflare cache rule for the homepage, or use stale-while-revalidate.
7. LOW - Static assets have only `max-age=14400` (4 h), including the images, CSS and JS. Fix: versioned URLs with `max-age=31536000, immutable` (CSS already has `?v=`).
8. LOW - The CSS is render-blocking (one stylesheet, 3 KB gzip, fine). site.js is 0.9 KB, no heavy JS. A blocked third-party tracker (tccl.min.js) is loaded synchronously, no `async`. Fix: add `async` or remove it if unused.
9. LOW - Service page CLS 0.052 on mobile (under 0.1, good). Probably caused by the font swap. Adding dimensions, and a size-adjusted fallback font, would help.
10. INFO - JS main thread is light (TBT 0 ms), so INP risk looks low, but this is not a measurement.

## Priority order
Compress logo (1), compress/replace hero video (2), fix 403 images (4), convert partner images (3), self-host fonts (5), cache headers (6, 7).
Expected result: mobile home LCP from 16 s lab to a lab target of 2.5-3.5 s.

Raw script: /tmp/claude-0/-home-user-arwa/ed564dc0-de5d-58c9-befe-0e9230a34c41/scratchpad/m.js (not in the output dir).
