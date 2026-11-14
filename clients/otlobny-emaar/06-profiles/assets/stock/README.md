# otlobny-emaar: open-licence stock library for company profile v04

Status: **29 files.**
- Round 1: 8 from Wikimedia Commons.
- Round 2: 14 from Flickr via the Openverse API.
- Round 3: 7 Gulf-credible images from Flickr via Openverse.

**8 files are DEMOTED** (see below). Compiled by the art-director, date accessed 2026-11-14.

Contact sheets:
- `06-profiles/_work/stock_contact_v05.png`: current, all 29 files.
- `06-profiles/_work/stock_contact_v04.png`: kept for the record.

**Round 3 is the current guidance. Its sections below (page plan, grade, demotions) override the round-2 "Recommended cover set".**

## Round 3: answer to review_v04_r1 M4 / M5

### v05 page plan (no image used twice anywhere in the book)

| Page | Hero (large) | Tiles |
|---|---|---|
| Cover | cover-hero_blue-glass-facade_wikimedia-glass-building-corner.jpg | 1. contracting_tower-construction-with-palms_flickr-3384156664.jpg<br>2. cleaning_rope-access-blue-glass-tower_flickr-16633802875.jpg<br>3. landscaping_palm-park-riyadh-museum_flickr-51949716085.jpg<br>4. maintenance_technician-headlamp-tools_flickr-51315198261.jpg |
| p2 Contents | none: type only (the old p2 image was the cover facade cleaners) | — |
| p4 About / Madinah | opener_madinah-haram-plaza-umbrellas_wikimedia-masjid-al-nabawi-2024-3.jpg. **Crop or retouch any legible hotel signage ("TAIBA FRONT HOTEL", review M5).** Keep the crop to umbrellas, minarets and the marble. | — |
| p6 Services overview | opener_madinah-haram-panorama_wikimedia-mezquita-del-profeta-dd01.jpg (band). Check for and crop any legible Latin signage. | — |
| p7 General contracting | contracting_steel-erector-on-beams_flickr-132069821.jpg (2048 px: half-page at most) | 1. contracting_concrete-screeding-crew_flickr-4184357497.jpg<br>2. contracting_surveyor-theodolite_flickr-8756741875.jpg |
| p8 Landscaping | **UNFILLED.** Interim: landscaping_date-palm-walkway-doha_flickr-7631829614.jpg as a portrait panel, max about 90 mm tall | 1. landscaping_palms-dry-planting_flickr-4968666077.jpg |
| p9 Maintenance | maintenance_hvac-gauges_wikimedia-379th-eces-8502255.jpg (**this page only**) | 1. maintenance_rooftop-ac-units-technician_flickr-54752357237.jpg<br>2. contracting-electrical_distribution-board_wikimedia-small-house-distribution-panel-2.jpg (electrical maintenance) |
| p10 Cleaning | **UNFILLED.** Interim: cleaning_mop-and-trolley-floor_flickr-24978817211.jpg at tile size, as the lead image | 1. cleaning_rope-access-window-cleaner_flickr-4797579546.jpg |
| p11 Manpower supply | **UNFILLED.** Interim: manpower_gulf-site-workforce_flickr-9836421046.jpg at tile size | 1. manpower_waiter-pouring-tea_flickr-38075436525.jpg<br>2. manpower_catering-table-setup-overhead_flickr-6160161346.jpg |
| p12 Logistics | **UNFILLED.** Interim: logistics_warehouse-racking-aisle_flickr-4324416999.jpg at tile size, as the only image | — |

Other pages (vision, why us, our work, partners, contact) use **no stock photo**. If a layout needs one, ask the art-director rather than repeat an image.

**Not used anywhere in v05:** all DEMOTED files, plus the Madinah images beyond the two assigned above.

**UNFILLED means** no image of 2000 px or more that is credible for the Gulf could be sourced. On those pages, size the interim image within its tile limit and let type, colour and the diamond pattern carry the rest. Do not enlarge 1024 px files.

### Colour grade recipe (apply to every photo, identically)

1. **Saturation:** −20 (Photoshop Hue/Saturation, master). This tames the green lawns and the red and orange vests.
2. **Contrast:** Curves with two points:
   - 64 → 56
   - 192 → 200

   This is about +8 contrast. Black output is raised to 10 (of 255), so the darkest tone is #0A0A0A and no shadow goes to pure black.
