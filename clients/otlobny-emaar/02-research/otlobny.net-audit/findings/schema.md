# Structured data audit: otlobny.net

Date: 2026-11-27. Source: crawl of 23 URLs in `_work/crawl/` (raw HTML only, no rendering; external validators unavailable, so validation is manual against schema.org and Google documentation).

## Schema score: 52 / 100

| Area | Result |
|---|---|
| JSON-LD syntax | 22 of 22 blocks parse; @context is https://schema.org; absolute URLs |
| Coverage | Homepage plus 9 service pages carry schema; no BreadcrumbList, WebSite, LocalBusiness-type, or contact point |
| Accuracy | Phone and email match visible content; no invented values found |
| Hygiene | Duplicate Organization on 12 non-canonical URLs; 3 sitemap URLs without Service |

## Detection

- 23 URLs crawled; 22 returned 200 and each has exactly one JSON-LD block. No Microdata or RDFa found. `page_14` (`/cdn-cgi/l/email-protection`) is 404 with no schema (Cloudflare artefact, ignore).
- Homepage (page_01): Organization with @id `https://otlobny.net/#organization`, name, url, logo, email, telephone, description.
- 9 service pages (`?service=` cleaning, maintenance, landscaping, logistics, hotel-staffing, cleaning-staff, hotel-operations, contracting, workforce): Service with name, serviceType, description, provider (@id reference), areaServed Country, url.
- 12 URLs return the homepage Organization block (`?service=operation|hospitality|staffing` and the 9 `?quote_service=*` URLs). All canonicalise to the homepage.
- A FAQ section is visible on the homepage; there is no FAQPage markup. This is correct and no change is recommended (no Google SERP benefit since May 2026).

## Validation per block

| Block | Verdict | Notes |
|---|---|---|
| Organization (home) | Pass, thin | Valid. Missing sameAs, address, contactPoint, areaServed, identifiers. |
| Service x9 | Pass with warnings | Valid. Names, descriptions and URLs match the visible H1 and copy. Missing image and serviceOutput, plus the issues below. |
| Organization on 12 duplicate URLs | Warning | Valid but redundant, see F4. |

Value check against visible content:
- Phone +966549555514 matches the footer and WhatsApp link (`wa.me/966549555514`).
- Email info@otlobny.co: Cloudflare-obfuscated in the HTML, decoded `data-cfemail` is info@otlobny.co, so it matches the visible email. The domain differs from the site domain (.co vs .net). This is a business question, not a schema error. Confirm with the client.
- Logo https://otlobny.net/assets/images/logo.png returns 200.
- Service description wording matches page text.

## Findings

