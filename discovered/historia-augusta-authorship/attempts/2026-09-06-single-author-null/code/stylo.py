"""Shared stylometric machinery: features, Burrows's Delta, split statistics.

Nothing here is HA-specific. Every experiment in this attempt calls into it so
that the Historia Augusta and the single-author control collections are
measured with exactly the same instrument.
"""

import json
import os
from collections import Counter

import numpy as np

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


def load():
    with open(os.path.join(DATA, "segments.json")) as fh:
        return json.load(fh)


def by_corpus(segs, name):
    return [s for s in segs if s["corpus"] == name]


def mfw_list(segs, n):
    """Most frequent words of a pooled reference corpus.

    The feature set is chosen from texts that are NOT under test, so that no
    experiment can pick features that flatter its own corpus.
    """
    c = Counter()
    for s in segs:
        c.update(s["tokens"])
    return [w for w, _ in c.most_common(n)]


def matrix(segs, words):
    """Relative frequencies of `words` in each segment (rows = segments)."""
    idx = {w: i for i, w in enumerate(words)}
    m = np.zeros((len(segs), len(words)))
    for r, s in enumerate(segs):
        c = Counter(s["tokens"])
        n = max(1, s["n_tokens"])
        for w, k in c.items():
            j = idx.get(w)
            if j is not None:
                m[r, j] = k / n
    return m


def zscore(m, mu=None, sd=None):
    if mu is None:
        mu = m.mean(axis=0)
    if sd is None:
        sd = m.std(axis=0)
    sd = np.where(sd == 0, 1.0, sd)
    return (m - mu) / sd


def delta_matrix(z):
    """Burrows's Delta: mean absolute difference of z-scores."""
    n = z.shape[0]
    d = np.zeros((n, n))
    for i in range(n):
        d[i] = np.abs(z - z[i]).mean(axis=1)
    return d


def group_separation(d, labels):
    """Standardised gap between cross-group and within-group distances.

    (mean between - mean within) / sd(all off-diagonal distances).
    Scale-free enough to compare across corpora of different sizes, but the
    experiments still self-normalise it against a permutation null.
    """
    labels = np.asarray(labels)
    n = len(labels)
    iu = np.triu_indices(n, 1)
    same = labels[iu[0]] == labels[iu[1]]
    vals = d[iu]
    if same.all() or (~same).all():
        return np.nan
    sd = vals.std()
    if sd == 0:
        return np.nan
    return (vals[~same].mean() - vals[same].mean()) / sd


def best_contiguous_split(d, min_group=3):
    """Largest separation achievable by cutting the sequence at one point.

    Rows of `d` must already be in the collection's transmitted order.
    Returns (statistic, split index k) where group A is rows [0, k).
    """
    n = d.shape[0]
    best, arg = -np.inf, None
    for k in range(min_group, n - min_group + 1):
        labels = np.array([0] * k + [1] * (n - k))
        s = group_separation(d, labels)
        if s is not None and not np.isnan(s) and s > best:
            best, arg = s, k
    return best, arg


def perm_null_split(d, n_perm, rng, min_group=3):
    """Null for `best_contiguous_split` under random reordering.

    Shuffling the order destroys any real sequential structure while keeping
    the texts, their lengths and their pairwise distances exactly as they are.
    """
    n = d.shape[0]
    out = np.empty(n_perm)
    for i in range(n_perm):
        p = rng.permutation(n)
        out[i] = best_contiguous_split(d[np.ix_(p, p)], min_group)[0]
    return out


def perm_null_labels(d, labels, n_perm, rng):
    labels = np.asarray(labels)
    out = np.empty(n_perm)
    for i in range(n_perm):
        out[i] = group_separation(d, rng.permutation(labels))
    return out


def z_against(obs, null):
    sd = null.std()
    return (obs - null.mean()) / (sd if sd else np.nan)


def chunk(seg, size):
    """Split a segment's token stream into non-overlapping blocks of `size`."""
    tk = seg["tokens"]
    return [tk[i:i + size] for i in range(0, len(tk) - size + 1, size)]
