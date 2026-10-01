#!/usr/bin/env python3
"""Generate a polished PDF report for Enverus from GAM data."""

import json, os, time, urllib.request, urllib.parse
import google.auth.transport.requests
from google.oauth2.credentials import Credentials

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "secrets", "gam-credentials.json")
NETWORK_CODE = "6933594"
ORDER_NAME = "MRF Enverus 2026/06"
BASE = f"https://admanager.googleapis.com/v1/networks/{NETWORK_CODE}"

with open(CREDENTIALS_FILE) as f:
    cred_data = json.load(f)

creds = Credentials(
    token=None,
    refresh_token=cred_data["refresh_token"],
    client_id=cred_data["client_id"],
    client_secret=cred_data["client_secret"],
    token_uri=cred_data["token_uri"],
    scopes=["https://www.googleapis.com/auth/admanager"],
)
creds.refresh(google.auth.transport.requests.Request())

def get(url):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {creds.token}"})
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def post(path, body={}):
    url = f"{BASE}/{path}"
    payload = json.dumps(body).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# --- Create and run report ---
print("Creating report...")
report = post("reports", {
    "displayName": f"Enverus All-Time - {time.strftime('%Y%m%d%H%M%S')}",
    "reportDefinition": {
        "reportType": "HISTORICAL",
        "dimensions": ["DATE", "ORDER_NAME", "LINE_ITEM_NAME", "AD_UNIT_NAME"],
        "metrics": ["AD_SERVER_IMPRESSIONS", "AD_SERVER_CLICKS", "AD_SERVER_CTR"],
        "dateRange": {
            "fixed": {
                "startDate": {"year": 2026, "month": 6, "day": 1},
                "endDate": {"year": 2026, "month": 6, "day": 30},
            }
        },
    },
})
report_id = report["reportId"]
print(f"Report ID: {report_id}")

run_op = post(f"reports/{report_id}:run", {})
op_name = run_op["name"].replace(f"networks/{NETWORK_CODE}/", "")

print("Waiting for results...")
for _ in range(30):
    time.sleep(3)
    op = get(f"{BASE}/{op_name}")
    if op.get("done"):
        break

result_path = op["response"]["reportResult"]
fetch_url = f"https://admanager.googleapis.com/v1/{result_path}:fetchRows"

# Paginate through all rows
all_rows = []
page_token = None
while True:
    url = fetch_url + ("?" + urllib.parse.urlencode({"pageSize": 1000, "pageToken": page_token}) if page_token else "?pageSize=1000")
    resp = get(url)
    all_rows.extend(resp.get("rows", []))
    page_token = resp.get("nextPageToken")
    if not page_token:
        break

print(f"Total rows: {len(all_rows)}")

# --- Filter for Enverus ---
def row_val(row, idx):
    dv = row["dimensionValues"][idx]
    return dv.get("stringValue") or str(dv.get("intValue", ""))

def metric_val(row, idx):
    v = row["metricValueGroups"][0]["primaryValues"][idx]
    return v.get("intValue") or v.get("doubleValue") or 0

enverus_rows = [r for r in all_rows if row_val(r, 1) == ORDER_NAME]
print(f"Enverus rows: {len(enverus_rows)}")

# Aggregate by date
from collections import defaultdict
by_date = defaultdict(lambda: {"impressions": 0, "clicks": 0})
ad_units = set()
line_items = set()

for row in enverus_rows:
    date_raw = row_val(row, 0)
    date_str = f"{date_raw[:4]}-{date_raw[4:6]}-{date_raw[6:]}"
    impr = int(metric_val(row, 0))
    clicks = int(metric_val(row, 1))
    by_date[date_str]["impressions"] += impr
    by_date[date_str]["clicks"] += clicks
    ad_units.add(row_val(row, 3))
    line_items.add(row_val(row, 2))

total_impressions = sum(v["impressions"] for v in by_date.values())
total_clicks = sum(v["clicks"] for v in by_date.values())
overall_ctr = (total_clicks / total_impressions * 100) if total_impressions else 0

print(f"Total impressions: {total_impressions:,}")
print(f"Total clicks: {total_clicks:,}")
print(f"Overall CTR: {overall_ctr:.4f}%")
print(f"Ad units: {ad_units}")
print(f"Line items: {line_items}")

# --- Build PDF ---
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics import renderPDF
except ImportError:
    print("Installing reportlab...")
    import subprocess
    subprocess.run(["pip3", "install", "--break-system-packages", "reportlab"], check=True)
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics import renderPDF

OUT = os.path.join(os.path.dirname(__file__), "..", "Enverus-Ad-Performance-Report.pdf")

# Color palette
NAVY = colors.HexColor("#0D1B2A")
TEAL = colors.HexColor("#00B4D8")
LIGHT_TEAL = colors.HexColor("#90E0EF")
GOLD = colors.HexColor("#F4A261")
OFF_WHITE = colors.HexColor("#F8F9FA")
LIGHT_GRAY = colors.HexColor("#E9ECEF")
MID_GRAY = colors.HexColor("#6C757D")

