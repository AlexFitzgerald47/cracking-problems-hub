"""Experiment D - do the two corrections stack, and does either one hollow out the other?

A found that detrending against real dates more than doubles cross-register micro
accuracy (0.169 -> 0.356). C found that the cross-register numbers are inflated by
a sink which a register-centring wipes out. D1 asks whether A's gain was just the
sink moving; D2 and D3 put both corrections together and ask what is left.

The culminating number this folder can produce is the last line printed here: the
best cross-register accuracy obtainable with both corrections applied, against the
same pipeline's within-register accuracy on the same corpus.
"""
import sys, os, json, collections, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import delta as D
from expC_mechanism import attribute, score, pear
from expA2_scalefree import within_loo_clean

N_NULL = 200


def main():
    rng = random.Random(C.SEED)
    docs_full, _ = C.load()
    docs, _ = C.load(require_year=True)
    vocab = D.vocabulary(docs_full)
    X = D.vectors(docs, vocab)
    years = np.array([d['yr'] for d in docs], float)
    au = np.array([d['author'] for d in docs])
    rg = np.array([d['register'] for d in docs])
    wk = np.array([d['work'] for d in docs])
    dmask = rg == 'drama'
    nd = np.where(rg == 'nondrama')[0]
    authors27 = sorted(set(au[dmask]))
    out = {}

    print('%-34s %9s %9s %9s %9s %9s' %
          ('treatment', 'Lyly%', 'HHI27', 'mac27', 'mac8', 'mic8'))
    print('-' * 86)
    rows = {}
    for tag, deg, centre in (('none', 0, False), ('detrend', 1, False),
                             ('centre', 0, True), ('detrend+centre', 1, True)):
        Xt = X if deg == 0 else C.detrend(X, years, dmask, degree=deg)
        Z = C.zscale(Xt, dmask)
        c27 = np.stack([Z[dmask & (au == a)].mean(0) for a in authors27])
        c8 = np.stack([Z[dmask & (au == a)].mean(0) for a in C.PANEL])
        T = Z[nd] - (Z[nd].mean(0) if centre else 0.0)
        p27 = attribute(T, c27, authors27)
        p8 = attribute(T, c8, C.PANEL)
        sh = {a: float(np.mean([q == a for q in p27])) for a in authors27}
        s27 = score(p27, au[nd], C.PANEL)
        s8 = score(p8, au[nd], C.PANEL)
        rows[tag] = {'lyly_share27': sh['Lyly, John'],
                     'hhi27': float(sum(v * v for v in sh.values())),
                     'zeros27': sum(1 for v in sh.values() if v == 0),
                     'macro27panel': s27['macro'], 'micro27panel': s27['micro'],
                     'macro8': s8['macro'], 'micro8': s8['micro'],
                     'per_author8': s8['per_author'],
                     'share27': sh}
        print('%-34s %8.1f%% %9.4f %9.3f %9.3f %9.3f'
              % (tag, 100 * sh['Lyly, John'], rows[tag]['hhi27'],
                 s27['macro'], s8['macro'], s8['micro']))
    out['treatments'] = rows

    print('\nD1  Lyly share under detrending: %.1f%% (predicted > 20%%; untreated 41.0%%)'
          % (100 * rows['detrend']['lyly_share27']))
    print('D2  detrend+centre 8-author macro: %.3f (predicted < 0.50)'
          % rows['detrend+centre']['macro8'])

    # ---- D3 null for the combined treatment ----
    Xt = C.detrend(X, years, dmask, degree=1)
    Z = C.zscale(Xt, dmask)
    c8 = np.stack([Z[dmask & (au == a)].mean(0) for a in C.PANEL])
    T = Z[nd] - Z[nd].mean(0)
    pred = attribute(T, c8, C.PANEL)
    obs = score(pred, au[nd], C.PANEL)
    wk_nd = wk[nd]
    owner = {w: au[nd][wk_nd == w][0] for w in set(wk_nd)}
    nulls = []
    for _ in range(N_NULL):
        perm = C.PANEL[:]
        rng.shuffle(perm)
        mp = dict(zip(C.PANEL, perm))
        fake = np.array([mp[owner[w]] for w in wk_nd])
        nulls.append(score(pred, fake, C.PANEL)['macro'])
    nulls = np.array(nulls)
    out['D3_null'] = {'n': N_NULL, 'observed': obs['macro'],
                      'mean': float(nulls.mean()), 'p95': float(np.percentile(nulls, 95)),
                      'max': float(nulls.max()),
                      'p_one_sided': float(np.mean(nulls >= obs['macro']))}
    print('D3  detrend+centre macro %.3f vs %d-permutation null: mean %.3f, p95 %.3f, p = %.3f'
          % (obs['macro'], N_NULL, nulls.mean(), np.percentile(nulls, 95),
             np.mean(nulls >= obs['macro'])))
    print('    per author:')
    for a in C.PANEL:
        print('      %-22s %.3f  (n=%d)' % (a, obs['per_author'][a], int((au[nd] == a).sum())))

    # ---- the culminating comparison, both on the detrended features ----
    wi = within_loo_clean(X, years, docs, C.PANEL, 1)
    out['within_register_detrended_leakfree'] = wi
    out['final_comparison'] = {
        'within_register_macro': wi['macro'], 'within_register_micro': wi['micro'],
        'cross_register_best_macro': obs['macro'], 'cross_register_best_micro': obs['micro'],
        'chance': 1 / len(C.PANEL)}
    print('\nBEST AVAILABLE, both corrections, 8 candidate authors, chance 0.125')
    print('   within register (leave-one-work-out, detrended) macro %.3f  micro %.3f'
          % (wi['macro'], wi['micro']))
    print('   cross  register (detrended + register-centred)  macro %.3f  micro %.3f'
          % (obs['macro'], obs['micro']))

    # ---- exploratory: L1 proximity as a description of the sink ----
    Z0 = C.zscale(X, dmask)
    c27 = np.stack([Z0[dmask & (au == a)].mean(0) for a in authors27])
    m = Z0[nd].mean(0)
    l1 = {a: float(np.abs(m - c27[i]).sum()) for i, a in enumerate(authors27)}
    sh0 = rows['none']['share27']
    r = pear([-l1[a] for a in authors27], [sh0[a] for a in authors27])
    ranks = sorted(authors27, key=lambda a: l1[a])
    out['exploratory_L1_proximity'] = {
        'pearson_neg_L1_vs_absorption': r,
        'l1_to_nondrama_centre': l1,
        'nearest_five': ranks[:5],
        'top_five_absorbers': sorted(authors27, key=lambda a: -sh0[a])[:5]}
    print('\nEXPLORATORY (statistic chosen after the frozen cosine test underperformed):')
    print('   Pearson(-L1 from centroid to the non-dramatic centre of mass, absorption) = %+.3f' % r)
    print('   five centroids nearest that centre:  %s' % ', '.join(a.split(',')[0] for a in ranks[:5]))
    print('   five largest absorbers:              %s' %
          ', '.join(a.split(',')[0] for a in sorted(authors27, key=lambda a: -sh0[a])[:5]))
    C.save('expD_combined.json', out)


if __name__ == '__main__':
    main()
