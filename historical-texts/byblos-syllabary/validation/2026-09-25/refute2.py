#!/usr/bin/env python3
"""
Part 2 of the 2026-09-25 refuter checks: inventory sensitivity, a randomisation
null with the search budget matched on both sides, and the inventory-consistency
audit (is there ANY single OCBI inventory under which the claim's three
load-bearing statements are simultaneously true?).
"""
import json, os, random, itertools
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "ocbi_parsed.json")))
FR, SY = D["fragments"], D["syllabaries"]

ME, FOLL, Y, Z, T_CYL = "E49A", "E402", "E48F", "E412", "E491"
ME_MIRR, ATON, ATON_ST = "E4B0", "E4AF", "E416"
CYL = {"ra", "rb (Var. 1)", "rb (Var. 2)", "rb (Var. 3)",
       "rc (Var. 1)", "rc (Var. 2) ", "rc (Var. 3)", "rd"}
core = [f for f in FR if f["id"] not in CYL]
is_sign = lambda t: t["kind"] == "sign"

def memb(s):
    m = {}
    for i, g in enumerate(s["groups"]):
        for c in g:
            m[c] = i
    return m

print("=" * 78)
print("A. CORPUS SHAPE vs PROBLEM.md's description")
print("=" * 78)
objs = Counter()
for f in FR:
    base = f["id"].split(" (")[0].strip()
    objs[(base, f["group"])] += 1
b = len({o for o, g in objs if g == "BYBL"})
q = len({o for o, g in objs if g == "BYBL?"})
print("  distinct objects marked BYBL : %d   BYBL? : %d   (PROBLEM.md says 18 / 14)" % (b, q))
print("  fragment ENTRIES (variants counted separately): %d" % len(FR))

print()
print("=" * 78)
print("B. INVENTORY SENSITIVITY: rerun the ME transfer under each OCBI inventory")
print("=" * 78)
print("  For each inventory, map every off-cylinder token to its grapheme CLASS,")
print("  then ask the note's own question of the class containing E49A.")
print()
print("  %-8s %-7s %-6s %-7s %-9s %-8s  %s" %
      ("inv", "|ME cls|", "tokens", "clear", "follower", "invariant?", "followers"))
for s in SY:
    m = memb(s)
    if ME not in m:
        print("  %-8s ME absent" % s["id"]); continue
    cls = s["groups"][m[ME]]
    toks = []
    for f in core:
        for l in f["lines"]:
            for i, t in enumerate(l):
                if is_sign(t) and t["cp"] in cls:
                    nxt = l[i + 1] if i + 1 < len(l) else None
                    toks.append((f["id"], t["cp"], t["guess"],
                                 nxt["cp"] if nxt is not None and is_sign(nxt) else None))
    clear_toks = [t for t in toks if not t[2] and t[3] is not None]
    folls = Counter(t[3] for t in clear_toks)
    cls_follow = [m.get(x) for x in folls]           # follower CLASS under same inv
    inv_raw = len(folls) == 1 and len(clear_toks) > 1
    inv_cls = len(set(cls_follow)) == 1 and len(clear_toks) > 1
    print("  %-8s %-7d %-6d %-7d %-9s %-8s  %s" %
          (s["id"], len(cls), len(toks), len(clear_toks),
           "class" if inv_cls else "-", "YES" if inv_raw else "no",
           ", ".join("%s:%d" % x for x in folls.most_common())))

print()
print("  same, for the T-class bridge: is the BYBL k terminal E412 in the same class")
print("  as the cylinder's penultimate E491 under each inventory?")
for s in SY:
    m = memb(s)
    a, bb = m.get(Z), m.get(T_CYL)
    print("    %-8s E412->grp %-5s  E491->grp %-5s  %s" %
          (s["id"], a, bb, "MERGED" if (a is not None and a == bb) else "SPLIT/absent"))

print()
print("=" * 78)
print("C. INVENTORY CONSISTENCY AUDIT")
print("=" * 78)
req = []
for s in SY:
    m = memb(s)
    split_aton = (ATON_ST in m and ATON in m and m[ATON_ST] != m[ATON])
    merge_T    = (Z in m and T_CYL in m and m[Z] == m[T_CYL])
    me_alone   = (ME in m and len(s["groups"][m[ME]]) == 1)
    me_small   = (ME in m and len(s["groups"][m[ME]]) <= 5)
    req.append((s["id"], split_aton, merge_T, me_alone, me_small,
                len(s["groups"][m[ME]]) if ME in m else None))
print("  %-8s %-12s %-12s %-10s %-10s %s" %
      ("inv", "E416!=E4AF", "E412~E491", "ME alone", "ME cls<=5", "|ME class|"))
