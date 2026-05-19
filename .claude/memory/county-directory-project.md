---
name: county-directory-project
description: County Directory — Multi-tenant mineral rights professionals directory for Texas
metadata:
  type: project
---

# County Directory Project

**Repository:** /Users/chrismalone/Cursor/county-directory-pages (https://github.com/kedinterests/county-directory-pages)

**Status:** Active, deployed to Netlify

**Why:** KED project serving mineral owners by connecting them to trusted professionals (attorneys, landmen, engineers, appraisers, consultants) in their specific Texas county for mineral rights work.

## Stack

- Vanilla HTML/CSS with Tailwind CSS 3.4.13
- Netlify serverless functions
- Google Sheets as CMS (via Apps Script endpoints)
- Multi-domain/multi-tenant architecture

## Key Features

- Dynamic professional listings sourced from Google Sheets
- County-specific landing pages (Reeves, Atascosa, Culberson, Pecos, Ward, Loving, etc.)
- SEO optimization for county-specific mineral rights searches
- Integration with Mineral Rights Forum Discourse community
- Sitemap and robots.txt generation
- Health check endpoint

## Architecture

- `sites.json` — Multi-tenant configuration (domain, sheet URL, SEO, serving_line)
- `functions/` — Netlify serverless handlers (index.js renders pages, refresh.js updates data)
- Google Sheets — Professional listings for each county
- Return URLs link back to forum for community discussion

## Data Flow

Google Sheets → Apps Script macro → JSON endpoint → Netlify function → Directory page

## How to apply

When working on county-directory: understand it's a Vibe-style hand-coded project (not framework-based). Data drives from Google Sheets. Professional metadata updates trigger via refresh.js. SEO-focused county pages feed Mineral Rights Forum community categories.
