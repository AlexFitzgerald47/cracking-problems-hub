"""Part 3: null model for the 5-fold cross-fitted design.

The observed design confirms 16 distinct pairs in at least one of folds 2-5.
With four folds, ~48 candidates each and BH at 0.05 within fold, that union
count has a null expectation well above zero, and a pair confirmed in exactly
one of four folds is the suspect class. This measures the whole distribution.

Null: permute whole N-sign SET assignments among the eligible lines within each
tablet. M-sign occurrence, tablet structure, line counts and the joint
composition of every numeral expression are preserved exactly; only the pairing
between an M family and a numeral expression is destroyed. The entire 5-fold
pipeline -- screen, select, test, BH within fold -- is re-run on each replicate,
so the null prices the search, not just a single test.

Predictions P3.1-P3.3 frozen in PREDICTIONS.md @ dc1802b.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from common import mixed_lines_of
from fastfold import Design, run_fold_fast

corpus = Path(sys.argv[1])
reps = int(sys.argv[2]) if len(sys.argv) > 2 else 500
out = Path(__file__).resolve().parents[1] / "results"

lines = mixed_lines_of(corpus)
d = Design(lines)

obs_folds = [run_fold_fast(d, d.N, b) for b in range(5)]
obs_union = sorted({p for f in obs_folds[1:] for p in f})
obs_fold1 = len(obs_folds[0])
obs_counts = {p: sum(p in f for f in obs_folds[1:]) for p in obs_union}
print(f"observed: fold1={obs_fold1}  union(folds 2-5)={len(obs_union)}")

rng = np.random.default_rng(20261003)
null_union, null_fold1, null_perfold, null_maxrep = [], [], [], []
for r in range(reps):
    N2 = d.permute_within_tablet(rng)
    folds = [run_fold_fast(d, N2, b) for b in range(5)]
    u = {p for f in folds[1:] for p in f}
    null_union.append(len(u))
    null_fold1.append(len(folds[0]))
    null_perfold.extend(len(f) for f in folds[1:])
    null_maxrep.append(max((sum(p in f for f in folds[1:]) for p in u), default=0))
    if (r + 1) % 100 == 0:
        print(f"  {r + 1}/{reps} replicates; running mean union = "
              f"{np.mean(null_union):.2f}")

nu = np.array(null_union); nf = np.array(null_fold1); nm = np.array(null_maxrep)
pct = lambda a, q: float(np.percentile(a, q))
p_union = float((nu >= len(obs_union)).sum() + 1) / (reps + 1)
res = {
    "replicates": reps, "seed": 20261003,
    "observed_fold1": obs_fold1, "observed_union_blind": len(obs_union),
    "observed_blind_fold_counts": obs_counts,
    "null_union_mean": float(nu.mean()), "null_union_median": float(np.median(nu)),
    "null_union_p95": pct(nu, 95), "null_union_p99": pct(nu, 99),
    "null_union_max": int(nu.max()),
    "null_fold1_mean": float(nf.mean()), "null_fold1_median": float(np.median(nf)),
    "null_fold1_p95": pct(nf, 95),
    "null_per_fold_mean": float(np.mean(null_perfold)),
    "null_max_fold_replication_mean": float(nm.mean()),
    "null_max_fold_replication_p95": pct(nm, 95),
    "null_frac_any_pair_in_ge2_folds": float((nm >= 2).mean()),
    "null_frac_any_pair_in_ge3_folds": float((nm >= 3).mean()),
    "exact_p_union": p_union,
}
json.dump(res, open(out / "null_model.json", "w"), indent=2)

print(f"\n=== null distribution, {reps} replicates ===")
print(f"union(folds 2-5):  mean={nu.mean():.2f} median={np.median(nu):.0f} "
      f"p95={pct(nu,95):.0f} p99={pct(nu,99):.0f} max={nu.max()}   "
      f"OBSERVED={len(obs_union)}")
print(f"fold-1 count:      mean={nf.mean():.2f} median={np.median(nf):.0f} "
      f"p95={pct(nf,95):.0f}   OBSERVED={obs_fold1}")
print(f"pairs per blind fold: mean={np.mean(null_perfold):.2f}")
print(f"\nmost-replicated pair within a replicate: mean={nm.mean():.2f} "
      f"p95={pct(nm,95):.0f}")
print(f"  P(some pair reaches >=2 of 4 blind folds under the null) = "
      f"{(nm>=2).mean():.3f}")
print(f"  P(some pair reaches >=3 of 4 blind folds under the null) = "
      f"{(nm>=3).mean():.3f}")

print(f"\nP3.1 null median union <= 1: {np.median(nu):.0f} "
      f"{'HELD' if np.median(nu) <= 1 else 'FAILED'}")
print(f"P3.2 observed union > null p95: {len(obs_union)} vs {pct(nu,95):.0f} "
      f"{'HELD' if len(obs_union) > pct(nu,95) else 'FAILED'}  "
      f"(exact p = {p_union:.4g})")
print(f"P3.3 null fold-1 median == 0: {np.median(nf):.0f} "
      f"{'HELD' if np.median(nf) == 0 else 'FAILED'}")
print("\nwrote results/null_model.json")
