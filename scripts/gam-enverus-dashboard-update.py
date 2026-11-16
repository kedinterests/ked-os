#!/usr/bin/env python3
"""Roll the "Enverus on MRF" dashboard HTML forward to yesterday.

Usage: python3 scripts/gam-enverus-dashboard-update.py IN.html OUT.html

Reads the embedded `const D = {...}` data from IN.html, refetches the last
REFETCH_DAYS days plus everything after from Google Ad Manager, replaces those
days, then rewrites the hardcoded dates (footer, day count) and the order and
line item totals. Day index 0 is the campaign start (D.start).
"""

import json, os, sys, time, re, urllib.request, urllib.parse
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
import google.auth.transport.requests
from google.oauth2.credentials import Credentials

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "secrets", "gam-credentials.json")
NETWORK_CODE = "6933594"
ORDER_NAME = "MRF Enverus 2026/06"
BASE = f"https://admanager.googleapis.com/v1/networks/{NETWORK_CODE}"
REFETCH_DAYS = 2
MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

src, dst = sys.argv[1], sys.argv[2]
html = open(src).read()
m = re.search(r"^const D = (\{.*\});$", html, re.M)
D = json.loads(m.group(1))

start = date.fromisoformat(D["start"])
old_end = date.fromisoformat(D["end"])
yesterday = datetime.now(ZoneInfo("America/Chicago")).date() - timedelta(days=1)
fetch_from = max(start, old_end - timedelta(days=REFETCH_DAYS))
if yesterday < fetch_from:
    sys.exit("Nothing to update.")
first_idx = (fetch_from - start).days
last_idx = (yesterday - start).days
print(f"Refreshing {fetch_from} to {yesterday} (day {first_idx} to {last_idx})")

with open(CREDENTIALS_FILE) as f:
    cd = json.load(f)
creds = Credentials(token=None, refresh_token=cd["refresh_token"], client_id=cd["client_id"],
                    client_secret=cd["client_secret"], token_uri=cd["token_uri"],
                    scopes=["https://www.googleapis.com/auth/admanager"])
creds.refresh(google.auth.transport.requests.Request())


def call(url, body=None):
    req = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def run_report(name, dims, metrics):
    rep = call(f"{BASE}/reports", {
        "displayName": f"Enverus dashboard {name} {time.strftime('%Y%m%d%H%M%S')}",
        "reportDefinition": {
            "reportType": "HISTORICAL", "dimensions": dims, "metrics": metrics,
            "dateRange": {"fixed": {
                "startDate": {"year": fetch_from.year, "month": fetch_from.month, "day": fetch_from.day},
                "endDate": {"year": yesterday.year, "month": yesterday.month, "day": yesterday.day}}},
        },
    })
    op = call(f"{BASE}/reports/{rep['reportId']}:run", {})
    op_name = op["name"].replace(f"networks/{NETWORK_CODE}/", "")
    for _ in range(60):
        time.sleep(3)
        op = call(f"{BASE}/{op_name}")
        if op.get("done"):
            break
    if "error" in op:
        sys.exit(f"{name}: {op['error']}")
    url = f"https://admanager.googleapis.com/v1/{op['response']['reportResult']}:fetchRows"
    rows, token = [], None
    while True:
        q = {"pageSize": 1000}
        if token:
            q["pageToken"] = token
        resp = call(url + "?" + urllib.parse.urlencode(q))
        rows.extend(resp.get("rows", []))
        token = resp.get("nextPageToken")
        if not token:
            break
    out = []
    for r in rows:
        dv = []
        for v in r["dimensionValues"]:
            if "dateValue" in v:
                d = v["dateValue"]
                dv.append(date(d["year"], d["month"], d["day"]))
            elif "stringValue" in v:
                dv.append(v["stringValue"])
            else:
                dv.append(int(v.get("intValue", 0)))
        mv = []
        for v in r["metricValueGroups"][0]["primaryValues"]:
            mv.append(float(v["doubleValue"]) if "doubleValue" in v else int(v.get("intValue", 0)))
        if not isinstance(dv[0], date):
            ds = str(dv[0])
            dv[0] = date(int(ds[:4]), int(ds[4:6]), int(ds[6:]))
        out.append((dv, mv))
    print(f"  {name}: {len(out)} rows")
    return out


def idx(d):
    return (d - start).days


def only_order(rows):
    return [(dv[0], dv[2:], mv) for dv, mv in rows if dv[1] == ORDER_NAME]


