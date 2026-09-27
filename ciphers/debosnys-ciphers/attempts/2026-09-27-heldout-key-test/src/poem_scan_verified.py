#!/usr/bin/env python3
"""The 20-line cipher poem (#4a lines 1-15, #4b lines 16-20), scan-verified token by token.

BASE is Daniel Bourdeau's transcription, `targets/debosnys/verse_transcription.py` in
github.com/dbourdeau/cyphersolver at commit 648309e85b8a (2026-09-26), code MIT, notes CC BY 4.0.
It is imported here unchanged, with attribution. Every change this session made after checking
the 4x half-line crops of the Commons scans (provenance verified, NCC >= 0.999) is an explicit
row in OVERRIDES, with its reason. Token indices are 1-based over the whitespace-split line,
punctuation included, exactly as in BASE.

Component lists use the vocabulary of freeze_rules.py. "?..." marks a component whose
position cannot be fixed; freeze_rules excludes pairs touching it.
"""
BASE = [
    "DELTA_RING SL(o,o) GAM SL(t,d) N_O XS2 Y VENUS . SL(p,x) N_O? X TCURL ,",
    "HEART YB? BARS_II OSLASH CX NOTE DSMALL , VENUS XD N_O? SL(o,o) GAM TCURL",
    "DBLWAVE SL(p,d) HX XD XD CARET_RING PM ALPHA N_O STAR ODOWN XD -",
    "PIC_SUN OX ODOWN SL(o,d) XD N_OO BARS_II CC_BAR_O XS2 GAM ALPHA N_X XD -",
    "OMEGA SL(o,d) DELTA_BAR XD THETA CC_EQ VENUS TAURUS SL(t,d) TCURL CHEV_O X N_OX SL(y,o) ,",
    "V_RING EQ_O SL(t,d) TCURL II_BAR_O ARCH_BAR_O XD N_OO N_X ALPHA SL(o,x) UPS , SL(t,d) SL(y,o) .",
    "PLUS_O EQ_X CHEV_DASH DELTA_RING UPARROW XD XD VENUS MARS_II SL(o,o) CX THETA EQ3_O ,",
    "SL(o,o) BARS_O CHECK_DOT ODOWN SL(o,x) XD N_SL2 V VCURL OSLASH TCURL SL(t,d) EQ3_O ,",
    "SL(22,) OPLUS O_EQ_HOOK ALPHA XD BSL(o,o) TCURL PM XS2 UPS EQ_X BSL(x,x) N_O VENUS ,",
    "DBLWAVE_XX Y ODOWN . TAURUS NOTE DSMALL PIC_ARROW LEO N_O X N_X CC_EQ VENUS .",
    "XS2 O_STEM DSMALL SL(d,o) PIC_FISH XD CRES_E OX VENUS , XD ALPHA PIC_HOUSE SL(d,o) N_COLON XD XD DSMALL DELTA ,",
    "ARCH_EQ II_BAR_O OSLASH ODOWN XS2? CX? DBLWAVE ALPHA? SL(o,x)? LEO? PIC_? ? N_O SL(t,d) Q DELTA .",
    "PIC_LEAF Q D_COLON SL(d,d)? N_OX ARCH_EQ X TCURL V . N_X GAM O_SL2_EQ SIGMA QBAR QBAR XD OX",
    "PIC_ANCHOR XS2 O_EQ_HOOK HX ALPHA? GRID BX Y EQ_CUP SL(o,o) TCURL XD VENUS EQ_X II_EQ N_W OPLUS",
    "Z3 OPLUS VENUS XD XD DELTA_RING EQ_X N_SLO U_EQ GAM SIGMA VCURL DCURL DSMALL MARS_II",
    "CHEV_DASH HEART XD STAR HASH , UPARROW N_DASH_X CUP_III Y , DSMALL MARS_II",
    "DELTA TICKS_BAR O_HOOK CC_EQ_OO N_OX XD EQ_O SL(t,d) YB SL2_BAR_O HOOK_O CX CX SL(o,o) TCURL",
    "LOOP ARCH_EQ_X STAR CHEV_O_CHEV N_OX N_COLON NOTE ARCH_EQ CARET_O SL(t,d) TCURL .",
    "DELTA_RING SIGMA ARCH_BAR_O XD VENUS T_O_II OX . CHEV_O Y II_BAR_O N_OO THETA BX",
    "TARGET_J XD XD Q VCURL MTAIL Z3 Y TAURUS OMEGA HX GATE EIGHT XBAR BX",
]

