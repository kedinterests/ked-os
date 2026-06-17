# Skill: GAM Reporting

Pulls live data from Google Ad Manager (network 6933594, KED Interests, LLC.) and produces performance reports as PDF, Excel, or on-screen tables. All scripts live in `scripts/`. Credentials are in `secrets/gam-credentials.json` (gitignored).

## When to invoke

When Chris or Kenny say anything like: "run the GAM report", "give me ad performance", "how are our advertisers doing", "YTD report", "pull impressions for [advertiser]", "generate an ad report for [advertiser]", "update the performance report", or "what's serving on [ad unit]".

---

## Available reports

### 1. YTD summary — all advertisers by month

**What it produces:** impressions, clicks, CTR for every advertiser, broken out by month, year-to-date.

**Output options:**
- On-screen table (HTML widget)
- PDF (`KED-YTD-Ad-Performance-2026.pdf`) — landscape, one page
- Excel (`KED-YTD-Ad-Performance-2026.xlsx`) — one row per advertiser, months merged across columns

**Script:** `scripts/gam-ytd-pdf.py` (PDF) and `scripts/gam-ytd-excel-v2.py` (Excel)

**Process:**
1. Run `scripts/gam-enverus-report.py` as a template — or build a fresh report POST to `/reports` with:
   - `dimensions: ['MONTH_YEAR', 'ADVERTISER_NAME', 'ORDER_NAME']`
   - `metrics: ['AD_SERVER_IMPRESSIONS', 'AD_SERVER_CLICKS', 'AD_SERVER_CTR']`
   - `dateRange.fixed`: Jan 1 of current year through today
2. Poll the operation until done, fetch rows via GET `{resultPath}:fetchRows`
3. Save raw JSON to `secrets/ytd-report-raw.json`
4. Run the PDF and/or Excel export scripts

**Update the date range** each year: change `year: 202X` in the report POST body and update filenames.

---

### 2. Single-advertiser PDF report

**What it produces:** a polished client-facing PDF showing impressions, clicks, CTR, daily chart, and ad unit breakdown for one advertiser.

**Script:** `scripts/gam-enverus-pdf.py`

**To reuse for a different advertiser:**
1. Find the advertiser's order name by querying `/companies` and `/orders` filtered by `displayName`
2. Update `ORDER_NAME` at the top of the script
3. Adjust the date range in the report POST body
4. Update the output filename
5. Run the script

**Key variables to change:**
```python
ORDER_NAME = "MRF Enverus 2026/06"   # → the target order's displayName
# date range in the report definition
# OUT filename
```

---

### 3. Ad unit activity audit

**What it produces:** a list of every order/line item that has served impressions on a specific ad unit, with total impression counts.

**How to run:** build a HISTORICAL report with:
- `dimensions: ['ORDER_NAME', 'LINE_ITEM_NAME', 'AD_UNIT_NAME']`
- `metrics: ['AD_SERVER_IMPRESSIONS']`
- `filters: [{ fieldFilter: { field: { dimension: 'AD_UNIT_ID' }, operation: 'IN', values: [{ intValue: 'UNIT_ID' }] } }]`

**Note:** the filter with `intValue` on AD_UNIT_ID currently causes a server error from GAM. Workaround: run without filter, fetch all rows, filter by ad unit name in Python. See `scripts/gam-enverus-report.py` for the pattern.

---

## API basics

**Auth:** OAuth 2.0, credentials in `secrets/gam-credentials.json`. Re-run `scripts/gam-auth.py` if the token expires (tokens last ~60 days of inactivity).

**Base URL:** `https://admanager.googleapis.com/v1/networks/6933594`

**Report flow:**
1. `POST /reports` — create report definition → returns `reportId`
2. `POST /reports/{reportId}:run` → returns operation name
3. `GET /operations/reports/runs/{runId}` — poll until `done: true`
4. `GET {response.reportResult}:fetchRows` — retrieve data (paginate with `pageSize=1000`)

**Known API limits (v1):**
- Line items: read-only (`get`, `list`), no targeting fields returned
- Cannot create, update, or delete line items or orders
- Placements: readable, PATCH exists but targeting writes are unreliable
- Reporting: full access — any dimension/metric combination works

**Valid dimension names (selected):**
`DATE`, `MONTH_YEAR`, `ADVERTISER_NAME`, `ORDER_NAME`, `ORDER_ID`, `LINE_ITEM_NAME`, `AD_UNIT_NAME`, `AD_UNIT_ID`

**Valid metric names (selected):**
`AD_SERVER_IMPRESSIONS`, `AD_SERVER_CLICKS`, `AD_SERVER_CTR`, `AD_SERVER_REVENUE`

**Date range format:**
```json
"dateRange": { "fixed": { "startDate": { "year": 2026, "month": 1, "day": 1 }, "endDate": { "year": 2026, "month": 6, "day": 30 } } }
```

---

## File map

| File | Purpose |
|------|---------|
| `secrets/gam-credentials.json` | OAuth credentials (gitignored) |
| `scripts/gam-auth.py` | Re-run to get a new refresh token |
| `scripts/gam-test.py` | Verify API connection |
| `scripts/gam-enverus-pdf.py` | Single-advertiser PDF (reusable) |
| `scripts/gam-enverus-report.py` | Fetch report data for one advertiser |
| `scripts/gam-ytd-pdf.py` | YTD all-advertiser PDF |
| `scripts/gam-ytd-excel-v2.py` | YTD all-advertiser Excel |
| `secrets/ytd-report-raw.json` | Cached YTD raw data (gitignored) |
| `secrets/enverus-report-raw.json` | Cached Enverus raw data (gitignored) |

---

## Dependencies

```bash
pip3 install --break-system-packages google-api-python-client google-auth-oauthlib google-auth-httplib2 reportlab openpyxl
```

---

## Active advertisers on MRF (as of Jun 2026)

| Advertiser | Order | Notes |
|-----------|-------|-------|
| Aspen Grove Royalty Co | MRF Aspen 2025/01 | Active |
| CCFF Legal | MRF CCFF Legal 3 Discourse | Active, highest volume |
| Courthouse Direct (CHD) | MRF CHD | Active, best CTR |
| Enverus | MRF Enverus 2026/06 | New Jun 2026 |
| Legacy Mineral Management | MRF Legacy MM 2025/10 | Expired Apr 30 — check status |
| NARO Texas | MRF NARO TX 2026/05 | Active thru Jul 2026 |
| Overland Oil | MRF Overland | Active |
| Permico Royalties | MRF Permico | Active |
| Robbins Family Minerals | MRF Robbins 2026/01 | Active thru Jan 2027 |

---

## Notes

- GAM network code: `6933594`
- Network timezone: America/Chicago
- Currency: USD
- New "Suggested" line items (unit 23328696162 — `mrf topic above suggested`) were created Jun 2026 after removing that unit from the MRF Dec 2025 placement. Each active advertiser has a separate line item targeting that unit with a daily impression goal.
