# Website name decision — otlobny.net

**Date:** 2026-11-27  **Prepared by:** naming-specialist, for the Creative Director
**Status:** AGENCY DECISION, final for the website unless the client objects (decisions delegated by the client). Items marked PENDING need his confirmation.
**Basis:** commercial registration certificate shown 2026-11-27 (name «شركة اطلبني اعمار», single-person LLC, unified number 7029232878, Al Madinah; no Latin name); client ruling 2026-11-13 (wordmark «اطلبني», no hamza); `name-decision_2026-11-14.md`; the developer's staging `index.php`.
**Not a trademark clearance.** This is a naming and spelling decision. No trademark, domain or handle search was run for it (not verified). "Emar" still sounds like Emaar Properties; a formal SAIP search is required before any filing or signage.

## 1. Rulings

| # | Point | Ruling | Reason |
|---|---|---|---|
| 1 | Brand in running Arabic text | **«اطلبني»**, no hamza, alone. Replace every «أطلبني» on the site (templates, database settings, service texts, FAQ, chat). | It is the spelling of the logo, of the registered name and of the client's own ruling. A page that shows «اطلبني» in the logo and «أطلبني» beside it shows two spellings of one name. Search engines treat ا and أ as the same letter, so nothing is lost. |
| 1b | «اطلبني» or «اطلبني اعمار» | The brand on the site is **«اطلبني»**. «اطلبني اعمار» appears only inside the legal name. | Matches the wordmark and the domain; one short name is easier to say and search; it keeps «اعمار» out of headlines, where it invites association with Emaar Properties. |
| 2 | Legal name line | **«شركة اطلبني اعمار»**, character for character as registered: no hamza, no «المحدودة». Never restyled. | A legal name is copied, not corrected. |
| 3 | Descriptor (header and footer) | **«خدمات التشغيل والصيانة والنظافة للمنشآت»**. It replaces «أطلبني للتشغيل والصيانة», «للصيانة والنظافة والتشغيل» and the eyebrow «أطلبني لخدمات التشغيل والصيانة». | The old forms «اطلبني لل…» read as a company name, and one of them is the previous registered name. A descriptor must describe, not look like a second name. |
| 4 | Latin spelling | Brand: **OTLOBNY** (capitals, as in the 2026-11-14 decision and the domain). Full name where English needs it: **OTLOBNY Emar Company**. Not "Emaar"; not "Ltd."; not the National Address transliteration "atlubni aamar". **AGENCY DECISION PENDING CLIENT CONFIRMATION** (no registered Latin name exists). | "Emar" holds from 2026-11-14: it avoids reproducing the written mark of Emaar Properties. "Ltd." is dropped because «المحدودة» is not in the registered name. |

## 2. Exact strings for the developer

| Where | String |
|---|---|
| Site name (`site_name`, title suffix, `og:site_name`) | `اطلبني` |
| Header name | `اطلبني` |
| Header sub-line, footer descriptor, hero eyebrow | `خدمات التشغيل والصيانة والنظافة للمنشآت` |
| Homepage `<title>` (60 characters) | `اطلبني \| شركة تشغيل وصيانة ونظافة للمنشآت في المدينة المنورة` |
| Homepage meta description (142 characters) | `شركة اطلبني اعمار: خدمات التشغيل والصيانة والنظافة والضيافة وتأمين الكوادر والمقاولات للمنشآت، مقرها المدينة المنورة وتخدم جميع مناطق المملكة.` |
| Service page title pattern | `{عنوان الخدمة} \| اطلبني` |
| 404 title | `الصفحة غير موجودة \| اطلبني` |
| Chat assistant name | `مرشد اطلبني` |
| Chat greeting | `مرحبًا، أنا مرشد اطلبني. أخبرني عن منشأتك وما الخدمة التي تحتاجها.` |
| Copyright line | `© {السنة} شركة اطلبني اعمار. جميع الحقوق محفوظة.` |
| Footer legal line | `شركة اطلبني اعمار — شركة ذات مسؤولية محدودة (شركة شخص واحد)، المدينة المنورة` |
| Schema `name` | `اطلبني` |
| Schema `legalName` | `شركة اطلبني اعمار` |
| Schema `alternateName` | `["اطلبني اعمار", "أطلبني", "OTLOBNY", "OTLOBNY Emar"]` (PENDING for the two Latin values) |
| English contexts (short / full) | `OTLOBNY` / `OTLOBNY Emar Company` (PENDING) |

