#!/usr/bin/env python3
"""Early RIC keyword cipher reconstructed from Liam Archer, BMH WS 819.

Archer describes a 26-letter alphabet split into two 13-letter rows. The top row
starts with the deduplicated keyword, then the earliest unused alphabet letters are
appended until 13 symbols are present. The remaining 13 letters form the lower row.
Each letter substitutes with the letter directly opposite it, making the mapping an
involution: the same transform encrypts and decrypts.

This module intentionally implements only that documented early RIC system. Do not
apply it to military Playfair, later RIC double-key traffic, or numerical/figure
ciphers without first classifying the message family.
"""

from __future__ import annotations

import argparse
import string
from dataclasses import dataclass

ALPHABET = string.ascii_uppercase


@dataclass(frozen=True)
class RICKey:
    keyword: str
    top: str
    bottom: str

    @property
    def mapping(self) -> dict[str, str]:
        return dict(zip(self.top + self.bottom, self.bottom + self.top))


def normalize_keyword(keyword: str) -> str:
    """Uppercase and deduplicate A-Z letters while preserving first occurrence."""
    seen: set[str] = set()
    out: list[str] = []
    for ch in keyword.upper():
        if ch in ALPHABET and ch not in seen:
            seen.add(ch)
            out.append(ch)
    if not out:
        raise ValueError("keyword must contain at least one A-Z letter")
    if len(out) > 13:
        raise ValueError("deduplicated keyword is longer than the 13-letter row")
    return "".join(out)


def build_key(keyword: str) -> RICKey:
    """Construct the paired 13-letter rows described in BMH WS 819."""
    kw = normalize_keyword(keyword)
    remaining = [ch for ch in ALPHABET if ch not in kw]
    top = kw + "".join(remaining[: 13 - len(kw)])
    bottom = "".join(ch for ch in ALPHABET if ch not in top)
    assert len(top) == len(bottom) == 13
    assert set(top + bottom) == set(ALPHABET)
    return RICKey(keyword=kw, top=top, bottom=bottom)


def transform(text: str, keyword: str, *, preserve_nonletters: bool = True) -> str:
    """Encrypt or decrypt text: the historical mapping is self-inverse."""
    mapping = build_key(keyword).mapping
    out: list[str] = []
    for ch in text:
        up = ch.upper()
        if up in mapping:
            repl = mapping[up]
            out.append(repl if ch.isupper() else repl.lower())
        elif preserve_nonletters:
            out.append(ch)
    return "".join(out)


def strip_dead_prefix(text: str, n: int = 3) -> str:
    """Remove the documented RIC dead-letter prefix from alphabetic ciphertext."""
    removed = 0
    out: list[str] = []
    for ch in text:
        if ch.upper() in ALPHABET and removed < n:
            removed += 1
            continue
        out.append(ch)
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="RIC paired-alphabet keyword cipher (BMH WS 819)")
    parser.add_argument("keyword")
    parser.add_argument("text")
    parser.add_argument("--strip-dead-prefix", action="store_true", help="drop first 3 alphabetic ciphertext characters")
    parser.add_argument("--show-key", action="store_true")
    args = parser.parse_args()

    key = build_key(args.keyword)
    if args.show_key:
        print(key.top)
        print(key.bottom)
    text = strip_dead_prefix(args.text) if args.strip_dead_prefix else args.text
    print(transform(text, args.keyword))


if __name__ == "__main__":
    main()
