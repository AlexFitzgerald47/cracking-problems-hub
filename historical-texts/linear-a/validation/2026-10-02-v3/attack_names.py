#!/usr/bin/env python3
"""
ATTACK 4 — are the 'repeated dossier names' informative, and is DI-KI-SE a control?

  4a  frequency profile of the 13 / 9 shared types.  If they are the corpus's most
      frequent HT designations, their recurrence inside ANY 10-tablet subset is
      expected and the 'dossier' inference is circular.
  4b  DI-KI-SE as 'the strongest quasi-experimental status-switch control':
      base rate of name types occurring on >=2 HT tablets of which >=1 carries
      KI-RO and >=1 does not.
  4c  the five claimed status-switch controls, checked one by one in the raw corpus.
"""
import collections
from corpus import load_a, ht_tablet_faces, is_word, base
from attack_split import tablet_wordsets, ADMIN


def main():
    A = load_a()
    byT, meta = tablet_wordsets(A, False)
    byS, _ = tablet_wordsets(A, True)
    allt = sorted(byT)
    s9 = sorted(t for t in allt if "HT Scribe 9" in meta[t]["scribe"])

    freq = collections.Counter()
    for t in allt:
        for w in byT[t]:
            freq[w] += 1

    print("=" * 78)
    print("ATTACK 4a — are the 'dossier' shared types just the corpus's commonest names?")
    print("=" * 78)
    c = collections.Counter()
    for t in s9:
        for w in byT[t]:
            c[w] += 1
    shared = sorted((w for w, n in c.items() if n >= 2), key=lambda w: -freq[w])
    print(f"  the {len(shared)} shared types, with how many of the {len(allt)} HT")
    print(f"  tablets carry each one corpus-wide, and its rank by that frequency:")
    rank = {w: i + 1 for i, (w, n) in enumerate(freq.most_common())}
    for w in shared:
        inside = c[w]
        print(f"    {w:14s} on {freq[w]:3d}/{len(allt)} HT tablets "
              f"(rank {rank[w]:4d} of {len(freq)})   inside Scribe-9 set: {inside}")
    print(f"\n  median corpus-wide tablet count of the shared types: "
          f"{sorted(freq[w] for w in shared)[len(shared)//2]}")
    print(f"  median over ALL HT types: "
          f"{sorted(freq.values())[len(freq)//2]}")
    top20 = [w for w, n in freq.most_common(20)]
    print(f"  of the top 20 most widespread HT types, how many are in the shared set: "
          f"{len(set(top20) & set(shared))} -> {sorted(set(top20) & set(shared))}")
    print("  -> a type that appears on many HT tablets will appear on >=2 of ANY")
    print("     10-tablet subset almost automatically. The 'dossier cohesion' statistic")
    print("     is dominated by exactly those types.")

    # expected cohesion from marginal frequencies alone (independence model)
    n = len(allt); k = len(s9)
    from math import comb
    exp = 0.0
    for w, f in freq.items():
        # P(>=2 of the k drawn tablets carry w) under hypergeometric draw
        p0 = comb(n - f, k) / comb(n, k) if n - f >= k else 0.0
        p1 = (f * comb(n - f, k - 1) / comb(n, k)) if n - f >= k - 1 else 0.0
        exp += 1 - p0 - p1
    print(f"\n  expected cohesion of a RANDOM {k}-tablet subset from marginal")
    print(f"  frequencies alone (hypergeometric, no clustering): {exp:.2f}")
    print(f"  observed for Scribe 9: {len(shared)}")

    print("\n" + "=" * 78)
    print("ATTACK 4b — DI-KI-SE as 'the strongest quasi-experimental control'")
    print("=" * 78)
    kiro_t = {t for t in allt if "KI-RO" in byT[t]}
    print(f"  HT tablets containing KI-RO: {len(kiro_t)} -> {sorted(kiro_t)}")
    cands = []
    for w, f in freq.items():
        if f < 2 or "-" not in w or w in ADMIN:
            continue
        ts = {t for t in allt if w in byT[t]}
        if (ts & kiro_t) and (ts - kiro_t):
            cands.append((w, f, sorted(ts & kiro_t), sorted(ts - kiro_t)))
    cands.sort(key=lambda x: -x[1])
    print(f"  multi-sign name types occurring on >=1 KI-RO tablet AND >=1 non-KI-RO")
    print(f"  tablet: {len(cands)}")
    for w, f, a, b in cands:
        mark = "  <== claimed as a control" if w in (
            "DI-KI-SE", "KU-PA₃-NU", "PA-TA-NE", "PA-JA-RE", "SA-RU") else ""
        print(f"    {w:16s} n={f:2d}  KI-RO tablets {a}  non-KI-RO {b}{mark}")
    print(f"\n  -> the 'status-switch control' property is shared by {len(cands)} name")
    print("     types. DI-KI-SE is not a designed experiment; it is one member of a")
    print("     large class, and the class is exactly what you get when frequent names")
    print("     are spread over tablets some of which happen to carry KI-RO.")

    print("\n" + "=" * 78)
    print("ATTACK 4c — the five claimed controls, checked against witness A")
    print("=" * 78)
    for w in ["DI-KI-SE", "KU-PA₃-NU", "PA-TA-NE", "PA-JA-RE", "SA-RU"]:
        faces = sorted(k for k, v in A.items()
                       if w in v["transliteratedWords"])
        print(f"  {w:14s} occurs on faces {faces}")


if __name__ == "__main__":
    main()
