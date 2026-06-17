# MRF Dec 2025 Placement — Ad Unit 6162 Split

**Date:** 2026-06-17
**What:** Removed ad unit `23328696162` (`mrf topic above suggested`) from the MRF Dec 2025 placement's effective targeting. Created new dedicated "Suggested" line items in each active order targeting that unit directly, with a percentage-based daily impression split.
**Why:** The placement showed 4 units in GAM UI but only 3 were intended after removing 6162 months earlier. The placement itself was correct (3 units) but existing line items held stale targeting. Resolution: create separate line items for 6162 per advertiser rather than relying on placement targeting.
**Alternatives considered:** Updating existing line item targeting (API doesn't support it; would require re-saving each line item in GAM UI to re-resolve the placement).

## Impression split for unit 6162
| Advertiser | Daily Impressions | % |
|-----------|------------------|---|
| NARO Texas | 700 | 50% |
| Enverus | 210 | 15% |
| Aspen, CCFF Legal, CHD, Legacy MM, Overland, Permico, Robbins | 70 each | 5% each |

Based on ~1,400 avg daily impressions on that unit. New line items named "[Advertiser] Suggested" and created manually in GAM UI (API doesn't support line item creation in v1).
