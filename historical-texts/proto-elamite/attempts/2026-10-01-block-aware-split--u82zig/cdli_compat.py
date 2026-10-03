#!/usr/bin/env python3
"""Does the 2026-09-04 parser read live CDLI ATF the same way it reads SFU ATF?

The 130 new tablets are only usable as a holdout if the parser behaves
identically on the two serialisations. This compares the parse of the 1,467
tablets present in BOTH the pinned SFU corpus and the live CDLI export, tablet
by tablet, and reports every disagreement. Nothing about the 130 new tablets is
read here.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "analysis"))
sys.path.insert(0, str(_HERE.parents[1] / "attempts" / "2026-09-17-exact-form-and-face"))

from structure_associations import parse_tablet  # noqa: E402
from face_and_form import eligible  # noqa: E402


def profile(corpus: Path, names: set[str]):
    per = {}
    for name in sorted(names):
        lines = parse_tablet(corpus / f"{name}.values.atf")
        el = eligible(lines)
        per[name] = {
            "lines": len(lines),
            "eligible": len(el),
            "m": Counter(s for ln in el for s in ln.m_signs),
            "n": Counter(s for ln in el for s in ln.n_signs),
            "faces": Counter(ln.surface for ln in lines),
        }
    return per


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pin_corpus", type=Path)
    ap.add_argument("cdli_corpus", type=Path)
    args = ap.parse_args()

    pin_names = {p.name.split(".")[0] for p in args.pin_corpus.glob("*.values.atf")}
    cdli_names = {p.name.split(".")[0] for p in args.cdli_corpus.glob("*.values.atf")}
    both = sorted(pin_names & cdli_names)
    print(f"comparing {len(both)} tablets present in both serialisations")

    a = profile(args.pin_corpus, set(both))
    b = profile(args.cdli_corpus, set(both))

    diffs = {"lines": [], "eligible": [], "m_signs": [], "n_signs": [], "faces": []}
    for name in both:
        if a[name]["lines"] != b[name]["lines"]:
            diffs["lines"].append((name, a[name]["lines"], b[name]["lines"]))
        if a[name]["eligible"] != b[name]["eligible"]:
            diffs["eligible"].append((name, a[name]["eligible"], b[name]["eligible"]))
        if a[name]["m"] != b[name]["m"]:
            diffs["m_signs"].append(name)
        if a[name]["n"] != b[name]["n"]:
            diffs["n_signs"].append(name)
        if a[name]["faces"] != b[name]["faces"]:
            diffs["faces"].append(name)

    tot = lambda p, k: sum(v[k] for v in p.values())  # noqa: E731
    print(f"\n{'quantity':22} {'pinned SFU':>12} {'live CDLI':>12} {'tablets differing':>19}")
    print(f"{'numbered lines':22} {tot(a,'lines'):>12} {tot(b,'lines'):>12} "
          f"{len(diffs['lines']):>19}")
    print(f"{'eligible lines':22} {tot(a,'eligible'):>12} {tot(b,'eligible'):>12} "
          f"{len(diffs['eligible']):>19}")
    print(f"{'M-sign multiset':22} {'':>12} {'':>12} {len(diffs['m_signs']):>19}")
    print(f"{'N-sign multiset':22} {'':>12} {'':>12} {len(diffs['n_signs']):>19}")
    print(f"{'face assignment':22} {'':>12} {'':>12} {len(diffs['faces']):>19}")

    for key in ("lines", "eligible"):
        if diffs[key]:
            print(f"\nfirst 10 tablets differing on {key}:")
            for row in diffs[key][:10]:
                print(f"  {row}")
    for key in ("m_signs", "n_signs"):
        if diffs[key]:
            print(f"\nfirst 5 tablets differing on {key}:")
            for name in diffs[key][:5]:
                da = a[name]["m" if key == "m_signs" else "n"]
                db = b[name]["m" if key == "m_signs" else "n"]
                only_a = {k: v for k, v in da.items() if db.get(k, 0) != v}
                only_b = {k: v for k, v in db.items() if da.get(k, 0) != v}
                print(f"  {name}: pinned {only_a}  cdli {only_b}")

    # the two signs this session's test depends on
    print("\nCorpus-wide counts for the signs under test:")
    for sign, field in (("M288", "m"), ("M297", "m"), ("M263", "m"),
                        ("N45", "n"), ("N39B", "n"), ("N01", "n")):
        ca = sum(v[field].get(sign, 0) for v in a.values())
        cb = sum(v[field].get(sign, 0) for v in b.values())
        flag = "" if ca == cb else "   <-- DIFFERS"
        print(f"  {sign:6} pinned {ca:6}  live CDLI {cb:6}{flag}")

    out = {
        "tablets_compared": len(both),
        "pinned_total_lines": tot(a, "lines"),
        "cdli_total_lines": tot(b, "lines"),
        "pinned_total_eligible": tot(a, "eligible"),
        "cdli_total_eligible": tot(b, "eligible"),
        "tablets_differing": {k: (len(v) if isinstance(v, list) else v)
                              for k, v in diffs.items()},
        "line_count_diffs": diffs["lines"][:50],
        "eligible_diffs": diffs["eligible"][:50],
        "m_sign_diff_tablets": diffs["m_signs"][:50],
        "n_sign_diff_tablets": diffs["n_signs"][:50],
    }
    (_HERE / "results").mkdir(exist_ok=True)
    (_HERE / "results" / "cdli_compat.json").write_text(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
