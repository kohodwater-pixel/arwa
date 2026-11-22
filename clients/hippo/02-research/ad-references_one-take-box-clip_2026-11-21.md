# HIPPO — advertising reference check: one-take "box drops" clip

**Client:** hippo (HIPPO Brioche Bread / هيبو)  **Piece:** 15–18 s vertical, candid-phone-style, one continuous take; a HIPPO box lands in a Saudi car park, a hand opens it, the franchise invitation and QR codes are inside
**Date of check:** 2026-11-21  **Prepared by:** market-researcher  **Rule followed:** `.claude/rules/ad-references.md`
**For:** art-director (reads this and draws the conclusions for the concept)
**Builds on:** `ad-references_franchise-motion-ad_2026-11-18.md` (cases R1–R13 there are not repeated; R8 and R9 are cited where they bear on this clip)

> **Reference only, never a template.** Nothing below is to be copied: no layout, line, visual device or idea. Every "applies to HIPPO" line is a principle. No images were taken from any site and no screenshots were made today.

---

## 0. Read this first: what today's check can and cannot support

1. **The check is weakest exactly where the piece needs it most.** The brief asked for FOOH / CGI-in-real-footage stunts. **I could not open a single FOOH film or FOOH case page today.** Ads of the World now puts a CAPTCHA in front of every page, and the specialist FOOH library (fooh.com) is outside the session's allowed network. Group (a) below is therefore covered only by neighbouring work (staged "normal" videos that turn, a staged real-world stunt, a CCTV-footage format), not by FOOH proper.
2. **No film was watched.** Every piece below was read as a D&AD case page: title, entrant's description, category, country, year, public credits. Every film on those pages says "Log in to watch". Judgements about craft are from the written case, not from the work.
3. **The disclosure question (did brands label CGI stunts?) is NOT answered from sources opened today.** What I have is: the in-piece pattern of the cases I did read (section 4, observation 3), two web-search result summaries that I could not open, and prior knowledge. All are labelled.
4. **The time box was exceeded.** About 20 page loads were allowed; roughly 36 loaded successfully and about 20 more were refused (section 6). The overrun came from the main source being blocked and D&AD's search matching titles only.

Labels used: **(case text)** = read on the page today. **(inference)** = my reading. **(not verified today)** = prior knowledge, not opened today. **(search snippet, not opened)** = seen only as a search-result title or summary.

---

## 1. Sites: opened, not opened, why

| Site | Today | What happened |
|---|---|---|
| adsoftheworld.com | **Blocked** | 10 requests, none served. A browser-like client gets "403 Forbidden"; a plain HTTPS request gets HTTP 405 "Human Verification", an AWS WAF CAPTCHA page ("verify that you're not a robot by solving a CAPTCHA puzzle"). This is new since 2026-11-18, when plain requests returned 200. Not worked around. `templates/ad-reference-sources.md` is now out of date on this point. |
| dandad.org | **Opened** | 17 search pages and 15 archive case pages (HTTP 200). Search matches **titles only**: "found footage", "fake out of home", "hoax", "dashcam", "delivery box" returned nothing. Case text is public; films and most images need a login (not attempted). |
| thedrum.com | **Partly** | "Ad of the Day" topic page loaded (200) but was not mined. Site search returned an empty shell (results load by script). One opinion article on faux out-of-home loaded with its headline and standfirst only, then a registration wall. One insight article returned HTTP 202 with an empty body. Not worked around. |
| musebyclios.com | **Not attempted** | Needs the Chromium route and on 2026-11-18 article pages returned 403. The page budget was already spent. |
| canneslions.com | **Not opened** | Rule: agents do not fetch (terms forbid automated access and AI use). |
| oneshow.org | **Not opened** | Rule: archive is on oneclub.org, not reachable; agents do not fetch. |
| adforum.com | **Not opened** | Rule: blocks automated access. |
| theinspirationroom.com | **Not opened** | Rule: DO NOT OPEN (domain redirects elsewhere). |

**Outside the eight sites** (tried because the eight gave no FOOH work):

