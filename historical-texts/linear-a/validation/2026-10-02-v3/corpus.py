#!/usr/bin/env python3
"""
2026-10-02 VALIDATOR-3 (refuter) corpus layer for the Linear A
"labour-control / obligation-circuit / Scribe-9 dossier" claim.

Independent of the claimant's analysis/*.csv and analysis/*.md.

witness A : mwenge/lineara.xyz  LinearAInscriptions.js   (GORILA via G. Douros;
            carries numerals, scribe, findspot, support, context metadata)
witness B : SigLA (Salgarella & Castellan) per-document "word view" pages

Both vendored under ./data (copied from the 2026-09-25 session's vendored data so
this directory is self-contained; nothing is read from that directory at runtime).

`fetch` re-downloads; `run` works fully offline.
"""
import json, os, re, html, sys, urllib.request, urllib.parse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
A_URL = "https://raw.githubusercontent.com/mwenge/lineara.xyz/master/LinearAInscriptions.js"
SIGLA = "https://sigla.phis.me/document/{}/index-word.html"
SIGLA_DOCS = ["HT 85a","HT 85b","HT 87","HT 88","HT 94a","HT 94b",
              "HT 117a","HT 117b","HT 119","HT 122a","HT 122b"]

DIVIDER = "\U00010101"          # AEGEAN WORD SEPARATOR DOT
DIVIDER_LINE = "\U00010100"     # AEGEAN WORD SEPARATOR LINE
LACUNA = "\U0001076b"           # unassigned codepoint used by this corpus as the
                                # damage / lacuna / illegible marker
TOTALS = ("KU-RO", "PO-TO-KU-RO")

NUM = re.compile(r'^[\d\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079\u2070'
                 r'\u2044\u2080-\u2089/\u2248\s\.\-]+$')

IDEO = re.compile(r'^(GRA|VIN|OLE|OLIV|CYP|FIC|VIR|MUL|BOS|OVIS|CAP|SUS|AROM|TELA|'
                  r'HORD|QAPA|double|mina|\*\d)')


def fetch():
    os.makedirs(DATA, exist_ok=True)
    def get(u, p):
        req = urllib.request.Request(u, headers={"User-Agent": "cracking-problems-hub/validator3"})
        with urllib.request.urlopen(req, timeout=180) as r:
            open(p, "wb").write(r.read())
        print("ok", p)
    get(A_URL, os.path.join(DATA, "LinearAInscriptions.js"))
    for d in SIGLA_DOCS:
        get(SIGLA.format(urllib.parse.quote(d)),
            os.path.join(DATA, "sigla_" + d.replace(" ", "_") + ".html"))


def load_a():
    s = open(os.path.join(DATA, "LinearAInscriptions.js"), encoding="utf-8").read()
    start = s.index("new Map(") + len("new Map(")
    end = s.index("]);", start) + 1
    body = s[start:end]
    body = re.sub(r',(\s*[\]\}])', r'\1', body)
    body = re.sub(r'\\u\{([0-9a-fA-F]+)\}', lambda m: chr(int(m.group(1), 16)), body)
    return dict(json.loads(body))


def load_b():
    out = {}
    for d in SIGLA_DOCS:
        p = os.path.join(DATA, "sigla_" + d.replace(" ", "_") + ".html")
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        txt = html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', s)))
        seqs = re.findall(r'Sequence #\d+(.*?)\(\d+ signs?\)', txt)
        out[d] = [re.sub(r'\s+', '', x) for x in seqs]
    return out


# ------------------------------------------------------------------ predicates
def is_num(t):
    return bool(t) and bool(NUM.match(t)) and any(
        c.isdigit() or c in "\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079\u2070\u2044"
        for c in t)


def to_val(t):
    """Strict integer value, else None. Fractions/approximations deliberately
    excluded so no attack depends on a fraction convention."""
    t = (t or "").strip()
    return float(t) if re.fullmatch(r'\d+', t) else None


def is_word(t):
    if t in ("\n", DIVIDER, DIVIDER_LINE, LACUNA, "\u2014", "", " "):
        return False
    if is_num(t):
        return False
    if IDEO.match(t):
        return False
    if t.startswith("*") or t.startswith(LACUNA):
        return False
    return True


def base(name):
    m = re.match(r'^(HT\d+)', name)
    return m.group(1) if m else re.sub(r'[ab]$', '', name)


def damaged(v):
    """Does this face carry any lacuna/illegibility marker in the raw transcription?"""
    blob = (v.get("transcription") or "") + "".join(v.get("words") or [])
    return LACUNA in blob


def n_lacunae(v):
    blob = (v.get("transcription") or "")
    return blob.count(LACUNA)


def ht_tablet_faces(A):
    """Haghia Triada clay tablets carrying at least one syllabic sign-group."""
    return {k: v for k, v in A.items()
            if v.get("site") == "Haghia Triada" and v.get("support") == "Tablet"
            and any(is_word(w) for w in v["transliteratedWords"])}


def all_faces_with_words(A):
    return {k: v for k, v in A.items() if any(is_word(w) for w in v["transliteratedWords"])}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        fetch()
    else:
        A = load_a()
        print("documents:", len(A))
        print("HT tablet faces:", len(ht_tablet_faces(A)))
