"""Experiment C - the sink is a direction, and centring it out does not save the method.

Two causes for the cross-register sink have now been proposed and killed:
prose-ness (2026-09-17, refuted by its own frozen predictions) and training-set
size (Experiment B, refuted by equalising it). This is the third, and it is
geometric rather than literary.

In drama-scaled z-space the drama cloud sits at the origin by construction. Write

    m = mean of the non-dramatic chunks in that space

for the REGISTER DISPLACEMENT: the direction and distance by which writing prose
instead of plays moves a document, shared by every author because it is a property
of the register and not of the man. Under L1 nearest-centroid a test document far
out along m is taken by whichever author's centroid lies furthest along m. If that
is what is happening then

  C1  absorption is predicted by cos(centroid, m) across the 27 authors
  C2  the pageants, a different register with a different m, are taken by a
      DIFFERENT author, and which one is predictable from their own direction -
      which is the 2026-09-17 finding that the sink's identity is unstable
  C3  subtracting the test register's own mean before attributing breaks the sink
  C4  and does NOT give the method back
  C5  and what it does give back is scored against a label-permutation null

C3 is the honest repair attempt. The displacement m is estimable without knowing
who wrote anything - it is the mean of the questioned corpus - so a practitioner
really could do this. The question is whether it helps.
"""
import sys, os, json, csv, collections, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import delta as D
from expB_equaln import load_pageants

N_NULL = 200


def pear(x, y):
    x, y = np.array(x, float), np.array(y, float)
    x, y = x - x.mean(), y - y.mean()
    return float((x * y).sum() / np.sqrt((x * x).sum() * (y * y).sum()))


