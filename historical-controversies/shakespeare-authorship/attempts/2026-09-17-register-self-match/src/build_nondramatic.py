"""Builds the non-dramatic half of the register corpus from EEBO-TCP.

Selection rules, applied in this order and all recorded in the manifest:

 1. Sole-authored, TCP `Status == Free`, author string matched EXACTLY against
    the dated authority form, so that "Middleton, Thomas, d. 1627" (the
    dramatist) is not pooled with "Middleton, Thomas, Sir, 1586-1666".
 2. Drop anything whose TCP id appears in engdracor's index - that is a known
    play, by the drama corpus's own reckoning.
 3. Drop anything with <sp> speech markup. This is the load-bearing filter and
    it is structural, not lexical: it removes the masques, the civic pageants
    and the dialogues that titles alone would have let through.
 4. Drop texts under 3,000 words - below that a chunk cannot be formed.
 5. Drop near-duplicate reprints (8-gram overlap > 0.30 against a text already
    kept by the same author). Greene's `Pandosto` was reissued as `Dorastus and
    Fawnia`, and his `Disputation` as `Theeves falling out`; keeping both would
    let one work vote twice.
 6. A short, explicitly reasoned manual exclusion list for authorship and
    translation problems that markup cannot see.
"""
import sys, os, json, csv, re, collections
sys.path.insert(0, os.path.dirname(__file__))
import tcp

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'data')
MIN_WORDS = 3000
DUP_OVERLAP = 0.30

# Exclusions markup cannot see. Each needs a reason or it does not belong here.
MANUAL_EXCLUDE = {
    'A19241': "The defence of conny catching - published over 'Cuthbert Cunny-catcher', "
              "an attack ON Greene; TCP files it under Greene as a guess. Disputed authorship.",
    'A02216': "An Oration or funerall sermon ... at the buriall of Gregorie the 13 - "
              "a translation, not Greene's own composition.",
    'A46229': "A Strange banquet (1678) - 2 pages, posthumous broadside ballad printing, "
              "41 years after Jonson's death.",
}


def load_pool():
    rows = list(csv.DictReader(open(os.path.join('/tmp/w', 'TCP.csv'),
                                    encoding='utf-8', errors='replace')))
    drac = set(re.findall(r'sourceid="([^"]+)"',
                          open('/home/user/dracor-org/engdracor/index.xml').read()))
    AUTH = {
        'Jonson, Ben, 1573?-1637.': 'Jonson, Ben',
        'Chapman, George, 1559?-1634.': 'Chapman, George',
        'Dekker, Thomas, ca. 1572-1632.': 'Dekker, Thomas',
        'Greene, Robert, 1558?-1592.': 'Greene, Robert',
        'Lyly, John, 1554?-1606.': 'Lyly, John',
        'Middleton, Thomas, d. 1627.': 'Middleton, Thomas',
        'Marston, John, 1575?-1634.': 'Marston, John',
        'Heywood, Thomas, d. 1641.': 'Heywood, Thomas',
    }
    pool = []
    for r in rows:
        if r['Author'] in AUTH and r['Status'] == 'Free' and r['TCP'] not in drac:
            pool.append({'tcp': r['TCP'], 'author': AUTH[r['Author']],
                         'year': r['Date'], 'title': r['Title'][:120]})
    return pool


def main():
    pool = load_pool()
    kept, log = [], []
    by_author = collections.defaultdict(list)
    for r in sorted(pool, key=lambda r: (r['author'], r['year'])):
        rec = dict(r)
        if r['tcp'] in MANUAL_EXCLUDE:
            rec['drop'] = 'manual: ' + MANUAL_EXCLUDE[r['tcp']]
            log.append(rec); continue
        s = tcp.raw(r['tcp'])
        st = tcp.structure(s)
        w = tcp.words(s)
        rec.update(n_words=len(w), **{'sp': st['sp'], 'gap': st['gap']})
        rec['gap_rate'] = round(st['gap'] / max(1, len(w)), 5)
        if st['sp'] > 0:
            rec['drop'] = 'markup: %d <sp> speech elements - performance text' % st['sp']
            log.append(rec); continue
        if len(w) < MIN_WORDS:
            rec['drop'] = 'too short: %d words' % len(w)
            log.append(rec); continue
        dup = None
        for prev in by_author[r['author']]:
            ov = tcp.overlap(w, prev[1])
            if ov > DUP_OVERLAP:
                dup = (prev[0], round(ov, 3)); break
        if dup:
            rec['drop'] = 'near-duplicate of %s (8-gram overlap %.3f)' % dup
            log.append(rec); continue
        by_author[r['author']].append((r['tcp'], w))
        rec['words'] = w
        kept.append(rec)

    os.makedirs(OUT, exist_ok=True)
    json.dump(kept, open(os.path.join(OUT, 'nondramatic.json'), 'w'))
    for r in kept:
        r.pop('words', None)
    json.dump({'kept': kept, 'dropped': log},
              open(os.path.join(OUT, 'nondramatic_manifest.json'), 'w'), indent=1)

    print('pool %d -> kept %d, dropped %d' % (len(pool), len(kept), len(log)))
    tot = collections.Counter()
    for r in kept:
        tot[r['author']] += r['n_words']
    for a in sorted(tot):
        n = sum(1 for r in kept if r['author'] == a)
        print('  %-20s %2d texts  %7d words' % (a, n, tot[a]))
    print('\ndropped by reason:')
    c = collections.Counter(r['drop'].split(':')[0] for r in log)
    for k, v in c.most_common():
        print('  %-18s %d' % (k, v))


if __name__ == '__main__':
    main()
