"""Experiment E - is the repair real, or is it reading the answer off the test set?

D got cross-register micro from 0.169 to 0.499 by detrending against date and
subtracting the mean of the non-dramatic corpus. The second step uses the test
documents themselves. If author a's own chunks are a large share of the mean
subtracted from author a's chunks, the gain is transductive leakage.

So estimate the displacement from OTHER AUTHORS ONLY: for each author a, centre
a's non-dramatic chunks on the mean of everyone else's non-dramatic chunks. A
practitioner can do this - it needs a reference corpus of other writers in the
questioned register, which for early modern non-dramatic prose is abundant - and
it cannot see the questioned author.

Also fixes D's within-register line, which was computed on 27-author documents
against 8-author labels and so reported a meaninglessly diluted micro.

E4 takes the whole apparatus to the 19 civic pageants the 2026-09-17 session set
aside before computing any distance. Those are the closest thing this corpus has
to the real question, and nothing in A-D has touched them.
"""
import sys, os, json, collections, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import delta as D
from expC_mechanism import attribute, score
from expA2_scalefree import within_loo_clean
from expB_equaln import load_pageants

N_NULL = 200


def loao_centre(Z, idx, authors_of_idx, panel):
    """Centre each author's test chunks on the mean of the OTHER authors' chunks."""
    T = np.empty_like(Z[idx])
    for a in set(authors_of_idx):
        own = authors_of_idx == a
        other = ~own
        if other.sum() == 0:
            T[own] = Z[idx][own]
            continue
        T[own] = Z[idx][own] - Z[idx][other].mean(0)
    return T


def perm_null(pred, wk_test, owner, panel, rng, n=N_NULL, statistic='macro'):
    nulls = []
    for _ in range(n):
        p = panel[:]
        rng.shuffle(p)
        mp = dict(zip(panel, p))
        fake = np.array([mp[owner[w]] for w in wk_test])
        nulls.append(score(pred, fake, panel)[statistic])
    return np.array(nulls)


