"""Holdout test (FREEZE_HOLDOUT.md): Pelling's original 2011-key transcription
of other Blitz pages, against the same nulls and the same @470 calibration.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import fastnull

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_holdout(path, drop_excluded=True):
    paras, cur = {}, None
    for l in open(path):
        l = l.rstrip("\n")
        if l.startswith("#") or not l.strip():
            continue
        if l.startswith("="):
            cur = l[1:]; paras[cur] = []; continue
        paras[cur].append(list(l.strip()))
    if drop_excluded:
        paras = {k: v for k, v in paras.items() if "EXCLUDED" not in k}
    return paras


paras = load_holdout(os.path.join(HERE, "data", "holdout_2011key.txt"))
lines = [l for k in sorted(paras, key=lambda s: int(s[1:])) for l in paras[k]]
r = fastnull.run(lines, nperm=20000, seed=7)
b, d = r["bigram"], r["doublet"]
print(f"HOLDOUT (2011 key, P3 excluded): n={r['n_tokens']} types={r['n_types']}")
print(f"  bigram IC obs={b['obs']:.5f} exp={b['mean']:.5f} z={b['z']:+.2f} p={b['p_upper']:.5f}")
print(f"  doublets  obs={d['obs']:.0f} exp={d['mean']:.1f} z={d['z']:+.2f} "
      f"p_lower={d['p_lower']:.4f}")

cal = json.load(open(os.path.join(HERE, "out", "calibration.json")))
for key in ("copiale@470", "borg@470"):
    bz = sorted(cal["ref"][key]["bigram_z"])
    dz = sorted(cal["ref"][key]["doublet_z"])
    print(f"  vs {key}: genuine blocks with bigram z <= holdout: "
          f"{sum(1 for z in bz if z <= b['z'])}/{len(bz)}; "
          f"with doublet z >= holdout: {sum(1 for z in dz if z >= d['z'])}/{len(dz)}")

print("\n  VERDICT ON FROZEN PREDICTIONS")
print(f"  H1 (z>0, p<0.05):            {'PASS' if b['z']>0 and b['p_upper']<0.05 else 'FAIL'}")
print(f"  H2 (z < +9.18, in [3,9]):    "
      f"{'PASS' if b['z']<9.18 else 'FAIL'}"
      f"  (point range [3,9]: {'in' if 3<=b['z']<=9 else 'OUT'})")
print(f"  H3 (doublet z > -2.0):       {'PASS' if d['z']>-2.0 else 'FAIL'}")

# also run WITH the excluded paragraph, to show what excluding it did
allp = load_holdout(os.path.join(HERE, "data", "holdout_2011key.txt"), drop_excluded=False)
al = [l for k in sorted(allp, key=lambda s: int(s[1:3].rstrip('-'))) for l in allp[k]]
r2 = fastnull.run(al, nperm=20000, seed=7)
print(f"\n  [diagnostic] holdout INCLUDING the key-order paragraph: n={r2['n_tokens']} "
      f"bigram z={r2['bigram']['z']:+.2f} doublet z={r2['doublet']['z']:+.2f}")

json.dump({"holdout": r, "holdout_with_keyorder_para": r2},
          open(os.path.join(HERE, "out", "holdout.json"), "w"), indent=1)
print("\nwrote out/holdout.json")
