"""Audit the 2026-09-04 Voynich 'golden cell' against physical metadata.

This deliberately does no language fitting.  It asks whether there is actually a
cell in ZL3b in which Currier language varies while LFD hand *and physical quire*
are held fixed.  It also shows the quire composition of the inherited
A/H3/$I=S and B/H3/$I=S comparison.

Run from this directory in the same checkout used by the earlier attempt.  The
ZL3b path is inherited from ../../2026-09-04-hand-language-confound/src/vms.py.
"""
from collections import Counter, defaultdict
import os
import sys

HERE = os.path.dirname(__file__)
OLD_SRC = os.path.abspath(os.path.join(
    HERE, '..', '..', '2026-09-04-hand-language-confound', 'src'))
sys.path.insert(0, OLD_SRC)
import vms  # noqa: E402


def main():
    pages = vms.load()

    h3 = [p for p in pages.values() if p['attrs'].get('H') == '3']
    h3.sort(key=lambda p: p['page'])

    print('LFD Hand 3 pages')
    print('page\tL\tI\tQ\tB\twords')
    for p in h3:
        a = p['attrs']
        print('%s\t%s\t%s\t%s\t%s\t%d' % (
            p['page'], a.get('L', '-'), a.get('I', '-'), a.get('Q', '-'),
            a.get('B', '-'), p['n_words']))

    print('\nHand-3 page counts by (Currier language, illustration type, quire)')
    counts = Counter((p['attrs'].get('L', '-'),
                      p['attrs'].get('I', '-'),
                      p['attrs'].get('Q', '-')) for p in h3)
    for key, n in sorted(counts.items()):
        print('%s\t%s\t%s\t%d' % (*key, n))

    # Does any physical quire contain both A and B by the same LFD hand?
    langs_by_hand_quire = defaultdict(set)
    pages_by_hand_quire = defaultdict(list)
    for p in pages.values():
        a = p['attrs']
        lang = a.get('L')
        hand = a.get('H')
        quire = a.get('Q')
        if lang in {'A', 'B'} and hand and quire:
            langs_by_hand_quire[(hand, quire)].add(lang)
            pages_by_hand_quire[(hand, quire)].append(p['page'])

    print('\nSame-LFD-hand, same-quire A/B overlap cells')
    overlaps = []
    for key, langs in sorted(langs_by_hand_quire.items()):
        if langs == {'A', 'B'}:
            overlaps.append(key)
            print('H%s Q%s: %s' % (key[0], key[1],
                                   ', '.join(sorted(pages_by_hand_quire[key]))))
    if not overlaps:
        print('NONE')

    # Audit the exact inherited 'Stars' cells.  In IVTFF, $I=S means
    # illustration type 'marginal stars only'; it is not a physical section ID.
    print('\nInherited H3/$I=S cells by quire')
    for lang in ('A', 'B'):
        selected = [p for p in h3
                    if p['attrs'].get('L') == lang
                    and p['attrs'].get('I') == 'S']
        by_q = Counter(p['attrs'].get('Q', '-') for p in selected)
        print('%s: pages=%s quires=%s words=%d' % (
            lang,
            ','.join(p['page'] for p in selected),
            dict(sorted(by_q.items())),
            sum(p['n_words'] for p in selected)))


if __name__ == '__main__':
    main()
