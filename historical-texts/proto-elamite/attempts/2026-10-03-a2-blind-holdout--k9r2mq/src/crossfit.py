"""Part 2: 5-fold cross-fitted screen-and-test under the UNCHANGED 2026-09-04 rule.

The folder's standing hypothesis is that the published eight is a power-limited
sample: the 2026-09-04 design spends 80% of the corpus on screening and tests on
1,050 lines, so a real association of moderate size cannot clear BH over 54.
That hypothesis has never been tested against data it was not derived from.

The hash split already defines five buckets. This runs the published rule five
times -- screen on four buckets, test on the fifth -- so every line serves as
test data exactly once and every pair that the rule can find gets a blind test.
Nothing in the rule changes: the same occupancy bars, the same training BH
q <= 0.01 and |OR| >= 3 gate, the same within-tablet exact randomization test on
the held-out bucket, the same direction / effect-size / minimum-line criteria,
and BH taken within each fold over that fold's own selected set.

Fold 1 (test bucket 0) is the published design and is the gate.
Folds 2-5 have never been computed in this folder: they are the blind test.

Predictions P2.1-P2.6 frozen in PREDICTIONS.md @ dc1802b.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import load_audited, mixed_lines_of, bh

sa = load_audited()


def bucket(tablet: str) -> int:
    return int(hashlib.sha256(tablet.encode("ascii")).hexdigest()[:8], 16) % 5


def run_fold(lines, test_bucket, verbose=False):
    """The published numeral_association rule with `test_bucket` held out."""
    train = [ln for ln in lines if bucket(ln.tablet) != test_bucket]
    test = [ln for ln in lines if bucket(ln.tablet) == test_bucket]
    m_fams = sorted({s for ln in train for s in ln.m_signs})
    n_sgns = sorted({s for ln in train for s in ln.n_signs})

    raw = []
    for t in n_sgns:
        pred = lambda ln, tt=t: tt in ln.n_signs
        for m in m_fams:
            a, b, c, d = sa.contingency(train, m, pred)
            if a + b < 20 or a + c < 20:
                continue
            raw.append((m, t, (a, b, c, d), sa.odds_ratio(a, b, c, d),
                        sa.fisher_exact_two_sided(a, b, c, d)))
    qs = sa.bh_adjust([r[4] for r in raw])
    sel = [r for r, q in zip(raw, qs)
           if q <= 0.01 and (r[3] >= 3.0 or r[3] <= 1 / 3)]

    ps, cells_l = [], []
    for m, t, _, tor, _ in sel:
        pred = lambda ln, tt=t: tt in ln.n_signs
        cells = sa.contingency(test, m, pred)
        cells_l.append(cells)
        ps.append(sa.blocked_randomization_p(
            test, m, pred, "enriched" if tor > 1 else "depleted"))
    qs2 = sa.bh_adjust(ps)

    confirmed = []
    for (m, t, _, tor, _), cells, p, q in zip(sel, cells_l, ps, qs2):
        vor = sa.odds_ratio(*cells)
        same = (tor > 1 and vor > 1) or (tor < 1 and vor < 1)
        if (cells[0] + cells[1] >= 5 and same and q <= 0.05
                and (vor >= 1.5 or vor <= 1 / 1.5)):
            confirmed.append({"pair": f"{m}-{t}",
                              "direction": "enriched" if tor > 1 else "depleted",
                              "train_or": tor, "val_or": vor, "val_p": p, "val_q": q,
                              "val_cells": list(cells)})
    return {"test_bucket": test_bucket, "train_lines": len(train),
            "test_lines": len(test), "tested": len(raw), "selected": len(sel),
            "confirmed": confirmed}


if __name__ == "__main__":
    corpus = Path(sys.argv[1])
    out = Path(__file__).resolve().parents[1] / "results"
    lines = mixed_lines_of(corpus)
    folds = [run_fold(lines, b) for b in range(5)]

    PUBLISHED_EIGHT = {"M297-N39B", "M297-N24", "M297-N01", "M263-N30C",
                       "M263-N01", "M243-N39B", "M106-N24", "M288-N45"}
    print(f"{'fold':5s} {'testbk':>6s} {'trainL':>7s} {'testL':>6s} "
          f"{'tested':>7s} {'selected':>8s} {'confirmed':>9s}")
    for i, f in enumerate(folds, 1):
        print(f"{i:<5d} {f['test_bucket']:6d} {f['train_lines']:7d} "
              f"{f['test_lines']:6d} {f['tested']:7d} {f['selected']:8d} "
              f"{len(f['confirmed']):9d}")

    g = {c["pair"] for c in folds[0]["confirmed"]}
    print(f"\nP2.1 GATE fold 1 == published eight: "
          f"{'HELD' if g == PUBLISHED_EIGHT else 'FAILED ' + str(g ^ PUBLISHED_EIGHT)}")
    assert g == PUBLISHED_EIGHT, "gate failed; nothing below is believable"

    blind = folds[1:]
    counts = {}
    for f in blind:
        for c in f["confirmed"]:
            counts.setdefault(c["pair"], []).append(f["test_bucket"])
    union = sorted(counts, key=lambda p: (-len(counts[p]), p))
    print(f"\n=== folds 2-5 (blind): {len(union)} distinct pairs confirmed ===")
    for p in union:
        tag = "published" if p in PUBLISHED_EIGHT else "NEW"
        print(f"  {p:11s} folds={len(counts[p])} buckets={counts[p]}  [{tag}]")

    newly = [p for p in union if p not in PUBLISHED_EIGHT]
    print(f"\nP2.2 union(folds 2-5) > 8: {len(union)} "
          f"{'HELD' if len(union) > 8 else 'FAILED'}")
    for pid, pair, need in (("P2.3", "M288-N45", 1), ("P2.4", "M297-N39B", 2),
                            ("P2.5", "M288-N39B", 1), ("P2.6", "M297-N24", 2)):
        got = len(counts.get(pair, []))
        print(f"{pid} {pair:11s} confirmed in {got} of folds 2-5 (predicted >={need}): "
              f"{'HELD' if got >= need else 'FAILED'}")

    json.dump({"folds": folds, "blind_union": union,
               "blind_fold_counts": {p: counts[p] for p in union},
               "newly_warranted": newly},
              open(out / "crossfit.json", "w"), indent=1)
    print("\nwrote results/crossfit.json")
