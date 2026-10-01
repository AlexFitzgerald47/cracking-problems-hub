#!/usr/bin/env python3
"""The expanded constraint set, with every column an attacker would ask for.

For each pair clearing the corpus-wide face-blocked sweep: the exact p, BH and
Benjamini-Yekutieli q over the powered space, the p-floor, how many informative
(tablet, face) blocks carry it, **how many distinct tablets those blocks come from**
(the entry-level result in this session's RESULTS.md collapsed to one tablet, so
replicate count is a required column, not a nicety), and a tautology check: whether
the N-sign ever appears inside the entry field of a line carrying the M-sign, which
is the failure the 2026-09-04 session caught with M036+1(N30D).
"""
import csv, json, math, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from blocks import CONFIRMED
from finer_blocks import load_fine
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "analysis"))
from structure_associations import N_SIGN_RE, normalize_n_sign  # noqa: E402

corpus = Path(sys.argv[1])
rows = json.loads(Path("results/search_budget.json").read_text())["rows"]
fine = load_fine(corpus)
el = [ln for ln in fine if not ln.damaged and ln.m_signs and ln.n_signs]
by_face = defaultdict(list)
for ln in el:
    by_face[(ln.tablet, ln.surface)].append(ln)

published = {(m, n) for m, n, _ in CONFIRMED}
powered = [r for r in rows if r["p_floor"] <= 0.05]
# Benjamini-Yekutieli: BH q scaled by the harmonic number of the test count.
harmonic = sum(1.0 / i for i in range(1, len(powered) + 1))

sel = [r for r in powered if r["p"] <= 1e-4]
out = []
for r in sel:
    m, n = r["m"], r["n"]
    tablets = set()
    inf = 0
    for (tab, _s), bl in by_face.items():
        total = len(bl)
        s = sum(m in ln.m_signs for ln in bl)
        t = sum(n in ln.n_signs for ln in bl)
        if min(s, t) > max(0, s - (total - t)):
            inf += 1
            tablets.add(tab)
    bound = sum(1 for ln in el if m in ln.m_signs
                and n in {normalize_n_sign(v)
                          for v in N_SIGN_RE.findall(ln.text.split(",", 1)[0] if "," in ln.text else "")})
    a, b, c, d = r["pooled_cells"]
    out.append({
        "m_sign": m, "n_sign": n, "direction": r["direction"],
        "status": "published 2026-09-04" if (m, n) in published else "new 2026-10-01",
        "pooled_a": a, "pooled_b": b, "pooled_c": c, "pooled_d": d,
        "pooled_odds_ratio": round(r["pooled_or"], 4),
        "face_blocked_p": r["p"],
        "bh_q_powered_space": r["q_over_powered_space"],
        "by_q_powered_space": min(1.0, r["q_over_powered_space"] * harmonic),
        "p_floor": r["p_floor"],
        "informative_face_blocks": inf,
        "distinct_tablets_supplying_them": len(tablets),
        "n_sign_inside_entry_field_on_m_lines": bound,
    })
out.sort(key=lambda r: r["face_blocked_p"])

Path("results").mkdir(exist_ok=True)
with open("results/constraint_table.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0]))
    w.writeheader(); w.writerows(out)
Path("results/constraint_table.json").write_text(json.dumps(
    {"powered_tests": len(powered), "by_harmonic_factor": harmonic,
     "threshold": 1e-4, "rows": out}, indent=2) + "\n")

print(f"powered tests = {len(powered)}; Benjamini-Yekutieli factor = {harmonic:.2f}\n")
print(f"{'pair':12} {'dir':9} {'status':22} {'OR':>7} {'p':>11} {'BH q':>10} {'BY q':>10} {'infBlk':>7} {'tablets':>8} {'bound':>6}")
for r in out:
    print(f"{r['m_sign']+'-'+r['n_sign']:12} {r['direction']:9} {r['status']:22} "
          f"{r['pooled_odds_ratio']:7.2f} {r['face_blocked_p']:11.3e} "
          f"{r['bh_q_powered_space']:10.2e} {r['by_q_powered_space']:10.2e} "
          f"{r['informative_face_blocks']:7} {r['distinct_tablets_supplying_them']:8} "
          f"{r['n_sign_inside_entry_field_on_m_lines']:6}")
npub = sum(1 for r in out if r["status"].startswith("published"))
print(f"\n{len(out)} pairs at p <= 1e-4: {npub} of the published eight, {len(out)-npub} new to this folder")
weak = [r for r in out if r["distinct_tablets_supplying_them"] < 3]
print(f"pairs resting on fewer than 3 distinct tablets (treat as single-object): "
      f"{[r['m_sign']+'-'+r['n_sign'] for r in weak] or 'none'}")
