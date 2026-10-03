#!/usr/bin/env python3
"""
2026-10-03 VALIDATOR 3 (refuter), second pass — shared helpers.

Written independently of corpus.py's analytical predicates; only the raw-file
JSON extraction is shared in spirit (both just parse the vendored witness).
Nothing here reads the claimant's analysis/ files except attack_r4, which
audits them as the object under test.
"""
import json, os, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DIV   = "\U00010101"   # AEGEAN WORD SEPARATOR DOT
DIVL  = "\U00010100"   # AEGEAN WORD SEPARATOR LINE
LAC   = "\U0001076b"   # damage / illegible marker used by this corpus
TOTALS = ("KU-RO", "PO-TO-KU-RO")

# administrative operators / commodity classifiers that are not personal
# designations.  Frozen here before any result is looked at.
OPERATORS = {"KU-RO", "PO-TO-KU-RO", "KI-RO", "A-DU", "KU-DA", "KA-PA",
             "SA-RA\u2082", "MA-KA-RI-TE", "U-MI-NA-SI", "KI-KI-RA-JA",
             "DA-DU-MA-TA", "SA-TA", "A-KA-RU", "KA-RU"}

IDEO = re.compile(r'^(GRA|VIN|OLE|OLIV|CYP|FIC|VIR|MUL|BOS|OVIS|CAP|SUS|AROM|'
                  r'TELA|HORD|QAPA|double|mina|\*\d)')
NUMTOK = re.compile(r'^\d+$')


def load(snapshot="data"):
    p = os.path.join(HERE, snapshot, "LinearAInscriptions.js")
    s = open(p, encoding="utf-8").read()
    start = s.index("new Map(") + len("new Map(")
    end = s.index("]);", start) + 1
    body = re.sub(r',(\s*[\]\}])', r'\1', s[start:end])
    body = re.sub(r'\\u\{([0-9a-fA-F]+)\}', lambda m: chr(int(m.group(1), 16)), body)
    return dict(json.loads(body))


def is_sign_group(t):
    """A syllabic sign-group: not a numeral, divider, newline, damage marker,
    ideogram or starred-only sign."""
    if t in ("\n", DIV, DIVL, LAC, "", " ", "\u2014"):
        return False
    if re.fullmatch(r'[\d\s./\u00b9\u00b2\u00b3\u2074-\u2079\u2070\u2044\u2080-\u2089\u2248\-]+', t):
        return False
    if IDEO.match(t) or t.startswith("*") or t.startswith(LAC) or t.startswith("[["):
        return False
    return True


def is_name(t):
    """A multi-sign designation that is not an administrative operator.
    Single syllabograms are excluded: the board's own 2026-09-25 rule is that
    in an administrative corpus the shortest units cannot be separated from
    abbreviations."""
    return is_sign_group(t) and t not in OPERATORS and "-" in t


def tablet(face):
    m = re.match(r'^(HT\d+(?:\+\d+)?)', face)
    return m.group(1) if m else re.sub(r'[ab]$', '', face)


def ht_tablet_faces(A):
    return {k: v for k, v in A.items()
            if v.get("site") == "Haghia Triada" and v.get("support") == "Tablet"
            and any(is_sign_group(w) for w in v["transliteratedWords"])}


def ht_tablets(A):
    """tablet-id -> list of faces"""
    out = collections.defaultdict(list)
    for k, v in ht_tablet_faces(A).items():
        out[tablet(k)].append(k)
    return dict(out)


def types_on(A, faces):
    s = set()
    for f in faces:
        for w in A[f]["transliteratedWords"]:
            if is_sign_group(w):
                s.add(w)
    return s


def names_on(A, faces):
    return {w for f in faces for w in A[f]["transliteratedWords"] if is_name(w)}


def entries(A, face):
    """(sign-group, integer amount) pairs: a sign-group immediately followed by
    an integer numeral, newlines and dividers skipped."""
    ws = [w for w in A[face]["transliteratedWords"] if w not in ("\n",)]
    out = []
    for i, w in enumerate(ws):
        if is_sign_group(w):
            for j in range(i + 1, min(i + 3, len(ws))):
                if NUMTOK.fullmatch(ws[j]):
                    out.append((w, int(ws[j])))
                    break
                if is_sign_group(ws[j]) or ws[j] in (DIV, DIVL):
                    break
    return out


def amounts(A, face):
    """All bare integer numerals on a face, in order."""
    return [int(w) for w in A[face]["transliteratedWords"] if NUMTOK.fullmatch(w)]


def stated_totals(A, face):
    ws = A[face]["transliteratedWords"]
    out = []
    for i, w in enumerate(ws):
        if w in TOTALS:
            for j in range(i + 1, min(i + 4, len(ws))):
                if NUMTOK.fullmatch(ws[j]):
                    out.append((w, int(ws[j])))
                    break
                if is_sign_group(ws[j]):
                    break
    return out


DOSSIER = ["HT85", "HT87", "HT94", "HT112", "HT117", "HT119",
           "HT122", "HT128", "HT132", "HT135"]
