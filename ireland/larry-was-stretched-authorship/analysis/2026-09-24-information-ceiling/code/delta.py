#!/usr/bin/env python3
"""Burrows's Delta and Cosine Delta, plus leave-one-out attribution harness.

Delta (Burrows 2002): z-score the relative frequencies of the N most frequent
words across the reference set, then take the mean absolute difference between
a questioned document's z-vector and each candidate author profile.
Cosine Delta (Smith & Aldridge 2011 / Evert et al. 2017) uses cosine distance
on the same z-vectors and is the stronger variant on small samples.
"""
import re, math, random
from collections import Counter

WORD = re.compile(r"[a-z][a-z'’]*")

def tokens(text):
    t = text.lower().replace('’', "'")
    return WORD.findall(t)

def mfw_list(docs, n):
    """Most-frequent-word list over the pooled reference set."""
    c = Counter()
    for d in docs:
        c.update(tokens(d))
    return [w for w, _ in c.most_common(n)]

def freq_vec(text, mfw):
    tk = tokens(text)
    n = len(tk) or 1
    c = Counter(tk)
    return [c[w] / n for w in mfw]

def zscale(vecs):
    """Return (means, sds) computed over the supplied vectors."""
    k = len(vecs[0])
    means, sds = [], []
    for j in range(k):
        col = [v[j] for v in vecs]
        m = sum(col) / len(col)
        var = sum((x - m) ** 2 for x in col) / len(col)
        means.append(m)
        sds.append(math.sqrt(var) if var > 0 else 1e-12)
    return means, sds

def zvec(v, means, sds):
    return [(v[j] - means[j]) / sds[j] for j in range(len(v))]

def delta_burrows(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)

def delta_cosine(a, b):
    na = math.sqrt(sum(x * x for x in a)) or 1e-12
    nb = math.sqrt(sum(y * y for y in b)) or 1e-12
    return 1.0 - sum(x * y for x, y in zip(a, b)) / (na * nb)

DIST = {'burrows': delta_burrows, 'cosine': delta_cosine}

def attribute_loo(units, n_mfw=100, metric='cosine', min_units=2):
    """Leave-one-unit-out attribution.

    units: list of (author, text). For each unit, its author's profile is
    rebuilt from that author's OTHER units (so the held-out text never
    contributes to its own target), z-scaling is refit on the training
    units only, and the unit is assigned to the nearest author profile.

    Returns (n_tested, n_correct, per_case list, candidate_set_size).
    """
    from collections import defaultdict
    by_author = defaultdict(list)
    for a, t in units:
        by_author[a].append(t)
    authors = sorted(a for a in by_author if len(by_author[a]) >= min_units)
    cases = []
    for held_author in authors:
        for i in range(len(by_author[held_author])):
            test_text = by_author[held_author][i]
            train = {}
            for a in authors:
                texts = [t for j, t in enumerate(by_author[a])
                         if not (a == held_author and j == i)]
                if texts:
                    train[a] = '\n'.join(texts)
            if held_author not in train:
                continue
            mfw = mfw_list(list(train.values()), n_mfw)
            tr_vecs = [freq_vec(t, mfw) for t in train.values()]
            means, sds = zscale(tr_vecs)
            prof = {a: zvec(freq_vec(t, mfw), means, sds) for a, t in train.items()}
            q = zvec(freq_vec(test_text, mfw), means, sds)
            d = {a: DIST[metric](q, p) for a, p in prof.items()}
            pred = min(d, key=d.get)
            cases.append({'true': held_author, 'pred': pred,
                          'correct': pred == held_author,
                          'n_words': len(tokens(test_text)),
                          'dists': d})
    n = len(cases)
    k = len(set(c['true'] for c in cases))
    return n, sum(c['correct'] for c in cases), cases, k
