---
name: mineralwise-project
description: Mineralwise Astro website for mineral rights education and resources
metadata:
  type: project
---

# Mineralwise Project

**Repository:** /Users/chrismalone/mineralwise-astro (https://github.com/kedinterests/mineralwise-astro)

**Status:** Active, deployed to Cloudflare Pages

**Why:** KED project serving mineral rights education sector with content-rich Astro site backed by Decap CMS and web scraper.

## Stack

- Astro 5.17.1 (static site generation)
- Tailwind CSS 4.1.18 + UnoCSS
- Decap CMS (editorial interface)
- MDX support for content
- Cloudflare Pages hosting

## Key Features

- Scraper system ingests external content (410+ directories)
- Newsletter widget with mobile responsiveness (recently refactored)
- GDPR/CCPA cookie consent system
- Zoho Flow webhook integration for external automation
- SEO audit tooling built-in
- Image optimization pipeline

## Deployment

Cloudflare Pages: `npm run build && npx wrangler pages deploy dist --project-name=mineralwise-astro`

## How to apply

When working on mineralwise: reference this profile in `/internal/mineralwise/profile.md` for complete details. Use Astro patterns from `core/astro-patterns.md`. Newsletter widget changes require mobile testing before merge.
