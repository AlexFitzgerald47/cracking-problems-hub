"""Unconditioned replacement for the error-direction test.

P8 as preregistered conditioned on errors, and the winning configuration makes far
fewer of them (72 vs 129), so it compares a harder residual set against an easier one.
That test cannot be read. This is the version that does not condition on the outcome:
for every fold, rank all available authors by the model's own distance, rank them by
date-proximity to the questioned play, and take the Spearman correlation between the
two rankings. Averaged over all folds, it measures how date-driven the whole decision
surface is, not just the part that went wrong.
"""
import os, json
import numpy as np
import shared, ortho

T = 10
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'date_drivenness.json')


def zsc(Xtr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0); sd[sd == 0] = 1
    return (Xtr - mu) / sd, (Xte - mu) / sd


def dists(Xtr, ytr, Xte, how):
    Ztr, Zte = zsc(Xtr, Xte)
    a = sorted(set(ytr))
    c = np.stack([Ztr[ytr == k].mean(0) for k in a])
    if how == 'manhattan':
        d = np.abs(Zte[0] - c).sum(1)
    else:
        cn = c / np.maximum(np.linalg.norm(c, axis=1, keepdims=True), 1e-12)
        v = Zte[0] / max(np.linalg.norm(Zte[0]), 1e-12)
        d = 1 - cn @ v
    return a, d


def rank(v):
    o = np.argsort(v); r = np.empty(len(v)); r[o] = np.arange(len(v))
    return r


def measure(X, y, yr, how):
    n = len(y); rhos = []; topdate = 0; folds = 0
    for i in range(n):
        keep = np.ones(n, bool); keep[i] = False
        keep &= ~(np.abs(yr - yr[i]) <= T)
        if (y[keep] == y[i]).sum() < 1 or len(set(y[keep])) < 2:
            continue
        a, d = dists(X[keep], y[keep], X[i:i+1], how)
        prox = np.array([np.abs(yr[keep][y[keep] == k] - yr[i]).mean() for k in a])
        rd, rp = rank(d), rank(prox)
        rd -= rd.mean(); rp -= rp.mean()
        rho = float((rd * rp).sum() / np.sqrt((rd**2).sum() * (rp**2).sum()))
        rhos.append(rho)
        topdate += int(a[int(d.argmin())] == a[int(prox.argmin())])
        folds += 1
    rhos = np.array(rhos)
    return {'mean_spearman_distance_vs_dateproximity': float(rhos.mean()),
            'sd': float(rhos.std(ddof=1)), 'se': float(rhos.std(ddof=1) / np.sqrt(folds)),
            'frac_folds_top_ranked_author_is_date_nearest': topdate / folds,
            'n_folds': folds}


def main():
    plays = shared.load()
    for p in plays:
        p['keys'] = [ortho.key(w) for w in p['words']]
    y = np.array([p['author'] for p in plays])
    yr = np.array([float(p['year']) for p in plays])
    Xr = shared.vectors(plays, shared.vocabulary(plays, words_key='words'), words_key='words')
    Xk = shared.vectors(plays, shared.vocabulary(plays, words_key='keys'), words_key='keys')

    cells = {'raw+manhattan (2026-09-05 config)': (Xr, 'manhattan'),
             'norm+manhattan': (Xk, 'manhattan'),
             'raw+cosine': (Xr, 'cosine'),
             'norm+cosine (winner)': (Xk, 'cosine')}
    res = {}
    for k, (X, how) in cells.items():
        res[k] = measure(X, y, yr, how)
        r = res[k]
        print('%-36s rho = %+.3f ± %.3f (se)   top-ranked author is date-nearest in %.0f%% of folds'
              % (k, r['mean_spearman_distance_vs_dateproximity'], r['se'],
                 100 * r['frac_folds_top_ranked_author_is_date_nearest']))
    json.dump(res, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
