#!/usr/bin/env python3
"""Positional grammar: are any signs restricted to group-initial or group-final slots?

This was NOT the hypothesis I set out to test (see FREEZE.md); it fell out of the Q2
power calculation.  It is therefore exploratory and is charged a full 45-sign x 2-position
search budget = 90 tests, Bonferroni threshold 0.01/90 = 1.11e-4.

Null: permute the 241 legible sign tokens across the 242 sign SLOTS, holding the group
boundaries and group lengths fixed.  This preserves sign frequencies and the group-length
distribution exactly and destroys only the sign-to-position assignment -- one thing.
"""
import csv, os, json, random, math
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(20260925)
B = 200000
BUDGET = 90
THRESH = 0.01 / BUDGET

rows = list(csv.DictReader(open(os.path.join(HERE, "data", "phaistos_words.csv"))))
groups = [[int(x) for x in r["signs"].split("-")] for r in rows]
lens = [len(g) for g in groups]
flat = [s for g in groups for s in g]
legible = [s for s in flat if s != 0]
freq = Counter(legible)
NPOS = len(flat)

def positions(gs):
    """-> (initial counter, final counter, medial counter)"""
    ini, fin, med = Counter(), Counter(), Counter()
    for g in gs:
        for j, s in enumerate(g):
            if s == 0: continue
            if j == 0: ini[s] += 1
            elif j == len(g) - 1: fin[s] += 1
            else: med[s] += 1
    return ini, fin, med

def regroup(seq):
    out, k = [], 0
    for L in lens:
        out.append(seq[k:k + L]); k += L
    return out

obs_i, obs_f, obs_m = positions(groups)

# marginal expectations under the null
p_ini = 61 / NPOS
p_fin = 61 / NPOS

# ---- permutation null -------------------------------------------------------
pool = list(flat)
ge_i = Counter(); ge_f = Counter(); le_i = Counter()
for _ in range(B):
    random.shuffle(pool)
    ni, nf, _ = positions(regroup(pool))
    for s in freq:
        if ni[s] >= obs_i.get(s, 0): ge_i[s] += 1
        if nf[s] >= obs_f.get(s, 0): ge_f[s] += 1
        if ni[s] <= obs_i.get(s, 0): le_i[s] += 1

out = ["Phaistos Disc: positional grammar of the signary", ""]
out.append("241 legible tokens in 61 groups (242 slots incl. the illegible one).")
out.append("Marginal P(a token is group-initial) = 61/242 = %.4f" % p_ini)
out.append("Null: permute tokens across slots, group lengths fixed. B = %d, p-floor %.2e" % (B, 1/(B+1)))
out.append("Search budget charged: 45 signs x 2 positions = %d tests, threshold %.2e" % (BUDGET, THRESH))
out.append("")
out.append("sign  total  init  final  med   P(init>=obs)  P(init<=obs)  P(final>=obs)   verdict")
hits = []
for s, f in freq.most_common():
    if f < 4:   # below the detectability floor computed in power.py
        continue
    pi = (ge_i[s] + 1) / (B + 1)
    pl = (le_i[s] + 1) / (B + 1)
    pf = (ge_f[s] + 1) / (B + 1)
    v = []
    if pi < THRESH: v.append("INITIAL-RESTRICTED")
    if pl < THRESH: v.append("INITIAL-AVOIDING")
    if pf < THRESH: v.append("FINAL-PREFERRING")
    if v: hits.append((s, f, obs_i.get(s,0), obs_f.get(s,0), pi, pl, pf, ";".join(v)))
    out.append("  %02d    %3d   %3d   %3d   %3d   %10.6f   %10.6f   %10.6f   %s"
               % (s, f, obs_i.get(s,0), obs_f.get(s,0), obs_m.get(s,0), pi, pl, pf, ";".join(v)))

out.append("")
out.append("--- signs clearing the budget-charged threshold %.2e ---" % THRESH)
for s, f, i, fi, pi, pl, pf, v in hits:
    out.append("  sign %02d: %d occurrences, %d initial, %d final -> %s" % (s, f, i, fi, v))
if not hits:
    out.append("  none")

# ---- the 02-12 pair ---------------------------------------------------------
out.append("")
out.append("--- the 02 / 12 pair ---")
n02 = freq[2]; n12 = freq[12]
pair = sum(1 for g in groups for j in range(len(g)-1) if g[j]==2 and g[j+1]==12)
out.append("sign 02 occurs %d times, group-initial %d/%d; sign 12 occurs %d times, group-initial %d/%d"
           % (n02, obs_i.get(2,0), n02, n12, obs_i.get(12,0), n12))
out.append("the bigram 02-12 occurs %d times; it is group-initial in all of them: %s"
           % (pair, all(g[0]==2 and len(g)>1 and g[1]==12
                        for g in groups if len(g)>1 and g[0]==2 and g[1]==12)))
# bigram null
cnt = 0
for _ in range(B):
    random.shuffle(pool)
    gs = regroup(pool)
    c = sum(1 for g in gs for j in range(len(g)-1) if g[j]==2 and g[j+1]==12)
    if c >= pair: cnt += 1
out.append("P(02-12 bigram count >= %d | slot permutation) = %.6f" % (pair, (cnt+1)/(B+1)))
out.append("analytic sanity check: P(one sign strictly initial in all %d occurrences) = %.4f^%d = %.3e"
           % (n02, p_ini, n02, p_ini**n02))

txt = "\n".join(out)
print(txt)
open(os.path.join(HERE, "results", "position.txt"), "w").write(txt + "\n")
json.dump({"budget": BUDGET, "threshold": THRESH,
           "hits": [{"sign": s, "n": f, "init": i, "fin": fi, "p_init_ge": pi,
                     "p_init_le": pl, "p_fin_ge": pf, "verdict": v}
                    for s, f, i, fi, pi, pl, pf, v in hits],
           "pair_02_12": pair},
          open(os.path.join(HERE, "results", "position.json"), "w"), indent=1)
