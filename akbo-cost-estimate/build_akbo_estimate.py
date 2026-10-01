"""Build AKBO_Cost_Estimate.xlsx: AKBO items priced from the NZL price list, with subtotal, freight and NZD conversion."""
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment

OUT = Path(__file__).with_name("AKBO_Cost_Estimate.xlsx")

PRICELIST = Path(__file__).with_name("Pricelist_Nozzleworks_NZL_washdown_guns.xlsx")

# (requested code, price list code, note) - price list code differs only where there is no exact match
ITEMS = [
    ("AKRSV01-B", "AKRSV01-B", ""),
    ("AKRSHHL1-BL", "AKRSHHL1-BL", ""),
    ("AKRS001-B", "AKR001-B", "Not in price list; using AKR001-B (st. st. shower head, blue)"),
    ("AKRSHHL4-BL", "AKRSHH4-BL", "Not in price list; using AKRSHH4-BL (st. st. spray head, black)"),
    ("TWRWR02M", "TWRWR02M", "Listed twice in your request"),
    ("BMFTP11-B-PRIN", "BMFTP11-B-PRIN", ""),
    ("AKMN001-B", "AKMN001-B", ""),
    ("AKNN001-B", "AKNN001-B", ""),
    ("BABTN01-B", "BABTN01-B", ""),
    ("AKRHP01-R", "AKRHP01-R", ""),
    ("AKKS003-B", "AKKS003-B", ""),
    ("AKAWLU1-B", "AKAWLU1-B", ""),
    ("AGIL572", "AGIL572", ""),
    ("BABTLF1-B-V", "BABTLF1-BL", "Not in price list; closest is BABTLF1-BL (black) - confirm blue/Viton price with AKBO"),
    ("AKWMM01", "AKWMM01", ""),
    ("WRWR02XL", "TWRWR02XL", "Assumed typo for TWRWR02XL (Twister XL)"),
    ("TWRWR02L", "TWRWR02L", ""),
    ("TWRWR02M", "TWRWR02M", "Listed twice in your request"),
    ("SWIFB13-C17", "SWIFB13-C17", ""),
    ("SWIFB19-C24", "SWIFB19-C24", ""),
    ("SWIFB19-C24-34", "SWIFB19-C24-34", ""),
]

F = "Arial"
bold = Font(name=F, bold=True)
norm = Font(name=F)
blue = Font(name=F, color="0000FF")
hdr_font = Font(name=F, bold=True, color="FFFFFF")
hdr_fill = PatternFill("solid", fgColor="1F4E78")
input_fill = PatternFill("solid", fgColor="FFFF00")
thin = Side(style="thin", color="BFBFBF")
box = Border(left=thin, right=thin, top=thin, bottom=thin)
EUR = '€#,##0.00;(€#,##0.00);"-"'
NZD = '"NZ$"#,##0.00;("NZ$"#,##0.00);"-"'

wb = Workbook()
ws = wb.active
ws.title = "AKBO Estimate"

# Copy the AKBO price list (values, cols A:E) into its own sheet so the lookups are traceable
src = load_workbook(PRICELIST, data_only=True).active
pl = wb.create_sheet("Price List")
for row in src.iter_rows(min_col=1, max_col=5):
    for c in row:
        if c.value is not None:
            pl.cell(c.row, c.column, c.value.strip() if isinstance(c.value, str) and c.column == 1 else c.value).font = norm
for col in range(3, 6):
    for c in pl.iter_cols(min_col=col, max_col=col, min_row=10):
        for cell in c:
            if isinstance(cell.value, float):
                cell.number_format = '€#,##0.00'
for col, w in zip("ABCDE", [18, 80, 14, 14, 14]):
    pl.column_dimensions[col].width = w
PL_LAST = src.max_row
PL_CODES = f"'Price List'!$A$1:$A${PL_LAST}"

ws["A1"] = "AKBO Purchase - Cost Estimate"
ws["A1"].font = Font(name=F, bold=True, size=14)
ws["A2"] = ("Unit prices are looked up from the AKBO price list valid from 15-08-2026 ('Price List' tab), "
            "< 20 pcs tier. Blue text / yellow cells are inputs.")
ws["A2"].font = Font(name=F, italic=True, size=9)

headers = ["#", "Requested Code", "Price List Code", "Description (from price list)", "Qty",
           "Unit Price (EUR, < 20 pcs)", "Line Total (EUR)", "Notes"]
HR = 4
for c, h in enumerate(headers, 1):
    cell = ws.cell(HR, c, h)
    cell.font, cell.fill, cell.border = hdr_font, hdr_fill, box
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

