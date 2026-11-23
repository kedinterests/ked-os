#!/usr/bin/env python3
"""Pull live basin data for the eaglefordshale.com mockup and write data.json.

Sources (all public, no account needed):
  - FRED: WTI spot (DCOILWTICO) and Henry Hub spot (DHHNGSP), daily
  - EIA API v2, STEO: Eagle Ford region crude oil (COPREF) and natural gas (NGMPEF), monthly
  - EIA API v2: Texas field production of crude oil (MCRFPTX2), monthly
  - Baker Hughes weekly rig count, Eagle Ford basin: entered by hand in data.json under
    "manual" (Baker Hughes blocks scripted downloads; the weekly file is at
    https://rigcount.bakerhughes.com/na-rig-count, sheet "NAM Summary", Major Basin Variances).
    This script keeps whatever is already there.

Run:  python3 refresh-data.py
For production, set EIA_API_KEY to the real EIA key (Keeper: "EIA API Key"); DEMO_KEY is rate-limited.
"""
import csv, datetime, io, json, os, urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (eaglefordshale.com data refresh)"}
OUT = Path(__file__).with_name("data.json")
KEY = os.environ.get("EIA_API_KEY", "DEMO_KEY")


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def fred(series):
    start = (datetime.date.today() - datetime.timedelta(days=45)).isoformat()
    rows = list(csv.reader(io.StringIO(get(
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}&cosd={start}").decode())))
    pts = [(d, float(v)) for d, v in rows[1:] if v not in (".", "")]
    (d0, v0), (d1, v1) = pts[-2], pts[-1]
    return {"date": d1, "value": v1, "change": round(v1 - v0, 2)}


def steo(series):
    # STEO runs as a forecast past today; take the latest month before the current one (an EIA estimate)
    url = (f"https://api.eia.gov/v2/steo/data/?api_key={KEY}&frequency=monthly&data%5B0%5D=value"
           f"&facets%5BseriesId%5D%5B%5D={series}&sort%5B0%5D%5Bcolumn%5D=period"
           f"&sort%5B0%5D%5Bdirection%5D=desc&length=40")
    this_month = datetime.date.today().strftime("%Y-%m")
    rows = [r for r in json.loads(get(url))["response"]["data"] if r["period"] < this_month]
    cur, year_ago = rows[0], rows[12]
    return {"period": cur["period"], "value": float(cur["value"]), "units": cur.get("unit"),
            "year_ago": float(year_ago["value"])}


def eia_tx_crude():
    url = (f"https://api.eia.gov/v2/petroleum/crd/crpdn/data/?api_key={KEY}&frequency=monthly"
           "&data%5B0%5D=value&facets%5Bseries%5D%5B%5D=MCRFPTX2"
           "&sort%5B0%5D%5Bcolumn%5D=period&sort%5B0%5D%5Bdirection%5D=desc&length=2")
    cur, prev = json.loads(get(url))["response"]["data"][:2]
    return {"period": cur["period"], "bbl_d": int(float(cur["value"]) * 1000),
            "change": int((float(cur["value"]) - float(prev["value"])) * 1000)}


def main():
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    data = {"fetched": datetime.datetime.now().isoformat(timespec="minutes"),
            "manual": old.get("manual", {})}
    for name, fn in [("wti", lambda: fred("DCOILWTICO")), ("henry_hub", lambda: fred("DHHNGSP")),
                     ("ef_oil", lambda: steo("COPREF")), ("ef_gas", lambda: steo("NGMPEF")),
                     ("tx_crude", eia_tx_crude)]:
        try:
            data[name] = fn()
        except Exception as e:  # keep the last good value if one source is down
            print(f"{name}: failed ({e})")
            if name in old:
                data[name] = old[name]
    OUT.write_text(json.dumps(data, indent=2))
    print(f"wrote {OUT.name}: " + ", ".join(k for k in data if k != "fetched"))


if __name__ == "__main__":
    main()
