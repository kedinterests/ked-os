#!/usr/bin/env python3
"""Export YTD advertiser performance to a polished PDF matching the dashboard view."""

import json, os, time
from collections import defaultdict
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

with open('secrets/ytd-report-raw.json') as f:
    data = json.load(f)

MONTH_MAP = {
    '1512': 'Jan', '1513': 'Feb', '1514': 'Mar',
    '1515': 'Apr', '1516': 'May', '1517': 'Jun',
}
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

by_adv = defaultdict(lambda: defaultdict(lambda: [0, 0]))
for row in data.get('rows', []):
    dv = row['dimensionValues']
    mv = row['metricValueGroups'][0]['primaryValues']
    month = MONTH_MAP.get(str(dv[0].get('intValue', '')), '')
    adv = dv[1].get('stringValue', '')
    imp = int(mv[0].get('intValue', 0))
    clicks = int(mv[1].get('intValue', 0))
    by_adv[adv][month][0] += imp
    by_adv[adv][month][1] += clicks

ADVERTISERS = sorted(by_adv.keys())

OUT = 'KED-YTD-Ad-Performance-2026.pdf'

NAVY      = colors.HexColor('#0D1B2A')
TEAL      = colors.HexColor('#00B4D8')
LIGHT_TEAL= colors.HexColor('#D0EEF5')
OFF_WHITE = colors.HexColor('#F8F9FA')
ALT_ROW   = colors.HexColor('#EEF6F9')
MID_GRAY  = colors.HexColor('#6C757D')
LIGHT_GRAY= colors.HexColor('#DEE2E6')

doc = SimpleDocTemplate(
    OUT,
    pagesize=landscape(letter),
    leftMargin=0.6*inch, rightMargin=0.6*inch,
    topMargin=0.6*inch, bottomMargin=0.6*inch,
)
W = landscape(letter)[0] - 1.2*inch

LABEL = ParagraphStyle('label', fontSize=9, fontName='Helvetica-Bold',
    textColor=colors.white, alignment=TA_LEFT)
SUBLABEL = ParagraphStyle('sub', fontSize=8, fontName='Helvetica',
    textColor=LIGHT_TEAL, alignment=TA_LEFT)
CAPTION = ParagraphStyle('cap', fontSize=8, fontName='Helvetica',
    textColor=MID_GRAY, alignment=TA_LEFT)
TH = ParagraphStyle('th', fontSize=8, fontName='Helvetica-Bold',
    textColor=colors.white, alignment=TA_CENTER)
TD_ADV = ParagraphStyle('td_adv', fontSize=8, fontName='Helvetica-Bold',
    textColor=NAVY, alignment=TA_LEFT)
TD_IMP = ParagraphStyle('td_imp', fontSize=8, fontName='Helvetica-Bold',
    textColor=NAVY, alignment=TA_RIGHT)
TD_SUB = ParagraphStyle('td_sub', fontSize=7, fontName='Helvetica',
    textColor=MID_GRAY, alignment=TA_RIGHT)
TD_TOTAL_IMP = ParagraphStyle('td_tot_imp', fontSize=8, fontName='Helvetica-Bold',
    textColor=NAVY, alignment=TA_RIGHT)

def cell(imp, clicks):
    if not imp:
        return Paragraph('<font color="#BBBBBB">—</font>', TD_IMP)
    ctr = clicks / imp * 100
    return [
        Paragraph(f'{imp:,}', TD_IMP),
        Paragraph(f'{clicks} / {ctr:.3f}%', TD_SUB),
    ]

story = []

# Header
header_table = Table([[
    Paragraph('KED Interests, LLC.', LABEL),
    Paragraph('Year-to-date ad performance  ·  Jan – Jun 2026', SUBLABEL),
]], colWidths=[W*0.3, W*0.7])
header_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), NAVY),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ('LEFTPADDING', (0,0), (0,0), 16),
]))
story.append(header_table)
story.append(Spacer(1, 10))

# Build data table
# Columns: Advertiser | Jan | Feb | Mar | Apr | May | Jun* | Total
# Each month cell: impressions on top, "clicks / CTR%" below

