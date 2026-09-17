#!/usr/bin/env python3
"""Segment *The Francis Letters* (ed. Beata Francis & Eliza Keary, 1901) into
author-attributed, year-stamped private letters.

Why this volume and not a bibliography of "works by Philip Francis": a Philip Francis
author listing includes *A Complete Collection of Junius's Letters*, so scraping an
author bibliography puts the disputed target into the candidate's training set and
makes the attribution circular. Flagged by the 2026-09-05 session; respected here.

Why it is worth the parsing effort: the volumes are a FAMILY correspondence. In one
OCR pass of one edition they carry private letters by Sir Philip Francis (the
candidate), his father Dr Philip Francis, Edmund Burke, Alexander Mackrabie and
others. That is a source-matched rival panel in the private-letter genre -- edition,
scanner and OCR engine held constant across authors, which is the one confound a
cross-corpus attribution study otherwise cannot control.

Two OCR facts this parser depends on:
  * letters are headed by an all-caps "X TO Y." line; "THE SAME TO THE SAME" inherits
    the previous header;
  * every page carries a running head of the form "38 ftbe francis Xetters [1758" or
    "1758] ftbe Brands Xetters 37" (the gothic face OCRs as garbage but the bracketed
    year is reliable). These lines are interleaved into the body by the OCR. They are
    stripped, and the year is harvested from them before stripping.
"""
import json, os, re, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "data", "raw")
OUT = os.path.join(HERE, "..", "data", "corpus")

VOLUMES = ["francisletters01franuoft.txt", "francisletters02franuoft.txt"]

HEADER = re.compile(
    r"^[ \t]*((?:FROM[ \t]+)?[A-Z][A-Z0-9 .,'&;:()\-—]{6,74}?)[ \t]*\.?[ \t]*$", re.M)

# OCR mangles names (PHIUP for PHILIP, FKANCIS for FRANCIS); sender matching is loose
# and normalised to a canonical label.
SENDER_RULES = [
    (r"^(?:FROM\s+)?(?:THE\s+REV\.?\s+)?DR\.?\s+FRANCIS\b",        "Dr_Philip_Francis_sr"),
    (r"^(?:FROM\s+)?THE\s+REV\.?\s+PHILIP\s+FRANCIS,?\s+D\.?\s*D",  "Dr_Philip_Francis_sr"),
    (r"^(?:FROM\s+)?(?:SIR\s+)?PHI[LU]I?P\s+FRANCIS\b",             "Philip_Francis"),
    (r"^(?:FROM\s+)?EDMUND\s+BURKE\b",                              "Edmund_Burke"),
    (r"^(?:FROM\s+)?ALE[XK]ANDER\s+MACKRABIE\b",                    "Alexander_Mackrabie"),
    (r"^(?:FROM\s+)?ELIZABETH\s+MACKRABIE\b",                       "Elizabeth_Mackrabie"),
    (r"^(?:FROM\s+)?MRS\.?\s+FRANCIS\b",                            "Mrs_Francis"),
    (r"^(?:FROM\s+)?HARRIET\s+FRANCIS\b",                           "Harriet_Francis"),
    (r"^(?:FROM\s+)?ELIZA\s+FRANCIS\b",                             "Eliza_Francis"),
    (r"^(?:FROM\s+)?CATHERINE\s+FRANCIS\b",                         "Catherine_Francis"),
    (r"^(?:FROM\s+)?JOHN\s+BOURKE\b",                               "John_Bourke"),
    (r"^(?:FROM\s+)?RICHARD\s+TILGHMAN\b",                          "Richard_Tilghman"),
    (r"^(?:FROM\s+)?GODSCHALL\s+JOHNSON\b",                         "Godschall_Johnson"),
    (r"^(?:FROM\s+)?ELIZA\s+JOHNSON\b",                             "Eliza_Johnson"),
]
SENDER_RULES = [(re.compile(p), lab) for p, lab in SENDER_RULES]

RECIPIENT_ONLY = re.compile(r"^(?:FROM\s+[\w.]+,?\s+)?TO\s+", re.I)
SAME = re.compile(r"^THE\s+SAME\s+TO\b", re.I)

RUNHEAD_YEAR = re.compile(r"\[\s*(1[678]\d\d)|(1[678]\d\d)\s*\]")
BODY_YEAR = re.compile(r"\b(17[0-9]\d|18[0-2]\d)\b")


def classify(header):
    h = re.sub(r"\s+", " ", header).strip().rstrip(".")
    if RECIPIENT_ONLY.match(h):
        return None
    for pat, lab in SENDER_RULES:
        if pat.match(h):
            return lab
    return None


def clean(body):
    """Strip running heads, page numbers and footnote apparatus; harvest running-head years."""
    kept, years = [], []
    for line in body.split("\n"):
        s = line.strip()
        if not s:
            continue
        m = RUNHEAD_YEAR.search(s)
        if m and len(s) < 70:                       # page running head
            years.append(int(m.group(1) or m.group(2)))
            continue
        if re.fullmatch(r"\d{1,4}", s):             # bare page number
            continue
        if re.match(r"^\d{1,2}\s+[A-Z\"]", s) and len(s) < 90:   # numbered footnote
            continue
        if re.match(r"^\*\s", s):
            continue
        kept.append(s)
    t = re.sub(r"\s+", " ", " ".join(kept)).strip()
    return t, years


def main():
    os.makedirs(OUT, exist_ok=True)
    docs, skipped = [], Counter()
    for vol in VOLUMES:
        path = os.path.join(RAW, vol)
        if not os.path.exists(path):
            print(f"MISSING {vol}", file=sys.stderr)
            continue
        text = open(path, errors="replace").read()
        marks = [(m.start(), m.end(), m.group(1)) for m in HEADER.finditer(text)]
        marks = [m for m in marks if re.search(r"\bTO\b", m[2])]
        last_author, last_header = None, None
        for i, (s, e, hdr) in enumerate(marks):
            end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
            hdr_n = re.sub(r"\s+", " ", hdr).strip()
            if SAME.match(hdr_n):
                author, shown = last_author, f"{last_header} [THE SAME]"
            else:
                author, shown = classify(hdr_n), hdr_n
                if author:
                    last_author, last_header = author, hdr_n
            body, rh_years = clean(text[e:end])
            if author is None:
                skipped[hdr_n[:48]] += 1
                continue
            if len(body.split()) < 60:
                continue
            # year: prefer the running heads spanned by the letter, else a date in the
            # opening of the letter itself
            year = min(rh_years) if rh_years else None
            if year is None:
                m = BODY_YEAR.search(body[:400])
                year = int(m.group(1)) if m else None
            docs.append(dict(author=author, source=vol, header=shown, year=year,
                             genre="private_letter", n_words=len(body.split()), text=body))
    with open(os.path.join(OUT, "francis_letters.jsonl"), "w") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")

    c, w = Counter(), Counter()
    for d in docs:
        c[d["author"]] += 1
        w[d["author"]] += d["n_words"]
    print(f"{len(docs)} letters kept\n")
    print(f"{'author':26s} {'letters':>7s} {'words':>8s}  year range")
    for a, n in c.most_common():
        ys = [d["year"] for d in docs if d["author"] == a and d["year"]]
        rng = f"{min(ys)}-{max(ys)}" if ys else "?"
        print(f"  {a:26s} {n:4d} {w[a]:9d}  {rng}")
    print(f"\n{sum(skipped.values())} headers with no identified sender; top:")
    for h, n in skipped.most_common(10):
        print(f"  {n:3d}  {h}")


if __name__ == "__main__":
    main()
