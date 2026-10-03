#!/usr/bin/env python3
"""Blocking finer than the face: column, and the accounting entry itself.

The 2026-09-17 session blocked on (tablet, face) because the obverse carries itemised
entries and the reverse carries totals. The corpus has two finer spatial units the
folder has never used:

  * `@column` -- the audited parser deliberately keeps the physical face across column
    tags, which was the right fix for the header analysis but leaves columns untested
    as a confound here.
  * the **entry** -- ATF labels such as `2.A.` and `2.B.` are two sub-lines of one
    numbered accounting entry. On P008020 every entry is an M391 sub-line carrying
    N01 and an M288 sub-line carrying N45/N14. Blocking on the entry asks the sharpest
    possible version of the question: inside a single accounting entry, does the
    M-sign sub-line take the N-sign?

This parser adds column and entry identity. It is checked line-for-line against the
audited 2026-09-04 parser: same count, same order, same m_signs, same n_signs.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from blocks import load_corpus  # noqa: E402
_ANALYSIS = Path(__file__).resolve().parents[3] / "analysis"
sys.path.insert(0, str(_ANALYSIS))
from structure_associations import (  # noqa: E402
    DAMAGE_RE, FACE_TAGS, LINE_RE, M_SIGN_RE, N_SIGN_RE, normalize_n_sign,
)


@dataclass(frozen=True)
class FineLine:
    tablet: str
    surface: str
    column: str
    entry: str
    text: str
    m_signs: frozenset
    n_signs: frozenset
    damaged: bool


def parse_fine(path: Path) -> list[FineLine]:
    tablet = path.name.split(".", 1)[0]
    surface, column = "unspecified", "0"
    out: list[FineLine] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw.startswith("&"):
            m = re.match(r"&([A-Z][0-9]+)", raw)
            if m:
                tablet = m.group(1)
            continue
        if raw.startswith("@"):
            parts = raw[1:].strip().split()
            tag = parts[0].lower()
            if tag in FACE_TAGS:
                surface, column = tag, "0"
            elif tag == "column":
                column = parts[1] if len(parts) > 1 else "?"
            continue
        m = LINE_RE.match(raw)
        if not m:
            continue
        label, text = m.groups()
        numeric = text.split(",", 1)[1] if "," in text else text
        out.append(FineLine(
            tablet=tablet, surface=surface, column=column, entry=label, text=text,
            m_signs=frozenset(M_SIGN_RE.findall(text)),
            n_signs=frozenset(normalize_n_sign(v) for v in N_SIGN_RE.findall(numeric)),
            damaged=bool(DAMAGE_RE.search(text)),
        ))
    return out


def load_fine(corpus_dir: Path) -> list[FineLine]:
    out = []
    for path in sorted(Path(corpus_dir).glob("*.values.atf")):
        out.extend(parse_fine(path))
    return out


def check_against_audited(corpus_dir: Path) -> None:
    """Fail loudly if the fine parser disagrees with the audited one on any line."""
    base, _ = load_corpus(corpus_dir)
    fine = load_fine(corpus_dir)
    assert len(base) == len(fine), f"line count {len(base)} vs {len(fine)}"
    for a, b in zip(base, fine):
        assert (a.tablet, a.surface, a.text, a.m_signs, a.n_signs, a.damaged) == \
               (b.tablet, b.surface, b.text, b.m_signs, b.n_signs, b.damaged), \
               f"line mismatch at {a.tablet} {a.label}: {a.text!r} vs {b.text!r}"


if __name__ == "__main__":
    check_against_audited(Path(sys.argv[1]))
    print("fine parser agrees with the audited 2026-09-04 parser on every line")
