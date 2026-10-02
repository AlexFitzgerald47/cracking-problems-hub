#!/usr/bin/env python3
"""
REFUTER ATTACK 1 -- POWER / OVERFIT NULL on the three-name anchor.

PROBLEM.md criterion 1 demands "an explicit power analysis stating what a corpus
of this size can and cannot support".  No such analysis exists in
PARTIAL_BIGRAPH_KERNEL.md, PALIMPSEST_CHRONOLOGY.md, ME_ANCHOR_TRANSFER.md or
PROGRESS.md (see r9_paper_audit.py).  This script builds one.

The kernel's section 2 lists five "external constraints" that are supposed to
make the Amarna daughter-name alignment something other than an after-the-fact
fit.  Two of them (1: the three texts occupy the positions of the three named
daughters; 4: orientation follows the figures) are iconographic and cannot be
tested from the transcription -- they are taken as given here, i.e. GRANTED to
the claim.  Three of them are statements about the sign strings and ARE
testable:

  (2) relative text lengths: two shorter names vs one longer
  (3) the two -Aton daughters share a ME-family onset AND "the exact same
      terminal sign" E4AF
  (5) the longer name has E44D ("pa") in the expected internal position (4th)

This script asks: how surprising is a string configuration satisfying (2),(3),(5)?

Three nulls:
  K1  analytic per-trial probability from off-cylinder sign frequencies,
      with the search budget that the claim actually spent made explicit
  K2  empirical: how many triples ANYWHERE in the off-cylinder Dunand core
      satisfy exactly the same template?
  K3  Monte-Carlo over the seal itself: re-draw the seal's four columns from
      corpus sign statistics and ask how often the template appears, charging
      the variant-reading budget the OCBI actually offers.
"""
import itertools, random, collections, math, sys
import lib_ocbi as L

random.seed(20261002)
src = L.load_src()
frags = L.parse_fragments(src)
syls = L.parse_syllabaries(src)
GN = L.glyphnames()
byid = {f["id"]: f for f in frags}

ME_A, ME_B = "E49A", "E4B0"
PA = "E44D"
ATON_HUB = "E4AF"


def name(c):
    return GN.get(c, {}).get("name", "?")


def seq(fid):
    return [t["cp"] for t in byid[fid]["lines"][0] if t["kind"] == "sign"]


print("=" * 78)
print("K0.  WHAT THE SEAL ACTUALLY OFFERS  (primary source, not the write-up)")
print("=" * 78)
cols = [f["id"] for f in frags if f["id"] in L.CYLINDER]
print("  OCBI records %d entries for the seal, i.e. %d physical columns with"
      % (len(cols), len(set(c.split(" (")[0] for c in cols))))
print("  alternative readings:")
for c in cols:
    s = seq(c)
    print("    %-16s n=%d  %s" % (c, len(s), " ".join(s)))
print()
print("  -> the composition is said to carry THREE daughter names, but OCBI")
print("     transcribes FOUR columns (ra, rb, rc, rd).  Column rd is left")
print("     unaccounted for by the alignment; choosing which 3 of 4 columns to")
print("     use is a free parameter the kernel never charges.")
print("  -> rb has 3 alternative readings, rc has 3.  9 combinations.")

# ---------------------------------------------------------------- frequencies
off = L.corpus(canon=True, off_cylinder=True)
rs = L.runs(off)
tokens = [t["cp"] for _, _, r in rs for t in r]
freq = collections.Counter(tokens)
N = len(tokens)
p = {c: n / N for c, n in freq.items()}
print()
print("  off-cylinder canonical corpus: %d sign tokens, %d distinct forms" % (N, len(freq)))

sum_p2 = sum(v * v for v in p.values())
print("  P(two independently drawn signs are the SAME form)  = sum p_i^2 = %.5f"
      % sum_p2)

print()
print("=" * 78)
print("K1.  ANALYTIC PER-TRIAL PROBABILITY, AND THE BUDGET ACTUALLY SPENT")
print("=" * 78)

# onset constraint: how free is "mirrored/allographic me"?
# three readings of the licence, weakest -> strongest
onset_free = 1.0
# (b) same grapheme class in the inventory used
cm_default = L.classmap(syls[0])
cls = collections.Counter(cm_default.get(c, "?" + c) for c in tokens)
sum_pc2 = sum((v / N) ** 2 for v in cls.values())
# (c) OCBI's own explicit mirror taxonomy
mirror_pairs = 0
names = {c: name(c) for c in GN}
base = {}
for c, nm in names.items():
    core = nm.split("   ")[-1].strip() if "   " in nm else nm
    base.setdefault(core, []).append(c)
