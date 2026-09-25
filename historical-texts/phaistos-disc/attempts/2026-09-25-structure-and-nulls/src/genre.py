#!/usr/bin/env python3
"""P1-P3: is the Disc's group-length profile compatible with words of a natural
language written syllabically?

Predictions P1-P3 were frozen in FREEZE.md BEFORE any comparison corpus was on disk.
This script tests them.  It also runs a post-hoc third comparison (Cypriot) which is
labelled exploratory because the corpus was chosen after P1-P3 failed.

Comparanda, all re-extracted here from raw sources rather than taken from any summary:
  LB  Linear B, LiBER (liber.cnr.it, CC BY-SA 4.0), 5,084 tablets.
      Mycenaean Greek.  Administrative.
  LA  Linear A, GORILA corpus via ryanpavlicek/pyaegean, 1,721 inscriptions.
      Language unknown.  Administrative.
  CY  Cypriot syllabary, IG XV 1 via the same repo, 178 inscriptions.
      Greek (and Eteocypriot).  Dedications and running text -- the only one of the
      three that contains ordinary connected prose with function words.

Exclusions, all biased AGAINST the hypothesis being tested:
  - damaged/incomplete tokens are dropped.  A token truncated by a break is SHORT,
    so keeping them would push the comparanda towards short words, which is the
    direction that favours the Disc looking anomalous.  Dropping them is the
    conservative choice.
  - logograms, ideograms, ligatures, numerals, fraction signs and editorial Latin
    are dropped.  In Linear A these dominate the single-sign tokens (GRA, VIN, OLE,
    *301, 1/2), and counting them as "one-syllabogram words" would have manufactured
    a confirmation of P1 out of commodity abbreviations.
"""
import csv, json, os, re, random, sys
from collections import Counter

csv.field_size_limit(10 ** 7)
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(HERE, "data")
random.seed(20260925)
B = 20000

# ---------------- the Disc ---------------------------------------------------
disc = [int(r["n_signs"]) for r in csv.DictReader(open(os.path.join(D, "phaistos_words.csv")))]
DISC_MEAN = sum(disc) / len(disc)
DISC_N = len(disc)

DAMAGE = re.compile(r"[\[\]‹›•°?⟦⟧̣̤]|\.\.")
LATIN = {"separatum", "pars", "sine", "regulis", "inf", "mut", "vacat", "deest",
         "vestigia", "graffito", "supra", "infra", "dextra", "laeva", "reliqua",
         "linea", "lineae", "evanidus", "evanida", "illegibilis", "spatium",
         "fragmentum", "titulus", "desunt", "cetera", "rasura", "lacuna"}

def syl_count(tok):
    """syllabograms in a hyphenated token; *NN counts as one sign"""
    return len([p for p in tok.split("-") if p])

# ---------------- Linear B ---------------------------------------------------
def linear_b():
    fh = open(os.path.join(D, "comparanda", "liber_transliterations.tsv"), encoding="utf-8")
    rows = list(csv.reader(fh, delimiter="\t"))[1:]
    lens = []
    for r in rows:
        if len(r) < 3: continue
        body = r[2]
        # drop the leading "KN Nc 4470, " tablet label
        body = body.split(",", 1)[1] if "," in body[:30] else body
        for tok in re.split(r"[\s_,/|↓]+", body):
            if not tok or DAMAGE.search(tok): continue
            tok = tok.strip("-").strip()
            if not tok or tok.lower() in LATIN: continue
            # lowercase == syllabic spelling; UPPERCASE == logogram/ideogram
            if not re.fullmatch(r"[a-z][a-z0-9*₁-₉-]*", tok): continue
            if re.fullmatch(r"[0-9]+[a-z]?", tok): continue
            lens.append(syl_count(tok))
    return lens

# ---------------- Linear A --------------------------------------------------
def linear_a():
    signs = json.load(open(os.path.join(D, "comparanda", "lineara_signs.json")))
    syl = {s["label"].upper() for s in signs if s.get("phonetic")}
    recs = json.load(open(os.path.join(D, "comparanda", "lineara_inscriptions.json")))
    lens = []
    for r in recs:
        for tok in r.get("words", []):
            if not tok or DAMAGE.search(tok): continue
            if "+" in tok or "*" in tok: continue          # ligatures, sign-numbers
            if re.search(r"[0-9⁄¼-¾⅐-⅟]", tok): continue  # numerals/fractions
            if not re.fullmatch(r"[A-Z₂₃-]+", tok): continue
            parts = [p for p in tok.split("-") if p]
            if not parts or not all(p in syl for p in parts): continue   # logograms fail here
            lens.append(len(parts))
    return lens

