"""Experiment B - is the Lyly sink style, or is it centroid noise?

2026-09-17 found cross-register attribution collapsing onto one author: 41.0% of
943 non-dramatic chunks went to Lyly on the 27-author panel and twelve dramatists
absorbed nothing at all. It also found absorption correlating with training-set
size at -0.438 and with centroid L1 norm at +0.611, and correctly declined to
name a cause.

There is a mechanical reason those two correlations could be the whole story. A
centroid is a mean of n z-scored chunk vectors. Under sampling noise its squared
distance from the origin carries a term of order 1/n, so an author trained on 41
chunks sits systematically further from the centre of the drama cloud than one
trained on 251 - in a direction that is noise, not style. Test documents that lie
far outside the drama cloud, which is exactly what out-of-register documents are,
are then picked up preferentially by whichever centroid the noise pushed towards
them. Nothing about prose or style is required.

The test: give every author the same number of training chunks and see what is
left. Training-set size is the only thing that changes; the feature space, the
scaling, the test documents and the distance are all held fixed.

  B1  Lyly's share falls below 25% (from 41.0%)
  B2  authors absorbing exactly zero falls below 12
  B3  concentration falls below 0.1550 (from 0.2324)
  B4  8-author cross-register macro stays below 0.50 - the load-bearing one;
      B1-B3 can all hold and the register gap still be fatal
  B5  a label-permutation null concentrates LESS than the real equal-N run
  B6  Middleton+Heywood+Jonson recover under 25% of their own pageant chunks

Every statistic is averaged over REPS independent subsamples, because a single
subsample of 41 is itself noisy and quoting one would repeat the error being
diagnosed.
"""
import sys, os, json, csv, collections, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import delta as D
import tcp
from build_corpus import PAGEANTS, AUTH, chunks as chunkify

REPS = 50


def hhi(share):
    return float(sum(v * v for v in share.values()))


def run_once(Z, au, dmask, authors, N, rng, targets):
    """Build equal-N centroids and attribute each target block."""
    idx = {a: np.where(dmask & (au == a))[0] for a in authors}
    sel = np.concatenate([rng.sample(list(idx[a]), N) for a in authors])
    lab = np.concatenate([[a] * N for a in authors])
    cent = np.stack([Z[sel[lab == a]].mean(0) for a in authors])
    out = {}
    for name, (tidx, ttrue) in targets.items():
        pred = [authors[i] for i in
                np.abs(Z[tidx][:, None, :] - cent[None, :, :]).sum(2).argmin(1)]
        share = {a: float(np.mean([p == a for p in pred])) for a in authors}
        per = {}
        for a in set(ttrue):
            m = ttrue == a
            per[a] = float(np.mean([p == a for p, k in zip(pred, m) if k]))
        out[name] = {'share': share, 'per_author': per,
                     'hhi': hhi(share),
                     'zeros': sum(1 for v in share.values() if v == 0),
                     'micro': float(np.mean([p == t for p, t in zip(pred, ttrue)]))}
    out['centroid_norms'] = {a: float(np.abs(cent[i]).sum()) for i, a in enumerate(authors)}
    return out


def load_pageants():
    rows = {r['TCP']: r for r in csv.DictReader(
        open('/tmp/w/TCP.csv', encoding='utf-8', errors='replace'))}
    pag = []
    for tid in PAGEANTS:
        r = rows[tid]
        w, _ = tcp.words_with_damage(tcp.raw(tid))
        for j, c in enumerate(chunkify(w)):
            pag.append({'id': '%s#%d' % (tid, j), 'author': AUTH[r['Author']],
                        'register': 'pageant', 'work': tid, 'year': r['Date'], 'words': c})
    return pag


