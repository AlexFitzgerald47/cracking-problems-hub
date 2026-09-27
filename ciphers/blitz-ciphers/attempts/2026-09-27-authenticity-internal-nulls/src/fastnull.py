"""Vectorised within-line shuffle null for bigram-IC and doublet counts.

The null holds each line's symbol multiset fixed (so the page's unigram
distribution, its line lengths and its per-line composition are all preserved
exactly) and destroys only adjacency.  It is deliberately the tightest null that
still answers "is there structure beyond the unigram frequencies".
"""
import numpy as np


def pack(lines):
    """-> (padded int array, mask, n_symbols). Pad code is n_symbols."""
    vocab = sorted({t for l in lines for t in l})
    idx = {t: i for i, t in enumerate(vocab)}
    K = len(vocab)
    maxlen = max(len(l) for l in lines)
    X = np.full((len(lines), maxlen), K, dtype=np.int64)
    M = np.zeros((len(lines), maxlen), dtype=bool)
    for i, l in enumerate(lines):
        X[i, :len(l)] = [idx[t] for t in l]
        M[i, :len(l)] = True
    return X, M, K


def _stats(X, M, K):
    a, b = X[:, :-1], X[:, 1:]
    v = M[:, :-1] & M[:, 1:]
    n = int(v.sum())
    codes = (a * (K + 1) + b)[v]
    cnt = np.bincount(codes, minlength=(K + 1) * (K + 1))
    ic = float((cnt * (cnt - 1)).sum()) / (n * (n - 1)) if n > 1 else float("nan")
    dbl = int(((a == b) & v).sum())
    return ic, dbl, n


def run(lines, nperm=20000, seed=0):
    X, M, K = pack(lines)
    rng = np.random.default_rng(seed)
    ic_o, db_o, nb = _stats(X, M, K)
    ics = np.empty(nperm)
    dbs = np.empty(nperm)
    rowlen = M.sum(1)
    for p in range(nperm):
        keys = rng.random(X.shape)
        keys[~M] = 2.0
        order = np.argsort(keys, axis=1, kind="stable")
        Xs = np.take_along_axis(X, order, axis=1)
        ics[p], dbs[p], _ = _stats(Xs, M, K)

    def summ(obs, v):
        m, sd = float(v.mean()), float(v.std(ddof=1))
        return dict(obs=float(obs), mean=m, sd=sd,
                    z=float((obs - m) / sd) if sd > 0 else float("nan"),
                    p_upper=float((int((v >= obs).sum()) + 1) / (nperm + 1)),
                    p_lower=float((int((v <= obs).sum()) + 1) / (nperm + 1)),
                    nperm=nperm)
    return dict(n_tokens=int(M.sum()), n_types=K, n_bigrams=nb,
                bigram=summ(ic_o, ics), doublet=summ(db_o, dbs),
                mean_line_len=float(rowlen.mean()))
