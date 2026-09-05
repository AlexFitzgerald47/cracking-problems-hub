"""Runs the calibration experiments and writes results/calibration.json."""
import sys, os, json, collections, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import corpus, delta

SEED = 20260905
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'calibration.json')


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    plays = corpus.load()
    y = np.array([p['author'] for p in plays])
    years = np.array([p['year'] or -1 for p in plays])
    vocab = delta.vocabulary(plays)
    X = delta.vectors(plays, vocab)

    res = {'seed': SEED, 'top_k_words': delta.TOP_K,
           'n_plays': len(plays), 'n_authors': len(set(y)),
           'plays_per_author': dict(collections.Counter(y.tolist()))}

    # --- 1. baseline accuracy, and the null it must beat ---------------------
    acc, n, results = delta.loo(plays, X, y)
    majority = max(collections.Counter(y.tolist()).values()) / len(y)
    null = []
    for _ in range(25):
        yp = rng.permutation(y)
        a, _, _ = delta.loo(plays, X, yp)
        null.append(a)
    res['baseline'] = {
        'accuracy': acc, 'n_tested': n,
        'chance_uniform': 1 / len(set(y)),
        'chance_majority_class': majority,
        'label_permutation_null_mean': float(np.mean(null)),
        'label_permutation_null_max': float(np.max(null)),
        'n_permutations': len(null),
    }
    res['errors'] = [r for r in results if not r['ok']]

    # --- 2. how many plays per author does it need? --------------------------
    curve = []
    for k in (1, 2, 3, 4, 5, 8):
        accs = []
        for rep in range(8):
            keep = np.zeros(len(plays), bool)
            for a in set(y):
                idx = np.where(y == a)[0]
                pick = rng.permutation(idx)[:k]
                keep[pick] = True
            ok = tot = 0
            for i in range(len(plays)):
                if keep[i]:
                    continue
                tr = keep.copy()
                if (y[tr] == y[i]).sum() < 1 or len(set(y[tr])) < 2:
                    continue
                pred = delta.attribute(X[tr], y[tr], X[i:i + 1])[0]
                ok += pred == y[i]
                tot += 1
            if tot:
                accs.append(ok / tot)
        curve.append({'train_plays_per_author': k,
                      'accuracy_mean': float(np.mean(accs)),
                      'accuracy_sd': float(np.std(accs, ddof=1))})
    res['training_size_curve'] = curve

    # --- 3. how much test text does it need? ---------------------------------
    lengths = []
    for L in (500, 1000, 2000, 5000, 10000, 20000):
        XL = delta.vectors(plays, vocab, limit=L)
        ok = tot = 0
        for i in range(len(plays)):
            keep = np.ones(len(plays), bool)
            keep[i] = False
            pred = delta.attribute(X[keep], y[keep], XL[i:i + 1])[0]
            ok += pred == y[i]
            tot += 1
        lengths.append({'test_words': L, 'accuracy': ok / tot})
    res['test_length_curve'] = lengths

    # --- 4. does it survive a period gap? ------------------------------------
    gaps = []
    for T in (0, 5, 10, 20, 30):
        def mask_fn(i, T=T):
            if years[i] < 0:
                return np.ones(len(plays), bool)
            return ~((np.abs(years - years[i]) <= T) & (years >= 0)) | (np.arange(len(plays)) == i)
        a, n2, _ = delta.loo(plays, X, y, mask_fn=mask_fn)
        gaps.append({'exclude_training_within_years': T, 'accuracy': a, 'n_tested': n2})
    res['period_gap_curve'] = gaps

    res['runtime_seconds'] = time.time() - t0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(res, open(OUT, 'w'), indent=1)

    b = res['baseline']
    print('corpus: %d plays, %d authors' % (res['n_plays'], res['n_authors']))
    print('baseline leave-one-out accuracy: %.3f  (n=%d)' % (b['accuracy'], b['n_tested']))
    print('  uniform chance %.3f | majority class %.3f | label-permutation null %.3f (max %.3f)'
          % (b['chance_uniform'], b['chance_majority_class'],
             b['label_permutation_null_mean'], b['label_permutation_null_max']))
    print()
    print('training plays per author -> accuracy')
    for c in curve:
        print('   %2d  %.3f ± %.3f' % (c['train_plays_per_author'], c['accuracy_mean'], c['accuracy_sd']))
    print()
    print('test-sample words -> accuracy')
    for c in lengths:
        print('   %6d  %.3f' % (c['test_words'], c['accuracy']))
    print()
    print('exclude training plays within N years of the test play -> accuracy')
    for c in gaps:
        print('   +/-%2d yr  %.3f  (n=%d)' % (c['exclude_training_within_years'], c['accuracy'], c['n_tested']))
    print('\nruntime %.0fs' % res['runtime_seconds'])


if __name__ == '__main__':
    main()


def matched_period_control():
    """The period-gap curve tests fewer plays as the gap widens, because plays
    whose author has no surviving distant work are skipped. That changes the
    test set, so the drop could be composition rather than period. This recomputes
    the no-gap accuracy on exactly the plays each gap condition could test."""
    import numpy as np, collections
    plays = corpus.load()
    y = np.array([p['author'] for p in plays])
    years = np.array([p['year'] or -1 for p in plays])
    vocab = delta.vocabulary(plays)
    X = delta.vectors(plays, vocab)
    out = []
    for T in (0, 5, 10, 20, 30):
        testable, gap_ok, full_ok = [], 0, 0
        for i in range(len(plays)):
            keep = np.ones(len(plays), bool); keep[i] = False
            if years[i] >= 0:
                keep &= ~((np.abs(years - years[i]) <= T) & (years >= 0))
            if (y[keep] == y[i]).sum() < 1 or len(set(y[keep])) < 2:
                continue
            testable.append(i)
            gap_ok += delta.attribute(X[keep], y[keep], X[i:i+1])[0] == y[i]
            full = np.ones(len(plays), bool); full[i] = False
            full_ok += delta.attribute(X[full], y[full], X[i:i+1])[0] == y[i]
        n = len(testable)
        out.append({'gap_years': T, 'n_tested': n,
                    'accuracy_with_gap': gap_ok/n, 'accuracy_same_plays_no_gap': full_ok/n,
                    'drop': full_ok/n - gap_ok/n})
    return out


if __name__ == '__main__' and '--control' in sys.argv:
    import json
    r = matched_period_control()
    print('gap  n    with-gap  same plays, no gap   drop')
    for x in r:
        print('  %2d %4d   %.3f       %.3f            %+.3f'
              % (x['gap_years'], x['n_tested'], x['accuracy_with_gap'],
                 x['accuracy_same_plays_no_gap'], -x['drop']))
    p = os.path.join(os.path.dirname(__file__), '..', 'results', 'period_control.json')
    json.dump(r, open(p, 'w'), indent=1)
