#!/usr/bin/env python3
"""T15: manuscript-wide sweep. Is the period-7 ending cycle unique to the zodiac
nymph labels, or a property of every ordered list in the Voynich MS?

Each 'list' is a maximal ordered run of loci of one type on one page. Statistic and
null are exactly those of T12: pooled count of position pairs d apart sharing the
last two glyphs (and, separately, the penultimate glyph), null = permutation within
each list.
"""
import sys, os, json, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
from t12_final import pooled

ZOD = L.ZODIAC_FOLIOS


def folio_num(f):
    d = "".join(ch for ch in f[1:] if ch.isdigit())
    return int(d) if d else 0


def build(rows):
    """Return {group_name: [list_of_strings, ...]}"""
    g = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        if not r["words"]:
            continue
        f, t = r["folio"], r["ltype"]
        n = folio_num(f)
        if f in ZOD and t == "S":
            sec = "zodiac nymph LABELS"
        elif f in ZOD and t == "R":
            sec = "zodiac RING TEXT"
        elif t == "L" and 87 <= n <= 102:
            sec = "pharma LABELS (f88-f102)"
        elif t == "L" and n <= 66:
            sec = "herbal LABELS (f1-f66)"
        elif t == "L" and 67 <= n <= 73:
            sec = "astronomical LABELS (f67-f73)"
        elif t == "L":
            sec = "other LABELS (f74+)"
        elif t == "S":
            sec = "Q20 starred-para FIRST words"
        elif t in ("R", "C", "X", "Y"):
            sec = f"circular/radial text ({t})"
        elif t == "P":
            sec = "running text: para FIRST words"
        else:
            return_sec = None
            continue
        if sec == "Q20 starred-para FIRST words":
            g[sec][f].append((r["lnum"], r["line"], r["words"][0]))
        elif sec == "running text: para FIRST words":
            g[sec][f].append((r["lnum"], r["line"], r["words"][0]))
        else:
            g[sec][(f, r["lnum"])].append((r["line"], "".join(r["words"])))
    out = {}
    for sec, sub in g.items():
        lists = []
        for k, v in sub.items():
            v.sort()
            seq = [x[-1] for x in v]
            if len(seq) >= 8:
                lists.append(seq)
        if lists:
            out[sec] = lists
    # running-text lines: each P line's own word sequence, pages f1-f116
    lines = [r["words"] for r in rows if r["ltype"] == "P" and len(r["words"]) >= 8]
    out["running text: within-line words"] = lines[:400]
    return out


def main():
    rows = L.load()
    groups = build(rows)
    FE = {"last2": lambda w: w[-2:], "penult": lambda w: w[-2:-1]}
    print(f"{'group':33s} {'lists':>5s} {'items':>6s} {'feat':7s} "
          f"{'lag7 obs':>8s} {'/pairs':>6s} {'null':>7s} {'ratio':>6s} {'Z':>7s} {'p':>7s} {'best':>4s}")
    res = {}
    for gname in sorted(groups, key=lambda k: -sum(len(x) for x in groups[k])):
        seqs = groups[gname]
        nit = sum(len(x) for x in seqs)
        for fn, ff in FE.items():
            r = pooled(seqs, ff, maxlag=10, nperm=20000, seed=abs(hash(gname + fn)) % 9999)
            res[gname + "|" + fn] = r
            if 7 not in r:
                continue
            x = r[7]
            best = max(r, key=lambda d: r[d]["z"])
            print(f"{gname:33s} {len(seqs):5d} {nit:6d} {fn:7s} {x['obs']:8d} {x['tot']:6d} "
                  f"{x['null']:7.1f} {x['ratio']:6.2f} {x['z']:+7.2f} {x['p']:7.4f} {best:4d}")
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     '..', 'results', 't15_sweep.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
