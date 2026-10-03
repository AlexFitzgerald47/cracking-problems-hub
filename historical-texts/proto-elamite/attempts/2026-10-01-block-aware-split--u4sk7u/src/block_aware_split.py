#!/usr/bin/env python3
"""Recommended experiment 1 of the 2026-09-17 handover, run as specified.

Build a split that guarantees the validation set holds the informative
(tablet, face) blocks for the pair under test, re-screen candidates on the
complement with the unchanged 2026-09-04 screen, and re-run the face-blocked
exact test. Done for all eight published pairs, not only M288-N45, so the
pair of interest is read against its siblings rather than alone.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from blocks import (CONFIRMED, block_aware_split, blocked_exact, corpus_digest,
                    eligible, face_key, informative_blocks, load_corpus,
                    odds_ratio, pooled, rescreen, split_name, tablet_key)

corpus = Path(sys.argv[1])
lines, files = load_corpus(corpus)
el = eligible(lines)
out = {"corpus": {"file_count": len(files), "sha256": corpus_digest(files),
                  "eligible_lines": len(el)},
       "method": {
           "split": "validation = every tablet owning an informative (tablet, face) block "
                    "for the pair under test; training = all other tablets",
           "informative": "min(s,t) > max(0, s-(total-t)); a function of block marginals only, "
                          "never of the overlap",
           "screen": "unchanged 2026-09-04 numeral screen re-run on the new training set: "
                     "support >=20/>=20, Fisher two-sided, BH q<=0.01, corrected OR>=3 or <=1/3",
           "test": "exact conditional test permuting the target within (tablet, face)",
       },
       "pairs": {}}

for m, n, d in CONFIRMED:
    val_tablets = block_aware_split(el, m, n, face_key)
    train = [ln for ln in el if ln.tablet not in val_tablets]
    val = [ln for ln in el if ln.tablet in val_tablets]
    scr = rescreen(train)
    row = scr.get((m, n))
    res_face = blocked_exact(val, m, n, d, face_key)
    res_tab = blocked_exact(val, m, n, d, tablet_key)
    a, b, c, dd = pooled(val, m, n)
    out["pairs"][f"{m}-{n}"] = {
        "direction": d,
        "validation_tablets": len(val_tablets),
        "validation_lines": len(val),
        "training_lines": len(train),
        "informative_blocks_corpus": len(informative_blocks(el, m, n, face_key)),
        "informative_blocks_in_validation": res_face["informative_blocks"],
        "informative_blocks_left_in_training":
            len(informative_blocks(train, m, n, face_key)),
        "rescreen": None if row is None else {
            "cells": list(row["cells"]), "odds_ratio": row["or"],
            "p": row["p"], "q": row["q"], "selected": row["selected"]},
        "validation_pooled_cells": [a, b, c, dd],
        "validation_pooled_or": odds_ratio(a, b, c, dd),
        "face_blocked": res_face,
        "tablet_blocked": res_tab,
    }

Path("results").mkdir(exist_ok=True)
Path("results/block_aware_split.json").write_text(json.dumps(out, indent=2) + "\n")

print(f"{'pair':12} {'rescreen':>22} {'infBlk val':>10} {'floor':>10} {'obs/max':>9} {'p (face)':>10} {'verdict':>12}")
for pair, v in out["pairs"].items():
    r = v["rescreen"]
    scr = "not screened" if r is None else "q=%.2e OR=%.2f %s" % (r['q'], r['odds_ratio'], 'SEL' if r['selected'] else 'drop')
    f = v["face_blocked"]
    if not f["has_power_at_05"]:
        verdict = "UNTESTABLE"
    elif r is None or not r["selected"]:
        verdict = "no candidate"
    elif f["p"] <= 0.05:
        verdict = "CONFIRMS"
    else:
        verdict = "REFUTED"
    print(f"{pair:12} {scr:>22} {v['informative_blocks_in_validation']:10} "
          f"{f['p_floor']:10.2e} "
          f"{str(f['observed_overlap'])+'/'+str(f['max_possible_overlap']):>9} "
          f"{f['p']:10.3e} {verdict:>12}")
