# Advertising reference check

Before any advertisement, campaign or social ad set is designed, the agency looks at what the best work in the client's sector already looks like. This step is mandatory for services D (graphic design / advertising) and G (motion), and for any campaign idea presented to a client.

Source of this rule: the agency owner's instruction of 2026-11-18, with the eight sites below.

## The eight reference sites

| Site | What it is | Use it when |
|---|---|---|
| adsoftheworld.com | Archive of campaigns from every country, sorted by sector, medium and agency | You need to see what others have done in the client's own sector |
| canneslions.com | Cannes Lions winners each year, with the idea and the result explained | You need to know what the world counts as real creativity |
| dandad.org | D&AD awards archive (the Yellow Pencil), design and advertising | You are working on craft: typography, copy, art direction |
| oneshow.org | The One Club's archive of the strongest advertising and design work | You need examples of bold, simple ideas |
| musebyclios.com | Daily articles on new campaigns: who made them and why they worked | You want what is new, quickly |
| thedrum.com | Marketing and advertising news: new campaigns, analysis, interviews with creative directors | You need to understand the market, not only the ad |
| adforum.com | Work sorted by agency and brand, with the agencies' own profiles | You want to study one agency's style from its beginnings |
| theinspirationroom.com | Blog collecting notable ads from around the world, with campaign links | You want a quick dose of ideas before starting a brief |

## Status of the sites (checked 2026-11-18 — details in `templates/ad-reference-sources.md`)

- **Work from the agency's cloud environment:** adsoftheworld.com (by HTTP fetch; search by sector and country at `/campaigns`), dandad.org (full archive needs a free account), musebyclios.com (by browser).
- **Read for market context only:** thedrum.com (deeper content is paid).
- **For a person in an ordinary browser, not for agents:** canneslions.com — its terms forbid automated access and putting its content into AI tools, and the winners archive lives on lovethework.com; oneshow.org — the archive lives on oneclub.org, not reachable from here; adforum.com — blocks automated access. Agents record links supplied by a person; they do not fetch these.
- **DO NOT OPEN: theinspirationroom.com** — on 2026-11-18 both hosts redirect to an unrelated domain; the ad blog is no longer there. It stays in the table only until the owner confirms its removal.

## The step

1. **Who:** the market-researcher gathers; the art-director reads and draws the conclusions. The Creative Director does not skip the step to save time.
2. **When:** after the brief is approved and before any concept or layout is made.
3. **What to collect:** at least five relevant pieces — from the client's sector first, then from neighbouring sectors and from the Arab region where they exist. For each: campaign name, brand, agency, year, medium, the URL, one line on the idea, one line on why it works, and what (if anything) applies to this client.
4. **Where it goes:** `clients/<client>/02-research/ad-references_<campaign>_<date>.md`. The art-director's brief to the designer cites it.
5. **What comes out:** two or three observations that shape the concept, and a short list of things to avoid because the sector is already full of them.

## Limits

- **Reference, never a template.** Nothing is copied: no layout, headline, visual device or idea is lifted from another brand's work. `branding.md` already forbids imitating an existing identity; the same holds for campaigns.
- **No images are taken** from these sites into client work or into the client's folder as assets. Record links and descriptions; screenshots are for internal study only, kept in `02-research/_work/`.
- **Award work is not always right for the client.** Judge every reference against the approved strategy, the audience in `brand-context.md` and the client's market (Saudi and Gulf norms included).
- **Say what could not be checked.** Several of these sites put full case studies behind a login or a paid subscription, and a site may be unreachable from the cloud environment. Report which sites were opened, which were not, and why. Never describe a campaign you did not actually see.
- **Client isolation still applies:** a reference file belongs to one client and is not reused for another.
