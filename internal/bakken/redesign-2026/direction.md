# bakkenshale.com redesign: visual direction

Run as Sloane (brilliant-os `teammates/sloane-visual-designer.md`), 2026-10-08. Sam review at the end.

## Research summary

Full peer and inspiration passes ran against eaglefordshale.com, shaleexperts.com, rigzone.com,
hartenergy.com, ogj.com, naturalgasintel.com, willistonherald.com, NDIC/DMR (peers) and Texas Tribune,
Canary Media, High Country News, Axios Local, Grist, The Pudding (inspiration).

- **Sector conventions:** navy or black base, one hot accent, all-sans type, price ticker on top,
  stock rig photos, 300x250 right rail.
- **Honor:** a thin data strip near the masthead, newsletter above the fold, beat-based nav,
  ads as labeled fixed slots (ads are the revenue model).
- **Break:** stock rig hero, carousels, all-sans monotony, the bevelled logo, an ad before the first story.
- **Openings:** nobody is the *regional* publication for the Williston Basin; counties as a navigation
  layer is unclaimed; landowners and mineral owners get no calm reading register anywhere in the sector;
  NDIC data is published monthly and nobody displays it well.

**Finding that shapes the brief:** the live site has not published since March 2018 and the homepage shows
template placeholder text. The comp uses the most recent real headlines, with their real dates, as
labeled placeholders for a current news feed.

## Three directions

**A. Strata (recommended).** The regional paper of record for the basin. Warm paper, logo ink, logo green.
Heavy expanded grotesk for the masthead and data, a reading serif for headlines and body, mono for datelines.
Built on the logo's three bands, which are the formation's three layers.
Tradeoff: the most distinctive of the three. It needs a news cadence to look alive.

**B. Data desk.** A dark, terminal-style front page in the Shale Experts and NGI register. Prices and NDIC figures lead,
and headlines run as a dense feed. Tradeoff: credible to operators and investors, but cold for landowners and
job seekers, and it competes head-on with better-funded data products.

**C. Landowner's almanac.** All serif, cream and green, built around counties, courthouses, tax offices and
mineral rights explainers. News is secondary. Tradeoff: owns the landowner audience and the directory SEO,
but gives up the news and jobs positioning that the advertisers are paying for.

Strata holds all three audiences at once. Operators get the numbers, landowners get the reading register
and the county index, and job seekers get the hiring directory. That is why it is the recommendation.

## Strata: the system

**Palette** (from the logo, plus one working accent)

| Token | Hex | Role | Contrast |
|---|---|---|---|
| Lower Shale | `#1E1F1C` | Ink, dark bands, wordmark | 14.8:1 on Paper |
| Dolomite | `#387C2C` | Primary. Links, kickers, the green band | 4.6:1 on Paper; on Lower Shale use the tint `#7DBA6A` (7.2:1) |
| Upper Shale | `#818286` | Rules and the gray band only, never text | 3.4:1, decorative |
| Paper | `#F4F2EC` | Page ground | n/a |
| Flare | `#B4471A` | Deltas, the one hot accent, used rarely | 4.9:1 on Paper |

**Type**
- Archivo, variable width and weight (expanded 800 for the masthead and display figures, condensed 700 for
  nav and labels). The voice of a highway sign and an equipment plate.
- Source Serif 4 for headlines and body (body 18px desktop, 17px mobile). This is the reading register for landowners.
- IBM Plex Mono for datelines, sources and figures in tables. It is a third face with a job: it marks
  anything that is data, not prose.
- Portfolio check: none of the three is used on another BWW client design system.

