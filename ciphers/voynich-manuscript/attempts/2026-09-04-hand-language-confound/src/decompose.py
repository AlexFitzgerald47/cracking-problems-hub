"""Separating language, scribal hand and manuscript section.

The A/B "language" distinction is confounded twice over: Hand 1 wrote almost all
of Language A, and Language A is almost all Herbal. The ZL metadata carries all
three variables ($L language, $H hand, $I illustration/section type), and the
cell structure contains enough overlap to hold two constant while varying the
third:

  language, section held  A/Hand1/Herbal  vs  B/Hand2/Herbal      (hand varies)
  hand, both held         B/Hand2/Herbal  vs  B/Hand3|5/Herbal    (pure scribe)
  section, both held      B/Hand2/Herbal  vs  B/Hand2/Biological  (pure section)
  language, both held     A/Hand3/Stars   vs  B/Hand3/Stars       (the golden cell)

Distances are between group centroids in z-scored character-bigram space
(Burrows-style). Each is given a permutation null: pool the two groups' blocks,
relabel at random, recompute the centroid distance. That says whether a distance
is larger than the internal variability of the material.
"""
import sys, os, json, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import vms
from confound import bigrams, BLOCK, TOP_K

SEED = 20260904 + 21
N_PERM = 5000
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'decompose_results.json')

CELLS = {
    'A/H1/Herbal':      ('A', '1', 'H'),
    'A/H1/Pharma':      ('A', '1', 'P'),
    'A/H3/Stars':       ('A', '3', 'S'),
    'B/H2/Herbal':      ('B', '2', 'H'),
    'B/H2/Biological':  ('B', '2', 'B'),
    'B/H3/Herbal':      ('B', '3', 'H'),
    'B/H3/Stars':       ('B', '3', 'S'),
    'B/H5/Herbal':      ('B', '5', 'H'),
}

COMPARISONS = [
    ('language (section held, hand varies)', 'A/H1/Herbal', 'B/H2/Herbal'),
    ('LANGUAGE (hand and section held)',     'A/H3/Stars',  'B/H3/Stars'),
    ('hand only (language, section held)',   'B/H2/Herbal', 'B/H3/Herbal'),
    ('hand only (language, section held)',   'B/H2/Herbal', 'B/H5/Herbal'),
    ('hand only (language, section held)',   'B/H3/Herbal', 'B/H5/Herbal'),
    ('section only (language, hand held)',   'B/H2/Herbal', 'B/H2/Biological'),
    ('section only (language, hand held)',   'B/H3/Herbal', 'B/H3/Stars'),
    ('section only (language, hand held)',   'A/H1/Herbal', 'A/H1/Pharma'),
]


def cell_blocks(pages, lang, hand, sec, size=BLOCK):
    words = []
    for p in sorted(pages.values(), key=lambda x: x['page']):
        if p['lang'] == lang and p['hand'] == hand and p['attrs'].get('I') == sec:
            words.extend(p['words'])
    return [words[i:i + size] for i in range(0, len(words) - size + 1, size)]


def main():
    rng = np.random.default_rng(SEED)
    pages = vms.load()
    groups = {k: cell_blocks(pages, *v) for k, v in CELLS.items()}

    total = collections.Counter()
    for blks in groups.values():
        for b in blks:
            total += bigrams(b)
    feats = [g for g, _ in total.most_common(TOP_K)]

    vecs = {}
    for name, blks in groups.items():
        rows = []
        for b in blks:
            c = bigrams(b)
            n = sum(c.values()) or 1
            rows.append([c[f] / n for f in feats])
        vecs[name] = np.array(rows) if rows else np.zeros((0, len(feats)))

    allX = np.vstack([v for v in vecs.values() if len(v)])
    mu, sd = allX.mean(0), allX.std(0)
    sd[sd == 0] = 1
    Z = {k: (v - mu) / sd for k, v in vecs.items() if len(v)}

    res = {'seed': SEED, 'block_words': BLOCK, 'top_k_bigrams': TOP_K,
           'cell_blocks': {k: int(len(v)) for k, v in groups.items()},
           'cell_words': {k: int(sum(len(b) for b in v)) for k, v in groups.items()},
           'comparisons': []}

    for label, a, b in COMPARISONS:
        if a not in Z or b not in Z or len(Z[a]) < 2 or len(Z[b]) < 1:
            continue
        A, B = Z[a], Z[b]
        obs = float(np.linalg.norm(A.mean(0) - B.mean(0)))
        pool = np.vstack([A, B])
        na = len(A)
        null = np.empty(N_PERM)
        for i in range(N_PERM):
            idx = rng.permutation(len(pool))
            null[i] = np.linalg.norm(pool[idx[:na]].mean(0) - pool[idx[na:]].mean(0))
        res['comparisons'].append({
            'kind': label, 'a': a, 'b': b,
            'n_a': int(na), 'n_b': int(len(B)),
            'distance': obs,
            'null_mean': float(null.mean()), 'null_sd': float(null.std(ddof=1)),
            'p_value': float((null >= obs).mean()),
            'ratio_to_null': obs / float(null.mean()),
        })

    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)

    print('blocks per cell:', res['cell_blocks'])
    print()
    print('%-38s %-15s %-16s %5s %5s %8s %8s %6s'
          % ('effect', 'group A', 'group B', 'nA', 'nB', 'distance', 'null', 'p'))
    for c in res['comparisons']:
        print('%-38s %-15s %-16s %5d %5d %8.2f %8.2f %6.4f'
              % (c['kind'], c['a'], c['b'], c['n_a'], c['n_b'],
                 c['distance'], c['null_mean'], c['p_value']))


if __name__ == '__main__':
    main()