header_row = [
    Paragraph('Advertiser', TH),
    Paragraph('Jan', TH),
    Paragraph('Feb', TH),
    Paragraph('Mar', TH),
    Paragraph('Apr', TH),
    Paragraph('May', TH),
    Paragraph('Jun*', TH),
    Paragraph('Total', TH),
]

ADV_W = 1.6*inch
MONTH_W = (W - ADV_W - 0.1*inch) / 7
col_widths = [ADV_W] + [MONTH_W]*6 + [MONTH_W + 0.1*inch]

table_data = [header_row]
total_by_month = defaultdict(lambda: [0, 0])
grand = [0, 0]

for adv in ADVERTISERS:
    row = [Paragraph(adv, TD_ADV)]
    adv_imp = adv_clicks = 0
    for m in MONTHS:
        imp, clicks = by_adv[adv][m]
        adv_imp += imp
        adv_clicks += clicks
        total_by_month[m][0] += imp
        total_by_month[m][1] += clicks
        row.append(cell(imp, clicks))
    grand[0] += adv_imp
    grand[1] += adv_clicks
    total_ctr = adv_clicks / adv_imp * 100 if adv_imp else 0
    row.append([
        Paragraph(f'{adv_imp:,}', TD_TOTAL_IMP),
        Paragraph(f'{adv_clicks} / {total_ctr:.3f}%', TD_SUB),
    ])
    table_data.append(row)

# Totals row
totals_row = [Paragraph('All advertisers', ParagraphStyle('tot', fontSize=8,
    fontName='Helvetica-Bold', textColor=NAVY, alignment=TA_LEFT))]
for m in MONTHS:
    imp, clicks = total_by_month[m]
    totals_row.append(cell(imp, clicks))
grand_ctr = grand[1] / grand[0] * 100 if grand[0] else 0
totals_row.append([
    Paragraph(f'{grand[0]:,}', TD_TOTAL_IMP),
    Paragraph(f'{grand[1]} / {grand_ctr:.3f}%', TD_SUB),
])
table_data.append(totals_row)

n_data = len(table_data)
n_adv  = n_data - 2  # rows excluding header and totals

row_styles = []
for i in range(1, n_data - 1):
    bg = OFF_WHITE if i % 2 == 1 else ALT_ROW
    row_styles.append(('BACKGROUND', (0, i), (-1, i), bg))

t = Table(table_data, colWidths=col_widths, repeatRows=1)
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY),
    ('ROWBACKGROUNDS', (0, 1), (-1, n_data-2), [OFF_WHITE, ALT_ROW]),
    ('BACKGROUND', (0, n_data-1), (-1, n_data-1), LIGHT_TEAL),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('LINEBELOW', (0, 0), (-1, 0), 1, TEAL),
    ('LINEBELOW', (0, 1), (-1, n_data-2), 0.25, LIGHT_GRAY),
    ('LINEABOVE', (0, n_data-1), (-1, n_data-1), 0.75, TEAL),
    ('BOX', (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
    ('LINEAFTER', (0, 0), (0, -1), 0.5, LIGHT_GRAY),
    ('LINEBEFORE', (-1, 0), (-1, -1), 0.75, TEAL),
]))
story.append(t)
story.append(Spacer(1, 8))

# Footer
story.append(HRFlowable(width=W, thickness=0.5, color=TEAL))
story.append(Spacer(1, 4))
footer = Table([[
    Paragraph('Each month: impressions  ·  clicks / CTR%.   * Jun = partial month (through Jun 17).', CAPTION),
    Paragraph(f'Generated {time.strftime("%B %d, %Y")}  ·  Data: Google Ad Manager', ParagraphStyle(
        'fr', fontSize=8, fontName='Helvetica', textColor=MID_GRAY, alignment=TA_RIGHT)),
]], colWidths=[W*0.6, W*0.4])
footer.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)]))
story.append(footer)

doc.build(story)
print(f'PDF saved: {os.path.abspath(OUT)}')
