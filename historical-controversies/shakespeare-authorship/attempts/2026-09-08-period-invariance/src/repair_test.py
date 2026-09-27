"""Is normalisation removing a date-loaded feature, or repairing a corrupted one?

The dating test (results/dating.json) showed 98 random raw features date a play as well
as the 98 variant-pair features (MAE 13.0 vs 13.3 yr, leave-one-author-out). So the
variant features are not uniquely date-carrying, and "remove the date stamp" is the
wrong account.

The alternative: a variant pair is *one lexeme whose rate has been split across two
features in a proportion set by the printing date*. Merging does not delete date
information, it repairs a corrupted measurement of an authorial quantity. That predicts
the merged feature is both LESS date-loaded and MORE author-discriminating than either
of its components - which deleting a feature can never achieve.
"""
import os, json, collections
import numpy as np
import shared, ortho


def stats(x, y, yr):
    """R^2 on year, and author F, for one feature column."""
    z = (x - x.mean()) / (x.std() or 1)
    t = (yr - yr.mean()) / yr.std()
    b = (z * t).sum() / (t ** 2).sum()
    r2 = 1 - ((z - b * t) ** 2).sum() / max((z ** 2).sum(), 1e-12)
    a = sorted(set(y))
    g = z.mean()
    bet = sum((y == k).sum() * (z[y == k].mean() - g) ** 2 for k in a)
    wit = sum(((z[y == k] - z[y == k].mean()) ** 2).sum() for k in a)
    F = (bet / (len(a) - 1)) / max(wit / (len(z) - len(a)), 1e-12)
    return r2, F


def main():
    plays = shared.load()
    y = np.array([p['author'] for p in plays])
    yr = np.array([float(p['year']) for p in plays])
    vr = shared.vocabulary(plays, words_key='words')
    Xr = shared.vectors(plays, vr, words_key='words')

    grp = collections.defaultdict(list)
    for j, w in enumerate(vr):
        grp[ortho.key(w)].append(j)
    groups = {k: g for k, g in grp.items() if len(g) > 1}

    rows = []
    for k, g in sorted(groups.items()):
        merged = Xr[:, g].sum(1)
        mr2, mF = stats(merged, y, yr)
        comps = [stats(Xr[:, j], y, yr) for j in g]
        rows.append({'key': k, 'members': [vr[j] for j in g],
                     'merged_r2_date': mr2, 'merged_F_author': mF,
                     'component_r2_date_max': max(c[0] for c in comps),
                     'component_F_author_max': max(c[1] for c in comps)})

    less_dated = np.mean([r['merged_r2_date'] < r['component_r2_date_max'] for r in rows])
    more_auth = np.mean([r['merged_F_author'] > r['component_F_author_max'] for r in rows])
    both = np.mean([r['merged_r2_date'] < r['component_r2_date_max'] and
                    r['merged_F_author'] > r['component_F_author_max'] for r in rows])
    print('%d merge groups (%d raw features)\n' % (len(rows), sum(len(g) for g in groups.values())))
    print('merged feature less date-loaded than its most date-loaded component : %.0f%%' % (100 * less_dated))
    print('merged feature more author-discriminating than its best component   : %.0f%%' % (100 * more_auth))
    print('both at once                                                        : %.0f%%' % (100 * both))
    print('\nmean R2(year):  components (max) %.3f -> merged %.3f'
          % (np.mean([r['component_r2_date_max'] for r in rows]),
             np.mean([r['merged_r2_date'] for r in rows])))
    print('mean F(author): components (max) %.2f  -> merged %.2f'
          % (np.mean([r['component_F_author_max'] for r in rows]),
             np.mean([r['merged_F_author'] for r in rows])))
    print('\nlargest groups:')
    for r in sorted(rows, key=lambda r: -len(r['members']))[:12]:
        print('  %-12s %-34s R2 %.3f->%.3f   F %5.2f->%5.2f'
              % (r['key'], '/'.join(r['members']), r['component_r2_date_max'],
                 r['merged_r2_date'], r['component_F_author_max'], r['merged_F_author']))
    json.dump({'summary': {'frac_less_date_loaded': less_dated,
                           'frac_more_author_discriminating': more_auth,
                           'frac_both': both}, 'groups': rows},
              open(os.path.join(os.path.dirname(__file__), '..', 'results', 'repair_test.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
