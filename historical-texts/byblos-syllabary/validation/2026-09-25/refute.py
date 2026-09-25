#!/usr/bin/env python3
"""
Refuter checks for the Byblos "inventory split / conditional ME anchor transfer"
claim (PARTIAL_BIGRAPH_KERNEL.md, ME_ANCHOR_TRANSFER.md).

Run order follows board/PRACTICES.md:
  0. information ceiling  (BEFORE any alignment / normalisation validation)
  1. raw glyph identity   (reproduce the loci from the primary transcription)
  2. search freedom / budget-matched null
  3. row-by-row adjudication table

Usage: python3 parse_ocbi.py && python3 refute.py
"""
import json, os, itertools, random, math
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "ocbi_parsed.json")))
FR, SY = D["fragments"], D["syllabaries"]

ME      = "E49A"   # Maeder's me, exact form
ME_MIRR = "E4B0"   # mirrored me on BYBL rc
FOLL    = "E402"   # the invariant follower claimed in ME_ANCHOR_TRANSFER
Y       = "E48F"   # third sign, 2 of 3
Z       = "E412"   # third sign at BYBL k; the claimed T-class member
T_CYL   = "E491"   # penultimate cylinder sign of Meketaton
ATON    = "E4AF"   # GEAS Aton candidate
ATON_ST = "E416"   # stale syllableMap ATON
PA      = "E44D"

CYL = {"ra", "rb (Var. 1)", "rb (Var. 2)", "rb (Var. 3)",
       "rc (Var. 1)", "rc (Var. 2) ", "rc (Var. 3)", "rd"}

def is_sign(t):  return t["kind"] == "sign"
def clear(t):    return is_sign(t) and not t["guess"]

def line_signs(line, clear_only=False):
    """Sequence of sign tokens; wildcards/fractures become None (a break)."""
    out = []
    for t in line:
        if t["kind"] == "sign" and (clear(t) if clear_only else True):
            out.append(t)
        else:
            out.append(None)
    return out

def core_frags():
    return [f for f in FR if f["id"] not in CYL]

# ---------------------------------------------------------------- section 0
def sec0_ceiling():
    print("=" * 78)
    print("0. INFORMATION CEILING  (shared reference = the OCBI sign inventory)")
    print("=" * 78)
    # The shared reference is the grapheme inventory: every downstream statement
    # ("exact E49A", "E412 ~ E491", "E416 != E4AF") is read off it. OCBI ships
    # 10 realisations of that reference. Their disagreement is the reference's
    # own error, and it is systematic: it does not average down over tokens.
    names = [s["name"] + "/" + s["id"] for s in SY]
    def same(s, a, b):
        ga = [g for g in s["groups"] if a in g]
        gb = [g for g in s["groups"] if b in g]
        if not ga or not gb:
            return None           # sign absent from this inventory
        return 1 if ga[0] is gb[0] else 0

    pairs = [("E416/E4AF  (the inventory SPLIT claim)", ATON_ST, ATON),
             ("E412/E491  (the ME-?-T(?) bridge)",      Z, T_CYL),
             ("E49A/E4B0  (the ME allograph)",          ME, ME_MIRR)]
    print("\n per-pair verdict of each of the 10 OCBI inventories (1=merged, 0=split, .=absent)")
    print("  %-42s %s" % ("pair", " ".join("%-10s" % s["id"] for s in SY)))
    rows = {}
    for label, a, b in pairs:
        v = [same(s, a, b) for s in SY]
        rows[label] = v
        print("  %-42s %s" % (label,
              " ".join("%-10s" % ("." if x is None else x) for x in v)))
    print("\n d'_ceiling for 'is this pair one grapheme?', reference error estimated")
    print(" from the reference's own realisations (mu(A)=1 truly-same, mu(B)=0 truly-different):")
    for label, a, b in pairs:
        v = [x for x in rows[label] if x is not None]
        n = len(v); p = sum(v) / n
        sd = math.sqrt(p * (1 - p))
        d = float("inf") if sd == 0 else 1.0 / math.sqrt(2 * sd * sd)
        print("   %-42s n=%2d  p(merged)=%.3f  sigma_ref=%.3f  d'_ceiling=%s"
              % (label, n, p, sd, "inf" if d == float("inf") else "%.2f" % d))

    # Global reference error: over ALL codepoint pairs, how often do two
    # inventories disagree about co-membership?
    allcp = sorted({c for s in SY for g in s["groups"] for c in g})
    memb = []
    for s in SY:
        m = {}
        for i, g in enumerate(s["groups"]):
            for c in g:
                m[c] = i
        memb.append(m)
    dis = tot = 0
    agree_same = 0
    for a, b in itertools.combinations(allcp, 2):
        vs = [1 if m[a] == m[b] else 0 for m in memb if a in m and b in m]
        if len(vs) < 2:
            continue
        tot += 1
        if 0 < sum(vs) < len(vs):
            dis += 1
        if sum(vs) == len(vs):
            agree_same += 1
    print("\n global reference error: of %d codepoint pairs seen in >=2 inventories,"
          % tot)
    print("   %d (%.1f%%) are classed BOTH ways by different OCBI inventories;"
          % (dis, 100 * dis / tot))
    print("   %d (%.2f%%) are unanimously one grapheme." % (agree_same, 100*agree_same/tot))
    # conditional: among pairs ever merged, how often unanimous?
    ever = [ (a,b) for a,b in itertools.combinations(allcp,2)
             if any(m.get(a) is not None and m.get(a)==m.get(b) for m in memb) ]
    unan = 0
    for a,b in ever:
        vs = [1 if m[a]==m[b] else 0 for m in memb if a in m and b in m]
        if sum(vs)==len(vs): unan += 1
    print("   of the %d pairs merged by at least one inventory, only %d (%.1f%%) are"
          % (len(ever), unan, 100*unan/len(ever)))
    print("   merged by all of them -> the reference is unstable on %.1f%% of its own merges."
          % (100*(1-unan/len(ever))))
    return rows

