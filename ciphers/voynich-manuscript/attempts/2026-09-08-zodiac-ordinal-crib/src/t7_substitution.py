#!/usr/bin/env python3
"""T7: is the early/late zodiac-label regime difference ONE systematic substitution?

Design
------
1. Changepoint scan over the derived zodiac order (all 11 splits) on the label
   a/(a+e) profile, with a permutation null over diagram order.
2. Divergence decomposition. JSD between early-label and late-label glyph-bigram
   distributions, computed (a) raw, (b) after collapsing a candidate glyph pair.
   Baseline = JSD between random halves WITHIN each regime. If the collapse takes the
   cross-regime divergence down to the within-regime baseline, the two regimes are the
   same system under one substitution.
3. Every glyph pair is tried, so the a/e result is scored against its own search budget.
4. Type-overlap test: does mapping late labels through the substitution hit early label
   types more than the same map applied to matched ring-text words?
"""
import sys, os, math, random, itertools, collections, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
from t6_regime import ORDER, SIGN, spearman, perm_p, collect

GLYPHS = "otkpfcshdlrneaiqygxvmzu*"


def bigrams(words):
    c = collections.Counter()
    for w in words:
        s = "^" + w + "$"
        for i in range(len(s) - 1):
            c[s[i:i + 2]] += 1
    return c


def jsd(p, q):
    keys = set(p) | set(q)
    tp, tq = sum(p.values()), sum(q.values())
    if not tp or not tq:
        return float('nan')
    out = 0.0
    for k in keys:
        a, b = p.get(k, 0) / tp, q.get(k, 0) / tq
        m = (a + b) / 2
        if a: out += 0.5 * a * math.log2(a / m)
        if b: out += 0.5 * b * math.log2(b / m)
    return out


def collapse(words, x, y):
    """Merge glyph y into glyph x."""
    return [w.replace(y, x) for w in words]


def main():
    rows = L.load()
    lab, ring = collect(rows)
    labs = [lab[f] for f in ORDER]
    rings = [ring[f] for f in ORDER]

    # ---- 1. changepoint ----
    def a_ratio(ws):
        s = ''.join(ws); a, e = s.count('a'), s.count('e')
        return a / (a + e) if a + e else float('nan')
    prof = [a_ratio(x) for x in labs]

    def cp_stat(profile, k):
        lo, hi = profile[:k], profile[k:]
        return abs(sum(lo) / len(lo) - sum(hi) / len(hi))

    best = max(range(1, 12), key=lambda k: cp_stat(prof, k))
    obs = cp_stat(prof, best)
    rng = random.Random(3)
    pp = list(prof)
    cnt = 0
    NP = 200000
    for _ in range(NP):
        rng.shuffle(pp)
        if max(cp_stat(pp, k) for k in range(1, 12)) >= obs - 1e-12:
            cnt += 1
    print(f"== T7.1 changepoint ==\n  best split after diagram {best} ({SIGN[best-1]} | {SIGN[best]})"
          f"  gap={obs:.3f}  max-over-splits perm p = {(cnt+1)/(NP+1):.5f}")

    early = [w for x in labs[:best] for w in x]
    late = [w for x in labs[best:] for w in x]
    print(f"  early labels n={len(early)}  late labels n={len(late)}")

    # ---- 2/3. collapse scan ----
    def within_baseline(words, seed=5, reps=200):
        r = random.Random(seed)
        vals = []
        for _ in range(reps):
            w = list(words); r.shuffle(w)
            h = len(w) // 2
            vals.append(jsd(bigrams(w[:h]), bigrams(w[h:])))
        vals.sort()
        return sum(vals) / len(vals), vals[int(.95 * len(vals))]

    raw = jsd(bigrams(early), bigrams(late))
    be_m, be_95 = within_baseline(early, 5)
    bl_m, bl_95 = within_baseline(late, 6)
    base = (be_m + bl_m) / 2
    base95 = max(be_95, bl_95)
    print(f"\n== T7.2 divergence ==\n  raw cross-regime JSD            = {raw:.4f}")
    print(f"  within-regime baseline JSD mean = {base:.4f}   (95th pct {base95:.4f})")

    results = []
    for x, y in itertools.combinations(GLYPHS, 2):
        e2, l2 = collapse(early, x, y), collapse(late, x, y)
        d = jsd(bigrams(e2), bigrams(l2))
        b1, _ = within_baseline(e2, 5, 60)
        b2, _ = within_baseline(l2, 6, 60)
        results.append((d, (b1 + b2) / 2, x, y))
    results.sort(key=lambda t: t[0])
    print("\n  best glyph collapses (cross-regime JSD after merging y into x):")
    print(f"  {'pair':8s} {'crossJSD':>9s} {'withinJSD':>10s} {'excess':>8s} {'raw->':>8s}")
    for d, b, x, y in results[:12]:
        print(f"  {x+'/'+y:8s} {d:9.4f} {b:10.4f} {d-b:8.4f} {raw-d:8.4f}")
    print(f"  ... median cross-regime JSD over all {len(results)} pairs = "
          f"{sorted(r[0] for r in results)[len(results)//2]:.4f}")

    # ---- 4. type-overlap under the substitution ----
    def norm(ws, rules):
        out = []
        for w in ws:
            for a, b in rules:
                w = w.replace(a, b)
            out.append(w)
        return out

    RULES = [("eo", "a"), ("ee", "a"), ("e", "a")]
    E = set(early)
    rawhit = sum(1 for w in late if w in E) / len(late)
    En = set(norm(early, RULES))
    Ln = norm(late, RULES)
    subhit = sum(1 for w in Ln if w in En) / len(Ln)
    ringlate = [w for x in rings[best:] for w in x]
    Rn = norm(ringlate, RULES)
    ctrlhit = sum(1 for w in Rn if w in En) / len(Rn)
    ringearly = [w for x in rings[:best] for w in x]
    ctrl2 = sum(1 for w in norm(ringearly, RULES) if w in En) / len(ringearly)
    print(f"\n== T7.4 type overlap ==")
    print(f"  late labels matching an early label type, raw           = {rawhit:.3f}")
    print(f"  ... after e/ee/eo -> a normalisation                    = {subhit:.3f}")
    print(f"  same map applied to LATE ring-text words (control)      = {ctrlhit:.3f}")
    print(f"  same map applied to EARLY ring-text words (control)     = {ctrl2:.3f}")

    json.dump({"changepoint": best, "raw_jsd": raw, "baseline": base,
               "top_collapses": [(x, y, d, b) for d, b, x, y in results[:20]],
               "overlap": {"raw": rawhit, "sub": subhit, "ctrl_late_ring": ctrlhit,
                           "ctrl_early_ring": ctrl2}},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                                'results', 't7_substitution.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
