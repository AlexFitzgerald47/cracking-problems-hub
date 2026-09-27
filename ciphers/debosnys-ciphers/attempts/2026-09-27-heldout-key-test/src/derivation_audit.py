#!/usr/bin/env python3
"""D1/D2 of FREEZE.md: re-run the 2026-09-05 signature derivation with the DOT removed
(bare X, which is what the only public scan shows) and with the dot read first (top-first
order, which is where the only candidate mark sits). Uses the committed Hub derivation code
unchanged; only the component stream is varied.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "analysis"))
import signature_shifted_phonetic_model as m  # noqa: E402

UNITS = ["H", "EN", "EC", "OSD", "EB", "OSN", "OST", "YS"]
TARGET = "HENECOSDEBOSNOSTYS"
VARIANTS = {
    "published <X DOT>": ["C2", "B2", "X", "DOT", "N", "U", "O", "Z", "O", "O2RNO", "CROSSB"],
    "bare X (no DOT)": ["C2", "B2", "X", "N", "U", "O", "Z", "O", "O2RNO", "CROSSB"],
    "dot-first <DOT X>": ["C2", "B2", "DOT", "X", "N", "U", "O", "Z", "O", "O2RNO", "CROSSB"],
}


def run():
    out = {}
    for name, atoms in VARIANTS.items():
        m.ATOMS = atoms
        for mc in (2, 3, 4):
            sols = m.collect_solutions(TARGET, max_chunk=mc)
            ub = set(m.unit_boundaries(UNITS))
            aligned = [s for s in sols if ub.issubset(set(m.atom_boundaries(s)))]
            nd = [s for s in aligned if s.get("N") == "D"]
            out[(name, mc)] = (len(sols), len(aligned), len(nd), nd)
    return out


if __name__ == "__main__":
    res = run()
    for (name, mc), (s, a, nd, maps) in res.items():
        print(f"{name:20s} max_chunk={mc}: strict={s:5d} aligned={a:3d} aligned&N=D={nd}")
    assert res[("published <X DOT>", 2)][:3] == (57, 4, 2)
    assert res[("bare X (no DOT)", 2)][1] == 0
    assert all(res[("bare X (no DOT)", mc)][2] == 0 for mc in (2, 3, 4))
    s2 = res[("dot-first <DOT X>", 2)][3]
    assert all(mp["DOT"] == "EC" and mp["X"] == "OS" for mp in s2)
    print("\nD1: without the DOT no map survives with N=D at any chunk size <= 4.")
    print("D2: dot-first order keeps the fit but swaps the values: DOT=EC, X=OS.")
