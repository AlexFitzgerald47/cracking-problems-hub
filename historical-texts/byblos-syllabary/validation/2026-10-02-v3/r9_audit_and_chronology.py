#!/usr/bin/env python3
"""
REFUTER ATTACK 6 -- (a) does the claim set contain the artefacts the
pre-registered criteria require, and (b) is PALIMPSEST_CHRONOLOGY.md falsifiable
in practice as well as in principle?

(a) is a mechanical audit of the claimant's own files -- grep, not opinion.
(b) attempts the kill-test that PALIMPSEST_CHRONOLOGY.md section 5 nominates:
    "Classify signs without assigning phonetic values into (i) core fourteen
     texts, (ii) Linear Pseudo-Hieroglyphic, and (iii) secure palimpsest
     traces.  Then compare only diagnostic morphology."
"""
import os, re, json, collections, statistics
import lib_ocbi as L

HERE = os.path.dirname(os.path.abspath(__file__))
HUB = os.path.abspath(os.path.join(HERE, "..", ".."))
FILES = ["PROBLEM.md", "PARTIAL_BIGRAPH_KERNEL.md", "PALIMPSEST_CHRONOLOGY.md",
         "ME_ANCHOR_TRANSFER.md", "PROGRESS.md", "HANDOVER.md"]

print("=" * 78)
print("S1.  DOES A POWER ANALYSIS EXIST ANYWHERE IN THE CLAIM SET?")
print("=" * 78)
print("  criterion 1 verbatim: 'A reproducible structural audit: sign inventory")
print("  with documented variant-merging decisions, positional statistics, and")
print("  an explicit power analysis stating what a corpus of this size can and")
print("  cannot support.'")
pat = {
    "power analys": r'power analys\w*',
    "null model / permutation / randomis": r'null model|permut\w*|randomis\w*|randomiz\w*|monte[- ]carlo',
    "p-value / significance": r'p[- ]value|significan\w*|chance level',
    "positional statistics": r'positional statistic\w*|position\w* distribution',
    "sign inventory table": r'sign inventory',
}
for f in FILES:
    txt = open(os.path.join(HUB, f), encoding="utf-8").read()
    hits = {k: len(re.findall(v, txt, re.I)) for k, v in pat.items()}
    print("  %-28s %s" % (f, "  ".join("%s=%d" % (k.split()[0], v) for k, v in hits.items())))
print()
for f in FILES:
    txt = open(os.path.join(HUB, f), encoding="utf-8").read()
    for m in re.finditer(r'[^\n.]*power analys[^\n.]*', txt, re.I):
        print("  %-26s : %s" % (f, m.group().strip()))
print("  -> the phrase appears only where the criterion or an old recommendation")
print("     states that one SHOULD be run.  No file carries a null model, a")
print("     permutation test, a p-value, or a stated detection ceiling.")
print("     Criterion 1's power-analysis component is ABSENT from the claim set.")
print("     (The arithmetic is now in r4_power_null.py in this directory, and it")
print("      does not favour the claim.)")

print()
print("=" * 78)
print("S2.  WHICH CRITERIA DOES THE CLAIM SET EVEN ASSERT?")
print("=" * 78)
for f in ["PARTIAL_BIGRAPH_KERNEL.md"]:
    txt = open(os.path.join(HUB, f), encoding="utf-8").read()
    i = txt.find("## 7. The next frontier test")
    j = txt.find("## Verdict")
    print("  PARTIAL_BIGRAPH_KERNEL.md section 7, in its own words:")
    for line in txt[i:j].split("\n"):
        line = re.sub(r'[-]', lambda m: "<%04X>" % ord(m.group()), line).strip()
        if line.startswith("Then run") or line.startswith("If the anchors") or \
           line.startswith("The correct next move") or line.startswith("The important point"):
            print("    " + line)
print("  -> the kernel places the criterion-4 test in the FUTURE.  It does not")
print("     claim criterion 4, and criterion 4 is the criterion PROBLEM.md calls")
print("     'the critical bridge'.")

print()
print("=" * 78)
print("S3.  CITATION INTEGRITY ON THE ANCHORS' PRIMARY SOURCE")
print("=" * 78)
for f in FILES:
    txt = open(os.path.join(HUB, f), encoding="utf-8").read()
    for m in re.finditer(r'[^\n]*366580046[^\n]*', txt):
        print("  %-26s : %s" % (f, m.group().strip()[:150]))
print("  checked 2026-10-02: ResearchGate publication 366580046 is Michael")
print("  Maeder, 'Detecting word boundaries in an undeciphered script: The")
print("  Byblos syllabary', BAF-Online (Berner Altorientalisches Forum), also at")
print("  https://bop.unibe.ch/baf/article/view/7186 -- NOT 'Zwei")
print("  Lautwertvorschlaege zum Byblos-Syllabar: me und pa'.  The Hub files")
print("  attach that RG id to the me/pa paper in three places.  The me/pa paper")
print("  (Ugarit-Forschungen 52) is therefore cited but not located, and nothing")
print("  in the claim set quotes it directly; the operative wording of the")
print("  mirror/allograph argument reaches the Hub only through Schmutz & Maeder")
print("  2024 and GEAS's 2021 news page.")
print("  (Note the irony: the paper actually at that id is Maeder's WORD-BOUNDARY")
print("  paper, which is the one bearing on whether E402 is a divider.)")

