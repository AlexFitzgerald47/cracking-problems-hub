#!/usr/bin/env python3
"""Frozen prediction P5, plus the occupancy diagnostic (E6) and the M288 form audit.

P5. If M288 is a *face-level* marker rather than a line-level one, the association
should be visible with the tablet-face as the unit: faces bearing M288 carry N45 more
often than faces that do not, compared within the same tablet (so the obverse is read
against its own reverse). Same exact conditional machinery, one level up.

E6 (exploratory). Within-face occupancy per M-sign, and how much of each published
pair's co-occurrence evidence is destroyed by conditioning at each rung.

Form audit (2026-09-17 recommended experiment 3, for M288). The published analysis
merges every graphic variant of M288 into one family. Are plain M288 and the variant
forms homogeneous with respect to N45?
"""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from blocks import CONFIRMED, fisher_exact_two_sided, hypergeom_probability, odds_ratio
from finer_blocks import load_fine

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "attempts/2026-09-17-exact-form-and-face"))
from face_and_form import exact_forms  # noqa: E402


class Unit:
    """A pseudo-line standing for a whole tablet-face."""
    __slots__ = ("tablet", "m_signs", "n_signs")

    def __init__(self, tablet, has_m, has_n, m, n):
        self.tablet = tablet
        self.m_signs = frozenset([m]) if has_m else frozenset()
        self.n_signs = frozenset([n]) if has_n else frozenset()


def exact_blocked(units, m, n, direction, key):
    blocks = defaultdict(list)
    for u in units:
        blocks[key(u)].append(u)
    dist = [1.0]; obs = mx = mn = inf = 0
    for bl in blocks.values():
        total = len(bl)
        s = sum(m in u.m_signs for u in bl)
        t = sum(n in u.n_signs for u in bl)
        obs += sum(m in u.m_signs and n in u.n_signs for u in bl)
        lo, hi = max(0, s - (total - t)), min(s, t)
        mx += hi; mn += lo
        inf += hi > lo
        local = [0.0] * (hi + 1)
        for k in range(lo, hi + 1):
            local[k] = hypergeom_probability(k, s, t, total)
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        comb[i + j] += pi * pj
        dist = comb
    p = sum(dist[obs:]) if direction == "enriched" else sum(dist[: obs + 1])
    floor = sum(dist[mx:]) if direction == "enriched" else sum(dist[: mn + 1])
    return {"p": min(1.0, p), "p_floor": min(1.0, floor), "blocks": len(blocks),
            "informative_blocks": inf, "observed": obs, "max_possible": mx,
            "has_power_at_05": min(1.0, floor) <= 0.05}


corpus = Path(sys.argv[1])
fine = load_fine(corpus)
el = [ln for ln in fine if not ln.damaged and ln.m_signs and ln.n_signs]
faces = defaultdict(list)
for ln in el:
    faces[(ln.tablet, ln.surface)].append(ln)

out = {}

# ---- P5: face as the unit of analysis, blocked on tablet -------------------
p5 = {}
for m, n, d in CONFIRMED:
    units = [Unit(tab, any(m in l.m_signs for l in bl), any(n in l.n_signs for l in bl), m, n)
             for (tab, _s), bl in faces.items()]
    r = exact_blocked(units, m, n, d, lambda u: u.tablet)
    a = sum(m in u.m_signs and n in u.n_signs for u in units)
    b = sum(m in u.m_signs and n not in u.n_signs for u in units)
    c = sum(m not in u.m_signs and n in u.n_signs for u in units)
    dd = sum(m not in u.m_signs and n not in u.n_signs for u in units)
    r["pooled_face_cells"] = [a, b, c, dd]
    r["pooled_face_or"] = odds_ratio(a, b, c, dd)
    p5[f"{m}-{n}"] = r