# ---- scan-verified overrides (this session, 2026-09-27) -----------------------------------
# kind: "comp" = explicit components (same under S1/S2 unless given as a dict);
#       "exclude" = token unreadable or identity unresolved: all components position-ambiguous.
EXCL = "exclude"
OVERRIDES = {
    (1, 11): (EXCL, "under the stain; the part below the tilde cannot be read"),
    (1, 2): (["O", "Z", "?o_or_d"], "lower-right mark is a grey blob: o or dot"),
    (2, 3): (["?BARSII"], "ticks may sit above the bars here (reverse of line 4)"),
    (2, 11): (EXCL, "top stroke reads as a cup at least as well as a tilde"),
    (10, 14): (["VENUS", "?DOTIN"], "line-final venus has a clear dot inside its circle; line 9's is open"),
    (12, 5): (EXCL, "stain; cyphersolver '?'"), (12, 6): (EXCL, "stain; cyphersolver '?'"),
    (12, 8): (EXCL, "stain; cyphersolver '?'"), (12, 9): (EXCL, "stain; cyphersolver '?'"),
    (12, 10): (EXCL, "stain; cyphersolver '?'"), (12, 11): (EXCL, "stain; cyphersolver '?'"),
    (12, 12): (EXCL, "stain; cyphersolver '?'"),
    (13, 4): (EXCL, "stain; cyphersolver '?'"),
    (13, 7): (EXCL, "a faint mark above: X or dotted X"),
    (15, 6): (["?RINGDOT", "DELTA"], "the ring on top has a dot inside"),
    (17, 5): (["N", "X", "O"], "under the tilde the x stands LEFT of the o (coded N_OX)"),
    (18, 5): (EXCL, "an uncoded dot stands at the upper left, level with the tilde"),
    (18, 6): (["N", "DOT", "DOT", "BAR"], "an uncoded bar lies under the two dots"),
    (18, 10): (["TICK", "Z", "?d_or_t"], "lower-right mark is a short stroke: dot or tick"),
    (20, 12): (["?GATEDOTS"], "three uncoded dots inside the gate"),
}
# TCURL is the signature's third glyph <N U> (visual identity; NCC rank-sum p = 0.0027 with a
# validated instrument and specificity controls, see RESULTS.md). The key's derivation reads that
# glyph as N then U, so every TCURL is decomposed the same way.
TCURL_AS_NU = ["N", "U"]

# Dotted-X marks: 25 XD tokens. Variants for the dot/tick identity (see RESULTS.md):
XD_TICKS = {
    "V1_all_dots": set(),                                              # as coded by cyphersolver
    "V2_eye": {(6, 7), (7, 6), (7, 7), (14, 12), (17, 6)},            # this session, by eye
    "V3_measured": {(6, 7), (7, 6), (7, 7), (11, 11), (17, 6)},       # elongation >= 2.0
}


def tokens(line_no):
    return BASE[line_no - 1].split()


def resolved(line_no, conv, xd_variant="V2_eye", tcurl=True):
    """Scan-verified component lists for one line: list of (token_index, code, components)."""
    import freeze_rules as F
    out = []
    for i, code in enumerate(tokens(line_no), 1):
        if code in F.PUNCT:
            out.append((i, code, None))
            continue
        ov = OVERRIDES.get((line_no, i))
        if ov is not None:
            kind, _why = ov
            comps = ["?EXCL"] if kind == EXCL else list(kind)
        elif code.rstrip("?") == "TCURL" and tcurl:
            comps = list(TCURL_AS_NU)
        elif code == "XD" and (line_no, i) in XD_TICKS[xd_variant]:
            comps = ["X", "TICK"] if conv == "S1" else ["TICK", "X"]
        elif code.endswith("?"):
            comps = ["?EXCL"]  # cyphersolver's own uncertainty mark: excluded in primary
        else:
            comps, _ok = F.components(code, conv)
        out.append((i, code, comps))
    return out
