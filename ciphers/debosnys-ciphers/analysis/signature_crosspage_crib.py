#!/usr/bin/env python3
"""Cross-page crib test for the six-glyph Debosnys 'signature' line.

The cipher line was transcribed by Sektu as:
    C2B2 XP NU ZOO OM2N SHI
and decomposed as:
    <C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>

A different primary page (cryptogram 4b) ends with an unencrypted stylized
signature that reads approximately 'Hênecos Debosnostys'. A contemporary
Cipher Mysteries commenter independently parsed the surname as 'DE BOS NOS
TYA'. This script asks a deliberately narrow question:

Does that externally observed signature fit the published six-glyph component
stream materially better than the shorter official-form guesses previously
tried, under a strict context-independent atom -> 1-or-2-character model?

This is NOT a solve. The strict atom model is probably too simple. The nulls
below are included to measure whether the fit is merely combinatorial.
"""

import random
from collections import Counter

ATOMS = ["C2", "B2", "X", "DOT", "N", "U", "O", "Z", "O", "O2RNO", "CROSSB"]
GLYPHS = [
    ["C2", "B2"],
    ["X", "DOT"],
    ["N", "U"],
    ["O", "Z", "O"],
    ["O2RNO"],
    ["CROSSB"],
]

CANDIDATES = [
    "HENECOSDEBOSNOSTYS",  # primary-image reading favored in this session
    "HENECOSDEBOSNOSTYA",  # 2015 commenter: DE BOS NOS TYA
    "HENECOSDEBOSNYS",     # shorter official-form spelling
    "HENRYDEBOSNYS",
    "JACOBPOMRIES",
]


def collect_solutions(text: str, max_chunk: int = 2):
    mapping = {}
    out = []

    def rec(i: int, pos: int):
        if i == len(ATOMS):
            if pos == len(text):
                out.append(dict(mapping))
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
    return out


def glyph_outputs(mapping):
    return ["".join(mapping[a] for a in glyph) for glyph in GLYPHS]


def count_boundary_aligned(text: str, boundary: int = 7) -> int:
    """Count strict solutions whose first two whole glyphs end at word break 7."""
    n = 0
    for mapping in collect_solutions(text, 2):
        outputs = glyph_outputs(mapping)
        if len(outputs[0] + outputs[1]) == boundary:
            n += 1
    return n


def random_iid(n: int, rng: random.Random) -> str:
    return "".join(rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(n))


def permuted(text: str, rng: random.Random) -> str:
    xs = list(text)
    rng.shuffle(xs)
    return "".join(xs)


def monte_carlo(target: str, trials: int = 50_000, seed: int = 20260905):
    target_solutions = len(collect_solutions(target, 2))
    target_boundary = count_boundary_aligned(target, 7)
    rng = random.Random(seed)

    iid_tail = iid_boundary_tail = 0
    perm_tail = perm_boundary_tail = 0

    for _ in range(trials):
        s = random_iid(len(target), rng)
        if len(collect_solutions(s, 2)) >= target_solutions:
            iid_tail += 1
        if count_boundary_aligned(s, 7) >= target_boundary:
            iid_boundary_tail += 1

    for _ in range(trials):
        s = permuted(target, rng)
        if len(collect_solutions(s, 2)) >= target_solutions:
            perm_tail += 1
        if count_boundary_aligned(s, 7) >= target_boundary:
            perm_boundary_tail += 1

    return {
        "target_solutions": target_solutions,
        "target_boundary_solutions": target_boundary,
        "iid_tail_p": iid_tail / trials,
        "iid_boundary_tail_p": iid_boundary_tail / trials,
        "permutation_tail_p": perm_tail / trials,
        "permutation_boundary_tail_p": perm_boundary_tail / trials,
        "trials": trials,
    }


def print_natural_whole_glyph_hypothesis():
    # The primary signature can be segmented into exactly six natural-looking
    # chunks, matching the number of cipher glyphs. This is a higher-level crib
    # hypothesis; it does not assume that subglyphs concatenate as letters.
    print("\nwhole-glyph leap hypothesis")
    print("C2B2 -> HENE")
    print("XP   -> COS")
    print("NU   -> DE")
    print("ZOO  -> BOS")
    print("OM2N -> NOS")
    print("SHI  -> TYS/TYA")
    print("combined: HENE|COS DE|BOS|NOS|TYS(A)")
    print("important: <O Z O> -> BOS cannot be a simple linear atom-letter")
    print("mapping with identical non-empty O at both ends; this favors")
    print("positional/feature/syllabic composition over concatenative atoms.")


if __name__ == "__main__":
    print("strict atom->1/2-character solution counts")
    for candidate in CANDIDATES:
        sols = collect_solutions(candidate, 2)
        boundary = count_boundary_aligned(candidate, 7) if len(candidate) >= 7 else 0
        print(f"{candidate:24s} len={len(candidate):2d} solutions={len(sols):3d} boundary7={boundary:3d}")

    target = "HENECOSDEBOSNOSTYS"
    stats = monte_carlo(target)
    print("\n50k matched-budget null tests for", target)
    for k, v in stats.items():
        print(f"{k} = {v}")

    print("\nrepresentative strict mappings (first 10)")
    for mapping in collect_solutions(target, 2)[:10]:
        print(glyph_outputs(mapping), mapping)

    print_natural_whole_glyph_hypothesis()