3. **Brand tint:** solid colour layer #1F3162 (navy), blend mode Soft Light, opacity 15%.
4. **White balance:** none per image, except warm interiors (waiter pouring tea, catering): −5 on the Temperature slider (Camera Raw) before step 1, so they sit with the daylight images.

CSS equivalent for screen proofs:
```css
filter: saturate(0.8) contrast(1.08);
/* overlay: */
background: #1F3162;
mix-blend-mode: soft-light;
opacity: 0.15;
```

Duotone frames (cover tiles) may use #1F3162 → #3758B0 at 100% instead. If they do, use that treatment for **all** cover tiles, never a mix.

### DEMOTED (do not use in v05; files kept, not deleted)

| File | Why |
|---|---|
| contracting_rebar-worker_wikimedia-rebar-worker-j2.jpg | Winter: beanie, camouflage trousers (M5) |
| landscaping_palm-promenade-lawn_flickr-19570930662.jpg | Lush English lawn, Torquay (M5) |
| landscaping_gardener-trimmer_flickr-54576923958.jpg | European woodland gardener (M5) |
| landscaping_date-palm_wikimedia-date-palm-tree-landscape.jpg | Flat white sky, weak light |
| cleaning_floor-scrubbers-lobby_wikimedia-floor-scrubbers.jpg | Hazy, low contrast, maker mark |
| logistics_white-box-truck_flickr-51928284838.jpg | Danish plates, Thermo King, Mercedes star, door lettering (M5) |
| logistics_forklift-in-motion_flickr-4325154436.jpg | Motion blur; maker badge |
| contracting_site-at-blue-hour_flickr-2146788503.jpg | Not maintenance (M4); European night scene, not needed elsewhere |

### Round 3 additions (all Flickr via Openverse; **TILE ONLY**, 1024 px)

| File | Need | Pixels | Source page | Author | Licence | Attribution | Why chosen | Crop / notes |
|---|---|---|---|---|---|---|---|---|
| landscaping_date-palm-walkway-doha_flickr-7631829614.jpg | Landscaping | 768×1024 | https://www.flickr.com/photos/86665756@N00/7631829614 | Studio Sarah Lou | CC BY 2.0, https://creativecommons.org/licenses/by/2.0/ | **Yes** | Date palms along a sand-coloured path in arid haze: unmistakably Gulf, no landmark. | Portrait. Keep the palm rhythm and the vanishing path. A tower in the far haze is small and unidentifiable. |
| landscaping_palm-park-riyadh-museum_flickr-51949716085.jpg | Cover tile / landscaping | 1024×768 | https://www.flickr.com/photos/49399018@N00/51949716085 | amanderson2 | CC BY 2.0 | **Yes** | A real Saudi park: palm trunks frame a landscaped bed with stonework, in strong sun. | Diamond crop centred on the stone feature between the palms. A small seated figure (bottom right) can be cropped out. |
| maintenance_rooftop-ac-units-technician_flickr-54752357237.jpg | Maintenance | 1024×683 | https://www.flickr.com/photos/25802865@N08/54752357237 | chooyutshing | Public Domain Mark 1.0, https://creativecommons.org/publicdomain/mark/1.0/ | No | A bank of rooftop condenser units with a technician (hard hat) at work: central A/C maintenance, literally. | Crop to the unit rows and the worker. Trim the green wall on the right if it fights the grade. A red mark on the parapet edge is small; check it at final size. |
| maintenance_technician-headlamp-tools_flickr-51315198261.jpg | Cover tile / maintenance | 1023×683 | https://www.flickr.com/photos/85045231@N04/51315198261 | S.C. Air National Guard (US Gov) | Public Domain Mark 1.0 | No | Sharp, focused technician with headlamp and pliers, in plain T-shirt and safety glasses. | Crop to the face and hands; drop the aircraft parts at the top. Must not imply military endorsement. |
| cleaning_rope-access-blue-glass-tower_flickr-16633802875.jpg | Cover tile / cleaning | 1024×683 | https://www.flickr.com/photos/78341140@N00/16633802875 | waitscm | CC BY 2.0 | **Yes** | A rope-access team cleaning a blue glass tower. On-brand blue, high contrast, Gulf high-rise context. The tower is not identifiable. | Crop to the four or five cleaners on the glass; avoid the tower edge on the left. |
| contracting_tower-construction-with-palms_flickr-3384156664.jpg | Cover tile / contracting | 1024×677 | https://www.flickr.com/photos/86838704@N00/3384156664 | ianmunroe | CC BY 2.0 | **Yes** | A tower under construction with a crane, date palms in the foreground and a clear sky: reads as a Gulf city site. | Crop to the right-hand tower, crane and palms; lose the generic towers on the left. |
| manpower_gulf-site-workforce_flickr-9836421046.jpg | Manpower | 1024×768 | https://www.flickr.com/photos/89165847@N00/9836421046 | mikecogh | CC BY-SA 2.0, https://creativecommons.org/licenses/by-sa/2.0/ | **Yes** | A real Gulf workforce in hard hats and hi-vis on site: shows the manpower-supply offer honestly. | Busy frame: crop tight to the central group. Faces are small and candid, not posed. |

