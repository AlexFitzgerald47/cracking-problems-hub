#!/usr/bin/env python3
"""F1: the too-flat / index-of-coincidence test inherited from the 2026-09-24 handover.

Computes the p-floor and uses a SIMULATED null, not the analytic chi-square tail,
because with 45 categories and 241 tokens the expected count per cell is 5.36 and
the asymptotics are marginal.

Conclusion is stated as P(data | uniform) only, per the validation panel's same-day
correction to the gold-bar rule: a chi-square against uniform does not measure
P(data | cipher).
"""
import csv, os, json, random
from collections import Counter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(20260925)

rows = list(csv.DictReader(open(os.path.join(HERE, "data", "phaistos_words.csv"))))
signs = [int(x) for r in rows for x in r["signs"].split("-") if int(x) != 0]
N, K = len(signs), 45
freq = Counter(signs)
counts = [freq.get(s, 0) for s in range(1, K + 1)]
exp = N / K

def chi2(c, e):
    return sum((x - e) ** 2 / e for x in c)

def ic(c, n):
    # index of coincidence, normalised so that a uniform source over K gives ~1.0
    num = sum(x * (x - 1) for x in c)
    return (num / (n * (n - 1))) * K

obs_chi2 = chi2(counts, exp)
obs_ic = ic(counts, N)

# --- simulated null: N tokens drawn uniformly over K categories -------------
B = 200000
null_chi2, null_ic = [], []
for _ in range(B):
    c = [0] * K
    for _ in range(N):
        c[random.randrange(K)] += 1
    null_chi2.append(chi2(c, exp))
    null_ic.append(ic(c, N))
null_chi2.sort()

ge = sum(1 for v in null_chi2 if v >= obs_chi2)
le = sum(1 for v in null_chi2 if v <= obs_chi2)
p_upper = (ge + 1) / (B + 1)
p_lower = (le + 1) / (B + 1)
p_floor = 1.0 / (B + 1)

mean_null = sum(null_chi2) / B
lo, hi = null_chi2[int(0.025 * B)], null_chi2[int(0.975 * B)]

out = []
out.append("Phaistos Disc, F1 flatness / IC test")
out.append("N = %d legible sign tokens over K = %d signs; expected count/cell = %.3f" % (N, K, exp))
out.append("")
out.append("p-floor of this simulation (B = %d draws): p >= %.2e; no smaller p is reportable" % (B, p_floor))
out.append("chi-square asymptotics: expected/cell 5.36, marginal -> simulated null used, not analytic tail")
out.append("")
out.append("observed chi2 vs uniform      = %.3f  (df = %d)" % (obs_chi2, K - 1))
out.append("simulated uniform null: mean %.2f, 95%% range [%.2f, %.2f]" % (mean_null, lo, hi))
out.append("  P(chi2 >= observed | uniform) = %.5f" % p_upper)
out.append("  P(chi2 <= observed | uniform) = %.5f" % p_lower)
out.append("")
out.append("observed IC (normalised, uniform = 1.0) = %.4f" % obs_ic)
out.append("null IC: mean %.4f, 95%% range [%.4f, %.4f]" %
           (sum(null_ic)/B, sorted(null_ic)[int(0.025*B)], sorted(null_ic)[int(0.975*B)]))
out.append("")
out.append("most frequent signs: %s" % freq.most_common(8))
out.append("top sign 02 occurs %d times against a uniform expectation of %.2f (%.2fx)" %
           (freq[2], exp, freq[2]/exp))
out.append("hapaxes: %d; signs occurring <= 2 times: %d of %d" %
           (sum(1 for c in counts if c == 1), sum(1 for c in counts if c <= 2), K))
out.append("")
verdict = ("NOT too flat" if p_upper < 0.05 else
           ("TOO FLAT" if p_lower < 0.05 else "indistinguishable from uniform"))
out.append("VERDICT: %s." % verdict)
out.append("Stated at the only strength this statistic carries: this is P(data | uniform),")
out.append("NOT P(data | cipher). It does not by itself identify the script or the language.")

txt = "\n".join(out)
print(txt)
open(os.path.join(HERE, "results", "flatness.txt"), "w").write(txt + "\n")
json.dump({"N": N, "K": K, "chi2": obs_chi2, "p_upper": p_upper, "p_lower": p_lower,
           "p_floor": p_floor, "ic": obs_ic, "null_chi2_mean": mean_null,
           "null_chi2_95": [lo, hi], "B": B},
          open(os.path.join(HERE, "results", "flatness.json"), "w"), indent=1)
