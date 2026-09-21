"""Experiment F - the consolidated table, at BOTH panel sizes.

E4 compared the corrected pageant arm against the 2026-09-17 figure without
noticing that E4 used eight candidate authors and 2026-09-17 used twenty-seven.
Going from 27 candidates to 8 is itself worth a large accuracy gain and has
nothing to do with any correction. Everything is therefore recomputed at both
panel sizes, with the uncorrected cell at each size as its own baseline, so no
comparison crosses that boundary.

Reported for each (panel size x target register x treatment): micro, macro over
the authors present, the sink's largest share, and - for the pageants - the
recovery by Middleton, Heywood and Jonson of their own 25 chunks, which is the
number the 2026-09-17 power analysis bounded at about 0.10.
"""
import sys, os, json, collections, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import delta as D
from expC_mechanism import attribute, score
from expB_equaln import load_pageants
from expE_leakage import loao_centre

N_NULL = 200
TRIO = ['Middleton, Thomas', 'Heywood, Thomas', 'Jonson, Ben']


def main():
    rng = random.Random(C.SEED)
    docs_full, _ = C.load()
    docs, _ = C.load(require_year=True)
    pag = load_pageants()
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
    authors27 = sorted(set(au[dmask]))

    Zraw = C.zscale(X, dmask)
    Zdet = C.zscale(C.detrend(X, years, dmask, degree=1), dmask)
    out = {'note': 'both panel sizes; no comparison crosses panel size'}

    for panel_name, panel in (('8-author', C.PANEL), ('27-author', authors27)):
        cr = np.stack([Zraw[dmask & (au == a)].mean(0) for a in panel])
        cd = np.stack([Zdet[dmask & (au == a)].mean(0) for a in panel])
        for tgt_name, idx in (('nondrama', nd), ('pageant', pg)):
            present = [a for a in panel if (au[idx] == a).any()]
            print('\n=== %s panel, target = %s (%d chunks, %d of %d authors present, chance %.3f)'
                  % (panel_name, tgt_name, len(idx), len(present), len(panel), 1 / len(panel)))
            print('   %-44s %7s %7s %8s %9s' %
                  ('treatment', 'micro', 'macro', 'maxshare', 'trio' if tgt_name == 'pageant' else ''))
            block = {}
            for tag, Zc, cc, T in (
                    ('uncorrected', Zraw, cr, Zraw[idx]),
                    ('detrended', Zdet, cd, Zdet[idx]),
                    ('register-centred only', Zraw, cr, Zraw[idx] - Zraw[idx].mean(0)),
                    ('detrended + pooled centring', Zdet, cd, Zdet[idx] - Zdet[idx].mean(0)),
                    ('detrended + LOAO centring', Zdet, cd, loao_centre(Zdet, idx, au[idx], panel))):
                pred = attribute(T, cc, panel)
                s = score(pred, au[idx], present)
                sh = collections.Counter(pred)
                maxshare = max(sh.values()) / len(pred)
                rec = {'micro': s['micro'], 'macro': s['macro'],
                       'max_share': float(maxshare),
                       'top_absorber': sh.most_common(1)[0][0],
                       'per_author': s['per_author']}
                if tgt_name == 'pageant':
                    ns = {a: int((au[idx] == a).sum()) for a in TRIO}
                    rec['trio_recovery'] = sum((s['per_author'].get(a) or 0) * ns[a]
                                               for a in TRIO) / sum(ns.values())
                    rec['trio_n'] = sum(ns.values())
                block[tag] = rec
                print('   %-44s %7.3f %7.3f %7.1f%% %9s' %
                      (tag, s['micro'], s['macro'], 100 * maxshare,
                       ('%.3f' % rec['trio_recovery']) if tgt_name == 'pageant' else ''))
            # null for the best treatment
            best = 'detrended + LOAO centring'
            T = loao_centre(Zdet, idx, au[idx], panel)
            pred = attribute(T, cd, panel)
            owner = {w: au[idx][wk[idx] == w][0] for w in set(wk[idx])}
            nl = []
            for _ in range(N_NULL):
                p = present[:]
                rng.shuffle(p)
                mp = dict(zip(present, p))
                fake = np.array([mp[owner[w]] for w in wk[idx]])
                nl.append(score(pred, fake, present)['micro'])
            nl = np.array(nl)
            block[best]['null'] = {'mean': float(nl.mean()),
                                   'p95': float(np.percentile(nl, 95)),
                                   'p': float(np.mean(nl >= block[best]['micro']))}
            print('   null for the best row (%d permutations of author labels over works):'
                  % N_NULL)
            print('      micro null mean %.3f, p95 %.3f  ->  observed %.3f, p = %.3f'
                  % (nl.mean(), np.percentile(nl, 95), block[best]['micro'],
                     np.mean(nl >= block[best]['micro'])))
            out['%s|%s' % (panel_name, tgt_name)] = block

    C.save('expF_final.json', out)


if __name__ == '__main__':
    main()
