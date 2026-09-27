#!/usr/bin/env python3
"""Run the frozen held-out tests T1, T3, T4 and T6 on the scan-verified poem.

Rules, key typings, grammar and null come from freeze_rules.py (frozen before any held-out
data was opened). Data come from poem_scan_verified.py. Nothing here tunes a value.

    python3 heldout_test.py            # primary + all declared variants
"""
import itertools
import statistics
from collections import Counter

import freeze_rules as F
import poem_scan_verified as P

LINES = range(1, 21)


def glyph_seq(line_no, conv, xd, tcurl, punct_break=False):
    """Glyphs of a line as component lists; punctuation either skipped or kept as a break."""
    out = []
    for _i, code, comps in P.resolved(line_no, conv, xd, tcurl):
        if comps is None:
            if punct_break:
                out.append(None)
            continue
        out.append(comps)
    return out


def pairs(line_no, conv, xd, tcurl, punct_break=False):
    """Adjacent (a, b, where) pairs, both key signs, within a line; '?' positions break chains."""
    res = []
    gs = glyph_seq(line_no, conv, xd, tcurl, punct_break)
    prev_last = None
    for g in gs:
        if g is None:
            prev_last = None
            continue
        # within-glyph
        for a, b in zip(g, g[1:]):
            if F.is_key(a) and F.is_key(b):
                res.append((a, b, "within"))
        # across the whitespace boundary
        first = g[0]
        if prev_last is not None and F.is_key(prev_last) and F.is_key(first):
            res.append((prev_last, first, "across"))
        prev_last = g[-1] if not g[-1].startswith("?") else None
        if first.startswith("?"):
            pass
    return res


def line_final(line_no, conv, xd, tcurl):
    gs = glyph_seq(line_no, conv, xd, tcurl)
    return gs[-1][-1] if gs else None


def n_predecessors(line_no, conv, xd, tcurl, punct_break=False):
    """(predecessor component or 'LINE_START'/'NONKEY'/'AMBIG') for every glyph beginning with N."""
    out = []
    gs = glyph_seq(line_no, conv, xd, tcurl, punct_break)
    prev = "LINE_START"
    for g in gs:
        if g is None:
            prev = "BREAK"
            continue
        if g[0] == "N":
            out.append(prev)
        last = g[-1]
        prev = last if F.is_key(last) else ("AMBIG" if last.startswith("?") else "NONKEY")
    return out


def violations(pair_list, typing, greek=False):
    key = {s: (F.KEY_S1[s][0], typing[s]) for s in F.KEY_SIGNS}
    if greek:  # the lenient grammar needs the letter values that go with each sign
        key = {s: (F.KEY_S1[s][0], typing[s]) for s in F.KEY_SIGNS}
    c = Counter(F.pair_class(a, b, key, greek) for a, b, _ in pair_list)
    return c["violation"], c["hiatus"], c["canonical"]


def typing_of(key):
    return {s: key[s][1] for s in F.KEY_SIGNS}


def run(conv="S1", xd="V2_eye", tcurl=True, punct_break=False, greek=False, verbose=True):
    key = F.KEYS[conv]
    pl = [p for l in LINES for p in pairs(l, conv, xd, tcurl, punct_break)]
    tk = typing_of(key)
    kv = {s: (key[s][0], tk[s]) for s in F.KEY_SIGNS}
    cls = Counter(F.pair_class(a, b, kv, greek) for a, b, _ in pl)
    v_key = cls["violation"]
    null = []
    for t in F.all_typings(key):
        kvt = {s: (key[s][0], t[s]) for s in F.KEY_SIGNS}
        null.append(sum(F.pair_class(a, b, kvt, greek) == "violation" for a, b, _ in pl))
    p = sum(v <= v_key for v in null) / len(null)
    srt = sorted(null)
    q05, med = srt[int(0.05 * len(srt))], statistics.median(srt)
    out = dict(conv=conv, xd=xd, tcurl=tcurl, punct_break=punct_break, greek=greek, n_pairs=len(pl),
               canonical=cls["canonical"], hiatus=cls["hiatus"], violations=v_key, p=p,
               null_q05=q05, null_median=med, null_min=srt[0], pairs=pl)
    if verbose:
        print(f"[{conv} {xd} tcurl={'NU' if tcurl else 'opaque'} punct={'break' if punct_break else 'transp'} "
              f"{'greek' if greek else 'romance'}] pairs={len(pl)} canonical={cls['canonical']} "
              f"hiatus={cls['hiatus']} violations={v_key} | null min={srt[0]} q05={q05} median={med} "
              f"| p(V<=key)={p:.4f}")
    return out


