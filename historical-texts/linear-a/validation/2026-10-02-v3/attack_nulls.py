#!/usr/bin/env python3
"""
ATTACK 2 — coincidence base rates for every numeric 'structure' the dossier reads.

Nulls are generated from the CORPUS'S OWN amount distribution (empirical, with
replacement), never from a uniform one.

  2a  HT119  '*327 34 : VIR 68 = exactly 1:2' -> fixed manpower ratio
  2b  HT85   '66 = 11 x 6' -> eleven standardized six-person gangs
  2c  HT85a  'the first four entries are multiples of six and the last three sum to
             12 = 2 x 6' -> the partition really is in sixes
  2d  HT122  'KU-RO 65 + KU-DA 1 = HT85's 66' cross-tablet bridge
"""
import random, collections, itertools, math
from corpus import (load_a, ht_tablet_faces, all_faces_with_words, is_word, to_val,
                    DIVIDER, DIVIDER_LINE, LACUNA, TOTALS, base, n_lacunae)

SEED = 20261002
N = 200000


def entry_amounts(A, scope="HT"):
    """Empirical pool: every integer attached to a list entry on a Haghia Triada
    tablet, excluding the integer that follows a total marker."""
    pool = []
    faces = ht_tablet_faces(A) if scope == "HT" else all_faces_with_words(A)
    for k, v in faces.items():
        ws = v["transliteratedWords"]
        for i, w in enumerate(ws):
            x = to_val(w)
            if x is None:
                continue
            prev = None
            for j in range(i - 1, -1, -1):
                if ws[j] in ("\n", DIVIDER, DIVIDER_LINE, LACUNA):
                    continue
                prev = ws[j]; break
            if prev in TOTALS:
                continue
            pool.append(x)
    return pool


def ratio_pairs(vals, k=2):
    return [(x, y) for i, x in enumerate(vals) for y in vals[i + 1:]
            if x and y and (abs(y - k * x) < 1e-9 or abs(x - k * y) < 1e-9)]


