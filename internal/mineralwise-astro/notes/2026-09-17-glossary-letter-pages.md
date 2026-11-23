# MineralWise glossary rebuilt as letter pages

Date: 17 September 2026
Repo: `kedinterests/mineralwise-astro`, branch `glossary-letter-pages`, head `1139d522d4349f3f8e9a27044dce3d27bf48b727` (two commits on top of `c6fa3ed`, which is `main`: `bd74e30` the rebuild, `1139d52` the page naming)
Worktree: `~/Documents/mineralwise-astro-glossary` (main checkout at `~/Documents/mineralwise-astro` was not touched)
Preview: https://glossary-letter-pages.mineralwise-astro.pages.dev
Status: pushed to the branch only. Not merged, not deployed to production. No Cloudflare or DNS changes.

## How terms were stored, and what changed

Terms were NOT a collection. Each of the 198 terms was its own hand-generated page file, `src/pages/resources/oil-and-gas-terms/<slug>.astro`, passing a hard-coded `term` and `definition` to `TermPage.astro`. The CMS had no glossary collection, so Kenny could not edit terms. The glossary index listed terms from `src/data/hierarchy.ts`, using title-cased slugs as labels ("Api Number", "Basic Sediment And Water Bs And W").

A 199th term, Grantor, lived at the site root as `/grantor`: a raw Brizy import with three internal links that depended on redirects. It was not in the glossary index at all.

Now:

- Terms are a content collection: `src/content/terms/<anchor>.json`, fields `term` and `definition`. 199 files. The filename is the anchor id on the letter page.
- The CMS (it is Sveltia CMS reading `public/admin/config.yml`, not Decap itself) has a new "Glossary Terms" folder collection: JSON format, create allowed, delete turned off. The same block was added to `public/config.yml` to keep the two files in step.
- `src/pages/resources/oil-and-gas-terms/[letter].astro` builds one page per letter that has terms. No page is generated for a letter with no terms. A `0-9` page would appear only if a term started with a digit; none does.
- `src/data/glossary-rules.mjs` holds the letter and anchor rules in plain JS so the Astro pages and the redirect generator share one definition. `src/data/glossary.ts` loads and groups the collection.
- The glossary index now reads the collection, shows real term names, links each letter to its letter page and each term to `letter/#anchor`. Letters with no terms are shown greyed out and are not links.
- Deleted: the 198 term page files, `src/pages/grantor.astro`, `src/components/TermPage.astro`, and the 198 term rows in `hierarchy.ts`. Added a `/resources/oil-and-gas-terms` node to `hierarchy.ts` (it was missing, so breadcrumbs used to read "Home / Pugh Clause"). Letter page breadcrumbs read Home / Resources / Oil & Gas Terms / P.
- Definitions are carried over character for character from the visible definition on each old page, with HTML entities decoded (`&amp;` to `&`, `&nbsp;` to a normal space). A script compared every built `<h2>` and `<p>` with the JSON: no differences.
- Each letter page has one `<h1>` ("Oil and Gas Glossary: P Terms"), a one-sentence intro, A to Z navigation that links only to letters that exist, each term as `<h2 id>`, a unique title ("Oil and Gas Glossary: P Terms | MineralWise"), a unique meta description under 160 characters, canonical through the existing `BaseHead`, and `DefinedTermSet` / `DefinedTerm` JSON-LD with name, description and url including the anchor.
- 34 terms had stacked slugs. They got short anchors, for example `fracking`, `drilling-mud`, `held-by-production`, `plug-and-abandon`, `lact-unit`, `three-d-seismic`. The other 165 keep their old slug as the anchor.
- `/what-is-fracking/` was not touched. Its text on the preview is byte-identical to production after stripping tags.

## Letter pages

Naming follows the genuine Squarespace letter pages, which lived at `/library/oil-and-gas-terms/oil-gas-definitions-<letter>-terms`, were titled "Oil & Gas Glossary - P Terms", and ran roughly 300 to 700 words per letter (P had about 22 terms and 688 words; the new P page has 22 terms and 672 words). The `/oil-and-gas-terms-a` to `-z` URLs were Brizy-era stubs from April 2025 with about 21 words each, not Squarespace. Both sets redirect to the matching new letter page.

Words are all words inside `<main>` (breadcrumbs, heading, intro, letter navigation and button included, about 45 words of that is furniture).

