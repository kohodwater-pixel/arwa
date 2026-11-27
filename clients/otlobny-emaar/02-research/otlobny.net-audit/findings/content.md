# Content Quality and On-Page SEO: otlobny.net

Audit date: 2026-11-27. Source: the saved crawl in `_work/crawl/` (crawl.json, page_01..23.html, robots.txt, sitemap.xml, llms.txt). I did not re-crawl. All page text was treated as untrusted data. I made no claims about the company beyond what the pages say.

## Scores

| Metric | Score |
|---|---|
| **Content Quality** | **30 / 100** |
| **On-Page SEO** | **52 / 100** |
| E-E-A-T (weighted) | 27 / 100 |
| AI citation readiness | 22 / 100 |

E-E-A-T breakdown (this skill's internal weights, not Google's):

| Factor | Weight | Score | Basis |
|---|---|---|---|
| Experience | 20% | 25 | Two project tiles, both labelled `cleaning`, with no client, place, date, scope or result |
| Expertise | 25% | 20 | No team, no named managers, no certifications, no technical detail on any service page |
| Authoritativeness | 25% | 30 | 32 partner logos, every one with alt "شريك نجاح" and no name or context. No external citations |
| Trustworthiness | 30% | 30 | Phone, WhatsApp and email are shown. No address, CR, VAT number, privacy policy or terms. The email domain differs from the site domain |

How the On-Page SEO score was reached. Points were given for: a unique title and H1 on each indexable page, self-referencing canonicals, `lang="ar" dir="rtl"`, Organization and Service JSON-LD, and alt text on all images. Points were taken off for: thin pages, sitemap errors, a weak homepage title, a stock sentence repeated in every meta description, no Open Graph tags, `?service=` parameter URLs and no cross-linking between services.

## Inventory (from crawl.json)

| URL | Title chars | Desc chars | H1 | Total words | Main-content words |
|---|---|---|---|---|---|
| / | 34 | 55 | تشغيل بلا تعقيد.. وجاهزية بلا توقف | 430 | ~400 |
| ?service=maintenance | 39 | 78 | أعمال الصيانة | 106 | 43 |
| ?service=cleaning | 48 | 77 | أعمال النظافة والضيافة | 108 | 44 |
| ?service=contracting | 42 | 81 | المقاولات العامة | 106 | 43 |
| ?service=workforce | 39 | 82 | تأمين الكوادر | 102 | 39 |
| ?service=landscaping | 42 | 92 | الزراعة والتشجير | 116 | 53 |
| ?service=logistics | 43 | 98 | الخدمات اللوجستية | 112 | 49 |
| ?service=hotel-staffing | 51 | 109 | تأمين كوادر وعمالة فندقية | 132 | 67 |
| ?service=cleaning-staff | 50 | 116 | توفير عمال نظافة للمنشآت | 133 | 68 |
| ?service=hotel-operations | 46 | 102 | تشغيل وصيانة الفنادق | 130 | 66 |
| ?service=operation / hospitality / staffing | homepage copy, canonical → / | | | 430 | n/a |
| ?quote_service=* (9 URLs) | homepage copy, canonical → / | | | 430 | n/a |
| /cdn-cgi/l/email-protection | 404 (Cloudflare) | | | | |

Boilerplate share on service pages: the header, footer and chat widget make up 46-59% of each page's visible words. The fixed template labels inside `<main>` ("← العودة للرئيسية", "مزايا الخدمة", "كيف ننفذ العمل؟", "اطلب عرض سعر لهذه الخدمة") add about 12 more words. That leaves **roughly 27-56 unique words per service page**, so template text is about 55-70% of each page. All nine pages share one skeleton: an eyebrow line, the H1, one sentence, a list of 3-4 two-word "advantages" and three two-word "steps".

## Findings

### Critical

**C1. Service pages are severely thin.** The service-page floor is 800 words and these pages have 39-68 words of main content. Evidence: `?service=workforce` has one sentence, "نوفر كوادر نظامية ومؤهلة للتشغيل والضيافة والخدمات وفق متطلبات العمل.", followed by bullets "اختيار مناسب / مرونة تشغيلية / متابعة الاحتياج". `?service=contracting` lists "نطاق واضح / تنسيق فني / تنفيذ منظم". No page states scope items, facility types, cities served, SLAs, response times, staffing model, compliance (Saudization or Qiwa, safety), FAQs or a case example.
*Fix:* rebuild each page to 600-900 words with this structure: what is included (a specific task list), who it is for (government, private or commercial, with examples), where it is delivered (named cities), how the contract works (term, SLA, KPIs, reporting), compliance and licences, one real project with numbers, 4-6 service FAQs, and the CTA. All facts must come from the client. Do not pad.

