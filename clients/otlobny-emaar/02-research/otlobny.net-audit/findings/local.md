# Local SEO findings: otlobny.net (on-site signals only)
Date: 2026-11-27. Source: _work/crawl (23 files: 13 distinct service URLs, 9 quote_service duplicates, 1 email-protection 404).
Business type: service-area business (no address, no map). Vertical: commercial facilities services (B2B/B2G).

## Score: 18/100 (on-site only)
| Dimension | Weight | Score |
|---|---|---|
| GBP signals | 25 | 0/25 (no GBP/Maps link on site; GBP itself not checked) |
| Reviews and reputation | 20 | 0/20 (no testimonials, no aggregateRating) |
| Local on-page | 20 | 6/20 (service pages exist with unique titles/H1s; no city/region terms anywhere) |
| NAP and citations | 15 | 6/15 (name+phone+email consistent but incomplete; no address; citations not checked) |
| Local schema | 10 | 4/10 (Organization + Service with areaServed Country; no LocalBusiness subtype, address, geo, hours) |
| Local links/authority | 10 | 2/10 (8 partner logos only; no sameAs or external local links) |

## NAP
| Element | Finding |
|---|---|
| Name | Variants: "أطلبني" (footer/copyright, alt), "أطلبني للتشغيل والصيانة" (schema, footer, titles), "أطلبني لخدمات التشغيل والصيانة" (header). No Latin name. |
| Phone | +966549555514 in schema and as WhatsApp text/link (wa.me/966549555514). Rendered without spaces or separators. No tel: link anywhere. |
| Address | None visible, none in schema. |
| City/region | No Saudi city or region named in any page text. Only areaServed = Country (Saudi Arabia) in Service schema. |
| Email | Visible email is Cloudflare-obfuscated; decodes to info@otlobny.co. Site domain is otlobny.net: domain mismatch (.co vs .net). Verify .co is owned and monitored. |
| Hours | None. |

## Findings
1. CRITICAL: No GBP link, Maps embed or place reference. Fix: create/verify GBP (SAB: hide address, set service areas), link it in footer and add sameAs.
2. CRITICAL: No city/region targeting. No page, title, H1 or copy pairs service + city (e.g. "صيانة مرافق في الرياض"). Fix: add real city/region pages only for places actually served, with unique content.
3. HIGH: Schema is generic Organization on home; service pages use Service with areaServed Country. Fix: ProfessionalService (or HomeAndConstructionBusiness/ GeneralContractor per page as fits), areaServed as City/AdministrativeArea list, telephone, email, sameAs, hasMap; no address unless the client confirms one.
4. HIGH: No trust signals: no commercial registration (CR), VAT number, licences, certifications, years in business, client names. Key in Saudi B2B/B2G. Fix: display CR/VAT/licence numbers supplied by the client (not invented).
5. HIGH: No reviews/testimonials/case results; "projects" section has 2 generic image captions. No aggregateRating (do not add without real reviews).
6. HIGH: Phone not click-to-call (no tel:), phone only in footer; WhatsApp link is footer-only with no floating/header button. Fix: tel: and wa.me links with prefilled text in header and each service page.
7. MEDIUM: Duplicate URLs: ?service=operation/hospitality/staffing and all 9 ?quote_service= URLs return the homepage content (430 words, same title) with canonical to / (OK) yet listed in sitemap (operation/hospitality/staffing). Fix: remove from sitemap or give content.
8. MEDIUM: Service pages thin (102-133 words), query-string URLs, no unique local detail. Fix: clean paths (/services/maintenance), 400+ words with scope, sectors, cities, FAQ.
9. MEDIUM: Name inconsistency (see NAP) and email-domain mismatch.
10. LOW: No og tags, no sameAs, no social profile links; no opening hours (state 24/7 or hours if true).

## What works
HTTPS, 200s, lang=ar dir=rtl, unique titles/H1s on 10 service pages, canonical present, all images have alt, Organization schema with telephone, areaServed Saudi Arabia in service schema, WhatsApp link exists, quote form, FAQ, partner logos, robots/sitemap present.

## Not checked
GBP existence/category/reviews, Google Maps/local pack, Yelp/BBB and Saudi directories (Saudi Business Center, Daleel, etc.), review sites, backlinks, rankings, citation consistency off-site, browser render (raw HTML only), CR validity. WebFetch not attempted (network limited to otlobny.net). Proximity is outside our control.
