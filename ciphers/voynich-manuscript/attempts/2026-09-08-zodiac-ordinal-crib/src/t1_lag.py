#!/usr/bin/env python3
"""T1/T3: within-ring lag structure for zodiac labels, with control label sets."""
import sys, os, json, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vmsparse, labels as L, simlib

MAXLAG = 7
NPERM = 5000


def control_sets(rows):
    """Ordered label-ish sequences with physical order but no ordinal semantics."""
    out = {}
    # (a) 'L' loci: herbal / pharma / cosmological labels, grouped per folio
    byf = {}
    for r in rows:
        if r["ltype"] == "L" and r["words"]:
            byf.setdefault(r["folio"], []).append((r["lnum"], r["line"], "".join(r["words"])))
    for f, v in byf.items():
        v.sort()
        if len(v) >= 5:
            out[("L", f)] = [x[2] for x in v]
    # (b) Quire-20 starred-paragraph FIRST words, in page order (a real ordered list)
    q20 = {}
    for r in rows:
        if r["ltype"] == "S" and r["folio"] not in L.ZODIAC_FOLIOS and r["words"]:
            q20.setdefault(r["folio"], []).append((r["lnum"], r["line"], r["words"][0]))
    for f, v in q20.items():
        v.sort()
        if len(v) >= 5:
            out[("Q20first", f)] = [x[2] for x in v]
    # (c) running-text paragraph words chunked to ring-sized blocks (register floor)
    return out


def analyse(seqs, measure, tag, nperm=NPERM):
    simf = simlib.MEASURES[measure]
    rows = []
    for key, seq in sorted(seqs.items(), key=lambda kv: str(kv[0])):
        if len(seq) < 6:
            continue
        rng = random.Random(hash((str(key), measure)) & 0xffffffff)
        for d in range(1, MAXLAG + 1):
            if len(seq) - d < 3:
                continue
            res = simlib.perm_test_lag(seq, d, simf, nperm=nperm, rng=rng)
            rows.append({"set": tag, "key": str(key), "n": len(seq), "lag": d, **res})
    return rows


def stouffer(zs):
    zs = [z for z in zs if z is not None]
    return sum(zs) / math.sqrt(len(zs)) if zs else 0.0


def main():
    rows = L.load()
    zod = L.ring_strings(rows)
    zod = {k: v for k, v in zod.items() if len(v) >= 6}
    ctrl = control_sets(rows)

    allres = []
    for measure in ("lev", "lcs", "onset2", "coda2"):
        allres += analyse(zod, measure, "zodiac_" + measure)
        allres += analyse(ctrl, measure, "control_" + measure)

    # combine per (set, lag)
    print(f"{'set':22s} {'lag':>3s} {'rings':>5s} {'mean_obs':>9s} {'mean_null':>9s} {'Stouffer Z':>11s}")
    summary = {}
    for tag in sorted(set(r["set"] for r in allres)):
        for d in range(1, MAXLAG + 1):
            sub = [r for r in allres if r["set"] == tag and r["lag"] == d]
            if not sub:
                continue
            z = stouffer([r["z"] for r in sub])
            mo = sum(r["obs"] for r in sub) / len(sub)
            mn = sum(r["null_mean"] for r in sub) / len(sub)
            summary[(tag, d)] = z
            print(f"{tag:22s} {d:3d} {len(sub):5d} {mo:9.4f} {mn:9.4f} {z:11.3f}")
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "t1_lag_raw.json"), "w") as fh:
        json.dump(allres, fh, indent=1)


if __name__ == "__main__":
    main()
