"""Loading, canonicalisation and relabelling-invariant comparison of Dorabella
readings.

Under a monoalphabetic assumption the only cryptanalytically meaningful content
of a reading is its *partition*: which positions carry the same symbol. Two
readings that disagree only about which letter-name to give a symbol are the
same reading. So every comparison here is done on the equality relation
1[x_i == x_j], never on the letter names.
"""
import json, os, itertools
import numpy as np

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'transcriptions.json')


def load():
    with open(DATA) as fh:
        d = json.load(fh)
    for t in d['transcriptions']:
        t['text'] = ''.join(t['lines'])
        t['n'] = len(t['text'])
    return d


def canonical(s):
    """Relabel by order of first occurrence: the canonical name of a partition."""
    seen, out = {}, []
    for ch in s:
        if ch not in seen:
            seen[ch] = chr(ord('A') + len(seen))
        out.append(seen[ch])
    return ''.join(out)


def eq_matrix(s):
    a = np.frombuffer(s.encode(), dtype=np.uint8)
    return a[:, None] == a[None, :]


def pair_agreement(x, y):
    """Fraction of position-pairs on which two readings agree about equality,
    plus the two asymmetric error types."""
    assert len(x) == len(y)
    ex, ey = eq_matrix(x), eq_matrix(y)
    iu = np.triu_indices(len(x), k=1)
    a, b = ex[iu], ey[iu]
    return {
        'agree': float((a == b).mean()),
        'n_pairs': int(len(a)),
        'split_by_y': int((a & ~b).sum(),),   # same in x, different in y
        'merged_by_y': int((~a & b).sum()),   # different in x, same in y
    }


def stats(s):
    n = len(s)
    arr = np.frombuffer(s.encode(), dtype=np.uint8)
    _, counts = np.unique(arr, return_counts=True)
    counts = counts.astype(np.float64)
    ic = float((counts * (counts - 1)).sum() / (n * (n - 1)))
    doubles = int((arr[1:] == arr[:-1]).sum())
    bigrams = [s[i:i + 2] for i in range(n - 1)]
    trigrams = [s[i:i + 3] for i in range(n - 2)]
    rep_bi = sum(1 for g in set(bigrams) if bigrams.count(g) > 1)
    rep_tri = sum(1 for g in set(trigrams) if trigrams.count(g) > 1)
    longest = 0
    for L in range(3, n // 2 + 1):
        grams = [s[i:i + L] for i in range(n - L + 1)]
        if len(set(grams)) < len(grams):
            longest = L
        else:
            break
    p = counts / n
    entropy = float(-(p * np.log2(p)).sum())
    return {
        'n': n, 'distinct': int(len(counts)), 'ic': ic, 'entropy_bits': entropy,
        'doubles': doubles, 'repeated_bigram_types': rep_bi,
        'repeated_trigram_types': rep_tri, 'longest_repeat': longest,
        'hapax': int((counts == 1).sum()), 'max_symbol_count': int(counts.max()),
    }


def consensus(texts):
    """Majority vote on the equality relation, then the finest partition that
    respects every majority 'same' vote (union-find transitive closure).
    Returns the consensus string plus the count of majority 'different' votes
    that the closure was forced to override."""
    n = len(texts[0])
    votes = np.zeros((n, n), dtype=np.int32)
    for t in texts:
        votes += eq_matrix(t).astype(np.int32)
    maj = votes * 2 > len(texts)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            if maj[i, j]:
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[max(ri, rj)] = min(ri, rj)
    labels = [find(i) for i in range(n)]
    forced = int(sum(1 for i in range(n) for j in range(i + 1, n)
                     if not maj[i, j] and labels[i] == labels[j]))
    return canonical(''.join(chr(ord('A') + labels[i] % 26) if labels[i] < 26
                             else chr(ord('a') + labels[i] - 26) for i in range(n))), forced
