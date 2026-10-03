#!/usr/bin/env python3
"""Is the block-aware split a valid confirmatory procedure, or does it manufacture
significance?

The split chooses validation tablets using the pair's own block marginals. The exact
conditional test conditions on exactly those marginals, so in theory this is free. But
the chosen tablets are also the tablets where both signs are plentiful, which is where
any association is concentrated, so the claim needs checking rather than asserting.

Check: run the IDENTICAL procedure -- marginal-only block-aware split, screen on the
complement, face-blocked exact test on validation -- on every decoy pair, and read off
the rejection rate. Direction is taken from the complement, never from validation.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))

from structure_associations import odds_ratio  # noqa: E402
from weighted_null import load_eligible  # noqa: E402

from block_aware_split import block_freedom, face_blocked_p  # noqa: E402
from test_weighted_null import CONFIRMED  # noqa: E402

EXCLUDED = {(m, n) for m, n, _ in CONFIRMED}
TARGET_BLOCKS = 10


def split_for(lines, m_sign, n_sign):
    informative = {k: v for k, v in block_freedom(lines, m_sign, n_sign).items()
                   if v["dof"] > 0}
    by_tablet = defaultdict(list)
    for (tablet, _), info in informative.items():
        by_tablet[tablet].append(info["dof"])
    ranking = sorted(by_tablet.items(), key=lambda kv: (-sum(kv[1]), kv[0]))
    chosen: set[str] = set()
    held = 0
    for tablet, dofs in ranking:
        if held >= TARGET_BLOCKS:
            break
        chosen.add(tablet)
        held += len(dofs)
    return chosen, len(informative), held


def main() -> None:
    corpus = Path(Path(__file__).with_name("corpus_path.txt").read_text().strip())
    lines = load_eligible(corpus)
    m_counts = Counter(s for ln in lines for s in ln.m_signs)
    n_counts = Counter(s for ln in lines for s in ln.n_signs)
    m_signs = sorted(s for s, c in m_counts.items() if c >= 20)
    n_signs = sorted(s for s, c in n_counts.items() if c >= 20)

    rows = []
    for m_sign in m_signs:
        for n_sign in n_signs:
            if (m_sign, n_sign) in EXCLUDED:
                continue
            chosen, informative_total, held = split_for(lines, m_sign, n_sign)
            if held < TARGET_BLOCKS:
                continue  # corpus cannot supply 10 informative blocks for this pair
            validation = [ln for ln in lines if ln.tablet in chosen]
            train = [ln for ln in lines if ln.tablet not in chosen]
            a = b = c = d = 0
            for ln in train:
                has_sign = m_sign in ln.m_signs
                has_target = n_sign in ln.n_signs
                if has_sign and has_target:
                    a += 1
                elif has_sign:
                    b += 1
                elif has_target:
                    c += 1
                else:
                    d += 1
            if a + b < 20 or a + c < 20:
                continue
            train_or = odds_ratio(a, b, c, d)
            direction = "enriched" if train_or > 1 else "depleted"
            result = face_blocked_p(validation, m_sign, n_sign, direction)
            rows.append({
                "m_sign": m_sign, "n_sign": n_sign, "direction": direction,
                "train_odds_ratio": train_or,
                "informative_blocks_corpus": informative_total,
                "validation_informative_blocks": result["informative_blocks"],
                "validation_lines": len(validation),
                "p": result["p"], "p_floor": result["p_floor"],
                "has_power_05": result["p_floor"] <= 0.05,
            })

    powered = [r for r in rows if r["has_power_05"]]
    summary = {
        "decoys_runnable": len(rows),
        "decoys_with_power_at_05": len(powered),
        "reject_05": sum(1 for r in powered if r["p"] < 0.05) / len(powered),
        "reject_01": sum(1 for r in powered if r["p"] < 0.01) / len(powered),
        "median_p": sorted(r["p"] for r in powered)[len(powered) // 2],
    }
    print(json.dumps(summary, indent=2))
    print("\nmost extreme decoys under the block-aware split:")
    for r in sorted(powered, key=lambda r: r["p"])[:12]:
        print(f"  {r['m_sign']}-{r['n_sign']:7} {r['direction']:9} "
              f"valBlk {r['validation_informative_blocks']:3} "
              f"valLines {r['validation_lines']:4} p {r['p']:.5f}")
    Path("results").mkdir(exist_ok=True)
    Path("results/block_aware_decoys.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2) + "\n")


if __name__ == "__main__":
    main()
