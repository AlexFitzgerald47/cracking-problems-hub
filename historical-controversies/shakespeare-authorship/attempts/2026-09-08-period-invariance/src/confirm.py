"""Confirmation runs for the winning configuration: error direction, and the null."""
import os, json
import numpy as np
import shared, ortho
from grid import att_cosine, att_manhattan

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'confirm.json')
T = 10


def date_bias(X, y, yr, att):
    n = len(y)
    be = []
    for i in range(n):
        keep = np.ones(n, bool); keep[i] = False
        keep &= ~(np.abs(yr - yr[i]) <= T)
        if (y[keep] == y[i]).sum() < 1 or len(set(y[keep])) < 2:
            continue
        pred = att(X[keep], y[keep], X[i:i+1])
        if pred == y[i]:
            continue
        avail = sorted(set(y[keep]))
        d = {a: float(np.abs(yr[keep][y[keep] == a] - yr[i]).mean()) for a in avail}
        others = [d[a] for a in avail if a != y[i] and a != pred]
        if others:
            be.append(d[pred] - float(np.mean(others)))
    rng = np.random.default_rng(20260908)
    boot = [np.mean(rng.choice(be, len(be))) for _ in range(4000)]
    return {'n_errors': len(be), 'date_bias_years': float(np.mean(be)),
            'ci95': [float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))],
            'frac_date_proximate': float(np.mean(np.array(be) < 0))}


def gap_acc(X, y, yr, att):
    n = len(y); ok = tot = 0
    for i in range(n):
        keep = np.ones(n, bool); keep[i] = False
        keep &= ~(np.abs(yr - yr[i]) <= T)
        if (y[keep] == y[i]).sum() < 1 or len(set(y[keep])) < 2:
            continue
        tot += 1
        ok += att(X[keep], y[keep], X[i:i+1]) == y[i]
    return ok / tot, tot


def main():
    plays = shared.load()
    for p in plays:
        p['keys'] = [ortho.key(w) for w in p['words']]
    y = np.array([p['author'] for p in plays])
    yr = np.array([float(p['year']) for p in plays])
    vk = shared.vocabulary(plays, words_key='keys')
    Xk = shared.vectors(plays, vk, words_key='keys')
    vr = shared.vocabulary(plays, words_key='words')
    Xr = shared.vectors(plays, vr, words_key='words')

    res = {'gap_years': T}
    res['date_bias'] = {
        'raw+top500+manhattan (2026-09-05 config)': date_bias(Xr, y, yr, att_manhattan),
        'norm+top500+manhattan': date_bias(Xk, y, yr, att_manhattan),
        'norm+top500+cosine (winner)': date_bias(Xk, y, yr, att_cosine),
    }
    for k, v in res['date_bias'].items():
        print('%-42s date-bias %+.2f yr  CI [%+.2f,%+.2f]  %.0f%% proximate  (n=%d)'
              % (k, v['date_bias_years'], v['ci95'][0], v['ci95'][1],
                 100 * v['frac_date_proximate'], v['n_errors']))

    rng = np.random.default_rng(20260908)
    a, n = gap_acc(Xk, y, yr, att_cosine)
    null = [gap_acc(Xk, rng.permutation(y), yr, att_cosine)[0] for _ in range(25)]
    res['null'] = {'winner_gap_accuracy': a, 'n_tested': n,
                   'label_permutation_mean': float(np.mean(null)),
                   'label_permutation_max': float(np.max(null)),
                   'uniform_chance': 1 / len(set(y)), 'n_permutations': len(null)}
    print('\nwinner ±10 accuracy %.3f (n=%d) | label-permutation null %.3f (max %.3f) | chance %.3f'
          % (a, n, np.mean(null), np.max(null), 1 / len(set(y))))
    json.dump(res, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
