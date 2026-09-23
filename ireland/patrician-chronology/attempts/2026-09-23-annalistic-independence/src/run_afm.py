"""The holdout: the Annals of the Four Masters.

Tests P1-P5 of FREEZE.md.  P2 is the strong one and it cannot be run by "the
same procedure" as frozen, because that procedure is marker-driven and AFM has
no marker stratum to drive it -- which is itself the P1 result.  The substitute
is stated plainly and is the more demanding of the two available: find every
within-AFM near-duplicate notice in the window by self-matching, hand-audit it,
and report the largest consecutive gap among the survivors.
"""
import sys, json, re, collections
from common import load, idf, vec, cos, norm_tokens
from markers import is_marked, PATRICIAN
from doublet import self_matches
from match import DF_MAX

LO, HI = 430, 760
THRESH = 0.45      # raised from the 0.30 used cross-witness: within one witness
                   # the formulaic floor is much higher, so a low threshold
                   # returns dynastic coincidences (measured at ~1/15 precision).

# AFM carries TWO apparatus lines per year, not one: `.0` is "The Age of
# Christ, 470." and `.1` is the regnal year, "The twelfth year of Oilioll."
# The second is not an event and pairs with every other regnal line in the
# text; left in, it supplied 18 of the 20 widest "duplicates" on the first run.
REGNAL = re.compile(r"^The [a-z ]+ year of [A-Z][^.]*\.?$")


def main(afm_path, outp, dump):
    A = load(afm_path)
    idfmap = idf(A)
    df = collections.Counter()
    for e in A:
        df.update(set(norm_tokens(e["text"])))
    pool = []
    for e in A:
        if not (LO <= e["year"] < HI):
            continue
        if e["is_kalend"] and e["n_words"] < 25:
            continue
        if REGNAL.match(e["text"].strip()) or e["n_words"] < 5:
            continue
        e = dict(e)
        e["v"] = vec(e["text"], idfmap)
        e["rare"] = frozenset(w for w in e["v"] if df[w] <= DF_MAX)
        pool.append(e)
    idx = {e["id"]: e for e in pool}
    m = self_matches(pool, lag_min=1, lag_max=80, thresh=THRESH)
    print("AFM %d-%d: %d entries, %d within-witness near-duplicate pairs at cos>=%.2f"
          % (LO, HI, len(pool), len(m), THRESH))
    rows = []
    with open(dump, "w") as f:
        for a, b, s in sorted(m, key=lambda p: -abs(idx[p[0]]["year"] - idx[p[1]]["year"])):
            gap = abs(idx[a]["year"] - idx[b]["year"])
            pat = bool(PATRICIAN.search(idx[a]["text"]) or PATRICIAN.search(idx[b]["text"]))
            rows.append({"a": a, "b": b, "gap": gap, "score": s, "patrician": pat})
            f.write("gap=%2d score=%.2f%s\n   %s (%d): %s\n   %s (%d): %s\n\n"
                    % (gap, s, "  [PATRICIAN]" if pat else "", a, idx[a]["year"],
                       idx[a]["text"][:200], b, idx[b]["year"], idx[b]["text"][:200]))
    json.dump(rows, open(outp, "w"), indent=1)
    print("wrote", outp, dump)
    for r in rows[:20]:
        print("  gap=%2d cos=%.2f %s / %s%s" % (r["gap"], r["score"], r["a"], r["b"],
                                                "  [PATRICIAN]" if r["patrician"] else ""))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
