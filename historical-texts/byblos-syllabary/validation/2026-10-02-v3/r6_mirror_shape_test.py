#!/usr/bin/env python3
"""
REFUTER ATTACK 3 -- IS THE 'me' ANCHOR'S MIRROR CLAIM TRUE?

The whole ME anchor rests on one graphical assertion (Maeder, via Colless 2019:
"The sign in the shape of a '2' would be me ... The fact that one of the
'2'-shaped signs is mirrored fits the Egyptian names which also are mirrored"),
restated in PARTIAL_BIGRAPH_KERNEL.md section 3 as "Maeder treats these as
mirrored/allographic forms".  The two forms are E49A (rb) and E4B0 (rc).

That is a testable claim about two vector outlines, and the OCBI glyph outlines
are available.  Two independent checks:

  P1  OCBI's own taxonomy: which form does OCBI itself name as the mirror of
      which?
  P2  geometry: mirror E49A about a vertical axis and measure its distance to
      E4B0, calibrated against (i) OCBI's explicitly named mirror pairs as
      positive controls and (ii) random pairs as negative controls.

Glyph outlines come from validation/2026-09-25/glyphnames.json, which carries
the OCBI font's name and SVG path 'd' for 239 forms.  Nothing here depends on
the Hub write-ups.
"""
import re, json, math, random, itertools, collections
import lib_ocbi as L

random.seed(20261002)
GN = L.glyphnames()

NUM = re.compile(r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?')
CMD = re.compile(r'([MmLlHhVvCcSsQqTtAaZz])')


def points(d):
    """Walk an SVG path and return the absolute on-curve + control points."""
    toks = [t for t in CMD.split(d) if t.strip()]
    pts, cur, start, cmd = [], (0.0, 0.0), (0.0, 0.0), None
    i = 0
    while i < len(toks):
        t = toks[i]
        if CMD.fullmatch(t):
            cmd = t
            i += 1
            if cmd in "Zz":
                cur = start
                continue
            nums = [float(x) for x in NUM.findall(toks[i])] if i < len(toks) else []
            i += 1
        else:
            nums = [float(x) for x in NUM.findall(t)]
            i += 1
        if not nums:
            continue
        rel = cmd.islower()
        k = cmd.upper()
        step = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7}[k]
        j = 0
        first = True
        while j + step <= len(nums):
            ch = nums[j:j + step]
            if k in ("M", "L", "T"):
                nx, ny = ch[0], ch[1]
                if rel:
                    nx, ny = cur[0] + nx, cur[1] + ny
                cur = (nx, ny)
                pts.append(cur)
                if k == "M" and first:
                    start = cur
            elif k == "H":
                nx = ch[0] + (cur[0] if rel else 0)
                cur = (nx, cur[1]); pts.append(cur)
            elif k == "V":
                ny = ch[0] + (cur[1] if rel else 0)
                cur = (cur[0], ny); pts.append(cur)
            elif k in ("C", "S", "Q"):
                coords = []
                for a in range(0, step, 2):
                    x, y = ch[a], ch[a + 1]
                    if rel:
                        x, y = cur[0] + x, cur[1] + y
                    coords.append((x, y))
                pts.extend(coords)
                cur = coords[-1]
            elif k == "A":
                x, y = ch[5], ch[6]
                if rel:
                    x, y = cur[0] + x, cur[1] + y
                cur = (x, y); pts.append(cur)
            j += step
            first = False
            if k == "M":
                k = "L"      # implicit lineto after a moveto
    return pts


def norm(pts, mirror=False):
    if not pts:
        return []
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    if mirror:
        xs = [-x for x in xs]
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    xs = [x - cx for x in xs]; ys = [y - cy for y in ys]
    s = math.sqrt(sum(x * x + y * y for x, y in zip(xs, ys)) / len(xs)) or 1.0
    return [(x / s, y / s) for x, y in zip(xs, ys)]


def chamfer(A, B):
    if not A or not B:
        return float("nan")

    def one(P, Q):
        tot = 0.0
        for px, py in P:
            best = min((px - qx) ** 2 + (py - qy) ** 2 for qx, qy in Q)
            tot += math.sqrt(best)
        return tot / len(P)
    return 0.5 * (one(A, B) + one(B, A))


CLOUD = {}
for cp, v in GN.items():
    try:
        CLOUD[cp] = norm(points(v["d"]))
    except Exception:
        pass
MIR = {}
for cp, v in GN.items():
    try:
        MIR[cp] = norm(points(v["d"]), mirror=True)
    except Exception:
        pass


def core(nm):
    s = nm.split("   ")[-1] if "   " in nm else nm
    return re.sub(r'^\s*[a-zA-Z\'Α-ω]+\s+[IVXL\']+\s+\d+\s+', '', s).strip()


names = {cp: v["name"] for cp, v in GN.items()}
print("=" * 78)
print("P1.  OCBI'S OWN MIRROR TAXONOMY")
print("=" * 78)
pairs = []
bases = {}
for cp, n in names.items():
    c = core(n).lower()
    bases.setdefault(c, []).append(cp)
for cp, n in names.items():
    c = core(n).lower()
    if c.endswith("gespiegelt"):
        b = c[:-len("gespiegelt")].strip()
        cands = []
        for c2, lst in bases.items():
            if c2 == b or c2.replace("die ", "").replace("das ", "").replace("der ", "") == \
               b.replace("die ", "").replace("das ", "").replace("der ", ""):
                cands += [x for x in lst if x != cp]
        if cands:
            pairs.append((cp, cands[0], b))
