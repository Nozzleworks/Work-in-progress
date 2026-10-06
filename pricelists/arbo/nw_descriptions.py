"""Proposed Nozzleworks product descriptions for AKBO items.

Structure:  <Series> <product>, <feature(s)>, <colour>, <material>
e.g.        Classic water gun, w/o trigger insulation, blue, brass
            Blue King water gun, w/o trigger guard, blue, brass

Series names follow the NozzleWorks brochures
(OneDrive: 01 Marketing/04 Brochures/AKBO NL/NozzleWorks_Brochures):
  KLMN  Classic                         AKCN  Classic Protection Plus
  AKMN  Multi-Purpose (brass)           AKRN  Multi-Purpose (stainless)
  AKMN011/AKMNP11  Blue King            BMFT/BRFT  Blue Princess
  AKNN  Lightweight                     BABT/BMBT  Baby
  AKMB/AKRB  High-Flow                  AKRH  Hot-Water
  AKRNP01-BL-EX  ATEX                   AKRN002-LB-LAT  Sterilisable
  AKRSV01  The Squeezer                 AGIL572  Spray Gun XS Lite
  AKAWLU1  Air-Boosted                  AKKS  Shower Wash Head
  AKMSH/AKRSH (robust)  Twistflow WD Nozzle
  AKMSHL/AKRSHL (water-saving)  Twistflow Lite WD Nozzle
  AKNSH01  Twistflow-L Lite             TWRWR02  Twistflow M / L / XL
  BALR/BARR  Shielded ball valve
Items with no NozzleWorks brochure (water savers, Blue Nozzle, swivels, hose
tails) use a plain product name in the same structure.
"""
import re

COLOURS = {"B": "blue", "R": "red", "G": "green", "BL": "black", "Y": "yellow",
           "W": "white", "LB": "light blue"}

BR, CR, SS, SS304, AL, PA = ("brass", "chrome-plated brass", "stainless steel 316",
                             "stainless steel 304", "aluminium", "PA66 plastic")
NTG, TG = "w/o trigger guard", "w/ trigger guard"


def _d(*parts):
    return ", ".join(p for p in parts if p)


