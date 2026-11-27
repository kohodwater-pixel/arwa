# GEO / AI Search Readiness — otlobny.net (PARTIAL, first pass)

Status: partial. Based on _work/crawl/ (robots.txt, sitemap.xml, 23 raw HTML pages). Live AI-UA tests and /.well-known checks pending.

## First-pass findings
- robots.txt: `User-agent: *` Allow /; no AI-specific groups -> all AI crawlers allowed by robots.txt.
- /llms.txt: 404 (optional; ignored by Google Search).
- SSR: all content in raw HTML. Good.
- Organization JSON-LD on home: name, url, logo, email, telephone, description. Missing address, areaServed, sameAs, alternateName (Latin "Otlobny"), foundingDate.
- Email domain is info@otlobny.co while site is otlobny.net (entity-consistency question; verify with client).
- Service JSON-LD on 9 service pages, areaServed = Saudi Arabia.
- Sitemap lists ?service=operation / hospitality / staffing which return the homepage (canonical = /); omits ?service=contracting and ?service=workforce which are real pages.
- Citability: service pages 102-133 words; no city, founding year, client counts, certifications, or figures anywhere.
- FAQ: 4 short Q&As on home, generic.
- Accessibility: header/nav/main/footer landmarks present; quote form labels wrap inputs; chat input placeholder-only; close button "×" no accessible name; partner logos all alt "شريك نجاح".
