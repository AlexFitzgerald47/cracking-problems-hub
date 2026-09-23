"""Cross-witness event matching.

For every ordered pair of witnesses we align entries by IDF-weighted cosine
similarity inside a year window, then keep only mutual best matches above a
threshold.  The output is the raw material for two questions:

  * the collation itself (which witnesses attest which event), and
  * the *inter-witness date dispersion* of matched events, which is the
    quantity the Patrician test turns on.

Validation: the matcher is never told that AU runs one year ahead of true AD
before 1014.  If it works, that offset has to fall out of the modal year
difference of matched pairs.
"""
import sys, json, collections
from common import load, idf, vec, cos, norm_tokens, WITNESSES

WINDOW = 12          # +/- years searched for a partner
THRESH = 0.30        # cosine floor for a candidate match
DF_MAX = 50          # a match must share >=1 token this rare (a distinctive
                     # name), or purely formulaic notices pair up with each
                     # other -- and those false pairs land at large year
                     # offsets, which is exactly the statistic under test.


def build(entries):
    idfmap = idf(entries)
    df = collections.Counter()
    for e in entries:
        df.update(set(norm_tokens(e["text"])))
    by_w = collections.defaultdict(list)
    for e in entries:
        if e["is_kalend"] and e["n_words"] < 25:
            continue                      # pure chronological apparatus
        e = dict(e)
        e["v"] = vec(e["text"], idfmap)
        e["rare"] = frozenset(w for w in e["v"] if df[w] <= DF_MAX)
        by_w[e["witness"]].append(e)
    return by_w


def pair_matches(A, B, window=WINDOW, thresh=THRESH):
    """Mutual-best matching between two witnesses' entry lists."""
    byyear = collections.defaultdict(list)
    for e in B:
        byyear[e["year"]].append(e)
    cand = collections.defaultdict(dict)   # a_id -> {b_id: score}
    for a in A:
        for y in range(a["year"] - window, a["year"] + window + 1):
            for b in byyear.get(y, ()):
                if not (a["rare"] & b["rare"]):
                    continue
                s = cos(a["v"], b["v"])
                if s >= thresh:
                    cand[a["id"]][b["id"]] = s
    best_a = {aid: max(d.items(), key=lambda kv: kv[1]) for aid, d in cand.items()}
    rev = collections.defaultdict(dict)
    for aid, d in cand.items():
        for bid, s in d.items():
            rev[bid][aid] = s
    best_b = {bid: max(d.items(), key=lambda kv: kv[1]) for bid, d in rev.items()}
    out = []
    for aid, (bid, s) in best_a.items():
        if best_b.get(bid, (None,))[0] == aid:
            out.append((aid, bid, round(s, 4)))
    return out


def main(inp, outp):
    entries = load(inp)
    by_w = build(entries)
    index = {e["id"]: e for w in by_w for e in by_w[w]}
    res = {}
    for i, X in enumerate(WITNESSES):
        for Y in WITNESSES[i + 1:]:
            m = pair_matches(by_w[X], by_w[Y])
            res["%s-%s" % (X, Y)] = m
            offs = collections.Counter(index[a]["year"] - index[b]["year"] for a, b, _ in m)
            print("%s-%s  matches=%4d  modal year offset=%+d (n=%d)  |off|<=1: %.3f"
                  % (X, Y, len(m), offs.most_common(1)[0][0], offs.most_common(1)[0][1],
                     sum(c for o, c in offs.items() if abs(o) <= 1) / max(1, len(m))))
    json.dump(res, open(outp, "w"), indent=0)
    print("wrote", outp)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
