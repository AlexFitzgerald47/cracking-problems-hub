#!/usr/bin/env python3
"""Reduce raw concordance hits to one row per attestation.

Two sources of double-counting:
  1. Perseus ships several editions of the same work (Celsus De Medicina has three).
     Fix: keep exactly one edition per Perseus work id, chosen deterministically.
  2. The Latin Library and Perseus both carry some works (Caesar, Columella, ...).
     Fix: after (1), drop a Perseus hit whose +-4 alphabetic-word context already
     appears in a Latin Library hit.
Whatever survives is a distinct attestation.
"""
import json, re, sys, collections

def work_id(h):
    if h['corpus'] == 'perseus':
        p = h['file'].split('/')
        return ('perseus', p[1] + '/' + p[2])
    return ('latin_library', h['file'])

def ctxsig(h, n=4):
    l = h['left'].split()[-n:]
    r = h['right'].split()[:n]
    s = ' '.join(l + [h['norm_form']] + r)
    return re.sub(r'[^a-z]', '', s.lower())

def main(inp, outp):
    d = json.load(open(inp))
    hits = d['hits']

    # (1) one edition per Perseus work
    per_work_files = collections.defaultdict(set)
    for h in hits:
        if h['corpus'] == 'perseus':
            per_work_files[work_id(h)[1]].add(h['file'])
    chosen = {w: sorted(fs)[0] for w, fs in per_work_files.items()}
    step1 = [h for h in hits
             if h['corpus'] != 'perseus' or h['file'] == chosen[work_id(h)[1]]]

    # (2) cross-corpus overlap: Latin Library wins
    ll_sigs = {ctxsig(h) for h in step1 if h['corpus'] == 'latin_library'}
    step2 = [h for h in step1
             if h['corpus'] == 'latin_library' or ctxsig(h) not in ll_sigs]

    # (3) residual exact-duplicate guard inside a single file
    seen, final = set(), []
    for h in step2:
        k = (h['file'], h['token_index'])
        if k in seen:
            continue
        seen.add(k)
        final.append(h)

    json.dump({'n_raw': len(hits), 'n_edition_dedup': len(step1),
               'n_cross_dedup': len(step2), 'n_final': len(final),
               'perseus_editions_kept': chosen, 'hits': final},
              open(outp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"raw {len(hits)} -> one-edition {len(step1)} -> cross-corpus {len(step2)} -> final {len(final)}")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