# ---------------------------------------------------------------- section 1
def sec1_loci():
    print()
    print("=" * 78)
    print("1. RAW GLYPH IDENTITY: every occurrence of the anchor signs, from source")
    print("=" * 78)
    for tag, cpt in [("ME  E49A", ME), ("ME' E4B0", ME_MIRR), ("PA  E44D", PA),
                     ("ATON E4AF", ATON), ("E416", ATON_ST),
                     ("E412", Z), ("E491", T_CYL), ("E402", FOLL), ("E48F", Y)]:
        occ = []
        for f in FR:
            for li, line in enumerate(f["lines"], 1):
                for pi, t in enumerate(line, 1):
                    if t["kind"] == "sign" and t["cp"] == cpt:
                        occ.append((f["id"], li, pi, t["guess"]))
        nclear = sum(1 for o in occ if not o[3])
        ncore  = sum(1 for o in occ if o[0] not in CYL)
        ncoreclear = sum(1 for o in occ if o[0] not in CYL and not o[3])
        print("  %-10s total %3d  clear %3d  | off-cylinder %3d  off-cyl+clear %3d"
              % (tag, len(occ), nclear, ncore, ncoreclear))
        if cpt in (ME, ME_MIRR, ATON, PA):
            for o in occ:
                print("        %-18s line %2d pos %2d %s"
                      % (o[0], o[1], o[2], "(GUESS)" if o[3] else ""))

    print("\n  exact contexts of off-cylinder E49A, straight from the transcription:")
    for f in core_frags():
        for li, line in enumerate(f["lines"], 1):
            seq = line
            for pi, t in enumerate(line):
                if t["kind"] == "sign" and t["cp"] == ME:
                    ctx = []
                    for q in line[max(0, pi - 3): pi + 4]:
                        s = q["cp"] if q["kind"] == "sign" else q["kind"].upper()
                        if q["kind"] == "sign" and q["guess"]:
                            s += "?"
                        ctx.append(s)
                    print("    %-18s line %s pos %2d : %s"
                          % (f["id"], "IVXL"[0:0] or li, pi + 1, " ".join(ctx)))