FIXED = {
    # ---- Heavy duty guns
    "AKNN001-B": _d("Lightweight water gun", NTG, "blue", PA),
    "BMFT001-B": _d("Blue Princess water gun", NTG, "blue", BR),
    "BMFT001-B-PRIN": _d("Blue Princess water gun", NTG, "PRINCESS logo", "blue", BR),
    "BMFTP11-B-PRIN": _d("Blue Princess water gun", TG, "PRINCESS logo", "blue", BR),
    "AKMNP01-B": _d("Multi-Purpose water gun", TG, "blue", BR),
    "AKMNP01-B-SW12": _d("Multi-Purpose water gun", TG, '1/2" F swivel', "blue", BR),
    "AKMNP01-B-SW34": _d("Multi-Purpose water gun", TG, '3/4" F swivel', "blue", BR),
    "AKMN011-B": _d("Blue King water gun", NTG, "blue", BR),
    "AKMN011-B-KING": _d("Blue King water gun", NTG, "KING logo", "blue", BR),
    "AKMNP11-B": _d("Blue King water gun", TG, "blue", BR),
    "AKMNP11-B-KING": _d("Blue King water gun", TG, "KING logo", "blue", BR),
    "AKMB001-BL": _d("High-Flow water gun", NTG, "black", BR),
    "AKMBP01-BL": _d("High-Flow water gun", TG, "black", BR),
    "AKRB001-BL": _d("High-Flow water gun", NTG, "black", SS),
    "AKCN001-B": _d("Classic Protection Plus water gun", NTG, "blue", CR),
    "AKCNP01-B": _d("Classic Protection Plus water gun", TG, "blue", CR),
    "AKCNP01-W": _d("Classic Protection Plus water gun", TG, "white", CR),
    "BRFT003-B": _d("Blue Princess water gun", NTG, "blue", SS),
    "BRFT003-B-PRIN": _d("Blue Princess water gun", NTG, "PRINCESS logo", "blue", SS),
    "BRFTP03-B-PRIN": _d("Blue Princess water gun", TG, "PRINCESS logo", "blue", SS),
    "AKRN001-B": _d("Multi-Purpose water gun", NTG, "blue", SS),
    "AKRN001-W": _d("Multi-Purpose water gun", NTG, "white", SS),
    "AKRNP01-B": _d("Multi-Purpose water gun", TG, "blue", SS),
    "AKRNP01-W": _d("Multi-Purpose water gun", TG, "white", SS),
    "AKRHP01-R": _d("Hot-Water gun", TG, "Teflon/air insulated grip", "red", SS),
    "AKRHPB1-R": _d("Hot-Water gun", TG, "high flow", "Teflon/air insulated grip", "red", SS),
    "AKRHP02-R-L40": _d("Hot-Water gun", TG, "40 cm lance", "Teflon/air insulated grip", "red", SS),
    "AKRNP01-BL-EX": _d("ATEX water gun", TG, "Zone 1 & 2", "black", SS),
    "AKRN002-LB-LAT": _d("Sterilisable water gun", "latex jacket", "light blue", SS),
    "AKRSV01-B": _d("The Squeezer valve", 'self-closing, 1/2" F x 1/2" F', "blue", SS304),
    "AKR001-B": _d("The Squeezer shower head", '1/2" M', "blue", SS304 + " / PA66"),
    # ---- Baby series
    "BABTN01-B": _d("Baby water gun", "rear trigger", "blue", AL),
    "BABTLF1-BL": _d("Baby water gun", 'rear trigger, 1/2" F outlet', "black", AL),
    "BABTA01-B": _d("Baby water gun", "rear trigger, adapter outlet", "blue", AL),
    "BABTNAA-B": _d("Baby water gun", "rear trigger, adapter inlet & outlet", "blue", AL),
    "BMBTN01-B": _d("Baby water gun", "rear trigger", "blue", BR),
    "BMBNN01-B": _d("Baby water gun", 'rear trigger, 1/2" M outlet, adjustable nozzle', "blue", BR),
    "BMBTL01-B": _d("Baby water gun", 'rear trigger, 1/2" M outlet', "blue", BR),
    "BMBTA01-B": _d("Baby water gun", "rear trigger, adapter outlet", "blue", BR),
    "BMBTA02-B-V": _d("Baby water gun", "rear trigger, adapter outlet, Viton seals", "blue", BR),
    # ---- Other guns / spray heads
    "AGIL572": _d("Spray Gun XS Lite", '3/4" GHT outlet', "red", "chrome-plated zinc"),
    "AKMSHH4-BL": _d("Twistflow WD Nozzle", 'head only, 1/2" M', "black", BR),
    "AKRSHW3-W": _d("Twistflow WD Nozzle", "w/ handle", "white head / white handle", "stainless steel"),
    "AKRSHH4-BL": _d("Twistflow WD Nozzle", 'head only, 1/2" M', "black", "stainless steel"),
    "AKRSHH4-W": _d("Twistflow WD Nozzle", 'head only, 1/2" M', "white", "stainless steel"),
    "AKNSH01-B": _d("Twistflow-L Lite nozzle", '3/4" M', "blue", "polypropylene"),
    "AKMSHHL1-BL": _d("Twistflow Lite WD Nozzle", 'head only, 1/2" M', "black", BR),
    "AKMSHL1-B": _d("Twistflow Lite WD Nozzle", "w/ handle", "blue", BR),
    "AKRSHHL1-BL": _d("Twistflow Lite WD Nozzle", 'head only, 1/2" M', "black", SS304),
    "AKRSHL1-B": _d("Twistflow Lite WD Nozzle", "w/ handle", "blue", SS304),
    "AKRSHL1-W": _d("Twistflow Lite WD Nozzle", "w/ handle", "white", SS304),
    "TWRWR02M": _d("Twistflow M WD Nozzle", '1/2" BSPP M, 60° cone', "white / red guard", SS304),
    "TWRWR02L": _d("Twistflow L WD Nozzle", '3/4" BSPP M, 60° cone', "white / red guard", SS304),
    "TWRWR02XL": _d("Twistflow XL WD Nozzle", '1" BSPP M, 60° cone', "white / red guard", SS304),
    "AKAWLU1-B": _d("Air-Boosted water gun", "2x 10 mm hose tails (air & water)", "blue", AL),
    "BWNM045": _d("Blue Nozzle sprayer", '4.5 mm outlet, 3/4" F', "blue", BR),
    # ---- Shower heads
    "AKKS003-B": _d("Shower Wash Head", '1/2" F', "blue", PA),
    "AKKS003-W": _d("Shower Wash Head", '1/2" F', "white", PA),
    "AKKS003-B-19": _d("Shower Wash Head", '1/2" F, w/ 19 mm hose tail (loose)', "blue", PA),
    "AKKS003-W-19": _d("Shower Wash Head", '1/2" F, w/ 19 mm hose tail (loose)', "white", PA),
    # ---- Ball valves
    "BALR001-B": _d("Shielded ball valve", '1/2" F x 1/2" F, EPDM protection', "blue", SS304),
    "BALRCP1-B": _d("Shielded ball valve", '1/2" F x quick coupling, EPDM protection', "blue", SS304),
    "BALRCP1-NB": _d("Shielded ball valve", '1/2" F x quick coupling, nylon protection', "blue", SS304),
    "BARRCP2-B": _d("Shielded ball valve", '1/2" F x quick coupling, EPDM protection, lever guard', "blue", SS),
}

