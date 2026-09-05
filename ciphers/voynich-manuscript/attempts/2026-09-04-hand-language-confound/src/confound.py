"""Is Currier's A/B "language" distinction separable from the scribal hand?

The ZL transliteration's own metadata shows the two are almost perfectly
confounded: Hand 1 wrote 112 of the 114 Language A pages, and Language B is
written by Hands 2, 3, 5 and others. If that were the whole story, "two
languages" and "two scribes" would be indistinguishable claims.

One scribe breaks the confound. **Hand 3 wrote both** - 28 pages of B (10,907
words) and 2 pages of A (752 words). That permits the test that matters:

  language axis   trained on Hand 1 (A) vs Hand 2 (B) - fully confounded
  scribal axis    Hand 2 (B) vs Hand 3 (B) - same language, different scribe

If Hand 3's Language A text lands on the A side of the language axis, the A/B
difference survives holding the scribe constant, and is not merely scribal.

Unit of analysis is a fixed-size block of words rather than a page, so that
sample sizes are comparable. Hand-3-A yields only three blocks; that is the
binding limitation and it is reported rather than glossed.
"""
import sys, os, json, collections, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import vms

SEED = 20260904
BLOCK = 250          # words per block
TOP_K = 120          # character bigrams used as features
N_PERM = 20000
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'confound_results.json')


def blocks_for(pages, lang, hand, size=BLOCK):
    words = []
    for p in sorted(pages.values(), key=lambda x: x['page']):
        if p['lang'] == lang and p['hand'] == hand:
            words.extend(p['words'])
    return [words[i:i + size] for i in range(0, len(words) - size + 1, size)]


def bigrams(words):
    c = collections.Counter()
    for w in words:
        s = '^' + w + '$'
        for i in range(len(s) - 1):
            c[s[i:i + 2]] += 1
    return c


def feature_matrix(groups, top_k=TOP_K):
    total = collections.Counter()
    for blks in groups.values():
        for b in blks:
            total += bigrams(b)
    feats = [g for g, _ in total.most_common(top_k)]
    X, y = [], []
    for name, blks in groups.items():
        for b in blks:
            c = bigrams(b)
            n = sum(c.values()) or 1
            X.append([c[f] / n for f in feats])
            y.append(name)
    return np.array(X), np.array(y), feats


def main():
    rng = np.random.default_rng(SEED)
    pages = vms.load()

    groups = {
        'H1_A': blocks_for(pages, 'A', '1'),
        'H2_B': blocks_for(pages, 'B', '2'),
        'H3_B': blocks_for(pages, 'B', '3'),
        'H3_A': blocks_for(pages, 'A', '3'),
        'H5_B': blocks_for(pages, 'B', '5'),
    }
    counts = {k: len(v) for k, v in groups.items()}

    X, y, feats = feature_matrix(groups)
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1
    Z = (X - mu) / sd                      # Burrows-style z-scored features

    def cen(name):
        return Z[y == name].mean(0)

    # language axis: confounded A vs B (Hand 1 vs Hand 2)
    lang_axis = cen('H1_A') - cen('H2_B')
    lang_axis /= np.linalg.norm(lang_axis)
    # scribal axis: same language, different scribe
    hand_axis = cen('H2_B') - cen('H3_B')
    hand_axis /= np.linalg.norm(hand_axis)

    proj_l = {k: (Z[y == k] @ lang_axis) for k in groups}
    proj_h = {k: (Z[y == k] @ hand_axis) for k in groups}

    # midpoint of the training classes on the language axis
    mid = (proj_l['H1_A'].mean() + proj_l['H2_B'].mean()) / 2

    # Does Hand 3's Language A sit on the A side, relative to Hand 3's own B?
    a3, b3 = proj_l['H3_A'], proj_l['H3_B']
    # permutation test: pool H3 blocks, ask how often 3 random blocks reach
    # a mean projection as A-ward as the real Hand-3-A blocks
    pool = np.concatenate([a3, b3])
    obs = a3.mean()
    k = len(a3)
    perm = np.array([rng.permutation(pool)[:k].mean() for _ in range(N_PERM)])

    res = {
        'seed': SEED, 'block_words': BLOCK, 'top_k_bigrams': TOP_K,
        'block_counts': counts,
        'word_counts': {k: sum(len(b) for b in v) for k, v in groups.items()},
        'contingency_pages': {'%s|H%s' % (l, h): n
                              for (l, h), n in sorted(vms.contingency(pages).items())},
        'axis_alignment_cosine': float(lang_axis @ hand_axis),
        'language_axis_projection': {
            k: {'mean': float(v.mean()), 'sd': float(v.std(ddof=1)) if len(v) > 1 else None,
                'n': int(len(v)), 'values': [float(x) for x in v]}
            for k, v in proj_l.items()},
        'scribal_axis_projection': {
            k: {'mean': float(v.mean()), 'n': int(len(v))} for k, v in proj_h.items()},
        'training_midpoint': float(mid),
        'hand3_test': {
            'H3_A_mean_on_language_axis': float(obs),
            'H3_B_mean_on_language_axis': float(b3.mean()),
            'H1_A_mean': float(proj_l['H1_A'].mean()),
            'H2_B_mean': float(proj_l['H2_B'].mean()),
            'p_value_permutation_within_hand3': float((perm >= obs).mean()),
            'n_permutations': N_PERM,
            'n_A_blocks': int(k),
        },
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)

    print('blocks per group:', counts)
    print('words  per group:', res['word_counts'])
    print()
    print('cosine between the language axis and the pure scribal axis: %.3f'
          % res['axis_alignment_cosine'])
    print()
    print('projection onto the language axis (positive = towards Language A):')
    for k in ('H1_A', 'H2_B', 'H3_B', 'H5_B', 'H3_A'):
        v = proj_l[k]
        print('  %-6s n=%-3d mean %+7.3f  sd %s'
              % (k, len(v), v.mean(), ('%.3f' % v.std(ddof=1)) if len(v) > 1 else '  -'))
    print('  training midpoint: %+.3f' % mid)
    print()
    t = res['hand3_test']
    print('within Hand 3 (scribe held constant):')
    print('  Language A blocks: mean %+.3f (n=%d)' % (t['H3_A_mean_on_language_axis'], t['n_A_blocks']))
    print('  Language B blocks: mean %+.3f (n=%d)' % (t['H3_B_mean_on_language_axis'], len(b3)))
    print('  permutation p = %.5f' % t['p_value_permutation_within_hand3'])


if __name__ == '__main__':
    main()
