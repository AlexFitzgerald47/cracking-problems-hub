# Attempt: what do the two public Kryptos K4 cribs actually rule out?

**Date:** 2026-09-04 · **Status:** complete; three eliminations and one non-significant lead · **Reproducible:** yes

K4 is 97 characters with 24 characters of Sanborn-confirmed plaintext at known
positions (`EASTNORTHEAST` at 22–34, `BERLINCLOCK` at 64–74). That is unusual
leverage for an unsolved cipher, and it is mostly spent on narrow hypotheses.
This attempt spends it on the widest hypotheses it will reach, and measures how
much each answer is worth.

## Headline

- **Pure transposition is eliminated**, by a two-line argument that needs no search.
- **The Vigenère family is eliminated** (Vigenère, variant, Beaufort) at every
  period where the cribs have any power at all.
- **The general periodic-polyalphabetic family is barely touched** — the cribs
  eliminate only 19 of 97 periods against 72.6 expected by chance. Worth knowing
  before anyone spends a month on that family believing the cribs constrain it.
- **Composite schemes (transposition then polyalphabetic) show no signal above
  chance** across 12,901 hypotheses — Vigenère and Beaufort survive at or below
  the chance rate. The period-19 lead that looked interesting against the
  identity transposition does not survive this and is withdrawn.
- **The cribs' power has an exact structural source**: a period is testable iff
  two crib positions differing by a multiple of it carry the same plaintext
  letter. Verified with no overlap. This turns crib valuation into a count.
- **A ten-character third crib would roughly double the testable periods** — and
  it should be asked for near position 44–47. A crib abutting an existing one is
  worth almost nothing.

## Method

Any periodic polyalphabetic cipher of period *p* — Vigenère, Beaufort, all four
Quagmires, any keyed-alphabet scheme — applies one fixed monoalphabetic
substitution to every position in a residue class mod *p*. So within a class the
plaintext→ciphertext map must be a partial bijection. A *collision* (one
plaintext letter going to two ciphertext letters) or a *merge* (two plaintext
letters going to one ciphertext letter) eliminates period *p* for the entire
family at once, with no need to know the alphabet or the key.

Every elimination is paired with a null: random ciphertext letters at the crib
positions, drawn from K4's own letter distribution, 20,000 draws. A period that
"survives" is only informative if the null would usually have been caught.

```
data/k4.json               ciphertext + cribs, with the self-check described in it
src/k4.py                  loader; verifies the ciphertext against the published cribs
src/crib_constraints.py    general polyalphabetic + Vigenère + transposition tests
src/beaufort.py            Beaufort shift test
src/power_check.py         multiple-comparison and power accounting
src/composite.py           transposition x periodic polyalphabetic composites
src/crib_value.py          the exact power rule, and what another crib would buy
results/                   raw JSON
```

## Reproduction

```
pip install numpy
cd src
python crib_constraints.py   # ~3 min
python beaufort.py           # ~2 min
python power_check.py
python composite.py          # ~1 min
python crib_value.py         # ~2 min
```
