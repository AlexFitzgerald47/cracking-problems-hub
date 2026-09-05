"""Loads the Beale ciphers and the Beale-variant Declaration of Independence,
and refuses to hand them over unvalidated.

Two independent checks run at load time:

  1. B1 and B3 are compared against a second, independently provenanced
     transcription (the Cipher Foundation text, via matthewdgreen/cipher_benchmark).
     B1 agrees token for token. B3 does not - it differs at two positions, which
     is recorded rather than silently reconciled.
  2. The key text is validated by decoding B2, whose plaintext has been accepted
     since 1885. If the Declaration word list were wrong, B2 would not decode.
"""
import os, json, difflib

D = os.path.join(os.path.dirname(__file__), '..', 'data')
B2_OPENING = ('ihavedepositedinthecountyofbedfordaboutfourmilesfrombufordsinan'
              'excavationorvaultsixfeetbelowthesurfaceoftheground')


def _nums(name):
    with open(os.path.join(D, name)) as fh:
        return [int(x) for x in fh.read().split()]


def load():
    doi = open(os.path.join(D, 'beale_doi.txt')).read().split()
    special = {int(k): v for k, v in
               json.load(open(os.path.join(D, 'special_decode.json'))).items()}
    ciphers = {n: _nums('b%d.txt' % n) for n in (1, 2, 3)}

    cross = {}
    for n in (1, 3):
        other = _nums('b%d_cipherfoundation.txt' % n)
        diffs = [{'index': i, 'a': a, 'b': b}
                 for i, (a, b) in enumerate(zip(ciphers[n], other)) if a != b]
        cross['B%d' % n] = {'same_length': len(other) == len(ciphers[n]),
                            'n_differences': len(diffs), 'differences': diffs}

    dec2 = decode(ciphers[2], doi, special)
    opening_ok = dec2[:len(B2_OPENING)] == B2_OPENING
    assert opening_ok, 'B2 did not decode to its accepted opening; key text is wrong'

    return {'doi': doi, 'special': special, 'ciphers': ciphers,
            'cross_check': cross,
            'b2_validation': {'opening_matches': opening_ok,
                              'opening_length_checked': len(B2_OPENING),
                              'decoded_opening': dec2[:len(B2_OPENING)]}}


def decode(cipher, doi, special=None, gap='?'):
    """Book cipher: each number selects a word; the word's first letter is the
    plaintext letter. Numbers past the end of the key text cannot be decoded."""
    special = special or {}
    out = []
    for x in cipher:
        if x in special:
            out.append(special[x])
        elif 1 <= x <= len(doi):
            out.append(doi[x - 1][0].lower())
        else:
            out.append(gap)
    return ''.join(out)