| Host | Today | What happened |
|---|---|---|
| fooh.com (a FOOH library that lists Saudi entries) | **Blocked** | No connection through the session proxy (4 requests); WebFetch: host not resolvable (3 requests). **Needs to be allowed in the session's network settings.** |
| marketingbrew.com, adnews.com.au, campaignasia.com (articles on FOOH and disclosure) | **Blocked** | WebFetch: host not resolvable, one attempt each. Would need allowing. |
| Web search | **Used twice** | For leads only. Nothing from a search result is counted as a piece. |

---

## 2. Verified list: 9 case pages opened today (case text read; no film viewed)

Grouped as the brief asked. All URLs are D&AD Awards archive pages, accessed 2026-11-21.

### (a) Fake candid / staged "real" footage / stunt in the real world

**P1. Unboxing (Netflix with PlayStation)**
- Brand: Netflix. Agency: FCB&FiRe Spain (named in the case text). Country: Spain. Year: 2021. Categories: Media, PR, Digital Marketing. Medium: live Twitch stream.
- URL: https://www.dandad.org/work/d-ad-awards-archive/unboxing-2
- Idea (case text): a top streamer's first unboxing of the new PS5 is "hacked"; "what appeared to be a normal streaming became the first live horror film", directed live by a horror filmmaker.
- Why it works (inference): it borrows a format the audience watches every day, plays it completely straight, then breaks it once. The audience's trust in the format is the set-up.
- Applies to HIPPO: the candid car-park clip must first *be* a believable nothing-clip, in the exact grammar of that genre, so that the one impossible event lands. Also: the fiction is resolved inside the piece itself. Nobody leaves still believing it was an ordinary stream.

**P2. Unboxing (States United to Prevent Gun Violence)**
- Brand: SUPGV. Agency: Grey New York; production Chelsea Pictures; Townhouse (credits). Country: USA. Year: 2022. Category: Film.
- URL: https://www.dandad.org/work/d-ad-awards-archive/unboxing
- Idea (case text): a film that "opens like any other popular toy unboxing video" with a "fictional eight-year-old influencer", who then unboxes the pistol his parents keep hidden.
- Why it works (inference): the first seconds are indistinguishable from the genre; the content of the box overturns everything the viewer assumed.
- Applies to HIPPO: principle only (the subject matter is unrelated and far darker). What is *in the box* is where the meaning sits; the box is only a promise. Note that the entrant itself calls the character "fictional": the piece is a film, not a hoax.

**P3. Go With The Fake (Diesel)**
- Brand: Diesel. Agency: not shown on the public page; Publicis (not verified today). Entry country: United Kingdom. Year: 2018. Category: Experiential: Activation & Participation.
- URL: https://www.dandad.org/work/d-ad-awards-archive/go-with-the-fake
- Idea (case text): Diesel "secretly opened a real knock-off store called Deisel" on New York's Canal Street, the city's best-known fake-fashion street.
- Why it works (inference): the "fake" is physically real, so there is nothing for the viewer to debunk; the brand is in on the joke and the people fooled come out ahead.
- Applies to HIPPO: the most believable fake-candid is the one that actually happened. A real box, really dropped (safely, from just out of frame), really opened in one take, removes the "is this CGI/AI?" argument in the comments. This bears directly on the open production-route decision (real phone shoot vs AI-generated test).

**P4. Starr Park CCTV (Brawl Stars)**
- Brand: Brawl Stars / Supercell. Agencies: Supercell; design Buck Los Angeles; production Wild, Twisted Mountain Animation, Antfood. Countries: Austria, Canada, Finland, USA. Year: 2024. Category: Gaming & Virtual Worlds.
- URL: https://www.dandad.org/work/d-ad-awards-archive/starr-park-cctv
- Idea (case text): a "CCTV Security Room simulation" of a fictional park in 1995, with "live footage from 54 cameras", through which players dig out the game's backstory.
- Why it works (inference; the page also carries a jury comment about fan-built lore): the surveillance-footage look gives invented content the texture of evidence, and invites people to look closely and talk.
- Applies to HIPPO: limited. It confirms that "low-grade camera" aesthetics are a deliberate format with their own rules (fixed framing, bad audio, timestamps). It is a game world, not a fake of the real world.

