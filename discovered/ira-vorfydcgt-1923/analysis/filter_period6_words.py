"""Test ordinary 9-letter English words under a repeated 6-letter Vigenere key.

For target ciphertext VORFYDCGT, derive the Vigenere keystream required by
each 9-letter dictionary word.  If encryption used a 6-letter key reset at
the token start, keystream positions 1-3 must repeat at positions 7-9.

Dependency: pip install cmudict
The corpus is CMUdict's alphabetic 9-letter entries; this is a screening
corpus, not a proof over all names/codewords/English strings.
"""

import re
import string
import cmudict

TARGET = "VORFYDCGT"
ALPHABET = string.ascii_uppercase
A2I = {c: i for i, c in enumerate(ALPHABET)}


def required_keystream(plaintext: str) -> str:
    return "".join(
        ALPHABET[(A2I[c] - A2I[p.upper()]) % 26]
        for c, p in zip(TARGET, plaintext)
    )


def compatible_with_period(key_stream: str, period: int) -> bool:
    return all(key_stream[i] == key_stream[i % period] for i in range(len(key_stream)))


words = sorted({
    w.lower()
    for w in cmudict.words()
    if len(w) == len(TARGET) and re.fullmatch(r"[a-z]+", w)
})

hits = []
for word in words:
    stream = required_keystream(word)
    if compatible_with_period(stream, 6):
        hits.append((word, stream[:6], stream))

print("9-letter CMUdict entries screened:", len(words))
print("period-6-compatible entries:", len(hits))
for word, key, stream in hits:
    print(f"{word:12s} key={key} stream={stream}")

assert len(words) == 13124
assert hits == [
    ("bilzerian", "UGGGUM", "UGGGUMUGG"),
    ("embattled", "RCQFFK", "RCQFFKRCQ"),
    ("embezzled", "RCQBZE", "RCQBZERCQ"),
    ("embroiled", "RCQOKV", "RCQOKVRCQ"),
]
