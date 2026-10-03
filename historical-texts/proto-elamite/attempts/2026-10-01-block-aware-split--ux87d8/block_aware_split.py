#!/usr/bin/env python3
"""Settle M288-N45 with a block-aware split, and test the numeral-richness confound.

The 2026-09-17 session found that the face-blocked exact test could not answer the
M288-N45 question on the 2026-09-04 bucket-0 holdout: only 4 of 290 tablet-faces were
informative and the p-value floor was 0.12, so no data could have produced a significant
result. Its recommended experiment 1 was to build a split that guarantees the validation
set enough informative blocks for the test to fire.

This module does that, and adds a confound the folder had not tested.

THE DONOR SPLIT
  A (tablet, face) block is *informative* for a pair when the hypergeometric support for
  its overlap is non-degenerate: min(s, t) > max(0, s - (total - t)), with s the M-sign
  lines, t the target lines and total the eligible lines in the block. That depends only
  on the block marginals. A tablet is a *donor* when it carries >= 1 informative block.
  Validation = donor tablets, screening = every other tablet, disjoint by tablet.

  Selecting blocks this way is legitimate because the exact test already conditions on
  each block's marginals, and within-block permutation of the target preserves
  (total, s, t) in every block exactly. Donor status is therefore invariant under the
  null's own randomization group: the null cannot move a block in or out of the donor
  set. `calibration()` checks that numerically instead of taking it on trust.

THE NUMERAL-RICHNESS CONFOUND
  Counting N-signs other than the target, so the stratification is not circular, N45
  lines carry 2.07 and non-N45 lines 1.32; M288 lines carry 1.74 against 1.28. Both
  signs prefer numeral-rich lines, which could manufacture co-occurrence on its own.
  `richness_control()` blocks on (tablet, face, other-N-count) and reports the floor
  for every pair, since a test without power is not a verdict either way.

No lexical, phonetic or metrological value is assigned to any sign anywhere here.

Usage:
    python3 block_aware_split.py --json results/block_aware_split.json
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Callable, Sequence

_HERE = Path(__file__).resolve().parent
_FACE = _HERE.parent / "2026-09-17-exact-form-and-face"
_ANALYSIS = _HERE.parents[1] / "analysis"
sys.path.insert(0, str(_FACE))
sys.path.insert(0, str(_ANALYSIS))

# Reuse the audited 2026-09-04 parser/statistics and the 2026-09-17 blocked test
# verbatim. test_face_and_form.py pins blocked_randomization_p to the eight published
# validation p-values, so every number below is like-for-like with the published set.
from structure_associations import (  # noqa: E402
    Line,
    bh_adjust,
    corpus_digest,
    fisher_exact_two_sided,
    hypergeom_probability,
    odds_ratio,
)
from face_and_form import (  # noqa: E402
    CONFIRMED,
    blocked_randomization_p,
    contingency,
    eligible,
    load_lines,
)

RICHNESS_CAP = 3  # other-N-counts >= 3 share a stratum; fixed in PREDICTIONS.md


# ----------------------------------------------------------------- block keys


def key_tablet(line: Line, target: str) -> object:
    return line.tablet


def key_face(line: Line, target: str) -> object:
    return line.tablet, line.surface


def other_n_count(line: Line, target: str) -> int:
    """N-signs on the line other than the target, capped so strata stay populated.

    Excluding the target is what keeps the stratification from being circular: a
    stratification on the raw count would separate target-bearing lines by the target.
    """
    return min(len(line.n_signs - {target}), RICHNESS_CAP)


def key_richness(line: Line, target: str) -> object:
    return line.tablet, other_n_count(line, target)


def key_face_richness(line: Line, target: str) -> object:
    return line.tablet, line.surface, other_n_count(line, target)


BLOCK_KEYS: dict[str, Callable[[Line, str], object]] = {
    "tablet": key_tablet,
    "tablet+face": key_face,
    "tablet+richness": key_richness,
    "tablet+face+richness": key_face_richness,
}


# ----------------------------------------------------------- block arithmetic


def blocks_of(
    lines: Sequence[Line], m_sign: str, target: str, key: Callable
) -> list[tuple[int, int, int, int, int, int]]:
    """(total, s, t, lo, hi, observed overlap) for every block."""
    grouped: dict[object, list[Line]] = defaultdict(list)
    for line in lines:
        grouped[key(line, target)].append(line)
    out = []
    for block in grouped.values():
        total = len(block)
        s = sum(m_sign in line.m_signs for line in block)
        t = sum(target in line.n_signs for line in block)
        a = sum(m_sign in line.m_signs and target in line.n_signs for line in block)
        out.append((total, s, t, max(0, s - (total - t)), min(s, t), a))
    return out


def block_report(
    lines: Sequence[Line], m_sign: str, target: str, key: Callable, direction: str
) -> dict:
    """Blocked exact p-value with its power floor, in one pass.

    The floor is the p-value the test would return if every block showed the maximum
    overlap its marginals permit. If it exceeds 0.05 the test could not have confirmed
    the pair whatever the data said, and a failure carries no information.
    """
    distribution = [1.0]
    best = [1.0]
    observed = maximum = informative = 0
    for total, s, t, lo, hi, a in blocks_of(lines, m_sign, target, key):
        observed += a
        maximum += hi
        if hi > lo:
            informative += 1
        local = [0.0] * (hi + 1)
        for overlap in range(lo, hi + 1):
            local[overlap] = hypergeom_probability(overlap, s, t, total)
        for source, dest in ((distribution, "d"), (best, "b")):
            combined = [0.0] * (len(source) + len(local) - 1)
            for i, pi in enumerate(source):
                if pi:
                    for j, pj in enumerate(local):
                        if pj:
                            combined[i + j] += pi * pj
            if dest == "d":
                distribution = combined
            else:
                best = combined

    def tail(dist: list[float], point: int) -> float:
        if direction == "enriched":
            return min(1.0, sum(dist[point:]))
        return min(1.0, sum(dist[: point + 1]))

    if direction == "enriched":
        floor = tail(best, maximum)
    else:
        lowest = next(i for i, v in enumerate(best) if v > 0)
        floor = tail(best, lowest)
    a, b, c, d = contingency(lines, m_sign, target)
    return {
        "p": tail(distribution, observed),
        "p_floor": floor,
        "has_power_at_05": floor <= 0.05,
        "observed_overlap": observed,
        "max_possible_overlap": maximum,
        "informative_blocks": informative,
        "blocks": len(blocks_of(lines, m_sign, target, key)),
        "lines": len(lines),
        "cells": [a, b, c, d],
        "odds_ratio": odds_ratio(a, b, c, d),
    }


# ---------------------------------------------------------------- donor split


def donor_tablets(
    lines: Sequence[Line], m_sign: str, target: str, key: Callable
) -> set[str]:
    """Tablets carrying at least one informative block. Marginals-only rule."""
    grouped: dict[object, list[Line]] = defaultdict(list)
    for line in lines:
        grouped[key(line, target)].append(line)
    donors = set()
    for block in grouped.values():
        total = len(block)
        s = sum(m_sign in line.m_signs for line in block)
        t = sum(target in line.n_signs for line in block)
        if min(s, t) > max(0, s - (total - t)):
            donors.add(block[0].tablet)
    return donors


def screen(lines: Sequence[Line], min_sign_lines: int = 20, min_target: int = 20) -> dict:
    """The 2026-09-04 candidate screen, re-run on an arbitrary tablet set.

    Thresholds are the published ones: BH q <= 0.01 over every screened pair and a
    Haldane-Anscombe odds ratio >= 3 or <= 1/3.
    """
    m_signs = sorted({s for line in lines for s in line.m_signs})
    n_signs = sorted({s for line in lines for s in line.n_signs})
    pairs, p_values = [], []
    for target in n_signs:
        for m_sign in m_signs:
            a, b, c, d = contingency(lines, m_sign, target)
            if a + b < min_sign_lines or a + c < min_target:
                continue
            pairs.append((m_sign, target, (a, b, c, d), odds_ratio(a, b, c, d)))
            p_values.append(fisher_exact_two_sided(a, b, c, d))
    q_values = bh_adjust(p_values)
    selected = {}
    for (m_sign, target, cells, ratio), p, q in zip(pairs, p_values, q_values):
        if q <= 0.01 and (ratio >= 3.0 or ratio <= 1 / 3):
            selected[f"{m_sign}-{target}"] = {
                "cells": list(cells), "odds_ratio": ratio, "p": p, "q": q,
                "direction": "enriched" if ratio > 1 else "depleted",
            }
    return {"screened_pairs": len(pairs), "selected": selected}


def donor_split_test(
    lines: Sequence[Line], m_sign: str, target: str, direction: str, key: Callable
) -> dict:
    """Screen on the complement, test on the donor tablets."""
    donors = donor_tablets(lines, m_sign, target, key)
    validation = [line for line in lines if line.tablet in donors]
    complement = [line for line in lines if line.tablet not in donors]
    screening = screen(complement)
    pair = f"{m_sign}-{target}"
    report = block_report(validation, m_sign, target, key, direction)
    report["donor_tablets"] = sorted(donors)
    report["complement_tablets"] = len({line.tablet for line in complement})
    report["complement_lines"] = len(complement)
    report["screened_on_complement"] = pair in screening["selected"]
    report["screening"] = screening["selected"].get(pair)
    report["screened_pair_count"] = screening["screened_pairs"]
    return report


# ---------------------------------------------------------------- null models


def permute_within_blocks(
    lines: Sequence[Line], target: str, key: Callable, rng: random.Random
) -> list[Line]:
    """Reassign target presence uniformly within each block, preserving all marginals.

    This is the null the exact test computes in closed form. Drawing from it lets the
    whole procedure -- donor selection, screening and test -- be run on data with no
    within-block association, which is what calibration requires.
    """
    grouped: dict[object, list[int]] = defaultdict(list)
    for index, line in enumerate(lines):
        grouped[key(line, target)].append(index)
    out = list(lines)
    for indices in grouped.values():
        carriers = [i for i in indices if target in lines[i].n_signs]
        if not carriers or len(carriers) == len(indices):
            continue
        chosen = set(rng.sample(indices, len(carriers)))
        for i in indices:
            line = lines[i]
            has = target in line.n_signs
            want = i in chosen
            if has == want:
                continue
            signs = (line.n_signs | {target}) if want else (line.n_signs - {target})
            out[i] = Line(
                tablet=line.tablet, surface=line.surface, label=line.label,
                ordinal_on_surface=line.ordinal_on_surface, text=line.text,
                m_signs=line.m_signs, n_signs=frozenset(signs), damaged=line.damaged,
            )
    return out


def calibration(
    lines: Sequence[Line], m_sign: str, target: str, direction: str,
    key: Callable, replicates: int, seed: int = 20261001,
    invariance_checks: int = 50,
) -> dict:
    """Is the donor-split test calibrated once the selection rule is applied to it?

    Each replicate permutes the target within every block corpus-wide, re-derives the
    donor set on the permuted data, and re-runs the test. Under the invariance argument
    the donor set must come back identical every time; `invariance_checks` replicates
    verify that, and any failure is reported rather than assumed away.
    """
    rng = random.Random(seed)
    truth = donor_tablets(lines, m_sign, target, key)
    p_values, invariant = [], True
    for replicate in range(replicates):
        permuted = permute_within_blocks(lines, target, key, rng)
        if replicate < invariance_checks:
            if donor_tablets(permuted, m_sign, target, key) != truth:
                invariant = False
        validation = [line for line in permuted if line.tablet in truth]
        p_values.append(block_report(validation, m_sign, target, key, direction)["p"])
    p_values.sort()
    n = len(p_values)
    return {
        "replicates": n,
        "donor_set_invariant": invariant,
        "invariance_checks": invariance_checks,
        "fraction_p_le_05": sum(p <= 0.05 for p in p_values) / n,
        "fraction_p_le_01": sum(p <= 0.01 for p in p_values) / n,
        "fraction_p_le_001": sum(p <= 0.001 for p in p_values) / n,
        "median_p": p_values[n // 2],
        "min_p": p_values[0],
    }


def procedure_null(
    lines: Sequence[Line], key: Callable, exclude: set[tuple[str, str]],
    min_sign_lines: int = 20, min_target: int = 20,
) -> dict:
    """Run the whole donor-split procedure over every eligible pair in the corpus.

    A literal label permutation is degenerate here: donor status is fixed by the
    marginals, not chosen, and a random tablet set contains no informative blocks, so
    the permuted test has no power and returns p ~ 1 by construction. The question the
    2026-09-23 cross-reference actually asks -- does the split buy the difference for
    free? -- is answered by running the identical procedure at full search budget over
    every pair the corpus offers and reading where the real pair falls.
    """
    m_signs = sorted({s for line in lines for s in line.m_signs})
    n_signs = sorted({s for line in lines for s in line.n_signs})
    results = []
    for target in n_signs:
        for m_sign in m_signs:
            if (m_sign, target) in exclude:
                continue
            a, b, c, d = contingency(lines, m_sign, target)
            if a + b < min_sign_lines or a + c < min_target:
                continue
            ratio = odds_ratio(a, b, c, d)
            direction = "enriched" if ratio > 1 else "depleted"
            donors = donor_tablets(lines, m_sign, target, key)
            if not donors:
                continue
            validation = [line for line in lines if line.tablet in donors]
            report = block_report(validation, m_sign, target, key, direction)
            results.append({
                "pair": f"{m_sign}-{target}", "direction": direction,
                "p": report["p"], "p_floor": report["p_floor"],
                "informative_blocks": report["informative_blocks"],
                "has_power_at_05": report["has_power_at_05"],
            })
    powered = [r for r in results if r["has_power_at_05"]]
    return {
        "pairs_run": len(results),
        "pairs_with_power": len(powered),
        "fraction_powered_p_le_05": (
            sum(r["p"] <= 0.05 for r in powered) / len(powered) if powered else None
        ),
        "fraction_powered_p_le_001": (
            sum(r["p"] <= 0.001 for r in powered) / len(powered) if powered else None
        ),
        "results": sorted(results, key=lambda r: r["p"]),
    }


# ------------------------------------------------------------ richness control


def richness_control(lines: Sequence[Line]) -> dict:
    """Re-test all eight confirmed pairs under every block scheme, with floors.

    Reported on the full corpus. That includes the tablets the candidates were selected
    on, so these are not held-out confirmations; they establish which confounds can
    explain which pair, which is a question about the corpus rather than about novelty.
    The donor-split columns in `main()` carry the held-out version.
    """
    out = {}
    for m_sign, target, direction in CONFIRMED:
        row = {}
        for name, key in BLOCK_KEYS.items():
            row[name] = block_report(lines, m_sign, target, key, direction)
        row["richness_profile"] = {
            "mean_other_n_on_m_lines": sum(
                len(line.n_signs - {target}) for line in lines if m_sign in line.m_signs
            ) / max(1, sum(1 for line in lines if m_sign in line.m_signs)),
            "mean_other_n_on_target_lines": sum(
                len(line.n_signs - {target}) for line in lines if target in line.n_signs
            ) / max(1, sum(1 for line in lines if target in line.n_signs)),
            "mean_other_n_all_lines": sum(
                len(line.n_signs - {target}) for line in lines
            ) / len(lines),
        }
        out[f"{m_sign}-{target}"] = row
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=None)
    parser.add_argument("--json", type=Path, default=Path("results/block_aware_split.json"))
    parser.add_argument("--replicates", type=int, default=2000)
    args = parser.parse_args()

    corpus = args.corpus or Path(
        (_FACE / "corpus_path.txt").read_text().strip()
    )
    raw, files = load_lines(corpus)
    lines = eligible(raw)
    out: dict[str, object] = {
        "schema_version": 1,
        "corpus": {
            "dir": str(corpus), "file_count": len(files),
            "sha256_lf": corpus_digest(files), "eligible_lines": len(lines),
            "tablets_with_eligible_lines": len({line.tablet for line in lines}),
        },
        "block_keys": {
            "tablet": "2026-09-04 null",
            "tablet+face": "2026-09-17 null",
            "tablet+richness": f"new 2026-10-01; other-N-count capped at {RICHNESS_CAP}",
            "tablet+face+richness": "new 2026-10-01; both confounds at once",
        },
    }

    print("=== Test 1: the donor split (handover item 1) ===")
    out["donor_split"] = {}
    for scheme in ("tablet+face", "tablet+face+richness"):
        report = donor_split_test(lines, "M288", "N45", "enriched", BLOCK_KEYS[scheme])
        out["donor_split"][scheme] = report
        print(f"  {scheme:22} p={report['p']:.3e} floor={report['p_floor']:.3e} "
              f"inf={report['informative_blocks']} obs/max={report['observed_overlap']}"
              f"/{report['max_possible_overlap']} donors={len(report['donor_tablets'])} "
              f"screened={report['screened_on_complement']}")

    print("=== Test 2: calibration of the donor-selection rule ===")
    out["calibration"] = calibration(
        lines, "M288", "N45", "enriched", BLOCK_KEYS["tablet+face"], args.replicates
    )
    c = out["calibration"]
    print(f"  replicates={c['replicates']} invariant={c['donor_set_invariant']} "
          f"P(p<=.05)={c['fraction_p_le_05']:.4f} P(p<=.01)={c['fraction_p_le_01']:.4f} "
          f"P(p<=.001)={c['fraction_p_le_001']:.5f} median={c['median_p']:.3f}")

    print("=== Test 3: the procedure at full search budget ===")
    out["procedure_null"] = procedure_null(
        lines, BLOCK_KEYS["tablet+face"],
        exclude={(m, n) for m, n, _ in CONFIRMED},
    )
    p = out["procedure_null"]
    print(f"  pairs_run={p['pairs_run']} with_power={p['pairs_with_power']} "
          f"P(p<=.05)={p['fraction_powered_p_le_05']} "
          f"P(p<=.001)={p['fraction_powered_p_le_001']}")

    print("=== Test 4: richness control, all eight pairs, full corpus ===")
    out["richness_control"] = richness_control(lines)
    header = f"  {'pair':12}" + "".join(f"{k.replace('tablet','T'):>24}" for k in BLOCK_KEYS)
    print(header)
    for pair, row in out["richness_control"].items():
        cells = ""
        for k in BLOCK_KEYS:
            r = row[k]
            mark = "" if r["has_power_at_05"] else "*"
            cells += f"{r['p']:>12.4f}/{r['p_floor']:<10.1e}{mark:>2}"
        print(f"  {pair:12}{cells}")
    print("  * = p-floor > 0.05, test has no power, failure uninformative")

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
