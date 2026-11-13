# Competitor audit v02 — Sidra Coffee (سدرة للقهوة)

> **SYSTEM TEST — FICTIONAL CLIENT.** The client is invented. The three competitors below are real companies.

**Date:** 2026-11-13  **Supersedes:** `competitor-audit.md` (v01, kept unchanged)  **Scope:** 3 leading Saudi specialty roasters  **Prepared by:** Market Researcher

## Read this first: what changed and what did not

**The critical review issue is NOT resolved. No competitor's visual identity was observed in this round either.**

- On 2026-11-13 the three sites were fetched again and all failed with the same error as round 1 (`getaddrinfo ENOTFOUND`): `camelstep.com/en`, `elixirbunn.com/en`, `brew92.com/en`, and also `www.brew92.com/aboutus`. From inside this session the hosts are still not reachable, whatever the allowlist now says. A raw-HTML fetch to read CSS colours and fonts was also impossible (no shell tool was available in this round).
- **What did improve:** a web search restricted to each competitor's own domain returned summaries of their own pages. So **Messaging** rows are now based on the competitors' own published text, read as search-engine summaries, not on recall. Wording is the search tool's paraphrase unless it sits in quotation marks, and even those short quotes were not checked against the live page.
- **What is still not observable:** logo type and symbol, colours (no names, no HEX), typefaces, whether Arabic or English leads in the layout, imagery style, packaging, Instagram and any other social profile. These rows now say "not observed" instead of carrying recalled descriptions. The v01 recall has been removed from the table because it cannot be trusted for design decisions.

Labels: **[F]** fact from a third-party source · **[O]** from the competitor's own site, via search summary (not viewed directly) · **[I]** inference · **[A]** assumption. Source numbers refer to `sources.md`.

## Corrections to v01

- **Elixir Bunn founding date is disputed.** A third-party list says 2014 [F, S2]; a product page on its own site says the roastery "launched on March 31, 2018" [O, S14]. Do not state a founding year for it.
- **Brew92 founding year is now sourced:** 2016, per its own About page [O, S15]. Its site lists Jeddah, Riyadh, Dammam and Makkah, including airport branches and a drive-thru [O, S15].
- **All three sell wholesale or serve business customers** [O, S13-S15]. v01 marked this as an assumption; it is now sourced.
- **Brew92's own site is bilingual** (page titles appear in English and Arabic, with the Arabic name برو٩٢) [O, S15]. v01 called it "English-led"; that remains true of the name only. Which language leads the layout is not observed.

---

## 1. Camel Step — خطوة جمل (Riyadh)

| | |
|---|---|
| What they are | Saudi specialty coffee company, operating since 2013 [O, S13; F, S2]. Sells freshly roasted beans, brewing equipment and accessories online, runs cafés across Saudi Arabia, sells ready-to-drink cold brew in 250 ml cans, and runs a blog and training for coffee professionals [O, S13] |
| Positioning | The pioneer that raised the standard: its About page says it has worked since 2013 to raise the quality of the country's specialty coffee sector [O, S13, paraphrase]. A Riyadh guide calls it "a pioneer of Saudi specialty coffee" [F, S3] |
| Messaging | Sector leadership and knowledge. One blog title reads "Knowledge That Starts with the Team Reaches the Cup" [O, S13]. Product pages lead with origin, process and tasting notes (example: an anaerobic Rwanda with strawberry, guava, fig and hazelnut notes) [O, S13]. **Tagline: not found; none quoted** |
| Visual identity | **Not observed.** Logo, colours, typefaces, Arabic / English lead, imagery: unknown. The only safe statement is that the name refers to the camel [I from the name]. Product URLs on the site use Arabic slugs, which suggests Arabic-first content management [I, weak] |
| Strengths | Longest track record; widest range (beans, equipment, RTD, training); a culturally legible name [I] |
| Gaps | Breadth makes it a general coffee retailer as much as a roaster; a small café is one account among many [I]. It runs its own cafés, so it competes with wholesale customers [O for cafés, S13; I for the conflict] |

## 2. Elixir Bunn — إكسير البن (Riyadh)

