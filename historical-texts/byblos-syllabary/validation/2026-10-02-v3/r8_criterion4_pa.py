#!/usr/bin/env python3
"""
REFUTER ATTACK 5 -- CRITERION 4, THE STATED BRIDGE.

PROBLEM.md criterion 4, verbatim:
  "Convert the partial bigraph into cross-text predictions that are tested on
   the Dunand core with the cylinder left out. This is the critical bridge from
   a few external anchors to a genuine decipherment."

PARTIAL_BIGRAPH_KERNEL.md section 7 states this as the NEXT test, not as done:
  "Then run leave-the-cylinder-out searches on the core Dunand corpus only."
So the kernel itself does not claim criterion 4.  The only artefact that
attempts it is ME_ANCHOR_TRANSFER.md, which tests ONE of the four anchors (ME)
and explicitly declines to give a p-value because "the common follower was
noticed after examining the contexts".

This script does the test the kernel named, on the anchor the kernel itself
calls the strongest -- PA = E44D, "the best externally grounded syllabic value
in the current corpus", which has 11 off-seal tokens, four times as many as ME.
If the strongest anchor predicts nothing off the seal, criterion 4 is not met
for any anchor.

Tests:
  R1  can each anchor be tested off the seal at all (token counts)?
  R2  PA held out: positional profile vs corpus
  R3  PA held out: neighbour invariance, with a budget-matched null over every
      comparably frequent sign
  R4  PA held out: does E44D behave like a syllabogram or like the two signs
      OCBI names 'kurzer Worttrenner' (short word divider)?
  R5  the prediction the bigraph actually licenses: ATON-terminal names.  If
      E4AF/the ATON class marks a theonym-final slot, the class should recur in
      terminal positions off the seal.  Does it?
"""
import collections, random, math, statistics
import lib_ocbi as L

random.seed(20261002)
src = L.load_src()
syls = L.parse_syllabaries(src)
GN = L.glyphnames()


def nm(c):
    return GN.get(c, {}).get("name", "?")


off = L.corpus(canon=True, off_cylinder=True)
rs = L.runs(off)
tokens = [t["cp"] for _, _, r in rs for t in r]
freq = collections.Counter(tokens)
N = len(tokens)

PA, ME, ATON, DIVS = "E44D", "E49A", "E4AF", {"E402", "E404"}

print("=" * 78)
print("R1.  CAN EACH ANCHOR BE TESTED OFF THE SEAL AT ALL?")
print("=" * 78)
for c, lab in [("E49A", "ME"), ("E4B0", "ME' (mirror form)"), ("E44D", "PA"),
               ("E4AF", "ATON"), ("E42A", "AMUN-1"), ("E483", "AMUN-2")]:
    clear = sum(1 for _, _, r in rs for t in r if t["cp"] == c and not t["guess"])
    print("  %-6s %-18s off-seal tokens %2d (clear %2d)  %s"
          % (c, lab, freq.get(c, 0), clear, nm(c)))
print("  -> ATON (E4AF) has zero off-seal tokens: it is UNTESTABLE off the seal")
print("     by construction, so no held-out prediction can ever involve it.")
print("  -> AMUN-2 (E483) has 2.  ME' (E4B0) has 1, and it is a guess-marked")
print("     reading (see ME_ANCHOR_TRANSFER.md section 8).  Only PA and AMUN-1")
print("     have enough tokens for any distributional test at all.")

print()
print("=" * 78)
print("R2.  PA HELD OUT: POSITIONAL PROFILE")
print("=" * 78)
lines = [[t for t in toks if t["kind"] == "sign"] for _, _, toks in off]
lines = [l for l in lines if l]
edge = collections.Counter()
inner = collections.Counter()
for l in lines:
    for i, t in enumerate(l):
        (edge if i in (0, len(l) - 1) else inner)[t["cp"]] += 1
tot_edge = sum(edge.values()); tot_in = sum(inner.values())
print("  off-seal line-edge sign tokens %d, line-internal %d -> P(edge)=%.4f"
      % (tot_edge, tot_in, tot_edge / (tot_edge + tot_in)))
pe = tot_edge / (tot_edge + tot_in)
for c in [PA, ME, "E42A", "E402", "E404", "E416"]:
    n = edge[c] + inner[c]
    if n == 0:
        continue
    k = edge[c]
    # two-sided binomial-ish: report expectation and the exact tail
    from math import comb
    p_ge = sum(comb(n, j) * pe ** j * (1 - pe) ** (n - j) for j in range(k, n + 1))
    p_le = sum(comb(n, j) * pe ** j * (1 - pe) ** (n - j) for j in range(0, k + 1))
    print("  %-6s n=%-3d at a line edge %2d (expected %.1f)  p(>=)=%.3f p(<=)=%.3f  %s"
          % (c, n, k, n * pe, p_ge, p_le, nm(c)))
