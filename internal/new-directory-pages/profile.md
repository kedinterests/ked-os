---
name: "New Directory Pages"
status: active
stack: "Cloudflare Pages / Cloudflare Functions / Google Apps Script / KV Storage"
owner: "Chris"
updated: "2026-05-19"
---

# New Directory Pages

## Overview

Multi-county mineral rights professionals directory for MineralRightsForum, served via SSR Cloudflare Functions, data pulled from Google Sheets via Apps Script and cached in Cloudflare KV. Deployed to `directory.mineralrightsforum.com`.

Also hosts the MRF forum redesign proposal assets (static HTML pages in `/public`).

## Goals

- Serve a SEO-optimized directory page for each county on the MRF subdomain
- Pull directory listings from a single master Google Spreadsheet via Apps Script
- Support easy addition of new counties via Google Sheets (no code changes)
- Host the nationwide mineral services directory at `/mineral-services-directory`

## Tech Stack

- Cloudflare Pages (direct-upload deploy — **no git auto-deploy, must deploy manually from dashboard**)
- Cloudflare Functions (SSR, KV reads) — replaces former Astro static build
- Cloudflare KV for directory data storage
- Google Apps Script (`/functions/refresh.js` triggers data pull from master sheet)
- `sites.json` — county/site config
- Static HTML pages in `/public` for proposal assets

## Architecture

- `/functions/[slug].js` — SSR for each county directory page
- `/functions/index.js` — county index page (state/county grid)
- `/functions/counties.js` — full county listing with sidebar
- `/functions/refresh.js` — POST endpoint that pulls from Google Sheets and writes to KV; pre-indexes companies by county to avoid O(sites × companies) CPU timeout
- `/functions/data.json.js` — raw data API
- `/public/_routes.json` — routing config; excludes `/styles.css`, `/llms.txt`, `/*.html`, and named proposal pages from function handling

## Repos

- Canonical: `kedinterests/new-directory-pages` — local at `~/new-directory-pages-1/`
- Old fork: `chrismalone617/new-directory-pages` — local at `~/new-directory-pages/` (predecessor, do not use)

## Design System

The directory uses the MRF brand system — also the basis for the forum redesign proposal:
- **Navy:** `#0a192f` / `#0e2040`
- **Gold:** `#c5a059` (accent, CTAs, borders)
- **Off-white:** `#f8f6f1` (page background)
- **Fonts:** Playfair Display (headings) + Inter (body/UI)
- Card radius: 14px; shadow: `0 1px 2px rgba(0,0,0,.06), 0 8px 24px rgba(15,23,42,.06)`

## Proposal Assets (added 2026-05-15)

Three static HTML pages in `/public` for the MRF forum redesign pitch to Kenny:

| File | URL | Contents |
|---|---|---|
| `mrf-proposal.html` | `/mrf-proposal` | Pitch deck — opportunity, 3-phase transition plan, implementation scope |
| `logo-mockups.html` | `/logo-mockups` | 6 logo concepts (dark + light, multiple sizes) |
| `mrf-redesign-mockup.html` | `/mrf-redesign-mockup` | Discourse homepage mockup + full style guide |

See `notes/mrf-redesign-proposal.md` for full design system docs, logo descriptions,
Discourse CSS variable mappings, and implementation checklist.

## Notes

County configs live in `sites.json`. Each entry maps a slug (e.g. `reeves-county-texas`) to division metadata and SEO settings. Data for each county is stored in KV at `directory:{slug}:data`. The refresh endpoint (`/refresh` via POST with `X-Refresh-Key` header) pulls all counties in one shot from the master Google Sheet and writes to KV. This project supersedes `county-directory-pages` and the old single-county `reeves-county-texas` repo.

## Contact

Kenny Dubose — MRF site owner
