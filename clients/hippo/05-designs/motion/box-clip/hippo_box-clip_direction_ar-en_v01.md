# HIPPO — box clip «ما ينزل خفيف»: direction v01

Client: hippo. Date: 2026-11-22. By: art-director. Piece: 18 s, 9:16 (1080 × 1920, 30 fps), phone-footage style, franchise invitation.
Route: text-to-video (ElevenLabs, `bytedance-seedance-v2.5`, text prompt only), then our designer composites the real logo, card and QR.
Status: working direction under the client's blanket approval of 2026-11-21. Not reviewed. Nothing was generated for this document.

Sources read: both council notes (2026-11-21), `02-research/ad-references_one-take-box-clip_2026-11-21.md` (partial: case texts only, no film watched), the four packaging photos, `brand-context.md`, and the two VO takes (measured for length and pauses; not heard).

**Recommendation on one take versus two pieces: two pieces (A + B).** Three reasons: a single 18 s generation lets the box drift in shape and colour; the QR hold needs a near-still frame that a walking shot will not give; and each piece can be re-rolled alone inside the spend cap. An optional single-take prompt is given in 2.3 as a comparison only.

---

## 1. Shot plan, 0–18 s

VO times below are for take 1 dropped in whole at 9.40 s (segment boundaries measured by silence detection; which words fall in which segment is inferred from the script order, not heard). Take 2 runs 0.16 s longer; start it at 9.30 s.

| Time (s) | Picture | Sound | VO |
|---|---|---|---|
| 0.0–1.0 | Piece A. Ordinary car park, hazy daylight. Filmer walking, phone held chest-high, framing nothing in particular. One empty bay 8–10 m ahead, cars either side of it. | Phone-mic ambience: light wind on the mic, distant traffic, footsteps. No music. | — |
| 1.0–1.4 | A pink-and-lime box enters from the top edge and falls straight down, fast, no spin. | Ambience only. No whoosh. | — |
| 1.4 | Lands flat in the empty bay and stops dead: no bounce, no roll. Low ring of dust. Phone jolts. The two nearest cars dip once on their springs. | THUD: the loudest event in the clip, with a sub tail that clips the phone mic for an instant. | — |
| 1.6–3.0 | Filmer stops. Exposure hunts once and recovers. Dust drifts. | One car: a short double chirp at 1.9, then nothing. One breath at 2.4. | — |
| 3.0–7.6 | Filmer walks to the box. It grows from small to about a third of frame width. The box is intact and closed, lying slightly askew to the bay lines. | Footsteps on gritty asphalt, getting slower. Cloth rustle. | — |
| 7.6–8.2 | Filmer reaches it; the phone tips down fast (motion blur). **Join A → B inside this blur.** | Handling noise on the phone body, a knee-bend rustle. | — |
| 8.2–10.2 | Piece B. Looking down at the closed box, long side running up the frame. One hand comes in from the bottom edge, lifts the lid and folds it back flat. Hand leaves. | Cardboard: tab pop at 8.5, creak 8.8–9.8, lid touching the ground at 10.1. | 9.40–10.58 «هيبو إذا نزل…» |
| 10.2–10.8 | Phone settles directly above. The card on the inside of the lid is the centre of the frame. Clean cut of tone: from here the frame is steady and nothing is a joke. | Ambience drops 4 dB under the voice. | 10.90–11.79 «ما ينزل خفيف.» |
| 10.8–18.0 | HOLD (7.2 s). Card and QR still, fully in frame, sharp. Only a slight handheld drift (see 4.3). | Ambience low. Nothing else. | 12.23–13.69 «امتياز هيبو التجاري.» · 14.18–15.59 «افتح هيبو في مدينتك.» · 15.99–16.95 «امسح الرمز.» · 16.95–18.0 no voice |

Fixed points when retiming the generated footage: impact at 1.4 s (trim the head of A to get there; speed changes between 90 % and 115 % only, never slow motion at the impact); card fully visible and still from 10.8 s; QR on screen for 7 s or more.

---

## 2. Generation prompts (English, paste as written)

Settings for every piece: 9:16, highest resolution offered, 30 fps if selectable, audio on if offered (it is replaced in the mix; see 5). Length: A = 8 s; B = 10 s. ASSUMPTION: the model offers these lengths; I did not open its guide. If B is capped shorter, the hold is extended from a freeze frame (4.3).

The box is described from the real photos: long, narrow, tuck-end, matte hot pink, white inside, lid hinged on the long side. The plain lime stripe stands in for the lime lettering.

### 2.1 Piece A — drop and walk-up (119 words)

