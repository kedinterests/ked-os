# Mineral Auction ad: MRF 2026 off the Rotate Banner component

**Date:** 2026-11-19
**Status:** live, verified in a browser on desktop and mobile

## Where the ad lives now

| Theme | How the ad renders |
|---|---|
| Default (Mar 2024), the site default | "Rotate on Refresh Global Banner (JP)" component, theme 133, `header_items` setting. Left enabled on purpose (Chris). |
| MRF 2026, theme 213 | Native component `discourse/components/mrf-sponsor-banner.gjs`, rendered in `below-site-header` after `MrfHero` from `api-initializers/mrf-theme.gjs`. Theme 133 is no longer a child of MRF 2026. |

The MRF 2026 component outputs the same markup the old component did (`.alert-banner > .alert-info-banner > .rotate-banner`), so the banner styles already in MRF 2026's `common/scss` apply unchanged: an off-white strip with a gold border, a "Sponsored" pill from `.rotate-banner:has(a.sponsored)::before`, and a navy link with a gold underline. No new CSS was added.

Link classes `global_alert global_alert_styling sponsored` and the UTM string (`utm_campaign=global_text`, `utm_adv=blake_bergstrom`) match the old ad, so GA4 `advertiser_click` tracking is unchanged.

## To change the ad

- **Default theme:** the theme 133 `header_items` setting, as before.
- **MRF 2026:** edit `AD_URL`, `AD_LABEL` and `AD_TEXT` at the top of `mrf-sponsor-banner.gjs` in theme 213.

## API notes

- Key is in `.env.local`, user-scoped to Chris_Malone (admin). Send `Api-Username: Chris_Malone`.
- Use `https://www.mineralrightsforum.com`, because the bare domain 301s and drops the PUT.
- `PUT /admin/themes/{id}.json` with `theme.theme_fields` only replaces the fields sent. `theme.child_theme_ids` replaces the whole child list.
- The theme "After Header" field renders as `customHTML.top` inside `#main-container`. In MRF 2026 that is the content column below the hero, not full width, so it was dropped in favor of the outlet component.

## History of this change

1. Added the ad to After Header in theme 196 and deactivated theme 133. Chris re-enabled 133 because the default theme relies on it. Theme 196 was reverted to its original fields.
2. Added the ad to After Header in theme 213, which rendered in the content column under the hero, easy to miss. Replaced it with the outlet component above.
3. Removed theme 133 from MRF 2026's children; it stays a child of Default (Mar 2024).

Backups taken before any change: `internal/mrf-custom-css-scripts/backups/theme-{133,196,213}-2026-11-19.json`.

## Not verified

- A real click recorded in GA4 Realtime as `advertiser_click` on MRF 2026.
