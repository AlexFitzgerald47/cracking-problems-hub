#!/usr/bin/env python3
"""Falsification baseline for the six-glyph Debosnys 'signature-like' line.

Published Sektu component stream:
  <C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>

This deliberately tests a *strict* and simple model:
  1. each distinct component has one context-independent plaintext string;
  2. component order is plaintext order;
  3. every component emits a non-empty contiguous plaintext chunk unless
     the null-sensitivity test explicitly permits nulls;
  4. repeated O must emit the same plaintext chunk both times.

A zero result does not reject a candidate name in general. It rejects that
candidate under this simple linear-emission model and the published component
order. The purpose is to stop attractive cribs from being forced into the key.
"""

ATOMS = ["C2", "B2", "X", "DOT", "N", "U", "O", "Z", "O", "O2RNO", "CROSSB"]

# Candidate spellings/names previously raised in Debosnys research. HENECOS is
# included only because a plain handwritten 'Henecos' form is visible/discussed
# around the poem material; it is not asserted to be the ciphertext plaintext.
CANDIDATES = [
    "JACOBPOMRIES",
    "HENRYDEBOSNYS",
    "HENRYDELETNACKDEBOSNYS",
    "RAMPON",
    "LAUGRAN",
    "SOULA",
    "DELPECH",
    "ULTIME",
    "HENRICOSDEBOSNYS",
    "HENECOSDEBOSNYS",
]


def count_solutions(text: str, max_chunk: int = 4, max_nulls: int = 0) -> int:
    """Count consistent atom->substring assignments under the strict model."""
    mapping = {}
    null_atoms = set()
    count = 0

    def rec(i: int, pos: int, nulls_used: int) -> None:
        nonlocal count
        if i == len(ATOMS):
            if pos == len(text):
                count += 1
            return

        atom = ATOMS[i]
        if atom in mapping:
            s = mapping[atom]
            if text.startswith(s, pos):
                rec(i + 1, pos + len(s), nulls_used)
            return

        if atom in null_atoms:
            rec(i + 1, pos, nulls_used)
            return

        if nulls_used < max_nulls:
            null_atoms.add(atom)
            rec(i + 1, pos, nulls_used + 1)
            null_atoms.remove(atom)

        for length in range(1, max_chunk + 1):
            if pos + length <= len(text):
                mapping[atom] = text[pos : pos + length]
                rec(i + 1, pos + length, nulls_used)
                del mapping[atom]

    rec(0, 0, 0)
    return count


def collect_examples(text: str, max_chunk: int = 4, limit: int = 5):
    """Return a few zero-null mappings for diagnosing accidental fits."""
    mapping = {}
    out = []

    def rec(i: int, pos: int) -> None:
        if len(out) >= limit:
            return
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


if __name__ == "__main__":
    print("strict zero-null solution counts; columns=max chunk length 1,2,3,4")
    for candidate in CANDIDATES:
        counts = [count_solutions(candidate, m, 0) for m in (1, 2, 3, 4)]
        print(f"{candidate:28s} {counts}")

    print("\nnull sensitivity at max_chunk=4")
    for candidate in ["JACOBPOMRIES", "HENRYDEBOSNYS", "HENRYDELETNACKDEBOSNYS"]:
        one = count_solutions(candidate, 4, 1)
        two = count_solutions(candidate, 4, 2)
        print(f"{candidate:28s} one_null={one} two_nulls={two}")

    print("\nHENECOSDEBOSNYS accidental zero-null fits at max_chunk=4")
    for solution in collect_examples("HENECOSDEBOSNYS", 4):
        print(solution)

    print("\nInterpretation:")
    print("- No listed ordinary name/phrase fits when every component emits <=2 letters.")
    print("- HENECOSDEBOSNYS fits only when a single atom (Z) is allowed to emit 'DEBO' (4 letters).")
    print("- Permitting even one null produces many solutions, so null-enabled fits are not evidence.")
    print("- Therefore do not use this line as a naive one-atom/one-letter-or-digraph crib.")
