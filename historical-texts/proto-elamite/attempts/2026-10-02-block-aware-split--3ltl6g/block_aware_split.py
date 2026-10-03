#!/usr/bin/env python3
"""Block-aware split for the M288-N45 constraint (2026-10-02 Breaker session).

Recommended experiment 1 of the 2026-09-17 handover. The published tablet-hash holdout
leaves the face-blocked exact test with a p-value floor of 0.12 for M288-N45: only 4 of
290 tablet-faces are informative, so the test cannot return a significant answer however
the data fall. This builds a split that guarantees power, re-screens candidates on the
complement, and reports both complementary arms.

Legitimacy of designing a split from marginals: the face-blocked test conditions on each
block's (n_lines, n_M_lines, n_target_lines). Informativeness and the p-floor are
functions of exactly those three numbers. The observed overlap is never consulted by the
split rule. See PREDICTIONS.md.

Usage:
    python3 block_aware_split.py /path/to/pe-sign-value-data/corpus --json results/x.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Callable, Sequence

_HERE = Path(__file__).resolve().parent
_PREV = _HERE.parents[0] / "2026-09-17-exact-form-and-face"
_ANALYSIS = _HERE.parents[1] / "analysis"
sys.path.insert(0, str(_PREV))
sys.path.insert(0, str(_ANALYSIS))

from structure_associations import (  # noqa: E402
    Line,
    bh_adjust,
    corpus_digest,
    fisher_exact_two_sided,
    hypergeom_probability,
    odds_ratio,
    parse_tablet,
    split_name,
)
from face_and_form import CONFIRMED, eligible, load_lines  # noqa: E402

PAIR = ("M288", "N45")
FACE_KEY: Callable[[Line], object] = lambda ln: (ln.tablet, ln.surface)


# --------------------------------------------------------------------------- marginals

def block_marginals(lines: Sequence[Line], m_sign: str, n_sign: str, block_key=FACE_KEY):
    """Per-block (total, n_M_lines, n_target_lines) and nothing else.

    This is the only function the split rule is allowed to consult. It deliberately does
    not compute the overlap.
    """
    blocks: dict[object, list[Line]] = defaultdict(list)
    for ln in lines:
        blocks[block_key(ln)].append(ln)
    out = {}
    for key, bl in blocks.items():
        total = len(bl)
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(n_sign in ln.n_signs for ln in bl)
        out[key] = (total, s, t)
    return out


def informative_blocks(marginals):
    """Blocks whose overlap has freedom to vary, with P(max overlap) for each."""
    out = {}
    for key, (total, s, t) in marginals.items():
        lo = max(0, s - (total - t))
        hi = min(s, t)
        if hi > lo:
            out[key] = {
                "total": total,
                "m_lines": s,
                "target_lines": t,
                "lo": lo,
                "hi": hi,
                "p_max": hypergeom_probability(hi, s, t, total),
            }
    return out


def floor_from_blocks(info_blocks) -> float:
    """p-floor of an enriched face-blocked test = product of P(max) over informatives."""
    product = 1.0
    for v in info_blocks.values():
        product *= v["p_max"]
    return product


# ------------------------------------------------------------------------------- tests

def blocked_p_and_floor(lines, m_sign, n_sign, direction, block_key=FACE_KEY):
    """Exact blocked randomization p, with its floor, observed and max overlap.

    The convolution is identical in structure to analysis/structure_associations.py's
    blocked_randomization_p and to the 2026-09-17 power_floor.floors; it is reimplemented
    here only so that this file is self-contained and unit-testable against both.
    """
    blocks: dict[object, list[Line]] = defaultdict(list)
    for ln in lines:
        blocks[block_key(ln)].append(ln)

    dist = [1.0]
    observed = 0
    max_possible = 0
    min_possible = 0
    informative = 0
    for bl in blocks.values():
        total = len(bl)
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(n_sign in ln.n_signs for ln in bl)
        observed += sum(m_sign in ln.m_signs and n_sign in ln.n_signs for ln in bl)
        lo = max(0, s - (total - t))
        hi = min(s, t)
        max_possible += hi
        min_possible += lo
        if hi > lo:
            informative += 1
        local = [0.0] * (hi + 1)
        for k in range(lo, hi + 1):
            local[k] = hypergeom_probability(k, s, t, total)
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        comb[i + j] += pi * pj
        dist = comb

    if direction == "enriched":
        p = min(1.0, sum(dist[observed:]))
        p_floor = min(1.0, sum(dist[max_possible:]))
    elif direction == "depleted":
        p = min(1.0, sum(dist[: observed + 1]))
        p_floor = min(1.0, sum(dist[: min_possible + 1]))
    else:
        raise ValueError(direction)
    return {
        "p": p,
        "p_floor": p_floor,
        "observed_overlap": observed,
        "max_possible_overlap": max_possible,
        "min_possible_overlap": min_possible,
        "informative_blocks": informative,
        "blocks": len(blocks),
        "has_power_at_05": p_floor <= 0.05,
    }


def contingency(lines, m_sign, n_sign):
    a = b = c = d = 0
    for ln in lines:
        hs = m_sign in ln.m_signs
        ht = n_sign in ln.n_signs
        if hs and ht:
            a += 1
        elif hs:
            b += 1
        elif ht:
            c += 1
        else:
            d += 1
    return a, b, c, d


# ------------------------------------------------------------------------------- split

def carrier_tablets(lines, m_sign, n_sign):
    """Tablets holding >=1 informative (tablet,face) block for the pair. Marginals only."""
    info = informative_blocks(block_marginals(lines, m_sign, n_sign))
    return sorted({tablet for tablet, _face in info})


def arm_split(lines, arm: str, m_sign=PAIR[0], n_sign=PAIR[1]):
    """Validation = parity-assigned carriers UNION bucket-0 non-carriers."""
    carriers = carrier_tablets(lines, m_sign, n_sign)
    want = 0 if arm == "A" else 1
    assigned = {t for i, t in enumerate(carriers) if i % 2 == want}
    carrier_set = set(carriers)
    validation = set(assigned)
    for ln in lines:
        if ln.tablet not in carrier_set and split_name(ln.tablet) == "validation":
            validation.add(ln.tablet)
    return validation, carriers, sorted(assigned)


# ----------------------------------------------------------------------- full pipeline

def screen(train_lines, minimum_m_lines=20, minimum_target_lines=20):
    """Re-screen numeral associations from scratch on a training set.

    Identical rule to analysis/structure_associations.py discover_and_validate's
    selection stage: Fisher two-sided on lines, BH q <= 0.01, corrected OR >= 3 or <= 1/3.
    """
    m_signs = sorted({s for ln in train_lines for s in ln.m_signs})
    n_signs = sorted({s for ln in train_lines for s in ln.n_signs})
    raw = []
    for n_sign in n_signs:
        target_lines = sum(n_sign in ln.n_signs for ln in train_lines)
        if target_lines < minimum_target_lines:
            continue
        for m_sign in m_signs:
            a, b, c, d = contingency(train_lines, m_sign, n_sign)
            if a + b < minimum_m_lines:
                continue
            raw.append(
                {
                    "m_sign": m_sign,
                    "target": n_sign,
                    "cells": (a, b, c, d),
                    "odds_ratio": odds_ratio(a, b, c, d),
                    "p": fisher_exact_two_sided(a, b, c, d),
                }
            )
    qs = bh_adjust([r["p"] for r in raw])
    for r, q in zip(raw, qs):
        r["q"] = q
    selected = [
        r for r in raw
        if r["q"] <= 0.01 and (r["odds_ratio"] >= 3.0 or r["odds_ratio"] <= 1 / 3.0)
    ]
    return selected, raw


def validate(validation_lines, selected):
    """Face-blocked exact validation of a re-screened candidate set, with BH over it."""
    rows = []
    for r in selected:
        direction = "enriched" if r["odds_ratio"] > 1 else "depleted"
        res = blocked_p_and_floor(
            validation_lines, r["m_sign"], r["target"], direction
        )
        cells = contingency(validation_lines, r["m_sign"], r["target"])
        rows.append(
            {
                "m_sign": r["m_sign"],
                "target": r["target"],
                "direction": direction,
                "train_cells": list(r["cells"]),
                "train_odds_ratio": r["odds_ratio"],
                "train_q": r["q"],
                "validation_cells": list(cells),
                "validation_odds_ratio": odds_ratio(*cells),
                **res,
            }
        )
    qs = bh_adjust([r["p"] for r in rows])
    for r, q in zip(rows, qs):
        r["q"] = q
        same_dir = (
            (r["train_odds_ratio"] > 1 and r["validation_odds_ratio"] > 1)
            or (r["train_odds_ratio"] < 1 and r["validation_odds_ratio"] < 1)
        )
        r["confirmed"] = bool(
            same_dir
            and r["q"] <= 0.05
            and (r["validation_odds_ratio"] >= 1.5 or r["validation_odds_ratio"] <= 1 / 1.5)
            and (r["validation_cells"][0] + r["validation_cells"][1]) >= 5
        )
    return sorted(rows, key=lambda r: r["q"])


# ----------------------------------------------- exhaustive split-robustness enumeration

def enumerate_splits(lines, m_sign=PAIR[0], n_sign=PAIR[1], floor_cap=0.05):
    """Every assignment of the carrier tablets, exactly.

    The face-blocked p-value depends only on which informative blocks the validation set
    holds: non-informative blocks have hi == lo and shift the observed total and the
    null's support by the same constant. So enumerating subsets of carrier tablets
    characterises every possible block-aware split exhaustively -- no sampling.
    """
    info = informative_blocks(block_marginals(lines, m_sign, n_sign))
    by_tablet: dict[str, list[dict]] = defaultdict(list)
    for (tablet, _face), v in info.items():
        by_tablet[tablet].append(v)
    tablets = sorted(by_tablet)

    # observed overlap per informative block, needed only for the enumeration's p-values
    blocks: dict[object, list[Line]] = defaultdict(list)
    for ln in lines:
        blocks[FACE_KEY(ln)].append(ln)
    obs = {}
    for key in info:
        obs[key] = sum(
            m_sign in ln.m_signs and n_sign in ln.n_signs for ln in blocks[key]
        )
    obs_by_tablet: dict[str, list[int]] = defaultdict(list)
    for (tablet, face), v in info.items():
        obs_by_tablet[tablet].append(obs[(tablet, face)])

    results = []
    for mask in range(1 << len(tablets)):
        chosen = [t for i, t in enumerate(tablets) if mask >> i & 1]
        if not chosen:
            continue
        dist = [1.0]
        observed = 0
        max_possible = 0
        for t in chosen:
            for v, o in zip(by_tablet[t], obs_by_tablet[t]):
                observed += o
                max_possible += v["hi"]
                local = [0.0] * (v["hi"] + 1)
                for k in range(v["lo"], v["hi"] + 1):
                    local[k] = hypergeom_probability(
                        k, v["m_lines"], v["target_lines"], v["total"]
                    )
                comb = [0.0] * (len(dist) + len(local) - 1)
                for i, pi in enumerate(dist):
                    if pi:
                        for j, pj in enumerate(local):
                            if pj:
                                comb[i + j] += pi * pj
                dist = comb
        p = min(1.0, sum(dist[observed:]))
        p_floor = min(1.0, sum(dist[max_possible:]))
        results.append(
            {
                "mask": mask,
                "n_tablets": len(chosen),
                "n_blocks": sum(len(by_tablet[t]) for t in chosen),
                "p": p,
                "p_floor": p_floor,
                "observed_overlap": observed,
                "max_possible_overlap": max_possible,
            }
        )
    powered = [r for r in results if r["p_floor"] <= floor_cap]
    fired = [r for r in powered if r["p"] <= 0.05]
    return {
        "carrier_tablets": tablets,
        "total_assignments": len(results),
        "powered_at_05": len(powered),
        "fired_among_powered": len(fired),
        "fraction_fired": (len(fired) / len(powered)) if powered else None,
        "powered_p_quantiles": _quantiles([r["p"] for r in powered]),
        "all": results,
    }


def _quantiles(values, points=(0.0, 0.05, 0.25, 0.5, 0.75, 0.95, 1.0)):
    if not values:
        return {}
    s = sorted(values)
    out = {}
    for q in points:
        idx = min(len(s) - 1, max(0, int(round(q * (len(s) - 1)))))
        out[str(q)] = s[idx]
    return out


# -------------------------------------------------------------------------------- main

def run(corpus_dir: Path) -> dict:
    lines, files = load_lines(corpus_dir)
    el = eligible(lines)
    out: dict[str, object] = {
        "schema_version": 1,
        "corpus": {
            "file_count": len(files),
            "sha256": corpus_digest(files),
            "eligible_line_count": len(el),
        },
        "pair": "-".join(PAIR),
    }

    # published holdout, for the like-for-like comparison
    pub_val = [ln for ln in el if split_name(ln.tablet) == "validation"]
    out["published_holdout"] = blocked_p_and_floor(pub_val, *PAIR, "enriched")
    out["full_corpus"] = blocked_p_and_floor(el, *PAIR, "enriched")

    marg = block_marginals(el, *PAIR)
    info = informative_blocks(marg)
    out["informative_blocks_corpus_wide"] = {
        f"{t}|{f}": v for (t, f), v in sorted(info.items())
    }

    arms = {}
    for arm in ("A", "B"):
        val_tablets, carriers, assigned = arm_split(el, arm)
        val = [ln for ln in el if ln.tablet in val_tablets]
        train = [ln for ln in el if ln.tablet not in val_tablets]
        val_info = informative_blocks(block_marginals(val, *PAIR))
        selected, raw = screen(train)
        rows = validate(val, selected)
        pair_row = next(
            (r for r in rows if (r["m_sign"], r["target"]) == PAIR), None
        )
        pair_screen = next(
            (r for r in raw if (r["m_sign"], r["target"]) == PAIR), None
        )
        arms[arm] = {
            "assigned_carriers": assigned,
            "validation_tablets": len(val_tablets),
            "validation_lines": len(val),
            "training_lines": len(train),
            "validation_informative_blocks": len(val_info),
            "validation_p_floor_from_marginals": floor_from_blocks(val_info),
            "candidates_rescreened": len(selected),
            "pair_screened_in": pair_row is not None,
            "pair_training_screen": (
                {
                    "cells": list(pair_screen["cells"]),
                    "odds_ratio": pair_screen["odds_ratio"],
                    "p": pair_screen["p"],
                    "q": pair_screen["q"],
                }
                if pair_screen
                else None
            ),
            "pair_validation": pair_row,
            "all_validation_rows": rows,
        }
    out["arms"] = arms
    out["enumeration"] = enumerate_splits(el)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("corpus_dir", type=Path)
    ap.add_argument("--json", type=Path, required=True)
    args = ap.parse_args()
    res = run(args.corpus_dir)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    enum = res["enumeration"]
    slim = dict(res)
    slim["enumeration"] = {k: v for k, v in enum.items() if k != "all"}
    args.json.write_text(json.dumps(slim, indent=2) + "\n", encoding="utf-8")
    # The 32,767-row enumeration is written as gzipped CSV: committed so the
    # split-robustness claim is checkable without the corpus, small enough to live in git.
    import csv as _csv
    import gzip as _gzip
    with _gzip.open(args.json.parent / "enumeration_full.csv.gz", "wt", newline="",
                    compresslevel=9) as fh:
        w = _csv.writer(fh)
        w.writerow(["mask", "n_tablets", "n_blocks", "observed_overlap",
                    "max_possible_overlap", "p", "p_floor"])
        for r in sorted(enum["all"], key=lambda r: r["mask"]):
            w.writerow([r["mask"], r["n_tablets"], r["n_blocks"], r["observed_overlap"],
                        r["max_possible_overlap"], f"{r['p']:.10g}", f"{r['p_floor']:.10g}"])

    print(f"corpus digest {res['corpus']['sha256'][:12]}…  eligible {res['corpus']['eligible_line_count']}")
    pub, full = res["published_holdout"], res["full_corpus"]
    print(f"\n{'set':26} {'p':>10} {'floor':>10} {'obs/max':>9} {'infBlk':>7} power")
    print(f"{'published bucket-0':26} {pub['p']:10.5f} {pub['p_floor']:10.5f} "
          f"{str(pub['observed_overlap'])+'/'+str(pub['max_possible_overlap']):>9} "
          f"{pub['informative_blocks']:7} {'YES' if pub['has_power_at_05'] else 'NO'}")
    print(f"{'full corpus (in-sample)':26} {full['p']:10.5e} {full['p_floor']:10.5f} "
          f"{str(full['observed_overlap'])+'/'+str(full['max_possible_overlap']):>9} "
          f"{full['informative_blocks']:7} {'YES' if full['has_power_at_05'] else 'NO'}")
    for arm, v in res["arms"].items():
        r = v["pair_validation"]
        if r is None:
            print(f"{'arm '+arm+' (NOT re-screened)':26}")
            continue
        print(f"{'arm '+arm+' block-aware':26} {r['p']:10.5e} {r['p_floor']:10.3e} "
              f"{str(r['observed_overlap'])+'/'+str(r['max_possible_overlap']):>9} "
              f"{r['informative_blocks']:7} {'YES' if r['has_power_at_05'] else 'NO'}"
              f"   q={r['q']:.4g} OR={r['validation_odds_ratio']:.2f} confirmed={r['confirmed']}")
    for arm, v in res["arms"].items():
        s = v["pair_training_screen"]
        print(f"\narm {arm}: {v['validation_tablets']} validation tablets, "
              f"{v['validation_lines']} lines, {v['validation_informative_blocks']} informative blocks, "
              f"floor(marginals)={v['validation_p_floor_from_marginals']:.3e}")
        print(f"  carriers to validation: {', '.join(v['assigned_carriers'])}")
        print(f"  re-screened candidates: {v['candidates_rescreened']}; "
              f"M288-N45 training OR={s['odds_ratio']:.2f} q={s['q']:.3g} "
              f"-> screened in: {v['pair_screened_in']}")
        conf = [f"{r['m_sign']}-{r['target']}" for r in v["all_validation_rows"] if r["confirmed"]]
        print(f"  confirmed on this arm ({len(conf)}): {', '.join(conf)}")
    e = res["enumeration"]
    print(f"\nexhaustive split enumeration over {len(e['carrier_tablets'])} carrier tablets:")
    print(f"  assignments {e['total_assignments']}, powered at floor<=0.05: {e['powered_at_05']}, "
          f"of those p<=0.05: {e['fired_among_powered']} ({e['fraction_fired']:.4f})")
    print(f"  p quantiles among powered splits: " +
          ", ".join(f"{k}:{v:.4g}" for k, v in e["powered_p_quantiles"].items()))


if __name__ == "__main__":
    main()
