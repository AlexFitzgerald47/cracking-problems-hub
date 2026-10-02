#!/usr/bin/env python3
"""
VALIDATOR 3 (refuter) driver, 2026-10-02, Linear A.
Runs every attack in order and writes the whole log to out.txt.

    python3 run_all.py            # offline, against vendored ./data
    python3 corpus.py fetch       # re-download both witnesses
    python3 fetch_priorart.sh     # re-download the prior-art documents

Attack index
  1a-1d  attack_arith.py / attack_arith2.py / attack_arith3.py
         damage-aware audit of every total the dossier quotes; what the
         arithmetic mismatches actually mean
  2      attack_nulls.py       coincidence base rates for the 1:2 ratio, the
                               gang partition and the 65+1=66 bridge
  3,3'   attack_split.py       post-hoc decomposition: size-matched null, every
                               other scribe, findspot-matched null
  3d,3e  attack_split2.py      scribe-label permutation with selection
                               correction; findspot AND size matched null
  4      attack_names.py       are the shared names informative; DI-KI-SE base rate
  5      attack_structure.py   KI-RO scope on HT117; HT85 face balance; HT85b
                               witness divergence
  6,7    attack_unfalsifiable.py  A-DU polarity decidability; falsifiability of
                               the construction grammar; corpus coverage
  8      attack_controls.py    the claimed 'arithmetic/cardinality controls 6/6'
  9      attack_witness_drift.py  the digital witness is an unpinned moving edition
"""
import subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = ["attack_arith.py", "attack_arith2.py", "attack_arith3.py",
         "attack_nulls.py", "attack_split.py", "attack_split2.py",
         "attack_names.py", "attack_structure.py", "attack_unfalsifiable.py",
         "attack_controls.py", "attack_witness_drift.py"]

def main():
    out = []
    for s in STEPS:
        out.append("\n" + "#" * 78 + f"\n### {s}\n" + "#" * 78)
        r = subprocess.run([sys.executable, os.path.join(HERE, s)],
                           capture_output=True, text=True, cwd=HERE)
        out.append(r.stdout)
        if r.returncode != 0:
            out.append("STDERR:\n" + r.stderr)
    txt = "\n".join(out)
    open(os.path.join(HERE, "out.txt"), "w").write(txt)
    print(txt)

if __name__ == "__main__":
    main()
