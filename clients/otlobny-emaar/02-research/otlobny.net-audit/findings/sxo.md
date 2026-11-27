# SXO findings: otlobny.net (أطلبني)

Date: 2026-11-27. Status: COMPLETE.
Score label: **SXO Gap Score** (separate from the SEO Health Score).

## Method and limits (read first)

- Site data: `_work/crawl/` (crawl.json + raw HTML page_01..23). Not re-rendered with Playwright in this pass; the raw HTML contains full server-rendered text (homepage 430 words), so the site is not an SPA shell. Above-the-fold layout and mobile rendering were not visually checked.
- SERP data: 6 queries through the agent WebSearch tool. **This is not a Google SERP.** The tool returns a list of titles/URLs plus a summary; it does not show ad slots, map pack, People Also Ask, featured snippets or AI Overview, and results are not localised to a Saudi IP. Ranking pages were classified from title + URL only; none were opened (other hosts are blocked on this network). Treat SERP conclusions as directional.
- Not assessed: real Google rankings, Search Console data, Google Business Profile, backlinks, Core Web Vitals, the chat assistant's answers, form delivery.

## SERP observations (WebSearch tool, 2026-11-27)

| Query | What appeared (by title/URL) | Dominant type |
|---|---|---|
| شركة تشغيل وصيانة منشآت السعودية | Large FM brands (SGS O&M service page, Xenel/SSOC), PIF/news on FMTECH, alwatan news, HRSD PDF | Corporate service pages + news (informational/brand) |
| شركة نظافة منشآت بالرياض عقود | mourjan.com, opensooq (classifieds), sabq "best cleaning companies" listicle, slideshare/calameo profiles | Classifieds/directories + listicle |
| توفير عمالة فندقية السعودية | naukrigulf, sabbar (job boards), mourjan labour-recruitment, Saudization news (sabq, DLA Piper, gulfbusiness) | Job boards + regulation news (mixed intent) |
| شركة تشغيل وصيانة الفنادق في جدة | naukrigulf/sabbar jobs, mourjan Jeddah maintenance, hoteltechreport article | Job boards + classifieds |
| توفير عمال نظافة للشركات بالرياض | 9 of 9 results mourjan.com (Riyadh cleaning-services / labour pages) | Classifieds with city pages |
| شركة صيانة مباني وتشغيل مرافق بالرياض عقود سنوية | sabbar/jooble jobs, mourjan Riyadh maintenance, mstaml listings | Classifieds + job boards |

Consensus: for transactional B2B queries the visible winners are **city-specific listing pages** (mourjan `/sa/al-riyadh/cleaning-services/`) and job boards; no small FM company's own service page surfaced in any of the 6 lists. Confidence in "classifieds/city page dominant": ~70% for cleaning/labour queries; low for O&M (brand/news). Signal: almost every winning URL carries a **city** in the path or title.

Regulatory signal (from search summaries, verify before use): the HRSD/Ministry of Tourism Saudization of 41 tourism professions (phased from 22 Apr 2026) and 2025 rules allowing outsourcing of Saudi-designated hotel roles only to licensed/authorised providers. A hotel buyer will want proof the supplier is licensed and compliant.

## Target page classification

- Homepage: multi-service corporate landing page (hero, 9 service cards, 2 project images, 32 partner logos, 4 FAQs, quote form).
- `/?service=<slug>`: thin service detail view, 102-130 words, one image, Service JSON-LD with `areaServed: المملكة العربية السعودية`.
- No city pages, no about/licences page, no case studies, no articles.

## Findings

| # | Severity | Finding | Evidence | Fix |
|---|---|---|---|---|
| 1 | CRITICAL | Page-type mismatch: SERPs reward city-scoped service/listing pages; the site has no city landing pages and no city named anywhere (coverage area unknown) | 6/6 query sets show city-scoped winners (mourjan `/al-riyadh/...`); site text and schema mention only "المملكة العربية السعودية" | Confirm with client which cities are actually served; build service × city pages only for those (see architecture) |
| 2 | HIGH | Service pages too thin to satisfy a B2B buyer or compete | 102-130 words each (crawl.json); hotel-operations page = intro + 4 bullet "مزايا" + 3 steps | 600-1,000 words per core service: scope list, facility types, contract models, staffing levels, SLA/response, compliance, FAQ, proof |
| 3 | HIGH | Zero verifiable trust signals | No CR number, licences, address, years active, named clients or figures; 32 partner logos all alt="شريك نجاح" with no names; projects are 2 generic images | Add CR/VAT/licence numbers, HRSD/manpower licence if held, office address, named partners (with permission), 2-3 case studies; request all facts from client, do not invent |
| 4 | HIGH | Sitemap sends 3 URLs (operation, hospitality, staffing) that return the homepage; 2 real services (contracting, workforce) missing from sitemap | crawl.json: page_04-06 md5 = homepage, canonical `/`; sitemap.xml lacks `contracting`, `workforce` | Either build those 3 pages or remove from sitemap; add the 2 missing ones |
| 5 | MEDIUM | Query-parameter URLs (`/?service=`) for the main money pages | All service URLs are params on `/` | Move to clean paths with 301s (architecture below) |
| 6 | MEDIUM | Overlapping services split intent | cleaning vs cleaning-staff; workforce vs hotel-staffing; hotel-operations overlaps maintenance+cleaning | Group as 4 pillars (التشغيل والصيانة / النظافة / توفير العمالة / الفنادق) with sub-pages |
| 7 | MEDIUM | Hotel staffing query has job-seeker intent mixed in | naukrigulf/sabbar dominate توفير عمالة فندقية | Title/H1 must say "للفنادق والمنشآت" and B2B contract language; add a separate careers page so job seekers are routed away from the quote form |
| 8 | MEDIUM | Schema incomplete | Organization lacks address, sameAs, areaServed; no FAQPage, BreadcrumbList, LocalBusiness | Add once facts are confirmed (`/seo schema`) |
| 9 | LOW | Contact friction | No `tel:` link (only wa.me); email domain otlobny.co differs from site otlobny.net | Add tap-to-call in header; confirm the email domain with client |
| 10 | LOW | No pricing model or response-time statement | FAQ says scope is "وفق احتياج المنشأة" only | State contract models (monthly/annual, per-worker, per-sqm, per-visit) and response commitments the client can honour |

