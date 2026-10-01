#!/usr/bin/env python3
"""T8 (frozen to run because T4 met its frozen criterion): do decoded runs of the key produce
dictionary words more often than the same runs decoded with permuted values?

Runs: maximal sequences of >= 3 consecutive key-sign components within a poem line (chains
break at non-key or position-ambiguous components; punctuation transparent), scan-verified
poem, S1 and S2. Hits: distinct substrings of length >= 4 that are word types with count >= 3
in the seven pinned corpora (accents stripped; Greek transliterated with k -> C to match the
key's C). Null: 10,000 random permutations of the ten values over the ten signs, best of the
two conventions per draw, exactly as for the key.
"""
import os
import random
import re
import sys
import unicodedata
from collections import Counter

import freeze_rules as F
import poem_scan_verified as P
import t5_frequency as T5

CORPUS_DIR = sys.argv[1] if len(sys.argv) > 1 else "corpora"
GR = dict(zip("αβγδεζηθικλμνξοπρστυφχψω",
              ["A", "B", "G", "D", "E", "Z", "E", "TH", "I", "C", "L", "M", "N", "X", "O", "P", "R", "S",
               "T", "Y", "PH", "CH", "PS", "O"]))


def lexicon():
    words = Counter()
    for lang in F.CORPORA:
        txt = T5.strip(T5.body(open(os.path.join(CORPUS_DIR, f"{lang}.txt"), encoding="utf-8",
                                    errors="ignore").read()))
        if lang == "el":
            for w in re.findall(r"[α-ω]+", txt):
                words["".join(GR.get(c, "") for c in w)] += 1
        else:
            for w in re.findall(r"[a-z]+", txt):
                words[w.upper()] += 1
    return {w for w, c in words.items() if c >= 3 and len(w) >= 4}


def runs(conv):
    out = []
    for l in range(1, 21):
        cur = []
        for _i, _code, comps in P.resolved(l, conv, "V2_eye", True):
            if comps is None:
                continue
            for c in comps:
                if F.is_key(c):
                    cur.append(c)
                else:
                    if len(cur) >= 3:
                        out.append(cur)
                    cur = []
        if len(cur) >= 3:
            out.append(cur)
    return out


def hits(run_list, values, lex):
    found = set()
    for r in run_list:
        s = "".join(values[c] for c in r)
        for i in range(len(s)):
            for j in range(i + 4, len(s) + 1):
                if s[i:j] in lex:
                    found.add(s[i:j])
    return found


if __name__ == "__main__":
    lex = lexicon()
    R = {c: runs(c) for c in F.CONVENTIONS}
    vals = {c: {s: F.KEYS[c][s][0] for s in F.KEY_SIGNS} for c in F.CONVENTIONS}
    key_hits = {c: hits(R[c], vals[c], lex) for c in F.CONVENTIONS}
    k = max(len(key_hits["S1"]), len(key_hits["S2"]))
    print(f"lexicon: {len(lex)} word types (len>=4, count>=3)")
    for c in F.CONVENTIONS:
        dec = ["".join(vals[c][x] for x in r) for r in R[c]]
        print(f"{c}: {len(R[c])} runs; decoded: {dec}")
        print(f"   hits: {sorted(key_hits[c])}")
    rng = random.Random(20260927)
    base = [F.KEY_S1[s][0] for s in F.KEY_SIGNS]
    null = []
    for _ in range(10000):
        perm = base[:]
        rng.shuffle(perm)
        v1 = dict(zip(F.KEY_SIGNS, perm))
        v2 = dict(v1)
        v2["X"], v2["DOT"] = v1["DOT"], v1["X"]  # the same S1->S2 branch operation
        null.append(max(len(hits(R["S1"], v1, lex)), len(hits(R["S2"], v2, lex))))
    p = sum(n >= k for n in null) / len(null)
    null.sort()
    print(f"\nkey best-of-2 distinct hits = {k}; null median = {null[5000]}, 95th pct = {null[9500]}; "
          f"p(null >= key) = {p:.4f}")