first = HR + 1
for i, (req, code, note) in enumerate(ITEMS):
    r = first + i
    ws.cell(r, 1, i + 1).font = norm
    ws.cell(r, 2, req).font = norm
    k = ws.cell(r, 3, code); k.font = blue; k.fill = input_fill
    match = f"MATCH(C{r},{PL_CODES},0)"
    d = ws.cell(r, 4, f'=IFERROR(TRIM(CLEAN(INDEX(\'Price List\'!$B$1:$B${PL_LAST},{match}))),"NOT IN PRICE LIST")')
    d.font = norm; d.alignment = Alignment(wrap_text=True, vertical="top")
    q = ws.cell(r, 5, 1); q.font = blue; q.fill = input_fill
    u = ws.cell(r, 6, f"=IFERROR(INDEX('Price List'!$C$1:$C${PL_LAST},{match}),0)")
    u.font = Font(name=F, color="008000"); u.number_format = EUR
    t = ws.cell(r, 7, f"=E{r}*F{r}"); t.font = norm; t.number_format = EUR
    ws.cell(r, 8, note).font = Font(name=F, italic=True, color="C00000")
    ws.cell(r, 8).alignment = Alignment(wrap_text=True, vertical="top")
    for c in range(1, 9):
        ws.cell(r, c).border = box
        if c not in (4, 8):
            ws.cell(r, c).alignment = Alignment(horizontal="center" if c in (1, 5) else None, vertical="top")
last = first + len(ITEMS) - 1

r = last + 2
def row(label, formula=None, fmt=EUR, inp=False, bold_row=False, value=None, comment=None):
    global r
    ws.cell(r, 6, label).font = bold if bold_row else norm
    ws.cell(r, 6).alignment = Alignment(horizontal="right")
    c = ws.cell(r, 7, formula if formula is not None else value)
    c.number_format = fmt
    c.font = blue if inp else (bold if bold_row else norm)
    if inp:
        c.fill = input_fill
    c.border = box
    if comment:
        c.comment = Comment(comment, "Estimate")
    r += 1
    return r - 1

row("Lines", f"=COUNTA(B{first}:B{last})", fmt="0")
row("Total qty", f"=SUM(E{first}:E{last})", fmt="0")
sub_row = row("Subtotal (EUR, ex VAT)", f"=SUM(G{first}:G{last})", bold_row=True)
frt_row = row("Freight / shipping (EUR)", inp=True, comment="Enter AKBO's freight quote to NZ, if known.")
tot_row = row("Total (EUR)", f"=G{sub_row}+G{frt_row}", bold_row=True)
r += 1
fx_row = row("Exchange rate (NZD per 1 EUR)", inp=True, fmt="0.0000",
             comment="Enter the current EUR to NZD rate (e.g. from your bank on the day of purchase).")
nzd_row = row("Total (NZD, before GST/duty)", f"=G{tot_row}*G{fx_row}", fmt=NZD, bold_row=True)
gst_row = row("NZ GST rate on import", value=0.15, inp=True, fmt="0%",
              comment="NZ GST 15% charged on import (on value + freight). Set to 0% to exclude.")
gst_amt = row("GST (NZD)", f"=G{nzd_row}*G{gst_row}", fmt=NZD)
grand = row("Estimated landed total (NZD incl GST)", f"=G{nzd_row}+G{gst_amt}", fmt=NZD, bold_row=True)
ws.cell(grand, 7).fill = PatternFill("solid", fgColor="DDEBF7")

r += 1
ws.cell(r, 1, "Notes").font = bold
for n in [
    "Source: AKBO price list for Nozzleworks NZL (washdown guns), valid from 15-08-2026. Prices in EUR per piece, < 20 pcs tier (qty 1 each).",
    "Green prices are looked up from the 'Price List' tab by Price List Code. Change a code in column C to re-price that line.",
    "Three requested codes are not in the price list and use the closest match (see Notes column). WRWR02XL is treated as TWRWR02XL.",
    "TWRWR02M appears twice in the original list, so it is included twice. Delete one row if that was unintended.",
    "Customs duty, import fees and brokerage are not included.",
]:
    r += 1
    ws.cell(r, 1, "- " + n).font = Font(name=F, size=9)

for col, w in zip("ABCDEFGH", [5, 17, 17, 55, 6, 20, 18, 40]):
    ws.column_dimensions[col].width = w
ws.row_dimensions[HR].height = 30
ws.freeze_panes = ws.cell(first, 1)
ws.page_setup.orientation = "landscape"
ws.page_setup.fitToWidth = 1
ws.sheet_properties.pageSetUpPr.fitToPage = True

wb.calculation.fullCalcOnLoad = True  # no cached values from openpyxl; Excel computes on open
wb.save(OUT)
print(OUT)
