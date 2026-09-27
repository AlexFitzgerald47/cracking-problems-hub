#!/usr/bin/env python3
"""Transparent competitor comparison for Moynagh Lough side 2.

This is deliberately NOT a probability model. It separates:
1) phonological operations needed to map candidate Irish forms to the observed ogham;
2) external evidence such as attestation, morphology, formula parallels, and object semantics;
3) sensitivity of the qualitative ranking to reasonable positive re-weighting.

Run with Python 3 stdlib only.
"""

from __future__ import annotations
import random
from collections import Counter

OBSERVED = ("S", "N", "A", "V", "Q", "E")

# Phonological-token models. A single token may correspond to more than one manuscript
# grapheme (e.g. AI in -aige is represented here as one unstressed vowel plus
# consonant-quality information, because ogham does not normally encode palatal glides).
CANDIDATES = {
    "pipan_snamaige": {
        "label": "Pípán snámaige ('Pípán, swimmer')",
        "tokens": ("S", "N", "A", "M_LEN", "SCHWA", "G_PAL_LEN", "E"),
        "residual": "omit one post-tonic schwa; ogham does not mark palatalization",
    },
    "pipan_snamach": {
        "label": "Pípán snámach ('Pípán, swimmer/buoyant') + terminal/damaged sign",
        "tokens": ("S", "N", "A", "M_LEN", "CH"),
        "residual": "treat final damaged E/I-like sign as non-phonetic/terminal",
    },
    "tube_bark": {
        "label": "pípán *snamchae ('tube of bark')",
        "tokens": ("S", "N", "A", "M_LEN", "CH", "SCHWA", "E"),
        "residual": "omit/reduce one post-tonic vowel in hypothetical genitive",
    },
}

# Supported late-Irish/late-ogham correspondences used by BOTH the published reading
# and the competing swimmer readings.
TOKEN_TO_OGHAM = {
    "S": "S",
    "N": "N",
    "A": "A",
    "M_LEN": "V",      # lenited/intervocalic m ~ nasalised labial fricative
    "G_PAL_LEN": "Q", # late/merged guttural value; palatality not written in ogham
    "CH": "Q",        # alternative late guttural interpretation
    "E": "E",
}

# Ordinal evidence scores: +2 strong independent support, +1 useful support,
# 0 neutral/unknown, -1 cost, -2 major cost. These are explicit judgments, not data.
DIMENSIONS = (
    "period_first_unit",
    "second_form_attested",
    "independent_word_boundary",
    "m_to_v_supported",
    "q_guttural_supported",
    "final_sign_explained",
    "unwritten_vowel_cost",
    "portable_name_epithet_parallel",
    "object_semantics",
    "date_fit",
    "morphology_attested",
    "human_swimmer_parallel",
)

EVIDENCE = {
    "pipan_snamaige": (2, 2, 1, 1, 1, 2, -1, 2, 1, 2, 2, 1),
    "pipan_snamach":  (2, 2, 1, 1, 1,-2,  0, 2, 1, 2, 2, 2),
    "tube_bark":      (0,-1, 1, 1, 1, 2, -1, 0,-2, 0,-2, 0),
    "pipan_unknown":  (2,-2, 1, 0, 0, 0,  0, 2, 1, 2,-2, 0),
}

LABELS = {
    **{k: v["label"] for k, v in CANDIDATES.items()},
    "pipan_unknown": "Pípán + unresolved qualifier",
}


def collapse(tokens):
    out = []
    omitted = []
    for t in tokens:
        if t == "SCHWA":
            omitted.append(t)
            continue
        out.append(TOKEN_TO_OGHAM[t])
    return tuple(out), omitted


def show_phonological_comparison():
    print("Observed:", "".join(OBSERVED))
    print()
    for key, c in CANDIDATES.items():
        collapsed, omitted = collapse(c["tokens"])
        if key == "pipan_snamach":
            # candidate predicts SNAVQ; observed has one additional damaged sign
            exact = collapsed == OBSERVED[:-1]
        else:
            exact = collapsed == OBSERVED
        print(f"{key:16s} -> {''.join(collapsed):8s} match={exact}")
        print("  residual:", c["residual"])
    print()


def base_scores():
    return {k: sum(v) for k, v in EVIDENCE.items()}


def sensitivity(seed=42, n=100_000):
    """Perturb only the importance weights, not the evidence signs.

    Each dimension receives an independent weight U(0.5, 2.0). This asks whether
    the ranking depends on one arbitrary weighting choice. It does NOT produce
    posterior probabilities.
    """
    rng = random.Random(seed)
    wins = Counter()
    keys = list(EVIDENCE)
    for _ in range(n):
        weights = [rng.uniform(0.5, 2.0) for _ in DIMENSIONS]
        vals = {
            k: sum(w * s for w, s in zip(weights, EVIDENCE[k]))
            for k in keys
        }
        wins[max(vals, key=vals.get)] += 1
    return {k: wins[k] / n for k in keys}


def main():
    show_phonological_comparison()
    print("Ordinal evidence scores (not probabilities):")
    for k, score in sorted(base_scores().items(), key=lambda kv: -kv[1]):
        print(f"  {score:>3}  {LABELS[k]}")
    print("\nWeight-sensitivity winner shares (NOT solve probabilities):")
    for k, p in sorted(sensitivity().items(), key=lambda kv: -kv[1]):
        print(f"  {p:6.2%}  {LABELS[k]}")


if __name__ == "__main__":
    main()
