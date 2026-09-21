"""Experiment A, part 2. Two problems with part 1, and the null that settles them.

PROBLEM 1 - THE MARGIN IS NOT SCALE-FREE.
Detrending removes variance from the reference set, so z-scaling divides by a
smaller sd and EVERY Delta distance inflates. Part 1 showed the raw margin
(same-author-cross minus diff-author-same) falling 22.60 -> 8.13 under a linear
detrend, which reads as "register and period are the same effect". But all four
cells moved. Comparing a raw margin across treatments that rescale the units is
the same error as comparing a hill-climb score against a cheaper null: it
measures the treatment, not the effect.

So state both costs relative to the one cell that is neither, same author in the
same register:

    A = diff_author_same_register  - same_author_same_register   (cost of a different author)
    R = same_author_cross_register - same_author_same_register   (cost of a different register)
    R/A                                                          (scale-free; >1 means the
                                                                  register gap exceeds the
                                                                  author signal)

R/A is invariant to any common rescaling of the distance matrix, which is exactly
what a detrend does to it.

PROBLEM 2 - LEAKAGE IN THE WITHIN-REGISTER CONTROL.
Part 1 fitted the year trend on all drama chunks and then ran leave-one-work-out
attribution on those same chunks, so each held-out play helped define its own
correction. Here the trend is refitted from scratch with the test work excluded.
The cross-register arm never had this problem (trend fitted on drama, applied to
non-dramatic test documents), but the control has to be clean or the comparison
between the two is worthless.

THE NULL.
If detrending raises authorial accuracy, is that because chronology was masking
author signal, or because subtracting ANY two-parameter direction per feature and
then rescaling happens to help? Permute the year labels across works - keeping the
year distribution and the works intact, destroying only the link between a work
and its date - and run the identical pipeline. The null says how much of the gain
is chronology and how much is the shape of the operation.
"""
import sys, os, json, collections, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import delta as D
from expA_detrend import cells, attribute

N_NULL = 60


def costs(c):
    b = c['same_author_same_register']['mean']
    return {'A_author_cost': c['diff_author_same_register']['mean'] - b,
            'R_register_cost': c['same_author_cross_register']['mean'] - b,
            'ratio_R_over_A': (c['same_author_cross_register']['mean'] - b) /
                              (c['diff_author_same_register']['mean'] - b),
            'baseline_saSR': b,
            'raw_margin': c['same_author_cross_register']['mean'] -
                          c['diff_author_same_register']['mean']}


def within_loo_clean(X, years, docs, authors, degree, ref_is_drama=True):
    """Leave-one-WORK-out inside drama, refitting the detrend without that work.

    degree 0 means no detrend at all (the untreated control).
    """
    au = np.array([d['author'] for d in docs])
    rg = np.array([d['register'] for d in docs])
    wk = np.array([d['work'] for d in docs])
    dmask = rg == 'drama'
    preds, truth = [], []
    for w in sorted(set(wk[dmask])):
        te = dmask & (wk == w)
        tr = dmask & (wk != w)
        if len(set(au[tr])) < len(authors):
            continue
        ref = tr if ref_is_drama else (wk != w)
        Xt = X if degree == 0 else C.detrend(X, years, ref, degree=degree)
        Z = C.zscale(Xt, ref)
        cent = np.stack([Z[tr][au[tr] == a].mean(0) for a in authors])
        p = [authors[i] for i in np.abs(Z[te][:, None, :] - cent[None, :, :]).sum(2).argmin(1)]
        preds += p
        truth += list(au[te])
    per = {}
    for a in authors:
        h = [p == t for p, t in zip(preds, truth) if t == a]
        per[a] = float(np.mean(h)) if h else None
    return {'micro': float(np.mean([p == t for p, t in zip(preds, truth)])),
            'macro': float(np.mean([v for v in per.values() if v is not None])),
            'n': len(preds), 'per_author': per}