| # | Severity | Finding | Evidence | Fix |
|---|---|---|---|---|
| F1 | High | Organization is too thin and uses the generic type. A local service company has no ProfessionalService or LocalBusiness-type entity, no address, no hours, no sameAs. | page_01 block is about 406 bytes; no address, geo, openingHours, sameAs, contactPoint | Use `["Organization","ProfessionalService"]` with contactPoint now; add address, CR number, hours, geo only after the client supplies them (placeholders in template below). No social links found on the site, so sameAs stays empty until the client gives them. |
| F2 | High | Three service URLs in the sitemap have no Service schema and render the homepage. | `?service=operation`, `?service=hospitality`, `?service=staffing` in sitemap.xml; pages are md5 d748a8ac (identical to the homepage), canonical points to `/`, and H1 and title are the homepage's | Either build real pages for these services (then add Service schema) or remove the URLs from the sitemap and return 404 or 301. The homepage has no cards for these three services, so the content may not exist. Client decision. |
| F3 | Medium | No BreadcrumbList on service pages, although each has a visible "back to home" link. | No BreadcrumbList in any block | Add BreadcrumbList (Home > Service) to every service page; template below. Low rich-result value on Google today but it clarifies hierarchy. |
| F4 | Medium | Non-canonical `?quote_service=*` URLs (9) and 3 duplicate service URLs repeat the Organization block. | pages 04-06, 15-23 | Not harmful, but fix at the source: keep these URLs out of the sitemap and make sure they canonicalise to `/`, which they already do. |
| F5 | Medium | No WebSite entity. | Absent on all pages | Add WebSite with @id to the homepage graph. Do not add SearchAction, because the site has no search. |
| F6 | Medium | Service nodes re-declare provider type, name and url inline instead of a clean @id reference. | e.g. page_02 provider | Use `"provider": {"@id": "https://otlobny.net/#organization"}` only. |
| F7 | Low | Service has no `image`, `serviceOutput`, `audience`, or `url`-linked `WebPage`. B2B audience is not declared. | all Service blocks | Add `audience` (BusinessAudience) and `isPartOf`/mainEntityOfPage references. Service has no Google rich result, so this is semantic only. |
| F8 | Low | Query-string URLs are the canonical service URLs (`?service=cleaning`), so the schema `url` values inherit weak URL structure. | crawl.json canonicals | Longer term, move to clean paths such as `/services/cleaning/` with redirects; update schema urls to match. |
| F9 | Info | areaServed is the whole country. Fine if true; the client should confirm real coverage (cities). | all Service blocks | Narrow to City nodes if coverage is regional. |
| F10 | Info | FAQ section visible, no FAQPage. | homepage text | No action. |
| F11 | Info | No Review or AggregateRating anywhere, and no testimonials found. | whole crawl | Do not add ratings. Nothing visible supports them. |

Not recommended: HowTo, SpecialAnnouncement, FAQPage for SERP benefit.

## Missing facts (client must supply; never invent)

Street address and city, commercial registration (CR) number, VAT number (optional), opening hours, geo coordinates, social profile URLs, founding date, the cities served, whether the three sitemap services exist, and which email domain is canonical (.co or .net).

## Ready-to-paste JSON-LD

Replace every `TODO_` placeholder before publishing, or delete that property. A placeholder left in live markup fails the quality standard. Only facts visible on the site are used.