`/?quote_service=<slug>` returns the homepage with the service preselected and canonical `/`: works as intended, no action except keeping it out of the sitemap.

## SXO Gap Score: 32/100

| Dimension | Score | Evidence |
|---|---|---|
| Page type | 4/15 | No city or clean service URLs; 3 sitemap URLs duplicate home |
| Content depth | 3/15 | 100-130 words per service |
| UX signals | 8/15 | Clear quote CTA, WhatsApp, preselected quote form, chat guide; no tel link, no coverage info |
| Schema | 7/15 | Organization + Service present; no address/FAQ/breadcrumb |
| Media | 5/15 | 2 project images, 1 image per service, unnamed logos |
| Authority | 2/15 | No licences, CR, address, named clients, case studies |
| Freshness | 3/10 | No dates anywhere; only © 2026 |

## User stories (each tied to a signal)

1. Hotel facilities/operations manager in Jeddah: "I need a licensed supplier for housekeeping and maintenance staff so that I stay compliant with Saudization rules." Signal: hotel queries return job boards + Saudization/outsourcing-licence news.
2. Government procurement officer: "I need a company's CR, classification and past public-sector contracts so that I can shortlist it for a tender." Signal: O&M query returns established FM brands, PIF/FMTECH news and an HRSD PDF (institutional, credential-led).
3. Business owner in Riyadh needing cleaning staff: "I need workers available in my city on a monthly contract with a clear price basis so that I can start quickly." Signal: 9/9 mourjan Riyadh cleaning/labour pages, ads lead with monthly/annual rental and immediate availability.

## Persona scores (Relevance / Clarity / Trust / Action, 25 each)

| Persona | Page | R | C | T | A | Total |
|---|---|---|---|---|---|---|
| Procurement officer (gov) | Homepage | 14 | 10 | 4 | 12 | **40** |
| | `/?service=maintenance` | 12 | 8 | 3 | 13 | **36** |
| Business owner, cleaning staff | Homepage | 15 | 11 | 6 | 15 | **47** |
| | `/?service=cleaning-staff` | 17 | 9 | 5 | 16 | **47** |
| Hotel manager | Homepage | 15 | 11 | 6 | 15 | **47** |
| | `/?service=hotel-operations` | 18 | 10 | 5 | 16 | **49** |

Needed before a quote request, present (Y) / missing (N): scope Y (bullets only), coverage area N, proof N, licences N, pricing model N, response time N, contact path Y.

Fixes, weakest first:
- Procurement (36-40): "عن أطلبني" page with CR, VAT, licences, classification, address, sectors served, downloadable company profile PDF.
- Cleaning-staff owner (47): cities served, contract model (monthly/annual, per worker), minimum team size, lead time, nationality/uniform/supervision policy, tel link.
- Hotel manager (47-49): compliance statement (licence for outsourcing, Saudization handling), staffing roles list, hotel case study, SLA.

## Recommended page architecture

```
/                                   home: pillars, cities, proof, quote
/services/                          hub
/services/operation-maintenance/    التشغيل والصيانة (+ contracting as section or child)
/services/cleaning/                 نظافة المنشآت
/services/manpower/                 توفير العمالة (cleaning-staff, workforce as sections)
/services/hotels/                   تشغيل وصيانة الفنادق + عمالة فندقية
/services/landscaping/  /services/logistics/  /services/contracting/
/cities/riyadh/ , /cities/jeddah/ ...           ONLY cities the client confirms
/cities/riyadh/cleaning/ etc.                   only where real local capacity/proof exists
/about/                             CR, licences, address, team, sectors
/projects/ and /projects/<slug>/    case studies (client-supplied facts)
/careers/                           routes job seekers away from quote form
/quote/                             standalone form (noindex optional)
/blog/                              contract guides (e.g. عقد نظافة سنوي: ما يشمله)
```
301 every `/?service=<slug>` to its new path; drop operation/hospitality/staffing params from the sitemap until pages exist.

Cross-skill: `/seo content` (E-E-A-T), `/seo schema`, `/seo local` (GBP per city), `/seo page`.
