# -*- coding: utf-8 -*-
"""Frozen gazetteer.  See FREEZE.md.  Do not edit after the freeze commit.

Design rule: PLACE-NAMES AND ETHNONYMS ONLY.  Personal names are excluded even
when the person is certainly Ionan (Adomnan, Segene, Failbe...), because Irish
personal names recur across unrelated people and tagging on them would be the
single largest source of false positives.  This trades recall for precision.
Recall loss inflates nothing; it only shrinks the tagged counts.  The one way it
could bias a CHANGEPOINT is if the annalists' naming convention itself changed
over time -- that is checked by hand in the sample audit.

Ambiguous terms are deliberately EXCLUDED from the primary tag and collected in
SCOT_AMBIG for a sensitivity run:
  Cruithin   -- in the Irish annals normally the Ulster Cruthin, not the Picts
  Alba       -- means 'Britain' before c.900 and 'Scotland' after; it straddles
                the very transition under test
  Scots/Scotia/Scotland -- 'Scotti' means the IRISH in early insular Latin
  Rechru      -- Rathlin or Lambay, both Irish
  Manu/Manann -- Isle of Man, neither Ireland nor Dal Riata
  Lismore     -- Lios Mor Mochutu (Waterford) far outnumbers Lismore in Argyll
"""
import re

def _rx(terms):
    return re.compile("|".join(terms))

# --- primary: Scottish / Dal Riata / Pictish / Iona --------------------------
SCOT = _rx([
    r"(?<!Dath )(?<!Mac )\bÍ\b", r"\bIa\b", r"\bIona\b", r"\bHí\b",
    r"Dál Riat", r"Pict", r"Fortriu",
    r"Cenn Tíre", r"Kintyre", r"\bScí\b", r"\bMull\b", r"Tiriu", r"Tiree",
    r"\bEig\b", r"Mag Luinge",
    r"Dún At\b", r"Dún Ollaigh", r"Aporcrosan", r"Apor Crossan", r"Applecross",
    r"Cenn Garad", r"Kingarth", r"Ail Cluaithe", r"Dumbarton",
    r"Cenél Loairn", r"Cenél nGabráin", r"Cenél Comgaill",
    r"Druim Alban", r"Iardoman", r"Athfhotla", r"Circinn", r"Dún Nechtain",
])
SCOT_AMBIG = _rx([r"Cruithin", r"\bAlba", r"Scotia", r"\bScots\b", r"Scotland",
                  r"Rechru", r"\bManu\b", r"Manann", r"Lismore"])

# --- control 1: insular but non-Irish, non-Scottish --------------------------
# If the Scottish series falls but this one does not, the chronicle did not
# simply lose all foreign news.
INSULAR = _rx([r"Saxon", r"Briton", r"Britain", r"Britone", r"Northumbri",
               r"Bernic", r"\bDeir(a|i)\b", r"\bAngl", r"Wales", r"Welsh",
               r"Saxan", r"Saxolb"])

# --- control 2: the Irish midlands / Brega / Armagh axis ---------------------
# Where a chronicle leaving Iona for Ireland is usually placed.
MIDLAND = _rx([r"Brega", r"\bMide\b", r"Ard Macha", r"Cluain Moccu Nóis",
               r"Tailtiu", r"Temair", r"Lusca", r"Slane", r"Lugmad", r"Louth",
               r"Fir Rois", r"Cianachta", r"Cell Dara", r"Cluain Iraird",
               r"Dermag", r"Dam Liac", r"Fine Gall"])

# --- control 3: the far south, as a second Irish region ----------------------
MUNSTER = _rx([r"\bMumu\b", r"Caisel", r"Emly", r"Imlech", r"Laigin",
               r"Ciarraige", r"Éoganacht", r"Corcu", r"Luimnech"])

TAGSETS = {"SCOT": SCOT, "SCOT_AMBIG": SCOT_AMBIG, "INSULAR": INSULAR,
           "MIDLAND": MIDLAND, "MUNSTER": MUNSTER}

def tag(text):
    return {k: bool(rx.search(text)) for k, rx in TAGSETS.items()}
