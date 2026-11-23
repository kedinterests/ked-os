# Wayback content recovery, 17 September 2026

Compared every page the Internet Archive holds for mineralwise.com up to June
2025 (453 URLs) with what that URL serves today. Baseline is the last genuine
Squarespace capture where one exists (128 URLs), otherwise the latest capture
from the first Brizy months (325 URLs). Word counts are main content only:
header, footer, nav, scripts, and forms stripped.

Data: `wayback-recovery/results.csv` (all 453 rows) and
`wayback-recovery/old_text/` (recovered text for all 217 non-glossary URLs).

## Platform timeline, from the archive

- WordPress stub in 2015
- Squarespace from about April 2021 to late March 2025
- Brizy Cloud from April 2025 (first Brizy captures 24 April 2025)
- Astro from about March 2026

Only 61 URLs were ever archived before April 2025. The Brizy migration
multiplied the site into roughly 400 root-level pages, including one page per
glossary term. The Squarespace glossary was one page per letter at
`/library/oil-and-gas-terms/oil-gas-definitions-<letter>-terms`, 300 to 700
words each.

## Result by section (178 live non-glossary pages with a baseline)

| Section | Pages | Words then | Words now | Lost | Median old sentences kept |
|---|---|---|---|---|---|
| Shale plays | 22 | 8,492 | 4,102 | 52% | 23% |
| Owners guide | 8 | 3,055 | 1,472 | 52% | 78% |
| State pages | 26 | 5,517 | 4,129 | 25% | 58% |
| Operators | 78 | 18,726 | 15,684 | 16% | 74% |

Articles and legal pages at the root mostly survived, 80 to 100% of sentences
retained.

## Pages that lost 80 or more words (38 pages, 9,571 words)

| Words lost | Then | Now | Old sentences kept | Baseline | Page today |
|---|---|---|---|---|---|
| 1453 | 1679 | 226 | 0% | squarespace 20240824 | `/resources/oil-and-gas-operators/` |
| 949 | 1143 | 194 | 17% | brizy-era 20250613 | `/owners-guide/oil-and-gas-basics-for-mineral-owners/` |
| 824 | 1651 | 827 | 49% | squarespace 20241226 | `/surface-rights-vs-mineral-rights-in-oil-gas-leasing/` |
| 529 | 622 | 93 | 0% | squarespace 20240824 | `/resources/shale-plays/` |
| 495 | 659 | 164 | 26% | brizy-era 20250428 | `/owners-guide/cash-payment-for-oil-and-gas-royalty/` |
| 271 | 507 | 236 | 18% | brizy-era 20250424 | `/resources/shale-plays/marcellus-shale-new-york/` |
| 255 | 434 | 179 | 10% | brizy-era 20250418 | `/resources/shale-plays/marcellus-shale-ohio/` |
| 254 | 410 | 156 | 10% | squarespace 20250417 | `/resources/shale-plays/marcellus-shale-new-jersey/` |
| 251 | 418 | 167 | 19% | brizy-era 20250424 | `/resources/shale-plays/marcellus-shale-maryland/` |
| 248 | 385 | 137 | 6% | brizy-era 20250418 | `/resources/shale-plays/tuscaloosa-marine-shale-louisiana/` |
| 242 | 532 | 290 | 24% | brizy-era 20250424 | `/resources/shale-plays/marcellus-shale-pennsylvania/` |
| 216 | 406 | 190 | 6% | brizy-era 20250424 | `/resources/shale-plays/marcellus-shale-west-virginia/` |
| 210 | 431 | 221 | 18% | brizy-era 20250424 | `/resources/shale-plays/utica-shale/` |
| 201 | 385 | 184 | 20% | brizy-era 20250418 | `/resources/shale-plays/bakken-shale-north-dakota/` |
| 200 | 441 | 241 | 33% | brizy-era 20250424 | `/resources/shale-plays/haynesville-shale-louisiana/` |
| 198 | 431 | 233 | 39% | brizy-era 20250424 | `/resources/shale-plays/haynesville-shale-texas/` |
| 192 | 465 | 273 | 22% | brizy-era 20250418 | `/resources/shale-plays/utica-shale-ohio/` |
| 182 | 815 | 633 | 80% | brizy-era 20250424 | `/oil-and-gas-leasing-top-10-things-to-do/` |
| 179 | 318 | 139 | 22% | brizy-era 20250424 | `/resources/shale-plays/niobrara-shale-colorado-and-wyoming/` |
| 178 | 413 | 235 | 41% | brizy-era 20250424 | `/resources/shale-plays/eagle-ford-shale-texas/` |
| 171 | 320 | 149 | 46% | brizy-era 20250424 | `/resources/shale-plays/barnett-shale-texas/` |
| 149 | 356 | 207 | 32% | brizy-era 20250424 | `/resources/mineral-rights-by-state/texas-mineral-rights/` |
| 145 | 539 | 394 | 74% | brizy-era 20250418 | `/ad-valorem-taxes/` |
| 139 | 291 | 152 | 33% | brizy-era 20250418 | `/resources/shale-plays/utica-shale-new-york/` |
| 132 | 1351 | 1219 | 76% | brizy-era 20250418 | `/oil-and-gas-investment-basics/` |
| 130 | 303 | 173 | 50% | squarespace 20250418 | `/resources/shale-plays/fayetteville-shale-arkansas/` |
| 130 | 564 | 434 | 29% | squarespace 20250418 | `/royalty-in-suspense/` |
| 114 | 1397 | 1283 | 90% | squarespace 20250319 | `/what-is-fracking/` |
| 103 | 436 | 333 | 90% | squarespace 20250418 | `/gas-severance-tax/` |
| 102 | 487 | 385 | 66% | squarespace 20250329 | `/` |
| 102 | 885 | 783 | 89% | squarespace 20230326 | `/oil-gas-mineral-and-royalty-income-taxes/` |
| 100 | 218 | 118 | 29% | brizy-era 20250418 | `/resources/shale-plays/huron-shale/` |
| 100 | 439 | 339 | 90% | brizy-era 20250424 | `/oil-severance-tax/` |
| 92 | 353 | 261 | 60% | brizy-era 20250418 | `/resources/mineral-rights-by-state/alabama-mineral-rights/` |
| 87 | 937 | 850 | 90% | squarespace 20230312 | `/oil-gas-measurement/` |
| 83 | 279 | 196 | 54% | squarespace 20250418 | `/resources/oil-and-gas-operators/range-resources/` |
| 83 | 219 | 136 | 50% | brizy-era 20250418 | `/resources/shale-plays/woodford-shale-oklahoma/` |
| 82 | 255 | 173 | 43% | brizy-era 20250418 | `/resources/mineral-rights-by-state/new-york-mineral-rights/` |

