# -*- coding: utf-8 -*-
"""Personal-name extraction from the CELT English translations of the Irish annals.

The translations (Mac Airt & Mac Niocaill, Stokes, Hennessy) keep personal names in
Irish/Latin form and translate only the surrounding prose, so the name stock is
recoverable from an English-language file.  Extraction is deliberately HIGH PRECISION
and low recall: we only take names in syntactic frames that can hold nothing else.
Recall loss shrinks every group equally and cannot manufacture a difference between
groups; a false positive (a place-name captured as a person) can.

Normalisation folds the orthographic variation that is an artefact of four different
editors working a century apart (Aedan / Áedán / Aodhan; Oengus / Aengus / Áengus).
Without it the same man counts as three names and the "unattested in Ireland" rate --
the headline statistic -- is inflated by editorial practice rather than by history.
"""
import re, unicodedata

# A name is one or two capitalised words.  Two-word names are real in this corpus
# (Mael Dúin, Cenn Faelad, Domnall Brecc) and must not be split.
NAME = r"[A-ZÁÉÍÓÚÆŒ][a-záéíóúäëïöüḟṡ’'\-]+(?:\s+[A-ZÁÉÍÓÚ][a-záéíóú’'\-]+)?"

# Frames.  Group 1 is always the personal name.
FRAMES = [
    re.compile(r"\b(%s)\s+son of\b" % NAME),
    re.compile(r"\bson of\s+(%s)" % NAME),
    re.compile(r"\b(%s)\s+grandson of\b" % NAME),
    re.compile(r"\bgrandson of\s+(%s)" % NAME),
    re.compile(r"\bDeath of\s+(%s)" % NAME),
    re.compile(r"\bKilling of\s+(%s)" % NAME),
    re.compile(r"\b(%s),?\s+king of\b" % NAME),
    re.compile(r"\b(%s),?\s+abbot of\b" % NAME),
    re.compile(r"\b(%s),?\s+bishop of\b" % NAME),
    re.compile(r"\b(%s)\s+(?:dies|died|rested|was killed|fell)\b" % NAME),
]

# Words that pass the capitalisation test but are never personal names here.
STOP = set("""The A An And Or But In On At Of To By For From With After Before
Kalends January February March April May June July August September October November
December Death Killing Battle Repose Slaughter Burning Devastation Destruction Great
Saint Bishop Abbot King Queen Lord Christ Jesus God Easter Rome Roman Ireland Irish
Britain Britons Saxons Scotland Alba Mumu Laigin Connacht Ulaid Brega Mide Temair
Armagh Iona Picts Pictland Cruithin Danes Norsemen Foreigners Leinster Munster Ulster
Meath Tara Dublin Kalend Anno Domini Year Age Sunday Monday Tuesday Wednesday Thursday
Friday Saturday There Here This That These Those His Her Their It He She They We I
Now Then Thus So Also Item Idem Vel Et Item Hence Whence""".split())

_VAR = [
    # editorial orthographic variants -> single skeleton
    (r"^aod", "aed"), (r"^aedh", "aed"), (r"^oeng", "aeng"), (r"^oing", "aeng"),
    (r"^eng", "aeng"), (r"^onch", "donnch"),
    (r"^bruide$", "brude"), (r"^bridei$", "brude"), (r"^bredei$", "brude"),
    (r"^derile$", "derili"),
]

def skeleton(name):
    """Fold to a comparison key: strip accents, lowercase, collapse -gh-/-dh-, unify
    the common editorial variants.  Two-word names keep both words."""
    s = unicodedata.normalize("NFD", name)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower().replace("’", "").replace("'", "").replace("-", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # late-medieval editorial spellings -> early skeleton
    s = s.replace("bh", "b").replace("mh", "m").replace("dh", "d").replace("gh", "g")
    s = s.replace("th", "t").replace("ch", "c").replace("ph", "f").replace("sh", "s")
    s = re.sub(r"([aeiou])\1+", r"\1", s)
    for pat, rep in _VAR:
        s = re.sub(pat, rep, s)
    return s

def extract(text):
    """Return the list of personal-name surface forms in an entry, with duplicates."""
    out = []
    for fr in FRAMES:
        for m in fr.finditer(text):
            n = m.group(1).strip()
            first = n.split()[0]
            if first in STOP:
                continue
            if len(n.split()) == 2 and n.split()[1] in STOP:
                n = first
            out.append(n)
    return out
