#!/usr/bin/env python3
"""Reproduce the Ennis bead working decipherment.

The learned-ogham alphabet is represented as 20 tokens.  The modern
specialist's ordinary-sign route is DMVAVA.  Decrypt by moving each token
three places backward cyclically.
"""

OGHAM = ("B", "L", "V", "S", "N", "H", "D", "T", "C", "Q",
         "M", "G", "NG", "Z", "R", "A", "O", "U", "E", "I")
CIPHERTEXT = ("D", "M", "V", "A", "V", "A")
SHIFT = -3


def rotate_token(token: str, shift: int) -> str:
    i = OGHAM.index(token)
    return OGHAM[(i + shift) % len(OGHAM)]


def main() -> None:
    plaintext_tokens = tuple(rotate_token(t, SHIFT) for t in CIPHERTEXT)
    plaintext = "".join(plaintext_tokens)
    print("alphabet :", " ".join(OGHAM))
    print("cipher   :", " ".join(CIPHERTEXT))
    print("shift    :", SHIFT)
    print("tokens   :", " ".join(plaintext_tokens))
    print("plaintext:", plaintext)
    assert plaintext_tokens == ("S", "T", "I", "NG", "I", "NG")
    assert plaintext == "STINGING"


if __name__ == "__main__":
    main()