for c in ["B", "R", "G", "BL", "Y", "W"]:
    FIXED[f"KLMN001-{c}"] = _d("Classic water gun", "w/o trigger insulation", COLOURS[c], BR)
    FIXED[f"AKMN001-{c}"] = _d("Multi-Purpose water gun", NTG, COLOURS[c], BR)
for c in ["B", "R", "W"]:
    FIXED[f"AKMSH03-{c}"] = _d("Twistflow WD Nozzle", "w/ handle", f"black head / {COLOURS[c]} handle", BR)
    FIXED[f"AKRSH03-{c}"] = _d("Twistflow WD Nozzle", "w/ handle", f"black head / {COLOURS[c]} handle",
                               "stainless steel")
for m, name in [("S", "S, flat spray"), ("M", "M, 13 mm orifice"), ("L", "L, 9 mm orifice"),
                ("R", "R, 4.5 mm orifice")]:
    FIXED[f"AKWM{m}01"] = _d("Water Saver nozzle", f'model {name}, 3/4" F', "", BR)
    FIXED[f"AKWR{m}01"] = _d("Water Saver nozzle", f'model {name}, 3/4" F', "", SS304)


def _thread(t):
    t = re.sub(r"\bmale\b", "M", t)
    t = re.sub(r"\bfemale\b", "F", t)
    t = re.sub(r"\bBSP (?=[MF]\b)", "", t)  # plain BSP is the default; keep BSPT
    return t


def _fitting(code, desc):
    """Swivels and hose tails, built from AKBO's own description text."""
    d = " ".join(desc.replace("\n", " ").split()).rstrip(".")
    low = d.lower()
    if low.startswith("chrome plated brass"):
        mat = CR
    elif low.startswith(("st.st", "st. st", "stainless steel")):
        mat = SS
    elif low.startswith("brass"):
        mat = BR
    else:
        return None
    feats = []
    if code.startswith(("SWM", "SWC", "SWR")):
        name = "Ball bearing swivel"
        conn = re.search(r"(\d+(?:/\d+)?\"? (?:male|female) x \d+(?:/\d+)?\"? (?:male|female))", d)
        bore = re.search(r"(\d+)\s*mm bore", d)
        feats = [_thread(conn.group(1)) if conn else "", f"{bore.group(1)} mm bore" if bore else ""]
    elif code.startswith("SWIF"):
        name = "Swivel hose tail"
        tail = re.search(r"(\d+)\s*mm\s*x\s*(\d+/\d+\"\s*(?:BSPT?\s*)?male)", d)
        coll = re.search(r"(\d+)\s*mm collar", d)
        feats = ["full bore" if "full bore" in low else "",
                 f"{tail.group(1)} mm x {_thread(tail.group(2))}" if tail else "",
                 f"{coll.group(1)} mm collar" if coll else "",
                 "w/ anti-kink spring" if "spring" in low else ""]
    elif code.startswith(("MESS", "MESC", "RVST")):
        name = "Hose tail"
        conn = re.search(r"(\d+/\d+\"\s*(?:BSP\s*)?(?:male|female))", d)
        tail = re.search(r"x\s*(\d+)\s*mm", d)
        coll = re.search(r"(\d+)\s*mm collar", d)
        feats = [f"{tail.group(1)} mm x {_thread(conn.group(1))}" if tail and conn else "",
                 "w/ O-ring" if "o-ring" in low else "",
                 f"{coll.group(1)} mm collar" if coll else "",
                 "w/ anti-kink spring" if "spring" in low else ""]
    elif code.startswith("RVSW"):
        name = "Hose tail w/ union nut"
        tail = re.search(r"(\d+)\s*mm\s*x\s*(\d+(?:/\d+)?\"\s*BSP female)", d)
        coll = re.search(r"(\d+)\s*mm collar", d)
        seal = "conical seal" if "conical" in low else "flat seal" if "flat" in low else ""
        feats = [f"{tail.group(1)} mm x {_thread(tail.group(2))}" if tail else "", seal,
                 f"{coll.group(1)} mm collar" if coll else "",
                 "w/ anti-kink spring" if "spring" in low else ""]
    else:
        return None
    return _d(name, *feats, mat)


def nw_description(code, akbo_desc):
    """Return the proposed Nozzleworks description, or '' if none could be built."""
    if code in FIXED:
        return FIXED[code]
    return _fitting(code, akbo_desc) or ""