def main():
    A = load_a()
    rng = random.Random(SEED)
    pool = entry_amounts(A)
    print("=" * 78)
    print("ATTACK 2 — coincidence base rates, nulls drawn from the corpus's own amounts")
    print("=" * 78)
    print(f"  empirical amount pool: n={len(pool)} entry amounts on HT tablets")
    cnt = collections.Counter(pool)
    print(f"  most common amounts: {cnt.most_common(12)}")
    print(f"  mean {sum(pool)/len(pool):.2f}  median {sorted(pool)[len(pool)//2]:g}  "
          f"max {max(pool):g}")

    # ---------------------------------------------------------------- 2a
    print("\n--- 2a  HT119: an exact 2:1 pair somewhere in a 9-item list")
    hit2 = hit_any = hit_first2 = 0
    anyk = (2, 3, 4, 5)
    for _ in range(N):
        draw = [rng.choice(pool) for _ in range(9)]
        if ratio_pairs(draw, 2):
            hit2 += 1
        if any(ratio_pairs(draw, k) for k in anyk):
            hit_any += 1
        a, b = draw[0], draw[1]
        if a and b and (abs(b - 2 * a) < 1e-9 or abs(a - 2 * b) < 1e-9):
            hit_first2 += 1
    print(f"  P(at least one exact 2:1 pair in 9 corpus-like amounts)      = "
          f"{hit2/N:.4f}   ({hit2}/{N})")
    print(f"  P(at least one exact k:1 pair, k in {anyk})              = "
          f"{hit_any/N:.4f}")
    print(f"  P(the FIRST TWO entries are exactly 2:1)                     = "
          f"{hit_first2/N:.4f}")
    print("  observed on HT119: exactly one 2:1 pair, and it is the first two lines.")
    print("  -> the 'somewhere in the list' version of the observation is NOT rare;")
    print("     only the 'first two lines' version is, and that is the version the")
    print("     dossier actually states.  Note however that the pair is *327 34 :")
    print("     VIR 68, i.e. an UNIDENTIFIED sign against 'men'.  A 1:2 relation")
    print("     between an unknown unit and men is untestable: whatever the ratio")
    print("     had been, *327 could be defined as the unit that gives it.")

    # how many HT faces have ANY exact 2:1 pair among their entry amounts?
    print("\n  corpus check: how many HT tablet faces contain an exact 2:1 pair?")
    tot = has = 0
    examples = []
    for k, v in sorted(ht_tablet_faces(A).items()):
        ws = v["transliteratedWords"]
        vals = []
        for i, w in enumerate(ws):
            x = to_val(w)
            if x is None:
                continue
            prev = None
            for j in range(i - 1, -1, -1):
                if ws[j] in ("\n", DIVIDER, DIVIDER_LINE, LACUNA):
                    continue
                prev = ws[j]; break
            if prev in TOTALS:
                continue
            vals.append(x)
        if len(vals) < 2:
            continue
        tot += 1
        if ratio_pairs(vals, 2):
            has += 1; examples.append(k)
    print(f"    {has}/{tot} = {100*has/tot:.0f}% of HT faces with >=2 entry amounts "
          f"contain an exact 2:1 pair")
    print(f"    e.g. {examples[:18]}")
    print("    -> an exact 2:1 pair is a majority property of HT faces. As a")
    print("       'fixed manpower ratio' finding it carries no information.")

    # ---------------------------------------------------------------- 2b
    print("\n--- 2b  HT85: '66 = 11 x 6', eleven six-person gangs")
    print("  Degrees of freedom in the move: the gang size m is FREE; it is chosen")
    print("  after seeing the entry count on the other face.  The only constraint is")
    print("  total %% entrycount == 0 and quotient >= 2.")
    # base rate over every a/b face pair in the WHOLE corpus
    pairs = collections.defaultdict(dict)
    for k, v in all_faces_with_words(A).items():
        import re
        m = re.match(r'^(.+?)([ab])$', k)
        if m:
            pairs[m.group(1)][m.group(2)] = v
    tot = hits = 0; ex = []
    for t, f in sorted(pairs.items()):
        if set(f) != {"a", "b"}:
            continue
        for src, dst in (("a", "b"), ("b", "a")):
            ws = f[src]["transliteratedWords"]
            kur = [to_val(ws[i + 1]) for i, w in enumerate(ws)
                   if w in TOTALS and i + 1 < len(ws) and to_val(ws[i + 1])]
            n = sum(1 for w in f[dst]["transliteratedWords"] if is_word(w)) - 1
            for K in kur:
                if not K or n < 2:
                    continue
                tot += 1
                if K % n == 0 and K // n >= 2:
                    hits += 1; ex.append((t, src, int(K), n, int(K // n)))
    print(f"  base rate corpus-wide: {hits}/{tot} = {100*hits/max(tot,1):.0f}% of "
          f"(total on one face, entry count on the other) pairs give an integer "
          f"'gang size' >= 2")
    for e in ex:
        print("    ", e)
    print("  divisor count of 66 = ", len([d for d in range(1, 67) if 66 % d == 0]),
          "  ->", [d for d in range(1, 67) if 66 % d == 0])
    print("  so 66 admits 8 'k groups of m' stories; the one chosen is the one whose")
    print("  k matches the other face's entry count.  That is a fit, not a prediction.")

    # how often is a stated total divisible by a small integer >=2 at all?
    print("\n  P(a corpus-like total is divisible by some m in 2..12 with quotient>=2):")
    hit = 0
    tots = []
    for k, v in all_faces_with_words(A).items():
        ws = v["transliteratedWords"]
        for i, w in enumerate(ws):
            if w in TOTALS and i + 1 < len(ws) and to_val(ws[i + 1]):
                tots.append(to_val(ws[i + 1]))
    for T in tots:
        if any(T % m == 0 and T // m >= 2 for m in range(2, 13)):
            hit += 1
    print(f"    {hit}/{len(tots)} = {100*hit/len(tots):.0f}% of stated totals in the "
          f"whole corpus")

    # ---------------------------------------------------------------- 2c
    print("\n--- 2c  HT85a: 'first four entries are multiples of 6; last three sum to 12'")
    obs = [12, 12, 6, 24, 5, 3, 4]
    print(f"  observed entries {obs}, sum {sum(obs)}")
    print("  the claimant's partition statement, stated as a testable predicate:")
    print("    exists m>=2 and a split of the 7 entries into singly-divisible ones and")
    print("    a remainder whose sum is divisible by m, with total/m == 11")
    def passes(vals):
        T = sum(vals)
        for m in range(2, 13):
            if T % m or T // m < 2:
                continue
            div = [x for x in vals if x % m == 0]
            rest = [x for x in vals if x % m]
            if len(div) >= 1 and sum(rest) % m == 0:
                return True
        return False
    # any 7 corpus-like amounts
    hit = 0
    for _ in range(N):
        draw = [rng.choice(pool) for _ in range(7)]
        if passes(draw):
            hit += 1
    print(f"  P(a random 7-entry corpus-like list satisfies it) = {hit/N:.4f}")
    print("  -> the 'partitions into sixes' observation is ALMOST CERTAIN for any")
    print("     list: if m divides the total, the non-multiples' remainder is forced")
    print("     to be divisible by m. The statement is arithmetically vacuous.")
    print("     (sum(rest) == T - sum(div), and m | T, m | sum(div) => m | sum(rest).)")

    # ---------------------------------------------------------------- 2d
    print("\n--- 2d  HT122 'KU-RO 65 + KU-DA 1 = 66 = HT85 total' cross-tablet bridge")
    allt = sorted({to_val(v["transliteratedWords"][i + 1])
                   for k, v in all_faces_with_words(A).items()
                   for i, w in enumerate(v["transliteratedWords"])
                   if w in TOTALS and i + 1 < len(v["transliteratedWords"])
                   and to_val(v["transliteratedWords"][i + 1])})
    print(f"  distinct stated totals in the corpus: {len(allt)} -> "
          f"{[int(x) for x in allt]}")
    near = [x for x in allt if abs(x - 66) <= 1]
    print(f"  stated totals within +/-1 of 66: {[int(x) for x in near]}")
    print("  with a free +/-1 adjustment ('KU-DA 1'), the number of corpus totals that")
    print(f"  'reconcile' with 66 is {len(near)} of {len(allt)}; and the adjustment term")
    print("  was selected AFTER seeing the gap.  The bridge has one free parameter and")
    print("  one observation: it cannot be evidence either way.")


if __name__ == "__main__":
    main()
