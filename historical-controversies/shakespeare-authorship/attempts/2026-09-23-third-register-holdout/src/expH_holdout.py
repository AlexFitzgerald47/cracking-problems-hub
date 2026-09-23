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
        # Global centring uses the mean of the WHOLE questioned arm, so unlike
        # leave-one-work-out it contains no term in the test chunk's own author.
        # If the two agree, the LOWO gain is not the own-author amplification
        # that the 2026-09-21 session measured for the leave-one-author-out
        # variant, reappearing at work level.
        'detrend + global centre': (Zdet, Zdet[idx] - Zdet[idx].mean(0)),
    }


def run(docs_train, test, panel, rng, vocab_docs=None, subset=None):
    allv = docs_train + test
    vocab = D.vocabulary(vocab_docs if vocab_docs is not None else docs_train)
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
        nrng = random.Random(SEED)           # per-treatment seed: the printed
        for _ in range(N_NULL):              # p-values do not depend on run order
            p = present[:]
            nrng.shuffle(p)
            mp = dict(zip(present, p))
            fake = np.array([mp[owner[w]] for w in wk[idx]])
            nl.append(score(pred, fake, present)['micro'])
        nl = np.array(nl)
        rec['null'] = {'mean': float(nl.mean()), 'p95': float(np.percentile(nl, 95)),
                       'p': float((np.sum(nl >= rec['micro']) + 1) / (len(nl) + 1)),
                       'n_distinct_perm_floor': 1.0 / max(1, len(nl))}
        out[tag] = rec
    # How much date resolution does the detrend actually need? Give every test
    # chunk the arm's MEAN year instead of its own: the arm's period offset from
    # the drama training set is kept, all within-arm date variation is destroyed.
    ym = years.copy()
    ym[idx] = years[idx].mean()
    trm = treatments(X, years, dmask, idx, wk[idx], rng_years=ym)
    Z, T = trm['detrend + centre']
    cent = np.stack([Z[dmask & (au == a)].mean(0) for a in panel])
    s = score(attribute(T, cent, panel), au[idx], present)
    out['detrend + centre (test dated at arm mean year)'] = {
        'micro': s['micro'], 'macro': s['macro'],
        'arm_mean_year': float(years[idx].mean())}

    # Permuted-year control on the published correction, averaged over 20 draws:
    # a single permutation of 496 years is noisy enough to move the number by
    # 0.02 between runs, which is the size of effect being discussed.
    mics, macs = [], []
    prng = random.Random(SEED + 1)
    for _ in range(20):
        yrs = years.copy()
        perm = yrs[idx].copy()
        prng.shuffle(perm)
        yrs[idx] = perm
        trp = treatments(X, years, dmask, idx, wk[idx], rng_years=yrs)
        Z, T = trp['detrend + centre']
        cent = np.stack([Z[dmask & (au == a)].mean(0) for a in panel])
        s = score(attribute(T, cent, panel), au[idx], present)
        mics.append(s['micro']); macs.append(s['macro'])
    out['detrend + centre (test years permuted)'] = {
        'micro': float(np.mean(mics)), 'macro': float(np.mean(macs)),
        'micro_sd': float(np.std(mics)), 'n_draws': len(mics),
        'micro_min': float(np.min(mics)), 'micro_max': float(np.max(mics))}
    return out


def original_arm(docs, docs_full, panel, rng):
    """The same four-way decomposition on the 943-chunk arm the correction was
    developed on. expG reported only three rows and never separated the two
    halves of the correction, so whether they are additive there is unknown."""
    test = [d for d in docs if d['register'] == 'nondrama']
    train = [d for d in docs if d['register'] == 'drama']
    for d in test:
        d = d
    allv = train + [dict(d, register='nondrama_holdout') for d in test]
    return run(allv[:len(train)], allv[len(train):], panel, rng, vocab_docs=docs_full)


def main():
    rng = random.Random(SEED)
    docs_full, _ = C.load()                 # vocabulary set, exactly as expG
    docs, dropped = C.load(require_year=True)   # analysis set, exactly as expG
    print('training chunks %d (%d dropped for want of a year)' % (len(docs), dropped))
    test = load_holdout()
    panel = sorted(set(d['author'] for d in docs_full if d['register'] == 'drama'))
    os.makedirs(RESULTS, exist_ok=True)
    out = {}
    for name, sub in (('holdout', None), ('holdout|named_on_title', 'named_on_title')):
        r = run(docs, test, panel, rng, vocab_docs=docs_full, subset=sub)
        out[name] = r
        print('\n=== %s: %d chunks, %d authors, %d-author panel (chance %.3f)'
              % (name, r['n_chunks'], r['n_authors'], len(panel), r['chance']))
        print('   %-34s %7s %7s %8s %-18s %7s' %
              ('treatment', 'micro', 'macro', 'maxshr', 'top absorber', 'null p'))
        for tag in ('uncorrected', 'detrend only', 'centre only', 'detrend + centre',
                    'detrend + global centre'):
            b = r[tag]
            print('   %-34s %7.3f %7.3f %7.1f%% %-18s %7.3f'
                  % (tag, b['micro'], b['macro'], 100 * b['max_share'],
                     b['top_absorber'][:18], b['null']['p']))
        am = r['detrend + centre (test dated at arm mean year)']
        print('   %-34s %7.3f %7.3f   (all test dates set to %.0f)'
              % ('detrend + centre, one arm date', am['micro'], am['macro'],
                 am['arm_mean_year']))
        pc = r['detrend + centre (test years permuted)']
        print('   %-34s %7.3f %7.3f   (mean of %d draws, sd %.3f, range %.3f-%.3f)'
              % ('detrend + centre, years permuted', pc['micro'], pc['macro'],
                 pc['n_draws'], pc['micro_sd'], pc['micro_min'], pc['micro_max']))
        print('   per author, detrend + centre:')
        b = r['detrend + centre']
        for a in r['present']:
            print('      %-22s %.3f  (n=%d, uncorrected %.3f)'
                  % (a, b['per_author'][a], r['per_author_n'][a],
                     r['uncorrected']['per_author'][a]))
    r = original_arm(docs, docs_full, panel, rng)
    out['original_arm_943'] = r
    print('\n=== original 943-chunk arm, same decomposition (audit of expG)')
    print('   %-34s %7s %7s %8s %-18s %7s' %
          ('treatment', 'micro', 'macro', 'maxshr', 'top absorber', 'null p'))
    for tag in ('uncorrected', 'detrend only', 'centre only', 'detrend + centre',
                'detrend + global centre'):
        b = r[tag]
        print('   %-34s %7.3f %7.3f %7.1f%% %-18s %7.3f'
              % (tag, b['micro'], b['macro'], 100 * b['max_share'],
                 b['top_absorber'][:18], b['null']['p']))
    am = r['detrend + centre (test dated at arm mean year)']
    print('   %-34s %7.3f %7.3f   (all test dates set to %.0f)'
          % ('detrend + centre, one arm date', am['micro'], am['macro'],
             am['arm_mean_year']))
    pc = r['detrend + centre (test years permuted)']
    print('   %-34s %7.3f %7.3f   (mean of %d draws, sd %.3f, range %.3f-%.3f)'
          % ('detrend + centre, years permuted', pc['micro'], pc['macro'],
             pc['n_draws'], pc['micro_sd'], pc['micro_min'], pc['micro_max']))
    json.dump(out, open(os.path.join(RESULTS, 'expH_holdout.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
