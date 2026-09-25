#!/usr/bin/env python3
"""P2: is a physical bar FACE letter-balanced, or only the deduplicated inventory?

The panel's refuter reported that face 5.1's complete stamped text is itself
balanced at P = 4.0e-6, and drew the structural conclusion that "a bar face is
a physical object, so the argument that only a composer could produce the
balance does not stand". This tests that on all six photographed Latin faces,
using the line inventory read off the photographs rather than the IACR
arrangement diagram.
"""
import collections, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tail import exact_lower_tail, mc_lower_tail
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

rows = []
for line in open(os.path.join(HERE, "data", "instances_photographic.tsv")):
    if line.startswith("#") or line.startswith("face\t"): continue
    f, ln, s, conf, new = line.rstrip("\n").split("\t")
    rows.append((f, int(ln), s, conf, int(new)))

def counts_of(t):
    c = collections.Counter(t); return [c.get(x,0) for x in A]

def report(label, text, cap=400_000):
    c = counts_of(text)
    try:
        r = exact_lower_tail(c, cap=cap)
        P = f"{r['P_le']:.3E}"; how = "exact"
    except MemoryError:
        r = mc_lower_tail(c, reps=200_000)
        P = f"{r['P_le_mc']:.3E}"; how = f"MC {r['reps']}"
    n = sum(c); at = sum(1 for x in c if x == n//26)
    print(f"  {label:<28s} n={n:4d}  chi2={r['chi2']:8.3f}  P(chi2<=obs)={P:>12s} [{how}]  "
          f"letters at {n//26}: {at}/26")
    return {"label": label, "n": n, "chi2": r["chi2"], "P": P, "method": how}

print("=== per-face complete stamped text (every line, repeats included) ===")
faces = sorted(set(f for f,_,_,_,_ in rows))
out = []
for f in faces:
    t = "".join(s for ff,_,s,_,_ in rows if ff == f)
    out.append(report(f"face {f}", t))

print("\n=== bar 10 as one bar (both ends pooled) ===")
t = "".join(s for ff,_,s,_,_ in rows if ff.startswith("10.2"))
out.append(report("bar 10 (10.2a+10.2b)", t))

print("\n=== all 96 stamped instances pooled (the whole physical corpus) ===")
t = "".join(s for _,_,s,_,_ in rows)
out.append(report("all instances", t))

print("\n=== the deduplicated inventory, for comparison ===")
t = "".join(l.strip() for l in open(os.path.join(HERE, "data", "cryptograms_corrected.txt")) if l.strip())
out.append(report("16 distinct strings", t))

print(f"\ntotal line instances read from photographs: {len(rows)}")
print(f"  of which absent from the IACR arrangement page: {sum(r[4] for r in rows)}")
json.dump(out, open(os.path.join(HERE, "out", "face_balance.json"), "w"), indent=2)