| Letter | Terms | Words |
|---|---|---|
| A | 7 | 263 |
| B | 10 | 268 |
| C | 16 | 450 |
| D | 21 | 516 |
| E | 7 | 221 |
| F | 14 | 544 |
| G | 8 | 216 |
| H | 7 | 286 |
| I | 7 | 193 |
| L | 8 | 260 |
| M | 8 | 273 |
| N | 4 | 177 |
| O | 7 | 226 |
| P | 22 | 672 |
| Q | 1 | 76 |
| R | 12 | 375 |
| S | 21 | 524 |
| T | 7 | 232 |
| U | 4 | 146 |
| V | 2 | 114 |
| W | 6 | 174 |

21 pages, 199 terms. No page for J, K, X, Y, Z (no terms).

## Redirects

- Retired URLs: 199 (198 under `/resources/oil-and-gas-terms/` plus `/grantor`). They are listed in the new `scripts/retired-term-urls.json`, path to anchor. All 199 were already in `scripts/legacy-urls.txt`, so the inventory file did not change.
- Every retired URL, slashed and unslashed, 301s in one hop to `/resources/oil-and-gas-terms/<letter>/#<anchor>`. Cloudflare keeps the fragment in the `Location` header (confirmed on the preview).
- `scripts/build-redirects.mjs` now understands `page#anchor`. It refuses to generate when the page does not exist, when the anchor is not a term filed under that letter, when a retired URL is still a live page, or when any destination is itself a redirected URL.
- Legacy rules re-pointed: 253 rules in the old slug table pointed at single-term pages (199 were each page's own slug, which is what served the Squarespace root-level form such as `/pugh-clause`; 54 were aliases and legacy slugs such as `fracking`, `hbp`, `depletion-allowance-2`). All now point straight at a letter page anchor. The new table has 256 anchor destinations and zero rules pointing at a retired URL.
- Legacy letter URLs: `/oil-and-gas-terms-<letter>`, `/library/oil-and-gas-terms/oil-gas-definitions-<letter>-terms`, and `/oil-and-gas-terms/<letter>/` now go to the matching letter page for the 21 letters that exist (63 rules) and stay on the glossary index for J, K, X, Y, Z. `/all-oil-and-gas-terms` and `/library/oil-and-gas-terms` still go to the index.
- Old versus new middleware, over all 908 inventory URLs in both slash forms: 889 results identical, 428 re-pointed to the same term's anchor, 56 letter URLs re-pointed from the index to a letter page, 400 newly redirected (the 398 retired term URL variants plus `/api-number` and `/grantor`), 42 no longer redirected because they are now the live letter pages, and 0 unexpected changes.
- `/api-number` bug found and fixed: the middleware's passthrough pattern began `^/(api|...)` with no boundary, so `/api-number` was treated as a Pages Function path and fell through to a 404. Folder names in the pattern now must match a whole segment. `/api/geo` still passes through (200 on the preview).
- www legacy URLs used to take two hops (www to apex, then apex to the page). The middleware now fixes host and path in one redirect. This cannot be exercised on the pages.dev preview host; it is covered by the unit tests only.
- A malformed percent-encoded path used to throw inside the middleware. It now falls through to the normal 404.
- `npm run build` now runs `npm run redirects` first (generator, then tests). Reason: terms are now CMS content, and a rename that moves a term to another letter would leave the committed middleware pointing at the wrong page. With this change the middleware is regenerated on every deploy, and a change that would break a redirect fails the build instead of shipping.

All 455 Squarespace-era paths from the Wayback list were run against the preview: 204 are glossary term paths (202 at the root) and every one 301s in one hop to a 200 with the anchor present on the page. The other 251 behave exactly as the middleware predicts. Only `/archive` and `/news` are 404, and neither matches a term, so no redirect was invented for them.

## test-redirects output

```
routes: 207
glossary: 199 terms on 21 letter pages
legacy URLs: 908 (each tested with and without a trailing slash) | redirected: 651 | left alone: 257
retired single-term URLs: 199 | rules checked for dead ends and chains: 546

All redirect checks passed.
```

New assertions: both slash variants of the whole inventory; every retired URL gives exactly `https://mineralwise.com/<letter page>/#<anchor>`; every destination page exists and every anchor is a real term on that page; no chains (each destination is requested again and must not redirect), checked for every rule in the generated tables and not only inventory URLs; no rule points at a retired URL; unknown paths still 404; `/api-number` redirects while `/api/geo` passes through; www lands in one hop. Mutation checks confirmed the guards bite: removing a term file makes the generator refuse, renaming a term without regenerating fails the tests, and a hand-made chain in the generated file fails the tests.

## Preview verification (curl and fetch against the preview host)

- 21 letter pages: all 200. `<h2 id=` counts match the table above and sum to 199.
- J, K, X, Y, Z letter URLs 301 to the glossary index; `/resources/oil-and-gas-terms/0-9/` is 404.
- All 199 retired URLs, slashed and unslashed (398 requests): 301 with the right `letter/#anchor`, then 200, anchor present in the HTML. 0 failures.
- Named legacy URLs, all one hop to 200: `/oil-and-gas-terms/fracking/` and `/oil-and-gas-terms/fracking` to `/resources/oil-and-gas-terms/f/#fracking`; `/oil-and-gas-terms/a/` and `/oil-and-gas-terms/a` to `/resources/oil-and-gas-terms/a/`; `/home` and `/home/` to `/`; `/owners-guide/unleased-mineral-owner/mineral-rights-value` to `/mineral-rights-value/`; `/oil-and-gas-operators/anadarko-petroleum` to `/anadarko-petroleum/`; `/oil-and-gas-terms-p` and `/library/oil-and-gas-terms/oil-gas-definitions-p-terms` to the P page; `/oil-and-gas-terms-x`, `/all-oil-and-gas-terms`, `/library/oil-and-gas-terms` to the index; `/abandoned-well`, `/pugh-clause`, `/acre-feet`, `/api-number`, `/api-number/` to their anchors; a query string survives (`/f/?utm_source=x#fracking`).
- 200: `/what-is-fracking/`, `/`, `/admin/`, `/admin/config.yml`, the glossary index, `/api/geo`, `/robots.txt`, `/llms.txt`.
- 404: `/zzz-nonsense-path`, `/zzz-nonsense-path/`, `/resources/oil-and-gas-terms/zzz-not-a-term/`, `/oil-and-gas-terms/zzz-not-a-term`, `/news`, `/archive`.
- Sitemap: `sitemap-index.xml` lists `sitemap-0.xml`; 202 URLs, all on `https://mineralwise.com`; the 21 letter pages are listed; 0 retired URLs are listed; `/grantor/` is gone.
- Canonical on the P page: `https://mineralwise.com/resources/oil-and-gas-terms/p/`.
- Browser check: `/resources/oil-and-gas-terms/pugh-clause/` lands on the P page scrolled to the Pugh Clause heading, clear of the sticky header. Desktop and 375px mobile layouts look right, no horizontal scroll.

## Internal links fixed

No internal link pointed at a `/resources/oil-and-gas-terms/<slug>` URL. Five pointed at legacy forms that redirect to terms, and were changed to the final URL: `/oil-and-gas-terms/division-order` (division-orders), `/division-order-2` (mineral-rights-inheritance, royalty-in-suspense, unclaimed-oil-and-gas-royalty), `/depletion-allowance-2` (owners-guide/leased-and-producing). Also fixed because they were redirect-dependent: one shale play link on the West Virginia state page, and the five section links in `llms.txt`. A scan of every internal `href` in `src` through the new middleware now finds 0 that redirect. A scan of the built HTML, XML and text finds 0 references to a retired URL.

## Not verified, or blocked

- www single-hop behaviour: unit tested only, because the preview host is not under mineralwise.com.
- The CMS collection was not opened in the `/admin` UI (needs a GitHub login). The config is served (200) and follows the Decap/Sveltia JSON folder collection format. Worth one manual check by Chris: open Glossary Terms, edit a term, confirm the saved JSON keeps both fields.
- I could not see the Cloudflare build log or the build command set in the Pages dashboard. The preview deploy built and the same `npm run build` passed in a scratch copy. If the dashboard command is `npm run build` (from the repo root or from `astro-site`), the new generator and test step ran on Cloudflare and passed. If the dashboard runs `astro build` directly, that step is skipped and the committed middleware is used as is, which is also correct today but would not follow a CMS rename. Worth checking the build command once.
- Nothing was blocked. The push of the branch went through without a prompt.

## Surprising or risky

1. The repo lives in iCloud-synced `~/Documents` and iCloud had evicted about 1,900 files inside `.git` plus source files (flag `dataless`). That is why git takes minutes or fails (`git worktree add` died with "mmap failed: Operation canceled") and almost certainly why `astro build` hangs locally. After reading every evicted file once to force the download, git was fast and the worktree was created normally. A copy of the project in `/private/tmp` built in 13 seconds. There are also iCloud conflict copies in `.git` ("index 2" to "index 11"). Moving the repo out of iCloud (for example `~/dev`) would end this. The new worktree is in `~/Documents` too, so it can be evicted again.
2. The main checkout is on branch `seo-redirect-remediation`, not `main`. Both are at `c6fa3ed`, so nothing is lost, but it is easy to commit to the wrong branch there.
3. The CMS config commits to `main`. Once this is merged, a term Kenny adds or renames goes live on the next deploy, and the build regenerates redirects. Renaming a term so it starts with a different letter moves it to another letter page, and its redirects follow. Deleting terms is turned off in the CMS on purpose: a deleted term would make the generator refuse and fail the build (safe, but the site would stop deploying until fixed). Term files must not be renamed, because the filename is the anchor.
4. Q has a single term and V has two. Those letter pages are about as thin as the pages being retired (76 and 114 words). The brief said one page per letter that has terms, so they were built, but they may still be reported as "Crawled, currently not indexed". Options for later: add Q and V terms, or fold small letters into a neighbour.
5. Four old pages carried extra original text only in their meta description, never visible on the page: API Number (a paragraph on the 14-digit format), Natural Gas Liquids (one more sentence), Executive Rights to Minerals (two more sentences), and Overriding Royalty Interest (a whole article with headings, run together). I preserved the visible definitions only, as instructed. That extra text is now only in git history (`c6fa3ed`) and in `scraped/`. It looks like good material for expanding those entries. About 20 other pages had site boilerplate appended to their meta description, which is now gone.
6. Old term pages rendered `&amp;` wrongly in `<title>` ("D&amp;amp;A"). The letter pages do not have the problem.
7. Two pre-existing link targets look wrong in content terms and were kept as they are, only made direct: "Click here to view a Division Order Model Form from NADOA" points at the Division Order glossary definition, and the Owners Guide "Depletion Allowance" card ("Learn about this royalty tax saving strategy") points at the two-line glossary definition.
8. Sitewide, internal links are written without a trailing slash, and Cloudflare Pages answers each with a 308 to the slashed URL. So nearly every internal click and crawl takes a redirect hop. New glossary links use the slashed form. Fixing the rest is a separate, mechanical job.
9. `scripts/convert-term-pages.js` and `scripts/migrate-oil-gas-terms.js` would recreate the retired page files if someone ran them. The generator now refuses to run if a retired URL is a live page again, so it would be caught, but the scripts could be deleted.
10. The Cloudflare preview sends `x-robots-tag: noindex`, which is normal for preview deployments and does not apply to production.

## Next action

Chris: review the preview, then merge `glossary-letter-pages` into `main` to deploy. After deploy, re-run the curl checks against mineralwise.com (including a `www.` legacy URL to confirm the single hop), resubmit the sitemap in Search Console, and watch the "Crawled, currently not indexed" and 404 buckets over the following weeks.

## Deployed to production, 17 September 2026

Kenny and Chris approved the preview. main fast-forwarded c6fa3ed..1139d52 and
pushed; Cloudflare Pages deployed within a minute.

Verified on mineralwise.com after the deploy settled:

- all 21 letter pages return 200; `<h2 id=` counts sum to 199
- retired term URLs, slashed and unslashed, 301 in one hop to `letter/#anchor`
- root-level Brizy term URLs (`/pugh-clause`, `/abandoned-well`, `/acre-feet`,
  `/division-order`, `/grantor`) one hop to the anchor; `/api-number` no longer 404s
- both old letter URL sets go to the matching letter page; letters with no terms
  (J, K, X, Y, Z) go to the glossary index
- www legacy URLs reach the apex destination in ONE hop (this could not be
  tested on the preview host)
- unchanged: `/`, `/what-is-fracking/`, glossary index, `/admin/`, `/api/geo`,
  unknown paths still 404
- sitemap: 202 URLs, 21 letter pages, 0 retired term URLs

A check run during the first minute after deploy saw 0 terms on some letter
pages and a two hop `/pugh-clause`. Both were edge propagation; a rerun minutes
later was clean. Wait two or three minutes after a deploy before verifying.

Still open: test one term edit in the CMS; confirm the Pages build command is
`npm run build`; move the repo out of iCloud-synced ~/Documents; resubmit the
sitemap in Search Console once the KED connector is live.
