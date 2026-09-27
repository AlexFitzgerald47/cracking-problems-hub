#!/usr/bin/env python3
"""F3.4 (FREEZE.md): is Torquemada's OWN dedication narrative (Monarquia Indiana
lib. II cap. 63, the 72,344 chapter) in the Cronica X family?

The 2026-09-24 instrument is reused unchanged -- same five texts, same
normalisation, same rare-token rule (len >= 6, corpus count <= 60), same
2,400-token windows, same 500-draw null, same seed. The single change: the
2026-09-24 run anchored Torquemada on 'fueron ochenta mil', i.e. the chapter he
copies from Mendieta, so his own narrative of the dedication was never tested.
Here his window is centred on cap. 63 instead. The Mendieta-chapter anchor is
kept as a second Torquemada row ('torq_mendieta') so the old result reproduces.

Run from the directory that holds raw/ (see ../../2026-09-24-numeral-or-count/code/fetch_corpus.sh):
  PYTHONPATH=<path to 2026-09-24 code/> python3 content_overlap_torq63.py
The 5-gram block at the end is exploratory, not frozen.
"""
import random, itertools, statistics, collections
from parallels import words, window, find, overlap

random.seed(20260924)
TEXTS = {'duran': 'raw/duran_v1_scanA.txt', 'tezozomoc': 'raw/tezozomoc_scanB.txt',
         'mendieta': 'raw/mendieta_scanA.txt', 'torquemada': 'raw/torquemada_v1.txt',
         'ixtlilxochitl': 'raw/ixtl_B0.txt'}
W = {k: words(v) for k, v in TEXTS.items()}
GLOBAL = collections.Counter()
for k in W: GLOBAL.update(W[k])
def rare(ws): return {t for t in ws if len(t) >= 6 and GLOBAL[t] <= 60}
def jac(a, b):
    ra, rb = rare(a), rare(b)
    if not ra or not rb: return 0.0, 0
    return len(ra & rb) / min(len(ra), len(rb)), len(ra & rb)

HALF = 1200
ANCH = {'duran': ('duran', 'turo este sacrificio quatro dias arreo'),
        'tezozomoc': ('tezozomoc', 'duro las muertes y cruel carniceria'),
        'mendieta': ('mendieta', 'se sacrificaron ochenta mil y cuatrocientas personas'),
        'ixtlilxochitl': ('ixtlilxochitl', 'ochenta mil y cuatrocientos hombres en este modo'),
        'torq_mendieta': ('torquemada', 'fueron ochenta mil'),                          # 2026-09-24 anchor
        'torq_cap63': ('torquemada', 'elta Diabolica Dedicacion , fetenta y dos')}      # this session
WIN, SRC = {}, {}
for lab, (txt, phrase) in ANCH.items():
    i = find(W[txt], phrase)
    print(f"anchor {lab:14s} in {txt:13s}: {'at ' + str(i) if i is not None else 'NOT FOUND'}")
    WIN[lab], SRC[lab] = window(W[txt], i, HALF), txt

def run(a, b, stat, ndraw):
    obs, ni = stat(WIN[a], WIN[b])
    ta, tb = SRC[a], SRC[b]
    null = []
    for _ in range(ndraw):
        ca = random.randrange(HALF, len(W[ta]) - HALF); cb = random.randrange(HALF, len(W[tb]) - HALF)
        null.append(stat(window(W[ta], ca, HALF), window(W[tb], cb, HALF))[0])
    mu = statistics.mean(null); sd = statistics.pstdev(null) or 1e-12
    p = (sum(1 for x in null if x >= obs) + 1) / (len(null) + 1)
    return obs, ni, mu, sd, (obs - mu) / sd, p

PAIRS = [('duran', 'tezozomoc'),                      # calibration: must reproduce z = 3.7
         ('mendieta', 'torq_mendieta'),               # calibration: must reproduce z = 40.1
         ('duran', 'torq_cap63'), ('tezozomoc', 'torq_cap63'),   # F3.4
         ('ixtlilxochitl', 'torq_cap63'), ('mendieta', 'torq_cap63')]
print("\n=== rare-token (content) overlap, 500-draw null ===")
print(f"{'pair':30s} {'obs':>7s} {'shared':>6s} {'null mu':>8s} {'sd':>7s} {'z':>6s} {'p':>7s}")
for a, b in PAIRS:
    obs, ni, mu, sd, z, p = run(a, b, jac, 500)
    print(f"  {a:13s}x {b:14s} {obs:7.4f} {ni:6d} {mu:8.4f} {sd:7.4f} {z:6.1f} {p:7.4f}" + ('   <<<' if p <= 0.01 else ''))
for a, b in [('duran', 'torq_cap63'), ('tezozomoc', 'torq_cap63')]:
    print(f"\nshared rare tokens {a} x {b}:", sorted(rare(WIN[a]) & rare(WIN[b])))

print("\n=== exploratory: 5-gram overlap, 300-draw null ===")
for a, b in [('duran', 'torq_cap63'), ('tezozomoc', 'torq_cap63')]:
    obs, ni, mu, sd, z, p = run(a, b, overlap, 300)
    print(f"  {a:13s}x {b:14s} {obs:7.4f} {ni:6d} {mu:8.4f} {sd:7.4f} {z:6.1f} {p:7.4f}")
