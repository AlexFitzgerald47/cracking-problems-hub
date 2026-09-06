#!/usr/bin/env python3
"""Test the cross-page Henecos signature against Sektu's 2017 shifted-rhyme model.

Independent inputs:
1) 2015 plaintext observation: HENECOS DE BOS NOS TYA (accent stripped).
2) 2017 Sektu hypothesis: break phonetic text into the rhyme of one syllable
   plus the onset of the next; complex groups may be split across symbols.
3) 2017 Sektu deconstruction of the six-glyph signature-like line:
   <C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>
4) 2017 N-topology observation: N could be a syllable-initial consonant such
   as French b or d.

The script shows that these inputs select a very small family of atom maps
from the 57 strict <=2-character maps that merely fit the raw letter string.
"""

ATOMS = ["C2", "B2", "X", "DOT", "N", "U", "O", "Z", "O", "O2RNO", "CROSSB"]
TARGETS = ["HENECOSDEBOSNOSTYA", "HENECOSDEBOSNOSTYS"]
SYLLABLES = ["HE", "NE", "COS", "DE", "BOS", "NOS", "TYA"]
ONSETS = ["H", "N", "C", "D", "B", "N", "T"]
RIMES = ["E", "E", "OS", "E", "OS", "OS", "YA"]


def shifted_units(onsets=ONSETS, rimes=RIMES):
    """Initial onset; then rhyme_i+onset_(i+1); then final rhyme."""
    out = [onsets[0]]
    out.extend(rimes[i] + onsets[i + 1] for i in range(len(onsets) - 1))
    out.append(rimes[-1])
    return out


def collect_solutions(text, max_chunk=2):
    mapping = {}
    out = []

    def rec(i, pos):
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
                mapping[atom] = text[pos:pos + length]
                rec(i + 1, pos + length)
                del mapping[atom]

    rec(0, 0)
    return out


def atom_boundaries(mapping):
    pos = 0
    out = []
    for atom in ATOMS:
        pos += len(mapping[atom])
        out.append(pos)
    return out


def unit_boundaries(units):
    pos = 0
    out = []
    for u in units:
        pos += len(u)
        out.append(pos)
    return out


def flatten(mapping):
    return "".join(mapping[a] for a in ATOMS)


def candidate_branches(final_rime="YA"):
    # After enforcing all shifted-unit boundaries and the independently
    # motivated N=D onset assignment, exactly two clean branches remain.
    common = {
        "C2": "H",
        "B2": "EN",
        "X": "EC",
        "DOT": "OS",
        "N": "D",
        "U": "EB",
        "CROSSB": final_rime,
    }
    a = dict(common, O="O", Z="SN", O2RNO="ST")
    b = dict(common, O="OS", Z="N", O2RNO="T")
    return a, b


if __name__ == "__main__":
    units = shifted_units()
    target = "".join(SYLLABLES)
    assert "".join(units) == target
    print("syllables:", " | ".join(SYLLABLES))
    print("Sektu-style shifted units:", " | ".join(units))
    print("flattened:", "".join(units))

    sols = collect_solutions(target)
    sb = set(unit_boundaries(units))
    aligned = [s for s in sols if sb.issubset(set(atom_boundaries(s)))]
    n_onset = [s for s in aligned if s.get("N") == "D"]

    print("\nstrict <=2-char maps fitting target:", len(sols))
    print("maps preserving every shifted-unit boundary:", len(aligned))
    print("...and satisfying N=D onset hypothesis:", len(n_onset))

    print("\nremaining two branches:")
    for i, s in enumerate(n_onset, 1):
        print(i, s)
        print("  flattened:", flatten(s))
        print("  atom boundaries:", atom_boundaries(s))

    expected_a, expected_b = candidate_branches("YA")
    assert expected_a in n_onset
    assert expected_b in n_onset

    print("\nshared assignments selected by independent constraints:")
    shared = {k: expected_a[k] for k in expected_a if expected_a[k] == expected_b[k]}
    for k, v in shared.items():
        print(f"  {k:8s} -> {v}")
    print("ambiguous tail branch A: O=O, Z=SN, O2RNO=ST")
    print("ambiguous tail branch B: O=OS, Z=N, O2RNO=T")

    # Primary-image final TYS variant changes only the final atom output.
    tys_a, tys_b = candidate_branches("YS")
    assert flatten(tys_a) == TARGETS[1]
    assert flatten(tys_b) == TARGETS[1]
