#!/usr/bin/env python3
"""Exact-form audit for M263 and M288 — recommended experiment 3 of the 2026-09-17 handover.

2026-09-17 audited the M297 family merge and upheld it. M263 now carries the folder's most
robust constraint (M263-N01) and M288 carries the one this session is settling, and neither
family merge has been checked. `face_and_form.test_b` is documented as parameterised by
family but hardcodes `family = "M297"`, so the family loop is reimplemented here around the
same `exact_forms` parser and the same statistics.

Also reports the within-family homogeneity across every testable form, not just the top two.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[0] / "2026-09-17-exact-form-and-face"))
sys.path.insert(0, str(_HERE.parents[1] / "analysis"))

from face_and_form import eligible, exact_forms, load_lines  # noqa: E402
from structure_associations import fisher_exact_two_sided, odds_ratio  # noqa: E402

# Families to audit and the targets they carry in the 2026-09-04 constraint set.
FAMILIES = {
    "M263": ("N01", "N30C"),
    "M288": ("N45",),
    "M297": ("N39B", "N24", "N01"),  # re-run as a reproduction check against 2026-09-17
    "M243": ("N39B",),
    "M106": ("N24",),
}
MIN_LINES = 15


def audit(all_eligible, family, targets):
    per_form = defaultdict(list)
    counts = Counter()
    for ln in all_eligible:
        if family not in ln.m_signs:
            continue
        for form in exact_forms(ln.text, family):
            per_form[form].append(ln)
            counts[form] += 1
    others = [ln for ln in all_eligible if family not in ln.m_signs]
    testable = sorted((f for f, n in counts.items() if n >= MIN_LINES), key=lambda f: -counts[f])

    out = {
        "form_line_counts": dict(counts.most_common()),
        "testable_forms": testable,
        "targets": {},
    }
    for target in targets:
        c = sum(target in ln.n_signs for ln in others)
        d = len(others) - c
        forms = {}
        for form in testable:
            lines = per_form[form]
            a = sum(target in ln.n_signs for ln in lines)
            b = len(lines) - a
            forms[form] = {
                "lines": len(lines),
                "hits": a,
                "rate": a / len(lines),
                "odds_ratio_vs_rest": odds_ratio(a, b, c, d),
                "p_vs_rest": fisher_exact_two_sided(a, b, c, d),
            }
        pairs = []
        for i, f1 in enumerate(testable):
            for f2 in testable[i + 1:]:
                n1, n2 = forms[f1], forms[f2]
                a1, b1 = n1["hits"], n1["lines"] - n1["hits"]
                a2, b2 = n2["hits"], n2["lines"] - n2["hits"]
                pairs.append({
                    "form_1": f1, "form_2": f2, "table": [a1, b1, a2, b2],
                    "odds_ratio": odds_ratio(a1, b1, a2, b2),
                    "p_two_sided": fisher_exact_two_sided(a1, b1, a2, b2),
                })
        out["targets"][target] = {
            "base_rate_excluding_family": c / max(1, len(others)),
            "per_form": forms,
            "homogeneity_pairs": pairs,
        }
    return out


def main():
    corpus = Path((_HERE / "corpus_path.txt").read_text().strip())
    lines, _ = load_lines(corpus)
    el = eligible(lines)
    res = {"eligible_lines": len(el), "families": {}}
    for family, targets in FAMILIES.items():
        res["families"][family] = audit(el, family, targets)
    (_HERE / "results").mkdir(exist_ok=True)
    (_HERE / "results/exact_form_audit.json").write_text(json.dumps(res, indent=2) + "\n")

    for family, r in res["families"].items():
        forms = r["form_line_counts"]
        print(f"\n=== {family}  eligible-line counts by exact graphical form ===")
        print("  " + ", ".join(f"{f} {n}" for f, n in list(forms.items())[:8])
              + (f"  (+{len(forms)-8} more)" if len(forms) > 8 else ""))
        if len(r["testable_forms"]) < 2:
            print(f"  only {len(r['testable_forms'])} form(s) with >= {MIN_LINES} lines "
                  f"-> merge is not testable for this family")
            continue
        for target, t in r["targets"].items():
            print(f"  target {target}  base rate (non-{family} lines) {t['base_rate_excluding_family']:.3f}")
            for f, v in t["per_form"].items():
                print(f"    {f:12} n={v['lines']:4}  rate={v['rate']:.3f}  OR vs rest={v['odds_ratio_vs_rest']:6.2f}")
            for p in t["homogeneity_pairs"]:
                print(f"    homogeneity {p['form_1']} vs {p['form_2']}: "
                      f"OR={p['odds_ratio']:.2f}  p={p['p_two_sided']:.4f}")


if __name__ == "__main__":
    main()
