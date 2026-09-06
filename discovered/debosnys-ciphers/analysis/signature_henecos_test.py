#!/usr/bin/env python3
"""Test the Hênêcos / Debosnostya signature-crib hypothesis.

Evidence used before this test:
- Sektu independently labels the six-glyph sequence
    C2B2 XP NU ZOO OM2N SHI
  as a possible signature and gives the ordered subglyph decomposition.
- A different Debosnys page ends in a visible handwritten signature beginning
  Hênêcos Debo...
- A 2015 observer, independently of this proposed cipher alignment, read that
  surname as DE BOS NOS TYA.

The high-risk hypothesis tested here is therefore the WHOLE-GLYPH alignment

    C2B2 | XP  | NU | ZOO | OM2N | SHI
    HENE | COS | DE | BOS | NOS  | TYA

This script does *not* claim that each subglyph is a plaintext letter.  It
measures whether the repeated-subglyph structure is unusually compatible with
the candidate signature under a deliberately stricter atom->substring model.
Failure of that strict model does not falsify the whole-glyph hypothesis;
success is only a compatibility statistic, not a decryption proof.
"""

from __future__ import annotations
import random
from statistics import mean, median

ATOMS = ["C2", "B2", "X", "DOT", "N", "U", "O", "Z", "O", "O2RNO", "CROSSB"]

CANDIDATES = [
    "HENECOSDEBOSNOSTYA",   # independent 2015 reading of the visible signature
    "HENECOSDEBOSNOSTYS",   # final-letter ambiguity from the scan
    "HENECOSDEBOSNYS",      # conventional shortened surname
    "HENRYDEBOSNOSTYA",
    "HENRICUSDEBOSNOSTYA",
]

WHOLE_GLYPH_HYPOTHESIS = [
    ("C2B2", "HENE"),
    ("XP", "COS"),
    ("NU", "DE"),
    ("ZOO", "BOS"),
    ("OM2N", "NOS"),
    ("SHI", "TYA"),
]


def count_solutions(text: str, max_chunk: int = 2) -> int:
    """Count context-invariant atom->nonempty-substring assignments.

    Repeated atoms must emit the same substring. Component order is treated
    as plaintext order. This is intentionally stricter than the leading
    spatial/feature model.
    """
    mapping: dict[str, str] = {}
    count = 0

    def rec(i: int, pos: int) -> None:
        nonlocal count
        if i == len(ATOMS):
            count += int(pos == len(text))
            return

        atom = ATOMS[i]
        if atom in mapping:
            s = mapping[atom]
            if text.startswith(s, pos):
                rec(i + 1, pos + len(s))
            return

        for length in range(1, max_chunk + 1):
            if pos + length <= len(text):
                mapping[atom] = text[pos : pos + length]
                rec(i + 1, pos + length)
                del mapping[atom]

    rec(0, 0)
    return count


def permutation_null(text: str, trials: int = 10000, seed: int = 20260905):
    """Shuffle the same multiset of plaintext letters; preserve search budget."""
    rng = random.Random(seed)
    chars = list(text)
    observed = count_solutions(text, 2)
    null = []
    for _ in range(trials):
        rng.shuffle(chars)
        null.append(count_solutions("".join(chars), 2))
    p = (1 + sum(x >= observed for x in null)) / (trials + 1)
    return observed, mean(null), median(null), max(null), p


def main() -> None:
    print("WHOLE-GLYPH HYPOTHESIS")
    for glyph, chunk in WHOLE_GLYPH_HYPOTHESIS:
        print(f"  {glyph:6s} -> {chunk}")
    print()
    print("STRICT ATOM COMPATIBILITY (max emitted substring length 1..4)")
    for text in CANDIDATES:
        counts = [count_solutions(text, m) for m in (1, 2, 3, 4)]
        print(f"{text:24s} {counts}")
    print()
    print("MATCHED-BUDGET PERMUTATION NULL (max_chunk=2)")
    for text in CANDIDATES[:2]:
        obs, mu, med, mx, p = permutation_null(text)
        print(
            f"{text:24s} observed={obs:3d} null_mean={mu:.3f} "
            f"null_median={med:.1f} null_max={mx:3d} p={p:.6f}"
        )
    print()
    print("INTERPRETATION")
    print(
        "- The extended HENECOS DEBOSNOSTYA/S spelling is much more compatible "
        "with the repeated-atom pattern than HENECOS DEBOSNYS under the strict "
        "linear model."
    )
    print(
        "- The natural six-chunk alignment itself is non-concatenative at ZOO->BOS: "
        "the repeated O atoms cannot both emit ordinary nonempty substrings and "
        "concatenate to BOS. If the crib is right, at least some subglyphs must "
        "be spatial features/modifiers, not independent plaintext substrings."
    )
    print(
        "- Strong held-out predictions: XP should behave like COS; NU like DE; "
        "and the ZOO/OM2N pair should generalize as BOS/NOS on other pages."
    )


if __name__ == "__main__":
    main()
