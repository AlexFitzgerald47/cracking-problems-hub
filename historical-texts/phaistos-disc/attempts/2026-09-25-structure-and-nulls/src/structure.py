#!/usr/bin/env python3
"""H1: is the oblique-marked (section-final) slot formulaic?

Statistic S = (marked tokens) - (distinct marked types) = duplicate excess in the
marked set.  Null: permute WHICH words carry the oblique stroke, holding the word
sequence and the word multiset fixed.  Exactly one thing permuted.

N1  free permutation of the 18 labels over 61 words
N2  permutation stratified by group length  <- the one that counts (short groups
    repeat more easily by chance, and marked groups are slightly shorter)
N3  as N2 but with A24 dropped from the marked set (its oblique is a crack)

Failure condition fixed in FREEZE.md: p > 0.01 under N2 means H1 is not established.
Search budget charged there: 25 combinations, so p < 0.0004 clears the budget.
"""
import csv, os, json, random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(20260925)
B = 200000

rows = list(csv.DictReader(open(os.path.join(HERE, "data", "phaistos_words.csv"))))
for r in rows:
    r["oblique"] = int(r["oblique"]); r["n_signs"] = int(r["n_signs"])
words = [r["signs"] for r in rows]
marks = [r["oblique"] for r in rows]
lens = [r["n_signs"] for r in rows]
ids = [r["word_id"] for r in rows]

def S(sel):
    """duplicate excess among the selected words"""
    w = [words[i] for i in sel]
    return len(w) - len(set(w))

def perm_free(sel_idx, rng):
    return rng.sample(range(len(words)), len(sel_idx))

def strata():
    d = defaultdict(list)
    for i, L in enumerate(lens):
        d[L].append(i)
    return d

STR = strata()

def perm_strat(sel_idx, rng):
    """resample, within each length stratum, as many indices as sel_idx has there"""
    need = Counter(lens[i] for i in sel_idx)
    out = []
    for L, k in need.items():
        out += rng.sample(STR[L], k)
    return out

def run(sel_idx, permfn, label, out):
    obs = S(sel_idx)
    rng = random.Random(20260925)
    null = [S(permfn(sel_idx, rng)) for _ in range(B)]
    ge = sum(1 for v in null if v >= obs)
    p = (ge + 1) / (B + 1)
    mean = sum(null) / B
    ns = sorted(null)
    out.append("%s: n_marked=%d  observed S=%d  null mean %.3f  null 95%% max %d  p=%.6f%s"
               % (label, len(sel_idx), obs, mean, ns[int(0.95 * B)], p,
                  "  (at p-floor %.1e)" % (1/(B+1)) if ge == 0 else ""))
    return obs, p, mean

out = []
marked = [i for i, m in enumerate(marks) if m]
unmarked = [i for i, m in enumerate(marks) if not m]

# ---- descriptive -----------------------------------------------------------
wc = Counter(words)
rep_types = {w: c for w, c in wc.items() if c > 1}
out.append("Phaistos Disc, H1: is the section-final slot formulaic?")
out.append("")
out.append("61 groups, %d distinct; %d group types occur more than once:" % (len(wc), len(rep_types)))
for w, c in sorted(rep_types.items(), key=lambda kv: -kv[1]):
    where = [(ids[i], "marked" if marks[i] else "plain") for i, x in enumerate(words) if x == w]
    out.append("   %-24s x%d  %s" % (w, c, where))
out.append("")
out.append("marked set   : %d tokens, %d distinct, duplicate excess S = %d, redundancy %.1f%%"
           % (len(marked), len({words[i] for i in marked}), S(marked),
              100 * S(marked) / len(marked)))
out.append("unmarked set : %d tokens, %d distinct, duplicate excess S = %d, redundancy %.1f%%"
           % (len(unmarked), len({words[i] for i in unmarked}), S(unmarked),
              100 * S(unmarked) / len(unmarked)))
out.append("mean group length: marked %.2f, unmarked %.2f"
           % (sum(lens[i] for i in marked)/len(marked),
              sum(lens[i] for i in unmarked)/len(unmarked)))
straddle = sum(1 for w in rep_types
               if len({marks[i] for i, x in enumerate(words) if x == w}) > 1)
out.append("repeated group types straddling the marked/unmarked boundary: %d of %d"
           % (straddle, len(rep_types)))
out.append("")

# ---- tests -----------------------------------------------------------------
out.append("--- permutation tests (B = %d) ---" % B)
run(marked, perm_free, "N1 free label permutation          ", out)
o2, p2, _ = run(marked, perm_strat, "N2 length-stratified permutation    ", out)
marked_noA24 = [i for i in marked if ids[i] != "A24"]
o3, p3, _ = run(marked_noA24, perm_strat, "N3 stratified, A24 crack removed   ", out)

# ---- the same test on the label I did NOT pick, as a control ---------------
out.append("")
out.append("--- controls: the same statistic on other labels of the same size ---")
for lbl, sel in (("side A (31 words)", [i for i in range(61) if rows[i]["side"] == "A"]),
                 ("section-INITIAL words", None)):
    if sel is None:
        sel, nxt = [], True
        for i in range(61):
            if nxt: sel.append(i)
            nxt = bool(marks[i])
    run(sel, perm_strat, "   %-28s" % lbl, out)

out.append("")
out.append("--- verdict ---")
out.append("Failure condition from FREEZE.md: p > 0.01 under N2 means H1 not established.")
out.append("Search-budget threshold from FREEZE.md (25 combinations): p < 0.0004 to clear.")
if p2 > 0.01:
    v = "H1 NOT ESTABLISHED (N2 p = %.6f)" % p2
elif p2 < 0.0004:
    v = "H1 SURVIVES the budget-charged threshold (N2 p = %.6f < 0.0004)" % p2
else:
    v = "H1 SUGGESTIVE BUT NOT ESTABLISHED: clears 0.01 (p=%.6f) but not the 25-way budget" % p2
out.append("VERDICT: " + v)

txt = "\n".join(out)
print(txt)
open(os.path.join(HERE, "results", "structure.txt"), "w").write(txt + "\n")
json.dump({"S_marked": S(marked), "S_unmarked": S(unmarked), "p_N2": p2, "p_N3": p3,
           "straddling_types": straddle, "n_rep_types": len(rep_types), "B": B},
          open(os.path.join(HERE, "results", "structure.json"), "w"), indent=1)
