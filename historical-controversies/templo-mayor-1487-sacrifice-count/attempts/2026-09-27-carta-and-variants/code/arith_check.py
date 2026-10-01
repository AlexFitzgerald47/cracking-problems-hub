#!/usr/bin/env python3
"""F3.3 (FREEZE.md): can Torquemada's 72,344 be produced from the other figures
attested for this event, using ONLY the operations frozen before looking?

Components (frozen): 80,400; 20,000; 19,600; 16,000; 24,000; 16,000; 24,400; 62,000; 72,000.
Operations (frozen): sum of any subset; difference of any two; one confusion between
adjacent vigesimal orders (1<->20, 20<->400, 400<->8000) applied to one digit-group of
80,400 (10 xiquipilli + 1 tzontli) or 20,000 (2 xiquipilli + 10 tzontli).

Recorded after the fact, not part of the frozen test: Chimalpahin's 24,600 and his
implied total 80,600 were found later in the session; the script also reports what
adding them would change (nothing: every value stays a multiple of 20).
"""
from itertools import combinations

TARGET = 72344
FROZEN = [80400, 20000, 19600, 16000, 24000, 16000, 24400, 62000, 72000]
LATE = [24600, 80600]  # exploratory only

def reachable(comps):
    out = set()
    for r in range(1, len(comps) + 1):
        for c in combinations(comps, r): out.add(sum(c))
    for a in comps:
        for b in comps: out.add(abs(a - b))
    # vigesimal digit-group confusions on 80,400 = [10, 1, 0, 0] and 20,000 = [2, 10, 0, 0]
    units = [8000, 400, 20, 1]
    for digits in ([10, 1, 0, 0], [2, 10, 0, 0]):
        for i, d in enumerate(digits):
            if d == 0: continue
            for j in (i - 1, i + 1):          # move this group to an adjacent order
                if 0 <= j < 4:
                    v = sum(dd * u for k, (dd, u) in enumerate(zip(digits, units)) if k != i)
                    out.add(v + d * units[j])
    return out

S = reachable(FROZEN)
print(f"frozen set: {len(S)} distinct values; 72,344 reachable: {TARGET in S}")
print("every frozen value divisible by 20:", all(v % 20 == 0 for v in S), "| 72,344 % 20 =", TARGET % 20)
near = sorted(S, key=lambda v: abs(v - TARGET))[:5]
print("nearest reachable values:", near)
S2 = reachable(FROZEN + LATE)
print(f"exploratory, with Chimalpahin's 24,600/80,600 added: 72,344 reachable: {TARGET in S2}; "
      f"all divisible by 20: {all(v % 20 == 0 for v in S2)}")
q, r = divmod(TARGET, 8000); t, r2 = divmod(r, 400); p, u = divmod(r2, 20)
print(f"72,344 in Nahuatl orders: {q} xiquipilli + {t} tzontli + {p} pohualli + {u} units")
