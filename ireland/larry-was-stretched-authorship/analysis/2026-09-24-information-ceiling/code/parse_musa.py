#!/usr/bin/env python3
"""Parse Farmer, *Musa Pedestris* (1896) -- Gutenberg etext 8466 -- into an
author-labelled, genre-matched corpus of canting songs.

Strategy: the book's CONTENTS gives "Title (Author--year)" for every song.
We locate each title's header in the body, then take the song text as
everything between that header block and the next song's header, with
Farmer's editorial apparatus (glosses, provenance brackets, stanza
numerals, [Notes] markers) stripped.

Usage: parse_musa.py <gutenberg_txt> <out.json>
"""
import json, re, sys

SRC, OUT = sys.argv[1], sys.argv[2]
lines = open(SRC, encoding='utf-8').read().split('\n')

def key(t):
    t = t.replace('_', '')
    t = re.sub(r'\[Notes\]', '', t)
    t = t.lower()
    t = re.sub(r'[^a-z0-9 ]', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'^(the|a|an) ', '', t)
    t = re.sub(r' (the|a|an)$', '', t)
    return t.replace(' ', '')

# ---- 1. CONTENTS -> (title, author, year)
toc = []
toc_re = re.compile(r'^(.*?)\s*\(([^()]*?)--([^()]*?)\)\s*$')
for ln in lines[45:143]:
    m = toc_re.match(ln.strip())
    if m:
        toc.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))

body_start = next(i for i, l in enumerate(lines) if l.strip() == 'FOREWORDS')
body_end   = next(i for i, l in enumerate(lines) if l.strip() == 'NOTES' and i > body_start)

# ---- 2. locate each TOC title's header line in the body
body_keys = {}
for i in range(body_start, body_end):
    s = lines[i].strip()
    if not s or s.startswith('['):
        continue
    k = key(s)
    if len(k) >= 5:
        body_keys.setdefault(k, []).append(i)

# Farmer's CONTENTS misprints one title ("Banter's" for the body's
# "Bunter's"); without this the song is absorbed into the preceding one.
ALIAS = {"banterschristening": "bunterschristening"}

hits = []
for title, author, year in toc:
    k = ALIAS.get(key(title), key(title))
    cand = body_keys.get(k)
    if not cand:                     # substring fallback (subtitles, variants)
        for bk, idxs in body_keys.items():
            if len(bk) >= 8 and (bk.startswith(k[:12]) or k.startswith(bk[:12])):
                cand = idxs
                break
    if cand:
        hits.append({'title': title, 'author': author, 'year': year, 'line': cand[0]})

hits.sort(key=lambda h: h['line'])
# de-duplicate: keep first TOC entry per body line
seen, uniq = set(), []
for h in hits:
    if h['line'] in seen:
        continue
    seen.add(h['line'])
    uniq.append(h)
hits = uniq

WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")

def clean_song(block):
    """Strip Farmer's apparatus. Multi-line bracketed blocks are provenance
    notes or gloss lists; single-line [n] markers are footnote anchors."""
    txt = '\n'.join(block)
    txt = re.sub(r'\[[^\[\]]*\]', '', txt, flags=re.S)   # all bracketed spans
    out = []
    for ln in txt.split('\n'):
        s = ln.strip().replace('_', '')
        if not s:
            continue
        if re.match(r'^[IVXLCivxlc]+\.?$', s):            # stanza numeral
            continue
        if re.match(r'^[0-9]+\.?$', s):
            continue
        if re.match(r'^[-=*\s]+$', s):
            continue
        s = re.sub(r'\s+', ' ', s).strip()
        if s:
            out.append(s)
    return '\n'.join(out)

songs = []
for n, h in enumerate(hits):
    start = h['line'] + 1
    stop = hits[n+1]['line'] if n + 1 < len(hits) else body_end
    block = lines[start:stop]
    # drop a trailing subtitle/title fragment belonging to the next song
    while block and not block[-1].strip():
        block.pop()
    text = clean_song(block)
    songs.append({
        'title': h['title'], 'author': h['author'], 'year': h['year'],
        'text': text, 'n_words': len(WORD.findall(text)),
        'src_line': h['line'],
    })

json.dump(songs, open(OUT, 'w'), indent=1)
print(f"TOC entries: {len(toc)}   songs located: {len(songs)}")
missing = [t for t, a, y in toc if key(t) not in {key(s['title']) for s in songs}]
print("TOC titles not located:", missing)
from collections import Counter
c = Counter(s['author'] for s in songs)
print("\nauthors with >=2 songs:")
for a, n in c.most_common():
    if n >= 2:
        w = sum(s['n_words'] for s in songs if s['author'] == a)
        print(f"  {a:28s} songs={n:2d} words={w}")
print(f"\ntotal words: {sum(s['n_words'] for s in songs)}")
print("median song length:", sorted(s['n_words'] for s in songs)[len(songs)//2])
