#!/usr/bin/env python3
"""
ATTACK 3 — the post-hoc decomposition.

The dossier's central move: split the HT corpus by SCRIBE, observe that the
Scribe-9 subset shares names and header vocabulary, and conclude the subset is
one administrative dossier.  Three nulls, in increasing severity:

  3a  size-matched random tablet sets (the 09-25 session's test, re-run with more
      draws and a cleaner statistic)
  3b  EVERY OTHER HT SCRIBE scored by the same statistic.  If other scribes score
      as high, "coherent dossier" is a property of being a scribe, not of being
      Scribe 9.
  3c  FINDSPOT-matched null.  Scribe 9's ten tablets come from three adjacent
      deposits.  Draw ten tablets from those same deposits regardless of hand.
      If the cohesion survives there, "same hand" explains nothing that "found
      together" does not already explain.
"""
import random, collections, re, itertools
from corpus import (load_a, ht_tablet_faces, is_word, to_val, base, LACUNA)

SEED = 20261002
ADMIN = {"KU-RO", "PO-TO-KU-RO", "KI-RO", "KU-DA", "A-DU", "KA-PA", "SA-RA₂",
         "SA-RA2"}


def tablet_wordsets(A, strict):
    by = {}
    meta = {}
    for k, v in ht_tablet_faces(A).items():
        t = base(k)
        s = by.setdefault(t, set())
        for w in v["transliteratedWords"]:
            if not is_word(w):
                continue
            if strict and ("-" not in w or w in ADMIN):
                continue
            s.add(w)
        m = meta.setdefault(t, {"scribe": set(), "findspot": set()})
        if v.get("scribe"):
            m["scribe"].add(v["scribe"])
        if v.get("findspot"):
            m["findspot"].add(v["findspot"])
    return {t: s for t, s in by.items() if s}, meta


def cohesion(tabs, by):
    c = collections.Counter()
    for t in tabs:
        for w in by.get(t, ()):
            c[w] += 1
    sh = sorted(w for w, n in c.items() if n >= 2)
    return len(sh), sh


def norm_pval(obs, draws):
    return (sum(1 for d in draws if d >= obs) + 1) / (len(draws) + 1)


def run(A, strict, label):
    by, meta = tablet_wordsets(A, strict)
    allt = sorted(by)
    rng = random.Random(SEED)
    s9 = sorted(t for t in allt if "HT Scribe 9" in meta[t]["scribe"])
    obs, sh = cohesion(s9, by)
    sz = {t: len(by[t]) for t in allt}
    print(f"\n{'='*78}\n{label}\n{'='*78}")
    print(f"  pool: {len(allt)} HT tablets, {sum(sz.values())} sign-group type-slots")
    print(f"  Scribe 9 tablets ({len(s9)}): {s9}")
    print(f"  OBSERVED cohesion = {obs}; shared types = {sh}")

    # 3a size-matched null
    tgt = sum(sz[t] for t in s9)
    draws, tries = [], 0
    while len(draws) < 20000 and tries < 4000000:
        tries += 1
        pick = rng.sample(allt, len(s9))
        if abs(sum(sz[t] for t in pick) - tgt) <= 0.10 * tgt:
            draws.append(cohesion(pick, by)[0])
    draws.sort()
    print(f"\n  3a size-matched null (+/-10% of {tgt} type-slots), n={len(draws)}:")
    print(f"     mean {sum(draws)/len(draws):.2f}  95% [{draws[int(.025*len(draws))]}, "
          f"{draws[int(.975*len(draws))]}]  p = {norm_pval(obs, draws):.4f}")

    # 3b every other scribe
    print(f"\n  3b EVERY HT scribe with >=3 attributed tablets, same statistic,")
    print(f"     each against its OWN size-matched null:")
    byscribe = collections.defaultdict(list)
    for t in allt:
        for s in meta[t]["scribe"]:
            byscribe[s].append(t)
    rows = []
    for s, tabs in sorted(byscribe.items()):
        if len(tabs) < 3:
            continue
        o, _ = cohesion(tabs, by)
        tg = sum(sz[t] for t in tabs)
        d, tr = [], 0
        while len(d) < 4000 and tr < 400000:
            tr += 1
            p = rng.sample(allt, len(tabs))
            if abs(sum(sz[t] for t in p) - tg) <= 0.15 * max(tg, 1):
                d.append(cohesion(p, by)[0])
        if not d:
            continue
        rows.append((s, len(tabs), o, sum(d)/len(d), norm_pval(o, d)))
    rows.sort(key=lambda r: r[4])
    print(f"     {'scribe':16s} {'n':>3s} {'obs':>4s} {'null mean':>10s} {'p':>8s}")
    for s, n, o, m, p in rows:
        star = "  <-- Scribe 9" if s == "HT Scribe 9" else ""
        print(f"     {s:16s} {n:3d} {o:4d} {m:10.2f} {p:8.4f}{star}")
    better = [r for r in rows if r[4] <= next(x[4] for x in rows if x[0]=='HT Scribe 9')
              and r[0] != "HT Scribe 9"]
    print(f"     scribes at least as 'cohesive' as Scribe 9 by p: {len(better)} "
          f"-> {[r[0] for r in better]}")

    # 3c findspot-matched null
    fs9 = set().union(*[meta[t]["findspot"] for t in s9]) if s9 else set()
    poolfs = [t for t in allt if meta[t]["findspot"] & fs9]
    print(f"\n  3c FINDSPOT-matched null. Scribe-9 findspots = {sorted(fs9)}")
    print(f"     HT tablets from those same deposits (any hand): {len(poolfs)}")
    print(f"     {sorted(poolfs)}")
    if len(poolfs) > len(s9):
        d = []
        for _ in range(20000):
            d.append(cohesion(rng.sample(poolfs, len(s9)), by)[0])
        d.sort()
        print(f"     null mean {sum(d)/len(d):.2f}  95% [{d[int(.025*len(d))]}, "
              f"{d[int(.975*len(d))]}]  p = {norm_pval(obs, d):.4f}")
    else:
        print(f"     POOL TOO SMALL: only {len(poolfs)} tablets come from those "
              f"deposits, and {len(s9)} of them ARE the Scribe-9 set.")
        print(f"     The findspot null CANNOT be run -- which is itself the finding:")
        print(f"     'same hand' and 'same deposit' are not separable on this corpus.")
    return obs, s9, by, meta


def main():
    A = load_a()
    run(A, False, "ATTACK 3 — all sign-group types (the 09-25 statistic)")
    run(A, True, "ATTACK 3' — STRICT: multi-sign names only, admin operators removed")


if __name__ == "__main__":
    main()