def main():
    rng = random.Random(C.SEED)
    docs, _ = C.load()
    pag = load_pageants()
    allv = docs + pag
    vocab = D.vocabulary(docs)                       # as in wide_panel.py
    X = D.vectors(allv, vocab)
    au = np.array([d['author'] for d in allv])
    rg = np.array([d['register'] for d in allv])
    dmask = rg == 'drama'
    Z = C.zscale(X, dmask)                           # scale once, on all drama
    authors = sorted(set(au[dmask]))
    N = min(int((dmask & (au == a)).sum()) for a in authors)
    nd = np.where(rg == 'nondrama')[0]
    pg = np.where(rg == 'pageant')[0]
    targets = {'nondrama': (nd, au[nd]), 'pageant': (pg, au[pg])}
    print('27 authors, equal-N = %d training chunks each (%d of %d drama chunks used)'
          % (N, N * len(authors), int(dmask.sum())))
    print('targets: %d non-dramatic chunks, %d pageant chunks' % (len(nd), len(pg)))

    # ---- full-training reference, same code path, N = everything ----
    idx = {a: np.where(dmask & (au == a))[0] for a in authors}
    cent_full = np.stack([Z[idx[a]].mean(0) for a in authors])
    ref = {}
    for name, (tidx, ttrue) in targets.items():
        pred = [authors[i] for i in
                np.abs(Z[tidx][:, None, :] - cent_full[None, :, :]).sum(2).argmin(1)]
        share = {a: float(np.mean([p == a for p in pred])) for a in authors}
        per = {}
        for a in set(ttrue):
            m = ttrue == a
            per[a] = float(np.mean([p == a for p, k in zip(pred, m) if k]))
        ref[name] = {'share': share, 'per_author': per, 'hhi': hhi(share),
                     'zeros': sum(1 for v in share.values() if v == 0),
                     'micro': float(np.mean([p == t for p, t in zip(pred, ttrue)]))}
    ref['centroid_norms'] = {a: float(np.abs(cent_full[i]).sum()) for i, a in enumerate(authors)}

    # ---- equal-N, REPS replicates ----
    reps = [run_once(Z, au, dmask, authors, N, rng, targets) for _ in range(REPS)]

    # ---- null: author labels shuffled among drama chunks, then equal-N ----
    nulls = []
    for _ in range(REPS):
        fake = au.copy()
        d = np.where(dmask)[0]
        lab = list(au[d])
        rng.shuffle(lab)
        fake[d] = lab
        nulls.append(run_once(Z, fake, dmask, authors, N, rng, targets))

    def agg(rs, block, key):
        return np.array([r[block][key] for r in rs])

    def agg_share(rs, block, a):
        return np.array([r[block]['share'][a] for r in rs])

    def macro8(r, block):
        return float(np.mean([r[block]['per_author'][a] for a in C.PANEL
                              if a in r[block]['per_author']]))

    out = {'N': N, 'reps': REPS, 'authors': authors,
           'full_training': {k: v for k, v in ref.items()},
           'equal_n': {}, 'null_shuffled_labels': {}}

    print('\n%-22s %12s %14s %14s' % ('statistic', 'full-train', 'equal-N mean', 'null mean'))
    print('-' * 66)
    rowspec = [
        ('Lyly share (nondram)', ref['nondrama']['share']['Lyly, John'],
         agg_share(reps, 'nondrama', 'Lyly, John'), agg_share(nulls, 'nondrama', 'Lyly, John')),
        ('concentration HHI', ref['nondrama']['hhi'],
         agg(reps, 'nondrama', 'hhi'), agg(nulls, 'nondrama', 'hhi')),
        ('authors absorbing 0', ref['nondrama']['zeros'],
         agg(reps, 'nondrama', 'zeros'), agg(nulls, 'nondrama', 'zeros')),
        ('nondram micro (27)', ref['nondrama']['micro'],
         agg(reps, 'nondrama', 'micro'), agg(nulls, 'nondrama', 'micro')),
        ('8-panel macro', macro8(ref, 'nondrama'),
         np.array([macro8(r, 'nondrama') for r in reps]),
         np.array([macro8(r, 'nondrama') for r in nulls])),
        ('pageant HHI', ref['pageant']['hhi'],
         agg(reps, 'pageant', 'hhi'), agg(nulls, 'pageant', 'hhi')),
        ('pageant micro', ref['pageant']['micro'],
         agg(reps, 'pageant', 'micro'), agg(nulls, 'pageant', 'micro')),
    ]
    for name, f, e, n in rowspec:
        print('%-22s %12.4f %8.4f+-%.4f %8.4f+-%.4f'
              % (name, f, e.mean(), e.std(), n.mean(), n.std()))
        out['equal_n'][name] = {'mean': float(e.mean()), 'sd': float(e.std()),
                                'p5': float(np.percentile(e, 5)),
                                'p95': float(np.percentile(e, 95))}
        out['null_shuffled_labels'][name] = {'mean': float(n.mean()), 'sd': float(n.std())}
        out.setdefault('full_training_scalars', {})[name] = float(f)

    # ---- B6: own-pageant recovery under equal-N ----
    print('\nB6  own-pageant recovery, full training vs equal-N')
    b6 = {}
    for a in ('Middleton, Thomas', 'Heywood, Thomas', 'Jonson, Ben', 'Dekker, Thomas'):
        f = ref['pageant']['per_author'].get(a)
        e = np.array([r['pageant']['per_author'][a] for r in reps])
        n = np.array([r['pageant']['per_author'][a] for r in nulls])
        b6[a] = {'full': f, 'equal_n_mean': float(e.mean()), 'equal_n_sd': float(e.std()),
                 'null_mean': float(n.mean())}
        print('   %-20s full %.3f   equal-N %.3f +- %.3f   null %.3f'
              % (a, f, e.mean(), e.std(), n.mean()))
    trio = ['Middleton, Thomas', 'Heywood, Thomas', 'Jonson, Ben']
    ns = {a: int((au[pg] == a).sum()) for a in trio}
    comb_full = sum(ref['pageant']['per_author'][a] * ns[a] for a in trio) / sum(ns.values())
    comb_e = np.array([sum(r['pageant']['per_author'][a] * ns[a] for a in trio) / sum(ns.values())
                       for r in reps])
    b6['combined_trio'] = {'n_chunks': sum(ns.values()), 'full': comb_full,
                           'equal_n_mean': float(comb_e.mean()),
                           'equal_n_sd': float(comb_e.std()),
                           'equal_n_p95': float(np.percentile(comb_e, 95))}
    print('   combined %d chunks: full %.3f   equal-N %.3f +- %.3f  (p95 %.3f)'
          % (sum(ns.values()), comb_full, comb_e.mean(), comb_e.std(),
             np.percentile(comb_e, 95)))
    out['B6'] = b6

    # ---- the mechanism: centroid norm vs training size, before and after ----
    sizes = {a: int((dmask & (au == a)).sum()) for a in authors}
    nf = [ref['centroid_norms'][a] for a in authors]
    ne = [float(np.mean([r['centroid_norms'][a] for r in reps])) for a in authors]
    sh_f = [ref['nondrama']['share'][a] for a in authors]
    sh_e = [float(agg_share(reps, 'nondrama', a).mean()) for a in authors]
    sz = [sizes[a] for a in authors]

    def pear(x, y):
        x, y = np.array(x, float), np.array(y, float)
        x, y = x - x.mean(), y - y.mean()
        return float((x * y).sum() / np.sqrt((x * x).sum() * (y * y).sum()))
    out['mechanism'] = {
        'sizes': sizes,
        'corr_size_vs_norm_full': pear(sz, nf),
        'corr_size_vs_norm_equalN': pear(sz, ne),
        'corr_norm_vs_absorption_full': pear(nf, sh_f),
        'corr_norm_vs_absorption_equalN': pear(ne, sh_e),
        'corr_size_vs_absorption_full': pear(sz, sh_f),
        'corr_size_vs_absorption_equalN': pear(sz, sh_e),
        'centroid_norm_full': ref['centroid_norms'],
        'centroid_norm_equalN': dict(zip(authors, ne))}
    print('\nmechanism (Pearson over 27 authors)        full-train   equal-N')
    for k, a, b in (('training size vs centroid norm',
                     out['mechanism']['corr_size_vs_norm_full'],
                     out['mechanism']['corr_size_vs_norm_equalN']),
                    ('centroid norm vs absorption',
                     out['mechanism']['corr_norm_vs_absorption_full'],
                     out['mechanism']['corr_norm_vs_absorption_equalN']),
                    ('training size vs absorption',
                     out['mechanism']['corr_size_vs_absorption_full'],
                     out['mechanism']['corr_size_vs_absorption_equalN'])):
        print('   %-38s %+8.3f  %+8.3f' % (k, a, b))

    print('\nequal-N non-dramatic shares (mean over %d subsamples), top 10:' % REPS)
    order = sorted(authors, key=lambda a: -agg_share(reps, 'nondrama', a).mean())
    for a in order[:10]:
        print('   %-24s full %5.1f%%   equal-N %5.1f%%   null %5.1f%%'
              % (a, 100 * ref['nondrama']['share'][a],
                 100 * agg_share(reps, 'nondrama', a).mean(),
                 100 * agg_share(nulls, 'nondrama', a).mean()))
    out['equal_n_shares'] = {a: float(agg_share(reps, 'nondrama', a).mean()) for a in authors}
    out['null_shares'] = {a: float(agg_share(nulls, 'nondrama', a).mean()) for a in authors}
    C.save('expB_equaln.json', out)


if __name__ == '__main__':
    main()
