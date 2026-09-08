#!/usr/bin/env python3
"""T13: independent-transcription replication of the lag-7 ending effect.

Uses Glen Claston's v101 transcription (musyoku/voynich-transcription), which is an
independent reading of the same pages with its own alphabet AND its own word
segmentation. The test only needs symbol identity, so it runs directly on v101
strings with no v101->EVA mapping.

v101 does not tag label rings separately, so label rings are identified by matching
ring token counts against the Takahashi label-ring sizes for the same folio. The
matched rings are printed so the assignment can be checked by hand.
"""
import sys, os, re, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
from t6_regime import ORDER
from t12_final import pooled

V101 = os.environ.get("VMS_V101",
    "/tmp/claude-0/-home-user-cracking-problems-hub/634aa923-677e-5dc9-9564-f7bc199c0972/"
    "scratchpad/voynich-transcription/voynich.txt")

HDR = re.compile(r"^<(?P<folio>[0-9]+[rv][0-9]?)\.(?P<loc>[A-Za-z_0-9]+)>(?P<text>.*)$")


def load_v101():
    out = {}
    for line in open(V101, encoding="utf-8", errors="replace"):
        m = HDR.match(line.rstrip("\n"))
        if not m:
            continue
        d = m.groupdict()
        t = re.sub(r"[=\-]+$", "", d["text"]).replace(",", ".")
        toks = [w for w in t.split(".") if w]
        out.setdefault("f" + d["folio"], []).append((d["loc"], toks))
    return out


def main():
    rows = L.load()
    z = L.ring_strings(rows)
    v = load_v101()

    matched, unmatched_text = [], []
    print("ring matching (Takahashi label ring -> v101 ring):")
    for f in ORDER:
        tk = sorted([(k[1], len(vv)) for k, vv in z.items() if k[0] == f])
        rings = v.get(f, [])
        used = set()
        for rnum, n in tk:
            if n < 8:
                continue
            cand = sorted((abs(len(t) - n), i) for i, (loc, t) in enumerate(rings)
                          if i not in used)
            if not cand or cand[0][0] > 4:
                print(f"  {f} S{rnum} (n={n}) -> NO MATCH")
                continue
            _, i = cand[0]
            used.add(i)
            loc, toks = rings[i]
            matched.append(toks)
            print(f"  {f} S{rnum} (n={n:2d}) -> v101 {loc:14s} ({len(toks):2d} tokens)  {' '.join(toks[:5])}")
        for i, (loc, toks) in enumerate(rings):
            if i not in used and len(toks) >= 8:
                unmatched_text.append(toks)

    print(f"\nmatched label rings: {len(matched)}  "
          f"({sum(len(x) for x in matched)} tokens)")
    print(f"unmatched (mostly ring TEXT) rings: {len(unmatched_text)} "
          f"({sum(len(x) for x in unmatched_text)} tokens)\n")

    FE = {"last2": lambda w: w[-2:], "penult": lambda w: w[-2:-1]}
    print(f"{'set':30s} {'feat':7s} {'lag':>3s} {'obs':>4s} {'/pairs':>6s} {'null':>7s} "
          f"{'ratio':>6s} {'Z':>7s} {'p':>8s}")
    res = {}
    for tag, seqs in (("v101 zodiac LABEL rings", matched),
                      ("v101 zodiac RING TEXT", unmatched_text)):
        for fn, ff in FE.items():
            r = pooled(seqs, ff, maxlag=10, nperm=20000, seed=abs(hash(tag + fn)) % 9999)
            res[tag + "|" + fn] = r
            for d in (1, 2, 3, 4, 5, 6, 7, 8):
                if d not in r:
                    continue
                x = r[d]
                mark = "  <<<" if d == 7 else ""
                print(f"{tag:30s} {fn:7s} {d:3d} {x['obs']:4d} {x['tot']:6d} {x['null']:7.1f} "
                      f"{x['ratio']:6.2f} {x['z']:+7.2f} {x['p']:8.5f}{mark}")
            print()
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     '..', 'results', 't13_v101.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
