#!/usr/bin/env python3
"""
VALIDATOR 3 (refuter), SECOND PASS driver — 2026-10-03.

The 2026-10-02 refuter session built attack_arith*/nulls/split*/names/
structure/unfalsifiable/controls/witness_drift and died before posting a
verdict.  That suite is reproduced unchanged by `python3 run_all.py`
(verified bit-identical except for sort ties on equal-frequency items).

This driver runs only the NEW attacks added on 2026-10-03, so neither
out.txt nor any prior file is overwritten:

  R1  attack_r1_integration.py  the dossier as a GRAPH: is it "integrated"?
  R2  attack_r2_template.py     is the eight-node architecture a template
                                that fits any slice of the archive?
  R3  attack_r3_six.py          the two "fixed ratios" as corpus-wide
                                predictions; *327:VIR on its second attestation
  R4  attack_r4_cells.py        cell-level audit of scribe9_dossier.csv;
                                cohesion null drawn from attributed tablets only
  R5  attack_r5_priorart.py     are the frontier's results already written in
                                the commentary bundled with the claimant's own
                                data file?

    python3 run_refuter3b.py        -> out_refuter3b.txt
"""
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["attack_r1_integration.py", "attack_r2_template.py",
         "attack_r3_six.py", "attack_r4_cells.py", "attack_r5_priorart.py"]
out = []
for s in STEPS:
    out.append("\n" + "#" * 78 + f"\n### {s}\n" + "#" * 78)
    r = subprocess.run([sys.executable, os.path.join(HERE, s)],
                       capture_output=True, text=True, cwd=HERE)
    out.append(r.stdout)
    if r.returncode != 0:
        out.append("STDERR:\n" + r.stderr)
txt = "\n".join(out)
open(os.path.join(HERE, "out_refuter3b.txt"), "w").write(txt)
print(txt)