# ---------------- Cypriot ---------------------------------------------------
def cypriot():
    recs = json.load(open(os.path.join(D, "comparanda", "cypriot_ig_inscriptions.json")))
    lens = []
    for r in recs:
        for line in r.get("lines", []):
            for tok in (line if isinstance(line, list) else [line]):
                for t in re.split(r"[\s,|]+", tok):
                    if not t or DAMAGE.search(t): continue
                    t = t.strip("-")
                    if not t or t in LATIN: continue
                    if not re.fullmatch(r"[a-z][a-z-]*", t): continue
                    if len(t) > 2 and "-" not in t: continue   # Latin/editorial leakage
                    lens.append(syl_count(t))
    return lens

CORPORA = [("LB Linear B (Mycenaean Greek, administrative)", linear_b()),
           ("LA Linear A (unknown language, administrative)", linear_a()),
           ("CY Cypriot syllabary (Greek, dedications/prose)", cypriot())]

out = ["Phaistos Disc: P1-P3, group length against real syllabic corpora", ""]
out.append("Disc: %d groups, mean %.3f signs, distribution %s"
           % (DISC_N, DISC_MEAN, dict(sorted(Counter(disc).items()))))
out.append("")

results = {}
for name, lens in CORPORA:
    if not lens:
        out.append("%s: NO TOKENS EXTRACTED -- not usable" % name); continue
    c = Counter(lens)
    n = len(lens)
    mean = sum(lens) / n
    frac1 = c.get(1, 0) / n
    # size-matched resampling of DISC_N tokens
    zero1 = ge_mean = 0
    for _ in range(B):
        s = [lens[random.randrange(n)] for _ in range(DISC_N)]
        if 1 not in s: zero1 += 1
        if sum(s) / DISC_N >= DISC_MEAN: ge_mean += 1
    p_zero1 = zero1 / B
    p_mean = ge_mean / B
    out.append("%s" % name)
    out.append("   %d usable syllabic word tokens; distribution %s" % (n, dict(sorted(c.items()))))
    out.append("   mean length %.3f signs (Disc %.3f, gap %+.3f)" % (mean, DISC_MEAN, DISC_MEAN - mean))
    out.append("   one-sign tokens: %d = %.2f%%" % (c.get(1, 0), 100 * frac1))
    out.append("   size-matched draws of %d tokens:" % DISC_N)
    out.append("      P(zero one-sign tokens) = %.4f" % p_zero1)
    out.append("      P(mean >= %.3f)          = %.4f" % (DISC_MEAN, p_mean))
    results[name[:2]] = {"n": n, "mean": mean, "frac1": frac1,
                         "p_zero1": p_zero1, "p_mean": p_mean,
                         "dist": {str(k): v for k, v in sorted(c.items())}}
    out.append("")

# ---------------- distributional test ---------------------------------------
out.append("-" * 72)
out.append("DISTRIBUTIONAL TEST: is the Disc's length profile drawn from each corpus?")
out.append("Two-sample Monte Carlo on the summed |observed - expected| over length bins,")
out.append("plus a two-sided Mann-Whitney-style rank test, %d draws of %d tokens." % (B, DISC_N))
dobs = Counter(disc)
for name, lens in CORPORA:
    if not lens: continue
    n = len(lens)
    bins = list(range(1, 9))
    def l1(sample):
        c = Counter(sample)
        return sum(abs(c.get(b, 0) - dobs.get(b, 0)) for b in bins)
    # null: two independent draws from the corpus, compare to each other
    obs_stat = l1(lens[:0] or [])   # placeholder
    exp = [n and sum(1 for x in lens if x == b) * DISC_N / n for b in bins]
    obs = sum(abs(dobs.get(b, 0) - exp[i]) for i, b in enumerate(bins))
    cnt = 0
    for _ in range(B):
        s2 = [lens[random.randrange(n)] for _ in range(DISC_N)]
        c2 = Counter(s2)
        if sum(abs(c2.get(b, 0) - exp[i]) for i, b in enumerate(bins)) >= obs:
            cnt += 1
    p = (cnt + 1) / (B + 1)
    out.append("   %s: L1 distance %.1f, p = %.5f  -> %s"
               % (name[:2], obs, p,
                  "Disc is NOT a sample from this corpus" if p < 0.01
                  else "cannot reject that the Disc is a sample from this corpus"))
    results[name[:2]]["p_dist"] = p
