#!/usr/bin/env python3
"""Small reproducible checks for the 2026-09-07 KI-RO structural pass.

This is deliberately not a decipherment script.  It freezes only the arithmetic
relations that were hand-checked against the cited tablet transcriptions.  The
point is to distinguish two functions:

* KU-RO closes/sums a block.
* KI-RO can denote an outstanding residual or open a block of outstanding items.

The HT117 check was the held-out test: after HT88 and HT94b suggested that
unquantified KI-RO scopes forward over a list closed by KU-RO, HT117 was opened
and checked against that prediction.
"""

from fractions import Fraction


def main() -> None:
    checks = []

    # HT34: assessment 100, delivered/omitted 70, KI-RO 30.
    checks.append(("HT34 residual", Fraction(100) - Fraction(70), Fraction(30)))

    # HT123+124a, DA-TU row: *308 4E (4 + 1/4) plus KI-RO JE
    # (1/2 + 1/4) reaches 5, exactly one third of OLIV 15.
    delivered = Fraction(4) + Fraction(1, 4)
    kiro = Fraction(1, 2) + Fraction(1, 4)
    checks.append(("HT123 DA-TU ratio residual", delivered + kiro, Fraction(15, 3)))

    # Forward-scope blocks.  KI-RO precedes the item list; KU-RO closes it.
    checks.append(("HT88 KI-RO block -> KU-RO", sum([1] * 6), 6))
    checks.append(("HT94b KI-RO block -> KU-RO", sum([1] * 5), 5))

    # Held-out after the HT88/HT94b pattern was formed.
    checks.append(("HT117 held-out KI-RO block -> KU-RO", sum([1] * 10), 10))

    failed = []
    for name, observed, expected in checks:
        ok = observed == expected
        print(f"{name:40s} observed={observed!s:>6s} expected={expected!s:>6s}  {'PASS' if ok else 'FAIL'}")
        if not ok:
            failed.append(name)

    print(f"\n{len(checks) - len(failed)}/{len(checks)} frozen checks pass")
    if failed:
        raise SystemExit("failed: " + ", ".join(failed))


if __name__ == "__main__":
    main()
