#!/usr/bin/env python3
"""Split Gutenberg etext 18 (The Federalist Papers) into 85 papers with the
bylines as printed. Papers 49-58, 62, 63 carry the byline HAMILTON OR MADISON
in this edition -- those are the disputed papers (Mosteller & Wallace 1964).
"""
import json, re, sys
SRC, OUT = sys.argv[1], sys.argv[2]
txt = open(SRC, encoding='utf-8').read()
lines = txt.split('\n')

starts = [i for i, l in enumerate(lines) if l.strip() == 'THE FEDERALIST.']
ROMAN = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
def roman(s):
    s = s.strip().rstrip('.').upper(); tot = 0
    for i, ch in enumerate(s):
        v = ROMAN.get(ch, 0)
        tot += -v if i+1 < len(s) and ROMAN.get(s[i+1],0) > v else v
    return tot

AUTH = re.compile(r'^(HAMILTON|MADISON|JAY|HAMILTON AND MADISON|HAMILTON OR MADISON|MADISON, WITH HAMILTON)\s*$')
papers = []
for k, st in enumerate(starts):
    stop = starts[k+1] if k+1 < len(starts) else len(lines)
    blk = lines[st:stop]
    num = None
    for l in blk[:6]:
        m = re.match(r'^No\.\s+([IVXLC]+)\.?\s*$', l.strip())
        if m: num = roman(m.group(1)); break
    author, ai = None, None
    for i, l in enumerate(blk[:40]):
        m = AUTH.match(l.strip())
        if m: author, ai = m.group(1), i; break
    body = '\n'.join(blk[ai+1:]) if ai is not None else '\n'.join(blk[6:])
    body = body.split('PUBLIUS')[0]
    body = re.sub(r'^\s*To the People of the State of New York:?', '', body.strip())
    nw = len(re.findall(r"[A-Za-z][A-Za-z']*", body))
    papers.append({'no': num, 'author': author, 'n_words': nw, 'text': body.strip()})

json.dump(papers, open(OUT,'w'), indent=1)
from collections import Counter
print('papers:', len(papers))
print(Counter(p['author'] for p in papers))
print('disputed nos:', sorted(p['no'] for p in papers if p['author'] and 'OR' in p['author']))
print('total words:', sum(p['n_words'] for p in papers))
