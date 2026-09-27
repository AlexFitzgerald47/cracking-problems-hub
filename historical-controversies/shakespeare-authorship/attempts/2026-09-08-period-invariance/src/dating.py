"""Can spelling alone date a play?

Ridge regression from features to composition year, validated leave-one-author-out so
that no model can date a play by recognising who wrote it (authors cluster in time, and
leave-one-play-out would let that leak). Leave-one-play-out is reported alongside to
show the size of that leak.
"""
import os, json
import numpy as np
import shared, ortho

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'dating.json')
LAM = 1.0


def ridge_cv(X, yr, groups):
    """groups: array of fold ids. Returns MAE, R2, predictions."""
    pred = np.zeros(len(yr))
    for g in np.unique(groups):
        te = groups == g
        tr = ~te
        mu, sd = X[tr].mean(0), X[tr].std(0)
        sd[sd == 0] = 1
        A = (X[tr] - mu) / sd
        B = (X[te] - mu) / sd
        ym = yr[tr].mean()
        w = np.linalg.solve(A.T @ A + LAM * np.eye(A.shape[1]), A.T @ (yr[tr] - ym))
        pred[te] = B @ w + ym
    mae = float(np.abs(pred - yr).mean())
    r2 = float(1 - ((pred - yr) ** 2).sum() / ((yr - yr.mean()) ** 2).sum())
    return mae, r2, pred


def main():
    plays = shared.load()
    for p in plays:
        p['keys'] = [ortho.key(w) for w in p['words']]
    y = np.array([p['author'] for p in plays])
    yr = np.array([float(p['year']) for p in plays])

    vr = shared.vocabulary(plays, words_key='words')
    Xr = shared.vectors(plays, vr, words_key='words')
    vk = shared.vocabulary(plays, words_key='keys')
    Xk = shared.vectors(plays, vk, words_key='keys')

    # which raw features participate in a merge group?
    import collections
    grp = collections.defaultdict(list)
    for j, w in enumerate(vr):
        grp[ortho.key(w)].append(j)
    variant = sorted(j for g in grp.values() if len(g) > 1 for j in g)
    other = [j for j in range(len(vr)) if j not in set(variant)]

    sets = {
        'raw, all 500': Xr,
        'variant-pair features only (%d)' % len(variant): Xr[:, variant],
        'raw minus variant features (%d)' % len(other): Xr[:, other],
        'orthographically normalised, 500': Xk,
    }
    # a size-matched random control for the variant set
    rng = np.random.default_rng(20260908)
    sets['random %d raw features (mean of 10)' % len(variant)] = None

    au = np.array([sorted(set(y)).index(a) for a in y])
    play_folds = np.arange(len(yr))

    res = {'n_variant_features': len(variant),
           'variant_features': [vr[j] for j in variant], 'cells': []}
    print('%-46s %-22s %s' % ('feature set', 'leave-one-AUTHOR-out', 'leave-one-play-out'))
    for name, X in sets.items():
        if X is None:
            maes, r2s = [], []
            for _ in range(10):
                sel = rng.permutation(len(vr))[:len(variant)]
                m, r, _ = ridge_cv(Xr[:, sel], yr, au)
                maes.append(m); r2s.append(r)
            mae, r2 = float(np.mean(maes)), float(np.mean(r2s))
            mae2 = r22 = float('nan')
        else:
            mae, r2, _ = ridge_cv(X, yr, au)
            mae2, r22, _ = ridge_cv(X, yr, play_folds)
        res['cells'].append({'features': name, 'mae_author_out': mae, 'r2_author_out': r2,
                             'mae_play_out': mae2, 'r2_play_out': r22})
        print('%-46s MAE %5.1f yr  R2 %+.3f   MAE %5.1f yr  R2 %+.3f'
              % (name, mae, r2, mae2, r22))
    print('\nsd of the year variable: %.1f yr (a model that always guesses the mean has MAE %.1f)'
          % (yr.std(), np.abs(yr - yr.mean()).mean()))
    res['year_sd'] = float(yr.std())
    res['mae_predict_mean'] = float(np.abs(yr - yr.mean()).mean())
    json.dump(res, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
