"""Experiment H - the third-register holdout the 2026-09-21 handover asked for.

Nothing in the method changes. The vocabulary, the drama-scaled z-space, the
year detrend fitted on drama only, the leave-one-WORK-out centring and the
work-blocked label-permutation null are all imported from the 2026-09-21 session
and run unchanged. The only new thing is the test set: 496 chunks of non-dramatic
writing by eleven panel dramatists who contributed NONE of the 943 chunks the
correction was developed on.

Treatments are reported as a decomposition rather than as the three rows of
expG, because on a new arm the interesting question is which half of the
correction travels:

    uncorrected          drama-scaled z, no treatment
    detrend only         year trend fitted on drama, removed from everything
    centre only          leave-one-work-out centring, no detrend
    detrend + centre     the 2026-09-21 correction as published

plus a permuted-year control on the last one, which separates "removing real
chronology helps" from "the detrend operation moves the number".
"""
import sys, os, json, collections, random
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P21 = os.path.join(HERE, '..', '..', '2026-09-21-period-detrend-and-equal-n', 'src')
sys.path.insert(0, P21)
import common as C                                             # noqa: E402
import delta as D                                              # noqa: E402
from expC_mechanism import attribute, score                    # noqa: E402
from expG_authorblind import low_centre                        # noqa: E402

N_NULL = 1000
SEED = 20260923
DATA = os.path.join(HERE, '..', 'data')
RESULTS = os.path.join(HERE, '..', 'results')


def load_holdout():
    docs = json.load(open(os.path.join(DATA, 'holdout_chunks.json')))
    for d in docs:
        d['yr'] = int(str(d['year'])[:4])
    return docs


def treatments(X, years, dmask, idx, works, rng_years=None):
    """Return {tag: (centroids, test matrix)} for the four treatments."""
    Zraw = C.zscale(X, dmask)
    yr = years if rng_years is None else rng_years
    Zdet = C.zscale(C.detrend(X, yr, dmask, degree=1), dmask)
    return {
        'uncorrected': (Zraw, Zraw[idx]),
        'detrend only': (Zdet, Zdet[idx]),
        'centre only': (Zraw, low_centre(Zraw, idx, works)),
        'detrend + centre': (Zdet, low_centre(Zdet, idx, works)),
    }


def run(docs_train, test, panel, rng, tag_prefix='', subset=None):
    allv = docs_train + test
    vocab = D.vocabulary(docs_train)
    X = D.vectors(allv, vocab)
    years = np.array([d['yr'] for d in allv], float)
    au = np.array([d['author'] for d in allv])
    rg = np.array([d['register'] for d in allv])
    wk = np.array([d['work'] for d in allv])
    dmask = rg == 'drama'
    idx = np.where(rg == 'nondrama_holdout')[0]
    if subset is not None:
        keep = np.array([bool(allv[i].get(subset)) for i in idx])
        idx = idx[keep]
    present = [a for a in panel if (au[idx] == a).any()]
    owner = {w: au[idx][wk[idx] == w][0] for w in set(wk[idx])}
    out = {'n_chunks': int(len(idx)), 'n_authors': len(present),
           'present': present, 'chance': 1.0 / len(panel),
           'per_author_n': {a: int((au[idx] == a).sum()) for a in present}}
    tr = treatments(X, years, dmask, idx, wk[idx])
    for tag, (Z, T) in tr.items():
        cent = np.stack([Z[dmask & (au == a)].mean(0) for a in panel])
        pred = attribute(T, cent, panel)
        s = score(pred, au[idx], present)
        sh = collections.Counter(pred)
        rec = {'micro': s['micro'], 'macro': s['macro'],
               'max_share': float(max(sh.values()) / len(pred)),
               'top_absorber': sh.most_common(1)[0][0],
               'shares': {a: n / len(pred) for a, n in sh.most_common(6)},
               'per_author': s['per_author']}
        nl = []
        for _ in range(N_NULL):
            p = present[:]
            rng.shuffle(p)
            mp = dict(zip(present, p))
            fake = np.array([mp[owner[w]] for w in wk[idx]])
            nl.append(score(pred, fake, present)['micro'])
        nl = np.array(nl)
        rec['null'] = {'mean': float(nl.mean()), 'p95': float(np.percentile(nl, 95)),
                       'p': float((np.sum(nl >= rec['micro']) + 1) / (len(nl) + 1)),
                       'n_distinct_perm_floor': 1.0 / max(1, len(nl))}
        out[tag] = rec
    # permuted-year control on the published correction
    yrs = years.copy()
    perm = yrs[~dmask].copy()
    rng.shuffle(perm)
    yrs[~dmask] = perm
    dperm = yrs.copy()
    dperm[dmask] = years[dmask]
    trp = treatments(X, years, dmask, idx, wk[idx], rng_years=dperm)
    Z, T = trp['detrend + centre']
    cent = np.stack([Z[dmask & (au == a)].mean(0) for a in panel])
    s = score(attribute(T, cent, panel), au[idx], present)
    out['detrend + centre (test years permuted)'] = {'micro': s['micro'], 'macro': s['macro']}
    return out


def main():
    rng = random.Random(SEED)
    docs_full, _ = C.load()
    test = load_holdout()
    panel = sorted(set(d['author'] for d in docs_full if d['register'] == 'drama'))
    os.makedirs(RESULTS, exist_ok=True)
    out = {}
    for name, sub in (('holdout', None), ('holdout|named_on_title', 'named_on_title')):
        r = run(docs_full, test, panel, rng, subset=sub)
        out[name] = r
        print('\n=== %s: %d chunks, %d authors, %d-author panel (chance %.3f)'
              % (name, r['n_chunks'], r['n_authors'], len(panel), r['chance']))
        print('   %-34s %7s %7s %8s %-18s %7s' %
              ('treatment', 'micro', 'macro', 'maxshr', 'top absorber', 'null p'))
        for tag in ('uncorrected', 'detrend only', 'centre only', 'detrend + centre'):
            b = r[tag]
            print('   %-34s %7.3f %7.3f %7.1f%% %-18s %7.3f'
                  % (tag, b['micro'], b['macro'], 100 * b['max_share'],
                     b['top_absorber'][:18], b['null']['p']))
        pc = r['detrend + centre (test years permuted)']
        print('   %-34s %7.3f %7.3f   (control)' % ('detrend + centre, years permuted',
                                                    pc['micro'], pc['macro']))
        print('   per author, detrend + centre:')
        b = r['detrend + centre']
        for a in r['present']:
            print('      %-22s %.3f  (n=%d, uncorrected %.3f)'
                  % (a, b['per_author'][a], r['per_author_n'][a],
                     r['uncorrected']['per_author'][a]))
    json.dump(out, open(os.path.join(RESULTS, 'expH_holdout.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
