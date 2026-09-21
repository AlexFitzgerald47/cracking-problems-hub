#!/usr/bin/env python3
"""Shared loader for the 2026-09-21 shift-or-loss and damage tests.

Everything here reuses the 2026-09-17 corpus and tokeniser unchanged. The only new
machinery is (a) a feature-exclusion hook so a feature set can be refitted with a named
word list removed, and (b) a rank-matched random-exclusion null for that hook, so that
"removing these particular words changed the number" can be told apart from "removing
this many words changed the number".
"""
import os, sys, random
from collections import Counter, defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PRIOR = os.path.abspath(os.path.join(HERE, "..", "..", "2026-09-17-genre-matched-openset", "src"))
sys.path.insert(0, PRIOR)
import corpus as C
from funcwords import FUNCTION_WORDS
from delta import junius_chunks

N_FEATURES = 120
FORMAL = ("published_prose", "political_prose")
LETTERS = ("private_letter",)


def long_s_vulnerable(w):
    """True if an eighteenth-century fount would set a long s somewhere in this word.

    Long s is used initially and medially; round s only word-finally. So any word with
    an 's' at a position other than the last is a candidate for 's'->'f' OCR damage.
    'his', 'was', 'this', 'as' are safe; 'so', 'such', 'must', 'these' are not.
    """
    idx = [i for i, ch in enumerate(w) if ch == "s"]
    return any(i < len(w) - 1 for i in idx)


def load_docs():
    docs = list(C.load_jsonl("panel_chunks.jsonl")) + junius_chunks()
    fw = set(FUNCTION_WORDS)
    counts, tot = [], Counter()
    for d in docs:
        c = Counter(t for t in C.tokens(d["text"]) if t in fw)
        counts.append(c)
        tot.update(c)
    ranked = [w for w, _ in tot.most_common()]
    return docs, counts, ranked


def build_Z(counts, feats):
    X = np.zeros((len(counts), len(feats)))
    for i, c in enumerate(counts):
        s = sum(c.values()) or 1
        for j, w in enumerate(feats):
            X[i, j] = c[w] / s
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1e-12
    return (X - mu) / sd


def feats_excluding(ranked, excluded, n=N_FEATURES):
    """Top-n function words from the same ranked list, skipping `excluded`.

    Refitting to the SAME count matters: changing the dimensionality is itself a
    treatment that rescales every Delta, which is the trap recorded in
    board/log/2026-09-21-rescaled-metric-invalidates-margin.md.
    """
    out = [w for w in ranked if w not in excluded]
    return out[:n]


def rank_matched_null_exclusion(ranked, excluded, rng, pool_limit=400):
    """Pick a same-sized exclusion set matched on frequency rank.

    The long-s-vulnerable function words are disproportionately high-frequency (so, such,
    should, some, these). Excluding an equal number of words drawn uniformly would skip
    rarer words on average and would be a weaker treatment for reasons that have nothing
    to do with long s. So each excluded word is replaced by a non-vulnerable word drawn
    from a widening band around its own rank.
    """
    rank = {w: i for i, w in enumerate(ranked[:pool_limit])}
    safe = [w for w in ranked[:pool_limit] if w not in excluded]
    chosen = set()
    for w in sorted(excluded, key=lambda w: rank.get(w, 10**6)):
        if w not in rank:
            continue
        r = rank[w]
        for band in (10, 25, 60, 150, pool_limit):
            cands = [x for x in safe if x not in chosen and abs(rank[x] - r) <= band]
            if cands:
                chosen.add(rng.choice(cands))
                break
    return chosen


def centroids(Z, idx_by_author, skip_idx=None):
    out = {}
    for a, v in idx_by_author.items():
        vv = [i for i in v if i != skip_idx] if skip_idx is not None else v
        if vv:
            out[a] = Z[vv].mean(0)
    return out


def delta_to(z, cents):
    return {a: float(np.abs(z - c).mean()) for a, c in cents.items()}


def author_genre_cells(docs, min_chunks=8):
    cells = defaultdict(list)
    for i, d in enumerate(docs):
        cells[(d["author"], d["genre"])].append(i)
    return {k: v for k, v in cells.items() if len(v) >= min_chunks}