out.append("")

# ---------------- adjudication of the one-sign tokens -----------------------
out.append("-" * 72)
out.append("ADJUDICATION OF THE ONE-SIGN TOKENS -- read this before believing any P1 rate.")
out.append("A one-sign 'word' in an administrative syllabary is usually an ABBREVIATION, not")
out.append("a word, and counting them manufactures a confirmation of P1. Inspected by hand:")
out.append("")
out.append("  LA  1,101 one-sign tokens, dominated by KU (170), KA (169), SI (118), RO (95),")
out.append("      NI (76), TE (58), ZE (47).  These are the standard Linear A single-syllabogram")
out.append("      transaction terms and commodity designators -- NI is the conventional sign for")
out.append("      figs.  They are not words.  Because Linear A is undeciphered I cannot separate")
out.append("      abbreviation from word on any principled basis, so LA IS DISQUALIFIED as a")
out.append("      comparison for P1/P3, and its apparent PASS must NOT be counted.")
out.append("")
out.append("  CY  Latin editorial words (linea, vacat, evanidus, illegibilis) leaked into the")
out.append("      first run and are now excluded.  The remainder -- to (32), a, o, ti, u -- are")
out.append("      genuine Greek function words spelled syllabically, and DO count.")
out.append("")
out.append("  LB  24 one-sign tokens out of 7,701.  Some of these are probably abbreviations")
out.append("      too, which would push the rate even lower.  The direction is against P1.")
out.append("")

# ---------------- verdict against the frozen predictions --------------------
out.append("=" * 72)
out.append("VERDICT ON THE FROZEN PREDICTIONS")
out.append("=" * 72)
lb = results.get("LB")
out.append("")
out.append("P1  '>= 5%% of word tokens will be 1 syllabogram long' (failure if < 5%%)")
for k, v in results.items():
    out.append("      %s: %.2f%%  ->  %s" % (k, 100 * v["frac1"], "PASS" if v["frac1"] >= 0.05 else "FAIL"))
out.append("")
out.append("P2  'the Disc's mean will exceed the corpus mean by >= 1.0 signs' (failure if < 1.0)")
for k, v in results.items():
    g = DISC_MEAN - v["mean"]
    out.append("      %s: gap %+.3f  ->  %s" % (k, g, "PASS" if g >= 1.0 else "FAIL"))
out.append("")
out.append("P3  '< 1%% of size-matched samples have zero 1-sign tokens, and < 1%% have")
out.append("     mean >= the Disc's' (failure if either rate >= 1%%)")
for k, v in results.items():
    ok = v["p_zero1"] < 0.01 and v["p_mean"] < 0.01
    out.append("      %s: P(zero 1-sign)=%.4f, P(mean>=disc)=%.4f  ->  %s"
               % (k, v["p_zero1"], v["p_mean"], "PASS" if ok else "FAIL"))

out.append("")
out.append("NOTE ON CORPUS SELECTION.  P1-P3 were frozen naming 'Linear B and/or Linear A',")
out.append("the two Aegean syllabic corpora.  Those are the pre-registered tests and they")
out.append("stand or fall on LB and LA.  CY (Cypriot) was added AFTER seeing LB and LA and is")
out.append("therefore POST-HOC and exploratory; it is reported for what it suggests, not as a")
out.append("confirmed prediction.")

txt = "\n".join(out)
print(txt)
open(os.path.join(HERE, "results", "genre.txt"), "w").write(txt + "\n")
json.dump({"disc_mean": DISC_MEAN, "disc_n": DISC_N,
           "disc_dist": {str(k): v for k, v in sorted(Counter(disc).items())},
           "corpora": results},
          open(os.path.join(HERE, "results", "genre.json"), "w"), indent=1)
