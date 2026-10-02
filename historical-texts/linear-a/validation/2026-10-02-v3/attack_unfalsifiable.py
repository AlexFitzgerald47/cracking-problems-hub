#!/usr/bin/env python3
"""
ATTACK 6 — is the obligation circuit falsifiable, and is its polarity decidable?

  6a  A-DU's distribution.  The circuit model needs A-DU to be a state with a
      magnitude (RENDERED, or ASSESSED).  Does A-DU ever carry a quantity?
  6b  is ASSESSED = RENDERED + OUTSTANDING ever instantiated anywhere?
  6c  the internal polarity contradiction between the claimant's own two notes.
  6d  the '9/9 construction grammar' -- can it fail?

ATTACK 7 — coverage against the pre-registered criterion.
"""
import collections, re
from corpus import (load_a, all_faces_with_words, ht_tablet_faces, is_word, to_val,
                    is_num, DIVIDER, DIVIDER_LINE, LACUNA, TOTALS, base)

OPS = ["KU-RO", "PO-TO-KU-RO", "KI-RO", "A-DU", "KU-DA", "KA-PA", "SA-RA₂",
       "MA-KA-RI-TE", "U-MI-NA-SI", "KI-KI-RA-JA", "DA-DU-MA-TA", "SA-TA",
       "A-KA-RU", "KA-RU", "*21F-TU-NE"]


def nextnon(ws, i):
    for j in range(i + 1, len(ws)):
        if ws[j] in ("\n", LACUNA):
            continue
        return ws[j]
    return None


