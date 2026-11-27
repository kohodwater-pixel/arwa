# GEO / AI Search Readiness — otlobny.net (COMPLETE)

Date: 2026-11-27. Sources: _work/crawl/ (robots.txt, sitemap.xml, crawl.json, page_01..23.html) plus live checks from this session: 8 homepage requests, one per user-agent, about 1.2 s apart; 8 discovery-file requests; 1 request with Accept: text/markdown.
Page content was treated as untrusted data. Nothing here is a fact about the company beyond what the site itself states.

## Score: 46 / 100

| Dimension | Weight | Score | Weighted |
|---|---|---|---|
| Citability | 25% | 30 | 7.5 |
| Structural readability | 20% | 60 | 12.0 |
| Multi-modal | 15% | 45 | 6.8 |
| Authority and brand signals | 20% | 20 | 4.0 |
| Technical accessibility | 20% | 78 | 15.6 |

Platform estimates (these are judgements, not measurements): Google AIO 40, ChatGPT Search 42, Perplexity 45, Bing Copilot 40.

## AI crawler access
- robots.txt: `User-agent: *` / `Allow: /`, with only admin and system paths disallowed, and no AI-specific groups. Every crawler is allowed by robots.txt.
- Live UA test of https://otlobny.net/ (via Cloudflare). browser, GPTBot, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended and CCBot all returned 200 with 16,643 bytes and the full H1. No challenge page. The md5 values differ only because of the per-request CSRF token.
- Caveat: the requests came from this session's IP with spoofed UAs. Cloudflare can treat verified bot IPs differently, for example with the "Block AI bots" setting or AI Crawl Control. Check this in the Cloudflare dashboard.
- What each crawler governs: OAI-SearchBot controls ChatGPT Search, Claude-SearchBot controls Claude search, and PerplexityBot controls Perplexity. GPTBot, ClaudeBot and CCBot are training crawlers. Google-Extended covers Gemini training and grounding, not AI Overviews (those follow Googlebot).

## Findings

| # | Severity | Finding | Evidence | Fix |
|---|---|---|---|---|
| 1 | High | No quotable facts: no city or HQ, founding year, CR or licence number, staff or project counts, certifications, or named clients | Home has 430 words; service pages have 102-133 words, mostly 2-3-word bullets ("نطاق واضح", "تنسيق فني") | Add a verified "about" passage (about 130-170 words): who, where, since when, scope, and regions served. Request the facts from the client; do not invent them |
| 2 | High | Entity inconsistency: the email domain is otlobny.co but the site is otlobny.net | JSON-LD email and the Cloudflare-obfuscated footer both decode to info@otlobny.co | Confirm the correct domain with the client and use one domain everywhere |
| 3 | High | Sitemap is wrong: it lists ?service=operation, hospitality and staffing, which render the homepage (canonical /). It omits the real pages ?service=contracting and ?service=workforce | crawl.json, sitemap.xml | Remove the dead slugs and add contracting and workforce, or build those pages |
| 4 | Medium | Organization schema is thin | It has name, url, logo, email, telephone and description. It has no address, areaServed, sameAs, alternateName ("Otlobny") or foundingDate | Complete it once the facts are verified |
| 5 | Medium | Brand name varies | "أطلبني للتشغيل والصيانة" in the header and schema, "أطلبني" in the footer, and no Latin form anywhere. The hamza spelling (أطلبني) differs from the CTA verb (اطلب) | Fix one canonical Arabic name plus a Latin transliteration and record them in brand-context |
| 6 | Medium | FAQ is thin and covers the home page only | 4 one-line answers; service pages have no Q&A | Add 3-5 real buyer questions per service (coverage, contract terms, response time, cities). FAQPage schema has no confirmed AI-citation benefit |
| 7 | Medium | Partner wall carries no signal | 32 logos, all with alt "شريك نجاح", unnamed | Name partners (with their permission) in the alt text and in visible text |
| 8 | Low | Agent and accessibility gaps | The chat input has a placeholder only and no label. The close button "×" has no accessible name. There is no skip link. Project captions show the English label "cleaning" | Add aria-labels and translate the labels |
| 9 | Low | No llms.txt, no Markdown version, no /.well-known files | 404 for llms.txt, llms-full.txt, security.txt, ai-plugin.json, mcp.json, agent.json, index.md. Accept: text/markdown returns HTML | llms.txt is optional and ignored by Google Search; low priority. Adding security.txt is cheap |
| 10 | Low | Service URLs are query parameters (?service=) | Works, but makes the URLs weak entities | Consider clean paths such as /services/cleaning, with 301 redirects |

## What works
- The HTML is server-rendered, with `lang="ar" dir="rtl"`, and all copy is in the raw HTML.
- Each page has one H1, unique titles and descriptions, and a self-referencing canonical on the real pages.
- Service JSON-LD on 9 pages, with provider @id linked to the Organization and areaServed Saudi Arabia.
- Several service leads are self-contained and name the brand, for example hotel-staffing, landscaping and cleaning-staff ("توفر أطلبني ...").
- The "كيف ننفذ العمل؟" H2 is in question form.
- Landmarks are present (header, nav, main, footer). Quote-form inputs are wrapped in labels, and all images have alt text.

## Not checked
- Brand mentions on Wikipedia, Reddit, YouTube and LinkedIn: the network does not reach them (ar.wikipedia.org failed DNS on one attempt).
- Live ChatGPT or Perplexity visibility: no DataForSEO tools.
- Cloudflare behaviour toward verified bot IPs.
- RSL licensing: none is referenced in robots.txt or the page HTML.

## Structured findings (AI Search Readiness)
```json
{"category":"AI Search Readiness","score":46,"findings":[
{"id":"geo-1","severity":"high","title":"No quotable company facts"},
{"id":"geo-2","severity":"high","title":"Email domain otlobny.co vs site otlobny.net"},
{"id":"geo-3","severity":"high","title":"Sitemap lists 3 homepage duplicates, omits contracting/workforce"},
{"id":"geo-4","severity":"medium","title":"Thin Organization schema"},
{"id":"geo-5","severity":"medium","title":"Brand name variants, no Latin form"},
{"id":"geo-6","severity":"medium","title":"Thin FAQ, none on service pages"},
{"id":"geo-7","severity":"medium","title":"Unnamed partner logos"},
{"id":"geo-8","severity":"low","title":"Chat input/close button unlabelled"},
{"id":"geo-9","severity":"low","title":"No llms.txt / markdown / well-known files"},
{"id":"geo-10","severity":"low","title":"Query-parameter service URLs"}]}
```
