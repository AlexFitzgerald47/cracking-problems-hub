"""Does the number of independent sweeps that reported a pair predict whether it
survives a control none of those sweeps applied?  Exact permutation test -- the
sample is 11, so this is run before the pattern is believed."""
from __future__ import annotations
import json
from itertools import combinations
from pathlib import Path

rows = json.loads(Path("results/newcore_conumeral.json").read_text())
sweeps = [r["sweeps"] for r in rows]
surv = [r["verdict"] == "SURVIVES" for r in rows]
k = sum(surv)
obs = sum(s for s, v in zip(sweeps, surv) if v)
allsub = list(combinations(range(len(rows)), k))
ge = sum(1 for c in allsub if sum(sweeps[i] for i in c) >= obs)
p = ge / len(allsub)
by_tier = {}
for r in rows:
    t = by_tier.setdefault(r["sweeps"], [0, 0])
    t[1] += 1
    t[0] += r["verdict"] == "SURVIVES"
print("survival by sweep count:")
for s in sorted(by_tier, reverse=True):
    a, b = by_tier[s]
    print(f"  reported by {s}/4 sweeps: {a}/{b} survive")
print(f"\nobserved sum of sweep-counts among the {k} survivors: {obs}")
print(f"exact permutation p (one-sided, all C(11,{k})={len(allsub)} subsets): {p:.4f}")
print("VERDICT:", "suggestive, NOT significant" if p > 0.05 else "significant")
Path("results/sweep_trend.json").write_text(json.dumps(
    {"by_tier": {str(a): b for a, b in by_tier.items()}, "observed_sum": obs,
     "permutation_p": p, "subsets": len(allsub)}, indent=2))
