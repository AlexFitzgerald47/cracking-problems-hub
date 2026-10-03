#!/usr/bin/env python3
"""Reproduce the 2026-09-17 power_floor.json with the new generalised code.

If this cannot recover what is already established, the new code has a bug and
nothing downstream may be believed.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from blocks import (CONFIRMED, blocked_exact, eligible, face_key, load_corpus,
                    split_name, tablet_key)

corpus = Path(sys.argv[1])
published = json.loads((Path(__file__).resolve().parents[2]
                        / "2026-09-17-exact-form-and-face/results/power_floor.json").read_text())

lines, _ = load_corpus(corpus)
val = [ln for ln in eligible(lines) if split_name(ln.tablet) == "validation"]

bad = 0
print(f"{'pair':12} {'scheme':8} {'new p':>12} {'published p':>12} {'new floor':>12} {'pub floor':>12}  ok")
for m, n, d in CONFIRMED:
    for scheme, key in (("tablet", tablet_key), ("face", face_key)):
        got = blocked_exact(val, m, n, d, key)
        ref = published[f"{m}-{n}"][f"{scheme}_blocked"]
        ok = (abs(got["p"] - ref["p"]) < 1e-12
              and abs(got["p_floor"] - ref["p_floor"]) < 1e-12
              and got["observed_overlap"] == ref["observed_overlap"]
              and got["max_possible_overlap"] == ref["max_possible_overlap"]
              and got["informative_blocks"] == ref["informative_blocks"]
              and got["blocks"] == ref["blocks"])
        bad += not ok
        print(f"{m+'-'+n:12} {scheme:8} {got['p']:12.3e} {ref['p']:12.3e} "
              f"{got['p_floor']:12.3e} {ref['p_floor']:12.3e}  {'OK' if ok else 'MISMATCH'}")
print()
print("REPRODUCED EXACTLY" if bad == 0 else f"{bad} MISMATCHES — do not proceed")
sys.exit(1 if bad else 0)