def main():
    A = load_a()
    allf = all_faces_with_words(A)

    print("=" * 78)
    print("ATTACK 6a — does A-DU ever carry a quantity?")
    print("=" * 78)
    prof = collections.defaultdict(lambda: collections.Counter())
    for k, v in allf.items():
        ws = v["transliteratedWords"]
        for i, w in enumerate(ws):
            if not is_word(w):
                continue
            nx = nextnon(ws, i)
            if nx is None:
                prof[w]["end"] += 1
            elif to_val(nx) is not None:
                prof[w]["numeral"] += 1
            elif is_num(nx):
                prof[w]["fraction"] += 1
            elif nx in (DIVIDER, DIVIDER_LINE):
                prof[w]["divider"] += 1
            else:
                prof[w]["word/ideogram"] += 1
    print(f"  {'term':16s} {'num':>5s} {'frac':>5s} {'div':>5s} {'word':>5s} {'end':>5s}")
    for w in OPS:
        if w in prof:
            c = prof[w]
            print(f"  {w:16s} {c['numeral']:5d} {c['fraction']:5d} {c['divider']:5d} "
                  f"{c['word/ideogram']:5d} {c['end']:5d}")
    print("\n  A-DU takes a numeral in", prof["A-DU"]["numeral"], "of",
          sum(prof["A-DU"].values()), "attestations.")
    print("  => A-DU never carries a magnitude. It is a heading, like DA-DU-MA-TA,")
    print("     MA-KA-RI-TE, U-MI-NA-SI and KI-KI-RA-JA (all 0 numerals).")
    print("     CONSEQUENCE: whether A-DU means ASSESSED or RENDERED cannot be")
    print("     decided by any arithmetic the corpus contains, because no number is")
    print("     ever attached to it. The polarity of the obligation circuit is not")
    print("     merely 'unresolved' -- it is undecidable from this evidence. A model")
    print("     whose central arrow cannot be oriented by any possible observation in")
    print("     the corpus is not a reading of the corpus.")

    print("\n" + "=" * 78)
    print("ATTACK 6b — is ASSESSED = RENDERED + OUTSTANDING ever instantiated?")
    print("=" * 78)
    both = [k for k, v in allf.items()
            if "A-DU" in v["transliteratedWords"] and "KI-RO" in v["transliteratedWords"]]
    bothT = sorted({base(k) for k in both})
    adu = sorted({base(k) for k, v in allf.items() if "A-DU" in v["transliteratedWords"]})
    kiro = sorted({base(k) for k, v in allf.items() if "KI-RO" in v["transliteratedWords"]})
    print(f"  tablets with A-DU : {len(adu)} -> {adu}")
    print(f"  tablets with KI-RO: {len(kiro)} -> {kiro}")
    print(f"  tablets with BOTH on the same FACE : {both}")
    inter = sorted(set(adu) & set(kiro))
    print(f"  tablets with BOTH anywhere         : {inter}")
    print(f"  tablets with DA-DU-MA-TA           : "
          f"{sorted({base(k) for k,v in allf.items() if 'DA-DU-MA-TA' in v['transliteratedWords']})}")
    print("  tablets carrying ALL THREE states (DA-DU-MA-TA, A-DU, KI-RO):",
          sorted({base(k) for k, v in allf.items()
                  if 'DA-DU-MA-TA' in v["transliteratedWords"]}
                 & set(adu) & set(kiro)) or "NONE")
    print("\n  => the three-state lifecycle ASSESS -> RENDER -> OUTSTANDING is never")
    print("     attested together on any tablet in the corpus. It is assembled from")
    print("     HT95 (two faces, no KI-RO) plus HT88 (A-DU and KI-RO, no arithmetic")
    print("     link). The claimant's own note concedes this: 'HT95 does not itself")
    print("     contain KI-RO, so this bridge is an inference across the")
    print("     administrative system, not a direct three-way inscription.'")
    if "HT88" in [base(x) for x in both]:
        ws = A["HT88"]["transliteratedWords"]
        print("\n  HT88, the 'clean conceptual bridge', in full:")
        print("   ", " ".join(w.replace("\n", "/") for w in ws))
        print("    A-DU block quantities: VIR+KA 20, RE-ZA 6, KI-KI-NA 7  -> sum 33")
        print("    KI-RO block: six names at 1 each -> KU-RO 6")
        print("    33 and 6 stand in no stated relation. 33 - 6 = 27; 33 + 6 = 39;")
        print("    neither appears on the tablet. The 'both sides of the state system")
        print("    on one small tablet' claim is two unrelated blocks on one tablet.")

    print("\n" + "=" * 78)
    print("ATTACK 6c — the claimant's own two notes assign A-DU opposite polarities")
    print("=" * 78)
    print("  2026-09-07-obligation-circuit-post-award.md, Leap 2 and")
    print("  analysis/administrative_state_machine.csv:")
    print("      A-DU = 'rendered / contributed / delivered / fulfilled'  (medium-high)")
    print("  2026-09-08-scribe9-dossier-functional-reconstruction.md, New result 4:")
    print("      A-DU = 'ASSESSED / ACTIVATED OBLIGATION / ON-BOOK LIABILITY'")
    print("  These are the two ENDS of the state machine, not two shades of one gloss.")
    print("  The claimant's own frozen falsifier #3 is:")
    print("      'A-DU requiring incompatible meanings across labor and assessment")
    print("       records.'")
    print("  HT85a is headed A-DU and is read in one note as 'RENDERED / LEVIED")
    print("  PERSONNEL' and in the other as the 'assessed liability' source side.")
    print("  The falsifier is therefore already met inside the Hub's own files.")

    print("\n" + "=" * 78)
    print("ATTACK 6d — can the '9/9 construction grammar' fail?")
    print("=" * 78)
    print("  The rule classifies a KI-RO occurrence BY the token that follows it:")
    print("    numeral after KI-RO -> 'scalar residual';  divider after KI-RO ->")
    print("    'forward-scoping block'.  The classification and the prediction are")
    print("    the same observation, so no occurrence can contradict it.")
    nkiro = sum(1 for v in allf.values() for w in v["transliteratedWords"] if w == "KI-RO")
    print(f"  KI-RO tokens in the corpus: {nkiro}")
    perfect = [w for w, c in prof.items()
               if sum(c.values()) >= 4 and (c['numeral'] + c['divider']) == sum(c.values())]
    n4 = [w for w, c in prof.items() if sum(c.values()) >= 4]
    print(f"  word types with >=4 attestations: {len(n4)}")
    print(f"  ... of which EVERY attestation is followed by either a numeral or a")
    print(f"      divider, i.e. would also score 'n/n, 0 contradictions': "
          f"{len(perfect)}")
    print(f"      {sorted(perfect)}")
    both2 = [w for w in n4 if prof[w]['numeral'] and prof[w]['divider']]
    print(f"  ... and showing BOTH constructions (a 'two-construction grammar'): "
          f"{len(both2)}")
    print(f"      {sorted(both2)}")
    print("  => 'two constructions predicted by the next token' is a property of a")
    print("     large class of HT words, including pure commodity classifiers. It is")
    print("     not a discovery about KI-RO. The only non-vacuous part is whether the")
    print("     two constructions share one semantics, and that rests on exactly two")
    print("     arithmetically checkable cases (HT34, HT123+124).")

    print("\n" + "=" * 78)
    print("ATTACK 7 — coverage against the pre-registered criterion")
    print("=" * 78)
    ntot = len(A)
    nwords = len(allf)
    types = collections.Counter()
    toks = 0
    for k, v in allf.items():
        for w in v["transliteratedWords"]:
            if is_word(w):
                types[w] += 1; toks += 1
    s9faces = sorted(k for k, v in A.items() if v.get("scribe") == "HT Scribe 9")
    s9tok = sum(1 for k in s9faces for w in A[k]["transliteratedWords"] if is_word(w))
    s9types = {w for k in s9faces for w in A[k]["transliteratedWords"] if is_word(w)}
    htf = ht_tablet_faces(A)
    httok = sum(1 for v in htf.values() for w in v["transliteratedWords"] if is_word(w))
    print(f"  corpus records (witness A)                     : {ntot}")
    print(f"  records carrying >=1 syllabic sign-group       : {nwords}")
    print(f"  distinct sign-group types corpus-wide          : {len(types)}")
    print(f"  sign-group tokens corpus-wide                  : {toks}")
    print(f"  Haghia Triada tablet faces                     : {len(htf)}  "
          f"({httok} tokens = {100*httok/toks:.1f}% of corpus tokens)")
    print(f"  Scribe-9 faces                                 : {len(s9faces)} "
          f"(= {len(set(base(k) for k in s9faces))} tablets)")
    print(f"  Scribe-9 sign-group tokens                     : {s9tok} "
          f"= {100*s9tok/toks:.2f}% of corpus tokens")
    print(f"  Scribe-9 distinct sign-group types             : {len(s9types)} "
          f"= {100*len(s9types)/len(types):.2f}% of corpus types")
    glossed = [w for w in OPS if w in types and w != "*21F-TU-NE"]
    gtok = sum(types[w] for w in glossed)
    print(f"\n  sign-groups the claim assigns a function to    : {len(glossed)} "
          f"-> {glossed}")
    print(f"  their token coverage                           : {gtok} "
          f"= {100*gtok/toks:.2f}% of corpus sign-group tokens")
    print(f"  type coverage                                  : "
          f"{100*len(glossed)/len(types):.2f}% of the {len(types)} distinct types")
    print("\n  phonetic/lexical values recovered by the claim  : 0 (explicitly disclaimed)")
    print("  language family identified                     : none (explicitly disclaimed)")
    print("  readings of running text                       : none; the readings are")
    print("    database field labels over lists of numerals.")


if __name__ == "__main__":
    main()
