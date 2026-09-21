"""Experiment G - centring that never uses author grouping.

Leave-one-WORK-out centring: subtract from each test chunk the mean of every test
chunk belonging to a different work. Works are known without knowing authorship -
a pamphlet is a pamphlet - so this is available to a practitioner holding only a
reference corpus in the questioned register.

Reported at both panel sizes and on both target registers, always against the
uncorrected cell at the same panel size.
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


def low_centre(Z, idx, works):
    """Leave-one-WORK-out centring. No author information used."""
    T = np.empty_like(Z[idx])
    for w in set(works):
        own = works == w
        other = ~own
        T[own] = Z[idx][own] - (Z[idx][other].mean(0) if other.any() else 0.0)
    return T


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
    out = {}

    # amplification multipliers, for the record
    N = len(nd)
    amp = {a: float(int((au[nd] == a).sum()) / (N - int((au[nd] == a).sum())))
           for a in C.PANEL}
    out['loao_amplification_multiplier'] = amp
    print('leave-one-author-out amplification multiplier n_a/(N-n_a), N = %d:' % N)
    for a in sorted(amp, key=lambda a: -amp[a]):
        print('   %-22s %6.3f  (n=%d)' % (a, amp[a], int((au[nd] == a).sum())))

    for panel_name, panel in (('8-author', C.PANEL), ('27-author', authors27)):
        cd = np.stack([Zdet[dmask & (au == a)].mean(0) for a in panel])
        cr = np.stack([Zraw[dmask & (au == a)].mean(0) for a in panel])
        for tgt_name, idx in (('nondrama', nd), ('pageant', pg)):
            present = [a for a in panel if (au[idx] == a).any()]
            print('\n=== %s panel, %s (%d chunks, chance %.3f)'
                  % (panel_name, tgt_name, len(idx), 1 / len(panel)))
            print('   %-46s %7s %7s %8s %8s' %
                  ('treatment', 'micro', 'macro', 'maxshr',
                   'trio' if tgt_name == 'pageant' else ''))
            block = {}
            for tag, cc, T in (
                    ('uncorrected', cr, Zraw[idx]),
                    ('detrended + author-blind LOWO centring', cd,
                     low_centre(Zdet, idx, wk[idx])),
                    ('detrended + leave-one-AUTHOR-out centring', cd,
                     loao_centre(Zdet, idx, au[idx], panel))):
                pred = attribute(T, cc, panel)
                s = score(pred, au[idx], present)
                sh = collections.Counter(pred)
                rec = {'micro': s['micro'], 'macro': s['macro'],
                       'max_share': float(max(sh.values()) / len(pred)),
                       'top_absorber': sh.most_common(1)[0][0],
                       'per_author': s['per_author']}
                if tgt_name == 'pageant':
                    ns = {a: int((au[idx] == a).sum()) for a in TRIO}
                    rec['trio_recovery'] = sum((s['per_author'].get(a) or 0) * ns[a]
                                               for a in TRIO) / sum(ns.values())
                block[tag] = rec
                print('   %-46s %7.3f %7.3f %7.1f%% %8s'
                      % (tag, s['micro'], s['macro'], 100 * rec['max_share'],
                         ('%.3f' % rec['trio_recovery']) if tgt_name == 'pageant' else ''))
            key = 'detrended + author-blind LOWO centring'
            pred = attribute(low_centre(Zdet, idx, wk[idx]), cd, panel)
            owner = {w: au[idx][wk[idx] == w][0] for w in set(wk[idx])}
            nl = []
            for _ in range(N_NULL):
                p = present[:]
                rng.shuffle(p)
                mp = dict(zip(present, p))
                fake = np.array([mp[owner[w]] for w in wk[idx]])
                nl.append(score(pred, fake, present)['micro'])
            nl = np.array(nl)
            block[key]['null'] = {'mean': float(nl.mean()),
                                  'p95': float(np.percentile(nl, 95)),
                                  'p': float(np.mean(nl >= block[key]['micro']))}
            print('   null for the author-blind row: mean %.3f p95 %.3f -> observed %.3f p=%.3f'
                  % (nl.mean(), np.percentile(nl, 95), block[key]['micro'],
                     np.mean(nl >= block[key]['micro'])))
            if tgt_name == 'nondrama':
                print('   per author (author-blind):')
                for a in present:
                    print('      %-22s %.3f  (n=%d)'
                          % (a, block[key]['per_author'][a], int((au[idx] == a).sum())))
            out['%s|%s' % (panel_name, tgt_name)] = block

    b = out['27-author|nondrama']
    g1 = b['detrended + author-blind LOWO centring']['micro']
    print('\nG1  author-blind 27-panel non-dramatic micro = %.3f  (predicted > 0.30)' % g1)
    print('G3  uncorrected %.3f -> author-blind %.3f -> leave-one-author-out %.3f'
          % (b['uncorrected']['micro'], g1,
             b['detrended + leave-one-AUTHOR-out centring']['micro']))
    print('    gap blind-to-uncorrected %.3f   gap LOAO-to-blind %.3f  (G3: second < first)'
          % (g1 - b['uncorrected']['micro'],
             b['detrended + leave-one-AUTHOR-out centring']['micro'] - g1))
    C.save('expG_authorblind.json', out)


if __name__ == '__main__':
    main()
