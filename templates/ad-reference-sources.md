# Advertising reference sources: verification of the eight sites

Date checked: 2026-11-18
Checked by: market-researcher agent, from the agency's cloud environment (Chromium through the session proxy, plus plain HTTPS requests)
Rule this supports: `.claude/rules/ad-references.md`

How to read this file:
- Everything not marked otherwise was seen on a page opened on 2026-11-18 (the page is named).
- **(not verified today)** = from prior knowledge, not from a page opened today. Treat as a lead to check, not a fact.
- **(inference)** = my reading of what I saw, not something the page states.
- "Reachable" means reachable **from this environment on this date**. A designer on an ordinary office browser may get a different result.
- Method: one or two page loads per site, no logins, no attempts to get past bot checks or paywalls.

---

## Summary table

| Site | Reachable from our environment | Free / account / paid | Searchable by sector | Searchable by country | Last activity seen | Best starting URL | Verdict |
|---|---|---|---|---|---|---|---|
| adsoftheworld.com | **Partly**: plain HTTPS requests get 200; the Chromium browser gets "403 Forbidden" | Browsing and search free; login/register only for bookmarks and "watching" (paid tiers not seen) | **Yes**: 47 industries, including Food, Hospitality/Tourism, Travel and Tourism, Professional Services, Real Estate, Industrial | **Yes**: region (Middle East) and country (Saudi Arabia, UAE, Egypt and others) | Holiday 2026 campaigns on the homepage; Clio Sports awards show "December 8th" | https://www.adsoftheworld.com/campaigns (Advanced Search) | **Best single source for us.** Filter by sector and country; Arab-region work is present |
| canneslions.com | **Yes** for the festival site. **No** for the winners archive, which is on lovethework.com and is blocked by our proxy | Festival site free. Archive access on The Work could not be checked (paid subscription, not verified today) | Not on canneslions.com | Not on canneslions.com | Festival 2027 announced (21–25 June 2027); 2026 wrap-up published | https://www.canneslions.com/awards (for categories). The archive can't be reached from here | **Low practical value from here.** Terms ban scraping and putting site content into AI/LLMs (see notes) |
| dandad.org | **Yes** (200) | A few archive items are visible without login; "Create a free account or log in to explore the full D&AD archive" | Partly: filter by **category** (discipline), not by client industry | **Yes**: Countries filter; Saudi Arabia (17), UAE (139), Lebanon (18), Egypt (14) | D&AD Awards 2026 winners in archive; D&AD Alive 2027 booking open; New Blood briefs 2027 | https://www.dandad.org/work/d-ad-awards-archive | **Good for craft** (type, copy, art direction). A free account is needed for the full archive |
| oneshow.org | **Yes** for the entry site. **No** for the winners archive, which is on oneclub.org and is blocked by our proxy | Entry site free. Archive access model not checked | Archive not reachable | Archive not reachable | 2027 entry deadlines (first deadline 11 Dec 2026); Creative Week 17–21 May 2027 | https://oneshow.org/awards/ (links out to the archive) | **Not usable from here** until www.oneclub.org is allowed |
| musebyclios.com | **Partly**: Chromium browser 200; plain HTTPS requests get 403 (Cloudflare) | Free to read; newsletter sign-up pop-up; no paywall seen | Partly: editorial categories (Travel, Advertising, Health, Experiential…), not a filterable database | Partly: "Worldviews" regional round-ups (one recent item covers UAE work) | Current holiday-season 2026 articles (McDonald's, Hertz, Amazon) | https://musebyclios.com/category/worldviews/ | **Good for what's new**, weak for sector or country search. Same owner as Ads of the World (Clio) |
| thedrum.com | **Partly**: plain HTTPS requests get 200; the Chromium screenshot rendered blank | Many articles open; **The Drum+** paid membership: "Essential" from $299 per user (billing period not shown), "Pro" for 5+ users by enquiry. Case studies and World Creative Rankings are listed as member benefits | Not seen (topic pages only) | Not seen | Same-day news (GTA VI "launches in two days") | https://www.thedrum.com/topics/ad-of-the-day | **Market context, not a work archive.** Useful to read; the deeper content is paid |
| adforum.com | **No**: Cloudflare "Sorry, you have been blocked" in browser; 403 to plain requests | Not checked | Not checked | Not checked | Not checked | n/a | **Blocked.** Can't be used from this environment |
| theinspirationroom.com | **No, and unsafe**: both hosts return a 301 redirect to **xoilaczdc.tv**, an unrelated domain (our proxy refused it) | n/a | n/a | n/a | n/a | n/a | **Remove from the list.** The domain no longer serves the ad blog |

---

## Notes per site

### 1. Ads of the World (adsoftheworld.com)

- **Reachability.** `https://adsoftheworld.com/` returns 301 to `http://www.adsoftheworld.com/` (Amazon S3/CloudFront). `https://www.adsoftheworld.com/` returns 200 to a plain HTTPS request. The same URL opened in the Chromium capture returned a bare "403 Forbidden" page. Result: our scripted browser can't use it, but the agent's HTTP fetch can (both seen today).
- **Who runs it / what it holds.** The page title reads "Ads of the World™ | Part of The Clio Network", with links to The Clio Awards and Muse by Clios. "Highlighted Campaigns: 88907 Items. Creative advertisements from around the world highlighted by the AOTW team." Each campaign links to brand and agency pages (`/brands/<slug>`, `/agencies/<slug>`). The rule's description ("archive … sorted by sector, medium and agency") is **accurate**.
- **Access model.** The homepage and Advanced Search loaded without login. The header shows Login, Register, Bookmarks, Watching and Submit. A bookmark link goes to `/users/sign_in?flash_notice=Please+login+to+bookmark+campaigns`, so an account is needed only for bookmarking. No paid plan was shown on the two pages opened. Earlier paid tiers or download limits: (not verified today).
- **Search.** The form at `/campaigns` (GET) has these fields: `search` (keyword), `medium_type_ids[]` (up to 3), `industry_ids[]` (up to 3), `region_ids[]` (up to 2), `country_ids[]` (up to 3), `collection_ids[]`. IDs read from the form today:
  - Medium: Film 1, Print 2, OOH Outdoor 4, Digital 11, 360° 12
  - Industry: Food 10, Hospitality/Tourism 13, Industrial 15, Drinks (Non Alcoholic) 20, Professional Services 25, Retail Services 29, Travel and Tourism 37, Real Estate 38
  - Region: Middle East 2
  - Country: Saudi Arabia 172, United Arab Emirates 208, Egypt 57, Kuwait 103, Qatar 160, Bahrain 15, Oman 147, Jordan 98, Lebanon 107
  - Example (built from those field names; this exact URL was **not** loaded today): `https://www.adsoftheworld.com/campaigns?country_ids[]=172&industry_ids[]=10`
  - Note: a test with `?q=saudi` was ignored and showed "Latest Campaigns". The keyword parameter is `search`, not `q`.
  - Collections include "Highlighted Ramadan Campaigns", "Cannes Lions Winners 2026", "Clio Award Winners 2026" and "Creative Typography in Advertising".
- **Arab-region work present.** The highlighted feed shows "RAHA: Brand Campaign راحة اسم على مُسمى" (agency Müller's Mena), "Lion Chips: LION: QUIT SCARING. GIVE IT A GO." (agency ABDULLAH & SHOKRI), and Switz "yala-tfannani" (agency We Are Social). I did not open these entries and have not checked their countries. Saudi Arabia and Middle East appear as filter options.
- **Activity.** Current: holiday campaigns (Waitrose, M&S, Sky, Debenhams), "Clios Sports 2026 Winners Announced", awards show "December 8th".
- **Terms.** A `/legal` page exists; it was not opened today (page-load limit). Reuse of images: (not verified today). Under our own rule, record links only and take no images.

### 2. Cannes Lions (canneslions.com)

- **Reachability.** `https://canneslions.com/` returns 301 to `https://www.canneslions.com/`, which returns 200 (title "Cannes Lions International Festival of Creativity 2027").
- **Who runs it.** The website terms of use (opened today) say: "Our site is operated by Informa Festivals … a trading division of the Informa Group", parent Informa PLC.
- **What it holds: the rule's description is only partly accurate.** canneslions.com is the festival and awards site: passes, programme, award categories and learning. The winners and the case-study explanations sit on a separate site, **The Work at lovethework.com**. The homepage's "Winners & shortlists" and "Wrap-Up 2026" links both go to lovethework.com.
- **lovethework.com is blocked** by this environment's proxy (CONNECT 403). The archive could not be opened. Its access model is a paid "The Work" subscription with a limited free layer (not verified today).
- **Activity.** "21–25 June 2027, Cannes, France". "The Official Cannes Lions Wrap-Up 2026" published. LIONS B2B summit on 22 June 2027.
- **Terms: these matter to us** (`/website-terms-of-use`, opened today):
  - Permitted use is viewing and printing one copy. There is no reproduction, no commercial use, and images or video may not be used "separately from any accompanying text".
  - No scraping or "any … automated program … to access, extract, download, scrape" the material.
  - "not upload or input any materials including any of our content … onto any kind of Artificial Intelligence (AI) source or Large Language Models (LLM)", with an indemnity.
  - Links may go to the home page only: "nor may you create a link to any part of our Site other than the home page."
  - **(inference)** An AI agent reading canneslions.com pages to summarise them for our reference files appears to fall inside the scraping and AI/LLM clauses. The two automated page loads I made today happened before I read the terms. Cannes material should be read by a person in a normal browser, and our files should only record the campaign name and a link.

### 3. D&AD (dandad.org)

- **Reachability.** `https://dandad.org/` returns 301 to `https://www.dandad.org/`, which returns 200. `https://www.dandad.org/work/d-ad-awards-archive` also returns 200.
- **What it holds.** Navigation includes Awards (D&AD Awards, New Blood, Pencils), Work (D&AD Awards archive, New Blood archive, D&AD Annual 2026), Learn (masterclasses) and Insights. The rule's description is **accurate**. Its focus is craft, design and advertising.
- **Access model.** The archive page shows a few items, then: "Create a free account or log in to explore the full D&AD archive. Sign up / Login." So a **free account** is needed for the full archive. The site also has a shop (Pencils, printed Annuals, certificates, masterclasses), which are paid products. No archive paywall was seen.
- **Search.**
  - Site search: `https://www.dandad.org/search?term=<word>`, linked from the site's own "Most searched" list.
  - The archive has a Filters panel with **Years**, **Categories** (disciplines) and **Countries**, plus sort by A–Z or Year. Filtering happens in the page (JavaScript), and I could not see a shareable URL pattern.
  - Country counts in the filter today: United Arab Emirates (139), Lebanon (18), **Saudi Arabia (17)**, Egypt (14), Kuwait (2), Jordan (1), Qatar (1); for scale, GB 9,197 and US 3,639.
  - There is no client-industry filter; discipline pages exist at `/disciplines/advertising`, `/disciplines/branding` and `/disciplines/design`.
- **Activity.** Archive items dated 2026. "D&AD Alive 2027: Booking now open". "New Blood briefs 2027".
- **Terms.** `/policies/terms-and-conditions` exists; not opened today. Reuse terms: (not verified today).

### 4. The One Show (oneshow.org)

- **Reachability.** `https://www.oneshow.org/` returns 301 to `https://oneshow.org/`, which returns 200 (title "Home / The One Show 2027"). `https://oneshow.org/awards/` also returns 200.
- **Who runs it.** The One Club for Creativity, 450 W 31st Street, New York (footer of /awards/).
- **What it holds: the rule's description is only partly accurate.** oneshow.org is the **entry site** for the 2027 awards: categories, deadlines, fees and rules. The winners archive is at `https://www.oneclub.org/awards/theoneshow/-archive/awards/<year>/…`. The "Awards Archive" menu item and every "View 2026 Winners" link point there.
- **oneclub.org is blocked** by this environment's proxy. The archive, its access model and any country or industry filters could not be checked.
- **Activity.** Entry deadlines: Advance 11 Dec 2026, Early 22 Jan 2027, Standard 12 Feb 2027, Final 5 Mar 2027. Pencil winners will be announced during Creative Week, 17–21 May 2027, and "published in the online archives".
- **Terms.** Not opened. (not verified today)

### 5. Muse by Clios (musebyclios.com)

- **Reachability.** Plain HTTPS requests get 403 (Cloudflare) on both bare and www hosts. In the Chromium browser, `https://musebyclios.com/` and `/category/worldviews/` both returned 200 and rendered.
- **What it holds.** Daily editorial on new campaigns ("Best Ads & Creative Inspiration"), with author bylines, sections (Trending, Entertainment, Lifestyle, Community Voices, The Clios) and categories (`/category/advertising/`, `/category/travel/`, `/category/ad-of-the-week/`, `/category/worldviews/`, `/category/experiential/`, `/category/health/` and others). The rule's description is **accurate**.
- **Owner.** "Muse by Clios © 2026". Clio Awards, the same network as Ads of the World. The "Worldviews" round-ups are bylined "by Ads of the World".
- **Access model.** Articles open without login. A newsletter sign-up pop-up appears. No paywall was seen.
- **Search by sector or country.** There is no filterable database. Sector browsing is by category (for example `https://musebyclios.com/category/travel/`). Region browsing is by "Worldviews" round-ups. One current item reads "… campaigns from South Africa, the UAE and Brazil". There is a site search (magnifier icon), but I did not test its URL.
- **Activity.** Current holiday-season 2026 items (McDonald's/Macaulay Culkin, Hertz, Amazon/Schwarzenegger, e.l.f.). No dates are printed on the listing cards.
- **Terms.** The footer links "Terms of Service" and "Brand Guidelines" to clios.com, which is blocked by our proxy. Not checked.

### 6. The Drum (thedrum.com)

- **Reachability.** `https://thedrum.com/` returns 301 to `http://www.thedrum.com/`. `https://www.thedrum.com/` returns 200 to a plain HTTPS request, and so does `/membership`. The Chromium capture loaded the page, but the screenshot came out blank (probably a consent or render overlay; inference).
- **What it holds.** Marketing and advertising news, opinion columns, "Ad of the Day", "Creative Work", "The Big Interview", "Awards case studies" (`/awards-case-studies`), lists ("World Creative Rankings", "World's Best Ads of All Time", "Best Out-of-Home Ads Ever") and The Drum TV. The rule's description ("news … analysis, interviews with creative directors") is **accurate**.
- **Access model.** Homepage articles are listed openly. **The Drum+** (`/membership`, opened today):
  - "Essential … From $299 /per user". The billing period is not stated on the page.
  - "Pro" for teams of 5+ is priced by enquiry. Enterprise, academic and student options are mentioned.
  - Member benefits listed: "Access all areas", case studies, World Creative Rankings, market reports, Ask The Drum.
  - **(inference)** Some articles and case studies are behind The Drum+. How many could not be checked without logging in.
- **Search by sector or country.** Not seen. Topic pages exist (`/topics/ad-of-the-day`, `/topics/creative-work`, `/b2b`, `/commerce-media`). Middle East or Saudi coverage: not seen on the homepage. A regional edition for the Middle East: (not verified today).
- **Activity.** Same-day news: "GTA VI launches in two days", Q3 holding-company analysis, holiday ads.
- **Terms.** Not opened. (not verified today)

### 7. AdForum (adforum.com)

- **Reachability: blocked.** Plain HTTPS requests get 403 from Cloudflare on both bare and www hosts. In Chromium: "Sorry, you have been blocked. You are unable to access adforum.com". I made no further attempts, per instructions.
- Its description as an agency- and brand-sorted archive with agency profiles, and its mix of free browsing and a paid professional tier: (not verified today).

### 8. The Inspiration Room (theinspirationroom.com)

- **Reachability: not usable.**
  - `https://www.theinspirationroom.com/` returns 301 to `https://theinspirationroom.com/`.
  - That returns 301 to `https://xoilaczdc.tv/`, and `/daily/` returns 301 to `https://xoilaczdc.tv/daily/`. Both redirects are served through Cloudflare.
  - Our proxy refused the target host, so I never saw the destination page.
- **(inference)** The domain no longer serves the ad blog: it has lapsed, been sold or been compromised. The name of the destination resembles football-streaming sites. It should not be opened from agency machines.
- The site's former description (a New Zealand-run blog collecting ads, with an archive by country and industry): (not verified today).

---

## How to run the reference check in 20 minutes

These steps use only the sites that worked from here today. A person on a normal office browser can also open Cannes (The Work), the One Show archive and AdForum; record which route was used.

1. **(2 min) Set the frame.** From the approved brief, write down the client's sector, the medium (social, OOH, print, film) and the market (Saudi Arabia first, then the Gulf, then the Middle East).
2. **(8 min) Ads of the World: the main source.** Open `https://www.adsoftheworld.com/campaigns` and use Advanced Search:
   - **Pass 1:** Country = Saudi Arabia, plus the closest Industry. For our current clients:
     - cafés and restaurants: Food (10) or Drinks (Non Alcoholic) (20)
     - travel agency: Travel and Tourism (37) or Hospitality, Tourism (13)
     - contracting and facilities: Professional Services (25), Industrial (15) or Real Estate (38)
   - **Pass 2:** if Pass 1 returns little, widen to Region = Middle East with the same industry.
   - **Pass 3:** the same industry with no region, to see the best worldwide.
   - Also check the "Highlighted Ramadan Campaigns" collection when the campaign touches Ramadan or Eid.
   - Note campaign name, brand, agency, year, medium and URL for each piece kept.
   - Agents: a plain fetch works here, but our Chromium capture is blocked, so agents read the HTML and do not take screenshots.
3. **(4 min) D&AD: craft benchmark.** Open `https://www.dandad.org/work/d-ad-awards-archive`, set Countries = Saudi Arabia or United Arab Emirates, and pick the Category that matches the medium (category names such as Press & Outdoor, Branding or Writing for Advertising are (not verified today); use whatever the filter lists). The full archive needs the agency's **free D&AD account**, used by a person; agents do not log in.
4. **(3 min) Muse by Clios: what is new.** Open `https://musebyclios.com/category/worldviews/` and the sector category (for example `/category/travel/`). Scan for Gulf or MENA work from the last few months.
5. **(2 min) The Drum: market context, optional.** Use `https://www.thedrum.com/topics/ad-of-the-day` for one or two recent campaigns in the sector. Note any paywall hit; do not work around it.
6. **(1 min) Record.** Write the five or more pieces, two or three observations and an "avoid" list in `clients/<client>/02-research/ad-references_<campaign>_<date>.md`, per the rule. List which sites were opened, which were not, and why. Links only; no images are taken.

---

## What could NOT be verified today

1. **Cannes Lions winners and case studies.** They live on lovethework.com, which is blocked by our proxy. The access model (free versus subscription), the filters and the presence of Saudi or MENA work are all unchecked.
2. **The One Show archive.** It lives on www.oneclub.org, which is blocked by our proxy. Access model, filters and regional work are unchecked.
3. **AdForum, entirely.** It was blocked by Cloudflare's bot protection in both the browser and plain requests.
4. **The Inspiration Room, entirely.** The domain redirects to an unrelated site; I never saw its content.
5. **Muse by Clios terms of service** (hosted on clios.com, which is blocked) and **Clio Awards pages** (clios.com is blocked).
6. **Terms and reuse rules** for Ads of the World (`/legal`), D&AD (`/policies/terms-and-conditions`), The One Show and The Drum. These pages exist, but I did not open them because of the one-or-two-page limit. Only Cannes Lions' terms were read.
7. **Ads of the World's filtered result pages.** The filter field names and IDs come from the search form, but I did not load a filtered URL (such as Saudi Arabia plus Food), so result counts per country and sector are unknown. I also did not check the country of the Arabic-titled campaigns on its homepage.
8. **D&AD filter URLs.** Filtering runs in the page's JavaScript, and no shareable URL pattern was found.
9. **Whether any of these sites block a normal office browser.** All results above are for this cloud environment only.
10. **The Drum** article-level paywall coverage, Middle East coverage and the billing period of the $299 price.
11. **Exact publication dates.** "Last activity" is taken from what the pages say (event dates, "launches in two days", seasonal campaigns), not from dated items.

---

## What this means for the agency

1. **Rely on Ads of the World first.** It is the only site that worked from here and can be filtered by both sector and country (Saudi Arabia, Middle East), and it already holds Arabic-language work.
2. **Drop The Inspiration Room from `ad-references.md` now.** Its domain redirects to an unrelated site. Remove or replace AdForum until a person confirms it opens in a normal browser.
3. **Cannes Lions content is for human reading only.** Its terms ban automated access and putting its content into AI/LLM tools. The Creative Director should decide whether agents may touch canneslions.com or lovethework.com at all. My recommendation: no, a person browses and records links only.
4. **Correct the rule's descriptions.** The Cannes and One Show archives are on other domains (lovethework.com and oneclub.org). If agents are to use them, both hosts must be allowlisted, and the Cannes terms still apply.
5. **Open a free D&AD account for the agency.** Saudi and UAE work is in the archive, but most of it is behind the free login, which a person should use.