```
Vertical handheld smartphone video, one continuous take. Hazy bright afternoon, soft shadows, in an ordinary open-air car park: grey asphalt, plain white and silver cars, a bare beige wall. The filmer walks slowly; slight hand shake, wide phone lens, exposure hunting. Suddenly a long narrow matte hot-pink cardboard sandwich box with one plain lime-green stripe along its lid falls straight down from the sky into an empty bay far ahead and stops dead without bouncing, impossibly heavy: a low puff of dust, the nearest cars dip once, the phone jolts. The filmer pauses, walks up to the intact closed box and tilts the phone down at it. Nobody else present. No text, no logos, no faces, no licence plates.
```

### 2.2 Piece B — lid opens, top-down hold (123 words)

```
Vertical handheld smartphone video, one continuous take, looking down. Hazy afternoon, soft even light. A closed long narrow matte hot-pink cardboard sandwich box with one plain lime-green stripe along its lid lies on grey car-park asphalt, its long side running top to bottom of frame. A man's bare hand with a white cuff reaches in from the bottom edge, lifts the lid and folds it back flat on the asphalt, then leaves the frame. Inside the lid lies a plain blank white card covering it; the base is empty, lined with plain white paper. The phone moves directly overhead and holds almost still for six seconds, the blank card large, sharp and unshadowed. No text, no logos, no printing, no faces, no food.
```

### 2.3 Optional — single continuous take (123 words; comparison only)

```
Vertical handheld smartphone video, one continuous take, no cuts. Hazy bright afternoon in an ordinary open-air car park: grey asphalt, plain white and silver cars, bare beige wall. Slight hand shake, exposure hunting. A long narrow matte hot-pink cardboard sandwich box with one plain lime-green stripe along its lid falls from the sky into an empty bay ahead and stops dead without bouncing, impossibly heavy: dust puff, nearby cars dip once, phone jolts. The filmer walks up and crouches; one bare hand folds the lid back flat on the asphalt. Inside the lid lies a plain blank white card. The phone holds still directly above it for five seconds. Nobody else present. No text, no logos, no faces, no licence plates, no food.
```

### 2.4 Negative list (paste into the negative field; if there is none, append as one line starting "Avoid:")

```
text, letters, numbers, logos, brand marks, watermarks, captions, signage, QR codes, licence plates, faces, people, crowds, children, animals, drones, helicopters, parachutes, cranes, ropes, slow motion, cuts, music, cinematic lighting, shallow depth of field, lens flare, studio look, bouncing, tumbling, broken glass, dents, cracked ground, fire, smoke, explosion, food, landmarks, towers, minarets, shop fronts
```

Re-roll notes, in the order to try them:
- Box bounces or tumbles: add "lands like a concrete block" after "stops dead".
- Plates or signs appear: add "cars seen from the side only".
- B never settles: generate B from "The lid is already open" onward (delete the hand sentence) and use the last second of the first B for the opening.
- Stripe grows lettering: replace the stripe phrase with "completely plain, unprinted" and accept an all-pink box.

---

## 3. Card layout (for the designer)

The card is built flat as a vector/HTML file, then placed on the blank card in piece B. Tajawal from `assets/fonts/`. Arabic, RTL, centred blocks; no letter-spacing; Western numerals.

**Format.** Portrait, width W, height 2.6 W (may stretch to 2.85 W if the generated lid is longer; give the extra to the logo). Outer margin 0.07 W. Card ground white. In frame the card should be about 480 px wide by 1250 px tall (44 % of frame width).

Top to bottom:

| # | Element | Size (of W) | Colour |
|---|---|---|---|
| 1 | Logo, file as supplied (`_originals/hippo-franchise-kit_2026-11-18/01-logo/hippo-logo-vector.pdf`), centred, unaltered, on white | width 0.34 (height about 0.54) | as supplied |
| 2 | «امتياز هيبو التجاري» Tajawal Bold, one line | text size 0.085 | #181717 |
| 3 | Headline «افتح هيبو» / «في مدينتك.» Tajawal ExtraBold, two lines, line height 1.25, on a full-width lime band | text size 0.15; band height 0.45 | #181717 on #BBD032 |
| 4 | Proof, two lines, Tajawal Medium, line height 1.6: «علامة سعودية منذ 2021» / «5 فروع في منطقتين» (line break at the «·»; wording unchanged) | text size 0.068 | #181717 |
| 5 | QR, centred, white ground | 0.78 square including the quiet zone | #181717 on white only |
| 6 | Label «قدّم طلب الامتياز» Tajawal ExtraBold in a black pill | text size 0.08; pill height 0.15, width 0.78 | #BBD032 on #181717 |
| 7 | Thin strip along the bottom edge | height 0.05 | #DA6FA2 |

