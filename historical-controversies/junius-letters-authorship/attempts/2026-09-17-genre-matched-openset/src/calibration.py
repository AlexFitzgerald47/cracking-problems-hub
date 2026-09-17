#!/usr/bin/env python3
"""
SUPERSEDED, kept for the record. Requiring every large sample to measure every
variable collapsed the comparable variable set to ONE (on/upon), which is too fragile
to carry a conclusion -- that collapse is itself the finding that pushed this study off
binary synonym variables and onto function-word Delta. register_calibration.py is the
replacement.

The number the whole argument turns on: how far apart are TWO GENUINELY DIFFERENT
samples of one author?

scorecard.py's first calibration splits a single volume at random. That shares topic,
date, edition and OCR pipeline between the halves, so it measures sampling noise and
almost nothing else -- an optimistic lower bound. The honest calibration pairs samples
that differ the way Junius and Francis differ: different volume, different decade, or
different register.

If a same-author cross-sample distance is as large as the Junius-to-Francis distance,
then these variables cannot tell "different author" from "same author writing
something else", and no ranking built on them is evidence either for or against the
attribution. That is a real finding and is reported as one.

All distances use ONE fixed variable set so that they are mutually comparable; a
profile missing any variable in that set is excluded rather than scored on fewer.
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
CORP = os.path.join(HERE, "..", "data", "corpus")
MIN_JOINT = 25


def prop(c, a, b):
    n = c[a] + c[b]
    return (c[a] / n) if n >= MIN_JOINT else None


def counts(texts):
    tot = Counter()
    for t in texts:
        tot.update(C.tokens(t))
    return tot


def load_groups():
    """Named samples, each a pooled token count, tagged with author / genre / source."""
    g = defaultdict(list)
    for name in ("panel_chunks.jsonl", "junius_1772_wikisource.jsonl",
                 "junius_1813_ocr.jsonl"):
        if not os.path.exists(os.path.join(CORP, name)):
            continue
        for d in C.load_jsonl(name):
            src = d.get("source", d.get("volume", "?"))
            g[(d["author"], d["genre"], src)].append(d["text"])
    return {k: counts(v) for k, v in g.items()}


def profile(c, variables):
    return {v: prop(c, *v.split("/")) for v in variables}


def dist(p, q, variables):
    if any(p[v] is None or q[v] is None for v in variables):
        return None
    return sum(abs(p[v] - q[v]) for v in variables) / len(variables)


def main():
    ge = json.load(open(os.path.join(RES, "genre_effect.json")))
    usable = [v for v, d in ge.items() if d["verdict"] == "usable"]

    groups = load_groups()
    # Merge the Junius digitisations into one public-letter sample, and keep each
    # other volume separate so that same-author cross-volume pairs exist.
    jun = Counter()
    for (a, g, s), c in groups.items():
        if a == "Junius":
            jun.update(c)

    # choose the largest variable subset measurable in Junius and in every sample of
    # at least 40k tokens -- fixed for all comparisons below
    big = {k: c for k, c in groups.items() if sum(c.values()) >= 40000}
    variables = [v for v in usable
                 if prop(jun, *v.split("/")) is not None
                 and all(prop(c, *v.split("/")) is not None for c in big.values())]
    print(f"Fixed comparable variable set ({len(variables)}): {', '.join(variables)}")
    print(f"(samples of >= 40,000 tokens: {len(big)})\n")

    jp = profile(jun, variables)
    print("Junius public letters:", {v: round(jp[v], 3) for v in variables}, "\n")

    # --- same author, different sample ------------------------------------
    byauthor = defaultdict(list)
    for (a, g, s), c in big.items():
        byauthor[a].append(((g, s), c))
    print("SAME AUTHOR, DIFFERENT SAMPLE (different volume and/or register)")
    print(f"{'author':18s} {'sample A':34s} {'sample B':34s} {'dist':>6s}")
    print("-" * 96)
    same = []
    for a, lst in sorted(byauthor.items()):
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                (g1, s1), c1 = lst[i]
                (g2, s2), c2 = lst[j]
                d = dist(profile(c1, variables), profile(c2, variables), variables)
                if d is None:
                    continue
                same.append((a, f"{g1}/{s1}", f"{g2}/{s2}", d))
                print(f"{a:18s} {(g1+'/'+s1)[:34]:34s} {(g2+'/'+s2)[:34]:34s} {d:6.3f}")
    sv = sorted(d for *_, d in same)
    if sv:
        print(f"\nsame-author cross-sample distance: min {sv[0]:.3f}, "
              f"median {sv[len(sv)//2]:.3f}, max {sv[-1]:.3f}  (n={len(sv)})")

    # --- different author, and the candidate ------------------------------
    print("\n\nDISTANCE FROM JUNIUS on the SAME fixed variable set")
    print(f"{'rank':>4s}  {'author':20s} {'sample':38s} {'tokens':>8s} {'dist':>6s}")
    print("-" * 84)
    rows = []
    for (a, g, s), c in big.items():
        if a in ("Junius", "Philo_Junius"):
            continue
        d = dist(jp, profile(c, variables), variables)
        if d is None:
            continue
        rows.append((a, f"{g}/{s}", sum(c.values()), d))
    rows.sort(key=lambda r: r[3])
    for i, (a, s, n, d) in enumerate(rows, 1):
        mark = "   <-- CANDIDATE" if a == "Philip_Francis" else ""
        print(f"{i:4d}  {a:20s} {s[:38]:38s} {n:8d} {d:6.3f}{mark}")

    fr = [r for r in rows if r[0] == "Philip_Francis"]
    print()
    for a, s, n, d in fr:
        closer = sum(1 for r in rows if r[3] < d)
        print(f"Francis ({s}): distance {d:.3f}; rank {closer+1} of {len(rows)}; "
              f"{closer} period writers closer to Junius.")
        if sv:
            inside = sum(1 for x in sv if x >= d)
            print(f"  same-author cross-sample distances at or above it: {inside}/{len(sv)}"
                  f"  -> this distance is {'NOT' if inside == 0 else ''} "
                  f"{'distinguishable from' if inside else 'typical of'} "
                  f"{'a same-author pair' if inside else 'same-author variation'}")

    json.dump(dict(variables=variables,
                   same_author=[dict(author=a, a=x, b=y, distance=round(d, 4))
                                for a, x, y, d in same],
                   from_junius=[dict(author=a, sample=s, tokens=n, distance=round(d, 4))
                                for a, s, n, d in rows]),
              open(os.path.join(RES, "calibration.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