doc = SimpleDocTemplate(
    OUT,
    pagesize=letter,
    leftMargin=0.75*inch,
    rightMargin=0.75*inch,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch,
)

WIDTH = letter[0] - 1.5*inch

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle("title", fontSize=28, textColor=colors.white,
    fontName="Helvetica-Bold", alignment=TA_LEFT, leading=34)
SUBTITLE_STYLE = ParagraphStyle("subtitle", fontSize=13, textColor=LIGHT_TEAL,
    fontName="Helvetica", alignment=TA_LEFT, leading=18)
SECTION_HEADER = ParagraphStyle("section", fontSize=13, textColor=NAVY,
    fontName="Helvetica-Bold", alignment=TA_LEFT, leading=16, spaceBefore=16, spaceAfter=8)
BODY = ParagraphStyle("body", fontSize=10, textColor=colors.HexColor("#333333"),
    fontName="Helvetica", leading=14)
CAPTION = ParagraphStyle("caption", fontSize=8, textColor=MID_GRAY,
    fontName="Helvetica", alignment=TA_CENTER)
METRIC_LABEL = ParagraphStyle("metric_label", fontSize=9, textColor=MID_GRAY,
    fontName="Helvetica", alignment=TA_CENTER, leading=12)
METRIC_VALUE = ParagraphStyle("metric_value", fontSize=26, textColor=NAVY,
    fontName="Helvetica-Bold", alignment=TA_CENTER, leading=30)
METRIC_SUB = ParagraphStyle("metric_sub", fontSize=9, textColor=TEAL,
    fontName="Helvetica-Bold", alignment=TA_CENTER)

story = []

# --- Hero Header ---
def make_header():
    header_data = [[
        Paragraph("Enverus", TITLE_STYLE),
        Paragraph("Advertising Performance Report", SUBTITLE_STYLE),
    ]]
    t = Table(header_data, colWidths=[WIDTH*0.4, WIDTH*0.6])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 22),
        ("BOTTOMPADDING", (0,0), (-1,-1), 22),
        ("LEFTPADDING", (0,0), (0,0), 22),
        ("RIGHTPADDING", (-1,-1), (-1,-1), 22),
    ]))
    return t

story.append(make_header())
story.append(Spacer(1, 14))

# --- Campaign Meta ---
dates = sorted(by_date.keys())
date_from = dates[0] if dates else "—"
date_to = dates[-1] if dates else "—"

meta_items = [
    ["Campaign", ORDER_NAME],
    ["Advertiser", "Enverus"],
    ["Line Item", " / ".join(sorted(line_items))],
    ["Period", f"{date_from}  to  {date_to}"],
    ["Ad Units", len(ad_units)],
]
meta_table = Table(meta_items, colWidths=[1.3*inch, WIDTH - 1.3*inch])
meta_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,-1), LIGHT_GRAY),
    ("BACKGROUND", (1,0), (1,-1), OFF_WHITE),
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("TEXTCOLOR", (0,0), (0,-1), NAVY),
    ("TEXTCOLOR", (1,0), (1,-1), colors.HexColor("#333333")),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 10),
    ("GRID", (0,0), (-1,-1), 0.5, LIGHT_GRAY),
    ("ROWBACKGROUNDS", (0,0), (-1,-1), [OFF_WHITE, colors.white]),
]))
story.append(meta_table)
story.append(Spacer(1, 18))

# --- KPI Cards ---
story.append(Paragraph("Campaign Performance", SECTION_HEADER))

def kpi_card(label, value, sub=None):
    inner = [
        [Paragraph(label, METRIC_LABEL)],
        [Paragraph(value, METRIC_VALUE)],
    ]
    if sub:
        inner.append([Paragraph(sub, METRIC_SUB)])
    t = Table(inner, colWidths=[WIDTH/3 - 8])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.white),
        ("BOX", (0,0), (-1,-1), 1.5, TEAL),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))
    return t

kpi_row = [[
    kpi_card("Total Impressions", f"{total_impressions:,}", "ad views delivered"),
    kpi_card("Total Clicks", f"{total_clicks:,}", "audience engagements"),
    kpi_card("Click-Through Rate", f"{overall_ctr:.3f}%", "industry avg ~0.035%"),
]]
kpi_table = Table(kpi_row, colWidths=[WIDTH/3]*3, hAlign="LEFT")
kpi_table.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 4),
    ("RIGHTPADDING", (0,0), (-1,-1), 4),
]))
story.append(kpi_table)
story.append(Spacer(1, 18))

