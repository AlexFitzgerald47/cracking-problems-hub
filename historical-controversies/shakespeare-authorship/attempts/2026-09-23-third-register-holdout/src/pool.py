"""Candidate pool for the third-register holdout.

Rule, deliberately identical in shape to the 2026-09-17 build:
  * one EXACT sole-author TCP string per panel dramatist, taken from the author
    string on that dramatist's OWN plays in engdracor (see author_map.py);
  * `attributed name` forms excluded - a holdout arm must be undisputed authorship;
  * Status == Free;
  * not an engdracor sourceid (those are the plays already in the training set).
"""
import csv, re, os, json, collections
import author_map

HAS_ND = {'Chapman, George', 'Dekker, Thomas', 'Greene, Robert', 'Heywood, Thomas',
          'Jonson, Ben', 'Lyly, John', 'Marston, John', 'Middleton, Thomas'}


def panel_authors():
    docs = json.load(open(os.path.join(os.path.dirname(__file__), '..', '..',
                                       '2026-09-17-register-self-match', 'data', 'chunks.json')))
    return sorted(set(d['author'] for d in docs if d['register'] == 'drama'))


def canonical_strings():
    m = author_map.build()
    out = {}
    for a in panel_authors():
        sole = [s for s in m.get(a, {}).get('sole', []) if 'attributed name' not in s]
        if not sole:
            out[a] = None
        else:
            out[a] = sole[0]
    return out


def pool():
    rows = author_map.load_rows()
    drac = set(re.findall(r'sourceid="([^"]+)"',
                          open(os.path.join(author_map.ROOT, 'index.xml')).read()))
    drac |= set(s.split('_')[0] for s in drac)
    canon = canonical_strings()
    want = collections.defaultdict(list)
    for r in rows:
        for a, s in canon.items():
            if s and r['Author'] == s and r['Status'] == 'Free' and r['TCP'] not in drac:
                want[a].append(r)
    return canon, want


if __name__ == '__main__':
    canon, want = pool()
    tot = 0
    for a in sorted(canon):
        tag = 'TRAINED-ND' if a in HAS_ND else 'holdout'
        n = len(want.get(a, []))
        tot += n if a not in HAS_ND else 0
        print('%-22s %-10s %-45s %4d' % (a, tag, canon[a], n))
    print('\ncandidate TCP texts for holdout authors:', tot)
