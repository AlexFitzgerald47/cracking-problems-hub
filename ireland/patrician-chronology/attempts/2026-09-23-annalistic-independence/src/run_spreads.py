"""Analysis 2: how far apart are the compiler's own alternative datings?

O'Rahilly's two-Patricks argument needs the annalistic spread between the
Patrician death-dates to be anomalous.  The corpus contains a ready-made
comparison class: every event the compilers themselves flagged with an
alternative-source marker has, by construction, at least two candidate years.
Pair each flagged entry with its counterpart and the spreads are measurable.

Pairing rule (fixed before any Patrician number was computed from it): for a
marked entry M in witness W, the counterpart is the entry of W, within +/-60
years and not in the same year, that maximises IDF-cosine subject to sharing at
least one token with corpus document frequency <= 50.  Every pair produced is
hand-audited in results/spread_audit.txt; only ACCEPTED pairs enter the
distribution.
"""
import sys, json, collections
from common import load, idf, vec, cos, norm_tokens
from markers import is_marked, PATRICIAN, MARKER
from match import DF_MAX

MAXLAG = 60
THRESH = 0.28


def main(inp, outp, dump):
    E = load(inp)
    # The marker phrase itself is shared vocabulary across every marked entry.
    # Left in, it pairs "Some books state that Maine son of Niall perished" with
    # "Repose of the elder Patrick, as some books state" on the formula alone.
    # Strip it before vectorising; keep it for classification.
    for e in E:
        e["body"] = MARKER.sub(" ", e["text"])
    idfmap = idf([{"text": e["body"]} for e in E])
    df = collections.Counter()
    for e in E:
        df.update(set(norm_tokens(e["body"])))
    for e in E:
        e["v"] = vec(e["body"], idfmap)
        e["rare"] = frozenset(w for w in e["v"] if df[w] <= DF_MAX)
    by_w = collections.defaultdict(list)
    for e in E:
        by_w[e["witness"]].append(e)

    pairs = []
    for e in E:
        if not is_marked(e["text"]):
            continue
        best = (None, 0.0)
        for o in by_w[e["witness"]]:
            if o["id"] == e["id"] or o["year"] == e["year"]:
                continue
            if abs(o["year"] - e["year"]) > MAXLAG:
                continue
            if not (e["rare"] & o["rare"]):
                continue
            s = cos(e["v"], o["v"])
            if s > best[1]:
                best = (o, s)
        if best[0] is not None and best[1] >= THRESH:
            o = best[0]
            pairs.append({"witness": e["witness"], "marked": e["id"], "other": o["id"],
                          "y1": e["year"], "y2": o["year"],
                          "spread": abs(e["year"] - o["year"]),
                          "score": round(best[1], 3),
                          "patrician": bool(PATRICIAN.search(e["text"]) or PATRICIAN.search(o["text"])),
                          "t1": e["text"][:200], "t2": o["text"][:200]})
    pairs.sort(key=lambda p: (p["witness"], p["y1"]))
    with open(dump, "w") as f:
        for p in pairs:
            f.write("%-3s spread=%2d score=%.2f %s%s\n   %s (%d): %s\n   %s (%d): %s\n\n"
                    % (p["witness"], p["spread"], p["score"], p["marked"],
                       "  [PATRICIAN]" if p["patrician"] else "",
                       p["marked"], p["y1"], p["t1"], p["other"], p["y2"], p["t2"]))
    json.dump(pairs, open(outp, "w"), indent=1)
    print("candidate pairs: %d  (%d Patrician)" % (len(pairs), sum(p["patrician"] for p in pairs)))
    sp = sorted(p["spread"] for p in pairs)
    print("spread distribution (all candidates, pre-audit): median %d  90th pct %d  max %d"
          % (sp[len(sp) // 2], sp[int(0.9 * len(sp))], sp[-1]))
    print("wrote", outp, dump)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