### Round 3 rejects

- Muscat Al Alam palace garden: identifiable royal landmark.
- "Palms in Medina": hazy, shot through a car window.
- Ageing split-AC condenser: odd subject.
- Chiller-plant shots (MTA): dark, cluttered, US subway project.
- Second headlamp technician: duplicate.
- "Cleaning the road" (2048 px): the worker is not cleaning; empty composition.
- Generic crane.
- Dubai and Abu Dhabi skylines; Sheikh Zayed Mosque: landmarks.
- Qatar Airways aircraft and the Panasonic AC unit: brand logos.
- Dakar, military and rally vehicles: wrong subject.

### Round 3 access log

- **Openverse searches:** 74 queries (37 Wikimedia + 37 Flickr), about one every 2.6 s. Many 504s: each retried once, then skipped. No 429 from Openverse. 529 results.
- **Wikimedia previews:**
  - Openverse's thumbnail endpoint returned HTTP 424 for every Wikimedia result.
  - upload.wikimedia.org returned **429 on the first thumbnail request**, so all Wikimedia access stopped there, as instructed.
  - As a result, **no Wikimedia image could be viewed or downloaded this round.** That source holds the large (≥2000 px) Gulf files, including titles such as "Ajwa Date palm tree (Dabinu)" CC0 3456×4608, "Saudi Arabia garden irrigation" 3264×1952, "Gardens in Saudi Arabia" 2976×3968, "Riyadh Construction Site" 3947×2204, "Foreign workers at a construction site of The Pearl" 3750×2640, "Single white truck in a Desert" CC0 4032×3024, "A dallah of Arabic coffee" 5472×3648 and "Arabic copper coffee Dallah" CC0 8160×6120.
  - These are **unseen candidates**, not approved images: they need a person to view and download them from a browser.
- **Flickr:** downloads from live.staticflickr.com; `_k`/`_h` tried once each. Only the hazy Medina palms (1500 px) and "cleaning the road" (2048 px) offered larger sizes, and both were rejected on quality.

**Size warning.** Every round-2 Flickr image except the steel erector (2048 px) is 1024 px or smaller, because Flickr's `_k` (2048) and `_h` (1600) sizes did not respond for them. These are **TILE ONLY**: use them in small collage frames or diamond frames at roughly 85 mm wide or less at 300 ppi (about 120 mm at 220 ppi), or as small screen images. Never use them full-bleed.

## Recommended cover set (hero + 5 tiles)

| Role | File | Says |
|---|---|---|
| Hero (large) | cover-hero_blue-glass-facade_wikimedia-glass-building-corner.jpg | Modern buildings; already on-brand blue |
| Tile 1 | contracting_concrete-screeding-crew_flickr-4184357497.jpg | Construction, in a sunny arid setting with palms |
| Tile 2 | cleaning_mop-and-trolley-floor_flickr-24978817211.jpg | Professional cleaning (no faces, blue trolley) |
| Tile 3 | landscaping_palm-promenade-lawn_flickr-19570930662.jpg | Landscaped grounds, palms and lawn |
| Tile 4 | logistics_white-box-truck_flickr-51928284838.jpg | Goods transport |
| Tile 5 | maintenance_hvac-gauges_wikimedia-379th-eces-8502255.jpg | Maintenance hands at work |

