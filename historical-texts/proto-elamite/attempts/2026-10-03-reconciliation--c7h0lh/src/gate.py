"""Gate: reproduce the 2026-09-04 corpus audit and the 2026-09-17 face-blocked
table with THIS session's independently written block machinery. Nothing
downstream is believed unless this passes."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from recon_common import (load_eligible, exact_blocked, crude_cells,
                          PUBLISHED_EIGHT, split_name, odds_ratio)

corpus = Path(sys.argv[1])
files, lines, eligible = load_eligible(corpus)
tablets = sorted({l.tablet for l in lines})
empty = [f.name for f in files if not __import__("recon_common").parse_tablet(f)]

audit = {
    "files": len(files),
    "files_without_numbered_lines": len(empty),
    "tablets": len(tablets),
    "numbered_lines": len(lines),
    "eligible_lines": len(eligible),
}
expected_audit = {"files": 1467, "files_without_numbered_lines": 10,
                  "tablets": 1457, "numbered_lines": 11013, "eligible_lines": 4869}
print("CORPUS AUDIT", audit)
assert audit == expected_audit, f"audit mismatch: {audit} vs {expected_audit}"
print("  -> matches 2026-09-04 exactly")

# 2026-09-17 face-blocked table on the bucket-0 holdout
val = [l for l in eligible if split_name(l.tablet) == "validation"]
print(f"\nholdout lines: {len(val)}  (2026-09-04 records 1050)")
assert len(val) == 1050

ref = json.loads((Path(__file__).parents[2] /
                  "2026-09-17-exact-form-and-face" / "results" /
                  "power_floor.json").read_text())
print(json.dumps(ref, indent=1)[:400])

print("\n=== GATE: my exact_blocked vs 2026-09-17 power_floor.json ===")
ok = True
for m, t, d in PUBLISHED_EIGHT:
    key = f"{m}-{t}"
    for scheme, kf in (("tablet_blocked", lambda l: l.tablet),
                       ("face_blocked", lambda l: (l.tablet, l.surface))):
        got = exact_blocked(val, m, t, kf, d)
        exp = ref[key][scheme]
        for a, b in (("p", "p"), ("floor", "p_floor"),
                     ("observed", "observed_overlap"),
                     ("informative_blocks", "informative_blocks"),
                     ("blocks", "blocks")):
            gv, ev = got[a], exp[b]
            close = (abs(gv - ev) <= 1e-12 * max(1.0, abs(ev))) if isinstance(ev, float) else gv == ev
            if not close:
                ok = False
                print(f"  MISMATCH {key} {scheme} {a}: {gv} vs {ev}")
    print(f"  {key:12s} face p={ref[key]['face_blocked']['p']:.6g} "
          f"floor={ref[key]['face_blocked']['p_floor']:.3g}  OK")
assert ok, "gate failed"
print("GATE PASSED: all 8 pairs x 2 block schemes x 5 quantities reproduce to 1e-12")