### (b) Unboxing as the reveal / the message is inside or on the package

**P5. Blurred Unboxing (Ramo)**
- Brand: Ramo. Agency: The Juju; production Los Notarios, Machina Audio Solutions. Country: Colombia. Year: 2025. Categories: Creator Content, Digital Marketing.
- URL: https://www.dandad.org/work/d-ad-awards-archive/blurred-unboxing
- Idea (case text): a big TikToker blurred the logo on "Ramo's signature box" to avoid giving free exposure; his followers recognised the box anyway. Within 24 hours the brand sent him a new box in which everything, even a jersey, carried a blurred logo, and got a second unboxing for free.
- Why it works (inference): the box is recognisable without its logo, and the inside of the box *continues the joke* set up outside.
- Applies to HIPPO: two tests. (1) Would the falling box read as HIPPO from its colours alone (lime, black, pink) in a blurred, moving, half-second glimpse? If not, the thud lands for nobody in particular. (2) The card inside should finish the sentence the outside started ("ما ينزل خفيف"), not change the subject.

**P6. Unboxing the Truth (Thomson Reuters Foundation)**
- Brand: Thomson Reuters Foundation. Agency: not shown on the public page. Country: USA. Year: 2019. Category: Digital Marketing.
- URL: https://www.dandad.org/work/d-ad-awards-archive/unboxing-the-truth
- Idea (case text): purpose-made shoes, make-up and headphones "with hidden facts symbolic of the hidden issue" (forced labour), sent to influencers to unbox on camera. The page gives the entrant's own result figures; they are not relevant to HIPPO and are not repeated.
- Why it works (inference): the message is physically hidden inside the object, so finding it is an event the viewer witnesses, not a caption they are shown.
- Applies to HIPPO: the franchise card should be *found* by the hand in the take (lifted, turned to camera), not appear as a graphic laid over the footage. An overlay would break the one-take, candid contract at the exact moment of payoff.

**P7. Pizza Box (7 West Restaurant)**
- Brand: 7 West (a 24-hour Toronto restaurant). Agency: Leo Burnett Canada (case text). Country: Canada. Year: 2020. Category: Packaging Design.
- URL: https://www.dandad.org/work/d-ad-awards-archive/pizza-box
- Idea (case text): twelve pizza boxes, each matched to a delivery hour, carrying a reason why the opposite hour is also pizza time. The page gives an entrant's result figure; not repeated here.
- Why it works (inference): a food box is media the customer already holds; one short line per box, tied to the moment it is opened.
- Applies to HIPPO: the lid and the card are the only "screens" in this clip. One line each, written for the half-second in which the lid lifts. Food sector, but consumer-facing; no franchise angle.

### (c) One take

**P8. Shot on iPhone 11 Pro – Hermitage (Apple)**
- Brand: Apple. Agency: not shown on the public page. Entry country: United Kingdom. Year: 2020. Category: Entertainment.
- URL: https://www.dandad.org/work/d-ad-awards-archive/shot-on-iphone-11-pro-hermitage
- Idea (case text): "A 5 hr 19 min 28 sec cinematic journey" through the Hermitage museum, "shot in 4K on iPhone 11 Pro in one continuous take."
- Why it works (inference): the unbroken take *is* the claim; a single cut would have cancelled it.
- Applies to HIPPO: the continuous take is the proof that the drop "happened". If the production needs a hidden cut (for example between the landing and the hand), viewers who look for it will find it, and the format's whole value is gone. It is the opposite end of the scale (five hours, polished) and has no physical surprise; I found no one-take film *with* a physical surprise that I could open today.

### (d) Saudi Arabia / the Gulf

