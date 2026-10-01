#!/usr/bin/env python3
"""FROZEN rules for the 2026-09-27 held-out test of the Debosnys shared signature key.

Committed together with ../FREEZE.md BEFORE any held-out transcription list (cyphersolver
VERSE / N9 / N10) or held-out scan region was opened. Nothing in this file may be edited after
that commit; post-freeze code imports it and must not override it. See FREEZE.md section 0 for
exactly what had been seen when it was written.

Contents
  KEY_S1 / KEY_S2   Branch B values and transition types, published order (S1) and top-first (S2)
  KEY_BRANCH_A      Branch A values (frequency test T5 only; incoherent under the rime|onset rule)
  CODES             cyphersolver code -> ordered components, per convention, from the docstring
                    code keys of verse_transcription.py and n10_transcription.py @ 648309e
  components()      parser (explicit table, then a conservative fallback for undocumented codes)
  pair_class()      the typed transition grammar: canonical / hiatus / violation
  all_typings()     the exact permutation null: every assignment of the key's type multiset
  CORPORA           pinned Project Gutenberg comparanda for T5
"""
from itertools import permutations

KEY_SIGNS = ["C2", "B2", "X", "DOT", "N", "U", "O", "Z", "O2RNO", "CROSSB"]

# --- the key under test (Branch B; types: O = onset only, RO = rime+onset, R = rime) --------
KEY_S1 = {  # published order <X DOT>
    "C2": ("H", "O"), "B2": ("EN", "RO"), "X": ("EC", "RO"), "DOT": ("OS", "R"),
    "N": ("D", "O"), "U": ("EB", "RO"), "O": ("OS", "R"), "Z": ("N", "O"),
    "O2RNO": ("T", "O"), "CROSSB": ("YS", "R"),
}
KEY_S2 = dict(KEY_S1)  # dot above the X read first, <DOT X>: the X and DOT values swap
KEY_S2["X"], KEY_S2["DOT"] = ("OS", "R"), ("EC", "RO")
KEY_BRANCH_A = {"O": "O", "Z": "SN", "O2RNO": "ST"}  # other values as KEY_S1

CONVENTIONS = ("S1", "S2")
KEYS = {"S1": KEY_S1, "S2": KEY_S2}

# Greek-legal initial clusters among the key's onset consonants (secondary, lenient grammar).
GREEK_OK_CLUSTERS = {("C", "T"), ("C", "N"), ("B", "D")}

# --- component vocabulary -----------------------------------------------------------------
# Key signs use the names above. Everything else is an opaque non-key component. "?" marks a
# component whose position in the reading order cannot be fixed from the code description;
# pairs touching it are excluded (conservative). NN = double tilde (Sektu's N.N), which the
# 09-06 model exempts from being N+N; it is non-key here and its use is reported separately.
#
# Reading order: top-to-bottom by the top edge of each component, ties left-to-right; slash
# composites SL(a,b) read a (upper left), Z (slash), b (lower right) -- Sektu's own <O Z O>.
# S1 differs from S2 in exactly one rule: a single dot placed directly above an X is read
# AFTER the X (the published <X DOT>); S2 reads it first.

def _same(seq):
    return {"S1": list(seq), "S2": list(seq)}

