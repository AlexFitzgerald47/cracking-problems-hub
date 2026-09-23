"""Within-witness doublet detection.

O'Rahilly's two-Patricks argument rests on the annals recording Patrick's
obit more than once -- an "elder Patrick" at AU 457, "here some record the
repose of Patrick" at AU 461, and the death of Patrick again at AU 492/493.
The inference only works if a duplicated obit is *unusual*.  Nobody appears to
have measured how unusual it is, so that is what this does: the same validated
cross-witness matcher, turned on a single witness against itself, counting
pairs of entries that record the same notice at different years.

A doublet here is: two entries in the SAME witness, years differing by
LAG_MIN..LAG_MAX, sharing at least one rare token and scoring at or above the
cosine threshold, under mutual-best matching.
"""
import sys, json, collections
from common import load, idf, vec, cos, norm_tokens, WITNESSES
from match import THRESH, DF_MAX

LAG_MIN, LAG_MAX = 1, 60


def build(entries):
    idfmap = idf(entries)
    df = collections.Counter()
    for e in entries:
        df.update(set(norm_tokens(e["text"])))
    by_w = collections.defaultdict(list)
    for e in entries:
        if e["is_kalend"] and e["n_words"] < 25:
            continue
        e = dict(e)
        e["v"] = vec(e["text"], idfmap)
        e["rare"] = frozenset(w for w in e["v"] if df[w] <= DF_MAX)
        by_w[e["witness"]].append(e)
    return by_w


def self_matches(E, lag_min=LAG_MIN, lag_max=LAG_MAX, thresh=THRESH):
    byyear = collections.defaultdict(list)
    for e in E:
        byyear[e["year"]].append(e)
    cand = collections.defaultdict(dict)
    for a in E:
        for y in range(a["year"] + lag_min, a["year"] + lag_max + 1):
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
    return [(a, b, round(s, 4)) for a, (b, s) in best_a.items()
            if best_b.get(b, (None,))[0] == a]


def main(inp, outp):
    entries = load(inp)
    by_w = build(entries)
    out = {}
    for w in WITNESSES:
        m = self_matches(by_w[w])
        out[w] = m
        print("%s: entries=%4d  doublet pairs=%3d  (%.3f of entries involved)"
              % (w, len(by_w[w]), len(m),
                 len({x for p in m for x in p[:2]}) / max(1, len(by_w[w]))))
    json.dump(out, open(outp, "w"), indent=0)
    print("wrote", outp)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
