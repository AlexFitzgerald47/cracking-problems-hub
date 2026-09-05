"""Burrows's Delta, and the measurements that say what it can resolve.

Delta: represent each text by the relative frequencies of the K commonest words,
z-score each feature using the training set only (not the whole corpus - that
leaks the test text into its own scaling), and attribute a text to the author
whose centroid is closest in Manhattan distance.

Everything here is a calibration rather than an attribution. The question is not
who wrote a given play but how much material, of what kind, Delta needs before
its verdict carries any information at all.
"""
import sys, os, json, collections, random
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import corpus

SEED = 20260905
TOP_K = 500


def vocabulary(plays, k=TOP_K):
    c = collections.Counter()
    for p in plays:
        c.update(p['words'])
    return [w for w, _ in c.most_common(k)]


def vectors(plays, vocab, limit=None):
    """Relative frequency of each vocabulary word, per play."""
    index = {w: i for i, w in enumerate(vocab)}
    X = np.zeros((len(plays), len(vocab)))
    for r, p in enumerate(plays):
        words = p['words'][:limit] if limit else p['words']
        c = collections.Counter(words)
        n = len(words) or 1
        for w, cnt in c.items():
            j = index.get(w)
            if j is not None:
                X[r, j] = cnt / n
    return X


def attribute(Xtrain, ytrain, Xtest):
    """Classic Delta: z-score on training statistics, nearest author centroid
    by Manhattan distance."""
    mu, sd = Xtrain.mean(0), Xtrain.std(0)
    sd[sd == 0] = 1
    Ztr, Zte = (Xtrain - mu) / sd, (Xtest - mu) / sd
    authors = sorted(set(ytrain))
    cent = np.stack([Ztr[ytrain == a].mean(0) for a in authors])
    d = np.abs(Zte[:, None, :] - cent[None, :, :]).sum(2)
    return [authors[i] for i in d.argmin(1)]


def loo(plays, X, y, mask_fn=None):
    """Leave-one-play-out attribution. `mask_fn(i)` may exclude further training
    plays for test play i - used for the period-confound experiment."""
    correct, total, results = 0, 0, []
    for i in range(len(plays)):
        keep = np.ones(len(plays), bool)
        keep[i] = False
        if mask_fn is not None:
            keep &= mask_fn(i)
        if len(set(y[keep])) < 2 or (y[keep] == y[i]).sum() < 1:
            continue
        pred = attribute(X[keep], y[keep], X[i:i + 1])[0]
        ok = pred == y[i]
        correct += ok
        total += 1
        results.append({'play': plays[i]['slug'], 'true': y[i], 'pred': pred, 'ok': bool(ok)})
    return correct / total if total else float('nan'), total, results
