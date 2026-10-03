#!/usr/bin/env python3
"""
ATTACK R2 (new, 2026-10-03) — TEMPLATE GENERATIVITY.

The earlier suite attacks the claim's parts one at a time. R2 attacks the
whole: it asks whether the eight-node architecture the dossier draws is a
discovery about Scribe 9 or a template that any comparable slice of the
Haghia Triada archive would satisfy.

Each of the claim's eight architectural nodes is turned into a detector that
is deliberately as generous as the claimant's own usage, and FROZEN before
any set is scored:

  1 accountable unit      a face whose first sign-group is followed by a
                          divider and carries no numeral (header slot) --
                          the slot U-MI-NA-SI / SA-TA / *21F-TU-NE occupy
  2 personnel assessment  a VIR / MUL ideogram, or an entry list of >=4
                          sign-groups each carrying the numeral 1
  3 standardized group    some stated total divisible by an m in 2..12 with
                          quotient >=2 and the quotient equal to an entry
                          count somewhere on the tablet
  4 assignment            >=2 header slots on one tablet (a list divided
                          between named responsible parties)
  5 roster checking       a name on the set recurring on >=2 of its tablets
  6 KI-RO exception       a KI-RO token
  7 census-linked prov.   a staple ideogram (GRA/OLE/OLIV/VIN/FIC/CYP/NI)
                          on a tablet of the set
  8 control totals        a KU-RO token (PO-TO-KU-RO scored separately)

A template that fits everything explains nothing.  If random 10-tablet HT
subsets routinely score 7/8 or 8/8, "an integrated labour-liability
administration" is not a reading of Scribe 9's dossier; it is a description
of the Haghia Triada archive's formatting, applied to one slice of it.
"""
import collections, random, re
import r_common as R

A = R.load()
T = R.ht_tablets(A)
POOL = sorted(T)
SEED = 20261003
STAPLE = re.compile(r'^(GRA|OLE|OLIV|VIN|FIC|CYP|NI|HORD|AROM)')
PERSON = re.compile(r'^(VIR|MUL)')


def header_slots(face):
    """sign-groups immediately followed by a divider and not by a numeral"""
    ws = [w for w in A[face]["transliteratedWords"] if w != "\n"]
    out = []
    for i, w in enumerate(ws):
        if R.is_sign_group(w) and i + 1 < len(ws) and ws[i + 1] in (R.DIV, R.DIVL):
            out.append(w)
    return out


def tokens(ts):
    return [w for t in ts for f in T[t] for w in A[f]["transliteratedWords"]]


def score(ts):
    """returns dict node -> bool, for a set of tablet ids"""
    toks = tokens(ts)
    s = {}
    s[1] = any(header_slots(f) for t in ts for f in T[t])
    s[2] = any(PERSON.match(w) for w in toks) or any(
        len([a for _, a in R.entries(A, f) if a == 1]) >= 4 for t in ts for f in T[t])
    # node 3: 'standardized group'
    n3 = False
    for t in ts:
        tots = [v for f in T[t] for _, v in R.stated_totals(A, f)]
        counts = [len(R.entries(A, f)) for f in T[t]]
        for v in tots:
            for m in range(2, 13):
                if v % m == 0 and v // m >= 2 and (v // m) in counts + [c - 1 for c in counts]:
                    n3 = True
    s[3] = n3
    s[4] = any(len(header_slots(f)) >= 2 for t in ts for f in T[t])
    nm = collections.Counter()
    for t in ts:
        for n in R.names_on(A, T[t]):
            nm[n] += 1
    s[5] = any(c >= 2 for c in nm.values())
    s[6] = "KI-RO" in toks
    s[7] = any(STAPLE.match(w) for w in toks)
    s[8] = "KU-RO" in toks
    return s


LABEL = {1: "accountable unit header", 2: "personnel assessment",
         3: "standardized group ratio", 4: "assignment (>=2 headers)",
         5: "roster checking (recurring name)", 6: "KI-RO exception",
         7: "census-linked staple", 8: "KU-RO control total"}

print("=" * 78)
print("ATTACK R2 — is the eight-node architecture a discovery or a template?")
print("=" * 78)

D = R.DOSSIER
sd = score(D)
print("\n-- the Scribe-9 dossier, scored by the frozen detectors")
for k in sorted(sd):
    print(f"   node {k}  {LABEL[k]:34s} {'YES' if sd[k] else 'no'}")
print(f"   dossier score = {sum(sd.values())}/8"
      f"   (PO-TO-KU-RO present: {'PO-TO-KU-RO' in tokens(D)})")

print("\n-- every HT scribe with >=3 attributed tablets, same detectors")
byscribe = collections.defaultdict(set)
for t in POOL:
    for f in T[t]:
        sc = A[f].get("scribe") or ""
        if sc.startswith("HT Scribe"):
            byscribe[sc].add(t)
rows = []
for sc, ts in sorted(byscribe.items()):
    if len(ts) >= 3:
        s = score(sorted(ts))
        rows.append((sum(s.values()), sc, len(ts), s))
for tot, sc, n, s in sorted(rows, reverse=True):
    miss = [k for k in sorted(s) if not s[k]]
    print(f"   {sc:15s} n={n:2d}  score {tot}/8   missing: {[LABEL[k] for k in miss] or '-'}")

print("\n-- random 10-tablet HT subsets (the null the claim never ran)")
rng = random.Random(SEED)
slots = {t: len(R.types_on(A, T[t])) for t in POOL}
target = sum(slots[t] for t in D)
dist = collections.Counter()
nodehit = collections.Counter()
N = 2000
done, tries = 0, 0
while done < N and tries < 2000000:
    tries += 1
    s = rng.sample(POOL, 10)
    if abs(sum(slots[t] for t in s) - target) > 0.10 * target:
        continue
    done += 1
    sc = score(s)
    dist[sum(sc.values())] += 1
    for k, v in sc.items():
        if v:
            nodehit[k] += 1
print(f"   size-matched draws (+/-10% of {target} type-slots): n={done}")
for k in sorted(dist):
    print(f"     score {k}/8 : {dist[k]:5d}  ({100*dist[k]/done:5.1f}%)")
ge = sum(c for k, c in dist.items() if k >= sum(sd.values()))
print(f"   P(a size-matched random 10-tablet subset scores >= the dossier's "
      f"{sum(sd.values())}/8) = {ge/done:.4f}")
print("   per-node hit rate in random subsets:")
for k in sorted(LABEL):
    print(f"     node {k}  {LABEL[k]:34s} {100*nodehit[k]/done:5.1f}%")

print("\n-- unmatched random 10-tablet subsets (no size matching)")
rng2 = random.Random(SEED + 7)
dist2 = collections.Counter()
for _ in range(2000):
    s = rng2.sample(POOL, 10)
    dist2[sum(score(s).values())] += 1
for k in sorted(dist2):
    print(f"     score {k}/8 : {dist2[k]:5d}  ({100*dist2[k]/2000:5.1f}%)")
ge2 = sum(c for k, c in dist2.items() if k >= sum(sd.values()))
print(f"   P(>= dossier score) = {ge2/2000:.4f}")
