#!/usr/bin/env python3
"""Recheck Sektu's 2017 N-glyph / French-nasalization comparison.

Inputs are the counts printed in Sektu's 2017-08-07 post.  No cipher
transcription is assumed here; this file only audits the published summary
statistics and computes exact small-sample probabilities under the stated
Baudelaire null model.
"""

from math import factorial

# Sektu: 3182 Alexandrine lines from Fleurs du Mal, 6536 nasalized vowels.
# The 6-7 bucket contains 32 lines.  The published total forces those 32 to
# comprise 25 sixes and 7 sevens: 25*6 + 7*7 = 199 residual nasal vowels.
baudelaire = {0: 366, 1: 816, 2: 897, 3: 658, 4: 312, 5: 101, 6: 25, 7: 7}
N_BAUD = sum(baudelaire.values())
assert N_BAUD == 3182
assert sum(k * v for k, v in baudelaire.items()) == 6536

# Sektu prints: 20 cipher-poem lines, 30 N-glyphs total, but then gives a
# histogram totaling only 19 lines: 0:2, 1:6, 2:9, 3:2.  Those 19 lines
# already account for all 30 N-glyphs, so the missing twentieth line must
# contain zero N-glyphs if the printed totals are both correct.
reported = {0: 2, 1: 6, 2: 9, 3: 2}
assert sum(reported.values()) == 19
assert sum(k * v for k, v in reported.items()) == 30
corrected = dict(reported)
corrected[0] += 1
assert sum(corrected.values()) == 20
assert sum(k * v for k, v in corrected.items()) == 30

# Collapse Baudelaire into 0,1,2,3,4+ to match the observed support.
p = [
    baudelaire[0] / N_BAUD,
    baudelaire[1] / N_BAUD,
    baudelaire[2] / N_BAUD,
    baudelaire[3] / N_BAUD,
    sum(v for k, v in baudelaire.items() if k >= 4) / N_BAUD,
]
obs = [corrected[0], corrected[1], corrected[2], corrected[3], 0]
n = sum(obs)
expected = [n * x for x in p]
pearson = sum((o - e) ** 2 / e for o, e in zip(obs, expected))

# Exact multinomial tail probability for Pearson statistic >= observed.
def multinomial_prob(xs):
    coeff = factorial(n)
    for x in xs:
        coeff //= factorial(x)
    out = float(coeff)
    for x, q in zip(xs, p):
        out *= q ** x
    return out

p_tail = 0.0
for a in range(n + 1):
    for b in range(n - a + 1):
        for c in range(n - a - b + 1):
            for d in range(n - a - b - c + 1):
                e = n - a - b - c - d
                xs = [a, b, c, d, e]
                stat = sum((o - ex) ** 2 / ex for o, ex in zip(xs, expected))
                if stat >= pearson - 1e-12:
                    p_tail += multinomial_prob(xs)

# Exact probability that 20 independent Baudelaire lines contain <=30 nasal
# vowels (i.e. mean <=1.5), using the empirical 0..7 distribution.
line_p = {k: v / N_BAUD for k, v in baudelaire.items()}
dp = {0: 1.0}
for _ in range(20):
    nxt = {}
    for total, prob in dp.items():
        for k, q in line_p.items():
            nxt[total + k] = nxt.get(total + k, 0.0) + prob * q
    dp = nxt
p_sum_le_30 = sum(prob for total, prob in dp.items() if total <= 30)

print("reported_histogram =", reported)
print("corrected_histogram =", corrected)
print("cipher_mean_N =", 30 / 20)
print("baudelaire_mean_nasal =", 6536 / 3182)
print("pearson_collapsed =", round(pearson, 6))
print("exact_multinomial_tail_p =", round(p_tail, 6))
print("P_Baudelaire(sum_20 <= 30) =", round(p_sum_le_30, 6))