for r in req:
    print("  %-8s %-12s %-12s %-10s %-10s %s" %
          (r[0], r[1], r[2], r[3], r[4], r[5]))
ok = [r[0] for r in req if r[1] and r[2]]
ok2 = [r[0] for r in req if r[1] and r[2] and r[4]]
print("\n  inventories satisfying BOTH (E416!=E4AF) and (E412~E491): %s" % (ok or "NONE"))
print("  ...and ALSO keeping the ME class small (<=5 forms):       %s" % (ok2 or "NONE"))

print()
print("=" * 78)
print("D. RANDOMISATION NULL, BUDGET MATCHED ON BOTH SIDES")
print("=" * 78)
# Null: keep each line's length and the multiset of signs in the whole off-cylinder
# corpus, shuffle sign identities across all positions (wildcards/fractures fixed).
positions = []
for fi, f in enumerate(core):
    for li, l in enumerate(f["lines"]):
        for pi, t in enumerate(l):
            if is_sign(t):
                positions.append((fi, li, pi, t["cp"], t["guess"]))
bag = [p[3] for p in positions]

def stats(assign):
    """assign: list of cp parallel to `positions`. Returns
       (#signs with exactly 3 clear tokens that have an invariant follower,
        #eligible, whether a *specified* 3-token sign is invariant)."""
    grid = {}
    for (fi, li, pi, _, g), cp in zip(positions, assign):
        grid[(fi, li, pi)] = (cp, g)
    occ = defaultdict(list)
    for (fi, li, pi), (cp, g) in grid.items():
        nxt = grid.get((fi, li, pi + 1))
        occ[cp].append((g, nxt[0] if nxt else None))
    hits = elig = 0
    tri_hits = tri_elig = 0
    for cp, v in occ.items():
        if len(v) == 3:
            elig += 1
            fol = [x[1] for x in v]
            if all(f is not None for f in fol) and len(set(fol)) == 1:
                hits += 1
    # trigraph: >=2 of exactly-3-token signs share follower+follower2
    for cp, v in occ.items():
        pass
    return hits, elig

random.seed(20260925)
obs_hits, obs_elig = stats([p[3] for p in positions])
print("  observed: %d of %d signs with exactly 3 off-cylinder tokens have a fully" %
      (obs_hits, obs_elig))
print("            invariant following sign.  (that one sign is E49A)")
NS = 4000
cnt_any, cnt_ge = 0, 0
tot_hits = 0
for _ in range(NS):
    a = bag[:]; random.shuffle(a)
    h, e = stats(a)
    tot_hits += h
    if h >= 1: cnt_any += 1
    if h >= obs_hits: cnt_ge += 1
print("  null (%d shuffles of sign identities over the same positions):" % NS)
print("    P(at least one 3-token sign has an invariant follower) = %.3f" % (cnt_any / NS))
print("    mean number of such signs per shuffle                  = %.3f" % (tot_hits / NS))
print("    p (>= observed, family-wise over all signs)            = %.3f" % (cnt_ge / NS))

# Single-sign null, no family correction: the externally fixed E49A only.
rn = Counter()
tot = 0
for f in core:
    for l in f["lines"]:
        for x, y2 in zip(l, l[1:]):
            if is_sign(x) and is_sign(y2):
                rn[y2["cp"]] += 1; tot += 1
p_coll = sum((c / tot) ** 3 for c in rn.values())
print("\n  single-sign null (E49A fixed externally, side and exactness chosen post hoc):")
print("    P(3 followers all identical) = %.5f  (1 in %.0f)" % (p_coll, 1 / p_coll))
print("    x2 for the free choice of side (left/right)  -> 1 in %.0f" % (1 / (2 * p_coll)))

print()
print("=" * 78)
print("E. ADJACENCY ROWS, EXACT, WITH MARKERS  (proximity is not construction)")
print("=" * 78)
for f in core:
    for li, l in enumerate(f["lines"], 1):
        for i, t in enumerate(l):
            if is_sign(t) and t["cp"] == ME:
                row = []
                for q in l:
                    if is_sign(q):
                        row.append(q["cp"] + ("?" if q["guess"] else ""))
                    else:
                        row.append(q["kind"][:4].upper())
                print("  %-4s line %d : %s" % (f["id"], li, " ".join(row)))
                left = l[i - 1] if i > 0 else None
                print("       left neighbour = %s   (ME_ANCHOR_TRANSFER table says: %s)"
                      % (left["cp"] if left is not None and is_sign(left) else "none",
                         {"i": "E442", "k": "E439", "m": "E410"}.get(f["id"], "?")))
