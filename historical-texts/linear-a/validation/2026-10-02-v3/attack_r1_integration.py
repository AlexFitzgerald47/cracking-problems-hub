#!/usr/bin/env python3
"""
ATTACK R1 (new, 2026-10-03) — the word the claim turns on is "INTEGRATED".

The claim is not that ten tablets exist in one hand. It is that they are
"an integrated labour-liability administration LINKING accountable units,
personnel assessments, standardized work groups, assignment, roster checking,
KI-RO exception reporting, census-linked provisioning and hierarchical
control totals".

"Linking" is a graph assertion and nothing in the earlier attack suite tests
it as one. R1 builds the dossier's own entity graph from the raw witness and
asks three questions the claim must answer YES to:

  R1a  is the dossier connected by shared designations at all, or is it ten
       tablets that share a hand and nothing else?
  R1b  do the KI-RO "exceptions" actually appear in the register they are
       supposedly exceptions against?  (roster checking)
  R1c  is the "census-linked provisioning" node attached to the labour nodes
       by anything other than a single syllabogram?
"""
import collections, random, itertools
import r_common as R

A = R.load()
T = R.ht_tablets(A)
D = R.DOSSIER
SEED = 20261003

print("=" * 78)
print("ATTACK R1 — is the dossier an INTEGRATED system, as a graph?")
print("=" * 78)
print("  witness: data/LinearAInscriptions.js (2026-09-25 snapshot, vendored)")
print()

names = {t: R.names_on(A, T[t]) for t in D}
alln  = {t: R.types_on(A, T[t]) for t in D}
for t in D:
    print(f"  {t:7s} faces={','.join(T[t]):15s} multi-sign designations={len(names[t]):2d}  all sign-groups={len(alln[t]):2d}")

# ---------------------------------------------------------------- R1a
print()
print("-- R1a  dossier link graph, edge = >=1 shared MULTI-SIGN designation")
edges = []
for a, b in itertools.combinations(D, 2):
    sh = names[a] & names[b]
    if sh:
        edges.append((a, b, sorted(sh)))
for a, b, sh in edges:
    print(f"     {a}--{b}: {sh}")
deg = collections.Counter()
for a, b, _ in edges:
    deg[a] += 1; deg[b] += 1
iso = [t for t in D if deg[t] == 0]
print(f"     edges={len(edges)} of {len(D)*(len(D)-1)//2} possible; isolated tablets={iso}")

# connected components
parent = {t: t for t in D}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x
for a, b, _ in edges:
    parent[find(a)] = find(b)
comp = collections.defaultdict(list)
for t in D:
    comp[find(t)].append(t)
print(f"     connected components: {len(comp)} -> {[sorted(v) for v in comp.values()]}")
big = max((len(v) for v in comp.values()), default=0)
print(f"     largest component covers {big}/10 tablets")

print()
print("-- R1a' same graph when single syllabograms ARE allowed as designations")
edges2 = []
for a, b in itertools.combinations(D, 2):
    sh = (alln[a] & alln[b]) - R.OPERATORS
    if sh:
        edges2.append((a, b, sorted(sh)))
print(f"     edges={len(edges2)}; the extra edges are carried by:")
extra = collections.Counter()
for a, b, sh in edges2:
    if not (names[a] & names[b]):
        for s in sh:
            extra[s] += 1
for s, c in extra.most_common():
    print(f"       {s:12s} supplies {c} of the extra edges   (single sign: {'-' not in s})")

# null: does a random 10-tablet HT set link up as much?
pool = sorted(T)
rng = random.Random(SEED)
nm_all = {t: R.names_on(A, T[t]) for t in pool}
def n_edges(ts):
    return sum(1 for a, b in itertools.combinations(ts, 2) if nm_all[a] & nm_all[b])
obs = n_edges(D)
# size-matched on sign-group type-slots, as the earlier suite does
slots = {t: len(R.types_on(A, T[t])) for t in pool}
target = sum(slots[t] for t in D)
draws, hits = 0, 0
vals = []
tries = 0
while draws < 20000 and tries < 4000000:
    tries += 1
    s = rng.sample(pool, 10)
    if abs(sum(slots[t] for t in s) - target) <= 0.10 * target:
        draws += 1
        e = n_edges(s)
        vals.append(e)
        if e >= obs:
            hits += 1