Gaps between elements 0.05–0.06 W. Hierarchy: headline band first, QR second, «امتياز» label third. Pink is an accent only; no text in pink or lime on white (contrast fails).

**QR rules.**
- Source: the client's franchise code (`_originals/hippo-franchise-profile-and-qr_2026-11-18/hippo-franchise-qr.png`); if it is soft at this size, regenerate from the same decoded URL, error correction M, and confirm it decodes to the identical URL.
- Share of frame: QR (with quiet zone) at least 30 % of frame width (324 px at 1080), target 35 % (about 375 px). Below 30 %: punch in on the footage (up to 115 %) or reject the take.
- Module size at least 7 px in the 1080-wide export. Quiet zone 4 modules of clean white on all four sides; nothing touches it (no pill, no shadow, no finger).
- No logo in the middle of the code, no rounding of modules, no colour.
- Position in frame: whole QR inside x 90–930 and y 300–1400, clear of the platform's caption and button areas. The pink strip and the lower margin are what the caption may cover.
- Smallest text on frame after scaling: 28 px high line size at 1080 wide. With W = 480 px the proof line is 33 px: do not go smaller.

**If the box comes out lying across the frame** (long side horizontal): landscape card, QR at the left at full card height less margins, text block at the right, same order. Only usable if the QR still reaches 30 % of frame width; otherwise re-roll B.

---

## 4. Compositing notes

### 4.1 HIPPO lettering on the box
- On the real box the lime HIPPO letters fill the top face of the lid along its length. In piece A that face is small, moving and handheld, so the lettering is **optional**: attempt it only from about 5.5 s to 7.6 s, when the box is at rest and large, as a planar-tracked patch (pink face plus lime lettering) that covers the whole lime stripe. If the track slides by even a pixel or two, drop it and leave the plain stripe. Never add it during the fall.
- In piece B the outside of the lid faces the ground after it opens; no lettering is needed. Before the lid opens (8.2–8.8) the stripe is left as it is.
- The brand is carried by the real logo on the card and by the voice. Pink plus lime is the colour cue before that.
- ASSUMPTION to confirm: lime lettering made from the supplied wordmark reproduces the client's own printed box (seen in his photo), so it is not a new logo colour variant. If that is not accepted, skip the lettering.

### 4.2 The join between A and B
- Cut inside the fast downward tilt at 7.6–8.2: last 3–4 blurred frames of A to the first frames of B, with a vertical directional blur across 6 frames and a 2-frame luminance dip (exposure hunt). The handling noise in the sound covers it.
- Backup if the tilt does not match: start B on the hand, already crossing the lens, and cut on the dark frame it makes.
- Match before joining: asphalt tone, shadow softness and white balance of B to A (grade B, since A sets the look). Box pink matched by eye at the cut.
- Do not describe the clip as one take in the caption or anywhere in the post.

### 4.3 What must stay still
- The hold is built from one sharp frame of B (the best frame after the hand has left), not from moving footage, if the generated hold drifts, breathes in focus or warps the card.
- Card artwork is fixed to that frame first; the handheld drift is then applied to frame and card together, so they move as one: position within ±6 px, rotation within ±0.3°, about 1 cycle per second, no scale change, no motion blur.
- QR fully in frame, unobstructed, for the whole hold. No hand, no shadow, no exposure change, no grain animated over the code strongly enough to break modules.
- Keep 3 real moving frames of dust or light wherever possible (edge of frame) so the hold does not read as a still.