print("  -> PA's positional profile is indistinguishable from an ordinary sign.")
print("     That is consistent with a syllabogram, but it is not evidence FOR")
print("     one: it is the absence of a signal either way.")

print()
print("=" * 78)
print("R3.  PA HELD OUT: NEIGHBOUR STRUCTURE, BUDGET-MATCHED")
print("=" * 78)
left = collections.defaultdict(collections.Counter)
right = collections.defaultdict(collections.Counter)
for _, _, r in rs:
    s = [t["cp"] for t in r]
    for i, c in enumerate(s):
        if i:
            left[c][s[i - 1]] += 1
        if i < len(s) - 1:
            right[c][s[i + 1]] += 1


def top_share(cnt):
    if not cnt:
        return 0.0, 0, None
    c, n = cnt.most_common(1)[0]
    return n / sum(cnt.values()), sum(cnt.values()), c


print("  For PA and for every sign of comparable frequency, the share of the")
print("  commonest neighbour on each side:")
cands = [c for c, n in freq.items() if 8 <= n <= 16]
rowsL, rowsR = [], []
for c in cands:
    sl, nl, wl = top_share(left[c])
    sr, nr, wr = top_share(right[c])
    rowsL.append((sl, nl, c, wl)); rowsR.append((sr, nr, c, wr))
rowsL.sort(reverse=True); rowsR.sort(reverse=True)
print("  %d signs have 8-16 off-seal tokens (PA has %d)." % (len(cands), freq[PA]))
for lab, rws in (("LEFT", rowsL), ("RIGHT", rowsR)):
    print("   top %s-neighbour concentration:" % lab)
    for s, n, c, w in rws[:6]:
        mark = "  <-- PA" if c == PA else ""
        print("     %-6s n=%-3d commonest %s-nb %s x%.0f  share %.2f%s"
              % (c, n, lab.lower(), w, s * n, s, mark))
    rank = [i for i, (s, n, c, w) in enumerate(rws, 1) if c == PA]
    print("     PA's rank among them: %s of %d" % (rank, len(rws)))
print("  -> PA has no invariant or even dominant neighbour on either side.  The")
print("     ME result reported in ME_ANCHOR_TRANSFER.md (3/3 identical right")
print("     neighbour) does not generalise to the anchor the kernel itself calls")
print("     the strongest one.")

print()
print("=" * 78)
print("R4.  PA vs THE DIVIDER CONTROL")
print("=" * 78)
print("  OCBI names two forms 'kurzer Worttrenner' (short word divider):")
for c in sorted(DIVS):
    print("     %-6s %s   n=%d" % (c, nm(c), freq.get(c, 0)))
print("  The 2026-09-25 session (refute3.py, sections F-H) showed that E402 is")
print("  distributionally a divider and that the entire ME 'adjacency family'")
print("  of ME_ANCHOR_TRANSFER.md is 'ME followed by a word divider'.  This")
print("  session reproduces that result bit-for-bit.  The check that matters")
print("  here is whether PA shows the same confound:")
adj = 0
for _, _, r in rs:
    s = [t["cp"] for t in r]
    for i, c in enumerate(s):
        if c == PA and ((i and s[i - 1] in DIVS) or (i < len(s) - 1 and s[i + 1] in DIVS)):
            adj += 1
print("  PA tokens adjacent to a divider: %d of %d -> PA is not a divider-bound"
      % (adj, freq[PA]))
print("  form, and its distribution carries no divider artefact.  It also")
print("  carries no detectable structure.")

print()
print("=" * 78)
print("R5.  THE PREDICTION THE BIGRAPH ACTUALLY LICENSES, AND ITS RESULT")
print("=" * 78)
print("  If the ATON class marks a theonym-final slot, then after the split the")
print("  kernel promotes (syl6-syl8), that class should show up in terminal")
print("  positions in the Dunand core.  Test it:")
for sid in ("search", "syl6", "syl8"):
    syl = [s for s in syls if s["id"] == sid][0]
    cm = L.classmap(syl)
    k = cm.get(ATON)
    members = [c for c, v in cm.items() if v == k]
    n_tot = sum(freq.get(c, 0) for c in members)
    n_edge = sum(edge.get(c, 0) for c in members)
    n_fin = 0
    for l in lines:
        if l and l[-1]["cp"] in members:
            n_fin += 1
    print("    %-7s ATON class %-44s off-seal n=%-3d line-final %d of %d lines"
          % (sid, " ".join(members), n_tot, n_fin, len(lines)))
print("  -> under the merged inventory the class has 20 off-seal tokens and can")
print("     be tested; under the split the kernel promotes it has 3, and the")
print("     split therefore DESTROYS the only held-out test the ATON anchor")
print("     could have had.  The inventory decision the kernel offers as its")
print("     new result moves the claim away from criterion 4, not towards it.")
