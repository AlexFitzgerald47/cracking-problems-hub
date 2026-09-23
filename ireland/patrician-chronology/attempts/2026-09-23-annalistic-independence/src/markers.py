"""The compiler's alternative-source markers.

These are the places where an annalist stops recording and starts *arbitrating*:
"Or here, the falling asleep of St Mochta", "Repose of the elder Patrick, as
some books state", "I have found this in the Book of Cuanu".  They are the only
direct, first-person evidence in the corpus about how the early sections were
assembled, and they are countable.

The pattern set was built by scanning the corpus for source-attribution and
alternative-statement language, then hand-audited: all 87 hits in the four
witnesses were read and all 87 are genuine (precision 1.00, see
results/marker_audit.txt).  Recall is not claimed to be 1.
"""
import re

MARKER = re.compile(r'''(
   \bsome\s+(?:books|say|records?|state|assert|authors|write)
 | \bothers?\b[^.]{0,25}\b(?:say|says|state|record|assert|compute|write)
 | \bas\s+(?:some|others|we|is\s+(?:said|found|stated))\b
 | \bor\s+here\b
 | \bhere\s+some\b
 | \bin\s+the\s+[Bb]ook\s+of\b
 | \b[Ii]\s+have\s+found\b
 | \bwe\s+have\s+found\b
 | \baccording\s+to\s+(?:some|others|the\s+[Bb]ook)
 | \but\s+dicitur\b | \but\s+alii\b | \balii\s+dicunt\b
 | \bin\s+another\s+book\b | \bin\s+some\s+books\b
)''', re.I | re.X)

# Patrician and Palladian material.  Personal-name stems only; deliberately not
# extended to disciples or churches, so the class stays checkable by eye.
PATRICIAN = re.compile(r'\b(Patric|Patraic|Patrik|Palladi|Pallad)', re.I)


def is_marked(text):
    return bool(MARKER.search(text))


def marker_of(text):
    m = MARKER.search(text)
    return m.group(0) if m else None