**C2. No verifiable identity of the business (Trust).** No page shows a physical address, city, Commercial Registration (CR) number, VAT number, legal entity name, about page, team or year founded. Contact is limited to WhatsApp "+966549555514" and an email address. This is a B2B supplier pitching to "المنشآت الحكومية" (`/` intro section), and procurement teams check exactly these details.
*Fix:* add a footer block with legal name, CR, VAT, national address, city and a map link. Add an About page covering history, management, headcount, licences (for example any contractor or manpower classification, but only if the client holds it) and certificates. Mirror these in Organization JSON-LD (`legalName`, `address`, `taxID`/`vatID`, `foundingDate`, `sameAs`).

### High

**H1. Three sitemap URLs serve the homepage.** `?service=operation`, `?service=hospitality` and `?service=staffing` return 200 with the homepage copy (md5 d748a8ac) and canonical `https://otlobny.net/`. These slugs are in sitemap.xml. Meanwhile the live pages `?service=contracting` and `?service=workforce` are missing from the sitemap.
*Fix:* remove the three dead slugs (or 301 them to the matching live page, for example staffing → workforce) and add contracting and workforce to the sitemap. An unknown `service=` value should return 404 or 301, not the homepage.

**H2. No privacy policy, even though a form collects personal data.** `#quote-form` collects full name, phone, email and company. The chat widget accepts free text. There is no privacy notice or terms link anywhere. This is a trust gap and probably a Saudi PDPL compliance question (not legal advice).
*Fix:* publish a privacy policy and terms page, link both from the footer, and add a consent line under the form.

**H3. Experience and proof are unverifiable.** The projects section ("العمل يظهر في أدق التفاصيل") has two tiles, both labelled with the English word `cleaning` and with generic captions: "فريق نظافة محترف", "تشغيل نظافة متكامل". The partners section shows 32 logos, all with `alt="شريك نجاح"` and no names. I did not view the logo images.
*Fix:* write 3-6 case studies (client or sector, city, scope, team size, duration, outcome) and only use those the client can publish. Name the partners in alt text and captions, and confirm the client has permission to show each logo.

**H4. Overlapping service pages compete with each other.** Several pages cover the same ground. Cleaning appears on `?service=cleaning`, `?service=cleaning-staff` and `?service=hotel-operations`. Staffing appears on `?service=workforce` and `?service=hotel-staffing`. Hospitality is in the cleaning page's title and on both hotel pages. With 40-60 words each, nothing differentiates them.
*Fix:* define one primary intent per page (for example "شركة نظافة منشآت" vs "توفير عمالة نظافة" vs "تشغيل فنادق") and write content that is distinct for each. Link the related pages to each other.

### Medium

**M1. Every service description ends with the same stock sentence.** All 9 service meta descriptions finish with "حلول احترافية للمنشآت مع طلب عرض سعر مباشر.". The first sentence of each is copied from the homepage card text. The `metadata_template.py` heuristic returned `site_risk: low`, `templated_ratio: 0.0`, `shared_cta_phrases: {}`, but it did not detect this Arabic CTA. On manual comparison, a shared closing phrase on 9 of 10 pages is the exact pattern that check is meant to catch.
*Fix:* write each description by hand (110-150 characters), with the service, its audience, the city or KSA, and one differentiator.

**M2. The homepage title is weak.** "أطلبني | للصيانة والنظافة والتشغيل" is 34 characters. The part after the pipe opens with a preposition, so it reads as a fragment. It has no head term ("شركة", "تشغيل وصيانة المنشآت") and no geography ("السعودية" or a city). The description, "خدمات صيانة ونظافة وتشغيل وضيافة وكوادر متخصصة للمنشآت.", is 55 characters with no CTA or location.
*Fix:* for example "أطلبني للتشغيل والصيانة | صيانة ونظافة وتشغيل المنشآت في السعودية". Add the city once the client confirms it. Write a 130-150 character description.