# ---------------------------------------------------------------- section 2
def sec2_null():
    print()
    print("=" * 78)
    print("2. SEARCH FREEDOM / BUDGET-MATCHED NULL")
    print("=" * 78)
    # a) how common is E402 overall and as a right-neighbour?
    core = core_frags()
    signs = [t["cp"] for f in core for l in f["lines"] for t in l if is_sign(t)]
    cnt = Counter(signs)
    N = len(signs)
    print("  off-cylinder sign tokens: %d ; distinct forms: %d" % (N, len(cnt)))
    print("  rank of E402 by frequency: %d of %d   (count %d, %.2f%% of tokens)"
          % (sorted(cnt.values(), reverse=True).index(cnt[FOLL]) + 1,
             len(cnt), cnt[FOLL], 100 * cnt[FOLL] / N))
    print("  top 12 off-cylinder signs:", ", ".join("%s:%d" % x for x in cnt.most_common(12)))

    # right-neighbour distribution over the whole off-cylinder corpus
    rn = Counter(); pairs = 0
    for f in core:
        for l in f["lines"]:
            for a, b in zip(l, l[1:]):
                if is_sign(a) and is_sign(b):
                    rn[b["cp"]] += 1; pairs += 1
    print("  adjacent sign-sign pairs: %d ; P(right neighbour = E402) = %.4f"
          % (pairs, rn[FOLL] / pairs))
    p402 = rn[FOLL] / pairs

    # b) the actual observed event, exactly as the note frames it
    print("\n  observed: 3 off-cylinder E49A tokens, all with right neighbour E402.")
    print("  naive p (i.i.d. right neighbour, no search correction) = %.4f^3 = %.3e"
          % (p402, p402 ** 3))
    # collision probability: probability 3 draws from the neighbour distribution coincide
    q = sum((c / pairs) ** 3 for c in rn.values())
    print("  p(3 right neighbours all EQUAL, whichever sign) = sum p_i^3 = %.4f  (1 in %.0f)"
          % (q, 1 / q))

    # c) BUDGET-MATCHED NULL: the note picked one sign (externally, fine) but the
    #    *pattern* (a shared neighbour) was chosen post hoc. Charge that budget by
    #    asking the same question of every sign with the same evidence weight.
    print("\n  budget-matched null -- same question asked of EVERY off-cylinder sign:")
    occ = defaultdict(list)
    for f in core:
        for l in f["lines"]:
            for i, t in enumerate(l):
                if is_sign(t):
                    left  = l[i-1] if i > 0 else None
                    right = l[i+1] if i + 1 < len(l) else None
                    occ[t["cp"]].append((
                        left["cp"]  if left  is not None and is_sign(left)  else None,
                        right["cp"] if right is not None and is_sign(right) else None))
    for k in (2, 3, 4):
        elig = {s: v for s, v in occ.items() if len(v) == k}
        hitR = [s for s, v in elig.items()
                if all(x[1] is not None for x in v) and len({x[1] for x in v}) == 1]
        hitL = [s for s, v in elig.items()
                if all(x[0] is not None for x in v) and len({x[0] for x in v}) == 1]
        hitEither = set(hitR) | set(hitL)
        print("   signs with exactly %d off-cylinder tokens: %3d | invariant RIGHT nb: %2d"
              "  invariant LEFT nb: %2d  either side: %2d (%.0f%%)"
              % (k, len(elig), len(hitR), len(hitL), len(hitEither),
                 100 * len(hitEither) / max(1, len(elig))))
        if k == 3:
            print("      the 3-token signs with an invariant right neighbour:",
                  ", ".join(sorted(hitR)))
            print("      the 3-token signs with an invariant left  neighbour:",
                  ", ".join(sorted(hitL)))

    # d) and the stronger claim: 2 of 3 share the whole trigraph
    print("\n  same budget for the TRIGRAPH claim (>=2 of the tokens share sign+2):")
    tri = defaultdict(list)
    for f in core:
        for l in f["lines"]:
            for i, t in enumerate(l):
                if is_sign(t) and i + 2 < len(l) and is_sign(l[i+1]) and is_sign(l[i+2]):
                    tri[t["cp"]].append((l[i+1]["cp"], l[i+2]["cp"]))
    elig3 = {s: v for s, v in tri.items() if len(v) >= 2}
    rep = [s for s, v in elig3.items() if max(Counter(v).values()) >= 2]
    print("   signs with >=2 full trigraph contexts: %d ; of those, %d (%.0f%%) repeat a trigraph"
          % (len(elig3), len(rep), 100 * len(rep) / len(elig3)))
    print("   repeated-trigraph signs:", ", ".join(sorted(rep)))

    # e) the corpus is formulaic: how repetitive is it generally?
    big = Counter()
    for f in core:
        for l in f["lines"]:
            for a, b in zip(l, l[1:]):
                if is_sign(a) and is_sign(b):
                    big[(a["cp"], b["cp"])] += 1
    rep_big = sum(1 for v in big.values() if v > 1)
    print("\n   distinct off-cylinder bigrams: %d ; repeated at least twice: %d (%.1f%%)"
          % (len(big), rep_big, 100 * rep_big / len(big)))
    print("   most repeated bigrams:", ", ".join("%s%s:%d" % (a, b, c)
          for (a, b), c in big.most_common(8)))
    print("   the claimed one, E49A-E402: %d  |  E402-E48F: %d"
          % (big[(ME, FOLL)], big[(FOLL, Y)]))

    # f) is E402->E48F special, as the note asserts?
    right_of_402 = Counter()
    for f in core:
        for l in f["lines"]:
            for a, b in zip(l, l[1:]):
                if is_sign(a) and a["cp"] == FOLL and is_sign(b):
                    right_of_402[b["cp"]] += 1
    tot402 = sum(right_of_402.values())
    print("   right-neighbour distribution of E402 off-cylinder (n=%d): %s"
          % (tot402, dict(right_of_402.most_common())))

# ---------------------------------------------------------------- section 3
def sec3_rows():
    print()
    print("=" * 78)
    print("3. ROW-BY-ROW ADJUDICATION (proximity is not construction)")
    print("=" * 78)
    for f in FR:
        if f["id"] in CYL:
            for li, l in enumerate(f["lines"], 1):
                s = " ".join((t["cp"] + ("?" if t["guess"] else ""))
                             if is_sign(t) else t["kind"][0].upper() for t in l)
                print("   %-18s : %s" % (f["id"], s))

if __name__ == "__main__":
    sec0_ceiling()
    sec1_loci()
    sec2_null()
    sec3_rows()
