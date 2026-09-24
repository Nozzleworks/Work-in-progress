"""Generate Quote_Template.xlsx — Nozzleworks quote laid out like Quote_template_r1.docx.

Sub-totals, GST and Total are formulas driven by Qty and Unit Price.
"""
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.drawing.image import Image
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.worksheet.datavalidation import DataValidation

FONT = "Calibri"
DARK, GREY, HDRFILL, RULECLR, WHITE = "404040", "666666", "4A4A4A", "CCCCCC", "FFFFFF"
RULE = Border(top=Side(style="thin", color=RULECLR))
MONEY = '#,##0.00;(#,##0.00);""'
NZD = '"NZD"#,##0.00'
DATE = "d mmm yyyy"

N_ITEMS = 10
ITEM_HDR = 13          # line-item header row
FIRST = ITEM_HDR + 1   # first item's data row; each item = data, description, spacer
ITEM_ROWS = [FIRST + 3 * i for i in range(N_ITEMS)]
LAST = ITEM_ROWS[-1] + 1

wb = Workbook()
ws = wb.active
ws.title = "Quote"
ws.sheet_view.showGridLines = False
# Column widths follow the Word line-item table [441, 4272, 818, 1468, 1469, 1278] DXA
for col, w in zip("ABCDEF", [4.5, 42, 8, 14, 14, 13]):
    ws.column_dimensions[col].width = w
ws.column_dimensions["G"].width = 4
ws.column_dimensions["H"].width = 16
ws.column_dimensions["I"].width = 12


def put(ref, value=None, size=9, color=GREY, bold=False, fmt=None, h="left", v="center", wrap=False):
    c = ws[ref]
    c.value = value
    c.font = Font(name=FONT, size=size, color=color, bold=bold)
    c.alignment = Alignment(horizontal=h, vertical=v, wrap_text=wrap)
    if fmt:
        c.number_format = fmt
    return c


# ---- Settings (outside the print area) ----
put("H1", "Settings", size=10, color=DARK, bold=True)
put("H2", "GST rate"); put("I2", 0.15, color="0000FF", fmt="0%")
put("H3", "Validity (days)"); put("I3", 30, color="0000FF")
ws["I2"].comment = Comment("NZ GST 15% (Inland Revenue).", "Template")
put("H5", "Edit: quote no., quote date, customer,", size=8, color="7F7F7F")
put("H6", "subject, part no., description, qty,", size=8, color="7F7F7F")
put("H7", "UoM, unit price, notes and terms.", size=8, color="7F7F7F")
put("H8", "#, sub-totals, GST, total and expiry", size=8, color="7F7F7F")
put("H9", "date are formulas - don't type over.", size=8, color="7F7F7F")
put("H10", "Hide unused item rows before printing.", size=8, color="7F7F7F")

# ---- Header: logo + company details (left), Quotation + dates (right) ----
logo = Image("nozzleworks_logo.png")  # 792x101 px, whitespace trimmed
logo.width, logo.height = 210, round(210 * 101 / 792)
ws.add_image(logo, "A1")
ws.merge_cells("A1:B1")
for r, txt in [(2, "GST 144-375-106"), (3, "info@nozzleworks.co.nz"), (4, "nozzleworks.co.nz")]:
    put(f"A{r}", txt, size=7, bold=True)
    ws.merge_cells(f"A{r}:B{r}")

put("D1", "Quotation", size=18, bold=True, h="right")
ws.merge_cells("D1:F1")
put("D2", '="# "&F3', size=11, bold=True, h="right")
ws.merge_cells("D2:F2")
put("E3", "Quote No :", h="right"); put("F3", "QT-26001", h="right")
put("E4", "Quote Date :", h="right"); put("F4", "=TODAY()", fmt=DATE, h="right")
put("E5", "Expiry Date :", h="right"); put("F5", "=F4+$I$3", fmt=DATE, h="right")
ws.row_dimensions[1].height = 26

# ---- To block ----
put("A7", "Client Full Name", size=10, color=DARK, bold=True)
put("A8", "Job Title")
put("A9", "Company Name")
for r in (7, 8, 9):
    ws.merge_cells(f"A{r}:C{r}")

# ---- Subject ----
put("A11", "Subject :")
ws.merge_cells("A11:B11")
put("A12", "Subject line", size=10, color=DARK)
ws.merge_cells("A12:F12")

# ---- Line items ----
for i, h in enumerate(["#", "Part No. & Description", "Qty", "UoM", "Unit Price", "Sub-Total"]):
    c = ws.cell(row=ITEM_HDR, column=i + 1, value=h)
    c.font = Font(name=FONT, size=9, bold=True, color=WHITE)
    c.fill = PatternFill("solid", fgColor=HDRFILL)
    c.alignment = Alignment(horizontal="right" if i in (2, 4, 5) else "left", vertical="center")