out["face_level_blocked_on_tablet"] = p5
print("P5 — unit = tablet-face, blocked on tablet (obverse read against its own reverse)")
print(f"{'pair':12} {'faces a/b/c/d':>22} {'faceOR':>8} {'infBlk':>7} {'floor':>10} {'p':>11} power")
for pair, r in p5.items():
    a, b, c, dd = r["pooled_face_cells"]
    print(f"{pair:12} {f'{a}/{b}/{c}/{dd}':>22} {r['pooled_face_or']:8.2f} "
          f"{r['informative_blocks']:7} {r['p_floor']:10.2e} {r['p']:11.3e} "
          f"{'YES' if r['has_power_at_05'] else 'no'}")

# ---- E6: occupancy ---------------------------------------------------------
occ = {}
signs = sorted({s for ln in el for s in ln.m_signs})
for m in signs:
    vals = [sum(m in l.m_signs for l in bl) / len(bl) for bl in faces.values()
            if any(m in l.m_signs for l in bl)]
    sat = sum(1 for bl in faces.values()
              if any(m in l.m_signs for l in bl)
              and all(m in l.m_signs for l in bl))
    if len(vals) >= 10:
        occ[m] = {"faces": len(vals), "mean_occupancy": sum(vals) / len(vals),
                  "saturated_faces": sat, "saturated_fraction": sat / len(vals),
                  "lines": sum(m in ln.m_signs for ln in el)}
out["occupancy"] = occ
carriers = sorted({m for m, _n, _d in CONFIRMED})
print("\nE6 — within-face occupancy of the constraint-carrying signs (exploratory)")
print(f"{'sign':6} {'lines':>6} {'faces':>6} {'meanOcc':>8} {'satFaces':>9} {'satFrac':>8}")
for m in carriers:
    r = occ[m]
    print(f"{m:6} {r['lines']:6} {r['faces']:6} {r['mean_occupancy']:8.3f} "
          f"{r['saturated_faces']:9} {r['saturated_fraction']:8.1%}")
rank = sorted(occ.items(), key=lambda kv: -kv[1]["saturated_fraction"])
print(f"   M288 saturation rank among {len(occ)} signs with >=10 faces: "
      f"{[k for k, _ in rank].index('M288') + 1}")
out["m288_saturation_rank"] = [k for k, _ in rank].index("M288") + 1
out["signs_ranked_by_saturation"] = [k for k, _ in rank][:10]

# ---- form audit for M288 ---------------------------------------------------
forms = Counter()
for ln in el:
    for f in exact_forms(ln.text, "M288"):
        forms[f] += 1
rows = {}
for f, cnt in forms.most_common():
    if cnt < 20:
        continue
    a = sum(1 for ln in el if f in exact_forms(ln.text, "M288") and "N45" in ln.n_signs)
    b = cnt - a
    rows[f] = {"lines": cnt, "with_N45": a, "rate": a / cnt}
keys = list(rows)
audit = {"form_counts": dict(forms.most_common()), "tested_forms": rows}
if len(keys) >= 2:
    f1, f2 = keys[0], keys[1]
    a, b = rows[f1]["with_N45"], rows[f1]["lines"] - rows[f1]["with_N45"]
    c, dd = rows[f2]["with_N45"], rows[f2]["lines"] - rows[f2]["with_N45"]
    audit["homogeneity"] = {"forms": [f1, f2], "cells": [a, b, c, dd],
                            "fisher_p": fisher_exact_two_sided(a, b, c, dd),
                            "odds_ratio": odds_ratio(a, b, c, dd)}
out["m288_form_audit"] = audit
print("\nM288 exact-form audit (2026-09-17 recommended experiment 3)")
for f, r in rows.items():
    print(f"   {f:18} lines={r['lines']:5}  with N45={r['with_N45']:4}  rate={r['rate']:.3f}")
if "homogeneity" in audit:
    h = audit["homogeneity"]
    print(f"   homogeneity {h['forms'][0]} vs {h['forms'][1]}: "
          f"Fisher p={h['fisher_p']:.4f}, OR={h['odds_ratio']:.2f}")

Path("results").mkdir(exist_ok=True)
Path("results/level_of_analysis.json").write_text(json.dumps(out, indent=2) + "\n")
