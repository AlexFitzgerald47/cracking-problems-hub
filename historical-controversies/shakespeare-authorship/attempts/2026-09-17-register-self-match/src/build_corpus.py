"""Builds BOTH registers from EEBO-TCP, through one identical extraction pipeline.

Why this design. The 2026-09-05 session refused to splice a modernised
Shakespeare into a TCP play corpus, because that would confound authorship with
edition. The same objection applies with full force to a register test: if the
plays are original-spelling TCP and the prose comes from a Victorian edited
reprint, any "register gap" found is partly a spelling gap. So both halves here
come from EEBO-TCP, and engdracor's own `sourceid` attributes ARE TCP ids, which
is how we know the 2026-09-05 play corpus is the same transcription tradition.
`pipeline_control.py` measures what little difference remains.

REGISTER IS DECIDED BY MARKUP, NOT BY TITLE.
  drama    : >= 5.0 <sp> speech elements per 1,000 words
  pageant  : the Lord Mayor's Shows, royal entries and masques - a third,
             performance-adjacent register, excluded by an explicit id list
             because no markup feature separates them from prose pamphlets
  nondrama : everything else

The 5.0/1k threshold sits in a wide empty gap, not at a fitted point: among
these authors' texts, non-dramatic candidates top out at 2.91/1k and the next
text up is 10.3/1k, while 268 confirmed engdracor plays have a median of 38/1k
and a 5th percentile of 20/1k.

ALL DOCUMENTS ARE 2,000-WORD CHUNKS, in both registers. This is not cosmetic:
Burrows's Delta distances grow as documents shorten, so comparing 25,000-word
plays against 8,000-word pamphlets would confound register with length and
produce a "register gap" out of arithmetic alone.
"""
import sys, os, json, csv, re, collections
sys.path.insert(0, os.path.dirname(__file__))
import tcp

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, '..', 'data')
DRAMA_SP_PER_1K = 5.0
MIN_WORDS = 3000
CHUNK = 2000
DUP_OVERLAP = 0.30

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

# Civic pageants, royal entries and court masques. Performance texts that carry
# little or no <sp> markup because they are mostly descriptive prose framing a
# few speeches. They are a third register and belong in neither half; listed by
# id rather than by title regex because "Pandosto the triumph of time" is a
# prose romance and would be caught by any rule matching "triumph".
PAGEANTS = {
    'A20069': "Dekker, The magnificent entertainment given to King James (1604) - royal entry",
    'A20090': "Dekker, Troia-Noua triumphans (1612) - Lord Mayor's Show",
    'A20053': "Dekker, Brittannia's honor (1628) - Lord Mayor's Show",
    'A07518': "Middleton, The triumphs of truth (1613) - Lord Mayor's Show",
    'A07494': "Middleton, Civitatis amor (1616) - royal entertainment",
    'A07513': "Middleton, The tryumphs of honor and industry (1617) - Lord Mayor's Show",
    'A07510': "Middleton, The sunne in Aries (1621) - Lord Mayor's Show",
    'A07502': "Middleton, Honorable entertainments (1621) - civic entertainments",
    'A07515': "Middleton, The triumphs of honor and vertue (1622) - Lord Mayor's Show",
    'A07516': "Middleton, The triumphs of integrity (1623) - Lord Mayor's Show",
    'A07512': "Middleton, The triumphs of health and prosperity (1626) - Lord Mayor's Show",
    'A07517': "Middleton, The triumphs of loue and antiquity (1619) - Lord Mayor's Show",
    'A03228': "Heywood, Londini artium & scientiarum scaturigo (1632) - Lord Mayor's Show",
    'A03229': "Heywood, Londini emporia (1633) - Lord Mayor's Show",
    'A03230': "Heywood, Londini speculum (1637) - Lord Mayor's Show",
    'A03233': "Heywood, Londini status pacatus (1639) - Lord Mayor's Show",
    'A03234': "Heywood, London ius honorarium (1631) - Lord Mayor's Show",
    'A03242': "Heywood, Porta pietatis (1638) - Lord Mayor's Show",
    'A04637': "Jonson, his part of King James's royal entertainment (1604) - royal entry",
}

MANUAL_EXCLUDE = {
    'A19241': "The defence of conny catching (1592) - published over 'Cuthbert Cunny-catcher' "
              "and is an ATTACK on Greene; TCP files it under him as a conjecture. Disputed.",
    'A02216': "An Oration or funerall sermon at the buriall of Gregorie the 13 (1585) - "
              "a translation, not Greene's own composition.",
    'A46229': "A Strange banquet (1678) - a 2-page broadside ballad printed 41 years after "
              "Jonson's death.",
}

# Ben Jonson's non-dramatic verse survives inside the 1616 folio Workes, which
# engdracor split into its nine plays. The folio is a sequence of <text>
# elements; index 11 is EPIGRAMMES + THE FORREST and index 13 is A Panegyre.
# Same volume, same printer, same transcription as his plays - the tightest
# register contrast obtainable anywhere in this corpus.
JONSON_FOLIO = ('A04632', {11: 'Epigrammes; The Forrest (1616 folio)',
                           13: 'A Panegyre (1616 folio)'})


