"""P12-P15. The held-out arm: the 19 civic pageants excluded from both registers.

These were classified and set aside by src/build_corpus.py before any distance
was computed, and nothing above has touched them. They are out-of-register text
of undisputed authorship by dramatists who are in the training set - which makes
them the cleanest available analogue of the actual authorship question.
"""
import sys, os, json, csv, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import tcp, delta as D
from analysis import load, scaled
from build_corpus import PAGEANTS, AUTH, chunks
from wide_panel import spearman

HERE = os.path.dirname(__file__)


def main():
    rows = {r['TCP']: r for r in csv.DictReader(
        open('/tmp/w/TCP.csv', encoding='utf-8', errors='replace'))}
    pag = []
    for tid in PAGEANTS:
        r = rows[tid]
        w, _ = tcp.words_with_damage(tcp.raw(tid))
        a = AUTH[r['Author']]
        for j, c in enumerate(chunks(w)):
            pag.append({'id': '%s#%d' % (tid, j), 'author': a, 'register': 'pageant',
                        'work': tid, 'year': r['Date'], 'words': c})
    print('held-out pageants: %d texts -> %d chunks' % (len(PAGEANTS), len(pag)))
    print('  by author:', dict(collections.Counter(d['author'] for d in pag)))

    docs = load()
    vocab = D.vocabulary(docs)
    drama = [d for d in docs if d['register'] == 'drama']
    authors = sorted(set(d['author'] for d in drama))
    allv = docs + pag
    Z = scaled(allv, vocab, drama)
    au = np.array([d['author'] for d in allv])
    rg = np.array([d['register'] for d in allv])
    cent = np.stack([Z[(au == a) & (rg == 'drama')].mean(0) for a in authors])

    def absorb(mask):
        idx = np.where(mask)[0]
        p = [authors[i] for i in np.abs(Z[idx][:, None, :] - cent[None, :, :]).sum(2).argmin(1)]
        return p, au[idx], collections.Counter(p), len(p)

    pp, pt, pc, pn = absorb(rg == 'pageant')
    np_, nt, nc, nn = absorb(rg == 'nondrama')
    pshare = [pc[a] / pn for a in authors]
    nshare = [nc[a] / nn for a in authors]
    rho = spearman(nshare, pshare)
    top = max(authors, key=lambda a: pc[a])
    zeros = sum(1 for a in authors if pc[a] == 0)

    print('\n%-24s %10s %10s' % ('author', 'pageant%', 'nondram%'))
    for a in sorted(authors, key=lambda a: -pc[a]):
        if pc[a] or nc[a]:
            print('%-24s %9.1f%% %9.1f%%' % (a, 100 * pc[a] / pn, 100 * nc[a] / nn))

    own = {}
    for a in ['Middleton, Thomas', 'Heywood, Thomas', 'Dekker, Thomas', 'Jonson, Ben']:
        m = pt == a
        own[a] = {'n': int(m.sum()),
                  'acc': float(np.mean([x == a for x, k in zip(pp, m) if k])) if m.any() else None}

    print('\nP12 top pageant absorber: %s  (predicted Lyly)' % top)
    print('P13 Spearman(nondramatic profile, pageant profile) = %+.3f  (predicted > +0.60)' % rho)
    print('P14 authors absorbing zero pageant chunks: %d of 27  (predicted >= 14)' % zeros)
    print('P15 own-pageant recovery (predicted < 0.25 each):')
    for a, v in own.items():
        print('    %-20s n=%3d  %s' % (a, v['n'], '%.3f' % v['acc'] if v['acc'] is not None else '-'))
    macro = float(np.mean([v['acc'] for v in own.values() if v['acc'] is not None]))
    print('    macro over these authors %.3f  (chance %.3f)' % (macro, 1 / len(authors)))

    json.dump({'n_chunks': pn, 'top_absorber': top, 'spearman_profiles': rho,
               'authors_absorbing_zero': zeros, 'own_pageant_recovery': own,
               'pageant_share': {a: pc[a] / pn for a in authors}},
              open(os.path.join(HERE, '..', 'results', 'heldout_pageants.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
