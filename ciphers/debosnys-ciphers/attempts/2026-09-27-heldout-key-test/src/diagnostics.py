#!/usr/bin/env python3
"""Post-hoc diagnostics on T4 (labelled exploratory in RESULTS.md): where the pass comes from."""
import statistics
from collections import Counter
import freeze_rules as F
import heldout_test as H


def split_test(conv="S1", xd="V2_eye", tcurl=True):
    key = F.KEYS[conv]
    pl = [p for l in H.LINES for p in H.pairs(l, conv, xd, tcurl)]
    for where in ("within", "across"):
        sub = [p for p in pl if p[2] == where]
        kv = {s: (key[s][0], key[s][1]) for s in F.KEY_SIGNS}
        vk = sum(F.pair_class(a, b, kv) == "violation" for a, b, _ in sub)
        null = []
        for t in F.all_typings(key):
            kvt = {s: (key[s][0], t[s]) for s in F.KEY_SIGNS}
            null.append(sum(F.pair_class(a, b, kvt) == "violation" for a, b, _ in sub))
        p = sum(v <= vk for v in null) / len(null)
        print(f"  {conv} {where:6s}: pairs={len(sub):3d} violations={vk:2d} null median={statistics.median(null):5.1f} "
              f"q05={sorted(null)[int(.05*len(null))]:2d} p={p:.4f}")
        c = Counter((a, b) for a, b, _ in sub)
        print("     commonest pairs:", c.most_common(8))


def list_violations(conv="S1", xd="V2_eye", tcurl=True):
    key = F.KEYS[conv]
    for l in H.LINES:
        for a, b, w in H.pairs(l, conv, xd, tcurl):
            if F.pair_class(a, b, key) == "violation":
                print(f"  L{l:2d} {w:6s} {a}->{b}  = {key[a][0]}|{key[b][0]}")


def position_profile(conv="S1", xd="V2_eye", tcurl=True):
    """Where in its glyph does each key sign sit? first / middle / last / alone."""
    prof = {s: Counter() for s in F.KEY_SIGNS}
    import poem_scan_verified as P
    for l in H.LINES:
        for _i, _code, comps in P.resolved(l, conv, xd, tcurl):
            if not comps:
                continue
            n = len(comps)
            for j, c in enumerate(comps):
                if c in prof:
                    prof[c]["alone" if n == 1 else ("first" if j == 0 else ("last" if j == n - 1 else "mid"))] += 1
    for s in F.KEY_SIGNS:
        print(f"  {s:7s} type={F.KEYS[conv][s][1]:2s} {dict(prof[s])}")


if __name__ == "__main__":
    for conv in F.CONVENTIONS:
        print(f"== within-glyph vs across-whitespace, {conv}, TCURL=NU ==")
        split_test(conv)
    print("\n== every violation, S1 primary ==")
    list_violations("S1")
    print("\n== every violation, S2 ==")
    list_violations("S2")
    print("\n== glyph-position profile of each key sign (S1) ==")
    position_profile("S1")


# Pairs the fit itself contains (signature line, both conventions). A held-out pair of the same
# ordered sign-pair is canonical by construction and carries no held-out information.
SIG_PAIRS = {
    "S1": {("C2", "B2"), ("X", "DOT"), ("N", "U"), ("O", "Z"), ("Z", "O"),
           ("B2", "X"), ("DOT", "N"), ("U", "O"), ("O", "O2RNO"), ("O2RNO", "CROSSB")},
    "S2": {("C2", "B2"), ("DOT", "X"), ("N", "U"), ("O", "Z"), ("Z", "O"),
           ("B2", "DOT"), ("X", "N"), ("U", "O"), ("O", "O2RNO"), ("O2RNO", "CROSSB")},
}


def non_inherited(conv="S1", xd="V2_eye", tcurl=True):
    key = F.KEYS[conv]
    pl = [p for l in H.LINES for p in H.pairs(l, conv, xd, tcurl)]
    new = [p for p in pl if (p[0], p[1]) not in SIG_PAIRS[conv]]
    kv = {s: (key[s][0], key[s][1]) for s in F.KEY_SIGNS}
    vk = sum(F.pair_class(a, b, kv) == "violation" for a, b, _ in new)
    null = []
    for t in F.all_typings(key):
        kvt = {s: (key[s][0], t[s]) for s in F.KEY_SIGNS}
        null.append(sum(F.pair_class(a, b, kvt) == "violation" for a, b, _ in new))
    p = sum(v <= vk for v in null) / len(null)
    print(f"  {conv}: all={len(pl)} inherited={len(pl)-len(new)} new={len(new)} violations(new)={vk} "
          f"null median={statistics.median(null)} q05={sorted(null)[int(.05*len(null))]} p={p:.4f}")
    return p


if __name__ == "__main__":
    print("\n== T4 on pairs NOT already present in the fitted signature line (exploratory) ==")
    for conv in F.CONVENTIONS:
        for xd in ("V1_all_dots", "V2_eye"):
            print(f" [{xd}]", end="")
            non_inherited(conv, xd)
