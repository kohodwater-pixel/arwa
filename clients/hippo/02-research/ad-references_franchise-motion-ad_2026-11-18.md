# HIPPO — advertising reference check: franchise motion-graphics ad

**Client:** hippo (HIPPO Brioche Bread / هيبو)  **Campaign:** franchise-recruitment motion-graphics ad, investor-facing
**Date of check:** 2026-11-18  **Prepared by:** market-researcher  **Rule followed:** `.claude/rules/ad-references.md`
**For:** art-director, who reads this file and draws the conclusions for the concept

> **Reference only, never a template.** Nothing below is to be copied: no layout, headline, visual device or idea. Every "transferable" line is a principle. No images from these sites have been placed in the client folder as assets. The only screenshots are internal study captures in `02-research/_work/ad-refs_2026-11-18/`, and their media frames are empty (see section 1).

---

## 1. What could and could not be checked today

| Site | Opened today? | What happened |
|---|---|---|
| adsoftheworld.com | **Yes**: search pages and 11 campaign pages (text) | Case pages (description, credits, date, country, medium) open through the session proxy. **The creative itself did not load:** the media hosts `image.adsoftheworld.com` and `video.adsoftheworld.com` were refused by the session's egress proxy (connect_rejected), and films are YouTube embeds that were not viewed. WebFetch could not resolve the domain at all; pages were read with curl and headless Chromium through the session proxy. |
| dandad.org | **Yes**: 4 archive pages (text) | Case text, category, country, year and credits are public. Images and videos need an account ("Unlock the full D&AD archive… Create a free account or log in"; films say "Log in to watch"). No login was attempted. |
| canneslions.com | **Partly**: homepage and "Winners spotlight" | Only winner titles, agency, client and year are public. The case studies are on The Work (lovethework.com), a paid subscription that was not attempted. `info.canneslions.com` (B2B Lions information) did not load. |
| oneshow.org | **Partly**: homepage and "Categories by type" | Category definitions only. The awards archive is on **oneclub.org**, which the session proxy refused (403 connect_rejected). No One Show winning work was seen. |
| musebyclios.com | **Homepage only** | Article pages returned **403 Forbidden** to both curl and headless Chromium (bot protection). Not worked around. |
| thedrum.com | **No** | Every article returned **HTTP 202 with an empty body**, a JavaScript bot challenge that also blocks a real headless browser. Not worked around. |
| adforum.com | **No** | **403, Cloudflare "Attention Required!"** bot check. Not worked around. |
| theinspirationroom.com | **No (site problem)** | `theinspirationroom.com` answers with a **301 redirect to an unrelated domain (`xoilaczdc.tv`)** on both `/` and `/daily/`. That looks like a lapsed or hijacked domain. The redirect was not followed, and the site should not be used until someone confirms it is the real blog. |

`templates/ad-reference-sources.md` (written by another agent verifying site access) **did not exist** when this check ran.

