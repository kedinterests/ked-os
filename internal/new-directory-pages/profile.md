---
name: "New Directory Pages"
status: active
stack: "Astro / Cloudflare Pages / Google Apps Script / Tailwind CSS"
owner: "Chris"
---

# New Directory Pages

## Overview

Multi-county mineral rights professionals directory for MineralRightsForum, driven by Google Sheets data via Apps Script and deployed per-county to Cloudflare Pages.

## Goals

- Serve a SEO-optimized directory page for each county on the MRF subdomain
- Pull directory listings from a single Google Spreadsheet per county
- Support easy addition of new counties via sites.json config

## Tech Stack

- Astro 5, Tailwind CSS, static output
- Cloudflare Pages with Cloudflare Functions (OAuth proxy for Decap CMS)
- Google Apps Script JSON endpoint per county
- Decap CMS for content editing

## Repos

- Canonical: `kedinterests/new-directory-pages` — local at `~/new-directory-pages-1/`
- Old fork: `chrismalone617/new-directory-pages` — local at `~/new-directory-pages/` (predecessor, less complete)

## Timeline

- Status: active

## Next Steps

1. Confirm which counties are live vs. in progress
2. Document county addition workflow in notes/

---

## Notes

County configs live in `sites.json`. Each entry maps a subdomain (e.g. `reeves-county-texas.mineralrightsforum.com`) to a Google Apps Script endpoint and SEO/display settings. This project supersedes `county-directory-pages` and the old single-county `reeves-county-texas` repo.

## Contact

Kenny Dubose — MRF site owner
