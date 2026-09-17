#!/usr/bin/env python3
"""Segment the 1813 Philadelphia edition of *Junius* (Bradford & Inskeep, 2 vols,
reprinting Woodfall's 1812 collection) into author-attributed public letters.

Purpose: this is the SECOND, independent digitisation of the same public letters that
Wikisource carries in proofread form from the 1772 Woodfall first edition. Having the
same texts from two editions and two transcription pipelines is what lets us measure
the edition/OCR source effect directly -- the size of the "same author, different
source" distance, against which any "different author, same source" distance has to be
judged. Without that measurement a cross-corpus attribution number means nothing.

Authorship comes from the signature at the foot of each letter, never from the
edition's framing: the collection interleaves replies by Sir William Draper, John
Wilkes and others among the numbered letters.

Known limitation, recorded rather than papered over: the 1812/1813 edition is heavily
annotated, and the OCR interleaves Good's footnotes with the letter text at page
breaks. The filters below remove the obvious apparatus but not all of it. Contamination
is therefore higher in this corpus than in the Wikisource one, which is part of why the
two are kept separate rather than pooled.
"""
import json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "data", "raw")
OUT = os.path.join(HERE, "..", "data", "corpus")

VOLUMES = ["juniusincludingl01.txt", "juniusincludingl02.txt"]

LETTER_HEAD = re.compile(r"\n[ \t]*LETTER[ \t]+([IVXLC]+)\.[ \t]*\n")

SIG_RULES = [
    (r"^PHILO\s+JUNIUS$",                    "Philo_Junius"),
    (r"^JUNIUS$",                            "Junius"),
    (r"^W(?:ILLIAM)?\.?\s*D(?:RAPER)?\.?$",  "William_Draper"),
    (r"^JOHN\s+WILKES$",                     "John_Wilkes"),
    (r"^MODESTUS$",                          "Modestus"),
    (r"^ANTI[- ]?SEJANUS$",                  "Anti_Sejanus"),
]
SIG_RULES = [(re.compile(p), lab) for p, lab in SIG_RULES]


def signature(block):
    """Authorship marker = the last all-caps signature line in the letter."""
    tail = block[-1200:]
    found = None
    for m in re.finditer(r"\n[ \t]*([A-Z][A-Z .&'\-]{1,30}?)\.?[ \t]*\n", tail):
        s = re.sub(r"\s+", " ", m.group(1)).strip().rstrip(".")
        for pat, lab in SIG_RULES:
            if pat.match(s):
                found = lab
    return found


def clean(body):
    kept = []
    for line in body.split("\n"):
        s = line.strip()
        if not s:
            continue
        if re.fullmatch(r"[\divxlc]{1,5}", s, re.I):          # page number
            continue
        # running heads: "LETTERS OF JUNIUS. 123" / "123 JUNIUS."
        if re.fullmatch(r"\d{0,4}\s*[A-Z][A-Z .,'\-]{4,40}\.?\s*\d{0,4}", s):
            continue
        if re.match(r"^[*†‡]\s", s):                 # footnote marker
            continue
        kept.append(s)
    return re.sub(r"\s+", " ", " ".join(kept)).strip()


def main():
    os.makedirs(OUT, exist_ok=True)
    docs = []
    unattributed = 0
    for vol in VOLUMES:
        path = os.path.join(RAW, vol)
        if not os.path.exists(path):
            print(f"MISSING {vol}", file=sys.stderr)
            continue
        text = open(path, errors="replace").read()
        marks = [(m.start(), m.end(), m.group(1)) for m in LETTER_HEAD.finditer(text)]
        for i, (s, e, num) in enumerate(marks):
            end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
            block = text[e:end]
            author = signature(block)
            body = clean(block)
            if author is None:
                unattributed += 1
                continue
            if len(body.split()) < 200:
                continue
            docs.append(dict(author=author, source="junius_1813_ocr", volume=vol,
                             letter=num, genre="public_letter",
                             n_words=len(body.split()), text=body))
    with open(os.path.join(OUT, "junius_1813_ocr.jsonl"), "w") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")
    c, w = Counter(), Counter()
    for d in docs:
        c[d["author"]] += 1
        w[d["author"]] += d["n_words"]
    print(f"{len(docs)} letters kept, {unattributed} blocks with no recognised signature\n")
    for a, n in c.most_common():
        print(f"  {a:18s} {n:3d} letters {w[a]:7d} words")


if __name__ == "__main__":
    main()
