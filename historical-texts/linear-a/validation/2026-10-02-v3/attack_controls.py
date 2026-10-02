#!/usr/bin/env python3
"""
ATTACK 8 — the claim 'arithmetic/cardinality controls: 6/6 pass'
(analysis/2026-09-07-kiro-unified-residual-grammar.md; PROGRESS.md).

Each of the six is examined against the raw corpus and against the commentary the
claimant itself cites.

  8a  HT88 / HT94b / HT117a: are these arithmetic CONTROLS, or tautologies?
  8b  HT34: does witness A contain the number the control needs?
  8c  HT123+124: does the ratio reading survive all four rows, or only the one
      row the claimant quotes?
  8d  HT15: is the 'held-out semantic HIT' a derivation or a gloss?
"""
import collections, re
from corpus import (load_a, all_faces_with_words, is_word, to_val, is_num,
                    DIVIDER, DIVIDER_LINE, LACUNA, TOTALS)

FR = {"¹⁄₃": 1/3, "¹⁄₄": .25, "³⁄₄": .75,
      "¹⁄₂": .5, "≈ ¹⁄₆": 1/6,
      "¹⁄₆": 1/6, "¹⁄₅": .2,
      "¹⁄₈": .125, "¹⁄₁₆": .0625}


def frac(t):
    t = t.strip()
    if re.fullmatch(r'\d+', t):
        return float(t)
    return FR.get(t)