CODES = {
    # x family
    "X": _same(["X"]),
    "XD": {"S1": ["X", "DOT"], "S2": ["DOT", "X"]},        # X with a dot (or tick) above
    "XS2": _same(["?X"]),                                    # X crossed by //: overlap, ambiguous
    "XBAR": _same(["BAR", "X"]),
    "CX": _same(["CX"]), "HX": _same(["HX"]), "BX": _same(["BX"]),  # other x-forms: not the key's X
    "XDD": {"S1": ["X", "DOT", "DOT"], "S2": ["DOT", "X", "DOT"]},
    "X_DOTBELOW": _same(["X", "DOT"]),
    "V_X": _same(["X", "V"]),
    "Z_X": _same(["ZX"]), "CX_BAR": _same(["CX", "BAR"]),
    # tilde family (single tilde = Sektu's N, always on top)
    "N_O": _same(["N", "O"]), "N_OO": _same(["N", "O", "O"]), "N_X": _same(["N", "X"]),
    "N_OX": _same(["N", "O", "X"]), "N_W": _same(["N", "W"]), "N_SLO": _same(["N", "Z", "O"]),
    "N_SL2": _same(["N", "SL2"]), "N_COLON": _same(["N", "DOT", "DOT"]),
    "N_DASH_X": _same(["N", "DASH", "X"]), "N_DASH_D": _same(["N", "DASH", "DOT", "DASH"]),
    "N_BAR_O": _same(["N", "BAR", "O"]),
    "DBLWAVE": _same(["NN"]), "DBLWAVE_XX": _same(["NN", "X", "X"]),
    "N2_X": _same(["NN", "X"]), "N2_COLON": _same(["NN", "DOT", "DOT"]),
    # bars (EQ = two bars = the key's B2)
    "EQ_O": _same(["B2", "O"]), "EQ_X": _same(["B2", "X"]), "EQ_CUP": _same(["B2", "U"]),
    "EQ3_O": _same(["B3", "O"]), "EQ3_X": _same(["B3", "X"]),
    "II_BAR_O": _same(["II", "BAR", "O"]), "ARCH_BAR_O": _same(["ARCH", "BAR", "O"]),
    "ARCH_EQ": _same(["ARCH", "B2"]), "ARCH_EQ_X": _same(["ARCH", "B2", "X"]),
    "ARCH_COLON": _same(["ARCH", "DOT", "DOT"]), "ARCH_O": _same(["ARCH", "O"]),
    "ARCH_TO": _same(["ARCH", "TT", "O"]),
    "CC_EQ": _same(["C2", "B2"]), "CC_BAR_O": _same(["C2", "BAR", "O"]),
    "CC_EQ_OO": _same(["C2", "B2", "O", "O"]),
    "BARS_II": _same(["B2", "II"]), "BARS_O": _same(["BAR", "O", "BAR"]),
    "TICKS_BAR": _same(["II", "BAR", "II"]),
    "U_EQ": _same(["U", "B2"]), "CUP_III": _same(["U", "?III"]),
    "II_BAR_U": _same(["II", "BAR", "U"]), "O_BAR_U": _same(["O", "BAR", "U"]),
    "O_BAR_II": _same(["O", "BAR", "II"]), "II_EQ_O": _same(["II", "B2", "O"]),
    "II_O": _same(["II", "O"]), "UPS_BAR_O": _same(["UPS", "BAR", "O"]),
    "UPS_BAR": _same(["UPS", "BAR"]),
    "O_EQ_HOOK": _same(["O", "?BARX", "HOOK"]),   # code says EQ, description says 'bar'
    "O_SL2_EQ": _same(["O", "SL2", "B2"]),
    # o family
    "ODOWN": _same(["O", "ARROWD"]), "OX": _same(["SMALLCROSS", "O"]),
    "OPLUS": _same(["CROSS", "O"]), "MARS_II": _same(["ARROW", "O", "II"]),
    "UPARROW": _same(["ARROWU", "DOT"]), "O_HOOK": _same(["HOOK", "O"]),
    "HOOK_O": _same(["HOOK", "O"]), "O_STEM": _same(["O", "STEM"]),
    "TARGET_J": _same(["O", "?DOTIN", "J"]), "T_O_II": _same(["CROSS", "O", "II"]),
    "CARET_O": _same(["CARET", "O"]), "PLUS_O": _same(["PLUS", "O"]), "Q": _same(["O", "TAIL"]),
    "CHEV_O": _same(["CHEV", "O"]), "CHEV_DASH": _same(["CHEV", "DASH"]),
    "CHEV_O_CHEV": _same(["CHEV", "O", "CHEV"]), "Y_RING_O": _same(["RING", "Y", "O"]),
    "OSLASH": _same(["?OZ"]), "BOX_O": _same(["?BOXO"]), "PAREN_SLO": _same(["?PARENSLO"]),
    "SL2_O": _same(["?SL2O"]),
    # singletons and others (non-key)
    "PM": _same(["CROSSB"]),
    "VENUS": _same(["VENUS"]), "DELTA": _same(["DELTA"]), "DELTA_RING": _same(["RING", "DELTA"]),
    "DELTA_BAR": _same(["?DELTABAR"]),  # defined 'underlined' in verse, 'bar above' in N10
    "SIGMA": _same(["SIGMA"]), "OMEGA": _same(["OMEGA"]), "THETA": _same(["THETA"]),
    "ALPHA": _same(["ALPHA"]), "GAM": _same(["GAM"]), "Y": _same(["Y"]), "YB": _same(["YB"]),
    "UPS": _same(["UPS"]), "V": _same(["V"]), "V_RING": _same(["RING", "V"]),
    "VCURL": _same(["?VCURL"]), "DSMALL": _same(["DSMALL"]), "DCURL": _same(["DCURL"]),
    "D_COLON": _same(["DCURL", "DOT", "DOT"]), "Z3": _same(["Z3"]), "TCURL": _same(["TCURL"]),
    "LOOP": _same(["LOOP"]), "MTAIL": _same(["MTAIL"]), "HEART": _same(["?HEART"]),
    "CHECK_DOT": _same(["?CHECKDOT"]), "CRES_E": _same(["CRESE"]), "GATE": _same(["GATE"]),
    "NOTE": _same(["NOTE"]), "TAURUS": _same(["TAURUS"]), "LEO": _same(["LEO"]),
    "STAR": _same(["STAR"]), "STAR2": _same(["STAR2"]), "HASH": _same(["HASH"]),
    "GRID": _same(["GRID"]), "EIGHT": _same(["EIGHT"]), "QBAR": _same(["QM", "BAR"]),
    "PHI": _same(["PHI"]), "CROSS": _same(["CROSS"]), "Z_CROSS": _same(["Z2", "CROSS2"]),
    "Y_VENUS": _same(["Y", "VENUS"]), "V_LOOP": _same(["VLOOP"]), "AMPER": _same(["AMPER"]),
    "CRES_DOT": _same(["?CRESDOT"]), "CHEV_DOT": _same(["?CHEVDOT"]),
    "CARET_RING": _same(["?CARETRING"]), "TAURUS_PLUS": _same(["TAURUS", "PLUS"]),
}
_SL_MARK = {"o": "O", "d": "DOT", "x": "X", "t": "TICK", "p": "PLUS", "y": "YHOOK", "22": "H22"}
PUNCT = {",", ".", "-"}