Alternatives:
- logistics_warehouse-racking-aisle (strong symmetry; looks good in a diamond frame)
- contracting_surveyor-theodolite
- cleaning_rope-access-window-cleaner

All six cover images take a light #3758B0 / #1F3162 duotone. Apply one treatment to all of them so they read as a set.

## Library

Licence URLs:
- CC BY 2.0: https://creativecommons.org/licenses/by/2.0/
- CC BY-SA 2.0: https://creativecommons.org/licenses/by-sa/2.0/
- CC BY 3.0 PL: https://creativecommons.org/licenses/by/3.0/pl/deed.en
- CC BY-SA 3.0: https://creativecommons.org/licenses/by-sa/3.0/
- CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
- CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/
- US-Gov public domain: https://commons.wikimedia.org/wiki/Template:PD-USGov-Military-Air_Force

**Share-alike (BY-SA):** an edited version of the photo itself (for example a tinted crop) must keep the same licence. Credit it as "modified".

| File | Need / page | Pixels | Source page | Author | Licence | Attribution required | Why chosen | Crop / focal point / notes |
|---|---|---|---|---|---|---|---|---|
| cover-hero_blue-glass-facade_wikimedia-glass-building-corner.jpg | Cover hero | 3600×2400 | https://commons.wikimedia.org/wiki/File:Glass_building_corner_(Unsplash).jpg (orig. https://unsplash.com/photos/jwhqbR3clzQ) | Jonathan Simcoe | CC0 1.0 | No | Calm, architectural, already blue. Takes the brand tint. Sky for text. | Keep the facade diagonal; the sky triangle carries the logo and title. |
| opener_madinah-haram-plaza-umbrellas_wikimedia-masjid-al-nabawi-2024-3.jpg | Opener: About us / Al Madinah | 3600×2700 | https://commons.wikimedia.org/wiki/File:Masjid_al-Nabawi_2024_(3).jpg | Radosław Botev | CC BY 3.0 PL | **Yes** | Home city, seen respectfully from the plaza, in bright light. | Horizon on the lower third. Do not cut through minarets. Text in sky or on the marble. |
| opener_madinah-haram-panorama_wikimedia-mezquita-del-profeta-dd01.jpg | Opener: wide band / back cover | 3600×1858 | https://commons.wikimedia.org/wiki/File:Mezquita_del_Profeta,_Medina,_Arabia_Saudita,_2025-05-22,_DD_01.jpg | Diego Delso | CC BY-SA 4.0 | **Yes** | Symmetrical, quiet, professional. | Panoramic band centred on the umbrella. The flat grey sky benefits from a light duotone. |
| contracting_steel-erector-on-beams_flickr-132069821.jpg | Contracting, wide image | 2048×1536 | https://www.flickr.com/photos/67513462@N00/132069821 | billjacobus1 | CC BY 2.0 | **Yes** | Clean steel frame against a flat blue sky, with the worker small in frame. Much calm space for text; the only round-2 file above 2000 px. | Half-page at most for print (2048 px). Text in the sky (top half). A blue boom lift sits on the left; keep or crop. |
| contracting_concrete-screeding-crew_flickr-4184357497.jpg | Cover tile / Contracting | 1024×681 **TILE ONLY** | https://www.flickr.com/photos/34728058@N08/4184357497 | USACE Europe District | CC BY 2.0 | **Yes** | Real crew screeding concrete in hard hats, with arid light, palms and plastered villas: reads as a Gulf site. | Diamond crop centred on the two workers and the fresh slab. |
| contracting_surveyor-theodolite_flickr-8756741875.jpg | Contracting tile | 1024×683 **TILE ONLY** | https://www.flickr.com/photos/14214150@N02/8756741875 | DFID – UK Department for International Development | CC BY 2.0 | **Yes** | Precision and engineering. The face is hidden by the instrument; yellow hard hat. | Tight crop on the helmet and instrument. The red shirt is strong: duotone or use small. |
| contracting_site-at-blue-hour_flickr-2146788503.jpg | Contracting tile / atmosphere | 1024×802 **TILE ONLY** | https://www.flickr.com/photos/94852245@N00/2146788503 | seier+seier | CC BY 2.0 | **Yes** | Building under construction at blue hour. Naturally on-brand navy. | Building and crane centre. The sky is a ready text area. |
| contracting_rebar-worker_wikimedia-rebar-worker-j2.jpg | Contracting | 3600×2585 | https://commons.wikimedia.org/wiki/File:Rebar_worker_J2.jpg | Jamain | CC BY-SA 3.0 | **Yes** | Worker tying rebar, head down, not posing. | Right two-thirds. **Small logo on the cap: crop or retouch.** |
| contracting-electrical_distribution-board_wikimedia-small-house-distribution-panel-2.jpg | Electrical detail | 1920×2880 | https://commons.wikimedia.org/wiki/File:Small_house_distribution_panel_2.jpg | "Retired electrician" (Commons user) | CC0 1.0 | No | Orderly MEP detail. | Crop to the middle breaker rows. Maker marks unreadable at profile sizes. |
| maintenance_hvac-gauges_wikimedia-379th-eces-8502255.jpg | Maintenance / cover tile | 3600×2400 | https://commons.wikimedia.org/wiki/File:379th_ECES_HVAC_technicians_combat_rising_temperatures_(8502255).jpg | U.S. Air Force, A1C Derrick Boleyn | Public domain (US Gov) | No | Hands reading A/C gauges outdoors in a Gulf climate. | Crop to hands and gauges. Must not imply DoD endorsement. |
| landscaping_palm-promenade-lawn_flickr-19570930662.jpg | Cover tile / Landscaping | 1023×683 **TILE ONLY** | https://www.flickr.com/photos/80140240@N04/19570930662 | Torquay Palms | CC BY-SA 2.0 | **Yes** | Well-lit landscaped grounds: palms, lawn, paths. **Replaces the weak date-palm image as the main landscaping picture.** | Crop out the road on the left; centre on the right palm and lawn. |
| landscaping_palms-dry-planting_flickr-4968666077.jpg | Landscaping tile | 1024×768 **TILE ONLY** | https://www.flickr.com/photos/8123170@N06/4968666077 | Port of San Diego | CC BY 2.0 | **Yes** | Water-wise planting with palms. Credible for an arid municipal landscape. | Centre on the palm group and the planted bed. |
| landscaping_gardener-trimmer_flickr-54576923958.jpg | Landscaping tile (people at work) | 681×1023 **TILE ONLY (small)** | https://www.flickr.com/photos/202780880@N02/54576923958 | nenad53 | CC BY 2.0 | **Yes** | Real grounds-maintenance work, back to camera, natural light. | Portrait. Crop to the worker and trimmer; the smallest file, so keep it small. Green setting is lush rather than arid. |
| landscaping_date-palm_wikimedia-date-palm-tree-landscape.jpg | Landscaping (backup only) | 3600×2700 | https://commons.wikimedia.org/wiki/File:Date_palm_tree_landscape.jpg | Srianix | CC0 1.0 | No | Large file, but flat light. Kept only as a large-format fallback. | Superseded by the palm promenade for normal use. |
| cleaning_mop-and-trolley-floor_flickr-24978817211.jpg | Cover tile / Cleaning | 1023×683 **TILE ONLY** | https://www.flickr.com/photos/137169575@N04/24978817211 | aqua.mech | CC BY 2.0 | **Yes** | Uniformed cleaner, legs only, with a professional trolley on a polished commercial floor. No faces, no logos; blue matches the brand. **Replaces the floor-scrubber image as the main cleaning picture.** | Crop to the mop head and trolley; the diagonal of the mop handle leads the eye. |
| cleaning_rope-access-window-cleaner_flickr-4797579546.jpg | Cleaning (facades) | 1024×680 **TILE ONLY** | https://www.flickr.com/photos/49547334@N02/4797579546 | Malte Sörensen | CC BY 2.0 | **Yes** | Rope-access cleaner on a window against a clean blue sky. Half the frame is a calm text area. | Keep the worker on the right third; text in the sky. |
| cleaning_floor-scrubbers-lobby_wikimedia-floor-scrubbers.jpg | Cleaning (backup) | 2655×1991 | https://commons.wikimedia.org/wiki/File:Floor_scrubbers.jpg | Z22 | CC BY-SA 4.0 | **Yes** | Machines in a marble lobby. | **"T5" maker mark on the left machine: crop to the right 60% or retouch.** Now a backup. |
| logistics_white-box-truck_flickr-51928284838.jpg | Cover tile / Logistics | 1024×683 **TILE ONLY** | https://www.flickr.com/photos/99460566@N06/51928284838 | Lav Ulv | CC BY 2.0 | **Yes** | Clean white box truck on the road with an unbranded body. | Small maker mark on the fridge unit and a Danish number plate: blur or crop the plate. The vehicle-make badge is acceptable at tile size. |
| logistics_warehouse-racking-aisle_flickr-4324416999.jpg | Logistics (storage) | 1024×681 **TILE ONLY** | https://www.flickr.com/photos/42408834@N06/4324416999 | toolstop | CC BY 2.0 | **Yes** | Symmetrical racking aisle, ordered and calm. Works in a diamond frame. | Centre on the vanishing point. Carton labels are not readable at tile size; check at final size. |
| logistics_forklift-in-motion_flickr-4325154436.jpg | Logistics (handling) | 1024×681 **TILE ONLY** | https://www.flickr.com/photos/42408834@N06/4325154436 | toolstop | CC BY 2.0 | **Yes** | A forklift moving through the warehouse; the motion blur gives energy. | Crop around the forklift (right). A maker badge on the forklift may be visible: check at final size; retouch if legible. |
| manpower_waiter-pouring-tea_flickr-38075436525.jpg | Manpower (hospitality) | 1024×681 **TILE ONLY** | https://www.flickr.com/photos/145472109@N04/38075436525 | www.ralfsteinberger.com | CC BY 2.0 | **Yes** | Waiter pouring tea from a height. A hospitality gesture familiar in the region; eyes on the tea, not the camera; no alcohol. | Crop to the waiter, teapot and tray. Warm interior: duotone lightly or use in colour. |
| manpower_catering-table-setup-overhead_flickr-6160161346.jpg | Manpower (events / catering) | 1024×682 **TILE ONLY** | https://www.flickr.com/photos/65919204@N07/6160161346 | TEDxLasPalmas | CC BY-SA 2.0 | **Yes** | Overhead view of two staff setting a catering table. Graphic and faceless; event-staff service shown literally. | **Crop off the left edge: it has a red event banner with text.** Centre on the round table. |