**M3. Inconsistent brand descriptors and contact details.** The brand appears as "أطلبني للتشغيل والصيانة" (logo, footer, JSON-LD) and with the tagline "للصيانة والنظافة والتشغيل" (homepage title, header). The eyebrow line says "أطلبني لخدمات التشغيل والصيانة" and the footer copyright says "© 2026 أطلبني". The Latin name "Otlobny" never appears on any page. The site is otlobny.**net**, but the email in the JSON-LD and the decoded footer email are `info@otlobny.co`.
*Fix:* fix one legal or brand name and one tagline. Add `alternateName` (["اطلبني","Otlobny"]) to the JSON-LD. Use an email on the site's own domain, or explain the .co domain.

**M4. Internal linking is shallow.** Service pages link only to `/`, `/#services`, `/#projects`, `/#faq` and `/?quote_service=…#quote`. There are no links between related services, no breadcrumbs and no footer list of services. The homepage links to all 9 services from cards with the anchor text "استكشف التفاصيل ←", which describes nothing.
*Fix:* use descriptive anchors (the service name), add a "خدمات ذات صلة" block, add a footer service menu and add BreadcrumbList.

**M5. Parameter URLs instead of clean paths.** Every service lives at `/?service=slug`, and the CTA URLs `/?quote_service=slug` are crawlable and index,follow (they canonical to `/`, which avoids duplication).
*Fix (lower priority):* move to `/services/maintenance/` with 301s, and add `noindex` or `rel=nofollow` handling for `quote_service` links.

**M6. The FAQ is incomplete and unmarked.** The FAQ answer "نقدم أعمال الصيانة والنظافة والضيافة والمقاولات العامة وتأمين الكوادر." omits landscaping, logistics and the hotel services. There are only four generic questions and no FAQPage markup.
*Fix:* update the answer to list all nine services and add real buyer questions (contract minimums, cities, response time, licensing). Add FAQPage JSON-LD for machine readability; Google rich results for FAQ are restricted, so this mainly helps AI parsing.

### Low

**L1. Heading and eyebrow issues.** Each page has one H1, with H2 and H3 in order, which is good. On `?service=landscaping` and `?service=logistics` the eyebrow line repeats the H1 exactly ("الزراعة والتشجير" / "الزراعة والتشجير"). Homepage H2s are split slogans ("مرافقك تستحق فريقًا يعرف تفاصيلها.") that contain no service keywords.
*Fix:* give the eyebrows their own text and put the service term in at least one H2.

**L2. Arabic copy details.**
- The H1 "تشغيل بلا تعقيد.. وجاهزية" uses a double period; use a comma or a dash.
- The English label `cleaning` appears inside the Arabic project tiles.
- The service list on the homepage ("صيانة، نظافة، تشغيل، ضيافة وكوادر متخصصة") is used in the hero but not consistently elsewhere.

I found no spelling errors in the body copy. A native proofread is still required.

**L3. Brand spelling ("أطلبني" vs "اطلبني").** The brand is spelled «أطلبني» consistently, 8-15 times per page, with no variant found. In standard orthography the imperative takes hamzat wasl («اطلبني»), and the site itself writes the CTA verb that way: «اطلب عرض سعر». Users searching may type «اطلبني». Treat the brand spelling as a client decision; do not change it.
*Fix:* record the decision in brand-context.md and add «اطلبني» and «Otlobny» as `alternateName`.

**L4. No Open Graph or Twitter tags** on any page, so shared links have no preview. *Fix:* add og:title, og:description, og:image and og:locale=ar_SA.

### Info

- **I1.** `llms.txt` returns 404. It is optional, but a short factual llms.txt (services, regions, contact) would help AI assistants describe the company.
- **I2.** The chat widget "مرشد أطلبني" does not say whether it is automated. Disclosing this is good practice.
- **I3.** Freshness: the pages carry no dates and no blog or news. The CSS version string `202611210905` suggests the site was updated recently. "© 2026" is current.
- **I4.** `/cdn-cgi/l/email-protection` returning 404 to crawlers is normal Cloudflare behaviour and needs no action.
- **I5.** Readability: sentences are short and plain Modern Standard Arabic, so the copy is easy to read. The problem is how little it says, not how it reads.
- **I6.** AI-generated-content markers (QRG Sept 2025): the copy is generic, makes interchangeable claims ("فرق مدربة", "متابعة الجودة", "تنفيذ منظم"), uses the same structure on every page and offers no first-hand detail. It does not have to be AI-written to read as low-effort, and it currently would.