**P9. LEGO News Rebuilt (LEGO Saudi Stores)**
- Brand: LEGO Saudi Stores. Agency: not shown on the public page. Entry country: United Arab Emirates. Year: 2021. Category: Media. Market: Saudi Arabia.
- URL: https://www.dandad.org/work/d-ad-awards-archive/lego-news-rebuilt
- Idea (case text): on Saudi National Day 2020 a team rebuilt a major newspaper's National Day edition entirely in LEGO (photographs, articles, even the ads) and printed it; it "hit newsstands across Saudi Arabia".
- Why it works (inference): an ordinary Saudi object turns out to be something else when you look closely; a physical surprise tied to a moment of national pride rather than to a prank.
- Applies to HIPPO: weak fit to the format, but it is the only Saudi-market case I could read today in this vein. The transferable part is tone: surprise in the Kingdom's mainstream work is generous and proud, not at someone's expense.

**Carried forward from the 2026-11-18 file (not re-opened today):** R9 "This Taste is Fire" (Burger King Arabia, published Saudi Arabia 2022: the product physically sets off a restaurant's sprinklers, made without CGI) and R8 "We the (in)visible" (effect shown before its cause). Both are closer to this clip than anything Saudi I could open today: a physical consequence caused by the product, done for real.

### Opened today but not counted

| Page | Why not counted |
|---|---|
| Unbox the Banner (IKEA, Germany, 2011, Direct) — https://www.dandad.org/work/d-ad-awards-archive/unbox-the-banner | Read; assemble-it-yourself web banners. Too far from this piece. |
| Hot & Spicy (Season 2) (KFC, Hong Kong/Thailand, 2020, Press & Outdoor) — https://www.dandad.org/work/d-ad-awards-archive/hot-spicy-season-2 | Read; fried chicken replaces explosions in stills. Print, not footage. |
| Akhou Nora (Saudi Telecom Company, J. Walter Thompson, Saudi Arabia, 2019) — https://www.dandad.org/work/d-ad-awards-archive/akhou-nora | Public page shows title and credits only, no description. I cannot say what the idea is. |
| Aero Delivery Man (Nestlé Rowntree, UK, 2002, Film) | Title and client only, no description. |
| Fake Views (Operation Black Vote, UK, 2020); Stadium's Food Delivery (Brahma, Brazil, 2021) | Read; not relevant. |
| The Drum, "Why the fake outrage about 'faux' out-of-home ads?" (Kirsty Hathaway, ECD at Joan London, 7 Dec 2023) — https://www.thedrum.com/opinion/why-the-fake-outrage-about-faux-out-home-ads | Headline and standfirst only: she "vigorously defends fake or CGI out-of-home ads. Does it matter if they're real if they make you feel?" The argument itself is behind registration. Evidence only that the question was a live trade debate in 2023. |

---

## 3. Leads NOT opened today (do not cite as verified)

**Saudi FOOH entries, seen only as search-result titles on fooh.com (blocked):**
- Philips: a large pink gift box lowered by helicopter near Kingdom Centre, Riyadh. *(search snippet, not opened)* **Closest known neighbour to our idea: a box coming down from the sky in Riyadh.** Someone must look at it before the concept is locked, to make sure HIPPO's clip does not resemble it.
- Noon: a delivery pod on the edge of a cliff. *(search snippet, not opened)*
- Adidas: a giant Saudi jersey hanging from the Kingdom Centre sky bridge; Garnier: giant products hanging from cranes at U Walk; PlayStation: a giant PS5 in Riyadh; McVitie's: giant biscuits loaded onto a truck; CeraVe: a giant jar in a Saudi plaza. *(search snippets, not opened)*
- Reading across those titles *(inference from titles only)*: the Saudi FOOH default is a **giant product on a Riyadh landmark**. An ordinary car park and a normal-sized box is a different register, which is to HIPPO's advantage.

**From prior knowledge (not verified today):**
- Maybelline "Sky High" mascara: lashes on a London Underground train and bus brushed by a giant wand; by the CGI artist Ian Padgham (Origiful), 2023, who is credited with the term "FOOH". Widely taken for real at first; trade coverage then discussed whether such films should say they are CGI.
- Jacquemus: giant "Bambino" handbags driving through Paris streets, 2023.
- The North Face / JD Sports: a giant puffer jacket on Big Ben.
- Old Spice "The Man Your Man Could Smell Like" (already listed as recalled in the 18 Nov file): the reference for a one-take with physical gags.

**From the previous check's working cache (fetched 2026-11-18, not re-opened today):** "Mana Macaron: When Imagination Meets Taste", a CGI trilogy by Lamana Agency on Ads of the World. Country and year not checked. A lead only.

---

## 4. Three observations that should shape THIS clip

All three are inferences from case texts, not from films watched. The art-director decides.

### 1. Hook: half a second of nothing, then the thud. The impact is the hook; the logo is not.
- P1 and P2 both "open like any other" clip of their genre, and the break is the event. At 15–18 s there is no room for a long set-up: the "ordinary" needs to be just long enough to register as ordinary (about a second), and the box must land inside the first second and a half. This agrees with the sound ruling already recorded for this client (hit at 1.000 s).
- The consequence sells the weight more than the box does: car bodies dipping, an alarm chirp, the phone jolting. This is R9's principle (the product causes something physical) and R8's (effect before cause): the viewer should feel the hit before they can read whose box it is.
- Per P5, the box must be identifiable as HIPPO by colour in a blurred glimpse. If it needs a readable logo to be recognised, the first three seconds work for nobody.

### 2. Believable vs cringe: play the genre straight, break exactly one rule, and prefer doing it for real.
- Believable (P1, P2, P3, P8): real phone grammar (imperfect framing, late reaction, clipped audio, no music until after the hit), one continuous take with no hidden cut, a real object with real weight, and only **one** impossible thing.
- Cringe *(inference)*: the box landing perfectly logo-up and centred; a filmer who over-acts or narrates; a hand already waiting; clean, mixed sound from frame one; the brand line arriving before the viewer has worked out what happened; stacking effects (every alarm, dust, slow motion). Each extra flourish tells the viewer it is an advert before the reveal can do so itself.
- P3 points to the production choice: a real, safely staged drop gives nothing to debunk. An AI-generated version invites "this is AI" as the top comment and brings a labelling duty with it (observation 3).

### 3. Pay-off and honesty: the card must finish the line, be found in-shot, and the clip must never ask to be believed.
- Pay-off (P5, P6, P7): the inside completes what the outside started. The heavy landing sets up a question (what is so heavy?); the card answers it (the invitation to carry the brand). The card is lifted and turned to camera by the hand, with one short line and the QR, then held still long enough to scan (the client record already has "QR static for at least 3 s").
- Disclosure, what I can and cannot say:
  - **Not verified today:** whether brands labelled their CGI stunts. From prior knowledge *(not verified today)*, the best-known FOOH films were first posted without any "CGI" label and were explained afterwards by the makers or the trade press. Web-search summaries *(not opened)* say there is no industry-wide disclosure standard for FOOH and quote an out-of-home company executive calling for one.
  - **Seen today in the case texts:** in P1, P2 and P3 the fiction is resolved *inside the piece* (the stream turns into a film; the character is described as fictional; the secret store is revealed). None of them leaves the viewer deceived at the end. *(inference)*
  - **For HIPPO:** the spoken line "هيبو إذا نزل، ما ينزل خفيف" is itself the wink that makes the clip read as a joke rather than as a claimed event. Keep it that way: no caption or post copy that presents it as something that really happened, no seeded "is this real?" accounts.
  - **To check before release (not verified today):** the platforms' rules on labelling AI-generated or realistically altered video (TikTok, Instagram/Meta, Snapchat, YouTube are each understood to have one), and Saudi advertising and media rules on misleading content. If any part of the clip is AI-generated or composited, assume it must carry the platform's label and plan the caption for it. The legal check is the client's.

---

## 5. Avoid

**Overused FOOH tropes** *(from search-result titles and prior knowledge; not verified by viewing)*
1. A giant product on a landmark (Kingdom Centre, Boulevard, U Walk). It is the Saudi FOOH default, and one lead is literally a box lowered from the sky in Riyadh.
2. The helicopter, crane or parachute delivery.
3. The "people filming from a car window, gasping" framing, and fake bystander reactions cut in.
4. A too-perfect CGI object with studio lighting in a phone shot.
5. Slow motion at the impact. It turns a candid clip into an advert at once.

**Reads as dangerous**
6. The box landing on, or within reach of, a person, a child, or an occupied or moving car. Keep the frame visibly empty of people at the moment of impact.
7. Anything that looks like load falling from a moving lorry on a road. That is the reference clip's mechanism and it shows a real road hazard; the car park and "from above" already move away from it. Do not drift back.
8. A drop that looks thrown from a building or bridge by a person, which invites imitation. The source of the fall should stay unexplained and impossible, not copyable.
9. Visible damage to cars (dents, broken glass). A shake and an alarm chirp are a joke; damage is a complaint.
10. On a real shoot: other people's number plates and bystanders' faces in frame. Use the production's own cars and people. Saudi rules on filming people in public: (not verified today), to be checked by the producer.

**Reads as deceiving the viewer**
11. Posting it as a real incident ("شوفوا وش صار اليوم"), or from an account that hides it is HIPPO's.
12. A hidden cut presented as one take.
13. A graphic overlay or AI-rendered card in place of a real card in the hand.
14. Unlabelled AI footage where the platform requires a label.
15. Any figure or promise on the card. The client's rule stands: no figures unless documented, and never "guaranteed". Invitation and QR only.

**Copying**
16. The reference creator's clip gives the mechanism only. Not its lorry, its framing, its message wording or its ending beat. Likewise nothing from P1–P9.

---

## 6. Access log (all 2026-11-21)

| Source | Requests | Result |
|---|---|---|
| adsoftheworld.com: 5 keyword searches (CGI, FOOH, unboxing, one take, found footage), homepage, /campaigns, one campaign page | 10 | All refused: 403, then 405 "Human Verification" CAPTCHA. Nothing read. |
| dandad.org search (`/search?term=`): unboxing (twice), one take, found footage, fake out of home, hoax, dashcam, delivery box, fake, box, one shot, CGI, CCTV, prank, delivery, Saudi, drop | 17 | 200. Title matches only; five terms returned nothing. |
| dandad.org archive case pages: unboxing, unboxing-2, blurred-unboxing, unboxing-the-truth, unbox-the-banner, go-with-the-fake, fake-views, pizza-box, shot-on-iphone-11-pro-hermitage, starr-park-cctv, hot-spicy-season-2, stadiums-food-delivery, akhou-nora, lego-news-rebuilt, aero-delivery-man | 15 | 200. Text read; every film "Log in to watch". |
| thedrum.com: topic page, site search, one opinion article, one insight article | 4 | Topic page 200 (not mined); search shell empty; opinion article standfirst only (registration wall); insight article 202 empty. |
| fooh.com (4 library entries by curl, 3 by WebFetch) | 7 | No connection / host not resolvable. |
| marketingbrew.com, adnews.com.au, campaignasia.com | 3 | Host not resolvable. |
| Web search | 2 | Leads only. |

Pages that loaded: about 36. Refused or empty: about 21. No logins, no CAPTCHA or paywall worked around. No screenshots taken; nothing added to `02-research/_work/`.

---

## What this means for the brand

1. **Shoot it for real if at all possible.** A real box, a real (safe) drop, a real hand and one unbroken take is the most believable version, sidesteps AI-labelling, and is the only version whose honesty needs no caption. *(inference from P3, P8 and R9)*
2. **The box has to be HIPPO at a glance, without the logo.** Colour and shape must identify it in a blurred half-second; test this on a phone before the shoot.
3. **The clip's meaning lives on the card.** One line that completes "ما ينزل خفيف", the QR, held still, found by the hand in-shot. No figures.
4. **Stay ordinary and small.** The Saudi FOOH field appears to be giant products on Riyadh landmarks; an everyday car park and a normal-sized box is HIPPO's own register. Before locking the concept, a person should look at the Philips "gift box from a helicopter" entry to rule out resemblance.
5. **This check is incomplete on FOOH and on disclosure.** Either allow `fooh.com` (and ideally `marketingbrew.com`, `adnews.com.au`, `campaignasia.com`) in the session's network settings and re-run that part, or have a person browse Ads of the World, FOOH examples and the platforms' AI-label rules in an ordinary browser and pass the links back.
