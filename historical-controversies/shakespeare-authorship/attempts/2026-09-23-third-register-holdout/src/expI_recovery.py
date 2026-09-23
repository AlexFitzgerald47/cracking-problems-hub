"""Which authors does the correction reach? (handover item 2, at n = 19.)

The 2026-09-21 handover named two candidate explanations for the two authors the
correction failed on, and said n = 8 could not separate them: the ratio of
non-dramatic to drama chunks, and the date gap between an author's two registers.
The holdout arm supplies eleven more authors, so the question is now testable at
n = 19 - still small, and the p-values below are reported with that in mind.
"""
import sys, os, json, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-09-21-period-detrend-and-equal-n', 'src'))
import common as C

RES = os.path.join(HERE, '..', 'results', 'expH_holdout.json')


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    rx, ry = rank(x), rank(y)
    rx, ry = rx - rx.mean(), ry - ry.mean()
    return float((rx * ry).sum() / np.sqrt((rx * rx).sum() * (ry * ry).sum()))


def rank(a):
    order = np.argsort(a)
    r = np.empty(len(a), float)
    r[order] = np.arange(len(a), dtype=float)
    # average ties
    for v in set(a.tolist()):
        m = a == v
        r[m] = r[m].mean()
    return r


def perm_p(x, y, rho, n=20000, seed=20260923):
    rng = np.random.default_rng(seed)
    y = np.asarray(y, float)
    c = 0
    for _ in range(n):
        if abs(spearman(x, rng.permutation(y))) >= abs(rho):
            c += 1
    return (c + 1) / (n + 1)


def main():
    out = json.load(open(RES))
    docs, _ = C.load(require_year=True)
    hold = json.load(open(os.path.join(HERE, '..', 'data', 'holdout_chunks.json')))
    yrs = collections.defaultdict(list)
    cnt = collections.Counter()
    for d in docs:
        yrs[(d['author'], d['register'])].append(int(str(d['year'])[:4]))
        cnt[(d['author'], d['register'])] += 1
    for d in hold:
        yrs[(d['author'], 'nondrama')].append(int(str(d['year'])[:4]))
        cnt[(d['author'], 'nondrama')] += 1

    rows = []
    for arm, key in (('original', 'original_arm_943'), ('holdout', 'holdout')):
        r = out[key]
        acc = r['detrend + centre']['per_author']
        for a in r['present']:
            nd, dr = cnt[(a, 'nondrama')], cnt[(a, 'drama')]
            gap = abs(np.mean(yrs[(a, 'nondrama')]) - np.mean(yrs[(a, 'drama')]))
            rows.append({'arm': arm, 'author': a, 'acc': acc[a], 'n_nd': nd, 'n_dr': dr,
                         'log_ratio': float(np.log(nd / dr)), 'date_gap': float(gap),
                         'acc_uncorrected': r['uncorrected']['per_author'][a]})
    rows.sort(key=lambda r: -r['acc'])
    print('%-22s %-8s %6s %6s %6s %8s %8s %8s' %
          ('author', 'arm', 'n_nd', 'n_dr', 'gap', 'logratio', 'acc', 'uncorr'))
    for r in rows:
        print('%-22s %-8s %6d %6d %6.1f %8.2f %8.3f %8.3f' %
              (r['author'], r['arm'], r['n_nd'], r['n_dr'], r['date_gap'],
               r['log_ratio'], r['acc'], r['acc_uncorrected']))

    acc = [r['acc'] for r in rows]
    for name in ('date_gap', 'log_ratio', 'n_nd'):
        v = [r[name] for r in rows]
        rho = spearman(v, acc)
        print('\nSpearman(%s, corrected accuracy) over %d authors = %+.3f  (permutation p = %.4f)'
              % (name, len(rows), rho, perm_p(np.asarray(v, float), acc, rho)))
    # holdout only, for P6
    h = [r for r in rows if r['arm'] == 'holdout']
    rho_n = spearman([r['n_nd'] for r in h], [r['acc'] for r in h])
    print('\nP6: Spearman(chunk count, corrected accuracy) on the 11 holdout authors = %+.3f' % rho_n)
    json.dump({'rows': rows}, open(os.path.join(HERE, '..', 'results', 'expI_recovery.json'), 'w'),
              indent=1)


if __name__ == '__main__':
    main()