## AI citation readiness (22/100)

There are no quotable facts. The site gives no numbers, no founding year, no cities, no client counts and no certifications. The structure is clean and machine-readable: Service schema with `areaServed` set to KSA, plus Organization schema. But an AI system has nothing to cite beyond the service names and a phone number.
*Fix:* add a factual "عن أطلبني" paragraph (name, CR, city, year, services, regions). Add one stats line using verified figures only. Add service FAQs and enrich the Organization schema.

## What works

- Every indexable page has a unique title (34-51 characters) containing the service plus the brand, and the service titles are well formed.
- Every page has exactly one H1 and a clean H1 > H2 > H3 order.
- Self-referencing canonicals are present, and the parameter duplicates canonical correctly to `/`.
- The pages are declared correctly with `lang="ar" dir="rtl"`. All 36 homepage images have alt text.
- Organization and Service JSON-LD are present on every page, linked through `@id`.
- robots.txt is sensible and declares the sitemap.
- Conversion paths are clear: a CTA for each service, WhatsApp, a quote form and chat.
- Service names match how buyers search, for example "توفير عمال نظافة للمنشآت" and "تأمين كوادر وعمالة فندقية".

## Could not check

- Rankings, search volumes, Search Console or GA data, and backlinks (no access).
- Competitor pages: only otlobny.net is reachable from this network.
- Core Web Vitals and rendered layout. I did not render pages; the hero uses three autoplay MP4s with `preload="none"`.
- The content of the partner logos and project images (not viewed).
- Whether the company holds a CR or licences: these are absent from the site, not proven missing.
- Any client-side content injected by `site.js`.
- Whether there are pages not linked from the crawl or the sitemap.

## Structured findings (for audit-data.json, category "Content Quality")

```json
{"category":"Content Quality","score":30,"onpage_seo_score":52,"eeat":{"experience":25,"expertise":20,"authoritativeness":30,"trustworthiness":30,"weighted":27},"ai_citation_readiness":22,
"metadata_template":{"site_risk":"low","templated_ratio":0.0,"shared_cta_phrases":{},"manual_override":"9/10 descriptions share closing sentence 'حلول احترافية للمنشآت مع طلب عرض سعر مباشر.' not detected by heuristic"},
"findings":[
{"id":"C1","severity":"Critical","title":"Service pages 39-68 main-content words vs 800 floor","urls":["/?service=*"]},
{"id":"C2","severity":"Critical","title":"No address, CR, VAT, legal name, about/team","urls":["/"]},
{"id":"H1","severity":"High","title":"Sitemap lists 3 slugs that serve the homepage; omits contracting, workforce","urls":["/?service=operation","/?service=hospitality","/?service=staffing"]},
{"id":"H2","severity":"High","title":"No privacy policy despite personal-data form and chat"},
{"id":"H3","severity":"High","title":"Unverifiable proof: 2 generic project tiles, 32 unnamed partner logos"},
{"id":"H4","severity":"High","title":"Overlapping cleaning/staffing/hotel pages with no distinct content"},
{"id":"M1","severity":"Medium","title":"Same closing sentence on all service meta descriptions"},
{"id":"M2","severity":"Medium","title":"Homepage title fragmentary, no head term or geography"},
{"id":"M3","severity":"Medium","title":"Brand descriptor inconsistency; email on otlobny.co vs site otlobny.net"},
{"id":"M4","severity":"Medium","title":"No cross-links between services; generic anchors"},
{"id":"M5","severity":"Medium","title":"Parameter-based service URLs"},
{"id":"M6","severity":"Medium","title":"FAQ omits 4 services; no FAQPage markup"},
{"id":"L1","severity":"Low","title":"Eyebrow duplicates H1 on landscaping/logistics; slogan H2s"},
{"id":"L2","severity":"Low","title":"Double period in H1; English 'cleaning' label in Arabic UI"},
{"id":"L3","severity":"Low","title":"Brand spelling أطلبني vs standard اطلبني; add alternateName"},
{"id":"L4","severity":"Low","title":"No Open Graph tags"},
{"id":"I1","severity":"Info","title":"llms.txt 404"},
{"id":"I2","severity":"Info","title":"Chat assistant not disclosed as automated"}]}
```
