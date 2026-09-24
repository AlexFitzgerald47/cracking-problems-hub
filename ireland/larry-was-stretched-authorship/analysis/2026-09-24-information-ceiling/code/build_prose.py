#!/usr/bin/env python3
"""Build non-song prose corpora for authors who also appear in *Musa Pedestris*.

Leakage hazard: Ainsworth's canting songs are printed INSIDE Rookwood, Egan's
inside Life in London, Sims's ballads alongside his journalism. Any overlap
between a prose profile and the song being attributed would manufacture a
cross-register "success" out of nothing. Defence, in order:
  1. drop short lines (verse is typeset short) and indented blocks;
  2. delete any line sharing a 5-gram with any Musa song by ANY author;
  3. report the residual 5-gram overlap so the reader can check it is zero.
"""
import json, re, sys, os
from collections import Counter

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
songs = json.load(open(f'{S}/corpus/musa_songs.json'))
WORD = re.compile(r"[a-z][a-z']*")

def toks(t):
    return WORD.findall(t.lower().replace('’', "'"))

song_5g = set()
for s in songs:
    w = toks(s['text'])
    for i in range(len(w) - 4):
        song_5g.add(tuple(w[i:i+5]))

SOURCES = {
    'W. H. Ainsworth': ['prose/ainsworth_rookwood.txt'],
    'Pierce Egan':     ['prose/egan_lifeinlondon.txt'],
    'W. E. Henley':    ['prose/henley_views.txt'],
    'G. R. Sims':      ['prose/sims_howpoorlive.txt'],
    'Thomas Dekker':   ['prose/dekker_nondramatic.txt'],
}

def clean(path):
    raw = open(f'{S}/corpus/{path}', encoding='utf-8', errors='replace').read()
    out, dropped_verse, dropped_leak = [], 0, 0
    for ln in raw.split('\n'):
        s = ln.rstrip()
        stripped = s.strip()
        if not stripped:
            continue
        # page furniture / running heads / numerals
        if re.match(r'^[\dIVXLCivxlc\.\s\-\[\]]+$', stripped):
            continue
        if len(stripped) < 35:            # verse lines, headings, catchwords
            dropped_verse += 1
            continue
        if stripped.isupper():
            continue
        w = toks(stripped)
        if len(w) < 7:
            continue
        if any(tuple(w[i:i+5]) in song_5g for i in range(len(w) - 4)):
            dropped_leak += 1
            continue
        out.append(re.sub(r'\s+', ' ', stripped))
    return '\n'.join(out), dropped_verse, dropped_leak

corpora = {}
for author, paths in SOURCES.items():
    txt, dv, dl = [], 0, 0
    for p in paths:
        t, a, b = clean(p)
        txt.append(t); dv += a; dl += b
    body = '\n'.join(txt)
    w = toks(body)
    # residual leakage check
    resid = sum(1 for i in range(len(w) - 4) if tuple(w[i:i+5]) in song_5g)
    corpora[author] = body
    print(f"{author:20s} {len(w):7d} prose words   "
          f"short/verse lines dropped: {dv:6d}   song-5gram lines dropped: {dl:3d}   "
          f"residual song 5-grams: {resid}")

json.dump(corpora, open(f'{S}/corpus/prose_corpora.json', 'w'))
