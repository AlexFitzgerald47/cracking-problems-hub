"""Headline decomposition + McNemar test, regenerated from scratch so the write-up
does not depend on numbers typed by hand."""
import os, json, re
import numpy as np
import shared, ortho
from grid import att_cosine, att_manhattan, evaluate

T = 10
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'headline.json')


def per_play(X, y, yr, att):
    n = len(y); rec = {}
    for i in range(n):
        keep = np.ones(n, bool); keep[i] = False
        keep &= ~(np.abs(yr - yr[i]) <= T)
        if (y[keep] == y[i]).sum() < 1 or len(set(y[keep])) < 2:
            continue
        rec[i] = att(X[keep], y[keep], X[i:i+1]) == y[i]
    return rec


def main():
    plays = shared.load()
    for p in plays:
        p['keys'] = [ortho.key(w) for w in p['words']]
    y = np.array([p['author'] for p in plays])
    yr = np.array([float(p['year']) for p in plays])
    Xr = shared.vectors(plays, shared.vocabulary(plays, words_key='words'), words_key='words')
    Xk = shared.vectors(plays, shared.vocabulary(plays, words_key='keys'), words_key='keys')

    old = per_play(Xr, y, yr, att_manhattan)
    new = per_play(Xk, y, yr, att_cosine)
    keys = sorted(set(old) & set(new))
    b = sum(1 for i in keys if old[i] and not new[i])   # old right, new wrong
    c = sum(1 for i in keys if new[i] and not old[i])   # new right, old wrong
    # exact McNemar (binomial, two-sided)
    from math import comb
    n_disc = b + c
    tail = sum(comb(n_disc, k) for k in range(0, min(b, c) + 1)) / 2 ** n_disc
    p = min(1.0, 2 * tail)

    res = {'n_tested': len(keys),
           'old_config': 'raw + top500 + Manhattan (2026-09-05)',
           'new_config': 'orthographic key + top500 + cosine (2026-09-08)',
           'old_accuracy': sum(old[i] for i in keys) / len(keys),
           'new_accuracy': sum(new[i] for i in keys) / len(keys),
           'discordant_old_only': b, 'discordant_new_only': c,
           'mcnemar_exact_p': p}
    print('±10-year gap, n=%d' % res['n_tested'])
    print('  2026-09-05 configuration : %.3f' % res['old_accuracy'])
    print('  2026-09-08 configuration : %.3f' % res['new_accuracy'])
    print('  discordant: new-only-right %d, old-only-right %d, exact McNemar p = %.3g'
          % (c, b, p))

    # decomposition for both configurations, gaps 5/10/20
    res['decomposition'] = {
        'old': evaluate(Xr, y, yr, att_manhattan, gaps=(5, 10, 20), reps=12),
        'new': evaluate(Xk, y, yr, att_cosine, gaps=(5, 10, 20), reps=12)}
    print('\n%-6s %-5s %8s %10s %8s %10s %10s' % ('cfg', 'gap', 'full', 'random-abl',
                                                  'time-gap', 'data-loss', 'chronology'))
    for tag in ('old', 'new'):
        for r in res['decomposition'][tag]:
            print('%-6s ±%-4d %8.3f %10.3f %8.3f %10.3f %10.3f'
                  % (tag, r['gap_years'], r['acc_full'], r['acc_random_ablation'],
                     r['acc_time_gap'], r['acc_random_ablation'] - r['acc_full'],
                     r['chronology_effect']))
    json.dump(res, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
