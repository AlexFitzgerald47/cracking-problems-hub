"""P7-P11. Widen the panel from 8 dramatists to all 27 and test the attractor
mechanism against 19 authors that played no part in deriving it.
"""
import sys, os, json, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import delta as D
from analysis import load, scaled, PANEL

HERE = os.path.dirname(__file__)


def spearman(x, y):
    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[o[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(x), rank(y)
    mx, my = np.mean(rx), np.mean(ry)
    a = sum((p - mx) * (q - my) for p, q in zip(rx, ry))
    b = (sum((p - mx) ** 2 for p in rx) * sum((q - my) ** 2 for q in ry)) ** .5
    return a / b


def main():
    docs = load()
    vocab = D.vocabulary(docs)
    drama_all = [d for d in docs if d['register'] == 'drama']
    nond = [d for d in docs if d['register'] == 'nondrama']
    authors = sorted(set(d['author'] for d in drama_all))
    Z = scaled(docs, vocab, drama_all)
    au = np.array([d['author'] for d in docs])
    rg = np.array([d['register'] for d in docs])
    cent = np.stack([Z[(au == a) & (rg == 'drama')].mean(0) for a in authors])

    nd = np.where(rg == 'nondrama')[0]
    pred = [authors[i] for i in np.abs(Z[nd][:, None, :] - cent[None, :, :]).sum(2).argmin(1)]
    true = au[nd]
    dd = np.where(rg == 'drama')[0]
    pred_d = [authors[i] for i in np.abs(Z[dd][:, None, :] - cent[None, :, :]).sum(2).argmin(1)]

    tot = collections.Counter(pred); totd = collections.Counter(pred_d)
    pros = {r['author']: r['verse_lines_per_1k']
            for r in json.load(open(os.path.join(HERE, '..', 'results', 'proseness.json')))}

    rows = sorted(authors, key=lambda a: -tot[a])
    print('%-24s %8s %9s %9s' % ('author', 'verse/1k', 'nondram%', 'drama%'))
    for a in rows:
        print('%-24s %8.1f %8.1f%% %8.1f%%' % (a, pros[a], 100 * tot[a] / len(pred),
                                               100 * totd[a] / len(pred_d)))
    top3 = ['Lyly, John', 'Shadwell, Thomas', "D'Urfey, Thomas"]
    share3 = sum(tot[a] for a in top3) / len(pred)
    restoration = sum(tot[a] for a in ['Shadwell, Thomas', "D'Urfey, Thomas"]) / len(pred)
    rho = spearman([pros[a] for a in authors], [tot[a] / len(pred) for a in authors])

    per = {}
    for a in PANEL:
        m = true == a
        per[a] = float(np.mean([p == a for p, k in zip(pred, m) if k])) if m.any() else None
    macro = float(np.mean([v for v in per.values() if v is not None]))
    micro = float(np.mean([p == t for p, t in zip(pred, true)]))

    print('\nP7  top absorber: %s  (predicted: Lyly, Shadwell or D\'Urfey)' % rows[0])
    print('P8  three lowest-verse authors absorb %.1f%%  (predicted >50%%)' % (100 * share3))
    print('P9  Shadwell+D\'Urfey (Restoration) absorb %.1f%%  (predicted >10%%)' % (100 * restoration))
    print('P10 Spearman(verse density, non-dramatic share) = %.3f  (predicted < -0.45)' % rho)
    print('P11 cross-register macro on 27 authors = %.3f (8-author was 0.337; predicted <0.20)' % macro)
    print('    micro %.3f, chance %.3f' % (micro, 1 / len(authors)))
    print('\nper-author cross-register accuracy, 27-author panel:')
    for a in PANEL:
        print('   %-22s %.3f' % (a, per[a]))

    json.dump({'n_authors': len(authors), 'top_absorber': rows[0],
               'share_three_lowest_verse': share3, 'share_restoration_two': restoration,
               'spearman_verse_vs_absorption': rho, 'macro': macro, 'micro': micro,
               'chance': 1 / len(authors), 'per_author': per,
               'nondrama_share': {a: tot[a] / len(pred) for a in authors},
               'drama_share': {a: totd[a] / len(pred_d) for a in authors}},
              open(os.path.join(HERE, '..', 'results', 'wide_panel.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