| | |
|---|---|
| What they are | Specialty roaster headquartered in Al Nakheel, Riyadh [O, S14]. Founding date disputed (see corrections). Offers regional wholesale coffee supply, coffee equipment, consulting and training [O, S14] |
| Positioning | The blender and curator of origins. Its About text says the story "began with the search for the best way to compose distinct flavors" from Latin American, African and other origins [O, S14, short quote unverified against the live page] |
| Messaging | Roasting as art: a page is titled «التحميص: الفن الذي يصوغ هوية القهوة» ("Roasting: the art that shapes coffee's identity", researcher's translation) [O, S14]. Origin stories with a human angle: a Congo Kivu coffee presented as grown by more than 3,200 smallholder farmers [O, S14]. A flagship seasonal blend named "3x33" (three origins at 33% each) [O, S14]. A move from cafés towards a co-working style space called "Here" for creatives, entrepreneurs and students [O, S14]. **Tagline: not found; none quoted** |
| Visual identity | **Not observed.** Logo, colours, typefaces, imagery: unknown. Language: the search tool reports that most of the site's content is in Arabic, including Arabic page titles on English-locale URLs [O, S14]; so its web content is Arabic-heavy, which **contradicts the v01 assumption** that it reads as Latin-led |
| Strengths | Rich Arabic editorial content; a clear craft story; wholesale, consulting and training already packaged for business buyers [O, S14; I] |
| Gaps | Attention is moving to lifestyle spaces and co-working, away from the core roaster-supplier role [I from S14]. Runs its own cafés [F, S3]. Poetic, craft-led register rather than operational specifics such as roast and delivery days [I] |

## 3. Brew92 — برو٩٢ (Jeddah)

| | |
|---|---|
| What they are | Describes itself as a Saudi-based specialty café and roastery, founded in 2016 by coffee experts, roasters and baristas [O, S15]. Branches in Jeddah, Riyadh, Dammam and Makkah, several open 24 hours at airports, plus a drive-thru [O, S15]. Supplies business partners and offers consultancy and training [O, S15] |
| Positioning | The credentialed professional. Stated mission: to be a leading coffee brand that also advances the knowledge of the coffee community [O, S15, paraphrase] |
| Messaging | Proof by certification and grading: team trained to SCA standards, a Q-grader evaluates green samples, "100% specialty grade Arabica", some lots bought through Cup of Excellence auctions [O, S15]. **Tagline: not found; none quoted** |
| Visual identity | **Not observed.** Logo, colours, typefaces, imagery: unknown. Language: page titles carry both English and Arabic and the Arabic name is written برو٩٢ with Arabic-Indic numerals [O, S15]. Which language leads on the page is not observed |
| Strengths | Hard credentials (SCA, Q-grader, CoE); the widest geographic footprint of the three, including airports; consistency reputation in Riyadh [O, S15; F, S3] |
| Gaps | "Café and roastery" in its own words: café first, and a high-footfall chain at that [O, S15]. Not Riyadh-native. Credential language is technical and impersonal [I] |

---

## Does anything resemble Sidra's direction?

**This cannot be answered from evidence.** No logo, colour, device or wordmark of any competitor was seen. Per element:

| Sidra direction element | Camel Step | Elixir Bunn | Brew92 |
|---|---|---|---|
| Red / orange-red brand colour | Not observed | Not observed | Not observed |
| Bar or stripe devices | Not observed | Not observed | Not observed |
| Heavy Arabic wordmark on cream | Not observed | Not observed | Not observed |

- Nothing in the text sources mentions a colour, a stripe device or a wordmark style for any of the three, so there is **no evidence of a clash and no evidence of clearance**.
- The researcher declines to fill these cells from memory. Recall of these brands' colours is not reliable enough to clear or block a direction, and v01 already showed one recalled point (Elixir Bunn as Latin-led) to be doubtful.
- **This check must be done by eye before the identity is approved.** Ten minutes with a browser: the three homepages, one bag photo each, and the three Instagram grids. Until then, treat "red / orange-red is free in the category" as an **untested assumption**.
- Also outside this audit: the other Saudi roasters named in v01 (Black Knight, Arriyadh Roastery, Sout, Bunista, The Roasting House) were not checked for any of the three elements.

## Category conventions (revised)

- **Roaster, café chain and wholesaler in one.** All three run cafés and all three supply or serve business customers [O, S13-S15]. Now sourced, not assumed.
- **Training and consultancy are standard add-ons.** All three offer training; two also offer consulting [O, S13-S15]. Sidra's low-priority barista training is table stakes, not a differentiator [I].
- **Proof by origin, process, grading and competitions** [O, S13-S15; F, S4].
- **Arabic content is stronger than v01 assumed.** Elixir Bunn's site is mostly Arabic and Brew92 is bilingual [O, S14, S15]. Arabic-first web content alone will not set Sidra apart; an Arabic-led *identity* might, but that depends on the unobserved logos.
- **Visual conventions (minimal, black / kraft / cream): still an assumption** [A]. Not observed.

## White space (revised)

1. **Roaster only: the café's partner, not its rival.** Strengthened. All three competitors operate their own cafés, including a 24-hour airport chain and a co-working concept [O]. A roaster with no cafés of its own remains an open position, if the client confirms it.
2. **Operational reliability as the headline.** Strengthened. Competitors lead with pioneering, art and credentials [O]; none of the summaries shows roast day, delivery schedule or roast-to-order as the main promise [I, from absence in summaries, so weak].
3. **Plain, peer-to-peer Arabic.** Competitor registers are institutional (Camel Step), poetic (Elixir Bunn) and technical (Brew92) [I from O]. A direct, practical Arabic voice is open.
4. **Arabic-first identity: downgraded from "clear difference" to "to be verified".** It still fits the brief, but it can no longer be claimed as white space without seeing the competitors' logos.
5. **Sidr tree as symbol, warm non-green palette: unchanged, still an assumption** [A].

## What this means for the brand

1. **Build the positioning on structure and service, which are evidenced, not on looks, which are not.** "Roaster only, roasted to order weekly, for independent cafés" is supported by what the competitors say about themselves.
2. **Do not claim Arabic-first as the differentiator in the strategy text.** Keep it as a brand requirement from the brief. The competitors publish plenty of Arabic.
3. **Do not compete on credentials.** The client has no awards or certifications to publish, and Brew92 owns that ground. Lead with the one verified proof point: weekly roast to order.
4. **Hold the identity approval until the visual check is done.** The red / orange-red, bar device and heavy Arabic wordmark direction has not been tested against a single competitor.
5. **Treat training as a supporting service only**; every competitor has it.
