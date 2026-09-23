"""P2, the strong frozen prediction, tested on the holdout.

P2: no non-Patrician AFM cluster will have a consecutive gap of 31 years or
more.  It fails.
"""
import sys, json

def load(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"): continue
        name, years, span, maxgap, cross = line.split("\t")
        ys = [int(y) for y in years.split(",")]
        assert max(ys) - min(ys) == int(span), name
        gaps = [b - a for a, b in zip(ys, ys[1:])]
        assert max(gaps) == int(maxgap), name
        out.append({"event": name, "years": ys, "span": max(ys) - min(ys),
                    "maxgap": max(gaps), "cross": cross})
    return out

def main(path, outp):
    C = load(path)
    gaps = sorted(c["maxgap"] for c in C)
    print("AFM holdout class: %d non-Patrician duplicate-dating clusters, 430-760" % len(C))
    print("  maxgaps: %s" % gaps)
    P = [457, 493]          # AFM: 'Old Patrick yielded his spirit' / 'Patrick ... archbishop'
    pg = P[1] - P[0]
    print("  AFM Patrician obit: %s -> gap %d" % (P, pg))
    ge31 = [c for c in C if c["maxgap"] >= 31]
    print("\nP2 predicted: no non-Patrician cluster reaches 31.")
    print("P2 RESULT: %s -- %d cluster(s) reach 31:" % ("FAIL" if ge31 else "PASS", len(ge31)))
    for c in ge31:
        print("   %s  years %s  gap %d   [other witnesses: %s]"
              % (c["event"], c["years"], c["maxgap"], c["cross"]))
    print("\n  clusters with maxgap >= AFM Patrician gap (%d): %d/%d"
          % (pg, sum(1 for g in gaps if g >= pg), len(gaps)))
    print("  clusters with maxgap >= developed-class Patrician gap (31): %d/%d"
          % (sum(1 for g in gaps if g >= 31), len(gaps)))
    print("\n  power note: with n=%d the smallest excess this class could have called" % len(C))
    print("  significant at the 1-in-%d level is simply 'larger than every member'," % len(C))
    print("  i.e. larger than %d. The developed class (n=40, max 25) was the sharper" % max(gaps))
    print("  instrument and it is the one the holdout contradicts.")
    json.dump({"clusters": C, "maxgaps": gaps, "afm_patrick": P, "afm_patrick_gap": pg,
               "P2": "FAIL", "refuters": ge31}, open(outp, "w"), indent=1)
    print("\nwrote", outp)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
