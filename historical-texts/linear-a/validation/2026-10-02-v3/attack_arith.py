#!/usr/bin/env python3
"""
ATTACK 1 — damage-aware arithmetic audit.

The obligation-circuit reading depends on totals balancing. The 2026-09-25 session
reported several KU-RO "MISMATCHES" using a block rule of "every numeral since the
previous total marker on this face". That rule is wrong for the claimant's own
grammar: KI-RO opens a forward block, so a KU-RO after KI-RO closes the KI-RO block
only. This attack re-runs the audit under the CLAIMANT'S OWN segmentation rule
(the most favourable one available to them) and then asks:

  1. corpus-wide, how often does KU-RO actually balance?
  2. of the failures, how many sit on faces with a lacuna marker (damage) and how
     many on clean faces?
  3. what survives for the specific tablets the dossier quotes?
"""
import collections, sys
from corpus import (load_a, ht_tablet_faces, all_faces_with_words, is_word, to_val,
                    is_num, DIVIDER, DIVIDER_LINE, LACUNA, TOTALS, damaged, n_lacunae, base)


def blocks_claimant_rule(ws):
    """Yield (block_numerals, stated_total, marker, reset_reason).

    Block starts after the previous total marker, OR after a `KI-RO <divider>`
    (the claimant's forward-scope construction), whichever came later.
    """
    acc, out, reason = [], [], "face-start"
    i = 0
    while i < len(ws):
        w = ws[i]
        if w in TOTALS:
            nxt = None
            for j in range(i + 1, min(i + 3, len(ws))):
                if to_val(ws[j]) is not None:
                    nxt = to_val(ws[j]); break
                if ws[j] not in (DIVIDER, DIVIDER_LINE, "\n", LACUNA):
                    break
            out.append((list(acc), nxt, w, reason))
            acc = []; reason = "after-" + w
        elif w == "KI-RO":
            # does a divider (possibly over a newline) follow?
            fwd = None
            for j in range(i + 1, min(i + 4, len(ws))):
                if ws[j] in (DIVIDER, DIVIDER_LINE):
                    fwd = True; break
                if ws[j] == "\n":
                    continue
                break
            if fwd:
                acc = []; reason = "after-KI-RO-forward-scope"
        elif to_val(w) is not None:
            acc.append(to_val(w))
        i += 1
    return out


def audit(A, faces, label):
    rows = []
    for k, v in sorted(faces.items()):
        ws = v["transliteratedWords"]
        for ents, tot, mark, why in blocks_claimant_rule(ws):
            if tot is None or not ents:
                continue
            s = sum(ents)
            rows.append(dict(face=k, marker=mark, n=len(ents), sum=s, stated=tot,
                             ok=abs(s - tot) < 1e-9, dmg=damaged(v),
                             lac=n_lacunae(v), why=why,
                             frac=any(is_num(w) and to_val(w) is None
                                      for w in ws)))
    nt = len(rows); nok = sum(r["ok"] for r in rows)
    clean = [r for r in rows if not r["dmg"] and not r["frac"]]
    cok = sum(r["ok"] for r in clean)
    print(f"\n--- {label}: {nt} total-markers with a stated integer and >=1 preceding numeral")
    print(f"    exact balance overall          : {nok}/{nt} = {100*nok/max(nt,1):.1f}%")
    print(f"    faces with NO lacuna & NO fraction: {len(clean)}; exact balance "
          f"{cok}/{len(clean)} = {100*cok/max(len(clean),1):.1f}%")
    dmg = [r for r in rows if r["dmg"] or r["frac"]]
    dok = sum(r["ok"] for r in dmg)
    print(f"    faces WITH lacuna or fraction     : {len(dmg)}; exact balance "
          f"{dok}/{len(dmg)} = {100*dok/max(len(dmg),1):.1f}%")
    return rows


def main():
    A = load_a()
    print("=" * 78)
    print("ATTACK 1 — damage-aware arithmetic audit of KU-RO / PO-TO-KU-RO")
    print("=" * 78)

    allf = all_faces_with_words(A)
    rows_all = audit(A, allf, "WHOLE CORPUS (all sites, all supports)")
    htf = ht_tablet_faces(A)
    rows_ht = audit(A, htf, "HAGHIA TRIADA TABLETS")

    print("\n--- the ten faces the dossier quotes, under the claimant's own rule")
    quoted = ["HT85a", "HT85b", "HT87", "HT88", "HT94a", "HT94b", "HT117a", "HT117b",
              "HT119", "HT122a", "HT122b", "HT34", "HT15", "HT1", "HT2", "HT30", "HT37"]
    for t in quoted:
        if t not in A:
            print(f"  {t:8s} ABSENT from witness A"); continue
        v = A[t]; ws = v["transliteratedWords"]
        got = False
        for ents, tot, mark, why in blocks_claimant_rule(ws):
            if tot is None:
                continue
            got = True
            s = sum(ents)
            flag = "BALANCES" if abs(s - tot) < 1e-9 else f"SHORT/OVER by {s-tot:+g}"
            print(f"  {t:8s} {mark:11s} block={why:28s} n={len(ents):2d} "
                  f"sum={s:7g} stated={tot:7g}  {flag}"
                  f"   lacunae_on_face={n_lacunae(v)}")
        if not got:
            print(f"  {t:8s} no total marker with a stated integer "
                  f"(lacunae_on_face={n_lacunae(v)})")

    print("\n--- HT122: what actually supports the 'hierarchical control total'?")
    for f in ("HT122a", "HT122b"):
        v = A[f]
        print(f"  {f}: lacuna markers in raw transcription = {n_lacunae(v)}")
        print(f"        raw words with damage flags = "
              + " ".join(("[DMG]" if LACUNA in w else "") + w.replace("\n", "/")
                         for w in v["transliteratedWords"]))
    print("  stated-total identity 31 + KU-DA 1 + 65 = 97 :",
          31 + 1 + 65 == 97)
    print("  BUT the entry lines of neither face reach their own stated subtotal;")
    print("  the identity is arithmetic over three numbers the scribe wrote, not a")
    print("  reconciliation of the itemised detail.")

    # null for the stated-total identity: how often do a face's stated totals
    # satisfy subtotal+subtotal(+1 small item) = grand total by chance?
    print("\n--- null for 'a + b (+ small item) = grand total' over stated totals")
    tots = []
    for k, v in allf.items():
        ws = v["transliteratedWords"]
        vals = [to_val(ws[i + 1]) for i, w in enumerate(ws)
                if w in TOTALS and i + 1 < len(ws) and to_val(ws[i + 1]) is not None]
        if len(vals) >= 2:
            tots.append((k, vals))
    print(f"  faces carrying >=2 stated totals: {len(tots)}")
    hit = [k for k, vals in tots
           if any(abs(sum(vals[:-1]) + d - vals[-1]) < 1e-9 for d in (0, 1))]
    print(f"  of those, subtotals(+0 or +1) == last total: {len(hit)} -> {hit}")


if __name__ == "__main__":
    main()