def components(code, conv):
    """Ordered components of one cyphersolver token under convention S1/S2.

    Returns (list_of_components, recognised). Pictograms are one opaque component. A trailing
    '?' (cyphersolver's uncertainty mark) is stripped here; tests decide separately whether
    uncertain tokens are kept (primary: only after scan verification).
    """
    c = code.rstrip("?")
    if c in CODES:
        return list(CODES[c][conv]), True
    if c.startswith("PIC_") or c.startswith("NUM_") or c.startswith("CLEAR_"):
        return [c], True
    for pre, slash in (("SL(", "Z"), ("BSL(", "BZ")):  # backslash is NOT Z in primary
        if c.startswith(pre) and c.endswith(")"):
            a, b = c[len(pre):-1].split(",")
            return [_SL_MARK.get(a.strip(), "?" + a), slash, _SL_MARK.get(b.strip(), "?" + b)], True
    return ["?" + c], False  # undocumented code: opaque and position-ambiguous


def is_key(comp):
    return comp in KEY_SIGNS


def pair_class(a, b, key, greek=False):
    """Typed transition grammar for adjacent key signs a -> b within a line.

    canonical: (O|RO) -> (R|RO)  and  R -> O
    hiatus:    R -> (R|RO)       (onsetless syllable; allowed, reported)
    violation: (O|RO) -> O       (an onset followed by another onset)
    """
    ta, tb = key[a][1], key[b][1]
    if ta in ("O", "RO") and tb in ("R", "RO"):
        return "canonical"
    if ta == "R" and tb == "O":
        return "canonical"
    if ta == "R" and tb in ("R", "RO"):
        return "hiatus"
    if greek:
        if (key[a][0][-1], key[b][0][0]) in GREEK_OK_CLUSTERS:
            return "canonical"
    return "violation"


def line_final_class(comp, key):
    """A verse line must close on a rime: R ok; O or RO = dangling onset (violation)."""
    return "ok" if key[comp][1] == "R" else "violation"


def all_typings(key):
    """Exact null: every distinct assignment of the key's type multiset to the ten signs."""
    types = [key[s][1] for s in KEY_SIGNS]
    seen = set()
    for perm in permutations(types):
        if perm not in seen:
            seen.add(perm)
            yield dict(zip(KEY_SIGNS, perm))


def swap_x_dot(typing):
    """The S1->S2 branch operation, applied to any typing (matched-budget best-of-2 null)."""
    t = dict(typing)
    t["X"], t["DOT"] = t["DOT"], t["X"]
    return t


# --- pinned comparanda for T5 (Project Gutenberg ebook numbers) ---------------------------
CORPORA = {
    "es": 2000,   # Cervantes, Don Quijote
    "pt": 3333,   # Camoes, Os Lusiadas
    "fr": 6099,   # Baudelaire, Les Fleurs du Mal (Sektu's own control author)
    "la": 227,    # Virgil, Aeneidos
    "it": 1000,   # Dante, La Divina Commedia
    "en": 38230,  # Thomas Moore, The Odes of Anacreon (the source family on sheet #4)
    "el": 36248,  # Homer, Iliada (Palles, Greek)
}

MIN_TESTABLE_PAIRS = 20
ALPHA = 0.05

if __name__ == "__main__":
    n = sum(1 for _ in all_typings(KEY_S1))
    print("distinct typings in the exact null:", n)
    assert n == 4200
    assert components("XD", "S1")[0] == ["X", "DOT"] and components("XD", "S2")[0] == ["DOT", "X"]
    assert components("SL(o,o)", "S1")[0] == ["O", "Z", "O"]
    assert pair_class("DOT", "N", KEY_S1) == "canonical"   # signature: OS|D
    assert pair_class("X", "N", KEY_S1) == "violation"     # EC then D: onset cluster CD
    print("frozen rules self-check ok")
