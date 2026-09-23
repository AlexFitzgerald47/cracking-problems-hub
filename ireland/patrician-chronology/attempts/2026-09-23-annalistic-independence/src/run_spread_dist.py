"""The comparison distribution: how far apart are the annals' own alternative
datings, in the stratum where they make them?

Then: where does the Patrician obit sit against it?
"""
import sys, json, collections
from common import load
from markers import is_marked, PATRICIAN, MARKER
from audit_verdicts import ACCEPT, REJECT, ADDED, CANON_DROP


def main(inp, outp):
    E = load(inp)
    idx = {e["id"]: e for e in E}
    pairs = {}
    for a, b in list(ACCEPT.items()) + list(ADDED.items()):
        if a in CANON_DROP:
            continue
        pairs[a] = b
    rows = []
    for a, b in pairs.items():
        ya, yb = idx[a]["year"], idx[b]["year"]
        rows.append({"marked": a, "other": b, "y1": ya, "y2": yb,
                     "spread": abs(ya - yb), "witness": idx[a]["witness"],
                     "patrician": bool(PATRICIAN.search(idx[a]["text"])
                                       or PATRICIAN.search(idx[b]["text"])),
                     "t1": MARKER.sub("[MK]", idx[a]["text"])[:150],
                     "t2": idx[b]["text"][:150]})
    rows.sort(key=lambda r: r["spread"])
    sp = [r["spread"] for r in rows]
    n = len(sp)
    print("accepted alternative-dating pairs: %d  (rejected %d, hand-added %d)"
          % (n, len(REJECT), len(ADDED)))
    print("spreads:", sp)
    print("median %d   75th %d   90th %d   max %d"
          % (sp[n // 2], sp[int(0.75 * n)], sp[int(0.90 * n)], sp[-1]))
    early = [r for r in rows if r["y1"] < 700]
    se = sorted(r["spread"] for r in early)
    print("restricted to the pre-700 stratum (n=%d): median %d  90th %d  max %d"
          % (len(se), se[len(se) // 2], se[int(0.90 * len(se))], se[-1]))
    print("\nlargest five:")
    for r in rows[-5:]:
        print("  %-3s %d vs %d  spread %2d  %s | %s"
              % (r["witness"], r["y1"], r["y2"], r["spread"], r["t1"][:70], r["t2"][:70]))

    # --- the Patrician obit ---
    pat_ob = [e for e in E if PATRICIAN.search(e["text"])
              and 430 <= e["year"] <= 500
              and any(k in e["text"].lower() for k in
                      ("repose", "died", "death", "rested", "quievit", "falling asleep"))]
    print("\nPatrician obit notices, 430-500, all witnesses:")
    for e in sorted(pat_ob, key=lambda x: (x["year"], x["witness"])):
        print("  %-3s %4d %-11s %s%s" % (e["witness"], e["year"], e["id"],
                                         "[MARKED] " if is_marked(e["text"]) else "",
                                         e["text"][:130]))
    au = sorted(e["year"] for e in pat_ob if e["witness"] == "AU")
    allw = sorted(e["year"] for e in pat_ob)
    print("\n  AU candidate obit years: %s  -> within-witness spread %d" % (au, max(au) - min(au)))
    print("  all witnesses          : %s  -> spread %d" % (allw, max(allw) - min(allw)))
    ps = max(au) - min(au)
    ge = sum(1 for s in sp if s >= ps)
    ge_e = sum(1 for s in se if s >= ps)
    print("\n  comparison pairs with spread >= %d : %d/%d = %.3f (whole corpus)"
          % (ps, ge, n, ge / n))
    print("  comparison pairs with spread >= %d : %d/%d = %.3f (pre-700 stratum)"
          % (ps, ge_e, len(se), ge_e / len(se)))
    json.dump({"pairs": rows, "spreads": sp, "n": n,
               "patrician_AU_years": au, "patrician_all_years": allw,
               "patrician_AU_spread": ps,
               "frac_ge_corpus": ge / n, "frac_ge_pre700": ge_e / len(se)},
              open(outp, "w"), indent=1)
    print("\nwrote", outp)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
