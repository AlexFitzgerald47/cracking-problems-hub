#!/usr/bin/env python3
"""Conditional sanity check for the new N≈/d/ onset hypothesis.

If the signature crib is C2B2 XP NU ZOO OM2N SHI =
HENE COS DE BOS NOS TYA, then the simplest reading of NU->DE is N≈D, U≈E.
Sektu independently identified 'initial consonant' as one of the two structural
possibilities for N, so this is a falsifiable value hypothesis rather than a
free remapping.

This script asks only whether the published N count is rate-compatible with a
French /d/ at plausible poetic line lengths.  It is not a language proof.
"""

FRENCH_FREQ_PCT = {
    "a": 7.636, "b": 0.901, "c": 3.260, "d": 3.669, "e": 14.715,
    "f": 1.066, "g": 0.866, "h": 0.737, "i": 7.529, "j": 0.613,
    "k": 0.049, "l": 5.456, "m": 2.968, "n": 7.095, "o": 5.796,
    "p": 2.521, "q": 1.362, "r": 6.693, "s": 7.948, "t": 7.244,
    "u": 6.311, "v": 1.838, "w": 0.074, "x": 0.427, "y": 0.128,
    "z": 0.326,
}

LINES = 20
N_REPORTED = 30
# Sensitivity branch: if the four frozen N.N terminal forms are independent
# pair-codepoints and were counted among the published N-family total, ordinary
# N falls to 26. This assumption must be verified against the raw transcription.
N_PAIR_SENSITIVITY = 26


def implied_letters_per_line(count: int, freq_pct: float) -> float:
    return count / LINES / (freq_pct / 100.0)


def main() -> None:
    print("Observed N-family rate:", N_REPORTED / LINES, "per line")
    print()
    print("If a single N corresponds roughly to one plaintext letter occurrence,")
    print("the average plaintext line length implied by each French letter is:")
    rows = []
    for letter, freq in FRENCH_FREQ_PCT.items():
        implied = implied_letters_per_line(N_REPORTED, freq)
        if 25 <= implied <= 60:
            rows.append((abs(implied - 40), letter, freq, implied))
    for _, letter, freq, implied in sorted(rows):
        print(f"  {letter}: freq={freq:5.3f}% -> {implied:5.1f} letters/line")
    print()
    d30 = implied_letters_per_line(N_REPORTED, FRENCH_FREQ_PCT["d"])
    d26 = implied_letters_per_line(N_PAIR_SENSITIVITY, FRENCH_FREQ_PCT["d"])
    e30 = implied_letters_per_line(N_REPORTED, FRENCH_FREQ_PCT["e"])
    print(f"N≈D, all 30 counted as ordinary N: {d30:.1f} letters/line")
    print(f"N≈D, sensitivity count 26:       {d26:.1f} letters/line")
    print(f"N≈E, all 30 counted as ordinary N: {e30:.1f} letters/line")
    print()
    print("Interpretation:")
    print("- D lies naturally in the 35-41 letters/line range under both N-count branches.")
    print("- This does not identify N by frequency: c/m/p also give plausible line lengths.")
    print("- What makes D special is the independent signature-derived NU->DE prediction")
    print("  plus Sektu's structural observation that N could be an initial consonant.")
    print("- The decisive test is cross-page: NU should recur where /de/ is plausible, and")
    print("  other N+vowel composites should behave like /dV/, not merely fit aggregate counts.")


if __name__ == "__main__":
    main()
