import json, os, sys, time, urllib.request, urllib.parse, urllib.error
import google.auth.transport.requests
from google.oauth2.credentials import Credentials

ROOT = "/Users/chrismalone/os-systems/ked-os"
NETWORK_CODE = "6933594"
BASE = f"https://admanager.googleapis.com/v1/networks/{NETWORK_CODE}"
cred = json.load(open(f"{ROOT}/secrets/gam-credentials.json"))
creds = Credentials(token=None, refresh_token=cred["refresh_token"], client_id=cred["client_id"],
    client_secret=cred["client_secret"], token_uri=cred["token_uri"],
    scopes=["https://www.googleapis.com/auth/admanager"])
creds.refresh(google.auth.transport.requests.Request())

def get(url, params=None):
    if not url.startswith("http"): url = f"{BASE}/{url}"
    if params: url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {creds.token}"})
    with urllib.request.urlopen(req) as r: return json.loads(r.read())

def post(path, body):
    req = urllib.request.Request(f"{BASE}/{path}", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:1500]); raise

def run_report(name, dims, metrics, start, end, filters=None):
    body = {"displayName": name, "reportDefinition": {"reportType": "HISTORICAL",
        "dimensions": dims, "metrics": metrics,
        "dateRange": {"fixed": {"startDate": start, "endDate": end}}}}
    if filters: body["reportDefinition"]["filters"] = filters
    rep = post("reports", body)
    rid = rep["reportId"]
    op = post(f"reports/{rid}:run", {})
    op_name = op["name"].replace(f"networks/{NETWORK_CODE}/", "")
    for _ in range(40):
        time.sleep(3); o = get(op_name)
        if o.get("done"): break
    if "error" in o: print("REPORT ERROR", json.dumps(o["error"])[:1500]); return None
    result_path = o["response"]["reportResult"]
    rows, tok = [], None
    while True:
        p = {"pageSize": 1000}
        if tok: p["pageToken"] = tok
        r = get(f"https://admanager.googleapis.com/v1/{result_path}:fetchRows", p)
        rows += r.get("rows", []); tok = r.get("nextPageToken")
        if not tok: break
    return rows

start = {"year": 2026, "month": 6, "day": 1}
end = {"year": 2026, "month": 9, "day": 24}
out = {}

# Order + line items + creatives metadata
orders = get("orders", {"filter": "displayName:Enverus"})
out["orders"] = orders
oid = orders["orders"][0]["name"]
print("order:", oid, orders["orders"][0].get("displayName"))
out["lineItems"] = get("lineItems", {"filter": f'order="{oid}"'})
print("line items:", [li.get("displayName") for li in out["lineItems"].get("lineItems", [])])

mode = sys.argv[1] if len(sys.argv) > 1 else "all"
filt = [{"fieldFilter": {"field": {"dimension": "ORDER_NAME"}, "operation": "IN", "values": [{"stringValue": "MRF Enverus 2026/06"}]}}]

tries = {
 "daily": (["DATE","LINE_ITEM_NAME","AD_UNIT_NAME"],
           ["AD_SERVER_IMPRESSIONS","AD_SERVER_CLICKS","AD_SERVER_CTR"]),
 "device": (["DATE","DEVICE_CATEGORY_NAME"],
           ["AD_SERVER_IMPRESSIONS","AD_SERVER_CLICKS","AD_SERVER_CTR"]),
 "creative": (["CREATIVE_NAME","CREATIVE_SIZE" if False else "LINE_ITEM_NAME"],
           ["AD_SERVER_IMPRESSIONS","AD_SERVER_CLICKS","AD_SERVER_CTR"]),
 "viewability": (["DATE"],
           ["AD_SERVER_IMPRESSIONS","ACTIVE_VIEW_VIEWABLE_IMPRESSIONS","ACTIVE_VIEW_MEASURABLE_IMPRESSIONS","ACTIVE_VIEW_VIEWABLE_IMPRESSIONS_RATE","ACTIVE_VIEW_AVERAGE_VIEWABLE_TIME"]),
 "geo": (["COUNTRY_NAME","REGION_NAME"],
           ["AD_SERVER_IMPRESSIONS","AD_SERVER_CLICKS"]),
 "hour": (["HOUR"],
           ["AD_SERVER_IMPRESSIONS","AD_SERVER_CLICKS"]),
 "dow": (["DAY_OF_WEEK"],
           ["AD_SERVER_IMPRESSIONS","AD_SERVER_CLICKS"]),
}
for k,(d,m) in tries.items():
    if mode not in ("all", k): continue
    print("==", k, flush=True)
    try:
        rows = run_report(f"Enverus dash {k}", d, m, start, end, filt)
        print("  rows:", None if rows is None else len(rows))
        out[k] = {"dims": d, "metrics": m, "rows": rows}
    except Exception as e:
        print("  FAILED", k, str(e)[:300])
        out[k] = {"dims": d, "metrics": m, "error": str(e)[:500]}

json.dump(out, open(f"{ROOT}/secrets/enverus-dashboard-raw.json","w"), indent=1)
print("saved")
