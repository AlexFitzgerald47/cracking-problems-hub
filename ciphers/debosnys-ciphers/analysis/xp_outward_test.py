#!/usr/bin/env python3
"""Frozen outward test for the Debosnys shifted-signature key.

This script deliberately does no key search. It applies the seven-value shared
signature core to the independently observed poem-line terminal XP=<X DOT>,
then tests the old 'last 20/21 lines of Moore's Greek ode' plaintext candidate.

Sources:
- Sektu transcription revision (2017-08-04):
  https://sektu.blogspot.com/2017/08/debosnys-cipher-transcription-revision.html
- Sektu June 2017 archive, Moore-remainder hypothesis:
  https://sektu.blogspot.com/2017/06/
- Moore scan:
  https://upload.wikimedia.org/wikipedia/commons/0/09/The_poetical_works_of_Thomas_Moore_%28IA_poeticalworkstmo00moor%29.pdf
"""

SHARED_KEY = {
    "C2": "H",
    "B2": "EN",
    "X": "EC",
    "DOT": "OS",
    "N": "D",
    "U": "EB",
    "CROSSB": "YS",
}


def xp_terminal_syllable() -> str:
    """Reconstruct the terminal syllable predicted by XP=<X DOT>.

    X=EC is interpreted as previous-rime E + next-onset C.
    DOT=OS supplies the terminal rime. At the line boundary there is no later
    onset to borrow, so onset C + rime OS reconstructs COS.
    """
    x = SHARED_KEY["X"]
    dot = SHARED_KEY["DOT"]
    onset = x[-1]
    rime = dot
    return onset + rime


# Moore's 41-line Greek "An Ode by the Translator". For the falsifier we only
# need line-final words around the two possible cutoffs and the later /kos/
# anti-cherry-pick control. Numbering is 1-based to match the analysis note.
MOORE_ENDINGS = {
    21: "Λιναω",
    22: "εδωκας",
    23: "Κυπριδος",
    24: "Λιναον",
    25: "αινων",
    34: "γυναικος",
}


def direct_remainder_pair(start_line: int) -> tuple[str, str]:
    """Return Moore endings aligned to cipher lines 3 and 4."""
    return (MOORE_ENDINGS[start_line + 2], MOORE_ENDINGS[start_line + 3])


def main() -> None:
    predicted = xp_terminal_syllable()
    assert predicted == "COS"

    print(f"Frozen shared-core prediction for poem terminal XP: {predicted} (/kos/)")

    # Sektu says 20-21 Moore lines remain. With a 41-line original, direct
    # line-preserving plaintext can therefore start at Moore line 21 or 22.
    for start in (21, 22):
        pair = direct_remainder_pair(start)
        print(
            f"If cipher line 1 = Moore line {start}, "
            f"cipher lines 3-4 end: {pair[0]} / {pair[1]}"
        )

    assert direct_remainder_pair(21) == ("Κυπριδος", "Λιναον")
    assert direct_remainder_pair(22) == ("Λιναον", "αινων")

    # Neither pair is a repeated COS/KOS rhyme. The later gynaikos occurrence
    # is retained explicitly so it cannot be cherry-picked as a line-3/4 hit.
    print(f"Later Moore line 34 control: {MOORE_ENDINGS[34]} (gynaikos, final /kos/)")
    print("RESULT: direct 20/21-line Moore-remainder plaintext is rejected under frozen XP->COS.")


if __name__ == "__main__":
    main()
