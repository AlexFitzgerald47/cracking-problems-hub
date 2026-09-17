#!/usr/bin/env python3
"""Build the clean Junius corpus from the proofread Wikisource text of Woodfall's
1772 first edition, segmented by the signature at the foot of each letter.

This is the reference Junius corpus: proofread rather than OCR'd, from the edition
Junius himself supervised, and -- critically -- it carries the replies by his named
opponents in the SAME volume, same genre, same topic, same year, same printing. Those
replies are the only genre- and source-matched negative control this problem has, and
they are what makes a power calibration possible at all.

The Wikisource page header says `author = Junius` on every numbered letter. It is
wrong: Letter II is signed WILLIAM DRAPER. Attribution is taken from the signature.

Two rendering artefacts are repaired: the ProofreadPage navigation strip at the top of
every page, and drop capitals, which render as a separated initial ("J unius engages",
"A t the intercession").
"""
import json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "data", "raw", "wikisource_text")
OUT = os.path.join(HERE, "..", "data", "corpus")

SIG_RULES = [
    (r"^PHILO[\s-]*JUNIUS$",                      "Philo_Junius"),
    (r"^JUNIUS$",                                 "Junius"),
    (r"^W(?:ILLIAM)?\.?\s*DRAPER$",               "William_Draper"),
    (r"^W\.\s*D\.?$",                             "William_Draper"),
    (r"^MODESTUS$",                               "Modestus"),
    (r"^ANTI[\s-]*SEJANUS$",                      "Anti_Sejanus"),
    (r"^A\s+WHIG$",                               "A_Whig"),
    (r"^JOHN\s+HORNE$",                           "John_Horne_Tooke"),
    (r"^ATTICUS$",                                "Atticus"),
    (r"^BRUTUS$",                                 "Brutus"),
]
SIG_RULES = [(re.compile(p, re.I), lab) for p, lab in SIG_RULES]

NAV = re.compile(r"^.*?→\s*\d+\s+Letters of Junius\s+—\s+[^\n]*\n", re.S)
DATELINE = re.compile(r"^\s*\d{1,2}[.,]?\s+\w+[.,]?\s+\d{4}\.?\s*$", re.M)


def strip_nav(t):
    m = NAV.match(t)
    if m:
        return t[m.end():]
    # fallback: drop everything up to and including the "Letters of Junius — X" strip
    m = re.search(r"Letters of Junius\s+—\s+[^\n]*\n", t)
    return t[m.end():] if m else t


def fix_dropcaps(t):
    # "J unius engages" -> "Junius engages"; only a lone capital before a lowercase run
    return re.sub(r"(?<![A-Za-z])([A-Z]) ([a-z]{2,})", r"\1\2", t)


def signature(body):
    """Last recognised all-caps signature in the letter."""
    found = None
    for m in re.finditer(r"(?m)^\s*([A-Z][A-Z .&'\-]{1,28}?)\.?\s*$", body):
        s = re.sub(r"\s+", " ", m.group(1)).strip().rstrip(".")
        for pat, lab in SIG_RULES:
            if pat.match(s):
                found = lab
    return found


def main():
    os.makedirs(OUT, exist_ok=True)
    docs, unsigned = [], []
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".txt"):
            continue
        raw = open(os.path.join(SRC, fn)).read()
        body = strip_nav(raw)
        author = signature(body)
        # drop the heading block ("LETTER LXVI.", "TO THE PRINTER...", dateline)
        body = re.sub(r"(?m)^\s*LETTER\s+[IVXLC]+\.\s*$", " ", body)
        body = re.sub(r"(?m)^\s*TO\s+[A-Z][A-Z ,.'\-]{4,60}\.?\s*$", " ", body)
        body = DATELINE.sub(" ", body)
        body = fix_dropcaps(body)
        body = re.sub(r"\s+", " ", body).strip()
        n = len(body.split())
        if author is None:
            unsigned.append((fn, n))
            continue
        docs.append(dict(author=author, source="junius_1772_wikisource",
                         letter=fn[:-4], genre="public_letter",
                         n_words=n, text=body))
    with open(os.path.join(OUT, "junius_1772_wikisource.jsonl"), "w") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")
    c, w = Counter(), Counter()
    for d in docs:
        c[d["author"]] += 1
        w[d["author"]] += d["n_words"]
    print(f"{len(docs)} signed letters, {len(unsigned)} unsigned/unrecognised\n")
    for a, n in c.most_common():
        print(f"  {a:18s} {n:3d} letters {w[a]:7d} words")
    if unsigned:
        print("\nunsigned (excluded):")
        for fn, n in unsigned:
            print(f"  {fn:42s} {n:6d} words")


if __name__ == "__main__":
    main()
