---
name: "Mineralwise Astro"
status: active
stack: "Astro"
owner: "Chris"
---

# Mineralwise Astro

## Overview

MineralWise.com, Kenny's oil & gas mineral-owner site. Squarespace to Brizy Cloud
to Astro on Cloudflare Pages. Each migration changed the URL structure and the
redirects never fully caught up, which cost the site roughly 94% of its organic
traffic.

## Tech Stack

- Astro 5, static output, deployed to Cloudflare Pages
- Decap CMS at `/admin`
- Redirects: `astro-site/functions/_middleware.js` (generated), NOT `_redirects`
- `PUBLIC_SITE_URL` lives in `wrangler.toml` `[vars]`, never as a dashboard secret

## Repos

- `kedinterests/mineralwise-astro` (private)
- Local clone: `~/Documents/mineralwise-astro`

## Hard-won rules

- Cloudflare Pages silently ignores `_redirects` past ~112 rules. Keep that file
  under 10 lines; everything else goes in the middleware.
- `_redirects` matches literal paths, so it never fires on the no-trailing-slash
  variant. The middleware normalises before lookup.
- Never use a wildcard redirect whose destination is not verified to exist. A
  redirect into a 404 is worse for rankings than a plain 404.
- `git commit` (porcelain) hangs in this repo. Use plumbing:
  `tree=$(git write-tree) && c=$(git commit-tree $tree -p HEAD -F msg) && git update-ref HEAD $c`
- `astro build` also hangs locally before emitting output. Verify builds from a
  Cloudflare Pages preview deploy instead.

## Timeline

- 2026-02 to 2026-04: Astro migration built and launched
- 2026-06-09/11: first round of SEO fixes (post-mortem items 1-6)
- 2026-06-11 to 06-13: Search Console Validate Fix run, failed
- 2026-08-20: diagnosis showed 235 still-broken URLs, avg position 34.8
- 2026-08-27: redirect layer rebuilt on branch `seo-redirect-remediation`

## Next Steps

1. Verify the Pages preview build, then merge `seo-redirect-remediation`
2. Spot-check redirects live, request indexing, then run Validate Fix in GSC
3. GA4 hygiene (see `notes/2026-08-27-seo-remediation.md`)
4. Content depth on the 40-60 glossary terms that draw real impressions

---

## Notes

- `notes/2026-08-27-seo-remediation.md`
- `POST-MORTEM.md` in the repo is the full incident record

## Contact

Kenny Dubose
