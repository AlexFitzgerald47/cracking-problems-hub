#!/usr/bin/env python3
"""V1 reproduction, part 1: corpus census and coverage of the Scribe-9 / HT labour claim.
Reads only raw witness A (mwenge/lineara.xyz LinearAInscriptions.js, a tabulation of
Godart-Olivier GORILA). Does not read the claimant's analysis/*.csv."""
import sys, re, collections, json
sys.path.insert(0, '.')
from load import load

DIV = "\U00010101"; LAC = "\U0001076b"
NUMCH = "0123456789"
FRAC = "¹²³⁴⁵⁶⁷⁸⁹⁰⁄₀₁₂₃₄₅₆₇₈₉½⅓¼⅕⅙"
IDEO = re.compile(r'^(GRA|VIN|OLE|OLIV|CYP|FIC|VIR|MUL|BOS|OVIS|CAP|SUS|AROM|TELA|HORD|'
                  r'double mina|mina|CAPf|CAPm|OVISf|OVISm|BOSf|BOSm|SUSf|SUSm|\*)')
def is_num(t):
    t=t.strip()
    if not t: return False
    return all(c in NUMCH+FRAC+" ./≈-[]" for c in t) and any(c in NUMCH+FRAC for c in t)
def ival(t):
    t=t.strip()
    return float(t) if re.fullmatch(r'\d+', t) else None
def is_sg(t):
    """A syllabic sign-group (word): not a numeral, divider, newline, ruling, or
    ideogram/logogram.  Starred signs ARE kept when they are part of a hyphenated
    sign-group (*306-TU, *21F-TU-NE); a bare starred number or a ligature (X+Y) is an
    ideogram and is dropped."""
    if t in ("\n", DIV, "—", "", " ", LAC): return False
    if is_num(t): return False
    if "+" in t: return False
    if "-" in t: return True
    if IDEO.match(t): return False
    if t.startswith("\U0001076b"): return False
    return True
def basedoc(n):
    m=re.match(r'^(.*?)([ab]|\d)?$', n)
    m2=re.match(r'^([A-Z]+[0-9+]+)', n)
    return m2.group(1) if m2 else n

A = load()
print("### WITNESS A census (mwenge/lineara.xyz, GORILA-derived)")
print("records (faces/objects) :", len(A))
sites = collections.Counter(v.get('site') for v in A.values())
sup   = collections.Counter(v.get('support') for v in A.values())
print("supports:", dict(sup.most_common()))
print("top sites:", dict(sites.most_common(8)))

# sign-group census
tok_all = 0; typ_all = collections.Counter()
for k,v in A.items():
    for w in v.get('transliteratedWords',[]):
        if is_sg(w): tok_all += 1; typ_all[w]+=1
print(f"sign-group TOKENS corpus-wide : {tok_all}")
print(f"sign-group TYPES  corpus-wide : {len(typ_all)}")

docs = {}
for k,v in A.items():
    d = basedoc(k); docs.setdefault(d, []).append(k)
print("distinct documents (faces merged):", len(docs))

ht_tab = {k:v for k,v in A.items() if v.get('site')=='Haghia Triada' and v.get('support')=='Tablet'}
ht_tab_docs = sorted(set(basedoc(k) for k in ht_tab))
print(f"Haghia Triada TABLET faces: {len(ht_tab)}  documents: {len(ht_tab_docs)}")
ht_tok = sum(1 for k,v in ht_tab.items() for w in v['transliteratedWords'] if is_sg(w))
print(f"HT tablet sign-group tokens: {ht_tok}  ({100*ht_tok/tok_all:.1f}% of corpus tokens)")

# --- Scribe 9
s9 = sorted(k for k,v in A.items() if v.get('scribe')=='HT Scribe 9')
s9docs = sorted(set(basedoc(k) for k in s9))
s9tok = sum(1 for k in s9 for w in A[k]['transliteratedWords'] if is_sg(w))
s9typ = set(w for k in s9 for w in A[k]['transliteratedWords'] if is_sg(w))
print(f"\n### SCRIBE 9 (corpus metadata, not the claimant's csv)")
print("faces:", s9)
print("documents:", s9docs, f"(n={len(s9docs)})")
print("findspots:", dict(collections.Counter(A[k].get('findspot') for k in s9)))
print(f"sign-group tokens {s9tok} = {100*s9tok/tok_all:.2f}% of corpus tokens; "
      f"types {len(s9typ)} = {100*len(s9typ)/len(typ_all):.2f}% of corpus types")
print(f"documents {len(s9docs)}/{len(docs)} = {100*len(s9docs)/len(docs):.2f}% of documents")

# scribe coverage of corpus generally
sc = collections.Counter(v.get('scribe') for v in A.values() if v.get('scribe'))
print("\nfaces with ANY scribe attribution:", sum(sc.values()), "of", len(A))
print("distinct attributed hands:", len(sc))

# --- documents actually touched by the whole claim chain (all 4 analysis notes)
CLAIMED = """HT85 HT87 HT94 HT112 HT117 HT119 HT122 HT128 HT132 HT135
             HT88 HT95 HT86 HT2 HT97 HT28 HT1 HT15 HT34 HT30 HT37 HT123+124
             HT8 HT29 ZA10 HT93 ARKH4 HT96 HT118""".split()
present = [d for d in CLAIMED if d in docs or d+'a' in A or d in A]
print(f"\n### CLAIM FOOTPRINT (every document named anywhere in the 4 analysis notes)")
print("documents named:", len(CLAIMED), "; found in witness A:", len(present))
ctok=0; ctyp=set()
for d in CLAIMED:
    for k in docs.get(d, []):
        for w in A[k]['transliteratedWords']:
            if is_sg(w): ctok+=1; ctyp.add(w)
print(f"their sign-group tokens {ctok} = {100*ctok/tok_all:.2f}% of corpus tokens")
print(f"their sign-group types  {len(ctyp)} = {100*len(ctyp)/len(typ_all):.2f}% of corpus types")
print(f"documents {len(CLAIMED)}/{len(docs)} = {100*len(CLAIMED)/len(docs):.2f}%")

# how many sign-group TYPES get any functional gloss at all from the claim
GLOSSED = {"KU-RO","PO-TO-KU-RO","KI-RO","A-DU","KI-KI-RA-JA","DA-DU-MA-TA","KU-DA",
           "MA-KA-RI-TE","U-MI-NA-SI","SA-TA","*21F-TU-NE","A-KA-RU","KA-RU"}
gt = sum(typ_all[w] for w in GLOSSED if w in typ_all)
print(f"\n### LEXICAL FOOTPRINT: sign-group types given a functional value by the claim: "
      f"{len([w for w in GLOSSED if w in typ_all])} of {len(typ_all)} types "
      f"({100*len([w for w in GLOSSED if w in typ_all])/len(typ_all):.2f}%)")
print(f"   their token count {gt} = {100*gt/tok_all:.2f}% of all sign-group tokens")
for w in sorted(GLOSSED):
    print(f"     {w:14s} {typ_all.get(w,0):4d} tokens")
