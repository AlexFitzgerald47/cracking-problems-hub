#!/usr/bin/env python3
"""T5: can every circle in the poem be the rime /os/ (Branch B)?

Implied lower bound, from the scan-verified poem:
    L = #O / (#non-pictogram components + 3 * #pictograms)
Ceiling, from the pinned Gutenberg corpora (freeze_rules.CORPORA): the largest share of
orthographic syllables (maximal vowel groups) whose rime is an o-final vowel group followed by
an s-coda (s then consonant or word end). Orthographic counting overstates /os/ in French and
English, which biases the test towards the key. Corpora are fetched to CORPUS_DIR; pass the
directory as argv[1] to rerun.
"""
import os
import re
import sys
import unicodedata

import freeze_rules as F
import poem_scan_verified as P

CORPUS_DIR = sys.argv[1] if len(sys.argv) > 1 else "corpora"
LAT_V = set("aeiouy")
GRK_V = set("αεηιουω")


def body(txt):
    s = txt.find("*** START OF")
    e = txt.find("*** END OF")
    if s != -1:
        txt = txt[txt.find("\n", s) + 1:]
    if e != -1:
        txt = txt[:txt.find("*** END OF")]
    return txt


def strip(t):
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return t.replace("ς", "σ")


def shares(path, greek=False):
    txt = strip(body(open(path, encoding="utf-8", errors="ignore").read()))
    V = GRK_V if greek else LAT_V
    O = ("ο", "ω") if greek else ("o",)
    S = "σ" if greek else "s"
    letter = r"[α-ω]" if greek else r"[a-z]"
    syl = os_rime = o_nuc = 0
    for w in re.findall(letter + "+", txt):
        i = 0
        while i < len(w):
            if w[i] in V:
                j = i
                while j < len(w) and w[j] in V:
                    j += 1
                syl += 1
                grp = w[i:j]
                if grp[-1] in O:
                    o_nuc += 1
                    if j < len(w) and w[j] == S and (j + 1 == len(w) or w[j + 1] not in V):
                        os_rime += 1
                i = j
            else:
                i += 1
    return syl, os_rime / syl, o_nuc / syl


def poem_counts(conv="S1", xd="V2_eye", tcurl=True):
    n_o = n_dot = n_pic = n_other = 0
    for l in range(1, 21):
        for _i, _code, comps in P.resolved(l, conv, xd, tcurl):
            if not comps:
                continue
            for c in comps:
                if c.startswith("PIC_"):
                    n_pic += 1
                else:
                    n_other += 1
                    n_o += c == "O"
                    n_dot += c == "DOT"
    return n_o, n_dot, n_pic, n_other


if __name__ == "__main__":
    print("corpus  gutenberg  syllables   f_os(ortho)   f_o-nucleus")
    ceil_os = ceil_on = 0.0
    for lang, gid in F.CORPORA.items():
        p = os.path.join(CORPUS_DIR, f"{lang}.txt")
        syl, f_os, f_on = shares(p, greek=(lang == "el"))
        ceil_os, ceil_on = max(ceil_os, f_os), max(ceil_on, f_on)
        print(f"{lang:6s}  {gid:9d}  {syl:9d}   {f_os:10.4f}    {f_on:10.4f}")
    n_o, n_dot, n_pic, n_other = poem_counts()
    denom = n_other + 3 * n_pic
    L = n_o / denom
    L_dot = (n_o + n_dot) / denom
    print(f"\npoem (S1, V2, TCURL=NU): circles={n_o} dots={n_dot} pictograms={n_pic} other components={n_other}")
    print(f"Branch B implied minimum /os/ share  L = {n_o}/{denom} = {L:.4f}   (with S1 dots also /os/: {L_dot:.4f})")
    print(f"ceiling over the seven corpora: f_os max = {ceil_os:.4f}")
    print("T5 VERDICT (Branch B):", "FALSIFIED" if L > ceil_os else "not falsified",
          f"(L exceeds the most /os/-rich corpus by a factor {L/ceil_os:.1f})")
    print(f"Branch A, for information: circle share as /o/ nucleus = {L:.4f} vs max o-nucleus share {ceil_on:.4f}")
