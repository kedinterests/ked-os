# MineralWise status check and KED Google connectors, 17 September 2026

## Production is still unfixed

Tested live on 17 September. `seo-redirect-remediation` (c6fa3ed) was pushed to
origin on 27 August but never merged. `origin/main` is still 5aa5ab8 (11 June).

    /oil-and-gas-terms/fracking/   301 -> /resources/oil-and-gas-terms/fracking/ -> 404
    /owners-guide/unleased-mineral-owner/mineral-rights-value   404
    /home                          404
    www.mineralwise.com/resources/oil-and-gas-terms/royalty/   200 (duplicate host)

## The Pages preview build is verified

The open question from 27 August ("astro build hangs locally, confirm from the
Pages preview") is answered. The branch preview built and serves:

    https://seo-redirect-remediation.mineralwise-astro.pages.dev

Every spot-check URL, slashed and unslashed, 301s in one hop to a page that
returns 200. `/what-is-fracking/` and live glossary pages still return 200.
www consolidation cannot be tested on a preview host; check it after deploy.

The branch is a pure fast-forward of main (c6fa3ed's only parent is 5aa5ab8).

## Deployed 17 September

Chris pushed main (5aa5ab8..c6fa3ed). Cloudflare Pages deployed in under a
minute. Production spot check, all passing: every legacy URL, slashed and
unslashed, 301s in one hop to a 200; deep www URLs 301 to the apex with path
and query preserved; live pages still 200; unknown paths still 404 (no
catch-all); /sitemap.xml 301s to /sitemap-index.xml.

Google's recovery clock starts today. Read impressions first, at 4 to 12 weeks.

### How it was shipped

Claude's permission layer blocks production pushes. To ship:

    cd ~/Documents/mineralwise-astro
    git update-ref refs/heads/main c6fa3edb22818d180bf0fc8814c6a2616b3eaf6e 5aa5ab8085d118dccd257aa3c5e186196bc4e9e8
    git push origin main

(update-ref rather than checkout + merge because porcelain git hangs in this
repo. `git log` took over two minutes on 17 September.)

## Search Console and GA live in chris@kedinterests.com

Correction to the 27 August note, which said mineralwise.com "is not in either
connected Search Console account". True, but the reason is that both connected
accounts are BWW (pressnest@, nathan@brilliantly.net). The property and the GA4
property are owned by **chris@kedinterests.com**, which had no connector.

The BWW connector cannot be reused: its OAuth consent screen is Internal to the
brilliantly.net org, and it lives in brilliant-os, which KED work never writes
to. A KED-owned connector now lives at `integrations/gsc-mcp/` in ked-os,
written from scratch. See `integrations/gsc-mcp/SETUP.md`. It needs one Google
Cloud OAuth client and one browser login by Chris before it works.

Once connected: `search_analytics`, `inspect_url`, `list_sitemaps`,
`submit_sitemap` for Search Console, and Google's analytics-mcp for GA4.
Request Indexing has no API and stays manual.

## Semrush decision

Not now. The diagnosis is complete and more specific than a third-party crawl
would be. Revisit after redirects are live and 6 to 8 weeks of GSC data exist;
one month of Semrush or Ahrefs for a competitor keyword gap is the only use
that would pay for itself. Free stand-ins in the meantime: GSC, Bing Webmaster
Tools, Ahrefs Webmaster Tools.

## Ideas queued after the deploy

1. Wayback content recovery: diff Squarespace-era word counts against today for
   the top 50 legacy URLs; restore what the migrations flattened.
2. mineralrightsforum.com contextual links into matching guide and glossary
   pages. Owned authority on the exact topic.
3. DefinedTerm / DefinedTermSet JSON-LD on the 199 glossary pages.
4. Backlink reclamation from Ahrefs Webmaster Tools once redirects are live.
5. Expand the 40 to 60 terms with impressions in an owner-first format.
6. IndexNow / Crawler Hints toggle in Cloudflare.
