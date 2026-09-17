"""Is cross-register attribution failing at random, or collapsing onto one author?

If a method that crosses the register gap is measuring authorship badly, errors
scatter. If it is measuring REGISTER, errors concentrate: every author's prose
lands on whichever dramatist's plays are most prose-like, and that dramatist
then appears to "self-match" perfectly for a reason that has nothing to do with
having written the text.

Lyly is the obvious suspect - his comedies are mannered prose - so this test can
tell a real self-match from an accident of the sink.
"""
import sys, os, json, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import delta as D
from analysis import load, scaled, PANEL

HERE = os.path.dirname(__file__)


def main():
    docs = load()
    panel = [d for d in docs if d['author'] in PANEL]
    vocab = D.vocabulary(docs)
    drama = [d for d in panel if d['register'] == 'drama']
    Z = scaled(panel, vocab, drama)
    au = np.array([d['author'] for d in panel])
    rg = np.array([d['register'] for d in panel])
    cent = np.stack([Z[(au == a) & (rg == 'drama')].mean(0) for a in PANEL])

    nd = np.where(rg == 'nondrama')[0]
    dist = np.abs(Z[nd][:, None, :] - cent[None, :, :]).sum(2)
    pred = [PANEL[i] for i in dist.argmin(1)]
    true = au[nd]

    conf = collections.defaultdict(collections.Counter)
    for t, p in zip(true, pred):
        conf[t][p] += 1
    short = {a: a.split(',')[0][:9] for a in PANEL}
    print('CONFUSION: rows = true author of the NON-DRAMATIC text,')
    print('           cols = dramatist whose PLAYS it was attributed to\n')
    print('%-10s' % '', ''.join('%9s' % short[a] for a in PANEL), '   n')
    for a in PANEL:
        row = conf[a]; n = sum(row.values())
        print('%-10s' % short[a], ''.join('%9s' % (row[b] or '.') for b in PANEL), '%5d' % n)
    tot = collections.Counter(pred)
    print('\n%-10s' % 'TOTAL', ''.join('%9d' % tot[a] for a in PANEL), '%5d' % len(pred))
    print('%-10s' % 'share', ''.join('%8.1f%%' % (100 * tot[a] / len(pred)) for a in PANEL))

    # Same diagnostic for the within-register control: where do DRAMA chunks go?
    dd = np.where(rg == 'drama')[0]
    dist2 = np.abs(Z[dd][:, None, :] - cent[None, :, :]).sum(2)
    pred2 = [PANEL[i] for i in dist2.argmin(1)]
    tot2 = collections.Counter(pred2)
    print('\nfor comparison, where DRAMA chunks land (same centroids):')
    print('%-10s' % 'share', ''.join('%8.1f%%' % (100 * tot2[a] / len(pred2)) for a in PANEL))

    # how concentrated is the prose sink?
    hhi = sum((tot[a] / len(pred)) ** 2 for a in PANEL)
    hhi2 = sum((tot2[a] / len(pred2)) ** 2 for a in PANEL)
    print('\nconcentration (sum of squared shares; 0.125 = perfectly even over 8):')
    print('  non-dramatic chunks %.3f   drama chunks %.3f' % (hhi, hhi2))

    # Lyly removed: does anyone else's prose recover?
    alt = [a for a in PANEL if a != 'Lyly, John']
    cent2 = np.stack([Z[(au == a) & (rg == 'drama')].mean(0) for a in alt])
    nd2 = [i for i in nd if au[i] != 'Lyly, John']
    d2 = np.abs(Z[nd2][:, None, :] - cent2[None, :, :]).sum(2)
    p2 = [alt[i] for i in d2.argmin(1)]
    t2 = au[nd2]
    per = {a: float(np.mean([x == a for x, y in zip(p2, t2) if y == a])) for a in alt}
    print('\nLyly dropped from the panel (chance = %.3f), remaining authors:' % (1 / len(alt)))
    for a in alt:
        print('   %-20s %.3f' % (a, per[a]))
    print('   macro %.3f' % np.mean(list(per.values())))

    json.dump({'confusion': {a: dict(conf[a]) for a in PANEL},
               'nondrama_share': {a: tot[a] / len(pred) for a in PANEL},
               'drama_share': {a: tot2[a] / len(pred2) for a in PANEL},
               'concentration_nondrama': hhi, 'concentration_drama': hhi2,
               'without_lyly': per, 'without_lyly_macro': float(np.mean(list(per.values())))},
              open(os.path.join(HERE, '..', 'results', 'attractor.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
