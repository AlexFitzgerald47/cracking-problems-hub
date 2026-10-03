"""Can the tier A2 pairs be given the blind-holdout warrant tier A1 has?

ux87d8 section 6 established that the donor split and the plain hash holdout are
complementary: the donor split suits SPARSE pairs whose informative blocks a
random split would destroy, and eats the screening set of DENSE ones.  The A2
pairs are dense, so the published 80/20 hash holdout should retain informative
blocks on BOTH sides -- which is exactly the warrant A2 lacks.  This reports the
power available, as marginals only, so the next session knows before it runs."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from recon_common import (load_eligible, exact_blocked, crude_cells,
                          odds_ratio, fisher_exact_two_sided, split_name)

A2 = [("M288", "N39B", "enriched"), ("M376", "N08A", "enriched"),
      ("M288", "N14", "enriched"), ("M288", "N24", "enriched"),
      ("M362", "N14", "enriched"), ("M370", "N39B", "depleted")]

corpus = Path(sys.argv[1])
_, _, el = load_eligible(corpus)
tr = [l for l in el if split_name(l.tablet) == "train"]
va = [l for l in el if split_name(l.tablet) == "validation"]
face = lambda l: (l.tablet, l.surface)
conum = lambda t: (lambda l: frozenset(l.n_signs - {t}))

rows = []
for m, t, d in A2:
    a, b, c, dd = crude_cells(tr, m, t)
    f = exact_blocked(va, m, t, face, d)
    cn = exact_blocked(va, m, t, conum(t), d)
    promotable = f["floor"] <= 0.05 and cn["floor"] <= 0.05
    rows.append({"pair": f"{m}-{t}", "direction": d,
                 "train_or": odds_ratio(a, b, c, dd),
                 "train_fisher_p": fisher_exact_two_sided(a, b, c, dd),
                 "val_face_informative_blocks": f["informative_blocks"],
                 "val_face_floor": f["floor"],
                 "val_conumeral_informative_strata": cn["informative_blocks"],
                 "val_conumeral_floor": cn["floor"],
                 "promotable_on_plain_holdout": promotable})
    print(f"{m}-{t:6s} trainOR={odds_ratio(a,b,c,dd):7.2f} "
          f"| face: infB={f['informative_blocks']:3d} floor={f['floor']:.2g} "
          f"| conum: infS={cn['informative_blocks']:3d} floor={cn['floor']:.2g} "
          f"| {'PROMOTABLE' if promotable else 'no power on this holdout'}")

Path("results/a2_holdout_power.json").write_text(json.dumps(rows, indent=2))
n = sum(r["promotable_on_plain_holdout"] for r in rows)
print(f"\n{n} of {len(rows)} tier A2 pairs can be given a blind-holdout warrant "
      f"on the published 80/20 split.")
print("wrote results/a2_holdout_power.json")
