#!/usr/bin/env python3
"""Conservative structural branch enumerator for the Ennis amber bead.

This deliberately does NOT assign values to the anomalous signs or pretend that
reversing direction is just string reversal. It enumerates only alternatives
explicitly retained by the Dec-2023 / Jan-2024 OG(H)AM examination.
"""

from itertools import product

CORES = ("DMVA", "DMLO")
FORK_EXITS = {
    "right": "VA",   # right-hand branch as described by OG(H)AM
    "left": "?",     # anomalous left-hand branch; value intentionally unknown
}
DETACHED_PREFIX = "?"  # detached < shape, not a known ogham character
DIRECTIONS = ("upward", "opposite")


def upward_serialisations():
    """Return only physically explicit path serialisations in the proposed upward orientation."""
    for core, (path, tail) in product(CORES, FORK_EXITS.items()):
        yield {
            "core": core,
            "fork_path": path,
            "serialisation": f"{DETACHED_PREFIX}{core}{tail}",
        }


def structural_case_lower_bound() -> int:
    """Lower bound before anomalous-sign values or extra segmentations are introduced."""
    return len(CORES) * len(FORK_EXITS) * len(DIRECTIONS)


if __name__ == "__main__":
    print("Upward-orientation path serialisations:")
    for row in upward_serialisations():
        print(f"  {row['fork_path']:>5} | {row['core']} | {row['serialisation']}")
    print(f"\nStructural-case lower bound including direction: {structural_case_lower_bound()}")
    print("Note: opposite-direction ogham values must be recomputed from stroke geometry; do not simply reverse these strings.")