ws.row_dimensions[ITEM_HDR].height = 18

for n, r in enumerate(ITEM_ROWS, start=1):
    put(f"A{r}", f'=IF(OR(B{r}<>"",C{r}<>""),{n},"")', color=DARK)
    put(f"B{r}", None, color=DARK, bold=True)                 # part number
    put(f"C{r}", None, color=DARK, fmt="#,##0", h="right")
    put(f"D{r}", None)
    put(f"E{r}", None, color=DARK, fmt=MONEY, h="right")
    put(f"F{r}", f'=IF(OR(C{r}="",E{r}=""),"",C{r}*E{r})', color=DARK, fmt=MONEY, h="right")
    put(f"B{r + 1}", None, wrap=True, v="top")               # description
    if n < N_ITEMS:
        ws.row_dimensions[r + 2].height = 6                  # spacer row
        # thin rule between items, shown only when the next item is used
        nxt = r + 3
        rule = DifferentialStyle(border=Border(top=Side(style="thin", color=RULECLR)))
        ws.conditional_formatting.add(
            f"A{r + 2}:F{r + 2}",
            FormulaRule(formula=[f'OR($B${nxt}<>"",$C${nxt}<>"")'], border=rule.border),
        )

# Example item so the format is clear
ex = ITEM_ROWS[0]
ws[f"B{ex}"] = "NW-EXAMPLE-01"
ws[f"B{ex + 1}"] = "Example description - replace or delete this item"
ws[f"C{ex}"] = 2
ws[f"D{ex}"] = "pcs"
ws[f"E{ex}"] = 125.00

uom = DataValidation(type="list", formula1='"pcs,ea,set,m,kg,hr,lot"', allow_blank=True, showErrorMessage=False)
ws.add_data_validation(uom)
for r in ITEM_ROWS:
    uom.add(f"D{r}")

# ---- Totals ----
t = LAST + 2
for col in "ABCDEF":
    ws[f"{col}{t}"].border = RULE
ws.row_dimensions[t].height = 6
item_range = f"F{FIRST}:F{LAST}"
put(f"E{t + 1}", "Sub Total", h="right"); put(f"F{t + 1}", f"=SUM({item_range})", fmt=MONEY, h="right")
put(f"E{t + 2}", '="GST ("&TEXT($I$2,"0%")&")"', h="right")
put(f"F{t + 2}", f"=ROUND(F{t + 1}*$I$2,2)", fmt=MONEY, h="right")
for col in "DEF":
    ws[f"{col}{t + 3}"].border = RULE
ws.row_dimensions[t + 3].height = 6
put(f"E{t + 4}", "Total", size=10, color=DARK, bold=True, h="right")
put(f"F{t + 4}", f"=F{t + 1}+F{t + 2}", size=10, color=DARK, bold=True, fmt=NZD, h="right")

# ---- Notes ----
n = t + 6
put(f"A{n}", "Notes", size=11)
notes = [
    "Delivery: approx. 3 weeks",
    "Shipping terms: ex-works.",
    "Prices are GST exclusive.",
    "Order by emailing to Info@NozzleWorks.co.nz.",
]
for i, txt in enumerate(notes, start=1):
    put(f"A{n + i}", txt)
    ws.merge_cells(f"A{n + i}:F{n + i}")
ws.merge_cells(f"A{n}:B{n}")

# ---- Terms & Conditions (page 1 short version) ----
tc = n + len(notes) + 2
put(f"A{tc}", "Terms & Conditions", size=11)
ws.merge_cells(f"A{tc}:B{tc}")
terms = [
    "Shipping: Ex works",
    "Payment: On account, 20th month following date of invoice",
    '="Validity: "&$I$3&" days"',
]
for i, txt in enumerate(terms, start=1):
    put(f"A{tc + i}", txt)
    ws.merge_cells(f"A{tc + i}:F{tc + i}")
end = tc + len(terms)

# ---- Page setup: A4, margins as the Word template, footer ----
ws.print_area = f"A1:F{end}"
ws.page_setup.paperSize = ws.PAPERSIZE_A4
ws.page_setup.orientation = "portrait"
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.page_margins.left = ws.page_margins.right = ws.page_margins.top = 0.75
ws.page_margins.bottom = 1.0
ws.oddFooter.left.text = "POWERED BY  NOZZLEWORKS"
ws.oddFooter.left.font = f"{FONT},Regular"
ws.oddFooter.left.size = 7
ws.oddFooter.left.color = GREY
ws.oddFooter.right.text = "&P"
ws.oddFooter.right.font = f"{FONT},Regular"
ws.oddFooter.right.size = 7
ws.oddFooter.right.color = GREY

wb.calculation.fullCalcOnLoad = True  # Excel computes all formulas when opened
wb.save("Quote_Template.xlsx")