def folio_parts(tcp_id):
    s = tcp.raw(tcp_id)
    return re.split(r'(?=<text\b)', s.split('</teiHeader>', 1)[-1])


def chunks(words, size=CHUNK):
    return [words[i:i + size] for i in range(0, len(words) - size + 1, size)]


def main():
    rows = list(csv.DictReader(open('/tmp/w/TCP.csv', encoding='utf-8', errors='replace')))
    drac = set(re.findall(r'sourceid="([^"]+)"',
                          open('/home/user/dracor-org/engdracor/index.xml').read()))
    pool = [r for r in rows if r['Author'] in AUTH and r['Status'] == 'Free'
            and r['TCP'] not in drac]

    kept, dropped = [], []
    seen = collections.defaultdict(list)

    def consider(tcp_id, author, year, title, words, sp, gap, source):
        rec = {'tcp': tcp_id, 'author': author, 'year': year, 'title': title,
               'n_words': len(words), 'sp': sp, 'gap': gap,
               'sp_per_1k': round(sp / max(1, len(words)) * 1000, 3),
               'gap_rate': round(gap / max(1, len(words)), 5), 'source': source}
        if tcp_id in MANUAL_EXCLUDE:
            rec['drop'] = 'manual: ' + MANUAL_EXCLUDE[tcp_id]
        elif tcp_id in PAGEANTS:
            rec['drop'] = 'pageant: ' + PAGEANTS[tcp_id]
        elif rec['sp_per_1k'] >= DRAMA_SP_PER_1K:
            rec['drop'] = 'markup: %.1f <sp>/1k words - performance text' % rec['sp_per_1k']
        elif len(words) < MIN_WORDS:
            rec['drop'] = 'too short: %d words' % len(words)
        else:
            for pid, pw in seen[author]:
                ov = tcp.overlap(words, pw)
                if ov > DUP_OVERLAP:
                    rec['drop'] = 'near-duplicate of %s (8-gram overlap %.3f)' % (pid, ov)
                    break
        if 'drop' in rec:
            dropped.append(rec); return
        seen[author].append((tcp_id, words))
        rec['words'] = words
        kept.append(rec)

    for r in sorted(pool, key=lambda r: (AUTH[r['Author']], r['Date'])):
        s = tcp.raw(r['TCP']); st = tcp.structure(s)
        consider(r['TCP'], AUTH[r['Author']], r['Date'], r['Title'][:120],
                 tcp.words(s), st['sp'], st['gap'], 'tcp')

    fid, parts = JONSON_FOLIO
    ps = folio_parts(fid)
    for idx, label in parts.items():
        seg = '<text' + ps[idx]
        consider('%s_p%d' % (fid, idx), 'Jonson, Ben', '1616', label,
                 tcp.words(seg), len(re.findall(r'<sp\b', seg)),
                 len(re.findall(r'<gap\b', seg)), 'folio-division')

    # ---- chunk both registers identically ----
    docs = []
    for r in kept:
        for j, c in enumerate(chunks(r['words'])):
            docs.append({'id': '%s#%d' % (r['tcp'], j), 'author': r['author'],
                         'register': 'nondrama', 'work': r['tcp'],
                         'year': r['year'], 'words': c})
    sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-09-05-stylometry-calibration', 'src'))
    import corpus as playcorpus
    for p in playcorpus.load():
        for j, c in enumerate(chunks(p['words'])):
            docs.append({'id': '%s#%d' % (p['slug'], j), 'author': p['author'],
                         'register': 'drama', 'work': p['slug'],
                         'year': p['year'], 'words': c})

    os.makedirs(OUT, exist_ok=True)
    json.dump(docs, open(os.path.join(OUT, 'chunks.json'), 'w'))
    for r in kept:
        r.pop('words', None)
    json.dump({'kept': kept, 'dropped': dropped},
              open(os.path.join(OUT, 'manifest.json'), 'w'), indent=1)

    print('non-dramatic: pool %d -> kept %d' % (len(pool) + len(parts), len(kept)))
    c = collections.Counter(r['drop'].split(':')[0] for r in dropped)
    print('  dropped:', dict(c))
    print('\n%-20s %6s %8s | %6s %8s' % ('author', 'nd_tx', 'nd_chunk', 'plays', 'dr_chunk'))
    for a in sorted(AUTH.values()):
        nt = sum(1 for r in kept if r['author'] == a)
        nc = sum(1 for d in docs if d['author'] == a and d['register'] == 'nondrama')
        pw = len(set(d['work'] for d in docs if d['author'] == a and d['register'] == 'drama'))
        pc = sum(1 for d in docs if d['author'] == a and d['register'] == 'drama')
        print('%-20s %6d %8d | %6d %8d' % (a, nt, nc, pw, pc))
    print('\ntotal chunks: %d (nondrama %d, drama %d) across %d authors' % (
        len(docs), sum(1 for d in docs if d['register'] == 'nondrama'),
        sum(1 for d in docs if d['register'] == 'drama'),
        len(set(d['author'] for d in docs))))


if __name__ == '__main__':
    main()