**Signature moves (from the client's own assets)**
1. **The strata band.** The logo's three wavy bands (gray, green, black) become a full-bleed divider that breaks
   the container between sections, and the footer sits on it. Flat, no bevel.
2. **The cross-section.** The "about the play" section is laid out as the formation itself: three stacked
   horizontal layers, with the Three Forks below. Each layer carries its own facts.
3. **NDIC numbers at display scale.** Bakken and Three Forks production is set at roughly nine times body size
   in expanded Archivo. It takes the place of the stock rig photo every peer uses.
4. **The two-state county index.** 16 North Dakota and 11 Montana counties are set as a typographic map with county
   seats. This is the way into the directory pages, which hold most of the site's search value.

**Section rhythm:** 96px between sections on desktop and 64px on mobile. The masthead and data strip are exempt.
**Ground alternation:** Paper, then Paper with a rule, then the strata band, then the cross-section (three
tinted layers), then Paper, then Lower Shale (jobs), then the footer. Never two dark sections in a row.

## Template-tells critique (Sloane gate, against the rendered comp)

| Tell | Hit? |
|---|---|
| Icon-card grid | No |
| Identical rounded image boxes | No. The page has no photos; the map is the only image |
| Uniform alternating split rows | Deliberate, 1. The four geology layers share one structure because they are the formation; the middle dolomite is drawn thicker |
| Decorative chips or pills | No. Kickers are plain uppercase text |
| Scrim + headline + two buttons hero | No. The hero is a masthead and front page |
| Every section the same width | No. The strata bands and the cross-section run full-bleed |
| Display scale no larger than 2x body | No. The figure runs at about 9x body, the masthead at about 5x |

1 of 7, deliberate. Under the threshold of 3.

## Sam review (layout and usability)

- **Mobile:** the data strip scrolls sideways inside itself; the page never scrolls sideways. The cross-section
  layers stack, the county index drops to a single column per state, and the nav becomes a scrollable beat bar.
- **Touch targets:** nav items, county links and buttons are at least 44px tall.
- **Focus:** a 3px Dolomite outline with a 2px offset on Paper; the `#7DBA6A` tint on Lower Shale.
- **Ads:** two labeled fixed slots, a 728x90 in the lead column under the newsletter panel and a sticky 300x250
  in the rail after the headline list. Both sit after the first story, never before it.
- **Durability:** headlines of any length reflow. The display figure is one token that gets updated monthly from the
  NDIC Director's Cut.
- **Open item for Kenny:** who keeps the news fresh? The design assumes a weekly cadence (rig count, NDIC monthly).
  Without one, Direction C is the more honest choice.

## Facts to verify before anything ships

- ND production 1,153,000 bbl/d, of which Bakken and Three Forks 1,126,000 bbl/d, up 28,000 from May
  (June 2026, NDIC via Reuters, Aug 19 2026).
- ND rig count 26 (June 2026 Director's Cut; conflicting slide in August).
- All-time peak 218 rigs (DMR slides print 2012 and 2018 inconsistently).
- USGS 2008 recoverable estimate: the existing copy says both 4.0B and 4.3B.

## Verification

Rendered and walked at 1440, 768 and 375. No horizontal page scroll at any width (checked `scrollWidth`).
Fixed during the critique: wordmark clipping on phones, masthead overflow at tablet, the display figure
pushing its unit off the container, an ink sliver under the footer band, and a dead zone under the lead
column (the newsletter moved from the rail into the lead column, and the two columns now end level).

## Not done (the full Phase 2 sequence)

No type specimen or palette-options artifact, no `design-system.md`, no build-translation map. This is a home-page
comp to choose a direction. The site is Astro and Tailwind, not Beaver Builder, so the BB translation gate does not apply as written.

## Live data (added 2026-10-08)

The data strip, the display figure, the rig count and a new "where the rigs are" panel now read from `data.json`,
written by `refresh-data.py`. Sources are all public: FRED (WTI and Henry Hub daily spot), the EIA API
(North Dakota crude, monthly; runs on `DEMO_KEY` until the real key from Keeper is set as `EIA_API_KEY`) and the
NDIC active rig list (daily; gives county and operator per rig, so ND counties in the index show live rig counts).
The display figure changed from NDIC's Bakken + Three Forks number (no API) to EIA's statewide figure.
For the Astro build: run the same fetch at build time on a daily scheduled rebuild, or from a Cloudflare
Pages Function with a cached response. Never call EIA from the browser with the key.
