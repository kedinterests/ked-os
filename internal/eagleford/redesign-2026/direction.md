# eaglefordshale.com redesign: visual direction

Run as Sloane (brilliant-os `teammates/sloane-visual-designer.md`), 2026-10-08, same protocol as
`ked-os/internal/bakken/redesign-2026/`. Sam review at the end.

## Research summary

The sector-wide peer and inspiration passes from Bakken carry over (Rigzone, Hart, OGJ, NGI, Shale Experts;
Texas Tribune, Canary Media, High Country News). An Eagle Ford pass added STEER (now a TXOGA awards event),
the Texas Railroad Commission Eagle Ford page, San Antonio Report, Texas Standard, the Express-News and
Laredo Morning Times (stylesheet only) and UTSA IED.

- **Regional peers are thin.** Nobody publishes a current, designed Eagle Ford front page. RRC is the source of record
  (a list of spreadsheets); UTSA has dropped its Eagle Ford reports; STEER is now an awards event.
- **Merriweather is taken.** The current site and Texas Standard both use it, so it says nothing about this site.
- **What is regional:** ranch-country leases, a bilingual border (Webb, Maverick), and the formation's
  hydrocarbon windows, which run from oil to dry gas as the rock dips toward the Gulf.

**The finding that shapes the brief:** nothing has been published since February 6, 2019. The homepage shows
lorem ipsum, template address text, an invalid block on every page, and "over 100 rigs running" (Baker Hughes
shows 49). Every lodging listing expired in 2015 or 2016. As with Bakken, the comp uses the most recent real
headlines with their real dates as labeled stand-ins.

## Three directions

**A. Strata, network edition (recommended).** The same system as the Bakken comp: the same type, grid, data
strip, front page and jobs band. Each play is identified by its logo's middle band: Bakken green, Eagle Ford orange.
Only the play-specific sections change. Tradeoff: the two sites read as siblings. That is the point. One Astro
codebase can theme both, and advertisers can buy across the network.

**B. Independent South Texas identity.** Its own type and palette, built on ranch brands, caliche and the border.
Tradeoff: more distinctive for this one site, but it doubles the design and build cost and throws away the
logo family KED already owns.

**C. Data desk.** The same alternative offered for Bakken: a dark, numbers-first terminal look.
Tradeoff: cold for royalty owners and job seekers.

## Strata, Eagle Ford edition

**Palette.** Shared tokens with Bakken, plus the Eagle Ford accent and the window colors.

| Token | Hex | Role | Contrast |
|---|---|---|---|
| Lower Shale | `#1E1F1C` | Ink, dark bands | 14.8:1 on Caliche |
| Eagle Orange | `#E4701E` | The logo's middle band. Fills, and text on ink only | 5.2:1 on ink; 2.8:1 on paper, so never text there |
| Burnt Orange | `#A8480C` | Kickers, links and buttons on paper | 5.1:1 on Caliche; white on it 5.8:1 |
| Upper Shale | `#818286` | Rules and the gray band | decorative |
| Caliche | `#F4EFE6` | Page ground (warmer than Bakken's paper) | n/a |
| Oil / Dry gas | `#7E9A4A` / `#C2462B` | Window fills in the cross-section only | decorative |

**Type.** The same as Bakken: Archivo, Source Serif 4 and IBM Plex Mono. The network shares one type system.

**Signature moves (from Eagle Ford's own assets)**
1. **The strata band in Eagle Ford orange.** The logo's three bands, with the middle band orange, run as full-bleed dividers and above the footer.
2. **The dipping cross-section.** The site's geology copy (directly beneath the Austin Chalk; 4,000 to 14,000 ft)
   is drawn to scale as a schematic. The Austin Chalk sits above the Eagle Ford and the Buda Lime below it, dipping toward
   the Gulf. The Eagle Ford band itself is colored by window: oil, then wet gas and condensate, then dry gas.
3. **Live production at display scale.** EIA's Eagle Ford region oil estimate is set about nine times body size, with gas and the
   Baker Hughes rig count beside it.
4. **The lodging directory.** No other play site has it. The categories are set as large condensed type, each with the towns
   it serves. This is a workforce audience the Bakken site doesn't serve.

**Shared with Bakken (deliberately):** the masthead, nav, front page with rail, newsletter panel, ad slots, county
index pattern, jobs band and footer. Each of these becomes one component in the shared build.

**Ground alternation:** Caliche, then the strata band, then Caliche (numbers), then ink (cross-section), then
Caliche-2 (lodging), then Caliche (counties), then ink (jobs), then the band and footer. Never two dark sections in a row.

## Template-tells critique

| Tell | Hit? |
|---|---|
| Icon-card grid | No |
| Identical rounded image boxes | No |
| Uniform alternating split rows | No |
| Decorative chips | No |
| Scrim + headline + two buttons hero | No |
| Every section the same width | No. The strata bands are full-bleed and the cross-section spans the full grid |
| Display scale no larger than 2x body | No. Production figure about 9x, lodging categories about 3x |

0 of 7.

## Sam review

- Walked at 1440, 768 and 375. No horizontal page scroll at any width.
- **Cross-section on phones:** it keeps its proportions and scrolls sideways inside its own frame, with a "swipe" hint.
  Squashing it to 375px would make the dip unreadable.
- **Fixed during review:** the longer wordmark overflowed the masthead (now sized for "Eagle Ford Shale");
  the production figure showed false precision (1,105,316 from an estimate, now rounded to the thousand);
  a depth fact wrapped badly; the lodging rows were misaligned.
- **Touch targets** are at least 44px. **Focus** uses Burnt Orange on paper and Eagle Orange on ink.

## Live data

`refresh-data.py` writes `data.json`, and the page fills from it, with a built-in snapshot as fallback.
- **FRED:** WTI and Henry Hub daily spot.
- **EIA STEO:** Eagle Ford region oil (`COPREF`) and gas (`NGMPEF`). These are monthly EIA estimates, and the series runs into the future, so
  the script takes the latest month before the current one.
- **EIA:** Texas crude (`MCRFPTX2`), monthly.
- **Baker Hughes Eagle Ford rig count:** entered by hand in `data.json` under `manual`. Baker Hughes blocks scripted
  downloads, and the weekly file URL changes. 49 for the week of Oct 2, 2026.
- **DEMO_KEY** hit EIA's rate limit during this session. The Texas crude value is seeded from the research pass.
  Set `EIA_API_KEY` to the real key for production.
- **Also available, not wired:** RRC's monthly Eagle Ford production workbook (a stable URL, parseable with openpyxl).

## Verify before anything ships

- The window arrangement in the cross-section (oil updip to the northwest, dry gas downdip toward the Gulf) against an RRC or EIA map.
- Depth: the site says 4,000 to 14,000 ft; the RRC page says 4,000 to 12,000.
- The operator list. Names that no longer trade under that name were removed (Anadarko, BHP, Petrohawk, Marathon, Pioneer, Chesapeake, Hess).
- The lodging towns come from listings that expired in 2015 and 2016.
- The newsletter cadence, and who writes the news.
