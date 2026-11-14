# otlobny-emaar: open-licence stock library for company profile v04

Status: **PARTIAL, 8 images (target was 18–26).** Compiled by the art-director, date accessed 2026-11-14.
Contact sheet: `06-profiles/_work/stock_contact_v04.png`

## Why the set is short

- **Unsplash:** unsplash.com search pages answered 403 "Access Denied" to headless Chromium. Plain curl was redirected to a bot challenge page (`/.within.website`), and `/photos/<id>/download` went to the same challenge. I did not spoof a browser to get past it. Without the search pages there is no way to get `images.unsplash.com/photo-…` URLs. images.unsplash.com itself answers 200, but it needs those full URLs.
- **Pexels / Pixabay:** headless Chromium got 403 "Just a moment…" (Cloudflare challenge) once each. I did not try again.
- **Wikimedia Commons:** the API search worked: 712 candidates passed the licence filter (CC0 / PD / CC BY / CC BY-SA) and the ≥2400 px filter. I shortlisted 120 by title and reviewed thumbnails of 106 (the last sheet of 28 never built). Then upload.wikimedia.org started answering 429 ("robot policy") to original-file downloads. Thumbnails at 3840 px and 1920 px still worked, so only images wider than 3840 px (or portrait images ≥2400 px tall at 1920 wide) could be fetched. The coordinator then told me to stop requests to Wikimedia, and the API itself began answering 429.
- **Processing:** files are re-saved as sRGB JPEG at quality 90, with the long side capped at 3600 px. Nothing else was edited: no retouching and no crop.

## Library

| File | Need / page | Pixels | Source page | Photographer / author | Licence | Attribution required | Why chosen | Suggested crop / focal point |
|---|---|---|---|---|---|---|---|---|
| cover-hero_blue-glass-facade_wikimedia-glass-building-corner.jpg | Cover hero (or section opener) | 3600×2400 | https://commons.wikimedia.org/wiki/File:Glass_building_corner_(Unsplash).jpg (original: https://unsplash.com/photos/jwhqbR3clzQ) | Jonathan Simcoe | CC0 1.0, https://creativecommons.org/publicdomain/zero/1.0/ | No (courtesy credit optional) | Calm, architectural and already blue, so it takes the #3758B0 / #1F3162 tint without fighting it. Large clean sky gives room for the logo and title. Nothing that dates it, no logos. | Keep the facade edge as a diagonal running from bottom-left to top-right. The sky triangle (left) is where text sits. Fits the rounded-diamond frame language. |
| opener_madinah-haram-plaza-umbrellas_wikimedia-masjid-al-nabawi-2024-3.jpg | Section opener: "About us / Al Madinah" | 3600×2700 | https://commons.wikimedia.org/wiki/File:Masjid_al-Nabawi_2024_(3).jpg | Radosław Botev | CC BY 3.0 PL, https://creativecommons.org/licenses/by/3.0/pl/deed.en | **Yes** | The company's home city, seen respectfully from the open plaza at a distance. Bright natural light, no faces close to the lens. The large marble foreground and sky take text. | Wide crop with the horizon at the lower third. Keep the minarets and umbrellas whole; do not crop through a minaret. Text in the sky (top) or on the marble (bottom). |
| opener_madinah-haram-panorama_wikimedia-mezquita-del-profeta-dd01.jpg | Section opener: wide band / back cover | 3600×1858 | https://commons.wikimedia.org/wiki/File:Mezquita_del_Profeta,_Medina,_Arabia_Saudita,_2025-05-22,_DD_01.jpg | Diego Delso | CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/ | **Yes** (share-alike: an edited version of the photo itself, e.g. a tinted crop, must stay CC BY-SA) | Symmetrical, quiet composition centred on the umbrellas, from a professional architectural photographer. Hazy sky is a calm text area. | Panoramic band, centred on the large umbrella. The sky is flat grey: a light blue duotone helps. A small Arabic sign at bottom right may be read; it is Arabic, so acceptable. |
| contracting_rebar-worker_wikimedia-rebar-worker-j2.jpg | Service 1, General contracting (also a cover small) | 3600×2585 | https://commons.wikimedia.org/wiki/File:Rebar_worker_J2.jpg | Jamain | CC BY-SA 3.0, https://creativecommons.org/licenses/by-sa/3.0/ | **Yes** (share-alike as above) | A real worker tying rebar, head down, not posing. Strong graphic grid of mesh. Workwear is plausible for a Saudi site. | Crop to the worker and mesh (right two-thirds). The wall at the top can be cut away or tinted for text. **Note:** small logo on the cap. Crop or retouch it out, or keep the image small enough that it cannot be read. |
| contracting-electrical_distribution-board_wikimedia-small-house-distribution-panel-2.jpg | Service 1, electrical works (detail / small frame) | 1920×2880 | https://commons.wikimedia.org/wiki/File:Small_house_distribution_panel_2.jpg | "Retired electrician" (Commons user) | CC0 1.0, https://creativecommons.org/publicdomain/zero/1.0/ | No | Clean, credible MEP detail with orderly wiring. Colour is controlled and works in a diamond frame. | Portrait. Crop to the middle two rows of breakers for a diamond or square frame. Breaker maker marks are tiny and unreadable at profile sizes. Check at final size. |
| maintenance_hvac-gauges_wikimedia-379th-eces-8502255.jpg | Service 3, Maintenance (central A/C) | 3600×2400 | https://commons.wikimedia.org/wiki/File:379th_ECES_HVAC_technicians_combat_rising_temperatures_(8502255).jpg | U.S. Air Force, A1C Derrick Boleyn (US government work) | Public domain, https://commons.wikimedia.org/wiki/Template:PD-USGov-Military-Air_Force | No | Hands-only shot of a technician reading manifold gauges on an outdoor A/C unit in a Gulf climate. Literal, sharp, no face, no fake smile. | Crop to the hands and gauges (centre-right). The dark unit on the left is a natural text panel. Do not say or imply it shows OTLOBNY staff; the profile already marks images as illustrative. US DoD images must not imply endorsement. |
| landscaping_date-palm_wikimedia-date-palm-tree-landscape.jpg | Service 2, Landscaping | 3600×2700 | https://commons.wikimedia.org/wiki/File:Date_palm_tree_landscape.jpg | Srianix | CC0 1.0, https://creativecommons.org/publicdomain/zero/1.0/ | No | A date palm against a modern stone building: a planted, institutional setting with a Gulf feel, not a European forest. | Crop to the trunk and crown, focal point centre. The white sky at the top-right takes text. It is the weakest of the eight on light (flat sky). Replace it if a stronger arid palm-park image can be sourced. |
| cleaning_floor-scrubbers-lobby_wikimedia-floor-scrubbers.jpg | Service 4, Cleaning | 2655×1991 | https://commons.wikimedia.org/wiki/File:Floor_scrubbers.jpg | Z22 | CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/ | **Yes** (share-alike as above) | Professional floor-care machines in a modern marble and glass lobby. Reads as commercial facility cleaning and has calm white space. | **Conditional.** The walk-behind machine (left) carries a "T5" maker mark. Either crop to the right 60% (corridor and robot scrubber) or retouch the mark out. Only 2655 px wide, so use it at half-page size or smaller. |