**What "seen" means in this file:** for every piece in section 2 I read the case page on the site today (title, brand, agency, country, year, medium, the entrant's description of the idea, credits). **I did not watch any film or view any key visual**, because the media hosts were blocked or behind a login. Judgements about craft (motion, type, food styling) therefore come from the written case, not from the work. Before concept work, the art-director should watch the films that matter most on a machine where `image.` and `video.adsoftheworld.com` (and YouTube) load.

---

## 2. Verified list: case pages opened today (13)

Order follows the brief: (1) franchise and B2B-facing, (2) QSR film, motion and type craft, (3) Saudi and GCC food, (4) non-food B2B selling an opportunity.

### (1) Franchise-recruitment and franchisee-facing work

**R1. Tradeshow | Franchisee Headlines (ecomaids)**
- Brand: ecomaids (Happinest Brands). Agency: HeyLet'sGo!. Country: USA. Year: April 2023. Medium: design, direct mail, social, print, trade-show materials.
- URL: https://www.adsoftheworld.com/campaigns/tradeshow-franchisee-headlines
- Idea (from case text): a copy and design system that sells franchisees on the brand's one ownable operating standard (a cleaning checklist) through headlines with titles like "Shininess", "Top Shelf", "Dust Bunnies", "Bing, Bang, Boom".
- Why it works: it recruits franchisees with personality and one proprietary standard, not a wall of financial bullet points.
- Transferable to HIPPO (principle): a franchise pitch can be sold on *one ownable product truth* (for HIPPO, the brioche) told with wit. The investor buys the system that produces the product.

**R2. RE/MAX Franchising (RE/MAX Czech Republic)**
- Agency: Peppermint Digital (Prague); production Raketa media. Country: Czechia. Year: August 2022. Medium: online film ("image online spot").
- URL: https://www.adsoftheworld.com/campaigns/re-max-franchising
- Idea (from case text): an image film promoting the benefits of becoming a successful franchisee.
- Why it works / limits: it shows that franchise recruitment is made as a brand film, not just a brochure. The short case text suggests a conventional "success-lifestyle" treatment; this could not be confirmed because the film was not viewed.
- Transferable: confirms the format (a short online film aimed at would-be owners). It is also a marker of the category default HIPPO should move away from (see section 4).

**R3. Grand openings (McDonald's Canada)**
- Agency: Cossette; production Consulat; media OMD. Country: Canada. Year: February 2024. Medium: digital, OOH, print, plus a **toolkit for franchisees**.
- URL: https://www.adsoftheworld.com/campaigns/grand-openings
- Idea (from case text): a visual system and toolkit that franchisees use to celebrate new and renovated restaurants: iconic menu items in a burst of confetti.
- Why it works: the opening of a branch becomes a brand moment, and the hero products, not people or buildings, carry the celebration.
- Transferable: "a new door opening" can be shown as a *product event* rather than with ribbon-cutting clichés. The franchisee is promised a brand that arrives with a celebration already built in.

**R4. The Burger Report (McDonald's Germany)**
- Agency: Thjnk (credits list CDs Max Biedermann and Alexander Müsgens, ECD Axel Kaeser). Country: Germany. Year: 2016. Category: Graphic Design. D&AD pencil icon on page (appears to be Wood).
- URL: https://www.dandad.org/work/d-ad-awards-archive/the-burger-report
- Idea (case text, quoted in part): the CR report for franchise partners presented through "the one thing our partners are interested in: our burgers… the foundation of each individual franchisee's income." The data was shown in bar charts that are also minimal drawings of the best-selling burgers.
- Why it works: business information for franchisees is carried *by the product's own shape*, so it is dry content made appetising.
- Transferable: the product can *be* the business graphic. For HIPPO this works only as a visual principle: the client forbids figures unless documented, so the sandwich may stand in for growth or scale **without any number attached**.

### (2) QSR film, motion and typography craft

**R5. Movement, Your Way (Burger King / Restaurant Brands International)**
- Agency: Jones Knowles Ritchie (JKR). Countries: UK and USA. Year: 2021. Category: Graphic Design (motion design elements). D&AD archive page (award level shown in page data; not visually confirmed).
- URL: https://www.dandad.org/work/d-ad-awards-archive/movement-your-way
- Idea (case text): motion elements built from hand-drawn illustration and the bespoke typeface family Flame, "spinning, stretching and layering elements" to make the motion system feel "juicy" and "drool-worthy". The page also gives the entrant's own effect figures. They are not relevant to HIPPO and are not repeated here.
- Why it works: in motion, the *type and graphics behave like the food* (squash, stretch, drip), so the brand system itself is appetising.
- Transferable: HIPPO's motion language can take its physics from brioche (soft rise, squash, spring-back, sheen) and apply it to type and the mascot. This must be invented from HIPPO's own product, not borrowed from Burger King's look.

**R6. Flame, Your Way (Burger King / RBI)**
- Agency: Jones Knowles Ritchie. Countries: UK and USA. Year: 2021. Category: Type Design & Lettering.
- URL: https://www.dandad.org/work/d-ad-awards-archive/flame-your-way
- Idea (case text): custom typefaces meant to "evoke the soft juiciness" of the menu, with ligatures and swashes that "create a mouthwatering experience before customers take their first bite."
- Why it works: craveability is expressed in the letterforms, not only in the photography.
- Transferable: cinematic typography for HIPPO should carry *texture and appetite*, but within the approved fonts (Tajawal and Playfair Display) and the hand-drawn HIPPO logo. That means motion and treatment, not a new typeface. No commissioning of a new face is implied.

**R7. The curious case of the missing mascots (Burger King South Africa)**
- Agency: Net#Work BBDO; director Sifiso "Slick" Khosa. Country: South Africa. Year: November 2025. Medium: social-first film.
- URL: https://www.adsoftheworld.com/campaigns/the-curious-case-of-the-missing-mascots
- Idea (case text): a breakfast launch told through the *mascots* of two rival rugby franchises rather than the players, bringing match-day drama into the morning.
- Why it works: a mascot treated as a character with stakes and a rivalry, rather than a logo in a suit, carries the story and makes it local.
- Transferable: HIPPO's hippo can be the protagonist with a want and an obstacle, not a sign-off decoration. (The case is about consumer breakfast, not franchising.)

**R8. We the (in)visible (McDonald's Germany)**
- Agency: Jung von Matt SPORTS (with JvM Hamburg Craft & Production); production Sterntag Film. Country: Germany. Year: December 2023. Medium: integrated (hero film, DOOH, social).
- URL: https://www.adsoftheworld.com/campaigns/we-the-in-visible
- Idea (case text): sports moments with the athlete *missing* (a ball flies by itself, a splash with no swimmer), then the reveal of the para-athletes. The case also says the brand's franchisees have long been involved locally.
- Why it works: an **absence-then-reveal device** makes the viewer lean in from the first frame because something is impossible.
- Transferable: a hook can work by showing an *effect without its cause* and paying it off with the reveal. The mechanism is the reference; HIPPO's version must be its own content.

### (3) Saudi Arabia, the GCC and the Arab region (food)

**R9. This Taste is Fire (Burger King Arabia)**
- Agency: Wunderman Thompson MENA (Dubai); production BKP Group; credits include a motion-graphics designer. Published: Saudi Arabia, June 2022 (GCC focus, mainly UAE and KSA). Medium: film.
- URL: https://www.adsoftheworld.com/campaigns/this-taste-is-fire
- Idea (case text): the sandwiches are so hot they set off a restaurant's fire sprinklers. Made "entirely without the help [of] CGI": the water flooding the floor was actually released inside a Burger King restaurant in Dubai.
- Why it works: one exaggerated, physical consequence of the product is the whole film, and it plays on a regional truth (Gulf summer heat, a food culture that won't be stopped).
- Transferable: the food can *cause something to happen in the world*. A single product-driven consequence makes a stronger hook than a list of qualities. The market fit is proven for KSA.

**R10. Taste Rules (KFC Arabia)**
- Agency: TBWA\RAAD; director Ben Whitehouse; food stylist credited. Published: Saudi Arabia, November 2025; rolled out across KSA, UAE and Qatar (360°). Medium: film.
- URL: https://www.adsoftheworld.com/campaigns/taste-rules
- Idea (case text): a "manifesto for the messy" that playfully flips Arab hospitality etiquette: double-dipping, no cutlery, big bites. "Taste wins. Manners lose."
- Why it works: it is rooted in a precise local cultural code and bends it with humour without mocking it, aimed at Gen Z.
- Transferable: Saudi audiences reward work that knows the local codes. For HIPPO's *investor* audience the relevant code is the Saudi business majlis and pride in a homegrown brand, not consumer table manners. This is an inference, to be tested in strategy.

**R11. For the love of garlic (KFC Arabia)**
- Agency: TBWA\RAAD; director Omar Nayef (The people of tomorrow); production B.K.P; Arabic copywriter credited. Published: Saudi Arabia, February 2026. Medium: digital and film.
- URL: https://www.adsoftheworld.com/campaigns/for-the-love-of-garlic
- Idea (case text): people are so taken by the product that they can only praise it in **poetry**.
- Why it works: it uses Arabic poetry as a native-language device, so the copy is written in Arabic rather than translated.
- Transferable: the voice-over and on-screen Arabic should be *written* natively (rhythm, saj', wordplay on هيبو) rather than translated from an English script. Poetry itself is now associated with KFC Arabia, so HIPPO should not use it as its device.

**R12. KFC Secret Campaign (KFC Arabia)**
- Agency: Bates Pangulf (BPG Group, WPP). Published: Egypt, Saudi Arabia, UAE, May 2024. Medium: 360°, including "Motion Graphic videos for digital screens" and "Art Direction Motion Snaps".
- URL: https://www.adsoftheworld.com/campaigns/kfc-secret-campaign
- Idea (case text): "No secrets kept, but one": the brand shows its reasons to believe (sourcing, hygiene, shelf time, "the hard way") openly, keeping only the recipe secret.
- Why it works: transparency as confidence. Opening the kitchen while keeping one thing locked builds trust *and* intrigue.
- Transferable (strong for investors): **show the system, guard the secret.** An investor-facing film can make HIPPO's operating know-how feel valuable by *revealing a lot and withholding one thing*, which only a franchise partner gets. This is scarcity without figures.

### (4) Non-food B2B that sells an opportunity with wit

**R13. The Epic Split (Volvo Trucks)**
- Agency: Forsman & Bodenfors (Gothenburg). Country: Sweden. Year: D&AD 2014, categories Film and Digital Marketing (page data lists pencil awards; the specific level was not visually confirmed).
- URL: https://www.dandad.org/work/d-ad-awards-archive/the-epic-split
- Idea (case text): Jean-Claude Van Damme does the splits between two reversing trucks to demonstrate a steering system "in a spectacular and entertaining way to reach a wide audience. Because truck buyers are surrounded by lots of influencers."
- Why it works: a B2B product benefit (precision) is proven by a single impossible-looking image, with no specification sheet. It also recognises that a B2B buyer decides among people they listen to.
- Transferable: HIPPO's investor is also surrounded by influencers (family, partners, friends who have eaten at HIPPO). The film can win the *room*, not only the spreadsheet: one striking image that demonstrates "this system is precise and consistent" with no numbers.

### Seen as titles only (not counted)
- Canneslions.com "Winners spotlight" lists **IKEA Affordable Masterpieces — Memac Ogilvy, Dubai / IKEA Alsulaiman / 2026** (Art Directors). Only the title, agency, client and year were visible; the case is behind The Work subscription. It is regional (IKEA's Saudi operator, a Dubai agency), but I cannot describe the idea because I did not see it.

---

## 3. Recalled, not opened today (kept separate; do not cite as verified)

These come from prior knowledge. They were **not opened today**, details may be imprecise, and the art-director should open them before relying on them.

- **Burger King "Moldy Whopper"** (2020; INGO Stockholm, DAVID Miami, Publicis) — food-as-hero turned upside down: a burger decaying over time to prove no artificial preservatives. Strong hook by inversion. *(recalled, not opened today)*
- **KFC UK "FCK"** (Mother London, 2018) — an apology for a supply failure, made by rearranging the logo letters. A brand character with self-awareness in a crisis. *(recalled, not opened today)*
- **McDonald's "Raise Your Arches"** (Leo Burnett London, 2022) — a raised-eyebrow gesture standing for the brand with no product shot. A distinctive asset carrying a whole film. *(recalled, not opened today)*
- **Old Spice "The Man Your Man Could Smell Like"** (Wieden+Kennedy, 2010) — a single-take, fast-transition film in which one character carries everything. A reference for rhythm and impossible transitions. *(recalled, not opened today)*
- **Mailchimp "Did You Mean Mailchimp?"** (Droga5, 2019) — B2B brand fame built on wordplay with the brand name. Relevant to playing on "هيبو / HIPPO". *(recalled, not opened today)*

---

## 4. Clichés to avoid

### Franchise advertising (the category is full of these)
1. **The handshake / signing-the-contract shot**, the keys handed over, the "be your own boss" smile.
2. **Animated counters and charts**: branch counts ticking up, rising arrows, "ROI", "payback in X months". For HIPPO these are *forbidden anyway* unless documented by the client.
3. **The map with pins spreading across the region.** It implies figures and scale that have not been documented.
4. **Stock "successful owner" lifestyle footage**: suit, luxury car, rooftop, family on a terrace (the success-lifestyle default that R2 suggests the category leans on).
5. **Corporate voice-over clichés**: "a proven business model", "a golden opportunity", "join our family of success", "فرصة ذهبية", "استثمار مضمون". "Guaranteed" is also a claim risk.
6. **The brochure-as-video**: logo, bullet list of benefits, phone number, end.

### Food advertising (QSR especially)
1. **The slow-motion ingredient drop** (lettuce, tomato and sauce falling in slow motion onto a rotating bun on black).
2. **The cheese-pull / sauce-drip close-up** as the only appetite device.
3. **The 360° turntable sandwich with a lens flare.**
4. **The "bite and moan" reaction shot.**
5. **Messy eating as rebellion.** This was KFC Arabia's territory as recently as November 2025 (R10), so it is already taken locally.
6. **Arabic poetry about the product.** Taken locally by KFC Arabia (R11).
7. **The mascot as a sign-off sticker**, appearing only in the last frame with the logo.

---

## 5. Observations that should shape the concept

These are inferences from the cases above, not facts about HIPPO. The art-director decides.

1. **The hook is an impossible or consequential image in frame one, not a logo or a question.** The strongest cases open on something that *cannot be* or that *something caused*: a ball with no player (R8), sprinklers going off because of a sandwich (R9), a man in the splits between moving trucks (R13). For HIPPO the first 3 seconds should show an effect whose cause is the brioche or the hippo, with the cause revealed after second 3. No logo, no "Are you looking for an investment?" opener.

2. **Make the food heroic through physics, not only close-ups.** The craft cases put the product's *material qualities* into the motion system itself: type and graphics that squash, stretch and drip (R5, R6), and a product that physically changes the world around it (R9). HIPPO's own physics is brioche: soft rise, pillow squash and spring-back, glazed sheen, the white sleeve. The transitions can be built from that behaviour (a bun rising becomes a hill, becomes a new storefront), so food is the engine of every cut, not a beauty shot in the middle.

3. **The hippo must be a character with a want, not a mascot in the corner.** R7 shows mascots carrying a story when they have stakes and a rival. An investor film can give the hippo a goal (to go somewhere new, to find its next home, to grow) and an obstacle. The film is then a story the viewer wants to see finished, and the CTA is the next chapter, which the investor writes.

4. **Show the system, guard one secret: scarcity and confidence without figures.** The most useful single mechanism for an investor audience is R12's "no secrets kept, but one". Reveal openly what makes the brand run (the brioche standard, the studio-set visual world, the packaging system, the kitchen rhythm) and lock one thing away that only a partner receives. Confidence comes from openness and scarcity from the withheld piece. It needs **no numbers**, so it fits the client's rule.

5. **Address the investor's circle, not just the investor.** R13's insight, that B2B buyers are surrounded by influencers, fits Saudi family and partnership investment (an assumption to confirm with the client). A film that is fun enough to be shared in a family or business WhatsApp group does more than a pitch to one person. This argues for wit and spectacle over corporate tone, while the CTA remains clearly for serious enquiries.

6. **Write it in Arabic first, on a local code, with a device nobody local owns yet.** The Gulf references (R9–R11) work because they sit on precise local truths (heat, hospitality, poetry). Messiness and poetry are already taken by KFC Arabia. HIPPO needs its own code. Candidates to test, as inference: the pride of a homegrown Saudi brand travelling outward, the word play in هيبو, or the "opening day" moment as a celebration (R3's principle, made local).

7. **Product as proof of the business (R4), with no data.** The sandwich or the sleeve can visually stand in for "growth", "reach" or "a system that repeats perfectly" (for example the identical sleeve, frame after frame, in new places) without ever showing a figure, map pin or counter.

---

## 6. Open questions for the Creative Director and client

1. **Franchise facts:** which markets are offered (KSA only, GCC, wider)? Is there any documented fact the client allows on screen (founding year, number of branches with a source)? Without them the film runs on brand and product only, which is the working assumption.
2. **CTA destination:** phone, WhatsApp, form URL, email or QR code? The brief has this as an unfilled slot.
3. **The "one secret":** if observation 4 is used, what does the client consider genuinely proprietary (recipe, dough process, supplier, training)? Can it be named on screen at all?
4. **Mascot rights and range:** is the hippo drawing cleared for animation (expressions, body, movement)? Does a character model sheet exist, or does the identity designer need to create one?
5. **Tone with investors:** how far can humour go with this audience? Is the client comfortable with the hippo being playful in a B2B film?
6. **Sister brands** (Layla, Loomi, The End): confirmed out of scope for this ad? (The brief says yes unless the client says otherwise.)
7. **Viewing the references:** may the art-director (or the user) watch R9, R10, R12, R5 and R13 on an unrestricted machine, or ask for `image.adsoftheworld.com`, `video.adsoftheworld.com` and YouTube to be allowed in this environment? Craft judgements here are based on case text only.

---

## 7. Access log

All accessed 2026-11-18.

| Source | URL | Result |
|---|---|---|
| Ads of the World search "franchise" | https://www.adsoftheworld.com/campaigns?search=franchise | 200, no relevant franchise work |
| Ads of the World search "franchisee" | https://www.adsoftheworld.com/campaigns?search=franchisee | 200, led to R1–R3 |
| R1 | https://www.adsoftheworld.com/campaigns/tradeshow-franchisee-headlines | 200, text read; images blocked |
| R2 | https://www.adsoftheworld.com/campaigns/re-max-franchising | 200, text read; film not viewed |
| R3 | https://www.adsoftheworld.com/campaigns/grand-openings | 200, text read; images blocked |
| R4 | https://www.dandad.org/work/d-ad-awards-archive/the-burger-report | 200, text read; images need login |
| R5 | https://www.dandad.org/work/d-ad-awards-archive/movement-your-way | 200, text read; video needs login |
| R6 | https://www.dandad.org/work/d-ad-awards-archive/flame-your-way | 200, text read; images need login |
| R7 | https://www.adsoftheworld.com/campaigns/the-curious-case-of-the-missing-mascots | 200, text read; film not viewed |
| R8 | https://www.adsoftheworld.com/campaigns/we-the-in-visible | 200, text read; film not viewed |
| R9 | https://www.adsoftheworld.com/campaigns/this-taste-is-fire | 200, text read; film not viewed |
| R10 | https://www.adsoftheworld.com/campaigns/taste-rules | 200, text read; film not viewed |
| R11 | https://www.adsoftheworld.com/campaigns/for-the-love-of-garlic | 200, text read; film not viewed |
| R12 | https://www.adsoftheworld.com/campaigns/kfc-secret-campaign | 200, text read; assets not viewed |
| R13 | https://www.dandad.org/work/d-ad-awards-archive/the-epic-split | 200, text read; video needs login |
| Cannes Lions winners spotlight | https://www.canneslions.com/awards/winners-spotlight | 200, titles only |
| Cannes Lions B2B info | https://info.canneslions.com/cannes-lions-awards-creative-b2b-lions-information | did not load |
| One Show categories by type | https://oneshow.org/categories/by-type/ | 200, B2B category definition only |
| One Club awards archive | https://oneclub.org/awards/theoneshow/ | refused by session proxy (403) |
| Muse by Clio homepage | https://musebyclios.com/ | 200 |
| Muse by Clio article (Bojangles) | https://musebyclios.com/advertising/bojangles-just-made-the-most-deliciously-dumb-chicken-ads-ever/ | 403 bot protection |
| The Drum articles (BK Oscars, "And a Coke", KFC Australia) | thedrum.com/news/... | 202 empty (JavaScript challenge) |
| AdForum | https://www.adforum.com/ | 403 Cloudflare bot check |
| The Inspiration Room | https://theinspirationroom.com/ | 301 to unrelated domain xoilaczdc.tv; not followed |

Internal study captures (media frames empty; not assets, not for client use): `clients/hippo/02-research/_work/ad-refs_2026-11-18/` (8 PNGs).

---

## What this means for the brand

1. **Franchise advertising is creatively thin.** Very little franchise-recruitment work appears in these archives, and what does exist leans on success-lifestyle and benefit lists. A HIPPO film made with consumer-ad craft and a real idea will stand out in the category by default.
2. **The no-figures rule is a creative advantage, not a handicap.** The strongest mechanisms found (impossible image, product as proof, show the system and guard one secret) do not need numbers.
3. **The hippo and the brioche are the two assets no competitor can borrow.** The concept should be built so that only HIPPO could have made it, with the character and the bread's physics driving every scene.
4. **Locally, avoid KFC Arabia's recent territory** (messiness, poetry). Find a Saudi code of HIPPO's own, written natively in Arabic.
5. **The art-director should watch the key films before locking the concept.** Today's check rests on case texts, not on viewing the work.
