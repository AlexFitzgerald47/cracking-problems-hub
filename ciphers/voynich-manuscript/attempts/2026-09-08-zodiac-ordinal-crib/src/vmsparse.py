#!/usr/bin/env python3
"""Minimal IVTFF-style parser for the Takahashi transcription used by this attempt.

Locus header form:  <folio.LOCUSTYPE+NUM.LINENUM;TRANSCRIBER>
Takahashi ligature capitals are folded to standard lowercase EVA.
"""
import re, os, sys

LIG = [("cTh", "cth"), ("cKh", "ckh"), ("cPh", "cph"), ("cFh", "cfh"),
       ("Sh", "sh"), ("Th", "th"), ("Kh", "kh"), ("Ph", "ph"), ("Fh", "fh")]

HEADER = re.compile(r"^<(?P<folio>f[0-9]+[rv][0-9]?)\.(?P<ltype>[A-Za-z]+)(?P<lnum>[0-9]*)\.(?P<line>[0-9]+);(?P<who>[A-Z])>\s*(?P<text>.*)$")


def fold(s):
    for a, b in LIG:
        s = s.replace(a, b)
    return s


def clean_tokens(text):
    """Return list of EVA word tokens for one locus line."""
    t = fold(text)
    t = t.rstrip()
    t = re.sub(r"[=\-]+$", "", t)          # line/paragraph terminators
    t = t.replace("!", "").replace("%", "")  # uncertain-space fillers
    t = t.replace(",", ".")                  # uncertain word break -> break
    t = re.sub(r"<[^>]*>", "", t)            # inline comments
    words = [w for w in t.split(".") if w != ""]
    return words


def parse(path):
    rows = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            m = HEADER.match(raw.rstrip("\n"))
            if not m:
                continue
            d = m.groupdict()
            rows.append({
                "folio": d["folio"],
                "ltype": d["ltype"],
                "lnum": int(d["lnum"]) if d["lnum"] else 0,
                "line": int(d["line"]),
                "who": d["who"],
                "raw": d["text"].rstrip(),
                "words": clean_tokens(d["text"]),
            })
    return rows


if __name__ == "__main__":
    rows = parse(sys.argv[1])
    print(len(rows), "loci")
    from collections import Counter
    print(Counter(r["ltype"] for r in rows).most_common())