## Rejects (reviewed, not kept)

**Round 1 (Wikimedia):**
- HVAC wiring: military cap and a branded drill.
- Office towers: logos.
- Haringey cranes: signage.
- Posed rebar worker: looks at the camera.
- USACE vests: logos, military context.
- "FIRE DEPT" signage.
- OTIS lifts: logos.
- Waiters with wine / Coca-Cola: alcohol, brand.
- Branded delivery vehicles.
- Army chefs: flags.

**Round 2 (Openverse / Flickr):**
- Facade cleaners on a boom lift: "Genie" logo, busy.
- Louvre robotic cleaner: identifiable landmark, gimmick.
- HDR crane site: halo artefacts.
- Hotel reception: sculpture of a nude figure.
- Forklift with USAID cartons: logo.
- Ford van and city-logistics vans: branded or merely adequate.
- Smiling barista: posed.
- Chef plating and paella waiter: logos on clothing.
- Cutlery place setting: wine glasses.
- Army Ball images: alcohol, uniforms.
- Dodo Pizza couriers: brand.
- All "Ford Courier" results: vintage adverts.
- Cleanroom staff: wrong context.

## Gaps still open

- **Courier / parcel delivery:** every result was branded.
- **Vehicle fleet:** nothing usable.
- **Lift maintenance:** all OTIS-branded.
- **Fire systems / plumbing:** the sprinkler station found in round 1 could not be downloaded.
- **Calm wide architecture or interior openers:** the atrium, lobby and glass-facade queries timed out (504). The glass hero and the two Madinah images cover this for now.
- **Hotel housekeeping:** none found.

## Tools and sources log

- **Round 1:** Unsplash and Pexels/Pixabay were blocked by bot challenges and not bypassed. The Wikimedia Commons API gave candidates, but upload.wikimedia.org original files returned 429, so only 3840 px / 1920 px thumbnails could be fetched.
- **Round 2:** Openverse API, anonymous, about one request every 2.6 s. Several queries got 504 (gateway timeout, not rate limiting); each was retried once and skipped if it failed again. No 429 was received.
- **Flickr sizes:** downloads came from live.staticflickr.com only. `_k` then `_h` were tried once per image, falling back to `_b` (1024).
- **Hosts not used:** no other image hosts were used or needed.
