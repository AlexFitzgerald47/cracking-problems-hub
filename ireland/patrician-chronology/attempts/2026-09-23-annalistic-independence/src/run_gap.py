"""The statistic: the largest gap between consecutive variant datings.

O'Rahilly's premise is that the annals preserve two Patricks.  The annals'
own behaviour supplies a comparison class: every fifth-to-seventh-century
event for which AU offers more than one year.  If Patrick's variant years are
ordinary annalistic scatter, his largest consecutive gap should sit inside that
class's distribution.  If they are two traditions merged, it should not.

Span (max - min) and maxgap (largest consecutive step) are reported separately
because they say different things: a wide span with small steps is scatter, a
wide step is a discontinuity.
"""
import sys, json


def load_clusters(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        wit, name, years, span, maxgap = line.split("\t")
        ys = [int(y) for y in years.split(",")]
        assert max(ys) - min(ys) == int(span), name
        gaps = [b - a for a, b in zip(ys, ys[1:])]
        assert max(gaps) == int(maxgap), name
        out.append({"witness": wit, "event": name, "years": ys, "span": max(ys) - min(ys),
                    "maxgap": max(gaps), "n_years": len(ys)})
    return out


def pct_ge(vals, x):
    return sum(1 for v in vals if v >= x), len(vals)


def main(clusters_path, outp):
    C = load_clusters(clusters_path)
    spans = sorted(c["span"] for c in C)
    gaps = sorted(c["maxgap"] for c in C)
    n = len(C)
    print("comparison class: %d hand-verified alternative-dating clusters, AU/AT/CS/AI 430-760" % n)
    print("  variant years per cluster: %s" % sorted(c["n_years"] for c in C))
    print("  span   median %d  75th %d  90th %d  max %d  (%s)"
          % (spans[n // 2], spans[int(.75 * n)], spans[int(.90 * n)], spans[-1],
             max(C, key=lambda c: c["span"])["event"]))
    print("  maxgap median %d  75th %d  90th %d  max %d  (%s)"
          % (gaps[n // 2], gaps[int(.75 * n)], gaps[int(.90 * n)], gaps[-1],
             max(C, key=lambda c: c["maxgap"])["event"]))

    # Patrick's obit in AU: 457 (marked), 461 (marked), 492, 493
    P = [457, 461, 492, 493]
    pspan = max(P) - min(P)
    pgaps = [b - a for a, b in zip(P, P[1:])]
    pmax = max(pgaps)
    print("\nPatrick's obit in AU: years %s" % P)
    print("  span %d   consecutive gaps %s   maxgap %d" % (pspan, pgaps, pmax))
    a, b = pct_ge(spans, pspan)
    print("  clusters with span   >= %2d : %d/%d" % (pspan, a, b))
    a, b = pct_ge(gaps, pmax)
    print("  clusters with maxgap >= %2d : %d/%d" % (pmax, a, b))

    print("\n  within the two Patrician sub-traditions:")
    print("    457-461 : span 4   -> clusters with span >= 4 : %d/%d" % pct_ge(spans, 4))
    print("    492-493 : span 1   -> clusters with span >= 1 : %d/%d" % pct_ge(spans, 1))
    print("  and across all four witnesses the later obit is 489,491,492,493,496:")
    L = [489, 491, 492, 493, 496]
    print("    span %d, maxgap %d -> clusters with maxgap >= %d : %d/%d"
          % (max(L) - min(L), max(b_ - a_ for a_, b_ in zip(L, L[1:])),
             max(b_ - a_ for a_, b_ in zip(L, L[1:])),
             *pct_ge(gaps, max(b_ - a_ for a_, b_ in zip(L, L[1:])))))

    json.dump({"clusters": C, "spans": spans, "maxgaps": gaps,
               "patrick_AU_years": P, "patrick_span": pspan, "patrick_maxgap": pmax,
               "n_clusters": n,
               "clusters_span_ge_patrick": pct_ge(spans, pspan)[0],
               "clusters_maxgap_ge_patrick": pct_ge(gaps, pmax)[0]},
              open(outp, "w"), indent=1)
    print("\nwrote", outp)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