### 4.4 Making the card sit in the footage
- Corner-pin the card to the blank card; keep its edges 2–3 px inside the generated edges so no blank white rim shows unevenly.
- Card white is the footage's white, not #FFFFFF: sample the lid interior and tint the card to it. Lift the black to the footage's black level; pull the lime and pink saturation to sit with the box pink.
- Soft contact shadow, 2–3 px, on the side away from the light. A very slight light fall-off across the card (3–5 %) in the direction of the scene light.
- Blur the card 0.5–0.8 px to match the footage sharpness, then add the same grain. Re-check the QR after both.
- No glow, no bevel, no animated entrance. The card is simply there when the lid opens; from 8.8 to 10.2 it is tracked or, if the track fails, revealed only as the lid lands (cover the opening with the hand and the lid's own motion blur).

### 4.5 Clean-up passes on both pieces
Blur or paint out any plate-like shapes on cars, any pseudo-lettering on walls, cars or the box, any car badges that read in close-up, and anything person-shaped in the background.

### 4.6 Checks before it leaves the designer
- QR decoded from the exported MP4 at full size and at half size (540 wide). Scanning from one phone's screen with another phone cannot be done in this environment: a person must do it.
- Arabic on the card read on the exported frame: letters joined, right order, Tajawal, no fallback font.
- Frame-by-frame look at the impact, the join and the first hold frame.

---

## 5. Sound list

Generated audio from the video model is discarded. Everything below is built in the mix; all effects pass through a "phone mic" chain (band-limit about 150 Hz–9 kHz, light compression, mono) **except** the sub layer of the thud and the VO, which is clean and full-range. That contrast is the moment the clip admits it is an advert.

| Time (s) | Sound | Note |
|---|---|---|
| 0.0–18.0 | Open-air car-park ambience: light wind buffeting the mic, far traffic | Constant bed; down 4 dB from 10.2 |
| 0.0–1.2 | Two or three footsteps, cloth rustle | Stop just before the hit |
| 1.4 | THUD: dull heavy body (sandbag on asphalt) plus a 40–60 Hz sub tail of 0.5 s; 80 ms of mic clipping | Loudest event. No metal, no crash, no glass |
| 1.45 | Two cars' suspension creak, short grit scatter | Quiet, under the thud's tail |
| 1.9 | Car alarm: one short double chirp from one car, about 0.35 s | **Decision: yes, once.** No siren, no second car |
| 2.4 | One breath out through the nose | No word, no exclamation |
| 3.0–7.6 | Footsteps on gritty asphalt, eight to ten, slowing | |
| 7.6–8.2 | Phone handling rumble, knee-bend rustle | Covers the join |
| 8.5 | Cardboard tab pop | |
| 8.8–9.8 | Cardboard creak as the lid lifts | Under VO line 1 |
| 10.1 | Lid touching asphalt: soft paper slap | |
| 9.40–16.95 | VO (take chosen by ear; see below) | Clean, centred, no reverb |
| 16.95–18.0 | Ambience only | No sting, no sonic logo, no music anywhere |

No music at all. No whoosh before the drop (the earlier film's whoosh-then-hit rule is not used here: a whoosh announces an advert).
VO take: I could not listen. The Creative Director or a Saudi listener picks take 1 or take 2 by ear; timings in section 1 are for take 1.

---

## 6. Three things that would make it cringe (from the reference check, sections 4 and 5)

1. **A staged-looking landing.** Box centred and square to camera, slow motion at the hit, studio light on the box, every alarm going, big dust, cracked ground, dents. One impossible thing only: the weight. Everything else behaves like a dull Tuesday.
2. **Acting and polish before the reveal.** A filmer who talks or gasps, a hand already waiting, clean mixed sound or music from the first frame, the brand line arriving before the viewer has worked out what fell. The voice starts only as the lid opens.
3. **Asking to be believed, or a pasted-on card.** Posting it as a real incident, calling it one take, leaving it unlabelled, or a card that sits on the footage like a sticker (pure white, razor sharp, no shadow, wrong perspective). Also stay away from the Saudi stunt-film default named in the check: giant product, landmark, helicopter or crane.

---

## 7. Pass/fail test for a generated take

Pause on the impact, the join and the hold: **same plain pink box with a lime stripe in A and B; it lands dead with no bounce and nothing damaged; no person near it and no text, logo, plate, face or landmark anywhere; and in B a flat, unshadowed, blank white card at least 44 % of the frame wide stays sharp and nearly motionless for 5 seconds — one "no" and the take is rejected.**

---

## Assumptions and open points

- No approved strategy exists in `03-strategy/`; audience (Saudi franchise investors) is the standing assumption of 2026-11-18. This direction follows the client-approved line «هيبو إذا نزل، ما ينزل خفيف» and the Creative Director's rulings of 2026-11-21.
- Box proportions (about 3 : 1 lid, about 26–28 cm long) are estimated from the photos, not measured.
- The base of the box is shown empty (white paper only). Reason: generated food is not HIPPO's food. If a sandwich is wanted, it must come from a real HIPPO photo, composited, which adds a second risky composite.
- The hazy, soft light is a production choice: it makes A and B match and keeps hard shadows and blown whites off the card.
- Model lengths, negative-prompt field and audio behaviour of `bytedance-seedance-v2.5` were not checked.
- Open risk carried from the reference check: the unviewed Philips "pink gift box lowered by helicopter in Riyadh" lead. Our box is sandwich-sized, falls unaided in an anonymous car park, with no aircraft and no landmark; a person should still look at that film before posting.
- The join between A and B is a hidden cut; the reference check lists a hidden cut presented as one take as deceptive. The clip is therefore never called one take, and the caption carries «مشهد تمثيلي» and the platform's AI label.