def cosine(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def attribute(Z, cent, authors):
    return [authors[i] for i in
            np.abs(Z[:, None, :] - cent[None, :, :]).sum(2).argmin(1)]


def score(pred, true, panel):
    per = {}
    for a in panel:
        m = true == a
        per[a] = float(np.mean([p == a for p, k in zip(pred, m) if k])) if m.any() else None
    return {'micro': float(np.mean([p == t for p, t in zip(pred, true)])),
            'macro': float(np.mean([v for v in per.values() if v is not None])),
            'per_author': per}


def main():
    rng = random.Random(C.SEED)
    docs, _ = C.load()
    pag = load_pageants()
    allv = docs + pag
    vocab = D.vocabulary(docs)
    X = D.vectors(allv, vocab)
    au = np.array([d['author'] for d in allv])
    rg = np.array([d['register'] for d in allv])
    dmask = rg == 'drama'
    Z = C.zscale(X, dmask)
    authors = sorted(set(au[dmask]))
    cent = np.stack([Z[dmask & (au == a)].mean(0) for a in authors])

    nd = np.where(rg == 'nondrama')[0]
    pg = np.where(rg == 'pageant')[0]
    m_nd = Z[nd].mean(0)
    m_pg = Z[pg].mean(0)
    drama_mean = Z[dmask].mean(0)          # ~0 by construction; reported as a check

    out = {'n_authors': len(authors), 'n_nondrama': len(nd), 'n_pageant': len(pg),
           'drama_mean_L1': float(np.abs(drama_mean).sum()),
           'displacement_L1_nondrama': float(np.abs(m_nd).sum()),
           'displacement_L1_pageant': float(np.abs(m_pg).sum()),
           'cos_nondrama_pageant_directions': cosine(m_nd, m_pg)}
    print('register displacement in drama-scaled z-space (500 features)')
    print('  |drama mean|_1    = %8.2f   (0 by construction - sanity check)' % out['drama_mean_L1'])
    print('  |m_nondrama|_1    = %8.2f' % out['displacement_L1_nondrama'])
    print('  |m_pageant|_1     = %8.2f' % out['displacement_L1_pageant'])
    print('  cos(m_nondrama, m_pageant) = %+.3f' % out['cos_nondrama_pageant_directions'])

    pred_nd = attribute(Z[nd], cent, authors)
    pred_pg = attribute(Z[pg], cent, authors)
    share_nd = {a: float(np.mean([p == a for p in pred_nd])) for a in authors}
    share_pg = {a: float(np.mean([p == a for p in pred_pg])) for a in authors}
    cos_nd = {a: cosine(cent[i], m_nd) for i, a in enumerate(authors)}
    cos_pg = {a: cosine(cent[i], m_pg) for i, a in enumerate(authors)}
    proj_nd = {a: float(cent[i] @ m_nd / np.linalg.norm(m_nd)) for i, a in enumerate(authors)}

    c1 = pear([cos_nd[a] for a in authors], [share_nd[a] for a in authors])
    c2r = pear([cos_pg[a] for a in authors], [share_pg[a] for a in authors])
    out['C1_corr_cos_vs_absorption_nondrama'] = c1
    out['C2_corr_cos_vs_absorption_pageant'] = c2r
    out['C2_cos_pageant_peele'] = cos_pg['Peele, George']
    out['C2_cos_pageant_lyly'] = cos_pg['Lyly, John']
    out['C2_cos_nondrama_peele'] = cos_nd['Peele, George']
    out['C2_cos_nondrama_lyly'] = cos_nd['Lyly, John']
    out['corr_projection_vs_absorption_nondrama'] = pear(
        [proj_nd[a] for a in authors], [share_nd[a] for a in authors])

    print('\nC1  Pearson(cos(centroid, m_nondrama), non-dramatic share) = %+.3f   (predicted > +0.70)' % c1)
    print('    same with the unnormalised projection on m           = %+.3f' %
          out['corr_projection_vs_absorption_nondrama'])
    print('C2  Pearson(cos(centroid, m_pageant),  pageant share)      = %+.3f   (predicted > +0.70)' % c2r)
    print('    cos with m_pageant :  Peele %+.4f   Lyly %+.4f   (predicted Peele > Lyly)'
          % (cos_pg['Peele, George'], cos_pg['Lyly, John']))
    print('    cos with m_nondrama:  Peele %+.4f   Lyly %+.4f' 
          % (cos_nd['Peele, George'], cos_nd['Lyly, John']))

    print('\n%-24s %8s %8s %8s %8s' % ('author', 'cos m_nd', 'share_nd', 'cos m_pg', 'share_pg'))
    for a in sorted(authors, key=lambda a: -share_nd[a])[:12]:
        print('%-24s %+8.4f %7.1f%% %+8.4f %7.1f%%'
              % (a, cos_nd[a], 100 * share_nd[a], cos_pg[a], 100 * share_pg[a]))

    # ---- C3/C4: register-centring ----
    # Subtract the test register's own mean from every test document. This is
    # estimable in practice: it needs the questioned corpus, not its authorship.
    res = {}
    for tag, idx, mvec in (('nondrama', nd, m_nd), ('pageant', pg, m_pg)):
        Zc = Z[idx] - mvec
        p = attribute(Zc, cent, authors)
        sh = {a: float(np.mean([q == a for q in p])) for a in authors}
        s27 = score(p, au[idx], authors)
        s8 = score(p, au[idx], C.PANEL)
        res[tag] = {'share': sh, 'micro27': s27['micro'],
                    'macro8': s8['macro'], 'micro8': s8['micro'],
                    'per_author8': s8['per_author'],
                    'zeros': sum(1 for v in sh.values() if v == 0),
                    'hhi': float(sum(v * v for v in sh.values()))}
    out['register_centred'] = res
    out['uncentred_reference'] = {
        'nondrama': {'share_lyly': share_nd['Lyly, John'],
                     'macro8': score(pred_nd, au[nd], C.PANEL)['macro'],
                     'micro8': score(pred_nd, au[nd], C.PANEL)['micro'],
                     'hhi': float(sum(v * v for v in share_nd.values()))},
        'pageant': {'share_peele': share_pg['Peele, George'],
                    'hhi': float(sum(v * v for v in share_pg.values()))}}

    print('\nC3/C4  register-centring (subtract the test register\'s own mean)')
    print('   non-dramatic:  Lyly share %.1f%% -> %.1f%%   (C3 predicted < 15%%)'
          % (100 * share_nd['Lyly, John'], 100 * res['nondrama']['share']['Lyly, John']))
    print('                  concentration %.4f -> %.4f' %
          (out['uncentred_reference']['nondrama']['hhi'], res['nondrama']['hhi']))
    print('                  8-panel macro %.3f -> %.3f   (C4 predicted stays < 0.50)'
          % (out['uncentred_reference']['nondrama']['macro8'], res['nondrama']['macro8']))
    print('                  8-panel micro %.3f -> %.3f'
          % (out['uncentred_reference']['nondrama']['micro8'], res['nondrama']['micro8']))
    print('   pageants:      top absorber share %.1f%% -> concentration %.4f -> %.4f'
          % (100 * max(share_pg.values()), out['uncentred_reference']['pageant']['hhi'],
             res['pageant']['hhi']))
    print('   per-author, non-dramatic, register-centred (8-author panel):')
    for a in C.PANEL:
        print('      %-22s %.3f' % (a, res['nondrama']['per_author8'][a]))

    # ---- C5: label-permutation null for the centred run ----
    Zc = Z[nd] - m_nd
    works = sorted(set(allv[i]['work'] for i in nd))
    owner = {w: next(allv[i]['author'] for i in nd if allv[i]['work'] == w) for w in works}
    wk_nd = np.array([allv[i]['work'] for i in nd])
    p = attribute(Zc, np.stack([cent[authors.index(a)] for a in C.PANEL]), C.PANEL)
    obs = score(p, au[nd], C.PANEL)
    nulls = []
    for _ in range(N_NULL):
        perm = C.PANEL[:]
        rng.shuffle(perm)
        mp = dict(zip(C.PANEL, perm))
        fake = np.array([mp[owner[w]] if owner[w] in mp else owner[w] for w in wk_nd])
        nulls.append(score(p, fake, C.PANEL)['macro'])
    nulls = np.array(nulls)
    out['C5_null'] = {'n': N_NULL, 'observed_macro': obs['macro'],
                      'null_mean': float(nulls.mean()), 'p95': float(np.percentile(nulls, 95)),
                      'max': float(nulls.max()),
                      'p_one_sided': float(np.mean(nulls >= obs['macro']))}
    print('\nC5  register-centred, 8-author centroids only: macro %.3f' % obs['macro'])
    print('    %d author-label permutations: mean %.3f, p95 %.3f, max %.3f, p = %.3f'
          % (N_NULL, nulls.mean(), np.percentile(nulls, 95), nulls.max(),
             np.mean(nulls >= obs['macro'])))
    print('    within-register reference from 2026-09-17: macro 0.717')

    C.save('expC_mechanism.json', out)


if __name__ == '__main__':
    main()
