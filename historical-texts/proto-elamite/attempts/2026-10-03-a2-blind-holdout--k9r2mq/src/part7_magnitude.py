"""Part 7: is the M288 family a corollary of Born et al. 2023's magnitude fact?

Born, Monroe, Kelley, Sarkar (CAWL 2023, s5) report that entries ending in M288
carry the LARGEST capacity magnitudes on average and M263 among the SMALLEST.
That is a rival explanation for this folder's whole M288 enrichment family
(N45, N39B, N24, N14) and for M263-N01, and it predates every session here.

Step 1 reproduces their descriptive finding with an assumption-light proxy.
IMPORTANT: this is NOT their measure. They first disambiguate each numeral into
one of the S/D/B/C systems with a bootstrap classifier and then compute capacity
magnitudes. I read raw ATF multipliers and sum them, which conflates systems. So
agreement is corroboration and disagreement is weak evidence of my own error,
not of theirs. Stated before running, in PREDICTIONS.md @ 9d2dba1.

Step 2 stratifies the association test by that magnitude proxy and asks whether
the M288 associations survive conditioning on line magnitude.

Predictions P7.1-P7.3 frozen in PREDICTIONS.md @ 9d2dba1.
"""
from __future__ import annotations
import json, re, statistics, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import mixed_lines_of, exact_blocked, conumeral, odds_ratio
from fastfold import bucket

TOKEN = re.compile(r'(\d+)\(([A-Za-z0-9~@]+)\)')
corpus = Path(sys.argv[1])
out = Path(__file__).resolve().parents[1] / "results"
el = mixed_lines_of(corpus)


def magnitude(ln):
    """Sum of raw numeral multipliers on the line. System-agnostic proxy."""
    return sum(int(m.group(1)) for m in TOKEN.finditer(ln.text))


for ln in el:
    object.__setattr__(ln, "_mag", magnitude(ln)) if hasattr(ln, "__dataclass_fields__") else None
mag = {id(ln): magnitude(ln) for ln in el}

# ---- Step 1: reproduce Born et al. s5 descriptively -------------------------
fams = {}
for ln in el:
    for s in ln.m_signs:
        fams.setdefault(s, []).append(mag[id(ln)])
elig = {s: v for s, v in fams.items() if len(v) >= 20}
ranked = sorted(elig.items(), key=lambda kv: -statistics.mean(kv[1]))
n = len(ranked)
pos = {s: i for i, (s, _) in enumerate(ranked)}
print(f"=== Step 1: mean raw numeral-multiplier sum per M family "
      f"({n} families with >=20 lines) ===")
print("  top 8 by mean magnitude:")
for s, v in ranked[:8]:
    print(f"    {s:8s} n={len(v):4d} mean={statistics.mean(v):8.2f} "
          f"median={statistics.median(v):6.1f}")
print("  bottom 8:")
for s, v in ranked[-8:]:
    print(f"    {s:8s} n={len(v):4d} mean={statistics.mean(v):8.2f} "
          f"median={statistics.median(v):6.1f}")
for s in ("M288", "M263", "M297", "M376", "M106"):
    if s in pos:
        v = elig[s]
        print(f"  {s}: rank {pos[s]+1} of {n} by mean magnitude "
              f"(percentile {100*(1-pos[s]/(n-1)):.0f}), mean={statistics.mean(v):.2f}")
p71 = pos.get("M288", 999) <= 0.10 * n and pos.get("M263", -1) >= 0.60 * n
print(f"\nP7.1 M288 among the largest and M263 among the smallest: "
      f"{'HELD' if p71 else 'FAILED'}")

# ---- Step 2: magnitude-stratified association test --------------------------
# Bins chosen on magnitude ALONE, before looking at any association.
BINS = [0, 1, 2, 3, 5, 8, 13, 21, 34, 10**9]
def mbin(ln):
    m = mag[id(ln)]
    for i, b in enumerate(BINS):
        if m <= b:
            return i
    return len(BINS)

blind = [ln for ln in el if bucket(ln.tablet) != 0]
TARGETS = [("M288", "N39B", "enriched"), ("M288", "N24", "enriched"),
           ("M288", "N14", "enriched"), ("M288", "N45", "enriched"),
           ("M263", "N01", "enriched"), ("M376", "N08A", "enriched"),
           ("M297", "N39B", "enriched")]
print(f"\n=== Step 2: magnitude-stratified exact test, blind buckets 1-4 "
      f"({len(blind)} lines), bins={BINS[:-1]}+ ===")
print(f"{'pair':11s} {'crude OR':>9s} {'MH OR':>8s} {'p':>11s} {'floor':>10s} "
      f"{'strata':>6s} {'verdict':>22s}")
rows = []
for m, t, d in TARGETS:
    a = sum(m in ln.m_signs and t in ln.n_signs for ln in blind)
    b = sum(m in ln.m_signs and t not in ln.n_signs for ln in blind)
    c = sum(m not in ln.m_signs and t in ln.n_signs for ln in blind)
    dd = len(blind) - a - b - c
    r = exact_blocked(blind, m, t, mbin, d)
    powered = r["floor"] <= 0.05
    passes = r["p"] <= 0.05 and powered
    verdict = ("SURVIVES" if passes else
               ("REFUSED (has power)" if powered else "no power"))
    rows.append({"pair": f"{m}-{t}", "crude_or": odds_ratio(a, b, c, dd),
                 "mag_mh_or": r["mh_or"], "mag_p": r["p"], "mag_floor": r["floor"],
                 "mag_strata": r["informative_blocks"], "verdict": verdict})
    print(f"{m}-{t:5s} {odds_ratio(a,b,c,dd):9.2f} {r['mh_or']:8.2f} {r['p']:11.4g} "
          f"{r['floor']:10.2g} {r['informative_blocks']:6d} {verdict:>22s}")

g = {r["pair"]: r for r in rows}
p72 = g["M288-N39B"]["verdict"] == "SURVIVES"
p73 = g["M263-N01"]["verdict"] != "SURVIVES"
print(f"\nP7.2 M288-N39B survives magnitude stratification: {'HELD' if p72 else 'FAILED'}")
print(f"P7.3 M263-N01 does not survive:                     {'HELD' if p73 else 'FAILED'} "
      f"({g['M263-N01']['verdict']})")

json.dump({"proxy": "sum of raw ATF numeral multipliers per line; NOT Born et al.'s "
                    "system-disambiguated capacity measure",
           "families_ge20": n,
           "rank_by_mean_magnitude": {s: pos[s] + 1 for s in
                                      ("M288", "M263", "M297", "M376", "M106") if s in pos},
           "mean_magnitude": {s: statistics.mean(elig[s]) for s in
                              ("M288", "M263", "M297", "M376", "M106") if s in elig},
           "top8": [[s, statistics.mean(v), len(v)] for s, v in ranked[:8]],
           "bottom8": [[s, statistics.mean(v), len(v)] for s, v in ranked[-8:]],
           "bins": BINS[:-1], "stratified": rows},
          open(out / "part7_magnitude.json", "w"), indent=1)
print("\nwrote results/part7_magnitude.json")
