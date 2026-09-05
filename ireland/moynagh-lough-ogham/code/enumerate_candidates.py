#!/usr/bin/env python3
"""
Enumerate the serious Moynagh Lough I-MEA-003 reading branches.

This is deliberately small and explicit. The point is not to manufacture a
large search space; it is to ensure that orientation, correction/phase,
damaged-sign, and side-order assumptions are visible and costed.

Run:
    python code/enumerate_candidates.py > analysis/candidates.csv
"""
import csv
import sys
from itertools import product

SIDE1 = [
    ("COLORRS", "forward_full", 0.0, "published preferred full reading"),
    ("COLORS", "forward_correction_collapsed", 1.0,
     "one adjacent R treated as correction/improvement"),
    ("COLOR", "forward_first_carving_phase", 1.0,
     "last two finer-cut letters treated as later phase"),
    ("CRRODOS", "reverse_full", 1.0,
     "published reverse; spacing argues against"),
    ("CRODOS", "reverse_correction_collapsed", 2.0,
     "reverse plus one adjacent R treated as correction"),
]

SIDE2 = [
    ("PIBANSNAVQE", "P_final_E", 0.0, "published preferred P reading"),
    ("PIBANSNAVQI", "P_final_I", 1.0, "damaged final sign read I"),
    ("IBANSNAVQE", "initial_marker_final_E", 1.0,
     "initial sign treated as start marker, not phonetic"),
    ("IBANSNAVQI", "initial_marker_final_I", 2.0,
     "initial marker plus damaged final I"),
    ("KIBANSNAVQE", "X_forfid_K_final_E", 2.0,
     "initial sign treated as X-forfid K; placement atypical"),
    ("KIBANSNAVQI", "X_forfid_K_final_I", 3.0,
     "K forfid plus final I"),
    ("EIBANSNAVQE", "late_X_forfid_E_final_E", 2.5,
     "later X-forfid E; placement atypical/chronologically awkward"),
    ("ENTAQCQAHIP", "reverse_published", 1.5,
     "published reverse reading; semantically unpromising"),
]

RELATIONSHIPS = [
    ("independent", 0.0, "two sides need not form one text"),
    ("side1_to_side2", 1.0, "assume continuous text side 1 then side 2"),
    ("side2_to_side1", 1.0, "assume continuous text side 2 then side 1"),
]

FIELDS = [
    "side1", "side1_model", "side2", "side2_model",
    "relationship", "assumption_cost", "notes",
]

def rows():
    for (s1, s1model, c1, n1), (s2, s2model, c2, n2), (rel, cr, nr) in product(
        SIDE1, SIDE2, RELATIONSHIPS
    ):
        yield {
            "side1": s1,
            "side1_model": s1model,
            "side2": s2,
            "side2_model": s2model,
            "relationship": rel,
            "assumption_cost": c1 + c2 + cr,
            "notes": f"{n1}; {n2}; {nr}",
        }

def exact_hit_probability(branches, lexicon_size, length, alphabet=20):
    """Toy intuition for short-string overfitting under uniform symbols."""
    space = alphabet ** length
    per_branch = min(1.0, lexicon_size / space)
    return 1.0 - (1.0 - per_branch) ** branches

if __name__ == "__main__":
    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows())