def main():
    rng = random.Random(C.SEED)
    docs_full, _ = C.load()
    docs, _ = C.load(require_year=True)
    pag = [p for p in load_pageants()]
    for p in pag:
        p['yr'] = int(str(p['year'])[:4])
    allv = docs + pag
    vocab = D.vocabulary(docs_full)
    X = D.vectors(allv, vocab)
    years = np.array([d['yr'] for d in allv], float)
    au = np.array([d['author'] for d in allv])
    rg = np.array([d['register'] for d in allv])
    wk = np.array([d['work'] for d in allv])
    dmask = rg == 'drama'
    nd = np.where(rg == 'nondrama')[0]
    pg = np.where(rg == 'pageant')[0]
    out = {}

    Xt = C.detrend(X, years, dmask, degree=1)
    Z = C.zscale(Xt, dmask)
    c8 = np.stack([Z[dmask & (au == a)].mean(0) for a in C.PANEL])

    print('%-38s %8s %8s' % ('cross-register treatment (8 authors)', 'micro', 'macro'))
    print('-' * 56)
    variants = {}
    for tag, T in (
            ('detrended, uncentred', Z[nd]),
            ('detrended + pooled centring', Z[nd] - Z[nd].mean(0)),
            ('detrended + leave-one-author-out centring',
             loao_centre(Z, nd, au[nd], C.PANEL))):
        pred = attribute(T, c8, C.PANEL)
        s = score(pred, au[nd], C.PANEL)
        variants[tag] = {'micro': s['micro'], 'macro': s['macro'],
                         'per_author': s['per_author'], 'pred': pred}
        print('%-38s %8.3f %8.3f' % (tag, s['micro'], s['macro']))
    out['nondrama_variants'] = {k: {x: y for x, y in v.items() if x != 'pred'}
                                for k, v in variants.items()}

    loao = variants['detrended + leave-one-author-out centring']
    print('\nE1  leave-one-author-out micro %.3f  (predicted > 0.40; pooled 0.499, raw 0.169)'
          % loao['micro'])

    owner = {w: au[nd][wk[nd] == w][0] for w in set(wk[nd])}
    nulls = perm_null(loao['pred'], wk[nd], owner, C.PANEL, rng, statistic='micro')
    nullsM = perm_null(loao['pred'], wk[nd], owner, C.PANEL, rng, statistic='macro')
    out['E2_null'] = {'micro_observed': loao['micro'], 'micro_null_mean': float(nulls.mean()),
                      'micro_null_p95': float(np.percentile(nulls, 95)),
                      'micro_p': float(np.mean(nulls >= loao['micro'])),
                      'macro_observed': loao['macro'], 'macro_null_mean': float(nullsM.mean()),
                      'macro_null_p95': float(np.percentile(nullsM, 95)),
                      'macro_p': float(np.mean(nullsM >= loao['macro']))}
    print('E2  null (%d permutations): micro mean %.3f p95 %.3f p=%.3f | macro mean %.3f p95 %.3f p=%.3f'
          % (N_NULL, nulls.mean(), np.percentile(nulls, 95), np.mean(nulls >= loao['micro']),
             nullsM.mean(), np.percentile(nullsM, 95), np.mean(nullsM >= loao['macro'])))
    print('    per author (leave-one-author-out):')
    for a in C.PANEL:
        print('      %-22s %.3f  (n=%d)' % (a, loao['per_author'][a], int((au[nd] == a).sum())))

    # ---- E3: within-register, computed on PANEL documents only (D's bug fixed) ----
    panel_docs = [d for d in docs if d['author'] in C.PANEL]
    Xp = D.vectors(panel_docs, vocab)
    yp = np.array([d['yr'] for d in panel_docs], float)
    wi_raw = within_loo_clean(Xp, yp, panel_docs, C.PANEL, 0)
    wi_det = within_loo_clean(Xp, yp, panel_docs, C.PANEL, 1)
    out['within_register_panel_only'] = {'untreated': wi_raw, 'detrended': wi_det}
    print('\nE3  within-register, 8-author documents only, leave-one-work-out:')
    print('      untreated  micro %.3f macro %.3f' % (wi_raw['micro'], wi_raw['macro']))
    print('      detrended  micro %.3f macro %.3f' % (wi_det['micro'], wi_det['macro']))
    print('      cross-register best (LOAO) micro %.3f macro %.3f'
          % (loao['micro'], loao['macro']))

    # ---- E4: the held-out pageants ----
    print('\nE4  held-out civic pageants (%d chunks), never used in A-D' % len(pg))
    trio = ['Middleton, Thomas', 'Heywood, Thomas', 'Jonson, Ben']
    pres = {}
    for tag, T in (('uncorrected', C.zscale(X, dmask)[pg]),
                   ('detrended, uncentred', Z[pg]),
                   ('detrended + pooled centring', Z[pg] - Z[pg].mean(0)),
                   ('detrended + leave-one-author-out centring',
                    loao_centre(Z, pg, au[pg], C.PANEL))):
        cc = c8 if tag != 'uncorrected' else np.stack(
            [C.zscale(X, dmask)[dmask & (au == a)].mean(0) for a in C.PANEL])
        pred = attribute(T, cc, C.PANEL)
        s = score(pred, au[pg], C.PANEL)
        ns = {a: int((au[pg] == a).sum()) for a in trio}
        hits = sum((s['per_author'][a] or 0) * ns[a] for a in trio)
        pres[tag] = {'micro': s['micro'], 'macro': s['macro'],
                     'per_author': s['per_author'],
                     'trio_recovery': hits / sum(ns.values()),
                     'trio_n': sum(ns.values())}
        print('   %-42s micro %.3f  trio %d chunks recovered %.3f'
              % (tag, s['micro'], sum(ns.values()), hits / sum(ns.values())))
    out['E4_pageants'] = pres
    print('   (2026-09-17 uncorrected trio recovery was 0.000 of 25; its power analysis')
    print('    bounded the true rate at about 0.10. E4 predicted > 0.10 after correction.)')
    print('   per author, leave-one-author-out centring:')
    best = pres['detrended + leave-one-author-out centring']
    for a in C.PANEL:
        n = int((au[pg] == a).sum())
        if n:
            print('      %-22s %.3f  (n=%d)' % (a, best['per_author'][a], n))

    C.save('expE_leakage.json', out)


if __name__ == '__main__':
    main()
