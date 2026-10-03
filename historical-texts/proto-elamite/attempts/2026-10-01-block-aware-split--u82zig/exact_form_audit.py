#!/usr/bin/env python3
"""Exact-form audit extended to M263 and M288 (folder item 3 of 2026-09-17).

2026-09-17 audited the M297 family merge and upheld it. M263 now carries two of
the three load-bearing constraints and M288 is the pair this session is about;
neither had been checked for the same merge assumption. The 2026-09-17 handover
says "same script, change the family argument in test_b" -- but `family` is a
hardcoded local in that function, not an argument, so this generalises it rather
than editing a committed attempt file.

The generalisation is verified by reproduction: run on M297 it must return the
published homogeneity p-values 0.0757 / 0.6941 / 0.1377 before its M263 and M288
output is trusted.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "analysis"))
sys.path.insert(0, str(_HERE.parents[1] / "attempts" / "2026-09-17-exact-form-and-face"))

from structure_associations import fisher_exact_two_sided, odds_ratio  # noqa: E402
from face_and_form import eligible, exact_forms, load_lines  # noqa: E402

# published direction for each family's targets
FAMILY_TARGETS = {
    "M297": ("N39B", "N24", "N01"),
    "M263": ("N30C", "N01"),
    "M288": ("N45",),
}
MIN_FORM_LINES = 15


def audit(all_eligible, family, targets):
    """test_b of face_and_form.py, with `family` as a parameter."""
    per_form_lines = defaultdict(list)
    form_counts = Counter()
    for ln in all_eligible:
        if family not in ln.m_signs:
            continue
        for form in exact_forms(ln.text, family):
            per_form_lines[form].append(ln)
            form_counts[form] += 1
    other_lines = [ln for ln in all_eligible if family not in ln.m_signs]

    out = {"form_line_counts": dict(form_counts.most_common()), "targets": {}}
    testable = [f for f, n in form_counts.items() if n >= MIN_FORM_LINES]
    for target in targets:
        base = sum(target in ln.n_signs for ln in other_lines) / max(1, len(other_lines))
        c = sum(target in ln.n_signs for ln in other_lines)
        d = len(other_lines) - c
        per_form = {}
        for form in sorted(testable, key=lambda f: -form_counts[f]):
            ls = per_form_lines[form]
            hits = sum(target in ln.n_signs for ln in ls)
            per_form[form] = {
                "lines": len(ls), "hits": hits, "rate": hits / len(ls),
                "odds_ratio_vs_rest": odds_ratio(hits, len(ls) - hits, c, d),
                "p_vs_rest": fisher_exact_two_sided(hits, len(ls) - hits, c, d),
            }
        homo = None
        if len(testable) >= 2:
            f1, f2 = sorted(testable, key=lambda f: -form_counts[f])[:2]
            n1, n2 = per_form[f1], per_form[f2]
            t = [n1["hits"], n1["lines"] - n1["hits"],
                 n2["hits"], n2["lines"] - n2["hits"]]
            homo = {"form_1": f1, "form_2": f2, "table": t,
                    "odds_ratio": odds_ratio(*t),
                    "p_two_sided": fisher_exact_two_sided(*t)}
        out["targets"][target] = {
            "corpus_base_rate_excluding_family": base,
            "per_form": per_form, "homogeneity_top_two_forms": homo,
        }
    return out


def main():
    corpus = Path((_HERE / "corpus_path.txt").read_text().strip())
    lines, _ = load_lines(corpus)
    el = eligible(lines)

    results = {}
    for family, targets in FAMILY_TARGETS.items():
        r = audit(el, family, targets)
        results[family] = r
        print("=" * 72)
        print(f"{family}  eligible-line counts by exact graphical form:")
        print("   " + "  ".join(f"{f} {n}" for f, n in r["form_line_counts"].items()))
        testable = [f for f, n in r["form_line_counts"].items() if n >= MIN_FORM_LINES]
        if len(testable) < 2:
            print(f"   only {len(testable)} form(s) reach {MIN_FORM_LINES} eligible "
                  "lines -- the merge is untestable for this family")
        for target, t in r["targets"].items():
            print(f"  target {target}  base rate (non-{family} lines) "
                  f"{t['corpus_base_rate_excluding_family']:.3f}")
            for form, v in t["per_form"].items():
                print(f"    {form:10} n={v['lines']:4}  rate {v['rate']:.3f}  "
                      f"OR vs rest {v['odds_ratio_vs_rest']:7.2f}")
            h = t["homogeneity_top_two_forms"]
            if h:
                print(f"    homogeneity {h['form_1']} vs {h['form_2']}: "
                      f"OR {h['odds_ratio']:.2f}  p = {h['p_two_sided']:.4f}")
        print()

    # reproduction gate
    pub = {"N39B": 0.0757, "N24": 0.6941, "N01": 0.1377}
    print("=" * 72)
    print("Reproduction gate -- M297 homogeneity p-values vs 2026-09-17 RESULTS.md")
    ok = True
    for target, expected in pub.items():
        got = results["M297"]["targets"][target]["homogeneity_top_two_forms"]["p_two_sided"]
        good = abs(got - expected) < 5e-5
        ok &= good
        print(f"  {target:5} published {expected:.4f}  recomputed {got:.4f}  "
              f"{'match' if good else 'MISMATCH'}")
    print(f"  gate: {'PASS -- the generalisation is faithful' if ok else 'FAIL'}")
    results["reproduction_gate_passed"] = bool(ok)

    (_HERE / "results").mkdir(exist_ok=True)
    (_HERE / "results" / "exact_form_audit.json").write_text(
        json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
