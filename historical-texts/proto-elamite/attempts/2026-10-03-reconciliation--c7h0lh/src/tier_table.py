"""The one tier table, with its basis declared in the table.

Every number is computed in this session (src/conumeral.py,
src/newcore_conumeral.py, src/verify_convergent.py) except the columns marked
as quoted from another session, which are labelled with that session's id."""
from __future__ import annotations
import csv, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from recon_common import load_eligible, exact_blocked, crude_cells, odds_ratio

corpus = Path(sys.argv[1])
_, _, eligible = load_eligible(corpus)
face = lambda l: (l.tablet, l.surface)

pub = {r["pair"]: r for r in json.loads(Path("results/conumeral.json").read_text())}
new = {r["pair"]: r for r in json.loads(Path("results/newcore_conumeral.json").read_text())}

# ux87d8's (tablet, face, other-N-count capped at 3) scheme, quoted from its
# RESULTS.md section 4 -- the independent second implementation of the control.
UX = {"M297-N39B": (0.0000, 7.0e-18), "M106-N24": (0.0000, 2.7e-13),
      "M263-N30C": (0.0017, 1.7e-3), "M288-N45": (0.0110, 4.0e-4),
      "M297-N24": (0.2959, 1.4e-14), "M297-N01": (0.5602, 2.0e-5),
      "M263-N01": (0.4696, 8.7e-4), "M243-N39B": (0.5648, 3.7e-2)}

rows = []
for pair, r in list(pub.items()) + list(new.items()):
    m, t = pair.split("-")
    d = r["direction"]
    warrant = ("screened+validated (2026-09-04 design)" if pair in pub
               else f"corrected search, {r['sweeps']}/4 sweeps")
    fb = exact_blocked(eligible, m, t, face, d)
    ux = UX.get(pair)
    rows.append({
        "pair": pair, "direction": d, "warrant": warrant,
        "crude_or": round(r["crude_or"], 2),
        "face_blocked_p_fullcorpus": f"{fb['p']:.3g}",
        "face_blocked_floor": f"{fb['floor']:.2g}",
        "conumeral_mh_or": round(r["mh_or"] if "mh_or" in r else r["conumeral_mh_or"], 2),
        "conumeral_p": f"{(r.get('p') or r['conumeral_p']):.3g}",
        "conumeral_floor": f"{(r.get('floor') or r['conumeral_floor']):.2g}",
        "conumeral_q": f"{(r.get('q_bh8') or r['conumeral_q']):.3g}",
        "conumeral_basis": "BH over the 8 published" if pair in pub else "BH over the 11 new-core",
        "richness_blocked_p_ux87d8": "" if not ux else f"{ux[0]:.4g}",
        "richness_blocked_floor_ux87d8": "" if not ux else f"{ux[1]:.2g}",
        "verdict": r["verdict"],
    })

order = {"SURVIVES": 0, "UNTESTABLE (no power)": 1, "FAILS (with power)": 2}
rows.sort(key=lambda x: (order[x["verdict"]], float(x["conumeral_q"])))
with open("results/tier_table.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

print(f"{'pair':11s} {'warrant':34s} {'MH-OR':>7s} {'conum q':>9s} {'ux87d8 p':>9s}  verdict")
for r in rows:
    print(f"{r['pair']:11s} {r['warrant']:34s} {r['conumeral_mh_or']:7.2f} "
          f"{r['conumeral_q']:>9s} {r['richness_blocked_p_ux87d8'] or '-':>9s}  {r['verdict']}")
agree = [r for r in rows if r["richness_blocked_p_ux87d8"]]
same = sum(1 for r in agree
           if (r["verdict"] == "SURVIVES") == (float(r["richness_blocked_p_ux87d8"]) <= 0.05))
print(f"\ntwo independent composition controls agree on {same}/{len(agree)} of the published eight")
print("wrote results/tier_table.csv")
