# GAM Ad Unit Integration in Directory Pages

**Date:** 2026-05-19
**What:** Directory ad cards now support Google Ad Manager (GAM) GPT ad units. Ad unit path stored in spreadsheet `ad_unit` column. GPT script loads in page `<head>`. Ad renders as 300x250 medium rectangle card. Image card (image_url + link) remains as fallback.
**Why:** Kenny already uses GAM for MRF ad management. Integrating GAM lets him use the same platform for directory ads without managing image hosting separately.
**Alternatives considered:** Image-only cards (too manual, no impression tracking); full script embed in spreadsheet (security risk, complex to manage).

## Key implementation details
- Ad unit path only in spreadsheet (e.g. `/6933594/mrf_card_ad_300_250`) -- not full tag code
- GPT `enableSingleRequest` deprecated -- use `enableServices()` only in head
- External stylesheet `height: auto` on iframes causes 150px default height -- must override with `.card--gam iframe { height: 250px !important; }`
- `nationwide?` column on Ads sheet targets national directory independently of county pages
