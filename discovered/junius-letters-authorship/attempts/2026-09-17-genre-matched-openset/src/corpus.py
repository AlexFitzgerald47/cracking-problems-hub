#!/usr/bin/env python3
"""Shared corpus utilities: tokenisation, OCR normalisation, generic chunking.

The chunker is deliberately generic and is applied IDENTICALLY to every volume,
including the candidate's. A per-letter segmenter exists for *The Francis Letters*
and for the Junius editions because those are the two corpora whose internal
authorship structure we have to resolve; but if Francis's samples were hand-cleaned
while the rivals' were machine-chunked, Francis would win on pipeline quality rather
than on style. Every open-set comparison therefore runs on chunker output for all
authors, the candidate included.
"""
import json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "data", "raw")
CORPUS = os.path.join(HERE, "..", "data", "corpus")

# ---------------------------------------------------------------- normalisation

# Long-s (ſ) is OCR'd as 'f' in eighteenth-century founts. We cannot undo that
# reliably, so instead we *measure* it: SUSPECT_LONG_S counts tokens that look like
# long-s damage, and the rate is reported per source so the reader can see which
# corpora are comparable.
SUSPECT_LONG_S = re.compile(
    r"\b(?:fhall|fhould|fuch|fame|fome|thefe|thofe|houfe|caufe|becaufe|"
    r"prefent|againft|muft|firft|moft|juft|laft|pafs|perfon|reafon|fenfe|"
    r"confider|neceffary|poffible|fervice|fubject|fufficient)\b")

TOKEN = re.compile(r"[a-z]+(?:'[a-z]+)?")


def normalise(text):
    text = text.lower()
    text = text.replace("—", " ").replace("–", " ")
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    # join words broken across an OCR line end: "consi- deration"
    text = re.sub(r"([a-z])-\s+([a-z])", r"\1\2", text)
    return text


def tokens(text):
    return TOKEN.findall(normalise(text))


def long_s_rate(text):
    toks = tokens(text)
    if not toks:
        return 0.0
    return len(SUSPECT_LONG_S.findall(" " + " ".join(toks) + " ")) / len(toks)


# ---------------------------------------------------------------- apparatus filter

# Lines that are library plates, running heads, page numbers, footnote bodies,
# index entries or catalogue matter. Deliberately conservative: it is better to drop
# a little real prose than to admit an editor's nineteenth-century voice into an
# eighteenth-century author's sample.
def is_apparatus(line):
    s = line.strip()
    if not s:
        return True
    if len(s) < 3:
        return True
    letters = sum(c.isalpha() for c in s)
    if letters < 0.55 * len(s):          # tables, page-number runs, catalogue rows
        return True
    if re.fullmatch(r"[^a-z]*", s):      # all-caps / no lowercase: heading or plate
        return True
    up = sum(c.isupper() for c in s if c.isalpha())
    if letters and up / letters > 0.45:
        return True
    if re.match(r"^\s*\d", s) and len(s) < 90:
        return True
    if re.match(r"^\s*[*†‡]", s):
        return True
    return False


BOILERPLATE = re.compile(
    r"digitized by|internet archive|google book|public domain|university library|"
    r"printed by|entered according to act|all rights reserved|this book is|"
    r"transcriber's note|project gutenberg", re.I)


GUT_START = re.compile(r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.S)
GUT_END = re.compile(r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK", re.S)


def strip_gutenberg(text):
    """Remove the Gutenberg licence wrapper. Gutenberg e-texts are hand-proofread, so
    unlike the archive.org OCR they need no head/tail fraction trim -- only the
    licence block, which is modern English and would otherwise pollute every profile."""
    m = GUT_START.search(text)
    if m:
        text = text[m.end():]
    m = GUT_END.search(text)
    if m:
        text = text[:m.start()]
    return text


def clean_volume(text, head_frac=0.06, tail_frac=0.04):
    """Drop front matter, back matter and per-line apparatus from a whole-volume OCR."""
    if "PROJECT GUTENBERG" in text[:3000] or "Project Gutenberg" in text[:3000]:
        text = strip_gutenberg(text)
        head_frac, tail_frac = 0.02, 0.01
    lines = text.split("\n")
    n = len(lines)
    lines = lines[int(n * head_frac): int(n * (1 - tail_frac))]
    keep = [l.strip() for l in lines
            if not is_apparatus(l) and not BOILERPLATE.search(l)]
    return re.sub(r"\s+", " ", " ".join(keep))


def chunk(text, size=2000):
    """Fixed-length word chunks. Trailing remainder shorter than size is discarded so
    that every document in every panel has exactly the same length -- Delta is
    length-sensitive and unequal samples silently favour the longer author."""
    w = text.split()
    return [" ".join(w[i:i + size]) for i in range(0, len(w) - size + 1, size)]


# ---------------------------------------------------------------- feature vectors

def freq_profile(toks, vocab):
    c = Counter(toks)
    n = len(toks) or 1
    return [c[w] / n for w in vocab]


def mfw(doc_tokens, k=200, exclude=()):
    """Most frequent words across the pooled corpus, excluding a stop list.

    Content words carry topic, and topic is the confound that makes polemical letters
    about Lord Granby look unlike private letters about a daughter's marriage. The
    exclude list is where proper nouns and period-topic words are removed.
    """
    c = Counter()
    for t in doc_tokens:
        c.update(t)
    out = []
    for w, _ in c.most_common():
        if w in exclude:
            continue
        out.append(w)
        if len(out) >= k:
            break
    return out


def delta(profiles, target, mu, sd):
    """Burrows's Delta: mean absolute difference of z-scores."""
    z_t = [(target[i] - mu[i]) / sd[i] for i in range(len(mu))]
    out = []
    for p in profiles:
        z_p = [(p[i] - mu[i]) / sd[i] for i in range(len(mu))]
        out.append(sum(abs(a - b) for a, b in zip(z_t, z_p)) / len(mu))
    return out


def load_jsonl(name):
    path = os.path.join(CORPUS, name)
    with open(path) as f:
        return [json.loads(l) for l in f]