print()
print(f"-- R1a'' null for the edge count (size-matched, +/-10% of {target} type-slots, n={draws})")
print(f"     observed edges among the dossier = {obs}")
if draws:
    vals.sort()
    print(f"     null mean {sum(vals)/len(vals):.2f}  95% [{vals[int(.025*len(vals))]}, {vals[int(.975*len(vals))-1]}]"
          f"  p = {(hits+1)/(draws+1):.4f}")

# ---------------------------------------------------------------- R1b
print()
print("-- R1b  ROSTER CHECKING: are the KI-RO 'exceptions' in the master register?")
# the KI-RO blocks the claim names, read off the raw faces
def kiro_block(face):
    ws = [w for w in A[face]["transliteratedWords"] if w != "\n"]
    if "KI-RO" not in ws:
        return []
    i = ws.index("KI-RO")
    out = []
    for w in ws[i + 1:]:
        if w in R.TOTALS:
            break
        if R.is_name(w):
            out.append(w)
    return out

exc = {}
for f in ["HT94b", "HT117a"]:
    exc[f] = kiro_block(f)
    print(f"     {f} KI-RO block names ({len(exc[f])}): {exc[f]}")
exc_all = set(exc["HT94b"]) | set(exc["HT117a"])

reg = R.names_on(A, T["HT122"])
print(f"     HT122 'master personnel liability/control register' names ({len(reg)}): {sorted(reg)}")
ov = exc_all & reg
print()
print(f"     exception names also in the master register: {len(ov)}/{len(exc_all)} -> {sorted(ov)}")
print(f"     register names that ever appear in a dossier KI-RO block: {len(ov)}/{len(reg)}")

# null from marginal frequencies: how often does a name on >=1 HT tablet
# also occur on HT122, given corpus-wide name frequencies?
tab_of = collections.defaultdict(set)
for t in pool:
    for n in nm_all[t]:
        tab_of[n].add(t)
rng2 = random.Random(SEED + 1)
pool_names = sorted(tab_of)
hits2, n2, dist = 0, 20000, []
for _ in range(n2):
    s = rng2.sample(pool_names, len(exc_all))
    k = len(set(s) & reg)
    dist.append(k)
    if k >= len(ov):
        hits2 += 1
dist.sort()
print(f"     null: {len(exc_all)} names drawn at random from the {len(pool_names)} HT multi-sign")
print(f"     designations; overlap with HT122's {len(reg)} names:")
print(f"       null mean {sum(dist)/len(dist):.2f}  p(>= observed {len(ov)}) = {(hits2+1)/(n2+1):.4f}")
print("     how common are the two overlapping names corpus-wide:")
for n in sorted(ov):
    print(f"       {n:12s} on {len(tab_of[n])} of {len(pool)} HT tablets -> {sorted(tab_of[n])}")

# ---------------------------------------------------------------- R1c
print()
print("-- R1c  'CENSUS-LINKED PROVISIONING': what attaches HT128 to the labour tablets?")
lab = set()
for t in ["HT85", "HT87", "HT94", "HT117", "HT119", "HT122"]:
    lab |= alln[t]
h128 = alln["HT128"]
print(f"     HT128 sign-groups: {sorted(h128)}")
print(f"     shared with the six labour tablets: {sorted(h128 & lab)}")
print(f"     of those, MULTI-SIGN: {sorted(x for x in (h128 & lab) if '-' in x)}")
print(f"     HT128 raw: ", " ".join(w for w in A['HT128a']['transliteratedWords'] if w != '\n'))
print(f"                ", " ".join(w for w in A['HT128b']['transliteratedWords'] if w != '\n'))
for t in ["HT112", "HT132", "HT135"]:
    sh = alln[t] & lab
    print(f"     {t}: shared with labour tablets {sorted(sh)}  (multi-sign {sorted(x for x in sh if '-' in x)})")