print()
print("=" * 78)
print("S4.  CHRONOLOGY: IS THE NOMINATED KILL-TEST RUNNABLE?")
print("=" * 78)
src = L.load_src()
frags = L.parse_fragments(src)
print("  PALIMPSEST_CHRONOLOGY.md section 5 requires every sign to be labelled")
print("  (i) core, (ii) Linear Pseudo-Hieroglyphic, (iii) secure palimpsest.")
print("  The machine-readable corpus carries these metadata fields only:")
keys = set()
for m in re.finditer(r'\{ id = "[^"]*", source = "([^"]*)", group = "([^"]*)", dir = (\w+)', src):
    keys.add(m.groups()[0:2])
print("    (source, group) values present: %s" % sorted(keys))
dirs = collections.Counter(f["dir"] for f in frags)
print("    dir values: %s" % dict(dirs))
print("  There is NO period, phase, medium, palimpsest or 'linear' field, and no")
print("  witness is labelled Linear Pseudo-Hieroglyphic.  The nominated kill-test")
print("  cannot be run from the only machine-readable corpus; it needs a phase")
print("  classification that does not exist and that the session did not build.")
print("  Status: INABILITY TO ASSESS, not refutation.")

print()
print("  Exploratory substitute (NOT the nominated test): OCBI's glyph outlines")
print("  carry a path-length field, a crude proxy for graphic complexity.  If a")
print("  'linearized terminal phase' is present in this corpus at all, some")
print("  witness should be enriched in simple forms.")
GN = L.glyphnames()
plen = {c: v["plen"] for c, v in GN.items()}


def witness(fid):
    b = fid.split(" (")[0].strip()
    return "r (seal)" if b in ("ra", "rb", "rc", "rd") else b


w = collections.defaultdict(list)
for f in frags:
    if f["id"] in L.CANON_DROP and witness(f["id"]) != "r (seal)":
        continue
    for ln in f["lines"]:
        for t in ln:
            if t["kind"] == "sign" and t["cp"] in plen:
                w[witness(f["id"])].append(plen[t["cp"]])
allv = [x for v in w.values() for x in v]
print("    corpus mean glyph path-length %.0f (median %.0f, n=%d)"
      % (statistics.mean(allv), statistics.median(allv), len(allv)))
rows = sorted((statistics.mean(v), len(v), k) for k, v in w.items() if len(v) >= 10)
print("    per-witness mean complexity (>=10 tokens), simplest first:")
for mu, n, k in rows:
    print("      %-12s n=%-4d mean %.0f" % (k, n, mu))
print("    spread: min %.0f  max %.0f  ratio %.2f" % (rows[0][0], rows[-1][0],
                                                      rows[-1][0] / rows[0][0]))
print("  -> the witnesses do not separate into a simple and a complex population;")
print("     means lie on a continuum with a ~%.1fx spread and no gap.  This is"
      % (rows[-1][0] / rows[0][0]))
print("     consistent with the two-phase model AND with a single-phase model, so")
print("     it discriminates nothing.  The model as written makes no prediction")
print("     that the available machine-readable evidence could falsify.")

print()
print("=" * 78)
print("S5.  THE LOGICAL SHAPE OF THE CHRONOLOGY ARGUMENT")
print("=" * 78)
for line in [
    "PALIMPSEST_CHRONOLOGY.md section 3 argues: IF the conventional/DEAPS royal",
    "chronology is approximately right, THEN a Byblos-script layer beneath KAI 3",
    "or KAI 4 predates the tenth century, so a ca. 900 invention is impossible.",
    "",
    "But the proposition 'the early royal Byblian Phoenician inscriptions are",
    "tenth-century' is precisely what Sass (2005) disputes and Rollston (2008)",
    "and Lemaire (2006) defend.  Sass's ca. 900 invention is a package that",
    "includes lowering that series.  Conditioning on the series being tenth-",
    "century therefore assumes the contested premise; the document's own text",
    "concedes as much ('None of those moves is individually impossible.  The",
    "problem is cumulative') and then rests on parsimony rather than on a test.",
    "",
    "That is a legitimate and well-argued position in a palaeographic dispute.",
    "It is not a falsification of Sass, and the document's 'moderate confidence'",
    "grading is honest about it.  What it is NOT is new evidence: every element",
    "of the chain (DEAPS dates, Sheshonq/Osorkon monuments, the Yehimilk-Elibaal",
    "genealogy, Vita & Zamora's reinspection) is cited literature, assembled",
    "rather than tested.  Criterion 3 asks for 'progress on the dating question",
    "by systematically separating core, linear/palimpsest and later comparanda'.",
    "The separation is PROPOSED here and nowhere performed on the signs.",
]:
    print("  " + line)
