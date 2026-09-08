#!/usr/bin/env python3
"""T12: definitive pooled lag battery for the penultimate-glyph / last-2 effect.

Discovery vs confirmation is kept explicit. Lag 7 was selected in T8 from a
7-measure x 14-lag scan on ALL zodiac rings. Everything below is confirmation on
partitions and controls that were not used to pick it.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
from t6_regime import ORDER

NPERM = 40000
FEATS = {"last2": lambda w: w[-2:], "penult": lambda w: w[-2:-1]}


def pooled(seqs, feat, maxlag=10, nperm=NPERM, seed=9):
    rng = np.random.default_rng(seed)
    codes = {}
    arrs = [np.array([codes.setdefault(feat(w), len(codes)) for w in s]) for s in seqs]
    out = {}
    for d in range(1, maxlag + 1):
        usable = [s for s in arrs if len(s) - d >= 1]
        if not usable:
            continue
        obs = sum(int(np.sum(s[:-d] == s[d:])) for s in usable)
        tot = sum(len(s) - d for s in usable)
        nulls = np.empty(nperm)
        for i in range(nperm):
            nulls[i] = sum(int(np.sum((p := rng.permutation(s))[:-d] == p[d:])) for s in usable)
        mu, sd = nulls.mean(), nulls.std(ddof=1)
        out[d] = {"obs": obs, "tot": tot, "null": float(mu),
                  "ratio": obs / mu if mu else 0.0,
                  "z": float((obs - mu) / sd) if sd else 0.0,
                  "p": float((np.sum(nulls >= obs) + 1) / (nperm + 1))}
    return out


def main():
    rows = L.load()
    z = L.ring_strings(rows)
    rings = {k: v for k, v in z.items() if len(v) >= 8}
    order = sorted(rings, key=lambda k: (ORDER.index(k[0]), k[1]))

    groups = {
        "ZODIAC all (discovery set)": [rings[k] for k in order],
        "ZODIAC early Psc-Cnc": [rings[k] for k in order if ORDER.index(k[0]) < 7],
        "ZODIAC late Leo-Sgr": [rings[k] for k in order if ORDER.index(k[0]) >= 7],
        "ZODIAC big rings n>=14": [rings[k] for k in order if len(rings[k]) >= 14],
        "ZODIAC small rings n<14": [rings[k] for k in order if len(rings[k]) < 14],
        "ZODIAC inner rings S<=1": [rings[k] for k in order if k[1] <= 1],
        "ZODIAC outer rings S>=2": [rings[k] for k in order if k[1] >= 2],
    }

    # controls with matched ring-size profile
    sizes = [len(rings[k]) for k in order]
    byf = {}
    for r in rows:
        if r["ltype"] == "L" and r["words"]:
            byf.setdefault(r["folio"], []).append((r["lnum"], r["line"], "".join(r["words"])))
    Lseq = [x[2] for f in sorted(byf) for x in sorted(byf[f])]
    q = sorted((r["folio"], r["lnum"], r["line"], r["words"][0]) for r in rows
               if r["ltype"] == "S" and r["folio"] not in L.ZODIAC_FOLIOS and r["words"])
    Qseq = [x[3] for x in q]
    Pseq = [w for r in rows if r["ltype"] == "P" for w in r["words"]]
    # zodiac RING TEXT of the same pages, cut to the same profile
    Rseq = [w for r in rows if r["folio"] in ORDER and r["ltype"] == "R" for w in r["words"]]
    for nm, seq in (("CONTROL herbal/pharma L-labels", Lseq),
                    ("CONTROL Q20 star-para 1st words", Qseq),
                    ("CONTROL running text (P loci)", Pseq),
                    ("CONTROL zodiac RING TEXT", Rseq)):
        chunks, pos = [], 0
        for n in sizes:
            if pos + n > len(seq):
                break
            chunks.append(seq[pos:pos + n]); pos += n
        groups[nm] = chunks

    print(f"{'group':34s} {'feat':7s} {'lag7 obs':>8s} {'/pairs':>6s} {'null':>7s} "
          f"{'ratio':>6s} {'Z':>7s} {'p':>8s}   {'best lag':>8s}")
    allout = {}
    for gname, seqs in groups.items():
        for fname, f in FEATS.items():
            res = pooled(seqs, f, seed=hash((gname, fname)) & 0xffff)
            allout[f"{gname}|{fname}"] = res
            if 7 not in res:
                continue
            r = res[7]
            best = max(res, key=lambda d: res[d]["z"])
            print(f"{gname:34s} {fname:7s} {r['obs']:8d} {r['tot']:6d} {r['null']:7.1f} "
                  f"{r['ratio']:6.2f} {r['z']:+7.2f} {r['p']:8.5f}   {best:8d}")
    json.dump(allout, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        '..', 'results', 't12_final.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
