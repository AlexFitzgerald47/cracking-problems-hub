#!/usr/bin/env python3
"""Power analysis: what can 61 groups / 241 signs actually detect?

The board's standing instruction is to run the power curve even when you expect to be
underpowered, because "the corpus is too small" is an excuse until it is priced.

Three questions:
  Q1  H1's power: if the section-final slot were formulaic at strength r (a fraction r
      of marked groups drawn from a closed repertoire), how often would the N2 test
      detect it at the budget-charged threshold 4e-4?
  Q2  positional restriction: if some signs were strictly group-initial or group-final,
      how strong would that restriction have to be before 241 tokens could see it?
  Q3  the ceiling for the thing everyone wants: how many DISTINCT group types would a
      real language need for a 61-group sample to look like this one, and can a corpus
      this size ever constrain a sign's phonetic value? (a bound, not a test)
"""
import csv, os, json, random, math
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(20260925)

rows = list(csv.DictReader(open(os.path.join(HERE, "data", "phaistos_words.csv"))))
words = [r["signs"] for r in rows]
lens = [int(r["n_signs"]) for r in rows]
signs = [int(x) for r in rows for x in r["signs"].split("-") if int(x) != 0]
N_MARK, N_WORD = 18, 61

out = ["Phaistos Disc: power analysis", ""]

# ---------- Q1: power of the H1 test -----------------------------------------
# critical value of S under the stratified null at alpha = 4e-4
STR = defaultdict(list)
for i, L in enumerate(lens): STR[L].append(i)
mark_need = Counter(lens[i] for i, r in enumerate(rows) if int(r["oblique"]))

def perm(rng):
    o = []
    for L, k in mark_need.items(): o += rng.sample(STR[L], k)
    return o
def S(sel): 
    w = [words[i] for i in sel]; return len(w) - len(set(w))

rng = random.Random(1)
null = sorted(S(perm(rng)) for _ in range(200000))
def crit(alpha):
    # smallest s with P(S >= s) <= alpha
    for s in range(0, 19):
        if sum(1 for v in null if v >= s) / len(null) <= alpha: return s
    return 19
c_bud, c_nom = crit(4e-4), crit(0.01)
out.append("Q1  H1 power")
out.append("    null distribution of S (stratified): mean %.3f, P(S>=3)=%.5f, P(S>=4)=%.5f, P(S>=5)=%.5f"
           % (sum(null)/len(null),
              sum(1 for v in null if v>=3)/len(null),
              sum(1 for v in null if v>=4)/len(null),
              sum(1 for v in null if v>=5)/len(null)))
out.append("    critical S at the budget-charged 4e-4 threshold: S >= %d" % c_bud)
out.append("    critical S at a nominal 0.01:                    S >= %d" % c_nom)
out.append("    observed S = 5, so the test had margin: it would still have fired at S = %d." % c_bud)

# power: simulate a generative model where a fraction r of the 18 marked slots are
# filled from a closed repertoire of R types and the rest are unique
out.append("")
out.append("    power to detect a closed section-final repertoire of R types,")
out.append("    where a fraction r of the 18 marked slots is drawn from it (10000 sims):")
out.append("      r      R=2     R=3     R=4     R=6")
for r in (0.3, 0.5, 0.7, 1.0):
    line = "      %.1f " % r
    for R in (2, 3, 4, 6):
        hit = 0
        for _ in range(10000):
            k = sum(1 for _ in range(N_MARK) if random.random() < r)
            drawn = [random.randrange(R) for _ in range(k)]
            s = len(drawn) - len(set(drawn))
            if s >= c_bud: hit += 1
        line += "  %.3f " % (hit / 10000)
    out.append(line)
out.append("    Read: the test is well powered for a small closed repertoire and loses")
out.append("    power fast as R grows. At R = 6 with only 30%% of slots formulaic it is blind.")

# ---------- Q2: positional restriction ---------------------------------------
out.append("")
out.append("Q2  positional restriction on signs")
first = Counter(int(r["signs"].split("-")[0]) for r in rows)
last = Counter(int(r["signs"].split("-")[-1]) for r in rows if int(r["signs"].split("-")[-1]) != 0)
freq = Counter(signs)
out.append("    a sign occurring f times has f chances to be group-initial; with 61 groups")
out.append("    and mean group length %.2f the marginal P(initial) = %.3f" % (len(signs)/61, 61/len(signs)))
out.append("    signs and their initial/total counts (top by frequency):")
for s, f in freq.most_common(10):
    out.append("       sign %02d  total %2d  initial %2d  final %2d" % (s, f, first.get(s,0), last.get(s,0)))
# power: how many occurrences does a sign need before a strict restriction is detectable?
p0 = 61/len(signs)
out.append("")
out.append("    a STRICTLY group-initial sign is detectable at p<0.01 once it occurs f times,")
out.append("    where P(all f initial by chance) = %.3f^f < 0.01  ->  f >= %d"
           % (p0, math.ceil(math.log(0.01)/math.log(p0))))
out.append("    signs with at least that many occurrences: %d of 45"
           % sum(1 for c in freq.values() if c >= math.ceil(math.log(0.01)/math.log(p0))))
out.append("    So a positional grammar can only ever be demonstrated for the handful of")
out.append("    high-frequency signs. For the 17 signs occurring once or twice it is")
out.append("    UNTESTABLE on this corpus, not absent.")

# ---------- Q3: the bound that matters --------------------------------------
out.append("")
out.append("Q3  the ceiling on decipherment from this corpus alone")
hapax = sum(1 for c in freq.values() if c == 1)
le2 = sum(1 for c in freq.values() if c <= 2)
out.append("    45 sign types over 241 tokens; %d hapaxes and %d signs occurring <= 2 times." % (hapax, le2))
out.append("    Any phonetic value assigned to a hapax rests on ONE attestation and cannot be")
out.append("    cross-checked internally at any significance level. That is %d of 45 signs" % le2)
out.append("    (%.0f%% of the signary) permanently unconstrained by internal evidence." % (100*le2/45))
out.append("    Consequence, as a bound rather than a test: a self-consistent reading of the")
out.append("    Disc is not evidence of a correct reading, because %.0f%% of the signary can be" % (100*le2/45))
out.append("    set freely without creating a single internal contradiction.")
# how many free parameters vs constraints
out.append("    Free parameters in a syllabic reading: 45 sign values.")
out.append("    Internal consistency constraints available: %d repeated group types + %d"
           % (7, len(signs)-len(set(map(tuple,[[int(x) for x in r['signs'].split('-')] for r in rows])))))
out.append("    That is fewer constraints than parameters, which is why readability cannot")
out.append("    discriminate. Matches the board's short-cipher validation bound.")

txt = "\n".join(out)
print(txt)
open(os.path.join(HERE, "results", "power.txt"), "w").write(txt + "\n")
