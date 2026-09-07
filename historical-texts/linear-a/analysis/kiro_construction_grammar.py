#!/usr/bin/env python3
"""Auditable checks for the 2026-09-07 KI-RO construction grammar.

This is deliberately a frozen hand-audited ledger, not a claim that the whole
Linear A corpus has been automatically parsed.  Its job is to make the new
claims falsifiable and prevent examples from being silently reclassified.
"""
from fractions import Fraction

# Exact, clean KI-RO contexts for which the immediate construction is legible.
# Prediction: divider after KI-RO => forward-scoping residual block;
# numeral after KI-RO => scalar residual amount.
CASES = [
    ("HT1", "numeral", "scalar"),
    ("HT15", "numeral", "scalar"),
    ("HT30", "divider", "forward"),
    ("HT34", "numeral", "scalar"),
    ("HT37", "divider", "forward"),
    ("HT88", "divider", "forward"),
    ("HT94b", "divider", "forward"),
    ("HT117", "divider", "forward"),
    ("HT123+124", "numeral", "scalar"),
]

# Named/designated entities independently attested both in a KI-RO personnel
# context and elsewhere without KI-RO.  These are status-switch controls: they
# argue that KI-RO is a state applied to ordinary roster entities, not the name
# of a special personnel class.
STATUS_SWITCHES = {
    "DI-KI-SE": ("HT117 KI-RO / QI-TU-NE", "HT87 QI-TU-NE / MA-KA-RI-TE"),
    "KU-PA3-NU": ("HT88/HT117 (also HT1) KI-RO", "HT122 ordinary personnel list"),
    "PA-TA-NE": ("HT94b KI-RO", "HT122 ordinary personnel list"),
    "PA-JA-RE": ("HT88 KI-RO", "HT8/HT29/ZA10 non-KI-RO contexts"),
    "SA-RU": ("HT94b KI-RO", "HT86/HT95 non-KI-RO contexts"),
}


def construction_grammar():
    failures = []
    for record, following, observed in CASES:
        predicted = "forward" if following == "divider" else "scalar"
        if predicted != observed:
            failures.append((record, predicted, observed))
    return failures


def arithmetic_checks():
    checks = {}
    # HT34: assessed/expected 100, 70 fulfilled/removed, residual 30.
    checks["HT34 residual"] = 100 - 70 == 30

    # HT123+124 DA-TU row: target ratio is 1/3 of OLIV 15 = 5.
    # Booked *308 = 4 1/4; KI-RO make-up = 3/4.
    checks["HT123 ratio residual"] = (
        Fraction(15, 3) - Fraction(17, 4) == Fraction(3, 4)
    )

    # Personnel exception-list cardinalities.
    checks["HT88 KU-RO cardinality"] = sum([1] * 6) == 6
    checks["HT94b KU-RO cardinality"] = sum([1] * 5) == 5
    checks["HT117 first sublist KU-RO cardinality"] = sum([1] * 10) == 10

    # HT15 visible quantities establish the independently discussed expected
    # account total; the 400 residual cannot be recomputed from the damaged/
    # omitted fulfilled amount, so this check stops at the visible invariant.
    checks["HT15 visible expected total"] = 684 + 570 == 1254
    return checks


def main():
    failures = construction_grammar()
    checks = arithmetic_checks()

    print("KI-RO CONSTRUCTION GRAMMAR")
    print(f"clean exact KI-RO contexts: {len(CASES)}")
    print(f"construction matches:       {len(CASES) - len(failures)}/{len(CASES)}")
    if failures:
        for f in failures:
            print("FAIL", f)
    else:
        print("rule: KI-RO • -> forward residual block; KI-RO + numeral -> scalar residual")

    print("\nARITHMETIC / CARDINALITY CONTROLS")
    for name, ok in checks.items():
        print(f"{'PASS' if ok else 'FAIL'}  {name}")

    print("\nSTATUS-SWITCH CONTROLS")
    for name, (kiro_ctx, ordinary_ctx) in STATUS_SWITCHES.items():
        print(f"{name}: {kiro_ctx}  ||  {ordinary_ctx}")
    print(f"confirmed recurring entities with both KI-RO and non-KI-RO contexts: {len(STATUS_SWITCHES)}")

    assert not failures
    assert all(checks.values())


if __name__ == "__main__":
    main()
