# -*- coding: utf-8 -*-
"""Frozen three-way north-channel gazetteer.  See FREEZE.md.  Do not edit after the
freeze commit.

The sister folder (early-irish-annals-reliability, 2026-09-23) established that on this
corpus THE GAZETTEER DECIDES THE ANSWER: two defensible Scottish tag sets put the same
changepoint 70 years apart and were not distinguishable from each other.  That warning
is load-bearing here, because this folder's whole debate is about which evidence counts
as Irish and which as Scottish.  Two consequences, both built in below:

  1. The Argyll-facing material is split THREE ways, not tagged one way, because the
     three parts have different known answers and two of them are controls:

       IONA   -- the Columban familia.  Known to be recruited from Ireland, heavily
                 from Cenel Conaill.  Resident in Argyll, Irish by descent.
                 POSITIVE CONTROL: must look Irish.  If it does not, the pipeline is
                 broken, not the history.
       DALR   -- Dal Riata / Argyll secular.  THE TEST SET.
       PICT   -- Picts, Fortriu, Pictish royal centres.  Known to be a different
                 people speaking a different (P-Celtic) language.
                 NEGATIVE CONTROL: must look non-Irish.

  2. Every headline number is reported under TWO tag sets (STRICT and WIDE below).
     If they disagree, that disagreement is the finding.

Design rule inherited from the sister gazetteer: PLACE-NAMES AND ETHNONYMS ONLY for
assigning an entry to a region.  Personal names are what we are MEASURING, so using
them to assign region would be circular.  This is the single most important rule in
this file.
"""
import re

def _rx(terms):
    return re.compile("|".join(terms))

# ---------------------------------------------------------------- IONA (pos. control)
# Columban familia: Iona itself and its dependent houses in Britain.
# NOT Durrow/Kells/Derry -- those are in Ireland and would import Irish material
# into the control by construction.
IONA_STRICT = _rx([r"(?<!Dath )(?<!Mac )(?<!mac )\bÍ\b", r"\bIa\b", r"\bIona\b", r"\bHí\b",
                   r"Í Coluim", r"Hii\b", r"Iae\b"])
IONA_WIDE = _rx([IONA_STRICT.pattern, r"Mag Luinge", r"Tiriu", r"Tiree", r"Hinba"])

# ---------------------------------------------------------------- DAL RIATA (test set)
# Argyll secular.  The kingdom, its cenela, its royal centres and its islands.
DALR_STRICT = _rx([r"Dál Riat", r"Dál Riad", r"Dalriad", r"Dalariad", r"Dál Ríat",
                   r"Cenél Loairn", r"Cenél nGabráin", r"Cenél Comgaill",
                   r"Dún At\b", r"Dún Ollaigh", r"Dún Att"])
# WIDE adds the Argyll/Hebridean geography and the Dalriadic west coast.  These are
# Dal Riata's territory but an entry naming them need not be about the kingdom.
DALR_WIDE = _rx([DALR_STRICT.pattern,
                 r"Cenn Tíre", r"Kintyre", r"\bMull\b", r"\bSkye\b", r"\bScí\b",
                 r"\bEig\b", r"Aporcrosan", r"Apor Crossan", r"Applecross",
                 r"Cenn Garad", r"Kingarth", r"Iardoman", r"Cend Tíre"])

# ---------------------------------------------------------------- PICTS (neg. control)
PICT_STRICT = _rx([r"Pict", r"Fortr(iu|enn|iu)", r"Fortriu", r"Cruithentúaith"])
PICT_WIDE = _rx([PICT_STRICT.pattern, r"Circinn", r"Athfhotla", r"Atholl",
                 r"Dún Nechtain", r"Dún Caillen", r"Duncalden", r"Monoth",
                 r"Druim Alban", r"Nechtan"])

# ---------------------------------------------------------------- Irish reference pool
# An entry is IRISH-REFERENCE only if it names an Irish region/people/church AND
# matches none of the three north-channel sets above.  Requiring a positive Irish
# marker (rather than taking "everything untagged") keeps undated, foreign and
# purely ecclesiastical-universal entries out of the reference distribution.
IRISH = _rx([
    # Ui Neill / midlands / Brega / Armagh
    r"Brega", r"\bMide\b", r"Ard Macha", r"Armagh", r"Cluain Moccu Nóis", r"Clonmacnois",
    r"Tailtiu", r"Temair", r"Temuir", r"\bTara\b", r"Lusca", r"Slane", r"Lugmad", r"Louth",
    r"Fir Rois", r"Cianacht", r"Ciannacht", r"Cell Dara", r"Kildare", r"Cluain Iraird",
    r"Dermag", r"Durrow", r"Dam Liac", r"Fine Gall", r"Uí Néill", r"Ui Neill", r"Ailech",
    r"Cenél Conaill", r"Cenél nEógain", r"Cenel Conaill",
    # Ulster
    r"Ulaid", r"Ulidia", r"Ulster", r"Dál Araid", r"Dál Fiatach", r"Dál nAraide",
    r"Dún Lethglaise", r"Bangor", r"Bennchor", r"Airgialla", r"Oriel", r"Mag Roth",
    # Leinster
    r"Laigin", r"Leinster", r"Osraige", r"Ossory", r"Uí Cheinnselaig", r"Uí Failg",
    r"Uí Fhailgi", r"Glenn Dá Locha", r"Glendalough", r"Ferna", r"Cell Ausaili",
    # Munster
    r"\bMumu\b", r"Munster", r"Caisel", r"Cashel", r"Emly", r"Imlech", r"Ciarraige",
    r"Éoganacht", r"Eoganacht", r"Corcu", r"Luimnech", r"Lismore", r"Les Mór",
    # Connacht
    r"Connacht", r"Connachta", r"Uí Briúin", r"Uí Maine", r"Uí Fhiachrach", r"Cruachan",
    r"Síl Muiredaig", r"Clonfert", r"Cluain Ferta",
    # generic
    r"\bIreland\b", r"\bÉriu\b", r"\bEriu\b", r"\bHibern",
])

TAGSETS = {
    "STRICT": {"IONA": IONA_STRICT, "DALR": DALR_STRICT, "PICT": PICT_STRICT},
    "WIDE":   {"IONA": IONA_WIDE,   "DALR": DALR_WIDE,   "PICT": PICT_WIDE},
}

def region(text, tagset="STRICT"):
    """Return the set of north-channel groups an entry matches (may be empty or >1)."""
    ts = TAGSETS[tagset]
    return {k for k, rx in ts.items() if rx.search(text)}

def is_irish_ref(text, tagset="STRICT"):
    """True iff the entry carries a positive Irish marker and NO north-channel marker."""
    return bool(IRISH.search(text)) and not region(text, tagset)
