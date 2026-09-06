#!/usr/bin/env python3
"""Sensitivity of the Debosnys N/nasalization argument to paired N.N tokens.

Sektu reported 30 N-glyphs across 20 cipher-poem lines and compared that to
3182 Baudelaire Alexandrines containing 6536 nasalized vowels. The Hub's prior
`n_glyph_recheck.py` showed P(sum_20 <= 30) ~= 0.03444 under Sektu's empirical
per-line Baudelaire distribution.

Sektu also explicitly observed that N.N frequently occurs as a stand-alone glyph
and may be a different subglyph/codepoint from single N. Primary cryptogram-4
scans show the repeated terminal class on lines 1,2,17,18 as a stacked double-wave
form, strongly consistent with this N.N paired class.

This script asks a conditional question: if 0..4 of the 30 counted N-family tokens
should instead be excluded because they belong to an independent N.N codepoint,
how much weaker does the universal `single N = every French nasalization` model
become? This is a sensitivity analysis, not proof that all four were included in
Sektu's published count or that N.N has no nasal function.
"""

# Sektu's published Baudelaire distribution, with the 6-7 bucket split by the
# published total: 25 sixes + 7 sevens gives the required residual count.
BAUDELAIRE = {0: 366, 1: 816, 2: 897, 3: 658, 4: 312, 5: 101, 6: 25, 7: 7}
N_LINES = sum(BAUDELAIRE.values())
assert N_LINES == 3182
assert sum(k * v for k, v in BAUDELAIRE.items()) == 6536

line_p = {k: v / N_LINES for k, v in BAUDELAIRE.items()}

dp = {0: 1.0}
for _ in range(20):
    nxt = {}
    for total, prob in dp.items():
        for k, q in line_p.items():
            nxt[total + k] = nxt.get(total + k, 0.0) + prob * q
    dp = nxt

print("excluded_NN_family\tcomparable_single_N\tmean_per_line\tP_Baudelaire(sum_20<=count)")
for excluded in range(0, 5):
    comparable = 30 - excluded
    p_lower = sum(prob for total, prob in dp.items() if total <= comparable)
    print(f"{excluded}\t{comparable}\t{comparable / 20:.2f}\t{p_lower:.9f}")

print("\nInterpretation")
print("0 excluded reproduces the prior <=30 result (~0.034436).")
print("If four known rhyme-terminal N.N tokens are independent codepoints and were counted in the 30,")
print("the comparable single-N count falls to 26 and the lower-tail probability to ~0.005298.")
print("Thus paired-form parsing is not cosmetic: it materially affects phonological model scoring.")