IMP, CLK = "AD_SERVER_IMPRESSIONS", "AD_SERVER_CLICKS"
new = {}
rows = only_order(run_report("daily", ["DATE", "ORDER_NAME", "LINE_ITEM_NAME", "AD_UNIT_NAME"], [IMP, CLK]))
new["daily"] = [[idx(d), k[0], k[1], int(mv[0]), int(mv[1])] for d, k, mv in rows if mv[0] or mv[1]]
rows = only_order(run_report("device", ["DATE", "ORDER_NAME", "DEVICE_CATEGORY_NAME"], [IMP, CLK]))
new["device"] = [[idx(d), k[0], int(mv[0]), int(mv[1])] for d, k, mv in rows if mv[0] or mv[1]]
rows = only_order(run_report("creative", ["DATE", "ORDER_NAME", "CREATIVE_NAME", "AD_UNIT_NAME"], [IMP, CLK]))
new["creative"] = [[idx(d), k[0], k[1], int(mv[0]), int(mv[1])] for d, k, mv in rows if mv[0] or mv[1]]
rows = only_order(run_report("hour", ["DATE", "ORDER_NAME", "HOUR"], [IMP, CLK]))
new["hour"] = [[idx(d), int(k[0]), int(mv[0]), int(mv[1])] for d, k, mv in rows if mv[0] or mv[1]]
rows = only_order(run_report("geo", ["DATE", "ORDER_NAME", "COUNTRY_NAME", "REGION_NAME"], [IMP, CLK]))
new["geo"] = [[idx(d), k[0] or "Unknown", "" if k[1] in ("", "(Not set)", "Unknown") else k[1], int(mv[0]), int(mv[1])]
              for d, k, mv in rows if mv[0] or mv[1]]
rows = only_order(run_report("viewability", ["DATE", "ORDER_NAME", "LINE_ITEM_NAME"], [
    "ACTIVE_VIEW_VIEWABLE_IMPRESSIONS", "ACTIVE_VIEW_MEASURABLE_IMPRESSIONS", "ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME"]))
new["viewLi"] = [[idx(d), k[0], int(mv[0]), int(mv[1]), round(mv[2], 2)] for d, k, mv in rows if mv[1]]

old_daily = [r for r in D["daily"] if r[0] >= first_idx]
delta_imp, delta_clk = {}, {}
for r in new["daily"]:
    delta_imp[r[1]] = delta_imp.get(r[1], 0) + r[3]
    delta_clk[r[1]] = delta_clk.get(r[1], 0) + r[4]
for r in old_daily:
    delta_imp[r[1]] = delta_imp.get(r[1], 0) - r[3]
    delta_clk[r[1]] = delta_clk.get(r[1], 0) - r[4]

for key, rows_new in new.items():
    kept = [r for r in D[key] if r[0] < first_idx]
    D[key] = kept + sorted(rows_new, key=lambda r: (r[0], str(r[1:3])))

D["end"] = yesterday.isoformat()
D["order"]["impressionsDelivered"] += sum(delta_imp.values())
D["order"]["clicksDelivered"] += sum(delta_clk.values())
for li in D["lineItems"]:
    li["impr"] += delta_imp.get(li["name"], 0)
    li["clicks"] += delta_clk.get(li["name"], 0)
    days = {r[0]: r[3] for r in D["daily"] if r[1] == li["name"]}
    li["last7"] = [days.get(i, 0) for i in range(last_idx - 6, last_idx + 1)]

html = html[:m.start()] + "const D = " + json.dumps(D, separators=(",", ":")) + ";" + html[m.end():]
html, n1 = re.subn(r"Data through [A-Z][a-z]{2} \d{1,2}, \d{4}",
                   f"Data through {MON[yesterday.month - 1]} {yesterday.day}, {yesterday.year}", html)
html, n2 = re.subn(r"Date\.UTC\(\d{4}, \d{1,2}, \d{1,2}\) - T0\) / 864e5\) \+ 1",
                   f"Date.UTC({yesterday.year}, {yesterday.month - 1}, {yesterday.day}) - T0) / 864e5) + 1", html)
if n1 != 1 or n2 != 1:
    sys.exit(f"Expected one footer and one day-count replacement, got {n1} and {n2}")
open(dst, "w").write(html)
print(f"Wrote {dst}. Order impressions {D['order']['impressionsDelivered']:,}, clicks {D['order']['clicksDelivered']}")
