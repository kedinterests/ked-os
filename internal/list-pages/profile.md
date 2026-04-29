---
name: "List Pages"
status: active
stack: "Astro / Cloudflare Pages / Google Apps Script"
owner: "Chris"
---

# List Pages

## Overview

Astro-based list/directory pages for MRF (testimonials and similar content), same architecture as new-directory-pages but for non-county listing content.

## Goals

- Serve testimonials and other list-format pages for MRF
- Pull data from Google Apps Script endpoints

## Tech Stack

- Astro, Cloudflare Pages, Cloudflare Functions
- Google Apps Script (`APPS_SCRIPT_CODE.gs`) for data
- Sites config in `sites.json`

## Repos

- `kedinterests/list-pages` — not cloned locally as of 2026-04-29

## Timeline

- Last updated: 2026-02-05
- Status: active

## Next Steps

1. Clone locally
2. Document which list pages are live

---

## Notes

Shares architecture with `new-directory-pages`. The `APPS_SCRIPT_CODE.gs` in root suggests a single shared script for all list sites.

## Contact

Kenny Dubose — MRF site owner
