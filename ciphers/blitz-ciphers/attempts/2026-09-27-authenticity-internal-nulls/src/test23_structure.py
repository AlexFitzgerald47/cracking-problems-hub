"""Tests 2 and 3 of FREEZE.md: bigram structure and doublet rate against a
within-line unigram-shuffle null.  Pipeline is validated on Copiale and Borg
(known-genuine, solved, verified) before being applied to Blitz.

Usage: python3 src/test23_structure.py <comparanda_dir>
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from blitzlib import load_blitz, load_canonical, flat
import fastnull

COMP = sys.argv[1]
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = {"targets": {}}


def run(name, lines, nperm=20000, seed=7):
    r = fastnull.run(lines, nperm=nperm, seed=seed)
    out["targets"][name] = r
    b, d = r["bigram"], r["doublet"]
    print(f"{name:26s} n={r['n_tokens']:6d} types={r['n_types']:3d} | "
          f"bigramIC obs={b['obs']:.5f} exp={b['mean']:.5f} z={b['z']:+8.2f} "
          f"p_up={b['p_upper']:.5f} | doublets obs={d['obs']:.0f} "
          f"exp={d['mean']:.1f} z={d['z']:+6.2f} p_up={d['p_upper']:.4f} "
          f"p_lo={d['p_lower']:.4f}")
    sys.stdout.flush()


blitz = load_blitz(os.path.join(HERE, "data"))
cop = load_canonical(os.path.join(COMP, "copiale"))
borg = load_canonical(os.path.join(COMP, "borg"))

print("=== Blitz (primary evidence) ===")
run("blitz_p7", blitz["p7"])
run("blitz_p8", blitz["p8"])
run("blitz_p7+p8", blitz["p7"] + blitz["p8"])

print("\n=== Known-genuine, single pages (prediction 2a / 3a) ===")
for label, doc in (("copiale", cop), ("borg", borg)):
    ks = sorted(doc)
    for k in (ks[len(ks) // 10], ks[len(ks) // 2], ks[9 * len(ks) // 10]):
        run(f"{label}:{k}", doc[k])

print("\n=== Known-genuine, whole documents ===")
run("copiale:ALL", [l for k in sorted(cop) for l in cop[k]], nperm=2000)
run("borg:ALL", [l for k in sorted(borg) for l in borg[k]], nperm=2000)

json.dump(out, open(os.path.join(HERE, "out", "test23_targets.json"), "w"), indent=1)
print("\nwrote out/test23_targets.json")
