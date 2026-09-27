#!/usr/bin/env python3
"""Extract zodiac (and control) label sets from the Takahashi transcription."""
import os, sys, json
import vmsparse

ZODIAC_FOLIOS = ["f70v1", "f70v2", "f71r", "f71v", "f72r1", "f72r2", "f72r3",
                 "f72v1", "f72v2", "f72v3", "f73r", "f73v"]

DEFAULT_SRC = os.environ.get(
    "VMS_TAKAHASHI",
    "/tmp/claude-0/-home-user-cracking-problems-hub/634aa923-677e-5dc9-9564-f7bc199c0972/scratchpad/voynich/analysis/takahashi_original.txt")


def load(path=None):
    return vmsparse.parse(path or DEFAULT_SRC)


def zodiac_rings(rows):
    """Return {(folio, ring): [ (idx, [words]), ... ] } in transcription order."""
    out = {}
    for r in rows:
        if r["folio"] in ZODIAC_FOLIOS and r["ltype"] == "S":
            key = (r["folio"], r["lnum"])
            out.setdefault(key, []).append((r["line"], r["words"]))
    for k in out:
        out[k].sort()
    return out


def ring_strings(rows, joiner=""):
    """Ring -> ordered list of label strings (multi-word labels concatenated)."""
    rings = zodiac_rings(rows)
    return {k: [joiner.join(w) for _, w in v] for k, v in rings.items()}


def ring_first_words(rows):
    rings = zodiac_rings(rows)
    return {k: [w[0] if w else "" for _, w in v] for k, v in rings.items()}


if __name__ == "__main__":
    rows = load()
    rs = ring_strings(rows)
    tot = 0
    for k in sorted(rs):
        print(k, len(rs[k]), rs[k])
        tot += len(rs[k])
    print("total labels:", tot)
