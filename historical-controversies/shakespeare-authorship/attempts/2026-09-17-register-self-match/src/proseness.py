"""Verse density per dramatist, measured from TEI markup, not from the text.

If the register attractor is real, the sink should be the dramatist who writes
the least verse - whose plays are physically closest to prose on the page. That
is measurable from the <l> (verse line) and <p> (prose paragraph) markup in
engdracor's TEI, evidence that plays no part in any Delta computation.
"""
import os, re, sys, json, collections

ROOT = '/home/user/dracor-org/engdracor'
HERE = os.path.dirname(__file__)


def main():
    sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-09-05-stylometry-calibration', 'src'))
    import corpus
    plays = corpus.load()
    by = collections.defaultdict(lambda: [0, 0, 0])
    for p in plays:
        s = open(os.path.join(ROOT, 'tei', p['slug'] + '.xml'), errors='replace').read()
        body = s.split('<body', 1)[-1]
        by[p['author']][0] += len(re.findall(r'<l\b', body))
        by[p['author']][1] += len(re.findall(r'<p\b', body))
        by[p['author']][2] += p['n_words']
    rows = []
    for a, (nl, np_, nw) in by.items():
        rows.append({'author': a, 'verse_lines': nl, 'prose_paras': np_, 'words': nw,
                     'verse_lines_per_1k': round(nl / nw * 1000, 2),
                     'prose_share_of_blocks': round(np_ / max(1, nl + np_), 4)})
    rows.sort(key=lambda r: r['verse_lines_per_1k'])
    json.dump(rows, open(os.path.join(HERE, '..', 'results', 'proseness.json'), 'w'), indent=1)
    print('%-26s %10s %10s %10s' % ('author', 'verse/1k', 'prose_blk', 'words'))
    for r in rows:
        print('%-26s %10.2f %9.1f%% %10d' % (r['author'], r['verse_lines_per_1k'],
                                             100 * r['prose_share_of_blocks'], r['words']))


if __name__ == '__main__':
    main()
