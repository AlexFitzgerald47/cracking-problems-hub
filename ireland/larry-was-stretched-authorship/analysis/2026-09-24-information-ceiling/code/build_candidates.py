#!/usr/bin/env python3
"""Build the Larry candidate corpora and the two Larry witnesses."""
import re, os, json, sys
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = re.compile(r"[A-Za-z][A-Za-z']*")

def clean_prose(path, drop_short=35):
    out = []
    for ln in open(f'{S}/corpus/cand/{path}', encoding='utf-8', errors='replace'):
        s = ln.strip()
        if not s or s.isupper():
            continue
        if re.match(r'^[\dIVXLCivxlc\.\s\-\[\]\*]+$', s):
            continue
        if len(s) < drop_short:
            continue
        out.append(re.sub(r'\s+', ' ', s))
    return '\n'.join(out)

def clean_verse(path, lo=18, hi=60):
    """Verse lines are short; keep the band and drop prose and furniture."""
    out = []
    for ln in open(f'{S}/corpus/cand/{path}', encoding='utf-8', errors='replace'):
        s = re.sub(r'\s+', ' ', ln.strip())
        if not s or s.isupper():
            continue
        if re.match(r'^[\dIVXLCivxlc\.\s\-\[\]\*,]+$', s):
            continue
        if not (lo <= len(s) <= hi):
            continue
        if sum(c.isdigit() for c in s) > 2:
            continue
        out.append(s)
    return '\n'.join(out)

def strip_google(t):
    """Drop the Google-scan boilerplate that opens every *goog scan."""
    i = t.find('About Google Book Search')
    return t[i:] if i > 0 else t

cands = {}
cands['Curran (oratory)'] = clean_prose('curran_speeches.txt')
cands['Burrowes (sermons)'] = strip_google(clean_prose('burrowes_sermons.txt')) + '\n' + \
                              strip_google(clean_prose('burrowes_discourses.txt'))
cands['Lysaght (verse)'] = strip_google(clean_verse('lysaght1811.txt'))
cands['Curran (verse)'] = open(f'{S}/corpus/candidates/curran_verse.txt').read()

# --- the two Larry witnesses
cands_out = {}
for k, v in cands.items():
    n = len(W.findall(v))
    cands_out[k] = v
    print(f"{k:22s} {n:7d} words")

raw = open(f'{S}/corpus/univsong_v3_byu.txt', errors='replace').read().split('\n')
us = []
for i in range(34041, 34146):
    s = re.sub(r'\s+', ' ', raw[i]).strip()
    if not s:
        continue
    if 'UNIVERSAL SONGSTER' in s or s.strip() == '141':
        continue
    us.append(s)
us = '\n'.join(us)
open(f'{S}/corpus/candidates/larry_universalsongster1828.txt', 'w').write(us)
print(f"\nLarry, Universal Songster 1828 : {len(W.findall(us))} words")
farmer = open(f'{S}/corpus/larry_farmer.txt').read()
print(f"Larry, Farmer 1896             : {len(W.findall(farmer))} words")
json.dump(cands_out, open(f'{S}/corpus/larry_candidates.json', 'w'))
