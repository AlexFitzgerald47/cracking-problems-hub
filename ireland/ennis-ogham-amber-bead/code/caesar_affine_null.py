#!/usr/bin/env python3
"""Matched-budget null tests for the Ennis bead `DMVAVA -> STINGING` candidate.

Requires optional local packages for the two reference lexicons used in the session:
    pip install cmudict textblob

The script:
  * tokenizes words into the 20 ordinary-ogham positions, with V sharing Fern/F;
  * allows NG either as one ogham sign or as N + G;
  * counts Caesar-orbit reachability for random six-sign ciphertexts;
  * enumerates all 20 Caesar shifts of DMVAVA and comparison branches;
  * enumerates all 160 invertible affine maps modulo 20.

No language score or manual word choice is used: membership is exact after lowercasing.
"""

from __future__ import annotations

from math import gcd
from typing import Iterable, Iterator, Sequence

ALPHABET = ("b", "l", "f", "s", "n", "h", "d", "t", "c", "q",
            "m", "g", "ng", "z", "r", "a", "o", "u", "e", "i")
IDX = {s: i for i, s in enumerate(ALPHABET)}
N = len(ALPHABET)


def normalize_letters(word: str) -> str | None:
    """Normalize an English headword to letters representable by core ogham.

    V shares the epigraphic F/Fern position. K/Q-like modern distinctions are not
    invented; q is accepted because it is an ordinary ogham sign, while letters
    outside the twenty-sign inventory are rejected.
    """
    w = word.strip().lower()
    if not w.isalpha():
        return None
    w = w.replace("v", "f")
    allowed = set("blfsnhdtcqmgzraouei")
    if any(ch not in allowed for ch in w):
        return None
    return w


def tokenizations(word: str) -> Iterator[tuple[str, ...]]:
    """Yield all segmentations using NG either as one sign or as N,G."""
    w = normalize_letters(word)
    if w is None:
        return

    def rec(pos: int, out: list[str]) -> Iterator[tuple[str, ...]]:
        if pos == len(w):
            yield tuple(out)
            return
        if w.startswith("ng", pos):
            out.append("ng")
            yield from rec(pos + 2, out)
            out.pop()
        ch = w[pos]
        if ch in IDX:
            out.append(ch)
            yield from rec(pos + 1, out)
            out.pop()

    yield from rec(0, [])


def to_indices(tokens: Sequence[str]) -> tuple[int, ...]:
    return tuple(IDX[t] for t in tokens)


def render(indices: Sequence[int]) -> str:
    return "".join(ALPHABET[i % N] for i in indices)


def caesar(seq: Sequence[int], shift: int) -> tuple[int, ...]:
    return tuple((x + shift) % N for x in seq)


def affine(seq: Sequence[int], a: int, b: int) -> tuple[int, ...]:
    return tuple((a * x + b) % N for x in seq)


def canonical_caesar_orbit(seq: Sequence[int]) -> tuple[int, ...]:
    return min(caesar(seq, k) for k in range(N))


def load_cmudict_words() -> set[str]:
    import cmudict  # type: ignore
    return {w.lower() for w in cmudict.words() if w.isalpha()}


def load_textblob_words() -> set[str]:
    from textblob.en import spelling  # type: ignore
    return {str(w).lower() for w in spelling.keys() if str(w).isalpha()}


def six_token_sequences(words: Iterable[str]) -> tuple[set[tuple[int, ...]], dict[tuple[int, ...], set[str]]]:
    seqs: set[tuple[int, ...]] = set()
    owners: dict[tuple[int, ...], set[str]] = {}
    for word in words:
        for tok in tokenizations(word):
            if len(tok) != 6:
                continue
            s = to_indices(tok)
            seqs.add(s)
            owners.setdefault(s, set()).add(word.lower())
    return seqs, owners


def caesar_orbit_count(seqs: Iterable[tuple[int, ...]]) -> int:
    return len({canonical_caesar_orbit(s) for s in seqs})


def words_reachable_from(seq: Sequence[int], owners: dict[tuple[int, ...], set[str]]) -> list[tuple[str, int]]:
    hits: list[tuple[str, int]] = []
    for k in range(N):
        out = caesar(seq, k)
        for w in sorted(owners.get(out, ())):
            hits.append((w, k))
    return hits


def affine_hits(seq: Sequence[int], owners: dict[tuple[int, ...], set[str]]) -> list[tuple[str, int, int]]:
    hits: list[tuple[str, int, int]] = []
    for a in range(N):
        if gcd(a, N) != 1:
            continue
        for b in range(N):
            out = affine(seq, a, b)
            for w in sorted(owners.get(out, ())):
                hits.append((w, a, b))
    return hits


def main() -> None:
    branches = {
        "DMVAVA": ("d", "m", "f", "a", "f", "a"),
        "DMLOVA": ("d", "m", "l", "o", "f", "a"),
        "ATATML": ("a", "t", "a", "t", "m", "l"),
        "ATODML": ("a", "t", "o", "d", "m", "l"),
    }
    branch_indices = {k: to_indices(v) for k, v in branches.items()}

    print("Canonical ordinary-ogham order:", " ".join(ALPHABET))
    print("\nAll Caesar shifts of DMVAVA:")
    for k in range(N):
        print(f"{k:+3d}: {render(caesar(branch_indices['DMVAVA'], k))}")

    for name, loader in (("CMUdict", load_cmudict_words), ("TextBlob", load_textblob_words)):
        words = loader()
        seqs, owners = six_token_sequences(words)
        orbits = caesar_orbit_count(seqs)
        p = orbits / (N ** 5)
        print(f"\n{name}")
        print("eligible six-token sequences:", len(seqs))
        print("distinct Caesar orbits:", orbits)
        print("random Caesar-family reachability:", p, f"({100*p:.6f}%)")
        for label, seq in branch_indices.items():
            print(label, "Caesar hits:", words_reachable_from(seq, owners))
        print("DMVAVA affine hits:", affine_hits(branch_indices["DMVAVA"], owners))


if __name__ == "__main__":
    main()