## Notable rejects (reviewed, not kept)

- **HVAC technician wiring (379th ECES 8502259):** downloaded, then rejected. Military camouflage cap and scarf, and a branded yellow power drill in frame. Never copied into this folder.
- **Office towers with brand names** (EY/Cloudflare complex, Sofitel-type tower, Westdeutsche Lotterie with flags): third-party logos.
- **Tower cranes at Broadwater Farm:** "Haringey London" and crane-maker signage readable.
- **Rebar worker (smiling to camera, "Rebar worker.jpg"):** posed look straight at the camera.
- **US Army Corps of Engineers site shots:** USACE logo vests, military context.
- **Fire department connection / sprinkler alarm (Butler, PA):** readable English "FIRE DEPT / BASEMENT" signage.
- **OTIS lift repair shots (Hong Kong, Sweden):** OTIS logos on barriers and uniforms.
- **Waiters with wine / rosé bottle / Coca-Cola tray:** alcohol and brand logos; culturally out of place for the client's market.
- **All delivery vehicles and couriers found** (Iceland, Lazada, Uber Courier, "boy" box, Budweiser, Coca-Cola): branded.
- **Catering chefs (US Army culinary arts):** shortlisted, but US flags and military badges in frame. Not downloaded after the Wikimedia stop.
- **Rebar tying hands (PD), sprinkler valve station (Brisbane):** chosen, but the original-file download failed (429). Not in the set.

## Gaps still open (no image in the library)

- **Cover supports:** cleaning in a commercial interior with people, landscaped grounds, logistics.
- **Service 1:** fire systems (sprinkler station chosen but not downloadable) and plumbing.
- **Service 3:** lift maintenance (everything found carried OTIS branding).
- **Service 5, Manpower supply:** hospitality / event / café staff. Nothing acceptable was found on Commons.
- **Service 6, Logistics:** warehouse racking, forklift, box truck, courier, fleet. Commons shortlist 1100 / 1034 / 1071 / 1099 was not reviewed or downloaded.
- **Wide neutral modern architecture openers:** Commons Unsplash mirrors 1009 / 1023 / 1025 were shortlisted but not downloaded.

**Recorded Unsplash IDs (from Commons mirror metadata), usable once Unsplash can be browsed:**
- glass corner: jwhqbR3clzQ
- concrete architecture: Knlde4SUjDE
- angular modern architecture: 9A42JPe_b8Q
- black building: f75w4vv0J7s
