---
name: "Bakken"
status: in progress
stack: "Astro / Tailwind CSS v4 / Decap CMS / Cloudflare Pages"
owner: "Chris"
---

# Bakken

## Overview

Oil & gas site for the Bakken region, built from scraped HTML, with Decap CMS for frontend content editing.

## Goals

- Migrate scraped HTML content into a clean Astro-based site
- Enable Kenny or staff to edit content via Decap CMS admin at /admin
- Deploy to Cloudflare Pages

## Tech Stack

- Astro 5, Tailwind CSS v4, MDX
- Decap CMS with GitHub OAuth via Cloudflare Functions
- Cloudflare Pages hosting
- Source content: scraped HTML at `~/Documents/bakken/scraped`

## Repos

- Local only: `~/bakken/` — no git remote as of 2026-04-29

## Timeline

- Status: in progress (no git remote yet, not deployed)

## Next Steps

1. Initialize git and push to kedinterests org
2. Complete Decap CMS OAuth setup (GitHub OAuth app + Cloudflare env vars)
3. Deploy to Cloudflare Pages

---

## Notes

Build documentation in `~/bakken/build/`: BUILD_STEPS.md, DECAP_FIRST_BUILD_GUIDE.md, DEPLOYMENT_AND_SETUP.md, README_CMS.md.

## Contact

Kenny Dubose
