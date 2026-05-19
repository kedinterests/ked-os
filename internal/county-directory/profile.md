---
name: "County Directory"
status: active
stack: "Vibe"
owner: "Chris"
repo: "https://github.com/kedinterests/county-directory-pages"
location: "/Users/chrismalone/Cursor/county-directory-pages"
---

# County Directory

## Overview

Multi-tenant directory system for mineral rights professionals serving Texas oil & gas counties. Dynamic pages powered by Google Sheets, served through county-specific domains on Mineral Rights Forum.

## Tech Stack

- **Frontend:** Vanilla HTML/CSS with Tailwind CSS 3.4.13
- **Hosting:** Netlify Functions (serverless)
- **Data:** Google Sheets via Apps Script JSON endpoints
- **Integration:** Mineral Rights Forum Discourse community
- **Build:** npm build script for CSS compilation

## Features

- Multi-domain support (county-specific subdomains on mineralrightsforum.com)
- Dynamic professional listings from Google Sheets
- County-specific landing pages with SEO optimization
- Links back to Discourse forum categories
- Responsive directory interface
- Sitemap and robots.txt generation

## Served Counties

- Reeves County, TX
- Atascosa County, TX
- Culberson County, TX
- Pecos County, TX
- Ward County, TX
- Loving County, TX
- (Additional counties managed in sites.json)

## Data Sources

Each county directory pulls from a dedicated Google Sheet via Apps Script macro URL. Configuration stored in `sites.json`:
- Sheet URL (Apps Script JSON endpoint)
- SEO metadata (title, description)
- Directory intro text
- Return URL (back to forum category)

## Functions

Netlify serverless functions in `functions/`:
- `counties.js` — List available county directories
- `index.js` — Main directory rendering logic
- `refresh.js` — Refresh data from Google Sheets
- `health.js` — Health check endpoint
- `sitemap.xml.js` — Dynamic sitemap generation
- `robots.txt.js` — Robots.txt generation

## Deployment

Deployed to Netlify. Triggered updates via `refresh.js` function.

## Build

```bash
npm run build:css  # Compile Tailwind CSS to public/styles.css
npm run build      # Full build
```

## Directory Purpose

Connects mineral owners to trusted professionals (attorneys, landmen, engineers, appraisers, consultants) serving their specific county. Part of Mineral Rights Forum's broader mission since 2009.

---

## Notes

- Vibe-style hand-built implementation, not framework-based
- Google Sheets as CMS for professional listings
- Sites.json drives multi-tenant configuration
- SEO-optimized for county-specific searches
- Returns users to Discourse forum for community engagement

## Contact

Kenny Dubose (founder, kenny@kedinterests.com)
Chris Malone (developer, chris@m11design.com)
