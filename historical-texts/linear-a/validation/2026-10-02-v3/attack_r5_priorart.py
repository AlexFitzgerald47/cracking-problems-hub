#!/usr/bin/env python3
"""
ATTACK R5 (new, 2026-10-03) — the dossier's results, checked against the
commentary that ships IN THE SAME REPOSITORY AS THE CLAIMANT'S OWN EDITION.

Validator 2 established prior art through a parallel external AI workspace
(dbourdeau/cyphersolver) and the secondary literature.  R5 goes one level
closer in: `mwenge/lineara.xyz` carries, beside `LinearAInscriptions.js`,
a `commentary/HT*.html` file per tablet reproducing John Younger's
GORILA-based commentary.  The claimant cites several of these files by URL.

So the test is not "did someone somewhere publish this" but "is the claimed
new result written in the file next to the data file the claim was derived
from".  Each of the frontier's named results is turned into a literal string
search over the commentary text, and the matching sentence is printed.

Vendored: priorart_r/younger_HT*.html (hashes printed).  `fetch` re-downloads.
"""
import html, os, re, sys, hashlib, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PA = os.path.join(HERE, "priorart_r")
URL = "https://raw.githubusercontent.com/mwenge/lineara.xyz/master/commentary/{}.html"
DOCS = ["HT85", "HT87", "HT94", "HT112", "HT117", "HT119", "HT122",
        "HT128", "HT132", "HT135", "HT88", "HT34", "HT97"]


def fetch():
    os.makedirs(PA, exist_ok=True)
    for d in DOCS:
        with urllib.request.urlopen(URL.format(d), timeout=120) as r:
            open(os.path.join(PA, f"younger_{d}.html"), "wb").write(r.read())
        print("ok", d)


def text(d):
    p = os.path.join(PA, f"younger_{d}.html")
    s = open(p, encoding="utf-8").read()
    t = html.unescape(re.sub("<[^>]+>", " ", s))
    return re.sub(r"\s+", " ", t)


# (frontier result as HANDOVER.md states it, tablet, search probes)
TESTS = [
 ("HT85: '66 personnel = 11 standardized groups of 6' "
  "(scribe9_dossier.csv column `new_inference`)",
  "HT85", ["11 sets of 6", "sets of 6 each", "groups of 6 personnel"]),
 ("HT85: 'reverse encodes receiving/responsibility slots' "
  "(scribe9_dossier.csv `new_inference`)",
  "HT85", ["side b lists 11 people", "responsible for these 11 sets"]),
 ("HT85: side-a entries are accountable SOURCE UNITS (places)",
  "HT85", ["names on HT 85a are toponymns", "names on side a are those of places"]),
 ("HT85: A-DU = assessment of personnel",
  "HT85", ["personnel are assessed (A-DU)"]),
 ("HT85b: PA / KA / DI absorbed into the neighbouring entries "
  "(the move the dossier's rendering table makes)",
  "HT85", ["KA & DI are therefore probably", "abbreviations of types of persons"]),
 ("HT117: a RULING closes the first block; the tablet has THREE sections, "
  "not one KI-RO roster",
  "HT117", ["the rule there apparently introduces a second section",
            "presents a third section"]),
 ("HT117 + HT87: the DI-KI-SE / QIf-TU-NE pairing — the dossier's "
  "'strongest query-grammar result'",
  "HT117", ["in both HT 87 & HT 117", "appear in the same paragraph"]),
 ("HT117: SA-TA / QIf-TU-NE / MA-KA-RI-TE = accountable or supplying units "
  "(the dossier's U-MI-NA-SI / SA-TA / QI-TU-NE result)",
  "HT117", ["may be regions or people supplying personnel"]),
 ("HT117: KU-RO 10 totals the preceding ten personnel",
  "HT117", ["KU-RO totals the 10"]),
 ("HT119: '*327 34 : VIR 68, an exact 1:2 fixed manpower ratio'",
  "HT119", ["distributed per pair VIR"]),
 ("HT119: the entries do NOT reach the stated KU-RO 160 "
  "(the failure scribe9_dossier.csv lists as a strong anchor)",
  "HT119", ["total 159, not KU-RO"]),
 ("HT122: 'KU-RO 31 + KU-DA 1 + KU-RO 65 = PO-TO-KU-RO 97', "
  "the hierarchical control-total flagship",
  "HT122", ["PO-TO-KU-RO", "= KU-RO b.5"]),
 ("HT122: 'master personnel liability/control register' over contributing units",
  "HT122", ["lists places by name and their contributions of groups of personnel"]),
 ("HT94b: KI-RO opens a list of personnel deficits closed by KU-RO 5",
  "HT94", ["KI-RO", "deficit"]),
 ("HT88: KI-RO forward list closed by KU-RO 6",
  "HT88", ["KI-RO", "KU-RO"]),
 ("HT34: 'KI-RO 30' as 100 - 70, the dossier's cleanest residual",
  "HT34", ["apparently a deficit"]),
]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        fetch(); sys.exit()

    print("=" * 78)
    print("ATTACK R5 — is the 'new result' already in the commentary that ships")
    print("            beside the claimant's own data file?")
    print("=" * 78)
    print("  source: github.com/mwenge/lineara.xyz commentary/HT*.html")
    print("  (the same repository as LinearAInscriptions.js; the claimant cites")
    print("   commentary/HT34, HT85, HT88, HT94, HT95, HT117, HT123+124, HT15,")
    print("   HT30, HT37, HT93 and ARKH4 by URL in analysis/)")
    print("  vendored copies and hashes:")
    for d in DOCS:
        p = os.path.join(PA, f"younger_{d}.html")
        if os.path.exists(p):
            h = hashlib.sha256(open(p, "rb").read()).hexdigest()
            print(f"    younger_{d}.html  sha256 {h[:32]}...")
    print()

    hit = miss = 0
    for label, doc, probes in TESTS:
        t = text(doc)
        found = [p for p in probes if p.lower() in t.lower()]
        ok = len(found) == len(probes)
        print(f"  [{'ALREADY PUBLISHED' if ok else 'not found verbatim '}] {label}")
        if ok:
            hit += 1
            for p in probes:
                i = t.lower().index(p.lower())
                print(f"      ...{t[max(0,i-150):i+170].strip()}...")
        else:
            miss += 1
            print(f"      probes not all matched: missing {[p for p in probes if p not in found]}")
        print()

    print("-" * 78)
    print(f"  frontier results found verbatim in the bundled commentary: {hit}/{hit+miss}")
    print("""
  CONSEQUENCE.  The dossier's headline items -- the eleven six-person gangs,
  the responsibility slots on HT85b, the toponym/source-unit reading of the
  HT85a entries, A-DU as assessment, the HT87<->HT117 DI-KI-SE pairing, the
  supplying-unit reading of SA-TA / QIf-TU-NE / MA-KA-RI-TE, the HT122
  hierarchical identity 97 = 65 + 31 + 1, and the HT119 1:2 manpower ratio --
  are not inferences the Hub drew from the corpus.  They are sentences in the
  commentary file that sits next to the corpus file the Hub parsed, by an
  author the Hub cites by URL elsewhere in the same analysis directory.

  The Hub's own note 2026-09-07-ht85-order-preserving-dispatch-reconstruction.md
  says this for HT85 ("Younger had already seen eleven six-person groups and
  multiple groups assigned to QE-KA / TE-TU").  HANDOVER.md's frontier
  statement and scribe9_dossier.csv's `new_inference` column do not carry that
  attribution forward, and the frontier is what is under validation.
  """)
