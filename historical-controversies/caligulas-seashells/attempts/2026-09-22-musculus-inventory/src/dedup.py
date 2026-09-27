#!/usr/bin/env python3
"""Collapse concordance hits to unique attestations.

The two corpora overlap (Caesar is in both) and Perseus ships multiple editions of the
same work, so raw hit counts triple-count some passages. We key each attestation on
(normalised form, normalised +-6-word context) and keep one representative, preferring
the Latin Library copy for readability of the locator.
"""
import json, re, sys, collections, hashlib

def ctxkey(h, n=6):
    l = h['left'].split()[-n:]
    r = h['right'].split()[:n]
    sig = ' '.join(l) + ' | ' + h['norm_form'] + ' | ' + ' '.join(r)
    sig = re.sub(r'[^a-z |]', '', sig.lower())
    return hashlib.md5(sig.encode()).hexdigest()

def main(inp, outp):
    d = json.load(open(inp))
    buckets = collections.OrderedDict()
    for h in d['hits']:
        k = ctxkey(h)
        buckets.setdefault(k, []).append(h)
    uniq = []
    for k, v in buckets.items():
        rep = sorted(v, key=lambda x: (x['corpus'] != 'latin_library', x['file']))[0]
        rep = dict(rep)
        rep['n_copies'] = len(v)
        rep['copies'] = sorted({x['file'] for x in v})
        rep['key'] = k
        uniq.append(rep)
    json.dump({'n_unique': len(uniq), 'n_raw': len(d['hits']), 'hits': uniq},
              open(outp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"raw {len(d['hits'])} -> unique {len(uniq)}")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
