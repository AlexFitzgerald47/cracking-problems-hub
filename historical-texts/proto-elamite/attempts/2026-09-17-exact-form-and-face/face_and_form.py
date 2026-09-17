#!/usr/bin/env python3
"""Three audits of the 2026-09-04 Proto-Elamite constraint set.

A. Face-blocked null. The 2026-09-04 validation permutes the target within *tablet*,
   so any confound constant within a tablet is already controlled. Position within the
   tablet is not: a Proto-Elamite obverse carries itemised entries and the reverse
   carries totals. This re-runs the identical exact test with blocks keyed on
   (tablet, face).

B. Exact-form audit of M297. The published analysis merges M297, M297~B, M297~C,
   M297~D, M297~A, M297@b and compound membership into one family. This tests whether
   the plain form and the ~B form actually behave alike.

C. Cross-class self-match. Distance between an M-sign's numeral-context profile on the
   obverse and on the reverse, compared against the distance between different M-signs
   on the same face, with a within-tablet face-permutation null.

No lexical or phonetic value is assigned to any sign anywhere in this file.

Usage:
    python3 face_and_form.py /path/to/pe-sign-value-data/corpus --json results.json
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

# Reuse the audited 2026-09-04 parser and statistics verbatim.
_ANALYSIS_DIR = Path(__file__).resolve().parents[2] / "analysis"
sys.path.insert(0, str(_ANALYSIS_DIR))

from structure_associations import (  # noqa: E402
    Line,
    bh_adjust,
    corpus_digest,
    fisher_exact_two_sided,
    hypergeom_probability,
    normalize_n_sign,
    odds_ratio,
    parse_tablet,
    split_name,
)

# The eight numeral associations confirmed on held-out tablets in 2026-09-04,
# with the direction reported there. Source: analysis/results/associations.csv.
CONFIRMED = [
    ("M297", "N39B", "enriched"),
    ("M297", "N24", "enriched"),
    ("M297", "N01", "depleted"),
    ("M263", "N30C", "depleted"),
    ("M263", "N01", "enriched"),
    ("M243", "N39B", "enriched"),
    ("M106", "N24", "enriched"),
    ("M288", "N45", "enriched"),
]

# A sign token in this corpus appears either bare (`M297`, `M297~B`) or with the SFU
# value annotation `value<family<exactform` (`ri2<M297<M297~B`). The exact graphical
# form is the last `M###` token of the group, with its ~variant / @orientation intact.
EXACT_FORM_RE = re.compile(r"M[0-9]{3}(?:~[A-Za-z0-9]+)?(?:@[a-z]+)?")


def exact_forms(text: str, family: str) -> set[str]:
    """Exact graphical forms of `family` occurring in the entry field of a line."""
    entry_field = text.split(",", 1)[0] if "," in text else text
    found: set[str] = set()
    for group in entry_field.split():
        tokens = EXACT_FORM_RE.findall(group)
        if not tokens:
            continue
        relevant = [t for t in tokens if t.startswith(family)]
        if not relevant:
            continue
        if "<" in group:
            # value<family<exactform : the exact form is the final token.
            found.add(tokens[-1] if tokens[-1].startswith(family) else relevant[-1])
        else:
            # Bare sign or compound; every family member present is its own form.
            found.update(relevant)
    return found


def load_lines(corpus_dir: Path) -> tuple[list[Line], list[Path]]:
    files = sorted(corpus_dir.glob("*.values.atf"))
    lines: list[Line] = []
    for path in files:
        lines.extend(parse_tablet(path))
    return lines, files


def eligible(lines: Sequence[Line]) -> list[Line]:
    """Intact lines carrying both an M-sign and an accounting N-sign.

    This is the same eligibility filter the 2026-09-04 numeral analysis used.
    """
    return [ln for ln in lines if not ln.damaged and ln.m_signs and ln.n_signs]


def contingency(lines: Sequence[Line], m_sign: str, n_sign: str) -> tuple[int, int, int, int]:
    a = b = c = d = 0
    for ln in lines:
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
    return a, b, c, d


def blocked_randomization_p(
    lines: Sequence[Line],
    m_sign: str,
    n_sign: str,
    direction: str,
    block_key,
) -> float:
    """Exact one-sided test permuting the target only within each block.

    Identical to the 2026-09-04 `blocked_randomization_p` except that the block key
    is a parameter. `block_key=lambda ln: ln.tablet` reproduces that function exactly;
    `block_key=lambda ln: (ln.tablet, ln.surface)` is the stricter face-blocked null.
    """
    blocks: dict[object, list[Line]] = defaultdict(list)
    for ln in lines:
        blocks[block_key(ln)].append(ln)

    distribution = [1.0]
    observed_total = 0
    for block_lines in blocks.values():
        total = len(block_lines)
        sign_count = sum(m_sign in ln.m_signs for ln in block_lines)
        target_count = sum(n_sign in ln.n_signs for ln in block_lines)
        observed_total += sum(
            m_sign in ln.m_signs and n_sign in ln.n_signs for ln in block_lines
        )
        lower = max(0, sign_count - (total - target_count))
        upper = min(sign_count, target_count)
        local = [0.0] * (upper + 1)
        for overlap in range(lower, upper + 1):
            local[overlap] = hypergeom_probability(overlap, sign_count, target_count, total)

        combined = [0.0] * (len(distribution) + len(local) - 1)
        for i, pi in enumerate(distribution):
            if pi == 0.0:
                continue
            for j, pj in enumerate(local):
                if pj:
                    combined[i + j] += pi * pj
        distribution = combined

    if direction == "enriched":
        return min(1.0, sum(distribution[observed_total:]))
    if direction == "depleted":
        return min(1.0, sum(distribution[: observed_total + 1]))
    raise ValueError(direction)


# ---------------------------------------------------------------- Test A


def test_a(validation_lines: Sequence[Line]) -> dict:
    """Re-test the eight confirmed pairs under tablet-blocked and face-blocked nulls."""
    rows = []
    for m_sign, n_sign, direction in CONFIRMED:
        a, b, c, d = contingency(validation_lines, m_sign, n_sign)
        p_tablet = blocked_randomization_p(
            validation_lines, m_sign, n_sign, direction, lambda ln: ln.tablet
        )
        p_face = blocked_randomization_p(
            validation_lines,
            m_sign,
            n_sign,
            direction,
            lambda ln: (ln.tablet, ln.surface),
        )
        # How much blocking actually happened: blocks that became singletons carry no
        # information, so report the effective block structure too.
        tab_blocks = len({ln.tablet for ln in validation_lines})
        face_blocks = len({(ln.tablet, ln.surface) for ln in validation_lines})
        rows.append(
            {
                "m_sign": m_sign,
                "n_sign": n_sign,
                "direction": direction,
                "a": a,
                "b": b,
                "c": c,
                "d": d,
                "odds_ratio": odds_ratio(a, b, c, d),
                "p_tablet_blocked": p_tablet,
                "p_face_blocked": p_face,
                "tablet_blocks": tab_blocks,
                "face_blocks": face_blocks,
            }
        )
    for key, out in (("p_tablet_blocked", "q_tablet_blocked"), ("p_face_blocked", "q_face_blocked")):
        for row, q in zip(rows, bh_adjust([r[key] for r in rows])):
            row[out] = q
    return {"rows": rows}


def test_a_within_face(validation_lines: Sequence[Line]) -> dict:
    """Same eight pairs, computed separately on obverse-only and reverse-only lines."""
    rows = []
    for m_sign, n_sign, direction in CONFIRMED:
        entry = {"m_sign": m_sign, "n_sign": n_sign, "direction": direction}
        for face in ("obverse", "reverse"):
            face_lines = [ln for ln in validation_lines if ln.surface == face]
            a, b, c, d = contingency(face_lines, m_sign, n_sign)
            entry[face] = {
                "a": a,
                "b": b,
                "c": c,
                "d": d,
                "sign_lines": a + b,
                "odds_ratio": odds_ratio(a, b, c, d),
                "p_blocked": blocked_randomization_p(
                    face_lines, m_sign, n_sign, direction, lambda ln: ln.tablet
                )
                if a + b
                else None,
            }
        rows.append(entry)
    return {"rows": rows}


# ---------------------------------------------------------------- Test B


def test_b(all_eligible: Sequence[Line], targets=("N39B", "N24", "N01")) -> dict:
    """Exact-form audit: does plain M297 behave like M297~B?

    Run on the whole eligible corpus, not the 20% holdout: the question is about
    within-family homogeneity, not about confirming the published association, and
    M297~B has only 80 corpus occurrences in total.
    """
    family = "M297"
    per_form_lines: dict[str, list[Line]] = defaultdict(list)
    form_counts: Counter[str] = Counter()
    for ln in all_eligible:
        if family not in ln.m_signs:
            continue
        forms = exact_forms(ln.text, family)
        for form in forms:
            per_form_lines[form].append(ln)
        form_counts.update(forms)

    other_lines = [ln for ln in all_eligible if family not in ln.m_signs]

    results = {"form_line_counts": dict(form_counts.most_common()), "targets": {}}
    testable = [f for f, n in form_counts.items() if n >= 15]
    for target in targets:
        base_rate = sum(target in ln.n_signs for ln in other_lines) / max(1, len(other_lines))
        per_form = {}
        for form in sorted(testable, key=lambda f: -form_counts[f]):
            lines = per_form_lines[form]
            hits = sum(target in ln.n_signs for ln in lines)
            a, b = hits, len(lines) - hits
            c = sum(target in ln.n_signs for ln in other_lines)
            d = len(other_lines) - c
            per_form[form] = {
                "lines": len(lines),
                "hits": hits,
                "rate": hits / len(lines),
                "odds_ratio_vs_rest": odds_ratio(a, b, c, d),
                "p_vs_rest": fisher_exact_two_sided(a, b, c, d),
            }
        homogeneity = None
        if len(testable) >= 2:
            f1, f2 = sorted(testable, key=lambda f: -form_counts[f])[:2]
            n1, n2 = per_form[f1], per_form[f2]
            homogeneity = {
                "form_1": f1,
                "form_2": f2,
                "table": [n1["hits"], n1["lines"] - n1["hits"], n2["hits"], n2["lines"] - n2["hits"]],
                "odds_ratio": odds_ratio(
                    n1["hits"], n1["lines"] - n1["hits"], n2["hits"], n2["lines"] - n2["hits"]
                ),
                "p_two_sided": fisher_exact_two_sided(
                    n1["hits"], n1["lines"] - n1["hits"], n2["hits"], n2["lines"] - n2["hits"]
                ),
            }
        results["targets"][target] = {
            "corpus_base_rate_excluding_family": base_rate,
            "per_form": per_form,
            "homogeneity_top_two_forms": homogeneity,
        }
    return results


# ---------------------------------------------------------------- Test C


def profile(lines: Sequence[Line], m_sign: str, vocabulary: Sequence[str]) -> list[float] | None:
    subset = [ln for ln in lines if m_sign in ln.m_signs]
    if not subset:
        return None
    return [sum(n in ln.n_signs for ln in subset) / len(subset) for n in vocabulary]


def total_variation(p: Sequence[float], q: Sequence[float]) -> float:
    """Mean absolute difference over the vocabulary.

    These are independent presence probabilities, not a distribution over one
    categorical draw, so the mean absolute difference is the honest summary; it is
    bounded in [0, 1] and is the L1 distance divided by the vocabulary size.
    """
    return sum(abs(a - b) for a, b in zip(p, q)) / len(p)


def test_c(all_eligible: Sequence[Line], min_lines: int = 20, seed: int = 20260917) -> dict:
    obv = [ln for ln in all_eligible if ln.surface == "obverse"]
    rev = [ln for ln in all_eligible if ln.surface == "reverse"]

    counts = Counter()
    for ln in all_eligible:
        counts.update(ln.n_signs)
    vocabulary = [n for n, c in counts.most_common(15)]

    sign_faces = Counter()
    for face_lines in (obv, rev):
        seen = Counter()
        for ln in face_lines:
            seen.update(ln.m_signs)
        for sign, c in seen.items():
            if c >= min_lines:
                sign_faces[sign] += 1
    both_faces = sorted([s for s, c in sign_faces.items() if c == 2])

    self_distances = {}
    for sign in both_faces:
        p_o = profile(obv, sign, vocabulary)
        p_r = profile(rev, sign, vocabulary)
        self_distances[sign] = total_variation(p_o, p_r)

    cross_sign = {}
    for face, face_lines in (("obverse", obv), ("reverse", rev)):
        pairs = []
        profiles = {s: profile(face_lines, s, vocabulary) for s in both_faces}
        for i, s1 in enumerate(both_faces):
            for s2 in both_faces[i + 1 :]:
                pairs.append(total_variation(profiles[s1], profiles[s2]))
        cross_sign[face] = {
            "n_pairs": len(pairs),
            "mean": sum(pairs) / len(pairs) if pairs else None,
            "median": sorted(pairs)[len(pairs) // 2] if pairs else None,
        }

    # Null: permute the face label among a tablet's lines, preserving each tablet's
    # obverse/reverse line counts. Any self-distance that survives this is not simply
    # the sampling noise of splitting a sign's lines into two groups.
    rng = random.Random(seed)
    by_tablet: dict[str, list[Line]] = defaultdict(list)
    for ln in all_eligible:
        by_tablet[ln.tablet].append(ln)

    null_self = defaultdict(list)
    for _ in range(200):
        n_obv: list[Line] = []
        n_rev: list[Line] = []
        for tablet_lines in by_tablet.values():
            k = sum(ln.surface == "obverse" for ln in tablet_lines)
            shuffled = list(tablet_lines)
            rng.shuffle(shuffled)
            n_obv.extend(shuffled[:k])
            n_rev.extend(shuffled[k:])
        for sign in both_faces:
            p_o = profile(n_obv, sign, vocabulary)
            p_r = profile(n_rev, sign, vocabulary)
            if p_o and p_r:
                null_self[sign].append(total_variation(p_o, p_r))

    null_summary = {}
    for sign, draws in null_self.items():
        draws_sorted = sorted(draws)
        observed = self_distances[sign]
        null_summary[sign] = {
            "null_mean": sum(draws) / len(draws),
            "null_p95": draws_sorted[int(0.95 * len(draws_sorted))],
            "observed": observed,
            "p_right_tail": (sum(d >= observed for d in draws) + 1) / (len(draws) + 1),
        }

    observed_vals = list(self_distances.values())
    return {
        "vocabulary": vocabulary,
        "min_lines_per_face": min_lines,
        "signs_on_both_faces": both_faces,
        "self_distance_across_faces": self_distances,
        "self_distance_summary": {
            "n": len(observed_vals),
            "mean": sum(observed_vals) / len(observed_vals) if observed_vals else None,
            "median": sorted(observed_vals)[len(observed_vals) // 2] if observed_vals else None,
        },
        "cross_sign_distance_within_face": cross_sign,
        "face_permutation_null": null_summary,
    }


# ---------------------------------------------------------------- main


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)

    lines, files = load_lines(args.corpus)
    all_eligible = eligible(lines)
    validation = [ln for ln in all_eligible if split_name(ln.tablet) == "validation"]

    out = {
        "corpus": {
            "file_count": len(files),
            "sha256_lf": corpus_digest(files),
            "eligible_lines": len(all_eligible),
            "validation_lines": len(validation),
        },
        "test_a_face_blocked_null": test_a(validation),
        "test_a_within_face": test_a_within_face(validation),
        "test_b_exact_form_m297": test_b(all_eligible),
        "test_c_cross_face_self_match": test_c(all_eligible),
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out["corpus"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
