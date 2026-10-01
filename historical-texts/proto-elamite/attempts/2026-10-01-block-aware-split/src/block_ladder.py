#!/usr/bin/env python3
"""The block ladder: tablet -> face -> column -> accounting entry.

For each published pair and each rung, report the exact conditional p, the p-floor,
how many blocks are informative, and how much of the pair's co-occurrence evidence
survives the conditioning at all. A pair that holds all the way down to the entry is
associated at the tightest spatial grain the corpus records; a pair whose floor rises
above 0.05 on a rung is untestable there, which is not the same as refuted.
"""
import json, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from blocks import CONFIRMED, hypergeom_probability
from finer_blocks import check_against_audited, load_fine

RUNGS = [
    ("tablet", lambda ln: (ln.tablet,)),
    ("face", lambda ln: (ln.tablet, ln.surface)),
    ("column", lambda ln: (ln.tablet, ln.surface, ln.column)),
    ("entry", lambda ln: (ln.tablet, ln.surface, ln.column, ln.entry)),
]


def test(lines, m, n, direction, key):
    blocks = defaultdict(list)
    for ln in lines:
        blocks[key(ln)].append(ln)
    dist = [1.0]
    obs = mx = mn = inf = 0
    forced_cooc = 0
    for bl in blocks.values():
        total = len(bl)
        s = sum(m in ln.m_signs for ln in bl)
        t = sum(n in ln.n_signs for ln in bl)
        o = sum(m in ln.m_signs and n in ln.n_signs for ln in bl)
        obs += o
        lo, hi = max(0, s - (total - t)), min(s, t)
        mx += hi; mn += lo
        if hi > lo:
            inf += 1
        else:
            forced_cooc += o
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
            "informative_blocks": inf, "observed_overlap": obs,
            "max_possible_overlap": mx, "min_possible_overlap": mn,
            "cooccurrences_in_forced_blocks": forced_cooc,
            "expected_under_null": sum(i * v for i, v in enumerate(dist)),
            "has_power_at_05": min(1.0, floor) <= 0.05}


corpus = Path(sys.argv[1])
check_against_audited(corpus)
fine = load_fine(corpus)
el = [ln for ln in fine if not ln.damaged and ln.m_signs and ln.n_signs]

out = {"eligible_lines": len(el), "rungs": [r[0] for r in RUNGS], "pairs": {}}
hdr = f"{'pair':12} {'rung':8} {'blocks':>7} {'infBlk':>7} {'obs/max':>9} {'forcedCo':>9} {'floor':>10} {'p':>11}  power"
print(hdr)
for m, n, d in CONFIRMED:
    out["pairs"][f"{m}-{n}"] = {"direction": d}
    co = sum(m in ln.m_signs and n in ln.n_signs for ln in el)
    out["pairs"][f"{m}-{n}"]["cooccurrences_total"] = co
    for name, key in RUNGS:
        r = test(el, m, n, d, key)
        out["pairs"][f"{m}-{n}"][name] = r
        print(f"{m+'-'+n:12} {name:8} {r['blocks']:7} {r['informative_blocks']:7} "
              f"{str(r['observed_overlap'])+'/'+str(r['max_possible_overlap']):>9} "
              f"{str(r['cooccurrences_in_forced_blocks'])+'/'+str(co):>9} "
              f"{r['p_floor']:10.2e} {r['p']:11.3e}  {'YES' if r['has_power_at_05'] else 'no'}")
    print()
Path("results").mkdir(exist_ok=True)
Path("results/block_ladder.json").write_text(json.dumps(out, indent=2) + "\n")