## Restore order

1. The two directory indexes: operators (1,679 to 226 words) and shale plays
   (622 to 93). Zero old sentences survive on either.
2. The 22 shale play pages. Each lost about half its text and only 6 to 46% of
   the old sentences remain, so these were rewritten shorter, not trimmed.
   These are the named-play searches ("Haynesville shale mineral rights").
3. Owners guide: oil and gas basics for mineral owners (1,143 to 194), cash
   payment for oil and gas royalty (659 to 164).
4. Surface rights vs mineral rights (1,651 to 827) and royalty in suspense.
5. Texas, Alabama, and New York state pages.

Old copy from 2021 to 2024 may carry dated figures (rig counts, operator names,
prices). Review before it goes live.

## Bug found along the way

`src/pages/oil-gas-lease-forms.astro` is 1.18 MB: the page body is pasted into
the source 128 times. Live page is 1.2 MB of HTML with 2,304 paragraphs. Only
this page is affected (no other source page is over 150 KB). Fix: keep one
copy. The Squarespace version was 1,342 words.

## Dead archived pages

`/news` (Squarespace, 220 words, a 2014-era Colorado fracking news item) is a
404 today. Not worth restoring. `/api-number` was a 404 when this ran and was
fixed by the glossary deploy the same day.

## Restoration built, 17 September 2026 (branch `content-restoration`, commit 9e56d51)

Preview: https://content-restoration.mineralwise-astro.pages.dev
Not merged. Parent is main 1139d52. Worktree at `~/Documents/mineralwise-astro-content`.

The premise changed once the source was open. The pages were not rewritten
shorter. The migration scripts dropped fields:

- Shale plays: `const geology = ""` or `","` on 20 of 21 pages. The location
  sentence, reading notes, and some county lists were dropped too. Meta
  descriptions held the entire page body (up to 2,600 characters, `&amp;amp;`).
- State pages: the producing counties section was never carried over, the
  component hard coded "<State> Oil and Gas Board" as the regulator for every
  state, and any intro paragraph between the first and last was dropped
  (Alabama).
- Oil and Gas 101, the guide every shale and state page links to, kept its
  intro and lost all eight body sections.

Approach: keep current text, add what is missing, never replace. Link targets
in restored copy were resolved against production so none point at a redirect.
En and em dashes in restored copy were converted per the house rule. Text
that was already live was left as it was.

| Page | Words live | Words restored |
|---|---|---|
| Oil and Gas 101 | 194 | 1,120 |
| Surface rights vs mineral rights | 827 | 1,651 |
| Shale plays index | 93 | 648 |
| Cash payment for royalty | 164 | 534 |
| Haynesville Shale Louisiana | 241 | 408 |
| Marcellus Shale West Virginia | 190 | 372 |
| Barnett Shale Texas | 149 | 298 |
| Texas mineral rights | 207 | 335 |
| Alabama mineral rights | 261 | 335 |
| Oil gas lease forms | 171,776 | 1,342 (128 copies reduced to 1) |

Verified: `npm run build` passes in a scratch copy (208 pages), redirect tests
pass, preview serves every restored page, links inside restored copy return
200, glossary and legacy redirects unaffected.

Decisions made, for Kenny to overrule:

- Operators index: restored the sourcing note only. The archive repeated one
  boilerplate sentence under each of 78 companies; not restored.
- Cash payment page: "Receive a Free, No Obligation Cash Proposal" was not
  restored because the form it introduced no longer exists on the site. If
  buying royalties is still part of the business, that form is worth rebuilding.
- "Lease My Land" links on touched pages now go to `/lease-my-land/` as they
  did originally, not to the 10 common mistakes article.
- Royalty in suspense needed nothing. Its "loss" was a paragraph the old page
  printed twice.

Dated copy to review before merge: shale play intros cite 2008 to 2011 activity
("As of 2010, the Haynesville shale has more rigs..."), acreage by operator,
and company lists with names since merged or gone (Petrohawk, Encana, Anadarko,
XTO). All of this was already live; restoration added geology and location
text, which does not date.

Not done yet: the long tail. About 50 pages sitewide still carry a meta
description over 300 characters, and 15 files contain `&amp;amp;`. Operators
(78 pages, 16% lost) were not examined page by page.