Notes: the `|` in titles is a plain vertical bar (the backslash above is table escaping only). `{السنة}` is the current year in Western numerals. «أطلبني» is kept only as a hidden `alternateName`, so the old spelling still resolves to the same entity. «جميع مناطق المملكة» is the client's own statement (2026-11-16). No other city, founding year, licence or certificate is to be added. Do not publish the street address until the client confirms it is current.

## 3. Service titles

| Live title | Ruling | Final title |
|---|---|---|
| أعمال النظافة والضيافة | Keep | `أعمال النظافة والضيافة` |
| أعمال الصيانة | Keep | `أعمال الصيانة` |
| الزراعة والتشجير | **Change**: «الزراعة» reads as farming; the service text itself describes tree planting and garden landscaping. | `التشجير وتنسيق الحدائق` |
| الخدمات اللوجستية | Keep | `الخدمات اللوجستية` |
| تأمين كوادر وعمالة فندقية | Keep | `تأمين كوادر وعمالة فندقية` |
| توفير عمال نظافة للمنشآت | Keep | `توفير عمال نظافة للمنشآت` |
| تشغيل وصيانة الفنادق | Keep | `تشغيل وصيانة الفنادق` |
| المقاولات العامة | **Keep the live title; reject the developer's** «المقاولات والخدمات المتخصصة». «الخدمات المتخصصة» names no service and promises a scope nobody has confirmed. | `المقاولات العامة` |
| تأمين الكوادر | **Adopt the developer's**: it says who the service is for and separates this page from the hotel staffing page. | `تأمين الكوادر للمنشآت` |

No service is added or removed. Page URLs stay as they are; only the displayed titles change. In the service texts, «أطلبني» becomes «اطلبني» and the contracting text drops the phrase «والخدمات المتخصصة».

## 4. Effect on the 2026-11-14 decision

| 2026-11-14 point | Status |
|---|---|
| Wordmark «اطلبني», no hamza | Holds; now extended to all running text on the website |
| «إعمار» with hamza | **Superseded on the website**: the registered spelling «اعمار» is used, and only inside the legal name |
| Descriptor «شركة اطلبني إعمار المحدودة» | **Superseded on the website** by «شركة اطلبني اعمار» |
| Running-text name «اطلبني إعمار» | **Superseded on the website** by «اطلبني» |
| Latin "Emar", not "Emaar"; OTLOBNY in capitals | Holds |
| "OTLOBNY EMAR COMPANY LTD." | Not used on the website ("OTLOBNY Emar Company" instead) |

Outside the website nothing changes until the client decides. Deliverables that carry the 2026-11-14 strings and would need re-issue if he chooses the registered form (none edited here):

- Logo lockup v02, four versions, in `04-identity/02-logo/`, and their copies in `06-profiles/assets/logo/`
- `04-identity/03-system/system.md` (lockup rules and strings)
- Company profile, current v20: the lockup on the cover, inside and back cover; «اطلبني إعمار» / "OTLOBNY Emar" in running text; the legal-form fact line; the fleet image with the lockup composited on vehicles
- `06-profiles/content-outline.md`
- The Canva copy of profile v03 (still reads "Emaar")
- `brand-context.md` section 1, brand name row and title

## 5. For the client to confirm

1. Latin spelling: OTLOBNY, and "OTLOBNY Emar Company" as the full English name.
2. The homepage title names «المدينة المنورة». On 2026-11-16 he asked that the profile not read as limited to Madinah; the description therefore adds «وتخدم جميع مناطق المملكة». If he prefers no city in the title, use `اطلبني | شركة تشغيل وصيانة ونظافة للمنشآت في المملكة`.
3. That «المقاولات العامة» is within the company's registered activities (not checked by the agency).
4. Whether the unified number 7029232878 is shown in the footer. It is left off until he says yes.
5. Whether the profile and the logo lockup follow the registered form «شركة اطلبني اعمار» or keep the 2026-11-14 form.
