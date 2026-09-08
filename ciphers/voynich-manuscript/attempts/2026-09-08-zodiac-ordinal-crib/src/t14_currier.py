#!/usr/bin/env python3
"""T14: is the Currier A/B difference in RUNNING TEXT the same glyph substitution that
separates the two zodiac-label regimes?

Finding 1b of this attempt showed that merging EVA `e` into `a` is, of all 276 glyph
pairs, the single best at closing the divergence between the early and late zodiac
label regimes. Currier A/B is the manuscript's other big register split, and A is
`a`-heavy where B is `e`-heavy. If one substitution accounts for both, that is a
statement about the writing system, not about two languages.

Method (same shape as T7, applied to running text):
  - page -> Currier language from OrcusLabs/voynich.science mappings_TTLI.json
  - divergence = JSD of glyph-bigram distributions, A pages vs B pages
  - baseline   = JSD between two random halves of the SAME language, split BY PAGE
  - collapse every glyph pair in turn, rescore, and rank
  - sample sizes matched by subsampling the larger side to the smaller
"""
import sys, os, json, math, random, itertools, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
from t7_substitution import bigrams, jsd, collapse, GLYPHS

MAP = os.environ.get("VMS_TTLI",
    "/tmp/claude-0/-home-user-cracking-problems-hub/634aa923-677e-5dc9-9564-f7bc199c0972/"
    "scratchpad/voynich.science/mappings_TTLI.json")


def page_languages():
    d = json.load(open(MAP))
    pages = {}
    for w, v in d["words"].items():
        for o in v.get("occurrences", []):
            lg = o.get("currier_language")
            if lg in ("A", "B"):
                pages.setdefault(o["folio"], collections.Counter())[lg] += 1
    return {f: c.most_common(1)[0][0] for f, c in pages.items()}


def main():
    rows = L.load()
    lang = page_languages()
    print(f"page language map: {len(lang)} pages "
          f"({sum(1 for v in lang.values() if v=='A')} A, "
          f"{sum(1 for v in lang.values() if v=='B')} B)")
    # pipeline check against a fact the map was not asked about
    print(f"  check: f1r -> {lang.get('f1r')} (expect A); f75r -> {lang.get('f75r')} (expect B)")

    byp = {}
    for r in rows:
        if r["ltype"] == "P" and r["words"] and r["folio"] in lang:
            byp.setdefault(r["folio"], []).extend(r["words"])
    A = {f: w for f, w in byp.items() if lang[f] == "A"}
    B = {f: w for f, w in byp.items() if lang[f] == "B"}
    print(f"running text: A {len(A)} pages / {sum(len(v) for v in A.values())} tokens; "
          f"B {len(B)} pages / {sum(len(v) for v in B.values())} tokens\n")

    rng = random.Random(20260908)

    def sample(pagedict, ntok):
        fs = list(pagedict); rng.shuffle(fs)
        out = []
        for f in fs:
            out += pagedict[f]
            if len(out) >= ntok:
                break
        return out[:ntok]

    ntok = min(sum(len(v) for v in A.values()), sum(len(v) for v in B.values()))

    def cross(rules=None):
        a, b = sample(A, ntok), sample(B, ntok)
        if rules:
            x, y = rules
            a, b = collapse(a, x, y), collapse(b, x, y)
        return jsd(bigrams(a), bigrams(b))

    def baseline(pagedict, rules=None, reps=40):
        fs = list(pagedict)
        vals = []
        for _ in range(reps):
            rng.shuffle(fs)
            h = len(fs) // 2
            p = [w for f in fs[:h] for w in pagedict[f]]
            q = [w for f in fs[h:] for w in pagedict[f]]
            n = min(len(p), len(q), ntok)
            p, q = p[:n], q[:n]
            if rules:
                x, y = rules
                p, q = collapse(p, x, y), collapse(q, x, y)
            vals.append(jsd(bigrams(p), bigrams(q)))
        return sum(vals) / len(vals)

    raw = cross()
    bA, bB = baseline(A), baseline(B)
    print(f"raw A-vs-B bigram JSD           = {raw:.4f}")
    print(f"within-A baseline (page halves) = {bA:.4f}")
    print(f"within-B baseline (page halves) = {bB:.4f}")
    print(f"excess over baseline            = {raw - (bA+bB)/2:.4f}\n")

    res = []
    for x, y in itertools.combinations(GLYPHS, 2):
        d = cross((x, y))
        res.append((d, x, y))
    res.sort()
    print(f"best glyph collapses out of {len(res)} (A-vs-B JSD after merging y into x):")
    print(f"  {'pair':8s} {'A-vs-B JSD':>11s} {'gap closed':>11s} {'within-A':>9s} {'excess':>8s}")
    for d, x, y in res[:10]:
        ba = baseline(A, (x, y), 12); bb = baseline(B, (x, y), 12)
        print(f"  {x+'/'+y:8s} {d:11.4f} {(raw-d)/(raw-(bA+bB)/2)*100:10.1f}% "
              f"{ba:9.4f} {d-(ba+bb)/2:8.4f}")
    print(f"  median over all pairs = {res[len(res)//2][0]:.4f}")

    # where does e/a rank?
    for i, (d, x, y) in enumerate(res, 1):
        if {x, y} == {"e", "a"}:
            print(f"\n  e/a collapse rank = {i} of {len(res)}, JSD {d:.4f}")

    json.dump({"raw": raw, "baseline_A": bA, "baseline_B": bB,
               "top": [(x, y, d) for d, x, y in res[:25]]},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                                'results', 't14_currier.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
