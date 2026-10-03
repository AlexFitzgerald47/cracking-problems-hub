"""Part 4: Null B -- the real screen, a permuted test arm.

Null A permutes the whole corpus, so the training screen finds almost nothing
and the union count sits near zero. That is decisive against "the pipeline
manufactures 16 pairs from noise" but it cannot price a pair confirmed in 1 of 4
blind folds, which is the suspect class here.

Null B holds every fold's REAL training screen -- real candidate set, real
directions, real per-fold correction base -- and permutes whole N-sign sets
within tablet in the TEST bucket only. The search stays at its true size and
what is measured is the false-confirmation rate of the test arm at the real
multiplicity.

Predictions P4.1-P4.5 frozen in PREDICTIONS.md @ 5afe79f, before this file existed.
"""
from __future__ import annotations
import hashlib, json, sys
from collections import Counter
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from common import load_audited, mixed_lines_of
from fastfold import Design, bucket

sa = load_audited()


def real_screen(d: Design, test_bucket: int):
    """Exactly the published training screen for this fold. Never permuted."""
    tr = d.bucket != test_bucket
    Mtr, Ntr = d.M[tr], d.N[tr]
    ntr = int(tr.sum())
    A = Mtr.T @ Ntr
    ab = Mtr.sum(0)[:, None]
    ac = Ntr.sum(0)[None, :]
    mi, nj = np.nonzero((ab >= 20) & (ac >= 20))
    raw = []
    for i, j in zip(mi, nj):
        a = int(A[i, j]); b = int(ab[i, 0]) - a; c = int(ac[0, j]) - a
        raw.append((i, j, sa.odds_ratio(a, b, c, ntr - a - b - c),
                    sa.fisher_exact_two_sided(a, b, c, ntr - a - b - c)))
    qs = sa.bh_adjust([r[3] for r in raw])
    return [r for r, q in zip(raw, qs) if q <= 0.01 and (r[2] >= 3.0 or r[2] <= 1 / 3)]


def test_arm(d: Design, N, sel, test_bucket: int):
    """The published test arm on `N`, for a fixed selected set."""
    te = d.bucket == test_bucket
    te_lines = [d.lines[k] for k in np.flatnonzero(te)]
    Mte, Nte = d.M[te], N[te]
    tablets = {}
    for pos, ln in enumerate(te_lines):
        tablets.setdefault(ln.tablet, []).append(pos)
    ps, cl = [], []
    for i, j, tor, _ in sel:
        mcol, ncol = Mte[:, i], Nte[:, j]
        a = int(np.dot(mcol, ncol)); b = int(mcol.sum()) - a
        c = int(ncol.sum()) - a
        cl.append((a, b, c, len(te_lines) - a - b - c))
        dist = [1.0]; obs = 0
        for pos in tablets.values():
            n = len(pos); s = int(mcol[pos].sum()); t = int(ncol[pos].sum())
            obs += int(np.dot(mcol[pos], ncol[pos]))
            lo, hi = max(0, s - (n - t)), min(s, t)
            local = [0.0] * (hi + 1)
            for k in range(lo, hi + 1):
                local[k] = sa.hypergeom_probability(k, s, t, n)
            comb = [0.0] * (len(dist) + len(local) - 1)
            for x, px in enumerate(dist):
                if not px:
                    continue
                for y, py in enumerate(local):
                    if py:
                        comb[x + y] += px * py
            dist = comb
        ps.append(min(1.0, sum(dist[obs:]) if tor > 1 else sum(dist[:obs + 1])))
    qs = sa.bh_adjust(ps)
    out = []
    for (i, j, tor, _), cells, q in zip(sel, cl, qs):
        vor = sa.odds_ratio(*cells)
        same = (tor > 1 and vor > 1) or (tor < 1 and vor < 1)
        if (cells[0] + cells[1] >= 5 and same and q <= 0.05
                and (vor >= 1.5 or vor <= 1 / 1.5)):
            out.append(f"{d.m_vocab[i]}-{d.n_vocab[j]}")
    return out


def permute_test_bucket(d: Design, test_bucket: int, rng):
    """Permute whole N-sign sets within tablet, inside the test bucket only."""
    N2 = d.N.copy()
    idx = np.flatnonzero(d.bucket == test_bucket)
    tb = {}
    for k in idx:
        tb.setdefault(d.tablet[k], []).append(k)
    for ks in tb.values():
        if len(ks) > 1:
            ks = np.array(ks)
            N2[ks] = N2[rng.permutation(ks)]
    return N2


