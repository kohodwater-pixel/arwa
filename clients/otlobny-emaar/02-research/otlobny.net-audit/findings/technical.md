# Technical SEO findings: otlobny.net (checked 2026-11-27)
Score: 58/100. Method: existing crawl (23 URLs), plus live header checks (<=1 req/s) and sitemap_discovery.py. Not checkable: PageSpeed/CrUX (blocked), Search Console indexing, rendered-DOM CWV.

## Category status
- Crawlability: PASS with issues (robots OK; sitemap valid but wrong content)
- Indexability: FAIL (duplicates, soft 404, sitemap/canonical conflicts)
- Security: PARTIAL (HTTPS+301 OK; missing HSTS, CSP, X-Frame-Options, Permissions-Policy)
- URL structure: FAIL (query-string URLs for all services)
- Mobile: PASS (viewport present, lang=ar dir=rtl)
- CWV (source): PARTIAL (no image dimensions, no-store caching, third-party script)
- Structured data: PARTIAL (Organization only)
- JS rendering: PASS (server-rendered PHP, content in raw HTML)

## Findings
### High
1. Sitemap lists 3 URLs that canonical to / (?service=operation, hospitality, staffing). Evidence: sitemap.xml; crawl md5 d748a8ac identical to homepage, canonical https://otlobny.net/. Fix: remove from sitemap, or build real pages for them.
2. Sitemap omits 2 real pages: ?service=contracting, ?service=workforce (200, self-canonical, unique content). Fix: add them. Sitemap helper: valid urlset, found via robots.txt; no sitemap_index/wp-sitemap (not needed).
3. Soft 404: /?service=zzzz returns 200 (cache-control no-store, session cookie). Fix: return 404 (or 301 to /) for unknown slugs and send noindex.
4. www.otlobny.net returns 200 with canonical to apex, not a 301. Evidence: curl, HTTP/2 200 plus its own session cookie. Fix: 301 www to apex in Cloudflare Redirect Rule. http to https already 301 (good).
5. All service pages use query strings (/?service=slug). Weak for ranking, easy to duplicate. Fix: clean paths (/services/cleaning/), 301 old URLs, update canonicals and sitemap.

### Medium
6. ?quote_service=* (11 URLs seen) serve the homepage, canonical to / (correct, but crawl waste). Fix: ignore the parameter server-side or add noindex; make sure no internal links point to them.
7. Thin service pages: 102-133 words each, near-identical template and description suffix "حلول احترافية للمنشآت مع طلب عرض سعر مباشر". Fix: expand to 400+ unique words (scope, process, cities, FAQs).
8. Overlapping pages: cleaning vs cleaning-staff, hotel-staffing vs workforce vs staffing, hotel-operations vs operation; keyword cannibalisation. Fix: one page per intent, or differentiate.
9. Cache-Control: no-store, no-cache on every HTML page plus Set-Cookie otlobny_session on every request (including bots and soft-404). Cloudflare shows DYNAMIC, so no edge caching; hurts TTFB (0.4-0.9 s observed) and cacheability. Fix: start sessions only on form/chat actions; send public, s-maxage for HTML with a Cloudflare cache rule.
10. Missing security headers: no HSTS, CSP, X-Frame-Options/frame-ancestors, Permissions-Policy. Present: X-Content-Type-Options, Referrer-Policy. Fix: add HSTS (max-age=31536000 after testing), CSP, frame-ancestors.
11. No Open Graph/Twitter tags on any page checked. Fix: add og:title/description/image/url/locale=ar_SA, twitter:card.
12. Images: 36 img tags on homepage, none with width/height (CLS risk); 32 lazy-loaded (check the LCP image is not lazy). Fix: add dimensions, fetchpriority=high on the hero, serve WebP/AVIF.

### Low
13. Structured data is Organization only. JSON-LD email is info@otlobny.co (domain .co, site is .net); confirm it is correct. Fix: add LocalBusiness/Service (areaServed SA), BreadcrumbList on service pages, sameAs.
14. Sitemap has no lastmod; changefreq/priority are ignored by Google. Fix: add accurate lastmod.
15. Homepage loads a third-party script https://img1.wsimg.com/traffic-assets/js/tccl.min.js (GoDaddy asset, not tested). Check it is intended; it adds a blocking third-party request. Not verified at runtime.
16. Page titles on the home and the 3 duplicate URLs are identical; home title is short (no Saudi city/service keywords). No hreflang (acceptable, single language).
17. Non-existent path returns real 404 but with an iso-8859-1 Apache-style page, not branded. Fix: custom UTF-8 404.
18. robots.txt: Allow /, disallows admin/setup/api/config/includes/storage/docs. It reveals sensitive directory names; ensure they are access-controlled, not just disallowed. No AI-crawler rules (no AI crawler policy defined).

### Info
- llms.txt is 404 (optional).
- /cdn-cgi/l/email-protection 404 is Cloudflare email obfuscation; harmless (noindex), but it is linked in the footer for crawlers; consider a plain mailto or tel.
- Cloudflare provides HTTP/2 and HTTP/3 (alt-svc).

## What works
HTTPS with 301 from http; valid robots.txt and sitemap.xml declared; lang=ar dir=rtl; viewport meta; self-canonicals on distinct service pages; unique titles/descriptions/H1 on 8 service pages; all images have alt text; server-rendered HTML (about 16 KB); single H1 per page; Organization JSON-LD on every page.