def best_of_two(xd="V2_eye", tcurl=True, punct_break=False, greek=False):
    """Matched budget: key stat = min over S1,S2; null = min over (T on S1 pairs, swap(T) on S2 pairs)."""
    pl = {c: [p for l in LINES for p in pairs(l, c, xd, tcurl, punct_break)] for c in F.CONVENTIONS}

    def V(t, c):
        kv = {s: (F.KEYS[c][s][0], t[s]) for s in F.KEY_SIGNS}
        return sum(F.pair_class(a, b, kv, greek) == "violation" for a, b, _ in pl[c])

    k = min(V(typing_of(F.KEY_S1), "S1"), V(typing_of(F.KEY_S2), "S2"))
    null = [min(V(t, "S1"), V(F.swap_x_dot(t), "S2")) for t in F.all_typings(F.KEY_S1)]
    p = sum(v <= k for v in null) / len(null)
    print(f"[best-of-2 {xd} tcurl={'NU' if tcurl else 'opaque'}] key min V={k} | null median="
          f"{statistics.median(null)} q05={sorted(null)[int(0.05*len(null))]} | p={p:.4f}")
    return k, p


def t1(conv, xd, tcurl):
    rows = []
    for l in LINES:
        c = line_final(l, conv, xd, tcurl)
        if c is None or not F.is_key(c):
            rows.append((l, c, "no prediction"))
        else:
            rows.append((l, c, F.line_final_class(c, F.KEYS[conv])))
    return rows


if __name__ == "__main__":
    print("=== T1  line-final rime (couplets counted once) ===")
    for conv in F.CONVENTIONS:
        for tcurl in (True, False):
            rows = t1(conv, "V2_eye", tcurl)
            bad = sorted({(l + 1) // 2 for l, c, r in rows if r == "violation"})
            print(f" {conv} tcurl={'NU' if tcurl else 'opaque'}: violating couplets {bad}  "
                  f"finals={[(l, c) for l, c, r in rows if r != 'no prediction']}")
    print("\n=== T3  predecessor of every glyph-initial single tilde N ===")
    for conv in F.CONVENTIONS:
        for tcurl in (True, False):
            preds = [p for l in LINES for p in n_predecessors(l, conv, "V2_eye", tcurl)]
            key = F.KEYS[conv]
            kinds = Counter(("key:" + key[p][1]) if F.is_key(p) else p for p in preds)
            viol = sum(1 for p in preds if F.is_key(p) and key[p][1] in ("O", "RO"))
            print(f" {conv} tcurl={'NU' if tcurl else 'opaque'}: n={len(preds)} {dict(kinds)} violations={viol}")
    print("\n=== T4  typed grammar, exact 4,200-typing null ===")
    run("S1", "V2_eye", True)                       # PRIMARY
    for conv, xd, tc, pb, gk in itertools.product(F.CONVENTIONS, ("V1_all_dots", "V2_eye", "V3_measured"),
                                                  (True, False), (False, True), (False, True)):
        if (conv, xd, tc, pb, gk) == ("S1", "V2_eye", True, False, False):
            continue
        run(conv, xd, tc, pb, gk)
    print()
    for xd in ("V1_all_dots", "V2_eye", "V3_measured"):
        for tc in (True, False):
            best_of_two(xd, tc)
