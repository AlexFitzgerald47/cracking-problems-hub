#!/usr/bin/env python3
"""Handover pre-check for the successor hypothesis (not part of the frozen test).

The untested whole-glyph reading of the same crib (analysis/signature_candidate_key_v1.json:
C2B2=HENE, XP=COS, NU=DE, ZOO=BOS, OM2N=NOS, SHI=TYS) makes the poem's commonest glyph, the
dotted X (9.0% of tokens; >= 6.8% counting only round dots), the syllable /kos/, and TCURL
(3.6%) the syllable /de/. This prints each syllable's share in the pinned corpora.

    python3 syllable_ceiling.py <corpora dir>
"""
import os
import re
import sys

import freeze_rules as F
import t5_frequency as T

CD = sys.argv[1] if len(sys.argv) > 1 else "corpora"

for lang in F.CORPORA:
    g = lang == "el"
    txt = T.strip(T.body(open(os.path.join(CD, f"{lang}.txt"), encoding="utf-8", errors="ignore").read()))
    V = T.GRK_V if g else T.LAT_V
    K = ("κ",) if g else ("c", "k", "q")
    O = ("ο", "ω") if g else ("o",)
    S = "σ" if g else "s"
    Dd = "δ" if g else "d"
    E = ("ε", "η", "αι") if g else ("e",)
    syl = cos = de = 0
    for w in re.findall((r"[α-ω]" if g else r"[a-z]") + "+", txt):
        i = 0
        while i < len(w):
            if w[i] in V:
                j = i
                while j < len(w) and w[j] in V:
                    j += 1
                syl += 1
                grp, on = w[i:j], (w[i - 1] if i > 0 else "")
                if on in K and grp[-1] in O and j < len(w) and w[j] == S and (j + 1 == len(w) or w[j + 1] not in V):
                    cos += 1
                if on == Dd and grp in E and (j == len(w) or w[j] in V or (j + 1 < len(w) and w[j + 1] in V)):
                    de += 1
                i = j
            else:
                i += 1
    print(f"{lang}: syllables={syl:7d}  /kos/ share={cos/syl:.4%}   /de/ (open) share={de/syl:.4%}")
