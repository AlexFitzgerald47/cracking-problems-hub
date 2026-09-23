"""Build the holdout non-dramatic arm, under the 2026-09-17 rules unchanged.

Same extractor (`tcp.py`), same register rule (>= 5.0 <sp> per 1,000 words is a
performance text), same 3,000-word floor, same 0.30 8-gram near-duplicate rule,
same 2,000-word chunking. The ONLY difference from `build_corpus.py` is which
authors are in scope: these are the panel dramatists who contributed no
non-dramatic text to the arm the correction was developed on.

Pageants are held out of the non-dramatic arm exactly as they were in 2026-09-17,
by an explicit id list built from inspection of the kept titles rather than by a
title regex, and are written to their own arm.
"""
import sys, os, json, collections, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', '2026-09-17-register-self-match', 'src'))
import tcp
import pool
import filters

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data')
DRAMA_SP_PER_1K = 5.0
MIN_WORDS = 3000
CHUNK = 2000
DUP_OVERLAP = 0.30

PAGEANT_IDS = json.load(open(os.path.join(HERE, 'pageant_ids.json'))) \
    if os.path.exists(os.path.join(HERE, 'pageant_ids.json')) else {}
MANUAL_EXCLUDE = json.load(open(os.path.join(HERE, 'manual_exclude.json'))) \
    if os.path.exists(os.path.join(HERE, 'manual_exclude.json')) else {}


def chunks(words, size=CHUNK):
    return [words[i:i + size] for i in range(0, len(words) - size + 1, size)]


def main():
    canon, want = pool.pool()
    kept, dropped, pageants = [], [], []
    seen = collections.defaultdict(list)
    for a in sorted(want):
        if a in pool.HAS_ND:
            continue
        for r in sorted(want[a], key=lambda r: (r['Date'], r['TCP'])):
            s = tcp.raw(r['TCP'])
            st = tcp.structure(s)
            w = tcp.words(s)
            rec = {'tcp': r['TCP'], 'author': a, 'year': r['Date'],
                   'title': r['Title'][:120], 'n_words': len(w),
                   'sp': st['sp'], 'gap': st['gap'],
                   'sp_per_1k': round(st['sp'] / max(1, len(w)) * 1000, 3),
                   'gap_rate': round(st['gap'] / max(1, len(w)), 5), 'source': 'tcp'}
            hard = filters.hard_drop(r, canon[a])
            rec['named_on_title'] = filters.named_on_title(r, canon[a])
            if r['TCP'] in MANUAL_EXCLUDE:
                rec['drop'] = 'manual: ' + MANUAL_EXCLUDE[r['TCP']]
            elif hard:
                rec['drop'] = hard
            elif rec['sp_per_1k'] >= DRAMA_SP_PER_1K:
                rec['drop'] = 'markup: %.1f <sp>/1k words - performance text' % rec['sp_per_1k']
            elif len(w) < MIN_WORDS:
                rec['drop'] = 'too short: %d words' % len(w)
            else:
                for pid, pw in seen[a]:
                    ov = tcp.overlap(w, pw)
                    if ov > DUP_OVERLAP:
                        rec['drop'] = 'near-duplicate of %s (8-gram overlap %.3f)' % (pid, ov)
                        break
            if 'drop' in rec:
                dropped.append(rec)
                continue
            seen[a].append((r['TCP'], w))
            rec['words'] = w
            if r['TCP'] in PAGEANT_IDS:
                rec['pageant_note'] = PAGEANT_IDS[r['TCP']]
                pageants.append(rec)
            else:
                kept.append(rec)

    docs, pdocs = [], []
    for r in kept:
        for j, c in enumerate(chunks(r['words'])):
            docs.append({'id': '%s#%d' % (r['tcp'], j), 'author': r['author'],
                         'register': 'nondrama_holdout', 'work': r['tcp'],
                         'year': r['year'], 'words': c,
                         'named_on_title': r['named_on_title']})
    for r in pageants:
        for j, c in enumerate(chunks(r['words'])):
            pdocs.append({'id': '%s#%d' % (r['tcp'], j), 'author': r['author'],
                          'register': 'pageant_holdout', 'work': r['tcp'],
                          'year': r['year'], 'words': c})
    os.makedirs(OUT, exist_ok=True)
    json.dump(docs, open(os.path.join(OUT, 'holdout_chunks.json'), 'w'))
    json.dump(pdocs, open(os.path.join(OUT, 'pageant_holdout_chunks.json'), 'w'))
    for r in kept + pageants:
        r.pop('words', None)
    json.dump({'kept': kept, 'pageants': pageants, 'dropped': dropped},
              open(os.path.join(OUT, 'holdout_manifest.json'), 'w'), indent=1)

    print('candidates %d -> kept %d non-dramatic, %d pageant, dropped %d'
          % (len(kept) + len(pageants) + len(dropped), len(kept), len(pageants), len(dropped)))
    print(' drops:', dict(collections.Counter(r['drop'].split(':')[0] for r in dropped)))
    print('\n%-22s %6s %8s %6s' % ('author', 'texts', 'chunks', 'pag_ch'))
    tot = 0
    for a in sorted(set(d['author'] for d in docs) | set(d['author'] for d in pdocs)):
        n = sum(1 for d in docs if d['author'] == a)
        p = sum(1 for d in pdocs if d['author'] == a)
        t = sum(1 for r in kept if r['author'] == a)
        tot += n
        print('%-22s %6d %8d %6d' % (a, t, n, p))
    print('\nholdout non-dramatic chunks: %d across %d authors; pageant %d across %d'
          % (len(docs), len(set(d['author'] for d in docs)),
             len(pdocs), len(set(d['author'] for d in pdocs))))


if __name__ == '__main__':
    main()