print("  OCBI forms explicitly named '<X> gespiegelt' with a locatable base form:")
for a, b, lab in sorted(pairs):
    print("    %-6s %-42s  <-> base %-6s %s" % (a, names[a], b, names[b]))
print()
print("  The two 'me' forms:")
for c in ("E49A", "E4B0", "E400", "E47D"):
    print("    %-6s %s" % (c, names.get(c)))
print("  E4B0 is named the mirror of 'die Zwei'.  The only form OCBI names")
print("  'die Zwei' is E47D.  E49A is named a variant ('gerundet') of 'das Z'")
print("  (E400).  On OCBI's own taxonomy E49A and E4B0 are variants of two")
print("  DIFFERENT base signs, and nothing in the source calls them mirrors of")
print("  each other.")

print()
print("=" * 78)
print("P2.  GEOMETRY: CALIBRATED MIRROR TEST")
print("=" * 78)
pos = []
for a, b, lab in pairs:
    if a in CLOUD and b in MIR:
        pos.append((chamfer(CLOUD[a], MIR[b]), a, b, lab))
pos.sort()
print("  positive controls -- distance between each OCBI-declared mirror pair")
print("  after mirroring one of them (lower = better match):")
for d, a, b, lab in pos:
    print("    %.4f   %-6s vs mirror(%-6s)   %s" % (d, a, b, lab))
import statistics
if pos:
    ds = [x[0] for x in pos]
    print("    positive-control mirror distance: median %.4f  max %.4f" %
          (statistics.median(ds), max(ds)))

cps = [c for c in CLOUD if CLOUD[c]]
neg = []
for _ in range(4000):
    a, b = random.sample(cps, 2)
    neg.append(chamfer(CLOUD[a], MIR[b]))
neg.sort()


def pctile(v, arr):
    import bisect
    return 100.0 * bisect.bisect_left(arr, v) / len(arr)


print()
print("  negative controls -- 4000 random form pairs, same statistic:")
print("    median %.4f   5th pct %.4f   1st pct %.4f"
      % (statistics.median(neg), neg[int(.05 * len(neg))], neg[int(.01 * len(neg))]))

print()
print("  THE CLAIM UNDER TEST:")
tests = [("E4B0 vs mirror(E49A)   [the kernel's ME allograph claim]", "E4B0", "E49A"),
         ("E49A vs mirror(E4B0)   [same, other orientation]", "E49A", "E4B0"),
         ("E4B0 vs mirror(E47D)   [OCBI's own naming: 'die Zwei gespiegelt']", "E4B0", "E47D"),
         ("E49A vs mirror(E400)   [OCBI's own naming: 'das Z gerundet' vs 'das Z']", "E49A", "E400"),
         ("E49A vs E400 unmirrored [same-family control]", "E49A", None),
         ("E4B0 vs E47D unmirrored [same-family control]", "E4B0", None)]
for lab, a, b in tests:
    if b is None:
        base = {"E49A": "E400", "E4B0": "E47D"}[a]
        d = chamfer(CLOUD[a], CLOUD[base])
    else:
        d = chamfer(CLOUD[a], MIR[b])
    print("    %-58s d=%.4f   better than %.1f%% of random pairs"
          % (lab, d, 100 - pctile(d, neg)))
print()
print("  Also: is the pair even the same size?  OCBI path lengths ('plen'):")
for c in ("E49A", "E4B0", "E400", "E47D"):
    print("    %-6s plen=%-6s %s" % (c, GN[c]["plen"], names[c]))

print()
print("=" * 78)
print("P3.  SAME TEST, BUT GIVING THE CLAIM ITS BEST SHOT")
print("=" * 78)
print("  P2 fixed the mirror axis to vertical.  Here the mirrored shape is also")
print("  rotated to whatever angle minimises the distance (5-degree grid), and")
print("  isotropic scale is already normalised.  Both controls get the same")
print("  treatment, so the comparison stays fair.")


def rot(pts, th):
    c, s = math.cos(th), math.sin(th)
    return [(x * c - y * s, x * s + y * c) for x, y in pts]


def best_mirror(a, b):
    A = CLOUD[a]
    best = float("inf")
    for deg in range(0, 360, 5):
        d = chamfer(A, rot(MIR[b], math.radians(deg)))
        best = min(best, d)
    return best


posb = sorted((best_mirror(a, b), a, b, lab) for a, b, lab in pairs if a in CLOUD and b in MIR)
print("  positive controls, best-rotation mirror distance:")
for d, a, b, lab in posb:
    print("    %.4f   %-6s vs best-rotated mirror(%-6s)  %s" % (d, a, b, lab))
negb = sorted(best_mirror(a, b) for a, b in
              (random.sample(cps, 2) for _ in range(400)))
print("  negative controls (400 random pairs): median %.4f  5th pct %.4f  1st pct %.4f"
      % (statistics.median(negb), negb[int(.05 * len(negb))], negb[int(.01 * len(negb))]))
d = best_mirror("E4B0", "E49A")
import bisect
print()
print("  CLAIM  E4B0 vs best-rotated mirror(E49A):  d=%.4f" % d)
print("         better than %.1f%% of random pairs; %d of %d genuine OCBI mirror"
      % (100 - 100.0 * bisect.bisect_left(negb, d) / len(negb),
         sum(1 for x in posb if x[0] < d), len(posb)))
print("         pairs score better.")
print("  CLAIM  E4B0 vs best-rotated mirror(E47D) [OCBI's own pairing]: d=%.4f"
      % best_mirror("E4B0", "E47D"))