# --- Impressions Bar Chart ---
if dates:
    story.append(Paragraph("Daily Impressions", SECTION_HEADER))

    chart_w = WIDTH
    chart_h = 2.2*inch
    drawing = Drawing(chart_w, chart_h + 30)

    bc = VerticalBarChart()
    bc.x = 40
    bc.y = 30
    bc.width = chart_w - 60
    bc.height = chart_h - 10
    bc.data = [[by_date[d]["impressions"] for d in dates]]
    bc.bars[0].fillColor = TEAL
    bc.bars[0].strokeColor = None
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = max((by_date[d]["impressions"] for d in dates), default=1) * 1.2
    bc.valueAxis.labelTextFormat = lambda v: f"{int(v):,}"
    bc.valueAxis.labels.fontSize = 7
    bc.categoryAxis.categoryNames = [d[5:] for d in dates]
    bc.categoryAxis.labels.angle = 45
    bc.categoryAxis.labels.fontSize = 7
    bc.categoryAxis.labels.dy = -6
    bc.groupSpacing = 3

    drawing.add(bc)
    story.append(drawing)
    story.append(Paragraph("Impression count by day. Campaign launched June 12, 2026.", CAPTION))
    story.append(Spacer(1, 14))

# --- Daily Breakdown Table ---
story.append(Paragraph("Daily Breakdown", SECTION_HEADER))

table_data = [["Date", "Impressions", "Clicks", "CTR"]]
for d in dates:
    row_impr = by_date[d]["impressions"]
    row_clicks = by_date[d]["clicks"]
    row_ctr = (row_clicks / row_impr * 100) if row_impr else 0
    table_data.append([
        d,
        f"{row_impr:,}",
        f"{row_clicks:,}",
        f"{row_ctr:.4f}%",
    ])

# Totals row
table_data.append(["TOTAL", f"{total_impressions:,}", f"{total_clicks:,}", f"{overall_ctr:.4f}%"])

col_widths = [1.5*inch, (WIDTH-1.5*inch)/3, (WIDTH-1.5*inch)/3, (WIDTH-1.5*inch)/3]
dt = Table(table_data, colWidths=col_widths)
dt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ALIGN", (1,0), (-1,-1), "RIGHT"),
    ("ALIGN", (0,0), (0,-1), "LEFT"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("ROWBACKGROUNDS", (0,1), (-1,-2), [colors.white, OFF_WHITE]),
    ("BACKGROUND", (0,-1), (-1,-1), LIGHT_GRAY),
    ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
    ("TEXTCOLOR", (0,-1), (-1,-1), NAVY),
    ("LINEBELOW", (0,-1), (-1,-1), 1.5, TEAL),
    ("LINEABOVE", (0,-1), (-1,-1), 1, LIGHT_GRAY),
    ("GRID", (0,0), (-1,-1), 0.25, LIGHT_GRAY),
]))
story.append(dt)
story.append(Spacer(1, 18))

# --- Ad Units ---
story.append(Paragraph("Ad Placements Active", SECTION_HEADER))
by_unit = defaultdict(lambda: {"impressions": 0, "clicks": 0})
for row in enverus_rows:
    unit = row_val(row, 3)
    by_unit[unit]["impressions"] += int(metric_val(row, 0))
    by_unit[unit]["clicks"] += int(metric_val(row, 1))

unit_data = [["Ad Unit", "Impressions", "Clicks", "CTR"]]
for unit, vals in sorted(by_unit.items(), key=lambda x: -x[1]["impressions"]):
    ctr = (vals["clicks"] / vals["impressions"] * 100) if vals["impressions"] else 0
    unit_data.append([unit, f"{vals['impressions']:,}", f"{vals['clicks']:,}", f"{ctr:.4f}%"])

ut = Table(unit_data, colWidths=col_widths)
ut.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), NAVY),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ALIGN", (1,0), (-1,-1), "RIGHT"),
    ("ALIGN", (0,0), (0,-1), "LEFT"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, OFF_WHITE]),
    ("GRID", (0,0), (-1,-1), 0.25, LIGHT_GRAY),
]))
story.append(ut)
story.append(Spacer(1, 22))

# --- Footer ---
story.append(HRFlowable(width=WIDTH, thickness=1, color=TEAL))
story.append(Spacer(1, 6))
footer_data = [[
    Paragraph("Mineral Rights Forum — KED Interests, LLC", ParagraphStyle("fl", fontSize=8, textColor=MID_GRAY, fontName="Helvetica")),
    Paragraph(f"Generated {time.strftime('%B %d, %Y')}  |  Data: Google Ad Manager", ParagraphStyle("fr", fontSize=8, textColor=MID_GRAY, fontName="Helvetica", alignment=TA_RIGHT)),
]]
ft = Table(footer_data, colWidths=[WIDTH/2, WIDTH/2])
ft.setStyle(TableStyle([("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 0)]))
story.append(ft)

doc.build(story)
print(f"\nPDF saved: {os.path.abspath(OUT)}")
