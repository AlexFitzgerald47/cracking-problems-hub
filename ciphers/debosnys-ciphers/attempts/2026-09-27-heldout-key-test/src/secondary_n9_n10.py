#!/usr/bin/env python3
"""Secondary corpus (FREEZE section 4): N9 (#2a + #2b prose, 25 lines) and N10 (#3 block, 4 lines),
as coded by cyphersolver @ 648309e (MIT; imported from its transcription files, attributed).
Parsed with the frozen table; undocumented codes are opaque, exactly as frozen. TCURL is read as
<N U>, the identity established on the poem. Prose line ends are not verse ends, so T1 does not
apply here. Pass the cyphersolver target directory as argv[1].
"""
import importlib.util
import statistics
import sys
from collections import Counter

import freeze_rules as F

SRC = sys.argv[1] if len(sys.argv) > 1 else "."


def _load(name):
    spec = importlib.util.spec_from_file_location(name, f"{SRC}/{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


N9 = _load("n9_transcription").N9
N10 = _load("n10_transcription").N10


def comps(code, conv):
    c = code.rstrip("?")
    if c == "TCURL":
        return ["N", "U"], True
    if code.endswith("?") or code == "?":
        return ["?EXCL"], False
    return F.components(c, conv)


def line_pairs(line, conv):
    out, prev, n_tok, n_rec = [], None, 0, 0
    for code in line.split():
        if code in F.PUNCT:
            continue
        g, rec = comps(code, conv)
        n_tok += 1
        n_rec += rec
        for a, b in zip(g, g[1:]):
            if F.is_key(a) and F.is_key(b):
                out.append((a, b, "within"))
        if prev is not None and F.is_key(prev) and F.is_key(g[0]):
            out.append((prev, g[0], "across"))
        prev = g[-1] if not g[-1].startswith("?") else None
    return out, n_tok, n_rec


def test(lines, label, conv):
    pl, nt, nr = [], 0, 0
    for l in lines:
        p, a, b = line_pairs(l, conv)
        pl += p
        nt += a
        nr += b
    key = F.KEYS[conv]
    for where in ("all", "within", "across"):
        sub = pl if where == "all" else [p for p in pl if p[2] == where]
        if not sub:
            print(f"  {label} {conv} {where}: no testable pairs")
            continue
        vk = sum(F.pair_class(a, b, key) == "violation" for a, b, _ in sub)
        null = [sum(F.pair_class(a, b, {s: (key[s][0], t[s]) for s in F.KEY_SIGNS}) == "violation"
                    for a, b, _ in sub) for t in F.all_typings(key)]
        p = sum(v <= vk for v in null) / len(null)
        flag = "  (UNDERPOWERED: < 20 pairs)" if len(sub) < F.MIN_TESTABLE_PAIRS else ""
        print(f"  {label} {conv} {where:6s}: tokens={nt} recognised={nr} pairs={len(sub):3d} "
              f"violations={vk:2d} null median={statistics.median(null):5.1f} p={p:.4f}{flag}")
    return pl


if __name__ == "__main__":
    for conv in F.CONVENTIONS:
        test(N9, "N9 ", conv)
        test(N10, "N10", conv)
    codes = Counter(c.rstrip("?") for l in N9 for c in l.split())
    undocumented = [c for c in codes if c not in F.CODES and not c.startswith(("PIC_", "SL(", "BSL(", "NUM_", "CLEAR_"))]
    print(f"\nN9 distinct codes: {len(codes)}; undocumented in either cyphersolver code key: {len(undocumented)} "
          f"covering {sum(codes[c] for c in undocumented)} of {sum(codes.values())} tokens")
