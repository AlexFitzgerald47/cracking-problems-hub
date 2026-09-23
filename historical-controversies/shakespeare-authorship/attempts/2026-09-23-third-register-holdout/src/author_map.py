"""Map each 27-panel dramatist to the EXACT TCP author string(s) of their own plays.

Why this and not a name regex. TCP has two distinct writers filed as
`Banks, John, d. 1706.` and `Banks, John, 1637-1710.`, and a surname regex merges
them. The plays in engdracor are the panel's definition of the author, and every
engdracor `sourceid` IS a TCP id, so the author string attached to a panel
author's own plays is the one identifier we can be sure refers to that person.
Sole-author strings only: a TCP string containing ';' is a collaboration, an
adaptation or a translation source, and the 2026-09-17 build excluded those by
requiring an exact match against a sole-author form. Keeping that rule unchanged
is what makes the holdout comparable.
"""
import csv, re, os, json, collections

ROOT = '/home/user/dracor-org/engdracor'
TCP_CSV = '/tmp/w/TCP.csv'


def load_rows():
    return list(csv.DictReader(open(TCP_CSV, encoding='utf-8', errors='replace')))


def engdracor_index():
    """slug -> sourceid and the author from engdracor's own metadata."""
    idx = dict(re.findall(r'sourceid="([^"]+)" slug="([^"]+)"',
                          open(os.path.join(ROOT, 'index.xml')).read()))
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'meta', 'author_titles.csv'))))
    return idx, rows


def build():
    rows = load_rows()
    by_tcp = {r['TCP']: r for r in rows}
    idx, meta = engdracor_index()
    src_by_author = collections.defaultdict(list)
    for r in meta:
        a = r['authors'].strip()
        if ';' in a or not a:
            continue
        sid = r['id']
        base = sid.split('_')[0]
        if base in by_tcp:
            src_by_author[a].append(base)
    out = {}
    for a, sids in src_by_author.items():
        c = collections.Counter(by_tcp[s]['Author'] for s in sids)
        sole = {s: n for s, n in c.items() if ';' not in s}
        out[a] = {'play_author_strings': c.most_common(),
                  'sole': sorted(sole, key=lambda s: -sole[s])}
    return out


if __name__ == '__main__':
    m = build()
    for a in sorted(m):
        print('%-22s %s' % (a, m[a]['sole']))
        if len(m[a]['sole']) != 1:
            print('     ALL:', m[a]['play_author_strings'])