def main():
    A = load_a()
    print("=" * 78)
    print("ATTACK 8a — HT88 / HT94b / HT117a: control or tautology?")
    print("=" * 78)
    for f in ("HT88", "HT94b", "HT117a"):
        ws = A[f]["transliteratedWords"]
        ik = ws.index("KI-RO")
        iu = ws.index("KU-RO")
        ents = []
        j = ik
        while j < iu:
            if is_word(ws[j]) and ws[j] != "KI-RO":
                nx = None
                for q in range(j + 1, iu):
                    if ws[q] in ("\n", DIVIDER, DIVIDER_LINE, LACUNA):
                        continue
                    nx = ws[q]; break
                if to_val(nx) is not None:
                    ents.append((ws[j], to_val(nx)))
            j += 1
        amts = [x[1] for x in ents]
        tot = to_val(ws[iu + 1])
        print(f"  {f:8s} entries {len(ents)}  amounts {[int(a) for a in amts]}  "
              f"KU-RO {tot:g}")
        print(f"           every amount == 1 ? {all(a == 1 for a in amts)}   "
              f"=> KU-RO == entry count is then arithmetically forced")
    print("\n  All three 'controls' are lists in which EVERY entry carries the numeral")
    print("  1. The sum of n ones is n. These cases therefore test only that KU-RO is")
    print("  a total -- which was never in dispute -- and carry ZERO information about")
    print("  what KI-RO means. Calling them 'residual personnel block has exact")
    print("  cardinality' restates 1+1+...+1 = n.")
    print("  They are also not independent of prior scholarship: the external")
    print("  workspace dbourdeau/cyphersolver reproduces exactly HT88:6, HT94b:5,")
    print("  HT117a:10 and labels the result 'replication, not discovery', citing")
    print("  John Younger's commentaries as already identifying these lists.")

    print("\n" + "=" * 78)
    print("ATTACK 8b — HT34: '100 - 70 = 30 = KI-RO', graded 'high' by the claimant")
    print("=" * 78)
    ws = A["HT34"]["transliteratedWords"]
    print("  witness A, HT34 in full:")
    print("   ", " ".join(w.replace("\n", "/") for w in ws))
    i = ws.index("KI-RO")
    print(f"\n  witness A reads KI-RO followed by: {ws[i+1]!r}")
    print("  the claimant's ledger (analysis/kiro_scope_ledger.csv) records")
    print("    HT34,scalar_residual,100,70,30  and '100 - 70 = 30 exactly', grade high")
    print("  100 - 70 = 30, but witness A's number is", ws[i+1])
    print("\n  ADJUDICATED against the source the claimant itself cites")
    print("  (mwenge/lineara.xyz commentary/HT34.html, John Younger's GORILA table):")
    print("    the table reads   KI-RO   30 [[7]]")
    print("    '[[7]]' is GORILA notation for an ERASED sign. The reading is 30 with an")
    print("    erased 7.  Witness A (Douros tabulation) has collapsed the erasure into")
    print("    the figure and prints 37.")
    print("  => this is a WITNESS defect, not claimant error. The claimant's 30 is right.")
    print("  But the control still does not do the work claimed for it, because the")
    print("  SAME commentary supplies the interpretation, conditionally:")
    print("    'If PA3 records an amount (70) to be omitted from *521 100, as if")
    print("     delivered ... then 30 is the result, apparently a deficit (KI-RO)'")
    print("  The 'exact arithmetic relation' is Younger's own hypothesis about what")
    print("  PA3 70 does, restated. Nothing on the tablet states that 70 is to be")
    print("  subtracted from 100; the two lines are adjacent entries among eight.")
    print("  Using it as independent confirmation of the residual model is circular.")

    print("\n" + "=" * 78)
    print("ATTACK 8c — HT123+124a: does the KI-RO make-up ratio hold on all four rows?")
    print("=" * 78)
    ws = A["HT123+124a"]["transliteratedWords"]
    print("  witness A, HT123+124a:")
    print("   ", " ".join(w.replace("\n", "/") for w in ws))
    rows = []
    cur = {}
    for idx, w in enumerate(ws):
        if w in ("OLIV",):
            vals = []
            for q in range(idx + 1, min(idx + 4, len(ws))):
                f = frac(ws[q])
                if f is not None:
                    vals.append(f)
                elif ws[q] != "\n":
                    break
            cur = {"name": ws[idx - 1] if idx else "?", "OLIV": sum(vals)}
        elif w == "*308" and cur:
            vals = []
            for q in range(idx + 1, min(idx + 4, len(ws))):
                f = frac(ws[q])
                if f is not None:
                    vals.append(f)
                elif ws[q] != "\n":
                    break
            cur["308"] = sum(vals) if vals else None
        elif w == "KI-RO" and cur:
            vals = []
            for q in range(idx + 1, min(idx + 4, len(ws))):
                f = frac(ws[q])
                if f is not None:
                    vals.append(f)
                elif ws[q] != "\n":
                    break
            cur["KIRO"] = sum(vals) if vals else None
            rows.append(cur); cur = {}
    print(f"\n  {'row':10s} {'OLIV':>8s} {'*308':>8s} {'KI-RO':>8s} "
          f"{'308+KIRO':>9s} {'OLIV/3':>8s} {'ratio implied':>14s}")
    for r in rows:
        if r.get("308") is None or r.get("KIRO") is None or not r.get("OLIV"):
            print(f"  {r['name']:10s} unreadable under this parse: {r}")
            continue
        s = r["308"] + r["KIRO"]
        print(f"  {r['name']:10s} {r['OLIV']:8.3f} {r['308']:8.3f} {r['KIRO']:8.3f} "
              f"{s:9.3f} {r['OLIV']/3:8.3f} {s/r['OLIV']:14.4f}")
    print("\n  The claimant quotes ONLY the DA-TU row (OLIV 15, *308 4 1/4, KI-RO 3/4,")
    print("  target 15/3 = 5) and grades HT123+124 'high'. The implied ratio")
    print("  (*308 + KI-RO)/OLIV is NOT constant across the rows, so a single")
    print("  conversion ratio with additive KI-RO cannot fit the tablet.")
    print("  The external workspace dbourdeau/cyphersolver derives the same result")
    print("  algebraically from rows 1-2 and finds the bundle forces ratio r = -1,")
    print("  i.e. no positive common ratio exists. Younger's commentary already")
    print("  discusses the underlying discrepancy.")
    print("  => the second of the claimant's two arithmetically checkable KI-RO cases")
    print("     is a row selected from a tablet that as a whole contradicts the model.")

    print("\n" + "=" * 78)
    print("ATTACK 8d — HT15: was the 'held-out semantic HIT' a derivation?")
    print("=" * 78)
    ws = A["HT15"]["transliteratedWords"]
    print("  witness A, HT15:", " ".join(w.replace("\n", "/") for w in ws))
    print("  684 + 570 =", 684 + 570, " <- this arithmetic is real and independent")
    print("  KI-RO 400: 1254 - 400 =", 1254 - 400, "(not on the tablet);")
    print("             1254 + 400 =", 1254 + 400, "(not on the tablet)")
    print("  The number 400 is not derivable from anything on HT15. The claimant's")
    print("  'HIT' consists of the cited commentary calling 400 a deficit. That is the")
    print("  received gloss the note elsewhere disclaims discovering, used as its own")
    print("  held-out confirmation. It is not a held-out test.")

    print("\n" + "=" * 78)
    print("SCORECARD: the claimant's 'arithmetic/cardinality controls: 6/6 pass'")
    print("=" * 78)
    for a, b in [
        ("HT88  cardinality", "tautology: n ones sum to n; tests KU-RO, not KI-RO"),
        ("HT94b cardinality", "tautology, same"),
        ("HT117a cardinality", "tautology, same; also the block it closes is NOT the"
                               " whole tablet (see ATTACK 5a)"),
        ("HT34  100-70=30", "restates Younger's conditional interpretation; the"
                            " subtraction is not stated by the tablet"),
        ("HT123+124 DA-TU row", "1 of 4 rows; the 4-row system admits no positive"
                                " common ratio"),
        ("HT15  held-out", "confirmation is the commentary's gloss, not a derivation"),
    ]:
        print(f"  {a:22s} -> {b}")
    print("\n  Surviving independent arithmetic support for KI-RO = residual: NONE.")
    print("  Surviving independent arithmetic support for KU-RO = total: 8 exact")
    print("  balancing blocks corpus-wide (ATTACK 1d), which is prior scholarship.")


if __name__ == "__main__":
    main()
