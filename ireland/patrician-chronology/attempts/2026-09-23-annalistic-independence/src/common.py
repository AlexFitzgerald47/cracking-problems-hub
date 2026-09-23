"""Shared loading / normalisation for the Patrician independence attempt.

Input is `entries.jsonl` as produced by
  ireland/early-irish-annals-reliability/attempts/2026-09-23-iona-transition/src/parse.py
(that parser is re-used unchanged; this attempt reproduced its committed
`entries_derived.csv` byte-for-byte before building anything on top of it).
"""
import json, re, math, collections, unicodedata

WITNESSES = ("AU", "AT", "CS", "AI")

# Chronological apparatus and high-frequency annalistic scaffolding.  These are
# removed before similarity scoring because they are shared by every entry and
# would manufacture matches between unrelated notices.
APPARATUS = set("""
kalends kalend kl kalendae calends january jan feria epact luna moon year years
age anno annus the a an of in on at to and or is was were be been by for from with
that this these those it its he she his her they them their who whom which what
i ii iii iv v vi vii viii ix x xi xii xiii xiv xv xvi xvii xviii xix xx
first second third fourth fifth sixth seventh eighth ninth tenth
one two three four five six seven eight nine ten eleven twelve twenty thirty forty fifty
sixty seventy eighty ninety hundred thousand
""".split())

TOKEN_RE = re.compile(r"[a-zà-ɏ]+")


def load(path):
    return [json.loads(l) for l in open(path, encoding="utf-8")]


def norm_tokens(text):
    t = unicodedata.normalize("NFKD", text.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    toks = TOKEN_RE.findall(t)
    return [w for w in toks if len(w) > 2 and w not in APPARATUS]


def idf(entries):
    df = collections.Counter()
    for e in entries:
        df.update(set(norm_tokens(e["text"])))
    n = len(entries)
    return {w: math.log(n / (1.0 + c)) for w, c in df.items()}


def vec(text, idfmap):
    toks = norm_tokens(text)
    v = collections.Counter()
    for w in set(toks):
        v[w] = idfmap.get(w, math.log(1000.0))
    nrm = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {w: x / nrm for w, x in v.items()}


def cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(w, 0.0) for w, x in a.items())