### 1. Homepage (`https://otlobny.net/`)

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["Organization", "ProfessionalService"],
      "@id": "https://otlobny.net/#organization",
      "name": "أطلبني للتشغيل والصيانة",
      "alternateName": "أطلبني",
      "url": "https://otlobny.net/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://otlobny.net/assets/images/logo.png"
      },
      "image": "https://otlobny.net/assets/images/logo.png",
      "description": "خدمات صيانة ونظافة وتشغيل وضيافة وكوادر متخصصة للمنشآت.",
      "email": "info@otlobny.co",
      "telephone": "+966549555514",
      "areaServed": {
        "@type": "Country",
        "name": "المملكة العربية السعودية"
      },
      "knowsLanguage": "ar",
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "sales",
        "telephone": "+966549555514",
        "email": "info@otlobny.co",
        "areaServed": "SA",
        "availableLanguage": "ar"
      },
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "TODO_CLIENT_STREET_ADDRESS",
        "addressLocality": "TODO_CLIENT_CITY",
        "addressCountry": "SA"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": "TODO_CLIENT_LATITUDE",
        "longitude": "TODO_CLIENT_LONGITUDE"
      },
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["TODO_CLIENT_DAYS"],
        "opens": "TODO_HH:MM",
        "closes": "TODO_HH:MM"
      },
      "identifier": {
        "@type": "PropertyValue",
        "name": "السجل التجاري",
        "value": "TODO_CLIENT_CR_NUMBER"
      },
      "sameAs": ["TODO_CLIENT_SOCIAL_PROFILE_URL"],
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "خدمات أطلبني",
        "itemListElement": [
          { "@type": "Offer", "itemOffered": { "@id": "https://otlobny.net/?service=maintenance#service" } },
          { "@type": "Offer", "itemOffered": { "@id": "https://otlobny.net/?service=cleaning#service" } },
          { "@type": "Offer", "itemOffered": { "@id": "https://otlobny.net/?service=contracting#service" } },
          { "@type": "Offer", "itemOffered": { "@id": "https://otlobny.net/?service=workforce#service" } },
          { "@type": "Offer", "itemOffered": { "@id": "https://otlobny.net/?service=landscaping#service" } },
          { "@type": "Offer", "itemOffered": { "@id": "https://otlobny.net/?service=logistics#service" } },
          { "@type": "Offer", "itemOffered": { "@id": "https://otlobny.net/?service=hotel-staffing#service" } },
          { "@type": "Offer", "itemOffered": { "@id": "https://otlobny.net/?service=cleaning-staff#service" } },
          { "@type": "Offer", "itemOffered": { "@id": "https://otlobny.net/?service=hotel-operations#service" } }
        ]
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://otlobny.net/#website",
      "url": "https://otlobny.net/",
      "name": "أطلبني للتشغيل والصيانة",
      "inLanguage": "ar",
      "publisher": { "@id": "https://otlobny.net/#organization" }
    },
    {
      "@type": "WebPage",
      "@id": "https://otlobny.net/#webpage",
      "url": "https://otlobny.net/",
      "name": "أطلبني | للصيانة والنظافة والتشغيل",
      "isPartOf": { "@id": "https://otlobny.net/#website" },
      "about": { "@id": "https://otlobny.net/#organization" },
      "inLanguage": "ar"
    }
  ]
}
```

Delete any TODO property (address, geo, openingHoursSpecification, identifier, sameAs) that the client cannot supply, rather than publishing placeholder text.

### 2. Service page template (example: `?service=cleaning`; repeat per page, changing the bracketed values to that page's visible H1, description and URL)

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Service",
      "@id": "https://otlobny.net/?service=cleaning#service",
      "name": "أعمال النظافة والضيافة",
      "serviceType": "أعمال النظافة والضيافة",
      "description": "نوفر بيئة نظيفة ومنظمة عبر خطط تشغيل تناسب المنشآت الحكومية والخاصة والتجارية.",
      "url": "https://otlobny.net/?service=cleaning",
      "provider": { "@id": "https://otlobny.net/#organization" },
      "areaServed": {
        "@type": "Country",
        "name": "المملكة العربية السعودية"
      },
      "audience": {
        "@type": "BusinessAudience",
        "audienceType": "المنشآت الحكومية والخاصة والتجارية"
      },
      "mainEntityOfPage": { "@id": "https://otlobny.net/?service=cleaning#webpage" }
    },
    {
      "@type": "WebPage",
      "@id": "https://otlobny.net/?service=cleaning#webpage",
      "url": "https://otlobny.net/?service=cleaning",
      "name": "أعمال النظافة والضيافة | أطلبني للتشغيل والصيانة",
      "isPartOf": { "@id": "https://otlobny.net/#website" },
      "inLanguage": "ar",
      "breadcrumb": { "@id": "https://otlobny.net/?service=cleaning#breadcrumb" }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://otlobny.net/?service=cleaning#breadcrumb",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "الرئيسية", "item": "https://otlobny.net/" },
        { "@type": "ListItem", "position": 2, "name": "أعمال النظافة والضيافة", "item": "https://otlobny.net/?service=cleaning" }
      ]
    }
  ]
}
```

Notes: the `audience` text for cleaning comes from the visible description. For other pages, use audience wording that appears on that page, or drop the property. The Organization node lives only on the homepage; service pages reference it by @id. Use of @id across pages is valid, but if you want each page self-contained, repeat the Organization node.

## Implementation order

1. Decide F2 (build or remove the three empty service URLs).
2. Replace the homepage block; add BreadcrumbList and clean provider references to the 9 service blocks.
3. Collect the missing facts from the client and fill them in.
4. Re-test in Google Rich Results Test and Schema Markup Validator (not available in this audit).

Caveat: the audit used raw HTML. The JSON-LD is present server-side. Rendered-DOM differences were not checked, and no browser sandbox was used.
