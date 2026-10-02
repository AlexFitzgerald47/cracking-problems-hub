#!/usr/bin/env python3
"""
ATTACK 5 — does the dossier's OWN KI-RO grammar permit the readings it makes?

The claimant's frozen grammar (analysis/2026-09-07-kiro-unified-residual-grammar.md,
analysis/kiro_construction_grammar.csv) is:

    Construction B:  KI-RO <divider>  [line items] ... [KU-RO N]
    "KI-RO opens/scopes a category of line-items; KU-RO closes/sums that category."

ATTACK 5a applies that rule to HT117 and asks what is actually inside KI-RO's scope.
ATTACK 5b checks HT85's two faces against each other arithmetically.
ATTACK 5c reconciles the HT85b entry count between the two witnesses.
"""
import re, html, collections
from corpus import (load_a, load_b, is_word, to_val, DIVIDER, DIVIDER_LINE, LACUNA,
                    TOTALS, SIGLA_DOCS)

RULING = "—"


def show(ws):
    out = []
    for w in ws:
        out.append({"\n": "/", RULING: " ===RULING=== ", DIVIDER: "·"}.get(w, w))
    return " ".join(out)


def main():
    A = load_a(); B = load_b()
    print("=" * 78)
    print("ATTACK 5a — HT117: what is inside KI-RO's scope under the claimant's own rule?")
    print("=" * 78)
    for f in ("HT117a", "HT117b"):
        print(f"  {f}: {show(A[f]['transliteratedWords'])}")
    ws = A["HT117a"]["transliteratedWords"]
    i_kiro = ws.index("KI-RO")
    i_kuro = ws.index("KU-RO")
    i_rule = ws.index(RULING) if RULING in ws else None
    i_sata = ws.index("SA-TA")
    print(f"\n  token index of KI-RO   : {i_kiro}")
    print(f"  token index of KU-RO 10: {i_kuro}  (closes the KI-RO block per the rule)")
    print(f"  token index of RULING  : {i_rule}  (a physical section line on the tablet)")
    print(f"  token index of SA-TA   : {i_sata}")
    inside = [w for w in ws[i_kiro + 1:i_kuro] if is_word(w)]
    print(f"\n  entries inside the KI-RO block (KI-RO ... KU-RO 10): "
          f"{len(inside)-1} personnel + the subheading U-MI-NA-SI")
    print(f"    {inside}")
    after = [w for w in ws[i_kuro + 2:] if is_word(w)]
    print(f"\n  everything AFTER the closing KU-RO 10, i.e. OUTSIDE KI-RO's scope:")
    print(f"    on face a (after a ruling): {after}")
    print(f"    on face b                 : "
          f"{[w for w in A['HT117b']['transliteratedWords'] if is_word(w)]}")
    print(f"\n  DI-KI-SE is on face {'HT117b' if 'DI-KI-SE' in A['HT117b']['transliteratedWords'] else '?'}"
          f", i.e. after the closing KU-RO 10 AND after a ruling AND on the other face.")
    print("  The SA-TA block on face a carries NO closing KU-RO at all:")
    NL = chr(10)
    tail = [w for w in ws[i_sata:] if w != NL]
    print("    tokens after SA-TA on face a: " + repr(tail))
    print("\n  CONSEQUENCE. Under the claimant's own frozen Construction B, KU-RO 10")
    print("  closes the KI-RO block. Therefore:")
    print("    * HT117 is NOT 'a large KI-RO exception roster grouped by units';")
    print("      only its first 10-name block is in KI-RO scope.")
    print("    * U-MI-NA-SI, SA-TA and *21F-TU-NE are NOT three parallel subheadings")
    print("      inside one KI-RO block: the first is inside, the other two are after")
    print("      it. The 'GROUP BY accountable unit' reading needs all three inside.")
    print("    * DI-KI-SE does NOT carry KI-RO. The 'status-switch' between HT87 and")
    print("      HT117 therefore has nothing switched: in HT87 DI-KI-SE stands under")
    print("      *21F-TU-NE · MA-KA-RI-TE, and in HT117b under *21F-TU-NE · -- the SAME")
    print("      unit heading, with no KI-RO in either case.")
    print("  This is the dossier's self-described strongest result, and it is")
    print("  contradicted by the dossier's own grammar applied to the raw corpus.")

    print("\n  (transcription note) the claimant writes QI-TU-NE; witness A reads")
    print("  *21F-TU-NE (an undeciphered sign variant) and witness B reads qif-tu-ne.")
    print("  Both witnesses agree the SAME sign-group heads HT87 and HT117b, so the")
    print("  pairing itself is not a transcription artefact -- only the name is.")

    print("\n" + "=" * 78)
    print("ATTACK 5b — HT85: do the two faces balance?")
    print("=" * 78)
    a = A["HT85a"]["transliteratedWords"]; b = A["HT85b"]["transliteratedWords"]
    print(f"  HT85a: {show(a)}")
    print(f"  HT85b: {show(b)}")
    av = [to_val(w) for w in a if to_val(w) is not None]
    bv = [to_val(w) for w in b if to_val(w) is not None]
    print(f"\n  face a entry amounts {[int(x) for x in av[:-1]]} -> sum "
          f"{sum(av[:-1]):g}; stated KU-RO {av[-1]:g}  BALANCES")
    print(f"  face b entry amounts {[int(x) for x in bv]} -> sum {sum(bv):g}; "
          f"NO stated total on face b")
    print(f"\n  So the tablet states 66 on one face and {sum(bv):g} units on the other.")
    print("  The dossier reads 'eleven standardized six-person work gangs'. That")
    print("  requires the unattested equation  1 (the numeral on every face-b line)")
    print("  = 6 persons.  Nothing on HT85 states it, and no other tablet in the")
    print("  corpus supplies it.  The straightforward reading of face b is eleven")
    print("  entries of one unit each, total eleven.")
    print("  The two faces do NOT balance under any reading the tablet supplies:")
    print(f"    66 vs {sum(bv):g}; the ratio 6 is supplied by the interpreter.")

    print("\n  double-counting check on the dossier's own rendering table")
    print("  (2026-09-07-haghia-triada-labor-control-functional-solve.md §2):")
    print("    that table lists EIGHT receiving rows (KI-RE-TA2, QE-KA, TE-TU, ME-ZA,")
    print("    RE-DI-SE, WA-DU-NI-MI, MA-DI, QA-*310-I) and assigns them")
    print("    1,2,3,1,1,1,1,1 = 11 gangs, having absorbed PA into QE-KA and KA,DI")
    print("    into TE-TU.  But the 66 = 11 x 6 argument needs ELEVEN entries.")
    print("    The number 11 is therefore used twice with two incompatible")
    print("    referents: eleven face-b entries, and eleven gangs over eight entries.")

    print("\n" + "=" * 78)
    print("ATTACK 5c — HT85b entry count: witness A vs witness B")
    print("=" * 78)
    wa = [w for w in b if is_word(w)]
    print(f"  witness A (GORILA via Douros): {len(wa)} sign-groups -> {wa}")
    wb = B.get("HT 85b", [])
    print(f"  witness B (SigLA)            : {len(wb)} sequences   -> {wb}")

    def norm(s):
        s = s.lower().replace("₂", "2").replace("₃", "3")
        s = s.replace("*", "a").replace("[?]", "").replace("[", "").replace("]", "")
        s = s.replace("?", "").rstrip("-")
        return s
    na = [norm(x) for x in wa]; nb = [norm(x) for x in wb]
    onlyA = [x for x in na if x not in nb]
    onlyB = [x for x in nb if x not in na]
    print(f"  after normalising * / subscripts / trailing hyphens:")
    print(f"    present only in witness A: {onlyA}")
    print(f"    present only in witness B: {onlyB}")
    print(f"\n  => the entire divergence is the three SINGLE-SIGN tokens "
          f"{[x for x in onlyA]}.")
    print("     Witness A treats PA, KA and DI as independent numbered entries;")
    print("     witness B does not segment them as separate words at all.")
    print(f"     entry count excluding the header: witness A {len(wa)-1}, "
          f"witness B {len(wb)-1}")
    print("     The '11 entries' on which 66 = 11 x 6 depends EXISTS IN ONE WITNESS")
    print("     ONLY.  Under SigLA's segmentation HT85b has 8 entries and 66/8 is")
    print("     not an integer, so the gang reading does not arise at all.")


if __name__ == "__main__":
    main()