n_mirror_named = sum(1 for nm in names.values() if "gespiegelt" in nm)
print("  licence (a) FREE  'declare any two forms mirror allographs': P=1")
print("  licence (b) same grapheme class in the DEFAULT OCBI inventory:")
print("              P(two random tokens in one class) = sum P(c)^2 = %.5f" % sum_pc2)
print("  licence (c) OCBI's own mirror taxonomy: %d of %d catalogued forms are"
      % (n_mirror_named, len(names)))
print("              explicitly named '<X> gespiegelt'.  For the ME claim this")
print("              licence FAILS outright -- see r6_mirror_shape_test.py:")
print("                %s = %s" % (ME_A, name(ME_A)))
print("                %s = %s" % (ME_B, name(ME_B)))
print("              i.e. OCBI names E4B0 the mirror of 'die Zwei' (E47D,")
print("              %s), NOT of E49A." % name("E47D"))

p_term = sum_p2
p_pa_pos = p.get(PA, 0.0)
budget_variant = 9          # rb x rc alternative readings
budget_colpair = len(list(itertools.combinations(range(4), 2)))  # which 2 of 4 are "the sisters"

print()
print("  constraint (3a) the two 4-sign columns end in the SAME exact form : p=%.5f" % p_term)
print("  constraint (3b) their onsets are an admissible ME pair           : p=%.5f (licence b)"
      % sum_pc2)
print("  constraint (5)  the long column has E44D at position 4            : p=%.5f" % p_pa_pos)
for lab, ponset in (("free mirror licence", onset_free), ("OCBI-class licence", sum_pc2)):
    per = p_term * ponset * p_pa_pos
    fam = 1 - (1 - per) ** (budget_variant * budget_colpair)
    print("  per-trial p (%-20s) = %.3e   family-wise over %d variant x column"
          % (lab, per, budget_variant * budget_colpair))
    print("      choices                                 -> p = %.4f" % fam)
print()
print("  Dropping constraint (5) -- which is a separate anchor, not part of the")
print("  two-sisters pattern -- the two-sister pattern alone is:")
for lab, ponset in (("free mirror licence", onset_free), ("OCBI-class licence", sum_pc2)):
    per = p_term * ponset
    fam = 1 - (1 - per) ** (budget_variant * budget_colpair)
    print("      %-22s per-trial %.4f   family-wise %.4f" % (lab, per, fam))

print()
print("=" * 78)
print("K2.  EMPIRICAL: THE SAME TEMPLATE, SEARCHED IN THE DUNAND CORE")
print("=" * 78)
print("  Enumerate every 4-sign window of consecutive, uninterrupted signs in")
print("  off-cylinder material (no wildcard/fracture/gap crossed), then count")
print("  pairs of windows that reproduce the two-sister pattern:")
print("    same exact final sign, different initial signs, initials in one")
print("    grapheme class of the inventory named.")

wins4 = []
for fid, ln, r in rs:
    s = [t["cp"] for t in r]
    for i in range(len(s) - 3):
        wins4.append((fid, ln, i, tuple(s[i:i + 4])))
print("  4-sign windows: %d  (from %d uninterrupted runs)" % (len(wins4), len(rs)))

for syl in syls:
    cm = L.classmap(syl)
    hits = 0
    distinct_terms = collections.Counter()
    for (a, b) in itertools.combinations(range(len(wins4)), 2):
        wa, wb = wins4[a][3], wins4[b][3]
        if wins4[a][0] == wins4[b][0] and abs(wins4[a][2] - wins4[b][2]) < 4 \
                and wins4[a][1] == wins4[b][1]:
            continue            # overlapping windows on one line: not two names
        if wa[3] != wb[3]:
            continue
        if wa[0] == wb[0]:
            continue
        if cm.get(wa[0], "a" + wa[0]) != cm.get(wb[0], "b" + wb[0]):
            continue
        hits += 1
        distinct_terms[wa[3]] += 1
    print("    %-7s  matching window pairs: %5d   distinct shared terminals: %d"
          % (syl["id"], hits, len(distinct_terms)))

print()
print("  Same thing under the FREE mirror licence (initials unconstrained,")
print("  only the exact shared terminal and distinct initials required):")
free_hits = 0
by_term = collections.Counter()
for (a, b) in itertools.combinations(range(len(wins4)), 2):
    wa, wb = wins4[a][3], wins4[b][3]
    if wins4[a][0] == wins4[b][0] and wins4[a][1] == wins4[b][1] \
            and abs(wins4[a][2] - wins4[b][2]) < 4:
        continue
    if wa[3] == wb[3] and wa[0] != wb[0]:
        free_hits += 1
        by_term[wa[3]] += 1
