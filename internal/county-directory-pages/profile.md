---
name: "County Directory Pages (Legacy)"
status: maintenance
stack: "Astro / Cloudflare Pages / Google Apps Script / Tailwind CSS"
owner: "Chris"
---

# County Directory Pages (Legacy)

## Overview

Predecessor to `new-directory-pages`. Multi-county MRF directory built on the same Astro + Apps Script architecture but without the single-spreadsheet migration, deployment docs, or Decap CMS integration.

## Goals

- Maintain existing deployed county pages until migrated to new-directory-pages

## Tech Stack

- Astro, Tailwind CSS, Cloudflare Pages
- Google Apps Script JSON endpoints
- Sites config in `sites.json`

## Repos

- `kedinterests/county-directory-pages` — not cloned locally as of 2026-04-29

## Timeline

- Last updated: 2026-03-10
- Status: maintenance / being superseded by new-directory-pages

## Next Steps

1. Audit which counties are live here vs. migrated to new-directory-pages
2. Migrate remaining counties and deprecate this repo

---

## Notes

Contains `migrate-to-astro.md` and `migrate-to-single-spreadsheet.md` — migration docs were developed here and carried forward to new-directory-pages. No DEPLOYMENT.md or HANDOFF.md (added in the newer repo).

## Contact

Kenny Dubose
