"""Is the register gap actually a TRANSCRIPTION gap?

TCP <gap> damage runs heavier in the non-dramatic half for 5 of the 8 authors
(Chapman 204 vs 117 per 10k words, Greene 156 vs 115). If damage rather than
register were driving the P1 result, the effect should weaken or vanish among the
authors whose two registers are transcribed equally cleanly.

Jonson (16.5 vs 18.2), Middleton (31.6 vs 24.8) and Heywood (78.9 vs 84.5) have
essentially no damage differential - Jonson and Heywood are in fact dirtier in the
DRAMA half. If P1 survives on those three, damage is not the explanation.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import delta as D
from analysis import load, scaled, cells, PANEL

HERE = os.path.dirname(__file__)
CLEAN = ['Jonson, Ben', 'Middleton, Thomas', 'Heywood, Thomas']


def run(authors, label):
    docs = load()
    sub = [d for d in docs if d['author'] in authors]
    vocab = D.vocabulary(docs)
    Z = scaled(sub, vocab, [d for d in sub if d['register'] == 'drama'])
    c = cells(Z, sub)
    sa_cr = c['same_author_cross_register']['mean']
    da_sr = c['diff_author_same_register']['mean']
    print('%s (n=%d authors, %d chunks)' % (label, len(authors), len(sub)))
    for k in ('same_author_same_register', 'diff_author_same_register',
              'same_author_cross_register', 'diff_author_cross_register'):
        print('   %-28s %8.2f' % (k, c[k]['mean']))
    print('   P1 margin (same-author cross-register MINUS diff-author same-register): %+.2f  -> %s'
          % (sa_cr - da_sr, 'HOLDS' if sa_cr > da_sr else 'FAILS'))
    return {'cells': c, 'p1_margin': sa_cr - da_sr, 'p1_holds': bool(sa_cr > da_sr)}


def main():
    out = {'all_eight': run(PANEL, 'all 8 authors'),
           'damage_matched_three': run(CLEAN, 'damage-matched subset (Jonson, Middleton, Heywood)')}
    json.dump(out, open(os.path.join(HERE, '..', 'results', 'damage_matched.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
