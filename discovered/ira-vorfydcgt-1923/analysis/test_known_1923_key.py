"""Reproduce a documented 1923 IRA short-cipher control and test VORFYDCGT.

The published Gillogly example gives the six-letter Vigenere key GVZKLG and
shows SDRDPX -> MISTER. This script first requires that control to reproduce,
then applies exactly the same standard Vigenere convention, resetting the key
at the start of the target token.
"""

import string

ALPHABET = string.ascii_uppercase


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    out = []
    for i, c in enumerate(ciphertext.upper()):
        if c not in ALPHABET:
            continue
        shift = ALPHABET.index(key[i % len(key)].upper())
        out.append(ALPHABET[(ALPHABET.index(c) - shift) % 26])
    return "".join(out)


KNOWN_CIPHERTEXT = "SDRDPX"
KNOWN_KEY = "GVZKLG"
KNOWN_PLAINTEXT = "MISTER"
TARGET = "VORFYDCGT"

control = vigenere_decrypt(KNOWN_CIPHERTEXT, KNOWN_KEY)
assert control == KNOWN_PLAINTEXT, (control, KNOWN_PLAINTEXT)

target_plaintext = vigenere_decrypt(TARGET, KNOWN_KEY)
assert target_plaintext == "PTSVNXWLU"

print(f"control: {KNOWN_CIPHERTEXT} --{KNOWN_KEY}--> {control}")
print(f"target:  {TARGET} --{KNOWN_KEY}--> {target_plaintext}")
print("Known-key reuse does not yield readable plaintext; this rejects only that exact key/reset hypothesis.")

# A pure transposition cannot change the target's letter multiset.
print("target sorted letters:", "".join(sorted(TARGET)))
print("target all letters distinct:", len(set(TARGET)) == len(TARGET))
