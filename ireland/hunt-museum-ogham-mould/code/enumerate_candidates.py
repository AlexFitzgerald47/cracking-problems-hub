#!/usr/bin/env python3
"""Enumerate serious HCA 686 reading branches and a simple exact-hit null.

This does NOT assign linguistic probabilities. It makes the branch/search budget
explicit so that a later lexical hit cannot be treated as if it were one pre-specified
reading.

Geometry is based on the published June 2025 OG(H)AM audit pending direct local render
of the CC0 mesh/images:
- published orientation cores: ALU, ALNG, MLU, MLNG
- upended counterparts: UDA, NGDA, UDM, NGDM
- sign 4: Younger-Futhark-like R (ʀ) or post-c.1050 Y value
- sign 5: either non-phonetic/terminal, or weak P hypothesis
- both reading directions are kept.

`assumption_cost` is only a transparent bookkeeping heuristic:
+1 per inclined/less-standard core choice; +1 for upended orientation; +1 for Y
rather than the earlier ʀ value; +2 for phonetic P because the cited y-like P form in
Bern MS 207 is reported as unattested elsewhere. Lower is fewer special assumptions,
not higher posterior probability.
"""

from itertools import product


def reverse_tokens(core: str) -> str:
    tokens = []
    i = 0
    while i < len(core):
        if core[i:i+2] == "NG":
            tokens.append("NG")
            i += 2
        else:
            tokens.append(core[i])
            i += 1
    return "".join(reversed(tokens))


TOP = {"ALU": 0, "ALNG": 1, "MLU": 1, "MLNG": 2}
UPENDED = {"UDA": 0, "NGDA": 1, "UDM": 1, "NGDM": 2}


def enumerate_candidates():
    out = []
    for orientation, cores in (("published", TOP), ("upended", UPENDED)):
        for core, geometry_cost in cores.items():
            for rune_value, rune_cost in (("R", 0), ("Y", 1)):
                for direction in ("left_to_right", "right_to_left"):
                    for sign5, sign5_cost in (("nonphonetic", 0), ("P", 2)):
                        if direction == "left_to_right":
                            sequence = core + rune_value + ("" if sign5 == "nonphonetic" else "P")
                        else:
                            sequence = ("" if sign5 == "nonphonetic" else "P") + rune_value + reverse_tokens(core)
                        out.append({
                            "orientation": orientation,
                            "core": core,
                            "rune_value": rune_value,
                            "direction": direction,
                            "sign5": sign5,
                            "sequence": sequence,
                            "phonetic_signs": 4 + (sign5 == "P"),
                            "assumption_cost": geometry_cost + rune_cost + sign5_cost + (orientation == "upended"),
                        })
    return sorted(out, key=lambda r: (r["assumption_cost"], r["sequence"]))


def exact_hit_probability(alphabet_size: int, lexicon_entries_per_length: int, n4=32, n5=32):
    """Illustrative matched-search null under uniform independent strings.

    This is deliberately simple and should not be mistaken for a language model.
    Its purpose is to show the multiple-testing burden created by branching a
    four/five-sign inscription before searching dictionaries and name lists.
    """
    p_no_4 = (1 - alphabet_size ** -4) ** (n4 * lexicon_entries_per_length)
    p_no_5 = (1 - alphabet_size ** -5) ** (n5 * lexicon_entries_per_length)
    return 1 - p_no_4 * p_no_5


if __name__ == "__main__":
    candidates = enumerate_candidates()
    print(f"candidates={len(candidates)} unique={len({r['sequence'] for r in candidates})}")
    for r in candidates:
        print("\t".join(str(r[k]) for k in ("assumption_cost", "orientation", "core", "rune_value", "direction", "sign5", "sequence")))

    print("\nNULL")
    for alphabet_size in (16, 20, 24):
        for n in (500, 1000, 5000, 10000):
            p = exact_hit_probability(alphabet_size, n)
            print(f"K={alphabet_size}\tN={n}\tp_any_exact={p:.6f}")
