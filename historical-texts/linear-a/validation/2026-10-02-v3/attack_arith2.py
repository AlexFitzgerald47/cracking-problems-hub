#!/usr/bin/env python3
"""
ATTACK 1b — fraction-aware honest KU-RO audit + per-tablet hierarchy null.

Fixes two unfairnesses in 1a:
  * strict-integer summation guaranteed failure on commodity blocks carrying
    fraction signs, so the 32% figure understated KU-RO. Here blocks containing
    any fraction/measure token are reported SEPARATELY rather than scored as fails.
  * the HT122 hierarchy spans two faces, so the null must be per TABLET.
"""
import re, collections, itertools, random
from corpus import (load_a, ht_tablet_faces, all_faces_with_words, is_word, to_val,
                    is_num, DIVIDER, DIVIDER_LINE, LACUNA, TOTALS, damaged,
                    n_lacunae, base)
from attack_arith import blocks_claimant_rule

FRAC = re.compile(r'[¹²³⁴-⁹⁰⁄₀-₉≈/]')
MEASURE = re.compile(r'(double|mina)')


def block_is_integer_clean(ws, lo, hi):
    """True iff every numeric token in the block is a plain integer and no measure
    word appears.  NB: subscripts inside sign-group NAMES (PA3 -> PA\u2083) must not
    count as fractions -- that was a bug in the first draft of this file."""
    seg = ws[lo:hi]
    for w in seg:
        if MEASURE.search(w):
            return False
        if is_num(w) and to_val(w) is None:
            return False
    return True


def blocks_with_span(ws):
    """Same as blocks_claimant_rule but also returns the token span of the block."""
    acc, out, reason, start = [], [], "face-start", 0
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
            out.append((list(acc), nxt, w, reason, start, i))
            acc = []; reason = "after-" + w; start = i + 1
        elif w == "KI-RO":
            fwd = None
            for j in range(i + 1, min(i + 4, len(ws))):
                if ws[j] in (DIVIDER, DIVIDER_LINE):
                    fwd = True; break
                if ws[j] == "\n":
                    continue
                break
            if fwd:
                acc = []; reason = "after-KI-RO-forward-scope"; start = i + 1
        elif to_val(w) is not None:
            acc.append(to_val(w))
        i += 1
    return out


def main():
    A = load_a()
    allf = all_faces_with_words(A)

    print("=" * 78)
    print("ATTACK 1b — how strong is the KU-RO arithmetic anchor, honestly counted?")
    print("=" * 78)
    nkuro = sum(1 for v in allf.values() for w in v["transliteratedWords"] if w in TOTALS)
    print(f"  total-marker tokens (KU-RO / PO-TO-KU-RO) in the corpus: {nkuro}")

    cat = collections.Counter()
    clean_rows, dirty_rows = [], []
    for k, v in sorted(allf.items()):
        ws = v["transliteratedWords"]
        for ents, tot, mark, why, lo, hi in blocks_with_span(ws):
            if tot is None:
                cat["no stated integer after the marker"] += 1; continue
            if not ents:
                cat["no preceding numeral in the block"] += 1; continue
            intclean = block_is_integer_clean(ws, lo, hi)
            row = dict(face=k, mark=mark, n=len(ents), sum=sum(ents), stated=tot,
                       ok=abs(sum(ents) - tot) < 1e-9, lac=n_lacunae(v), why=why)
            if intclean:
                clean_rows.append(row); cat["integer-only block, testable"] += 1
            else:
                dirty_rows.append(row); cat["block carries fractions/measures"] += 1
    for kk, vv in cat.most_common():
        print(f"    {kk:42s} {vv}")

    def report(rows, lab):
        n = len(rows); ok = sum(r["ok"] for r in rows)
        nd = [r for r in rows if r["lac"] == 0]
        okd = sum(r["ok"] for r in nd)
        print(f"\n  {lab}")
        print(f"    exact balance                     : {ok}/{n} = {100*ok/max(n,1):.1f}%")
        print(f"    restricted to faces with 0 lacunae: {okd}/{len(nd)} = "
              f"{100*okd/max(len(nd),1):.1f}%")
        bad = sorted([r for r in rows if not r["ok"]], key=lambda r: -abs(r["sum"]-r["stated"]))
        print(f"    failures, worst first:")
        for r in bad:
            print(f"      {r['face']:8s} {r['mark']:11s} n={r['n']:2d} sum={r['sum']:7g} "
                  f"stated={r['stated']:7g} delta={r['sum']-r['stated']:+8g} "
                  f"lacunae={r['lac']}")
        return ok, n, okd, len(nd)

    report(clean_rows, "INTEGER-ONLY BLOCKS (the fair test of 'KU-RO = total')")
    report(dirty_rows, "BLOCKS WITH FRACTIONS/MEASURES (not a fair integer test)")

    # ------------------------------------------------ per-tablet hierarchy null
    print("\n" + "=" * 78)
    print("ATTACK 1c — is '31 + KU-DA 1 + 65 = PO-TO-KU-RO 97' more than one lucky sum?")
    print("=" * 78)
    pertab = collections.defaultdict(list)
    for k, v in sorted(allf.items()):
        ws = v["transliteratedWords"]
        for i, w in enumerate(ws):
            if w in TOTALS:
                for j in range(i + 1, min(i + 3, len(ws))):
                    if to_val(ws[j]) is not None:
                        pertab[base(k)].append((k, w, to_val(ws[j]))); break
                    if ws[j] not in (DIVIDER, DIVIDER_LINE, "\n", LACUNA):
                        break
    multi = {t: r for t, r in pertab.items() if len(r) >= 3}
    print(f"  tablets with >=3 stated totals across their faces: {len(multi)}")
    for t, r in sorted(multi.items()):
        vals = [x[2] for x in r]
        gt = [x for x in r if x[1] == "PO-TO-KU-RO"]
        print(f"    {t:8s} {[(x[0], x[1], x[2]) for x in r]}")
    print("\n  tablets carrying a PO-TO-KU-RO at all:")
    pt = sorted({base(k) for k, v in allf.items()
                 if "PO-TO-KU-RO" in v["transliteratedWords"]})
    print("   ", pt)
    for t in pt:
        subs = [x for x in pertab[t] if x[1] == "KU-RO"]
        gts = [x for x in pertab[t] if x[1] == "PO-TO-KU-RO"]
        if not gts:
            print(f"    {t}: PO-TO-KU-RO present but no stated integer after it"); continue
        g = gts[-1][2]; s = sum(x[2] for x in subs)
        # any single extra stated non-total item needed to close the gap?
        gap = g - s
        print(f"    {t}: subtotals {[x[2] for x in subs]} sum={s}  grand={g}  gap={gap:+g}"
              f"   {'CLOSES with one unit item' if gap == 1 else ('EXACT' if gap==0 else 'does NOT close')}")
    print("\n  => the hierarchy claim rests on ONE tablet (HT122). n=1 is not a")
    print("     tested structure; it is a single arithmetic coincidence candidate.")
    print("     P(three stated integers a,b,c with a+1+b=c) is not estimable from n=1.")


if __name__ == "__main__":
    main()
