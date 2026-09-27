"""Shared loading + feature machinery for the period-invariance attempt.

Reuses the 2026-09-05 cached corpus verbatim (data/corpus.json in that attempt's
folder) so results are directly comparable to the calibration they extend.
"""
import os, sys, json, collections
import numpy as np

CAL = os.path.join(os.path.dirname(__file__), '..', '..',
                   '2026-09-05-stylometry-calibration')
CACHE = os.path.join(CAL, 'data', 'corpus.json')
TOP_K = 500


def load():
    plays = json.load(open(CACHE))
    plays = [p for p in plays if p['year']]
    return plays


def vocabulary(plays, k=TOP_K, words_key='words'):
    c = collections.Counter()
    for p in plays:
        c.update(p[words_key])
    return [w for w, _ in c.most_common(k)]


def vectors(plays, vocab, words_key='words'):
    index = {w: i for i, w in enumerate(vocab)}
    X = np.zeros((len(plays), len(vocab)))
    for r, p in enumerate(plays):
        c = collections.Counter(p[words_key])
        n = len(p[words_key]) or 1
        for w, cnt in c.items():
            j = index.get(w)
            if j is not None:
                X[r, j] = cnt / n
    return X


def attribute(Xtr, ytr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1
    Ztr, Zte = (Xtr - mu) / sd, (Xte - mu) / sd
    authors = sorted(set(ytr))
    cent = np.stack([Ztr[ytr == a].mean(0) for a in authors])
    d = np.abs(Zte[:, None, :] - cent[None, :, :]).sum(2)
    return [authors[i] for i in d.argmin(1)]