if __name__ == "__main__":
    corpus = Path(sys.argv[1])
    reps = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    out = Path(__file__).resolve().parents[1] / "results"
    d = Design(mixed_lines_of(corpus))
    screens = {b: real_screen(d, b) for b in range(5)}
    print("real per-fold candidate base:",
          {b: len(screens[b]) for b in range(5)})

    # gate: the real test arm on the real data must reproduce the cross-fit
    real = {b: test_arm(d, d.N, screens[b], b) for b in range(5)}
    cf = json.load(open(out / "crossfit.json"))
    for b in range(5):
        exp = sorted(c["pair"] for c in cf["folds"][b]["confirmed"])
        assert sorted(real[b]) == exp, (b, sorted(real[b]), exp)
    print("GATE: Null B's real-data path reproduces crossfit.json on all 5 folds")

    obs_ge2 = sum(1 for p, f in cf["blind_fold_counts"].items() if len(f) >= 2)
    obs_union = len(cf["blind_union"])
    obs_single = obs_union - obs_ge2
    print(f"observed: union={obs_union} ge2={obs_ge2} singletons={obs_single}")

    rng = np.random.default_rng(20261003)
    u, g2, g3, sing, mx = [], [], [], [], []
    for r in range(reps):
        cnt = Counter()
        for b in range(1, 5):
            for p in test_arm(d, permute_test_bucket(d, b, rng), screens[b], b):
                cnt[p] += 1
        u.append(len(cnt))
        g2.append(sum(1 for v in cnt.values() if v >= 2))
        g3.append(sum(1 for v in cnt.values() if v >= 3))
        sing.append(sum(1 for v in cnt.values() if v == 1))
        mx.append(max(cnt.values(), default=0))
        if (r + 1) % 50 == 0:
            print(f"  {r+1}/{reps}  mean union={np.mean(u):.2f} "
                  f"mean ge2={np.mean(g2):.3f} P(max>=2)={np.mean(np.array(mx)>=2):.3f}")

    u, g2, g3, sing, mx = map(np.array, (u, g2, g3, sing, mx))
    pct = lambda a, q: float(np.percentile(a, q))
    res = {"replicates": reps, "seed": 20261003,
           "per_fold_candidate_base": {str(b): len(screens[b]) for b in range(5)},
           "observed_union_blind": obs_union, "observed_ge2": obs_ge2,
           "observed_singletons": obs_single,
           "null_union_mean": float(u.mean()), "null_union_p95": pct(u, 95),
           "null_ge2_mean": float(g2.mean()), "null_ge2_p95": pct(g2, 95),
           "null_ge2_max": int(g2.max()),
           "null_ge3_mean": float(g3.mean()), "null_ge3_p95": pct(g3, 95),
           "null_singleton_mean": float(sing.mean()),
           "P_any_pair_ge2_folds": float((mx >= 2).mean()),
           "P_any_pair_ge3_folds": float((mx >= 3).mean()),
           "P_any_pair_ge4_folds": float((mx >= 4).mean()),
           "exact_p_ge2_count": float(((g2 >= obs_ge2).sum() + 1) / (reps + 1)),
           "exact_p_union": float(((u >= obs_union).sum() + 1) / (reps + 1))}
    json.dump(res, open(out / "null_b.json", "w"), indent=2)

    print(f"\n=== Null B, {reps} replicates ===")
    print(f"union(>=1 of 4 blind folds): mean={u.mean():.2f} p95={pct(u,95):.0f} "
          f"max={u.max()}   OBSERVED={obs_union}")
    print(f"pairs in >=2 folds:          mean={g2.mean():.3f} p95={pct(g2,95):.0f} "
          f"max={g2.max()}   OBSERVED={obs_ge2}")
    print(f"pairs in >=3 folds:          mean={g3.mean():.3f} p95={pct(g3,95):.0f}")
    print(f"singletons:                  mean={sing.mean():.2f}   OBSERVED={obs_single}")
    print(f"P(any pair >=2 folds)={ (mx>=2).mean():.4f}  "
          f"P(>=3)={(mx>=3).mean():.4f}  P(>=4)={(mx>=4).mean():.4f}")
    print(f"\nP4.1 null mean union in [1,12]: {u.mean():.2f} "
          f"{'HELD' if 1 <= u.mean() <= 12 else 'FAILED'}")
    print(f"P4.2 P(any >=2 folds) < 0.20: {(mx>=2).mean():.4f} "
          f"{'HELD' if (mx>=2).mean() < 0.20 else 'FAILED'}")
    print(f"P4.3 P(any >=3 folds) < 0.05: {(mx>=3).mean():.4f} "
          f"{'HELD' if (mx>=3).mean() < 0.05 else 'FAILED'}")
    print(f"P4.4 observed ge2 ({obs_ge2}) > null p95 ({pct(g2,95):.0f}): "
          f"{'HELD' if obs_ge2 > pct(g2,95) else 'FAILED'}  "
          f"exact p={res['exact_p_ge2_count']:.4g}")
    print(f"P4.5 null mean singletons >= 1: {sing.mean():.2f} "
          f"{'HELD' if sing.mean() >= 1 else 'FAILED'}")
    print("\nwrote results/null_b.json")