print("    matching window pairs: %d over %d distinct shared terminals"
      % (free_hits, len(by_term)))
print("    most productive terminals:", by_term.most_common(8))

print()
print("  And the full three-string template, requiring in addition a longer")
print("  (>=5 sign) window elsewhere with E44D at its 4th position:")
wins_long = []
for fid, ln, r in rs:
    s = [t["cp"] for t in r]
    for ll in range(5, 9):
        for i in range(len(s) - ll + 1):
            w = tuple(s[i:i + ll])
            if len(w) >= 4 and w[3] == PA:
                wins_long.append((fid, ln, i, w))
print("    long windows with E44D in position 4: %d" % len(wins_long))
print("    => complete templates available in the core corpus (free licence):")
print("       %d two-sister pairs x %d long windows = %d"
      % (free_hits, len(wins_long), free_hits * len(wins_long)))

print()
print("=" * 78)
print("K3.  MONTE CARLO OVER THE SEAL, CHARGING THE VARIANT BUDGET")
print("=" * 78)
print("  Re-draw the seal as 4 columns of the observed lengths (6,4,4,3) with")
print("  signs i.i.d. from off-cylinder frequencies.  For rb and rc draw 3")
print("  alternative readings each, exactly as OCBI offers.  Then ask whether")
print("  ANY admissible choice yields the kernel's pattern.")
forms = list(p.keys())
w = [p[c] for c in forms]
cm = L.classmap(syls[0])


def draw(n):
    return random.choices(forms, weights=w, k=n)


def test(rb_vars, rc_vars, ra, licence):
    for a in rb_vars:
        for b in rc_vars:
            if len(a) != 4 or len(b) != 4:
                continue
            if a[3] != b[3]:
                continue
            if a[0] == b[0]:
                continue
            if licence == "class" and cm.get(a[0], "x" + a[0]) != cm.get(b[0], "y" + b[0]):
                continue
            return True
    return False


TRIALS = 200000
for licence in ("free", "class"):
    hit2 = hit3 = 0
    for _ in range(TRIALS):
        rb_v = [draw(4) for _ in range(3)]
        rc_v = [draw(4) for _ in range(3)]
        ra_ = draw(6)
        ok2 = test(rb_v, rc_v, ra_, licence)
        if ok2:
            hit2 += 1
            if ra_[3] == PA:
                hit3 += 1
    print("  licence=%-6s  P(two-sister pattern found) = %.4f   "
          "P(+ pa in ra position 4) = %.5f"
          % (licence, hit2 / TRIALS, hit3 / TRIALS))
print("  (TRIALS=%d, seed 20261002)" % TRIALS)

print()
print("  SENSITIVITY: 'the expected internal position' for pa is position 4 only")
print("  under one chosen segmentation of Ankhesen-pa-amun (anch-e-sen-pa-AMUN).")
print("  If pa is merely required to be INTERNAL (positions 2..5 of 6), the")
print("  surviving significance degrades:")
for licence in ("free", "class"):
    hit = 0
    for _ in range(TRIALS):
        rb_v = [draw(4) for _ in range(3)]
        rc_v = [draw(4) for _ in range(3)]
        ra_ = draw(6)
        if test(rb_v, rc_v, ra_, licence) and PA in ra_[1:5]:
            hit += 1
    per = hit / TRIALS
    print("    licence=%-6s P(pattern + pa anywhere internal) = %.5f  "
          "family-wise over the 6 ways of picking 2 of 4 columns = %.4f"
          % (licence, per, 1 - (1 - per) ** budget_colpair))

print()
print("=" * 78)
print("K4.  THE NAME SIDE OF THE BUDGET")
print("=" * 78)
print("  Akhenaten and Nefertiti had SIX daughters: Meritaten, Meketaten,")
print("  Ankhesenpaaten, Neferneferuaten-tasherit, Neferneferure, Setepenre.")
print("  Three of the six end in -aten; two of those three begin with 'Me-'.")
print("  So the two facts the kernel treats as constraints (3) -- 'both short")
print("  names begin with the same syllable' and 'both end in the same divine")
print("  name' -- are properties of EGYPTIAN ONOMASTICS, fixed before any")
print("  Byblos sign is looked at.  They constrain the script side by exactly")
print("  one bit each: 'the two 4-sign columns must agree in position 1 (up to")
print("  a declarable mirror) and in position 4'.  Position 1 agreement is NOT")
print("  observed: the two onsets are different codepoints (E49A vs E4B0) and")
print("  are reconciled by an asserted mirror relation.  The only unpurchased")
print("  observation left is the identity of position 4 -- one coincidence of")
print("  p = %.4f per trial, against the budget computed in K1." % sum_p2)
