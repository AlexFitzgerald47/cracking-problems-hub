"""Where do the corrected predictions go for the authors the correction misses?

The board's prediction-sink rule says to tabulate where predictions land, not
only how often they are right. This does it per author on the holdout arm under
the published correction, and reports each failing author's top three
destinations.
"""
import sys, os, json, collections, random
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-09-21-period-detrend-and-equal-n', 'src'))
import common as C
import delta as D
from expC_mechanism import attribute
from expG_authorblind import low_centre
from expH_holdout import load_holdout


def main():
    docs_full, _ = C.load()
    docs, _ = C.load(require_year=True)
    test = load_holdout()
    panel = sorted(set(d['author'] for d in docs_full if d['register'] == 'drama'))
    allv = docs + test
    vocab = D.vocabulary(docs_full)
    X = D.vectors(allv, vocab)
    years = np.array([d['yr'] for d in allv], float)
    au = np.array([d['author'] for d in allv])
    rg = np.array([d['register'] for d in allv])
    wk = np.array([d['work'] for d in allv])
    dmask = rg == 'drama'
    idx = np.where(rg == 'nondrama_holdout')[0]
    Zdet = C.zscale(C.detrend(X, years, dmask, degree=1), dmask)
    cent = np.stack([Zdet[dmask & (au == a)].mean(0) for a in panel])
    pred = np.array(attribute(low_centre(Zdet, idx, wk[idx]), cent, panel))
    out = {}
    for a in sorted(set(au[idx])):
        m = au[idx] == a
        c = collections.Counter(pred[m])
        out[a] = {'n': int(m.sum()), 'top': c.most_common(4)}
        print('%-22s n=%4d  ->  %s' % (a, m.sum(),
              ', '.join('%s %.2f' % (k.split(',')[0], v / m.sum()) for k, v in c.most_common(4))))
    # and per work for the two failing authors
    print('\nper work, the authors the correction misses:')
    for a in ('Crowne, John', 'Settle, Elkanah'):
        for w in sorted(set(wk[idx][au[idx] == a])):
            m = (au[idx] == a) & (wk[idx] == w)
            c = collections.Counter(pred[m])
            print('   %-16s %-9s n=%3d  %s' % (a.split(',')[0], w, m.sum(),
                  ', '.join('%s %d' % (k.split(',')[0], v) for k, v in c.most_common(3))))
    json.dump(out, open(os.path.join(HERE, '..', 'results', 'expJ_confusion.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
