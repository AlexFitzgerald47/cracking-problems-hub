#!/usr/bin/env python3
"""The candidate scorecard: where does Philip Francis rank among period writers on
the synonym-choice variables, and is that rank distinguishable from chance?

Three numbers decide whether a shared preference is evidence, and the traditional
Junius argument reports only the first:

  1. the distance between Junius and the candidate;
  2. the distance between Junius and every OTHER writer of the period -- the
     competitor count, which supplies the denominator the argument lacks;
  3. the distance between two samples of a SINGLE author -- the calibration, without
     which no distance can be called small.

(3) is the one people skip. A Junius-to-Francis distance is only impressive if it is
of the size that two halves of one writer's own output produce. We measure that by
splitting each panel author's documents in half and scoring half against half.

Variables are restricted to those that survived the genre control in genre_effect.py:
a variable that moves as much between one author's two registers as it does between
two authors cannot speak to authorship here, because Junius and Francis are attested
in different registers.
"""
import json, os, random, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C
from synonym_test import PAIRS

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
MIN_JOINT = 25
SEED = 20260917


def prop(counter, a, b, min_joint=MIN_JOINT):
    n = counter[a] + counter[b]
    return (counter[a] / n) if n >= min_joint else None


def load_cells():
    """(author, genre) -> list of per-document token Counters."""
    cells = defaultdict(list)
    for name in ("panel_chunks.jsonl", "junius_1772_wikisource.jsonl", "junius_1813_ocr.jsonl"):
        path = os.path.join(HERE, "..", "data", "corpus", name)
        if not os.path.exists(path):
            continue
        for d in C.load_jsonl(name):
            src = d.get("source", "")
            key = (d["author"], d["genre"], "wikisource_1772" if "wikisource" in src
                   else ("junius_1813" if "1813" in src else "panel"))
            cells[key].append(Counter(C.tokens(d["text"])))
    return cells


def pooled(counters):
    tot = Counter()
    for c in counters:
        tot.update(c)
    return tot


def profile(counters, variables):
    c = pooled(counters)
    return {v: prop(c, *v.split("/")) for v in variables}


def distance(p, q):
    """Mean absolute difference over variables both profiles can measure."""
    shared = [v for v in p if p[v] is not None and q.get(v) is not None]
    if len(shared) < 3:
        return None, len(shared)
    return sum(abs(p[v] - q[v]) for v in shared) / len(shared), len(shared)


def main():
    os.makedirs(RES, exist_ok=True)
    ge = json.load(open(os.path.join(RES, "genre_effect.json")))
    variables = [v for v, d in ge.items() if d["verdict"] == "usable"]
    print(f"Variables surviving the genre control ({len(variables)}): {', '.join(variables)}\n")

    cells = load_cells()
    # Junius reference profile: the public letters, pooling both digitisations
    jun_docs = []
    for (a, g, s), docs in cells.items():
        if a == "Junius":
            jun_docs += docs
    jun = profile(jun_docs, variables)
    print("Junius (public letters, both digitisations pooled):")
    for v in variables:
        print(f"   {v:20s} {jun[v] if jun[v] is None else round(jun[v],3)}")
    print()

    # ---- (2) competitor table -------------------------------------------
    rows = []
    for (a, g, s), docs in sorted(cells.items()):
        if a in ("Junius", "Philo_Junius"):
            continue
        p = profile(docs, variables)
        d, k = distance(jun, p)
        if d is None:
            continue
        rows.append(dict(author=a, genre=g, n_docs=len(docs),
                         n_tokens=sum(sum(c.values()) for c in docs),
                         distance=round(d, 4), n_vars=k))
    rows.sort(key=lambda r: r["distance"])

    print("DISTANCE FROM JUNIUS -- every panel author, nearest first")
    print(f"{'rank':>4s}  {'author':22s} {'genre':16s} {'tokens':>8s} {'vars':>4s} {'distance':>8s}")
    print("-" * 70)
    for i, r in enumerate(rows, 1):
        mark = "  <-- the candidate" if r["author"] == "Philip_Francis" else ""
        print(f"{i:4d}  {r['author']:22s} {r['genre']:16s} {r['n_tokens']:8d} "
              f"{r['n_vars']:4d} {r['distance']:8.3f}{mark}")

    # ---- (3) within-author calibration ----------------------------------
    rnd = random.Random(SEED)
    within = []
    for (a, g, s), docs in sorted(cells.items()):
        if len(docs) < 8:
            continue
        d2 = list(docs)
        rnd.shuffle(d2)
        h = len(d2) // 2
        p1, p2 = profile(d2[:h], variables), profile(d2[h:], variables)
        d, k = distance(p1, p2)
        if d is not None:
            within.append((f"{a} ({g})", round(d, 4), k))
    within.sort(key=lambda x: x[1])
    print(f"\n\nWITHIN-AUTHOR CALIBRATION -- one author's own documents, split in half")
    print(f"{'author (genre)':42s} {'vars':>4s} {'distance':>8s}")
    print("-" * 58)
    for name, d, k in within:
        print(f"{name:42s} {k:4d} {d:8.3f}")
    wvals = [d for _, d, _ in within]
    if wvals:
        wmed = sorted(wvals)[len(wvals) // 2]
        wmax = max(wvals)
        print(f"\nwithin-author distance: median {wmed:.3f}, max {wmax:.3f}")

        fr = [r for r in rows if r["author"] == "Philip_Francis"]
        print("\nVERDICT INPUTS")
        for r in fr:
            closer = sum(1 for x in rows if x["distance"] < r["distance"])
            print(f"  Francis ({r['genre']}): distance {r['distance']:.3f}, "
                  f"rank {closer+1} of {len(rows)}, "
                  f"{closer} period writers closer to Junius than the candidate is.")
            print(f"    within-author distances run up to {wmax:.3f}; the candidate's "
                  f"distance is {'INSIDE' if r['distance'] <= wmax else 'OUTSIDE'} that range.")

    json.dump(dict(variables=variables, junius=jun, competitors=rows,
                   within_author=[dict(cell=n, distance=d, n_vars=k) for n, d, k in within]),
              open(os.path.join(RES, "scorecard.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
