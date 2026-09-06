#!/usr/bin/env python3
"""Factor the signature's repeated shifted-rime transitions.

Conditional premises:
- plaintext crib: HE | NE | COS | DE | BOS | NOS | TYS/A
- Sektu shifted mechanism: initial onset, then rime_i+onset_(i+1), final rime
- published component stream:
  C2 B2 X DOT N U O Z O O2RNO CROSSB

The previous strict search left two atom maps for the three OS transitions:
  OSD -> DOT N
  OSN -> O Z
  OST -> O O2RNO

This test adds one mechanistic constraint, not a language-frequency prior:
for a complex shifted unit RIME+ONSET represented by two subglyphs, the first
subglyph encodes the rime and the second encodes the next onset. This is the
literal factorization implied by the shifted-rime model and Sektu's suggestion
that complex groups can be split across symbols.

Under that constraint Branch B is uniquely selected.
"""

TRANSITIONS = [
    (("DOT", "N"), ("OS", "D")),
    (("O", "Z"), ("OS", "N")),
    (("O", "O2RNO"), ("OS", "T")),
]

BRANCH_A = {
    "DOT": "OS",
    "N": "D",
    "O": "O",
    "Z": "SN",
    "O2RNO": "ST",
}

BRANCH_B = {
    "DOT": "OS",
    "N": "D",
    "O": "OS",
    "Z": "N",
    "O2RNO": "T",
}


def respects_rime_onset_factorization(mapping):
    for (left_atom, right_atom), (rime, onset) in TRANSITIONS:
        if mapping[left_atom] != rime:
            return False
        if mapping[right_atom] != onset:
            return False
    return True


def show(mapping, name):
    print(name)
    for (a, b), (rime, onset) in TRANSITIONS:
        got = mapping[a] + mapping[b]
        target = rime + onset
        print(
            f"  {a}+{b}: {mapping[a]}|{mapping[b]} -> {got} "
            f"target={rime}|{onset} factorized={mapping[a] == rime and mapping[b] == onset}"
        )
    print("  passes:", respects_rime_onset_factorization(mapping))


if __name__ == "__main__":
    show(BRANCH_A, "Branch A")
    show(BRANCH_B, "Branch B")
    assert not respects_rime_onset_factorization(BRANCH_A)
    assert respects_rime_onset_factorization(BRANCH_B)
    print("\nSelected under explicit rime|onset splitting: Branch B")
    print("  DOT = OS   N = D")
    print("  O   = OS   Z = N")
    print("  O   = OS   O2RNO = T")
    print("\nPrediction: terminal <X DOT> decodes as EC | OS, whose final syllable is C+OS = COS.")
