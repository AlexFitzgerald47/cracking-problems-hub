"""What do the two public cribs actually rule out?

K4 is 97 characters with 24 characters of confirmed plaintext at known
positions. That is a lot of leverage if it is spent on a general enough
hypothesis.

The general test used here: *any* periodic polyalphabetic cipher of period p —
Vigenere, Beaufort, variant Beaufort, all four Quagmires, any keyed-alphabet
scheme — applies one fixed monoalphabetic substitution to every position in a
given residue class mod p. So within a residue class the plaintext-to-
ciphertext map must be a partial bijection. Two ways to violate that:

  collision : one plaintext letter maps to two different ciphertext letters
  merge     : two different plaintext letters map to the same ciphertext letter

Either violation eliminates period p for that entire family at once, without
needing to know the alphabet or the key. Vigenere proper is then tested
separately as the stricter special case (the shift must be constant within a
class), and pure transposition separately again (the plaintext must be an
anagram of the ciphertext).

The point of the null model is to say how much any of this is worth: a period
that "survives" is only interesting if random data would usually have been
caught.
"""
import sys, os, json, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import k4

SEED = 20260904
N_NULL = 20000
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'crib_results.json')


def violations(ct, known, p):
    """(collisions, merges, testable_pairs) for period p."""
    fwd = collections.defaultdict(dict)   # residue -> {pt: ct}
    rev = collections.defaultdict(dict)   # residue -> {ct: pt}
    coll = merge = 0
    for i, pt in sorted(known.items()):
        r = i % p
        c = ct[i]
        if pt in fwd[r] and fwd[r][pt] != c:
            coll += 1
        else:
            fwd[r][pt] = c
        if c in rev[r] and rev[r][c] != pt:
            merge += 1
        else:
            rev[r][c] = pt
    counts = collections.Counter(i % p for i in known)
    pairs = sum(n * (n - 1) // 2 for n in counts.values())
    return coll, merge, pairs


def vigenere_violations(ct, known, p):
    """Stricter: the shift (C - P) mod 26 must be constant within a class."""
    shifts = collections.defaultdict(set)
    for i, pt in known.items():
        shifts[i % p].add((ord(ct[i]) - ord(pt)) % 26)
    return sum(len(v) - 1 for v in shifts.values())


def main():
    rng = np.random.default_rng(SEED)
    d = k4.load()
    ct, known = d['ciphertext'], d['known']
    res = {'seed': SEED, 'n': len(ct), 'n_crib_chars': len(known),
           'crib_positions': sorted(known)}

    # --- null: what does a random ciphertext do? -----------------------------
    letters = np.array([ord(c) - 65 for c in ct])
    freq = np.bincount(letters, minlength=26) / len(letters)
    idx = sorted(known)
    null_pass = collections.defaultdict(int)
    null_pass_vig = collections.defaultdict(int)
    for _ in range(N_NULL):
        draw = rng.choice(26, size=len(idx), p=freq)
        fake = list(ct)
        for j, i in enumerate(idx):
            fake[i] = chr(65 + draw[j])
        fake = ''.join(fake)
        for p in range(1, 98):
            c, m, _ = violations(fake, known, p)
            if c + m == 0:
                null_pass[p] += 1
            if vigenere_violations(fake, known, p) == 0:
                null_pass_vig[p] += 1

    rows = []
    for p in range(1, 98):
        c, m, pairs = violations(ct, known, p)
        v = vigenere_violations(ct, known, p)
        rows.append({
            'period': p, 'collisions': c, 'merges': m, 'testable_pairs': pairs,
            'survives_general': c + m == 0,
            'vigenere_shift_conflicts': v, 'survives_vigenere': v == 0,
            'null_survival_rate_general': null_pass[p] / N_NULL,
            'null_survival_rate_vigenere': null_pass_vig[p] / N_NULL,
        })
    res['periods'] = rows
    res['n_null'] = N_NULL

    surv = [r['period'] for r in rows if r['survives_general']]
    surv_v = [r['period'] for r in rows if r['survives_vigenere']]
    res['surviving_periods_general'] = surv
    res['surviving_periods_vigenere'] = surv_v
    # a surviving period is only informative if the null usually fails
    res['informative_survivors_general'] = [
        r['period'] for r in rows
        if r['survives_general'] and r['null_survival_rate_general'] < 0.05]

    # --- pure transposition --------------------------------------------------
    ct_counts = collections.Counter(ct)
    crib_counts = collections.Counter(known.values())
    short = {ch: crib_counts[ch] - ct_counts.get(ch, 0)
             for ch in crib_counts if crib_counts[ch] > ct_counts.get(ch, 0)}
    res['pure_transposition'] = {
        'crib_letter_counts': dict(crib_counts),
        'letters_short_in_ciphertext': short,
        'consistent': len(short) == 0,
        'note': ('Under a pure transposition the plaintext is an anagram of the '
                 'ciphertext, so every crib letter must be available in the '
                 'ciphertext multiset.'),
    }

    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)

    print('K4: %d chars, %d crib characters at known positions' % (res['n'], res['n_crib_chars']))
    print()
    print('General periodic polyalphabetic (covers Vigenere, Beaufort, all Quagmires):')
    print('  periods 1-97 tested; %d eliminated, %d survive' % (97 - len(surv), len(surv)))
    print('  surviving:', surv)
    print('  of those, informative (null survival < 5%%): %s' % res['informative_survivors_general'])
    print()
    print('Vigenere proper (constant shift per class):')
    print('  %d eliminated, %d survive' % (97 - len(surv_v), len(surv_v)))
    print('  surviving:', surv_v)
    print()
    print('Pure transposition consistent with cribs:', res['pure_transposition']['consistent'],
          res['pure_transposition']['letters_short_in_ciphertext'])
    print()
    print('period  coll merge pairs  gen  null%%   vig  null%%')
    for r in rows[:24]:
        print('  %3d    %3d  %3d  %4d   %s  %5.1f   %s  %5.1f' % (
            r['period'], r['collisions'], r['merges'], r['testable_pairs'],
            'Y' if r['survives_general'] else '.', 100 * r['null_survival_rate_general'],
            'Y' if r['survives_vigenere'] else '.', 100 * r['null_survival_rate_vigenere']))


if __name__ == '__main__':
    main()
