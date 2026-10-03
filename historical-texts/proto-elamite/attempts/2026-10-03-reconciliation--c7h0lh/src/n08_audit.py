"""Is M376-N08A -- one of the three new pairs replicated by all four
candidate-expansion sweeps -- stable under the N08/N08A serialisation split
that u82zig flagged as a live-corpus renaming?"""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from recon_common import (load_eligible, exact_blocked, crude_cells,
                          odds_ratio, fisher_exact_two_sided)

corpus = Path(sys.argv[1])
_, _, eligible = load_eligible(corpus)
face = lambda l: (l.tablet, l.surface)

tally = {}
for l in eligible:
    for s in l.n_signs:
        if s.startswith("N08"):
            tally[s] = tally.get(s, 0) + 1
print("N08* signs on eligible lines (after the audited normaliser):", tally)

m376 = [l for l in eligible if "M376" in l.m_signs]
print(f"M376 eligible lines: {len(m376)}")
for s in sorted(tally):
    print(f"  carrying {s}: {sum(s in l.n_signs for l in m376)}")

out = {"n08_tally": tally, "m376_lines": len(m376), "variants": {}}
for label, tgt in (("N08A as parsed", {"N08A"}),
                   ("N08 alone", {"N08"}),
                   ("N08+N08A merged", {"N08", "N08A"}),
                   ("N08+N08A+N08B merged", {"N08", "N08A", "N08B"})):
    class _L:  # thin view that merges the target set into one pseudo-sign
        pass
    lines = []
    for l in eligible:
        v = _L(); v.tablet = l.tablet; v.surface = l.surface
        v.m_signs = l.m_signs
        v.n_signs = frozenset({"TGT"} if (l.n_signs & tgt) else set()) | (l.n_signs - tgt)
        lines.append(v)
    a, b, c, d = crude_cells(lines, "M376", "TGT")
    r = exact_blocked(lines, "M376", "TGT", face, "enriched")
    out["variants"][label] = {"cells": [a, b, c, d], "crude_or": odds_ratio(a, b, c, d),
                              "fisher_p": fisher_exact_two_sided(a, b, c, d),
                              "face_blocked_p": r["p"], "floor": r["floor"],
                              "informative_blocks": r["informative_blocks"]}
    print(f"{label:24s} cells={a:3d},{b:3d},{c:3d},{d:4d} OR={odds_ratio(a,b,c,d):8.2f} "
          f"face-blocked p={r['p']:.3g} floor={r['floor']:.2g} infB={r['informative_blocks']}")

Path("results/n08_audit.json").write_text(json.dumps(out, indent=2))
print("\nwrote results/n08_audit.json")
