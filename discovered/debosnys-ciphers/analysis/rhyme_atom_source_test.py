#!/usr/bin/env python3
"""Falsification tests for transparent atom-to-phoneme source alignments in DCP #4.

This is deliberately a *constraint* test, not a decoder.  It encodes only terminal
classes that have been frozen from the primary scans / prior published decomposition,
and asks what a proposed plaintext would require if Debosnys' visible atomic
components carried stable phoneme values.

The immediate test is Thomas Moore, Odes of Anacreon, Ode II.  Ode II remains useful
as a source hypothesis because it is 20 lines / 10 couplets and independently tied to
the sheet's Moore context.  This program tests a narrower mechanism:

    same plaintext phoneme => at least one shared visible atomic component

for line-final rhyme chunks.

Failure rejects a transparent deterministic atom->phoneme decomposition of the source;
it does NOT reject opaque syllable/rhyme codepoints, homophony, allography, positional
operators, or an adapted source.
"""

from itertools import combinations

# Frozen poem rhyme classes from the two public scans.
# Only classes with component decompositions strong enough to use are populated.
# A: lines 1-2 and 17-18, visually the same double-wave / N.N-like whole glyph.
# B: lines 3-4, dotted-X / <X DOT> family.
# G: lines 13-14, O + cross-like pair (published structural observation); not needed
#    for the decisive A-vs-B test but retained for future cross-class constraints.
OBSERVED = {
    "A": {"components": frozenset({"NN_PAIR"}), "lines": (1, 2, 17, 18)},
    "B": {"components": frozenset({"X", "DOT"}), "lines": (3, 4)},
    "C": {"components": None, "lines": (5, 6)},
    "D": {"components": None, "lines": (7, 8)},
    "E": {"components": None, "lines": (9, 10)},
    "F": {"components": None, "lines": (11, 12)},
    "G": {"components": frozenset({"O", "CROSS"}), "lines": (13, 14)},
    "H": {"components": None, "lines": (15, 16)},
    "I": {"components": None, "lines": (19, 20)},
}

# Broad rhyme nuclei/codas for Moore Ode II.  These are not intended as a complete IPA
# analysis; only shared final phonemes used by the tests matter.
ODE2 = {
    "A": {"words": ("song", "along"), "phonemes": frozenset({"AW", "NG"})},
    "B": {"words": ("string", "sing"), "phonemes": frozenset({"IH", "NG"})},
    "C": {"words": ("right", "to-night"), "phonemes": frozenset({"AI", "T"})},
    "D": {"words": ("high", "I"), "phonemes": frozenset({"AI"})},
    "E": {"words": ("dews", "infuse"), "phonemes": frozenset({"UU", "Z"})},
    "F": {"words": ("bound", "round"), "phonemes": frozenset({"AU", "N", "D"})},
    "G": {"words": ("thee", "ebriety"), "phonemes": frozenset({"II"})},
    "H": {"words": ("thought", "taught"), "phonemes": frozenset({"AW", "T"})},
    "I": {"words": ("string", "sing"), "phonemes": frozenset({"IH", "NG"})},
}


def required_shared_phonemes(a, b):
    return ODE2[a]["phonemes"] & ODE2[b]["phonemes"]


def observed_shared_components(a, b):
    ca = OBSERVED[a]["components"]
    cb = OBSERVED[b]["components"]
    if ca is None or cb is None:
        return None
    return ca & cb


def main():
    print("Transparent atom->phoneme falsification: Moore Ode II")
    print("=" * 61)

    powered = []
    pending = []
    contradictions = []

    for a, b in combinations(ODE2, 2):
        shared_ph = required_shared_phonemes(a, b)
        if not shared_ph:
            continue
        shared_atoms = observed_shared_components(a, b)
        row = (a, b, tuple(sorted(shared_ph)), None if shared_atoms is None else tuple(sorted(shared_atoms)))
        if shared_atoms is None:
            pending.append(row)
        else:
            powered.append(row)
            if not shared_atoms:
                contradictions.append(row)

    print("Powered tests (both terminal decompositions frozen):")
    for a, b, ph, atoms in powered:
        print(f"  {a}<->{b}: shared plaintext phoneme(s)={ph}; shared cipher atom(s)={atoms}")

    print("\nContradictions under the transparent deterministic model:")
    if contradictions:
        for a, b, ph, atoms in contradictions:
            print(f"  FAIL {a}<->{b}: requires a common encoding of {ph}, observed overlap={atoms}")
    else:
        print("  none yet")

    print("\nHighest-value pending tests:")
    priorities = [("C", "D", "shared AI"), ("C", "H", "shared T"), ("B", "I", "same IH+NG rhyme")]
    for a, b, why in priorities:
        print(f"  {a}<->{b}: {why}; freeze terminal atoms for {a} and {b}")

    print("\nInterpretation:")
    if contradictions:
        print("  REJECT: direct Ode-II + one stable visible atom per phoneme (transparent composition).")
        print("  KEEP: opaque rhyme/syllable codepoints, homophony/allography, positional operators,")
        print("        or an adapted / merely thematic Moore source.")
    else:
        print("  No powered contradiction yet.")


if __name__ == "__main__":
    main()
