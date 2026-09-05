"""Loads the K4 ciphertext and the two public cribs, and verifies them.

The cribs double as a transcription check: Sanborn's releases fix what the
ciphertext must read at those positions, so a corrupted ciphertext would fail
`load()` rather than silently poison everything downstream.
"""
import json, os

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'k4.json')
EXPECTED = {(22, 34): 'FLRVQQPRNGKSS', (64, 74): 'NYPVTTMZFPK'}


def load():
    with open(DATA) as fh:
        d = json.load(fh)
    ct = d['ciphertext']
    assert len(ct) == 97, 'K4 must be 97 characters, got %d' % len(ct)
    known = {}          # zero-based position -> plaintext letter
    for c in d['cribs']:
        s, e = c['start'] - 1, c['end']
        seg = ct[s:e]
        assert len(seg) == len(c['plaintext']), 'crib %s length mismatch' % c['plaintext']
        assert EXPECTED[(c['start'], c['end'])] == seg, \
            'ciphertext does not match the published crib segment at %d-%d' % (c['start'], c['end'])
        for k, ch in enumerate(c['plaintext']):
            known[s + k] = ch
    d['known'] = known
    return d
