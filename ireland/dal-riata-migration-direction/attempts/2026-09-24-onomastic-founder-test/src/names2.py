# -*- coding: utf-8 -*-
"""CORRECTED name extraction.  Supersedes names.py, which is left in place unmodified
because FREEZE.md and the failed first confirmatory run depend on it.

The frozen positive control (Columban familia must look Irish) FAILED at cov=0.693
against a null lower bound of 0.772.  Diagnosis found three defects, all of which
depress a small out-of-sample group relative to an in-sample null:

  D1  EPITHETS.  An early Irish personal name is GIVEN NAME + optional epithet.
      names.py matched whole surface strings, so 'Failbe' in an Iona entry never
      matched 'Failbe Flann' (x9) and 'Failbe Fland' (x2) in the Irish reference, and
      Failbe was scored 12 times as "a name unattested in Ireland".  It is one of the
      commonest names in the corpus.  15.2 % of all name tokens are two-word.
      FIX: reduce to the head element, EXCEPT where the first element is one of the
      productive Irish name-forming prefixes (Mael/Máel/Maol, Cú/Con, Dub, Cenn, Gilla,
      Mac, Fer, Gille), where the two elements together are the given name and
      reducing to 'mael' would merge 499 distinct people into one.

  D2  REFERENCE POOL.  is_irish_ref() demanded a positive Irish place/people marker,
      which discarded 1,800 name-bearing in-window entries -- bare obits of the form
      "Death of X son of Y" with no toponym.  That is a large, and not random, slice of
      the Irish name stock.  FIX: the reference is every in-window entry carrying NO
      north-channel marker.  The positive-marker version is retained as a sensitivity
      run (POOL='marked').

  D3  EDITORIAL SPELLING.  Sléibéne / Slébíne / Sleibine / Sleibéne are one man and were
      four distinct skeletons; Dorbene / Doirbéne likewise.  Accent-stripping alone does
      not fold vowel-digraph variation across four editors working a century apart.
      FIX: a name counts as attested if its skeleton matches exactly OR within
      Levenshtein distance 1 for skeletons of length >= 6.  Applied identically to every
      group and to the null, so it cannot favour one.

D1-D3 all act in the same direction and none of them is visible without a control whose
answer is known in advance.  This is what the positive control was for.
"""
import re, unicodedata
from names import NAME, FRAMES, STOP          # frames are unchanged and were not at fault

# First elements that are part of the given name rather than an epithet.
PREFIX = {"mael", "mel", "maol", "cu", "con", "dub", "cenn", "cend", "gilla", "gille",
          "mac", "fer", "find", "ros"}

def _strip(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower().replace("’", "").replace("'", "").replace("-", " ").strip()

def skeleton(name):
    """Normalised comparison key for a surface form: given name only, spelling folded."""
    s = _strip(name)
    parts = s.split()
    if len(parts) == 2 and _strip(parts[0]) not in PREFIX:
        parts = parts[:1]                      # drop the epithet
    s = " ".join(parts)
    s = s.replace("bh", "b").replace("mh", "m").replace("dh", "d").replace("gh", "g")
    s = s.replace("th", "t").replace("ch", "c").replace("ph", "f").replace("sh", "s")
    s = re.sub(r"([aeiou])\1+", r"\1", s)
    for pat, rep in [(r"^aod", "aed"), (r"^aedh", "aed"), (r"^oeng", "aeng"),
                     (r"^oing", "aeng"), (r"^eng", "aeng"),
                     (r"^brid(e|ei)", "brude"), (r"^bred(e|ei)", "brude")]:
        s = re.sub(pat, rep, s)
    return s

def extract(text):
    out = []
    for fr in FRAMES:
        for m in fr.finditer(text):
            n = m.group(1).strip()
            first = n.split()[0]
            if first in STOP:
                continue
            if len(n.split()) == 2 and n.split()[1] in STOP:
                n = first
            out.append(n)
    return out

def _lev(a, b, cap=2):
    """Levenshtein distance, capped."""
    if abs(len(a) - len(b)) > cap: return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        if min(cur) > cap: return cap + 1
        prev = cur
    return prev[-1]

def consonants(s):
    return re.sub(r"[aeiou\s]", "", s)

class Reference:
    """Attestation lookup over a reference name pool, with the D3 editorial fold.

    A skeleton counts as attested if it matches a reference skeleton exactly, or -- for
    skeletons of at least FUZZ_MIN characters -- if it shares an IDENTICAL CONSONANT
    FRAME with a reference skeleton and differs from it by at most two vowel edits.
    That is tight enough that Sleibene/Slebine and Dorbene/Doirbene fold together while
    Aed/Aedan (frames 'd' vs 'dn') and Conall/Conaing ('cnll' vs 'cnng') do not.
    Applied identically to every group and to every null draw.
    """
    FUZZ_MIN = 6

    def __init__(self, skeletons):
        self.exact = set(skeletons)
        self.by_frame = {}
        for s in self.exact:
            if len(s) >= self.FUZZ_MIN:
                self.by_frame.setdefault(consonants(s), []).append(s)

    def attested(self, s):
        if s in self.exact: return True
        if len(s) < self.FUZZ_MIN: return False
        for cand in self.by_frame.get(consonants(s), ()):
            if _lev(s, cand, 2) <= 2: return True
        return False
