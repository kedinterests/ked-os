#!/usr/bin/env python3
"""Pull live basin data for the bakkenshale.com mockup and write data.json.

Sources (all public, no account needed):
  - FRED: WTI spot (DCOILWTICO) and Henry Hub spot (DHHNGSP), daily
  - EIA API v2 (DEMO_KEY): North Dakota field production of crude oil, monthly
  - NDIC Department of Mineral Resources: active drilling rig list, updated daily

Run:  python3 refresh-data.py
For production, swap DEMO_KEY for the real EIA key (Keeper: "EIA API Key") via the
EIA_API_KEY env var; DEMO_KEY is rate-limited.
"""
import collections, csv, datetime, html, io, json, os, re, urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (bakkenshale.com data refresh)"}
OUT = Path(__file__).with_name("data.json")

# NDIC county codes on the rig list -> county slug used on the site
NDIC_COUNTY = {
    "BIL": "Billings", "BOT": "Bottineau", "BOW": "Bowman", "BRK": "Burke", "DIV": "Divide",
    "DUN": "Dunn", "GV": "Golden Valley", "MCH": "McHenry", "MCK": "McKenzie", "MCL": "McLean",
    "MTL": "Mountrail", "REN": "Renville", "SLP": "Slope", "STK": "Stark", "WRD": "Ward",
    "WIL": "Williams",
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def fred(series):
    start = (datetime.date.today() - datetime.timedelta(days=45)).isoformat()
    rows = list(csv.reader(io.StringIO(get(
        f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}&cosd={start}").decode())))
    pts = [(d, float(v)) for d, v in rows[1:] if v not in (".", "")]
    (d0, v0), (d1, v1) = pts[-2], pts[-1]
    return {"date": d1, "value": v1, "change": round(v1 - v0, 2),
            "series": [v for _, v in pts[-30:]]}


def eia_nd_crude():
    key = os.environ.get("EIA_API_KEY", "DEMO_KEY")
    url = ("https://api.eia.gov/v2/petroleum/crd/crpdn/data/?api_key=" + key +
           "&frequency=monthly&data%5B0%5D=value&facets%5Bduoarea%5D%5B%5D=SND"
           "&facets%5Bseries%5D%5B%5D=MCRFPND2"
           "&sort%5B0%5D%5Bcolumn%5D=period&sort%5B0%5D%5Bdirection%5D=desc&length=2")
    data = json.loads(get(url))["response"]["data"]
    cur, prev = data[0], data[1]
    return {"period": cur["period"], "bbl_d": int(float(cur["value"]) * 1000),
            "change": int((float(cur["value"]) - float(prev["value"])) * 1000)}


def ndic_rigs():
    s = get("https://www.dmr.nd.gov/oilgas/riglist.asp").decode("latin-1")
    rigs = []
    for row in re.findall(r"<tr.*?</tr>", s, re.I | re.S):
        c = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip()
             for x in re.findall(r"<td.*?</td>", row, re.I | re.S)]
        if len(c) == 9 and re.match(r"\d{4}-\d\d-\d\d", c[7]):
            rigs.append({"rig": c[0], "operator": c[1], "well": c[2], "county": c[4], "spud": c[7]})
    by_county = collections.Counter(NDIC_COUNTY.get(r["county"], r["county"]) for r in rigs)
    by_op = collections.Counter(r["operator"] for r in rigs)
    return {"date": datetime.date.today().isoformat(), "count": len(rigs),
            "by_county": dict(by_county), "by_operator": by_op.most_common(8),
            "latest": sorted(rigs, key=lambda r: r["spud"], reverse=True)[:5]}


def main():
    data = {"fetched": datetime.datetime.now().isoformat(timespec="minutes")}
    for name, fn in [("wti", lambda: fred("DCOILWTICO")), ("henry_hub", lambda: fred("DHHNGSP")),
                     ("nd_crude", eia_nd_crude), ("rigs", ndic_rigs)]:
        try:
            data[name] = fn()
        except Exception as e:  # keep the last good value on the page if one source is down
            print(f"{name}: failed ({e})")
    OUT.write_text(json.dumps(data, indent=2))
    print(f"wrote {OUT.name}: " + ", ".join(k for k in data if k != "fetched"))


if __name__ == "__main__":
    main()