def main():
    rng = random.Random(C.SEED)
    docs_full, _ = C.load()
    docs_all, _ = C.load(require_year=True)
    panel = [d for d in docs_all if d['author'] in C.PANEL]
    vocab = D.vocabulary(docs_full)
    X = D.vectors(panel, vocab)
    years = np.array([d['yr'] for d in panel], float)
    rg = np.array([d['register'] for d in panel])
    au = np.array([d['author'] for d in panel])
    wk = np.array([d['work'] for d in panel])
    drama = rg == 'drama'
    out = {'n_null': N_NULL}

    print('%-30s %8s %8s %8s %8s | %6s %6s | %6s %6s' %
          ('treatment', 'saSR', 'A', 'R', 'R/A', 'crMic', 'crMac', 'wiMic', 'wiMac'))
    print('-' * 106)

    rows = []
    for tag, deg in (('none', 0), ('detrend_linear', 1), ('detrend_quadratic', 2)):
        Xt = X if deg == 0 else C.detrend(X, years, drama, degree=deg)
        Z = C.zscale(Xt, drama)
        c = cells(Z, panel)
        k = costs(c)
        cr = attribute(Z[drama], au[drama], Z[~drama], au[~drama], C.PANEL)
        wi = within_loo_clean(X, years, panel, C.PANEL, deg)
        rows.append((tag, k, cr, wi))
        out[tag] = {'cells': c, 'costs': k,
                    'cross_register': {x: y for x, y in cr.items() if x != 'per_author'},
                    'cross_register_per_author': cr['per_author'],
                    'within_register_leakfree': wi}
        print('%-30s %8.2f %8.2f %8.2f %8.3f | %6.3f %6.3f | %6.3f %6.3f' %
              (tag, k['baseline_saSR'], k['A_author_cost'], k['R_register_cost'],
               k['ratio_R_over_A'], cr['micro'], cr['macro'], wi['micro'], wi['macro']))

    # ---- year-matched pairing, expressed the same way ----
    Zb = C.zscale(X, drama)
    out['year_matched_costs'] = {}
    for w in (5, 10, 20, None):
        c = cells(Zb, panel, window=w)
        k = costs(c)
        out['year_matched_costs']['W%s' % (w if w else 'inf')] = k
        print('%-30s %8.2f %8.2f %8.2f %8.3f |' %
              ('year_matched W=%s' % (w if w else 'all'), k['baseline_saSR'],
               k['A_author_cost'], k['R_register_cost'], k['ratio_R_over_A']))

    # ---- NULL: permute year labels across works ----
    print('\nnull: %d permutations of the work->year map (linear detrend)' % N_NULL)
    works = sorted(set(wk))
    wyear = {w: years[wk == w][0] for w in works}
    nul = collections.defaultdict(list)
    for it in range(N_NULL):
        vals = [wyear[w] for w in works]
        rng.shuffle(vals)
        fake = dict(zip(works, vals))
        yf = np.array([fake[w] for w in wk], float)
        Xt = C.detrend(X, yf, drama, degree=1)
        Z = C.zscale(Xt, drama)
        c = cells(Z, panel)
        k = costs(c)
        cr = attribute(Z[drama], au[drama], Z[~drama], au[~drama], C.PANEL)
        for key, v in (('A', k['A_author_cost']), ('R', k['R_register_cost']),
                       ('ratio', k['ratio_R_over_A']), ('raw_margin', k['raw_margin']),
                       ('cr_micro', cr['micro']), ('cr_macro', cr['macro'])):
            nul[key].append(v)
    obs = {'A': rows[1][1]['A_author_cost'], 'R': rows[1][1]['R_register_cost'],
           'ratio': rows[1][1]['ratio_R_over_A'], 'raw_margin': rows[1][1]['raw_margin'],
           'cr_micro': rows[1][2]['micro'], 'cr_macro': rows[1][2]['macro']}
    base = {'A': rows[0][1]['A_author_cost'], 'R': rows[0][1]['R_register_cost'],
            'ratio': rows[0][1]['ratio_R_over_A'], 'raw_margin': rows[0][1]['raw_margin'],
            'cr_micro': rows[0][2]['micro'], 'cr_macro': rows[0][2]['macro']}
    out['null_year_permuted'] = {}
    print('%-12s %10s %10s %10s %10s %10s' %
          ('statistic', 'untreated', 'real detr', 'null mean', 'null p5', 'null p95'))
    for key in ('A', 'R', 'ratio', 'raw_margin', 'cr_micro', 'cr_macro'):
        v = np.array(nul[key])
        p = float(np.mean(v >= obs[key])) if key in ('A', 'cr_micro', 'cr_macro') \
            else float(np.mean(v <= obs[key]))
        out['null_year_permuted'][key] = {
            'untreated': base[key], 'observed_detrended': obs[key],
            'null_mean': float(v.mean()), 'p5': float(np.percentile(v, 5)),
            'p95': float(np.percentile(v, 95)), 'p_one_sided': p}
        print('%-12s %10.3f %10.3f %10.3f %10.3f %10.3f   p=%.3f' %
              (key, base[key], obs[key], v.mean(),
               np.percentile(v, 5), np.percentile(v, 95), p))

    C.save('expA2_scalefree.json', out)


if __name__ == '__main__':
    main()
