---
name: "Mineralwise"
status: active
stack: "Astro"
owner: "Chris"
repo: "https://github.com/kedinterests/mineralwise-astro"
location: "/Users/chrismalone/mineralwise-astro"
---

# Mineralwise

## Overview

Astro-based website for mineral rights education and resources. Content-rich site with scraper integration, Decap CMS backend, and newsletter subscription.

## Tech Stack

- **Framework:** Astro 5.17.1
- **Styling:** Tailwind CSS 4.1.18, UnoCSS
- **CMS:** Decap CMS
- **Content:** MDX support
- **Icons:** Tabler Icons, Heroicons
- **Deployment:** Cloudflare Pages
- **Integrations:** Zoho Flow webhooks, GDPR/CCPA cookie consent

## Features

- Static site generation
- Content management via Decap CMS
- Newsletter widget with responsive mobile design
- Web scraper system (410+ scraped content directories)
- SEO audit tooling
- Image optimization pipeline
- Decap webhooks for content updates

## Timeline

- Status: Active and maintained
- Recent work: Newsletter responsiveness improvements, cookie consent system, Zoho Flow integration

## Deployment

```bash
npm run build && npx wrangler pages deploy dist --project-name=mineralwise-astro
```

## Scripts

- `npm run dev` — Dev server
- `npm run build` — Build with image optimization
- `npm run seo:audit` — SEO analysis
- `npm run download-images` — Scrape and cache images
- `npm run convert-html` — Convert HTML to Astro components

---

## Notes

- No WordPress. Astro-first approach.
- Scraper handles content ingestion from external sources.
- Decap CMS handles editorial updates.
- Newsletter widget recently refactored for mobile responsiveness.
- Cookie consent handles GDPR/CCPA compliance.
- Zoho Flow webhooks for external integrations.

## Contact

Kenny Dubose (founder, kenny@kedinterests.com)
Chris Malone (developer, chris@m11design.com)
