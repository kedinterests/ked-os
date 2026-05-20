---
project: County Directories
repo: kedinterests/new-directory-pages
local: /Users/chrismalone/new-directory-pages-1
status: active
---

# County Directories

Multi-county mineral rights professionals directory for MineralRightsForum. Deployed as static Astro sites per county to Cloudflare Pages, driven by Google Sheets data via Apps Script.

## GitHub

https://github.com/kedinterests/new-directory-pages

## Local Clone

/Users/chrismalone/new-directory-pages-1

## Stack

- Astro 5, Tailwind CSS, static output
- Cloudflare Pages with Cloudflare Functions (OAuth proxy for Decap CMS)
- Google Apps Script JSON endpoint per county
- Decap CMS for content editing
- County configs in `sites.json`

## Notes

Each county maps a subdomain (e.g. `reeves-county-texas.mineralrightsforum.com`) to a Google Apps Script endpoint and SEO/display settings. Supersedes the old `county-directory-pages` and single-county `reeves-county-texas` repos.

See also: `internal/new-directory-pages/profile.md` for the standalone project profile.
