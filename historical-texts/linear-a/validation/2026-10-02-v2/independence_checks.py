#!/usr/bin/env python3
"""
2026-10-02 VALIDATOR 2 (prior-art and independence) — Linear A
"Haghia Triada labour-control / obligation-circuit" + "Scribe-9 dossier" claim.

This is NOT a re-run of the 2026-09-25 refutation script. It asks four questions that
belong to the independence lane:

  P1  COVERAGE          how much of the corpus the reading actually touches.
  P2  LABEL PERMUTATION the orchestrator's cross-reference test, done literally:
                        every record stays in its own position, only the scribe /
                        document-class label is permuted.  Plus the test the claimant
                        never ran: is Scribe 9 special among HT scribes at all?
  P3  PRIOR-ART ABLATION the Davis & Valerio (2020) 19 recurring HT designations are a
                        PUBLISHED property of this corpus.  Does Scribe-9 "dossier
                        cohesion" survive removing them?
  P4  INFORMATION CEILING  the distinctions the reading needs vs. what the corpus can
                        resolve: single-sign "entities", two-edition disagreement, and
                        the gloss already baked into the digital edition.

Witness: mwenge/lineara.xyz LinearAInscriptions.js (GORILA via Douros tabulation,
Younger commentary), fetched 2026-10-02 into ./data.  Second witness: the SigLA word
views vendored by the 2026-09-25 session (read-only).

Nothing here reads the claimant's analysis/*.csv or analysis/*.md as evidence; the
claimant's files are read only to enumerate which tablets the claim names (P1).

Usage:  python3 independence_checks.py
"""
import collections
import glob
import html
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
SIGLA_DIR = os.path.abspath(os.path.join(HERE, "..", "2026-09-25", "data"))
CLAIM_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "analysis"))

DIVIDER = "\U00010101"
NUM = re.compile(r'^[\d\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079\u2070'
                 r'\u2080-\u2089\u2044/\u2248\s\.\-]+$')

# The six-term "provisional partial semantic lexicon" of
# analysis/administrative_state_machine.csv, plus KU-DA which the HT122 hierarchy needs.
CLAIM_LEXICON = ["KU-RO", "PO-TO-KU-RO", "KI-RO", "A-DU", "DA-DU-MA-TA",
                 "KI-KI-RA-JA", "KU-DA"]
# Further sign-groups the dossier assigns a functional TYPE to (not a translation).
CLAIM_TYPED = ["MA-KA-RI-TE", "U-MI-NA-SI", "SA-TA", "QI-TU-NE", "A-KA-RU", "KA-RU",
               "KA-PA", "SA-RA\u2082", "DI-KI-SE", "QA-RE-TO"]

# Davis & Valerio 2020's 19 recurring Haghia Triada designations, in their order, as
# quoted verbatim in analysis/2026-09-07-haghia-triada-labor-control-functional-solve.md
# section 1.  Variants are listed together, exactly as that section lists them.
DV19 = [
    ["DA-RI-DA"], ["PA\u2083-NI", "PA\u2083-NI-NA"], ["U-*325-ZA", "U-DE-ZA"],
    ["DA-SI-*118"], ["KU-ZU-NI"], ["TE-KI", "TE-KE"], ["DA-RE"], ["TE-TU"], ["ME-ZA"],
    ["RA-TI-SE", "RE-DI-SE"], ["WA-DU-NI-MI"], ["MA-DI"], ["QA-*310-I"], ["PA-DE"],
    ["*306-TU"], ["*324-DI-RA"], ["TA-I-*123"], ["A-RU"], ["KU-PA\u2083-NU"],
]
DV19_FLAT = {w for grp in DV19 for w in grp}

ADMIN_OPS = {"KU-RO", "PO-TO-KU-RO", "KI-RO", "KU-DA", "A-DU", "KA-PA", "SA-RA\u2082",
             "SA-RO", "A-KA-RU", "KA-RU", "DA-DU-MA-TA"}

# The dossier's own document classes (HANDOVER.md "Main new result: the Scribe-9 dossier"
# and analysis/scribe9_dossier.csv working_function column).
DOSSIER_CLASS = {
    "HT85": "ordinary", "HT87": "ordinary", "HT122": "ordinary",
    "HT94": "exception", "HT117": "exception",
    "HT112": "resource", "HT119": "resource", "HT128": "resource",
    "HT132": "resource", "HT135": "resource",
}


# ----------------------------------------------------------------- corpus
def load_corpus():
    s = open(os.path.join(DATA, "LinearAInscriptions.js"), encoding="utf-8").read()
    st = s.index("new Map(") + len("new Map(")
    en = s.index("]);", st) + 1
    body = re.sub(r',(\s*[\]\}])', r'\1', s[st:en])
    body = re.sub(r'\\u\{([0-9a-fA-F]+)\}',
                  lambda m: chr(int(m.group(1), 16)), body)
    return dict(json.loads(body))


def is_num(t):
    return bool(t) and bool(NUM.match(t)) and any(
        c.isdigit() or c in "\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079"
        "\u2070\u2044" for c in t)


def is_word(t):
    """A syllabic sign-group: not numeral, divider, ruling, ideogram or erasure."""
    if t in ("\n", DIVIDER, "\u2014", "", " "):
        return False
    if t.startswith("[["):            # editorial erasure
        return False
    if is_num(t):
        return False
    if re.match(r'^(GRA|VIN|OLE|OLIV|CYP|FIC|VIR|MUL|BOS|OVIS|CAP|SUS|AROM|TELA|HORD|'
                r'double|mina|E\+|QA2\+|MI\+|KI\+|SA\+|TI\+|\*\d)', t):
        return False
    if t.startswith("*") or t.startswith("\U0001076b"):
        return False
    if "+" in t:                      # ligature / logogram compound
        return False
    return True


def base(name):
    m = re.match(r'^([A-Z]+\d+)', name)
    return m.group(1) if m else name


def ht_tablet_faces(A):
    return {k: v for k, v in A.items()
            if v.get("site") == "Haghia Triada" and v.get("support") == "Tablet"}


def merge_sides(A, faces):
    """External counting note (dbourdeau/cyphersolver round 22): sides a/b are separate
    records in this corpus; merge them for any per-tablet test."""
    out = collections.defaultdict(lambda: {"words": [], "scribe": set(), "faces": []})
    for k in faces:
        t = base(k)
        out[t]["words"] += [w for w in A[k]["transliteratedWords"]]
        sc = A[k].get("scribe") or ""
        if sc:
            out[t]["scribe"].add(sc)
        out[t]["faces"].append(k)
    return dict(out)


# ----------------------------------------------------------------- P1 coverage
def p1_coverage(A, tablets):
    print("\n" + "=" * 78)
    print("P1  COVERAGE — how much of the corpus does this reading touch?")
    print("=" * 78)

    nrec = len(A)
    ndoc = len(set(base(k) for k in A))
    print(f"  corpus records (faces/objects)          : {nrec}")
    print(f"  distinct documents after merging faces  : {ndoc}")
    bysup = collections.Counter(v.get("support") for v in A.values())
    print(f"  of which support=Tablet                 : {bysup['Tablet']} records")
    print(f"  HT tablet records / merged HT tablets   : "
          f"{sum(1 for v in A.values() if v.get('site')=='Haghia Triada' and v.get('support')=='Tablet')}"
          f" / {len(tablets)}")

    # which documents does the claim actually name?
    named = set()
    for p in sorted(glob.glob(os.path.join(CLAIM_DIR, "*.md"))
                    + glob.glob(os.path.join(CLAIM_DIR, "*.csv"))):
        txt = open(p, encoding="utf-8").read()
        for m in re.finditer(r'\b(HT|ZA|KH|PH|ARKH|PK|KN)\s?(\d+)', txt):
            named.add(m.group(1) + m.group(2))
    incorpus = sorted(n for n in named if any(base(k) == n for k in A))
    print(f"\n  documents named anywhere in the claimant's analysis/ files: {len(named)}")
    print(f"  ... of which exist in the corpus                          : {len(incorpus)}")
    print(f"      {incorpus}")
    print(f"  => named-document coverage: {len(incorpus)}/{ndoc} = "
          f"{100.0*len(incorpus)/ndoc:.2f}% of documents")
    s9 = sorted(t for t, d in tablets.items() if "HT Scribe 9" in d["scribe"])
    print(f"  the dossier proper (Scribe 9)  : {len(s9)}/{ndoc} = "
          f"{100.0*len(s9)/ndoc:.2f}% of documents  {s9}")

    # token-level coverage of the claimed lexicon
    allw = [w for v in A.values() for w in v["transliteratedWords"]]
    wtok = [w for w in allw if is_word(w)]
    wtyp = set(wtok)
    lex = collections.Counter(w for w in wtok if w in CLAIM_LEXICON)
    typ = collections.Counter(w for w in wtok if w in CLAIM_TYPED)
    print(f"\n  sign-group tokens in the whole corpus   : {len(wtok)}")
    print(f"  distinct sign-group types               : {len(wtyp)}")
    print(f"  tokens of the 7-term claimed lexicon    : {sum(lex.values())} "
          f"= {100.0*sum(lex.values())/len(wtok):.2f}%   {dict(lex)}")
    print(f"  + the 10 further type-assigned groups   : {sum(typ.values())} "
          f"= {100.0*sum(typ.values())/len(wtok):.2f}%   {dict(typ)}")
    cov = sum(lex.values()) + sum(typ.values())
    print(f"  => sign-group tokens given ANY function : {cov}/{len(wtok)} = "
          f"{100.0*cov/len(wtok):.2f}%")
    print(f"  => sign-group TYPES given any function  : "
          f"{len([w for w in CLAIM_LEXICON+CLAIM_TYPED if w in wtyp])}/{len(wtyp)} = "
          f"{100.0*len([w for w in CLAIM_LEXICON+CLAIM_TYPED if w in wtyp])/len(wtyp):.2f}%")
    recs_with = sum(1 for v in A.values()
                    if any(w in CLAIM_LEXICON for w in v["transliteratedWords"]))
    print(f"  records containing at least one lexicon term: {recs_with}/{nrec} = "
          f"{100.0*recs_with/nrec:.2f}%")
    return s9


# ----------------------------------------------------------------- statistics
def typeset(words, strict=True, drop_dv19=False):
    out = set()
    for w in words:
        if not is_word(w):
            continue
        if strict:
            if "-" not in w:          # drop single-syllabogram tokens
                continue
            if w in ADMIN_OPS:
                continue
        if drop_dv19 and w in DV19_FLAT:
            continue
        out.add(w)
    return out


def cohesion(members, sets):
    """number of sign-group types attested on >=2 distinct tablets of the group"""
    c = collections.Counter()
    for t in members:
        for w in sets[t]:
            c[w] += 1
    shared = sorted(w for w, n in c.items() if n >= 2)
    return len(shared), shared


def mean_jaccard(members, sets):
    """size-normalised cohesion: mean pairwise Jaccard of the tablets' type sets"""
    vals = []
    for i, a in enumerate(members):
        for b in members[i + 1:]:
            u = sets[a] | sets[b]
            if u:
                vals.append(len(sets[a] & sets[b]) / len(u))
    return sum(vals) / len(vals) if vals else 0.0


def perm_p(obs, draws):
    return (sum(1 for d in draws if d >= obs) + 1) / (len(draws) + 1)


# ----------------------------------------------------------------- P2
def p2_label_permutation(tablets, s9, N=20000, seed=20261002):
    print("\n" + "=" * 78)
    print("P2  LABEL PERMUTATION — contents fixed in position, only the label moves")
    print("=" * 78)
    rng = random.Random(seed)
    allt = sorted(tablets)
    size = {t: sum(1 for w in tablets[t]["words"] if is_word(w)) for t in allt}

    for strict, tag in ((True, "STRICT (multi-sign groups, admin operators dropped)"),
                        (False, "LOOSE (every sign-group, as the dossier counts)")):
        sets = {t: typeset(tablets[t]["words"], strict=strict) for t in allt}
        obs, shared = cohesion(s9, sets)
        obsj = mean_jaccard(s9, sets)
        print(f"\n-- statistic: {tag}")
        print(f"   observed Scribe-9 cohesion = {obs} shared types; "
              f"mean pairwise Jaccard = {obsj:.4f}")
        print(f"   shared types = {shared}")

        # (i) literal label permutation: shuffle the scribe label over all HT tablets
        draws, draws_j = [], []
        for _ in range(N):
            pick = rng.sample(allt, len(s9))
            draws.append(cohesion(pick, sets)[0])
            draws_j.append(mean_jaccard(pick, sets))
        draws.sort(); draws_j.sort()
        print(f"   (i)  label permuted over all {len(allt)} HT tablets:")
        print(f"        count  null mean {sum(draws)/N:6.2f}  95% [{draws[int(.025*N)]}, "
              f"{draws[int(.975*N)]}]   p = {perm_p(obs, draws):.4f}")
        print(f"        Jaccard null mean {sum(draws_j)/N:6.4f}  95% "
              f"[{draws_j[int(.025*N)]:.4f}, {draws_j[int(.975*N)]:.4f}]   "
              f"p = {perm_p(obsj, draws_j):.4f}")

        # (ii) size-stratified: the label is confounded with tablet length
        tgt = sum(size[t] for t in s9)
        d2, d2j, tries = [], [], 0
        while len(d2) < 5000 and tries < 3_000_000:
            tries += 1
            pick = rng.sample(allt, len(s9))
            if abs(sum(size[t] for t in pick) - tgt) <= 0.10 * tgt:
                d2.append(cohesion(pick, sets)[0])
                d2j.append(mean_jaccard(pick, sets))
        if d2:
            d2.sort(); d2j.sort(); n2 = len(d2)
            print(f"   (ii) same permutation restricted to length-matched labels "
                  f"(+/-10% of {tgt} tokens, n={n2}):")
            print(f"        count  null mean {sum(d2)/n2:6.2f}  95% [{d2[int(.025*n2)]}, "
                  f"{d2[int(.975*n2)]}]   p = {perm_p(obs, d2):.4f}")
            print(f"        Jaccard null mean {sum(d2j)/n2:6.4f}  95% "
                  f"[{d2j[int(.025*n2)]:.4f}, {d2j[int(.975*n2)]:.4f}]   "
                  f"p = {perm_p(obsj, d2j):.4f}")

    # (iii) is Scribe 9 special among HT scribes at all?
    print("\n-- (iii) the test the claimant never ran: EVERY attested HT tablet scribe")
    sets = {t: typeset(tablets[t]["words"], strict=True) for t in allt}
    byscribe = collections.defaultdict(list)
    for t in allt:
        for sc in tablets[t]["scribe"]:
            byscribe[sc].append(t)
    rows = []
    for sc, mem in sorted(byscribe.items()):
        if len(mem) < 3:
            continue
        obs, sh = cohesion(mem, sets)
        obsj = mean_jaccard(mem, sets)
        d = [cohesion(rng.sample(allt, len(mem)), sets)[0] for _ in range(4000)]
        dj = [mean_jaccard(rng.sample(allt, len(mem)), sets) for _ in range(4000)]
        rows.append((sc, len(mem), sum(size[t] for t in mem), obs, perm_p(obs, d),
                     obsj, perm_p(obsj, dj), sh))
    print(f"   {'scribe':17s} {'n':>2s} {'tok':>4s} {'coh':>4s} {'p':>7s} "
          f"{'jacc':>6s} {'p':>7s}")
    for sc, n, tok, obs, p, oj, pj, sh in sorted(rows, key=lambda r: -r[3]):
        print(f"   {sc:17s} {n:2d} {tok:4d} {obs:4d} {p:7.4f} {oj:6.4f} {pj:7.4f}  {sh}")
    nsig = sum(1 for r in rows if r[4] < 0.05)
    print(f"   scribes with >=3 tablets: {len(rows)}; "
          f"count-cohesion p<0.05: {nsig}; Jaccard p<0.05: "
          f"{sum(1 for r in rows if r[6] < 0.05)}")

    # (iv) the Annals move itself: permute ONLY the document-class label inside Scribe 9
    print("\n-- (iv) permute ONLY the document-class label, inside Scribe 9")
    print("        (the orchestrator cross-reference's exact test: every tablet keeps its")
    print("         own content, only 'exception' vs 'ordinary' moves)")
    exc = [t for t in s9 if DOSSIER_CLASS.get(t) == "exception"]
    ordy = [t for t in s9 if DOSSIER_CLASS.get(t) == "ordinary"]
    pool = exc + ordy
    for strict, tag in ((True, "strict"), (False, "loose")):
        ss = {t: typeset(tablets[t]["words"], strict=strict) for t in allt}
        def cross(e, o):
            we = set().union(*[ss[t] for t in e]) if e else set()
            wo = set().union(*[ss[t] for t in o]) if o else set()
            return len(we & wo), sorted(we & wo)
        obs, sh = cross(exc, ordy)
        d = []
        for _ in range(20000):
            p = pool[:]
            rng.shuffle(p)
            d.append(cross(p[:len(exc)], p[len(exc):])[0])
        d.sort()
        print(f"   [{tag}] exception={exc} ordinary={ordy}")
        print(f"          observed cross-class shared types = {obs}  {sh}")
        print(f"          null mean {sum(d)/len(d):.2f}  95% [{d[int(.025*len(d))]}, "
              f"{d[int(.975*len(d))]}]   p = {perm_p(obs, d):.4f}")
        # how many distinct assignments exist at all?
        import math
        print(f"          distinct label assignments available = "
              f"{math.comb(len(pool), len(exc))}  (floor on any achievable p)")


# ----------------------------------------------------------------- P3
def p3_prior_art_ablation(tablets, s9, N=20000, seed=20261002):
    print("\n" + "=" * 78)
    print("P3  PRIOR-ART ABLATION — Davis & Valerio 2020's 19 recurring designations")
    print("=" * 78)
    rng = random.Random(seed)
    allt = sorted(tablets)
    print("  The 19-designation recurring set is a PUBLISHED property of the HT corpus")
    print("  (Davis & Valerio 2020), quoted verbatim in the claimant's own section 1.")
    print("  Any cohesion it supplies is prior art, not a Scribe-9 finding.")

    sets = {t: typeset(tablets[t]["words"], strict=True) for t in allt}
    obs, sh = cohesion(s9, sets)
    inDV = [w for w in sh if w in DV19_FLAT]
    print(f"\n  Scribe-9 shared types                 : {obs}  {sh}")
    print(f"  ... of which Davis-Valerio circuit words: {len(inDV)}  {inDV}")
    print(f"  ... remainder                           : "
          f"{[w for w in sh if w not in DV19_FLAT]}")

    sets2 = {t: typeset(tablets[t]["words"], strict=True, drop_dv19=True)
             for t in allt}
    obs2, sh2 = cohesion(s9, sets2)
    size = {t: len(sets2[t]) for t in allt}
    tgt = sum(size[t] for t in s9)
    d = [cohesion(rng.sample(allt, len(s9)), sets2)[0] for _ in range(N)]
    d.sort()
    d2, tries = [], 0
    while len(d2) < 5000 and tries < 3_000_000:
        tries += 1
        pick = rng.sample(allt, len(s9))
        if abs(sum(size[t] for t in pick) - tgt) <= 0.10 * max(tgt, 1):
            d2.append(cohesion(pick, sets2)[0])
    print(f"\n  AFTER removing the 19 published designations:")
    print(f"    observed cohesion = {obs2}  {sh2}")
    print(f"    label permuted over all HT tablets : null mean {sum(d)/N:.2f} "
          f"95% [{d[int(.025*N)]}, {d[int(.975*N)]}]  p = {perm_p(obs2, d):.4f}")
    if d2:
        d2.sort(); n2 = len(d2)
        print(f"    length-matched (n={n2})            : null mean {sum(d2)/n2:.2f} "
              f"95% [{d2[int(.025*n2)]}, {d2[int(.975*n2)]}]  p = {perm_p(obs2, d2):.4f}")

    # how much of the DV19 set sits on Scribe 9 vs the rest of HT?
    s9set = set().union(*[typeset(tablets[t]["words"], strict=False) for t in s9])
    rest = set().union(*[typeset(tablets[t]["words"], strict=False)
                         for t in allt if t not in s9])
    print(f"\n  DV19 members attested on Scribe-9 tablets : "
          f"{sorted(DV19_FLAT & s9set)}")
    print(f"  DV19 members attested elsewhere at HT     : "
          f"{sorted(DV19_FLAT & rest)}")


# ----------------------------------------------------------------- P4
def load_sigla():
    out = {}
    for p in sorted(glob.glob(os.path.join(SIGLA_DIR, "sigla_*.html"))):
        doc = os.path.basename(p)[6:-5].replace("_", " ")
        s = open(p, encoding="utf-8").read()
        txt = html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', s)))
        seqs = re.findall(r'Sequence #\d+(.*?)\(\d+ signs?\)', txt)
        out[doc] = [re.sub(r'\s+', '', x) for x in seqs]
    return out


def p4_ceiling(A, tablets):
    print("\n" + "=" * 78)
    print("P4  INFORMATION CEILING — are the needed distinctions resolvable at all?")
    print("=" * 78)

    # (a) single-sign tokens: the Hub's own 2026-09-25 rule
    htt = ht_tablet_faces(A)
    tok = [w for v in htt.values() for w in v["transliteratedWords"] if is_word(w)]
    one = [w for w in tok if "-" not in w]
    print(f"\n  (a) HT tablet sign-group tokens        : {len(tok)}")
    print(f"      one-syllabogram tokens            : {len(one)} = "
          f"{100.0*len(one)/len(tok):.1f}%")
    print(f"      most frequent                     : "
          f"{collections.Counter(one).most_common(10)}")
    print("      Board rule (2026-09-25, PRACTICES): in an administrative corpus the")
    print("      shortest units are mostly not words, and where the corpus is")
    print("      undeciphered there is no principled way to separate abbreviation from")
    print("      word, so the corpus is DISQUALIFIED for the question, not cleaned.")

    print("\n      single-sign tokens standing as 'entries' in the dossier's own lists:")
    for f in ["HT85b", "HT122a", "HT122b", "HT94a", "HT94b", "HT117a", "HT117b",
              "HT87", "HT119"]:
        if f not in A:
            continue
        ws = A[f]["transliteratedWords"]
        got = [w for w in ws if is_word(w) and "-" not in w]
        tot = [w for w in ws if is_word(w)]
        print(f"        {f:7s} {len(got)}/{len(tot)} sign-groups are single signs: {got}")

    # (b) the 11 x 6 count depends on that decision, and on the edition
    print("\n  (b) HT85's '66 = 11 x 6' depends on the entry count of HT85b:")
    b = A["HT85b"]["transliteratedWords"]
    allg = [w for w in b if is_word(w)]
    multi = [w for w in allg if "-" in w]
    print(f"      witness A (GORILA/Douros) sign-groups       : {len(allg)} {allg}")
    print(f"      ... minus the KI-KI-RA-JA heading           : {len(allg)-1}")
    print(f"      ... multi-sign only, minus heading          : {len(multi)-1} {multi[1:]}")
    S = load_sigla()
    if "HT 85b" in S:
        print(f"      witness B (SigLA) sequences                 : {len(S['HT 85b'])} "
              f"{S['HT 85b']}")
        print(f"      ... minus the heading                       : {len(S['HT 85b'])-1}")
    print("      66/11 = 6 exactly; 66/8 = 8.25; 66/7 = 9.43.  The 'standardized")
    print("      six-person gang' exists only on the 11-entry reading, which requires")
    print("      counting PA, KA and DI as personnel entries.")

    # (c) two-edition divergence on the dossier tablets
    print("\n  (c) two editions of the same eleven dossier faces:")
    norm = lambda s: re.sub(r'[\[\]\?\-]', '', s.lower()
                           .replace("\u2082", "2").replace("\u2083", "3")
                           .replace("*", "a"))
    tot_a = tot_b = agree = 0
    for doc, seqs in sorted(S.items()):
        key = doc.replace(" ", "")
        if key not in A:
            continue
        a = [norm(w) for w in A[key]["transliteratedWords"] if is_word(w)]
        bb = [norm(w) for w in seqs if w]
        inter = len(set(a) & set(bb))
        tot_a += len(set(a)); tot_b += len(set(bb)); agree += inter
        print(f"      {doc:9s} A={len(set(a)):2d} types  B={len(set(bb)):2d} types  "
              f"shared={inter:2d}  onlyA={sorted(set(a)-set(bb))}  "
              f"onlyB={sorted(set(bb)-set(a))}")
    print(f"      aggregate: {agree} shared of {tot_a} (A) / {tot_b} (B) types "
          f"=> Jaccard {agree/(tot_a+tot_b-agree):.3f}")
    print("      Each only-A / only-B item is a sign-group the reading would have to")
    print("      place, and the two editions do not agree that it exists.")

    # (d) the gloss is already in the edition
    print("\n  (d) the digital edition already carries the glosses under test:")
    for f in ["HT117a", "HT88", "HT94b", "HT15", "HT34", "HT85a"]:
        if f not in A:
            continue
        tw = A[f].get("translatedWords") or []
        g = sorted({w for w in tw if isinstance(w, str) and '"' in w})
        if g:
            print(f"      {f:7s} translatedWords contains: {g}")
    print("      'KI-RO -> owed' and 'U-MI-NA-SI -> owed?' are fields of the same file")
    print("      the claimant's held-out predictions were checked against.  A prediction")
    print("      scored against a labelled edition is not a held-out test.")

    # (e) A-DU polarity: the two frontier documents disagree
    print("\n  (e) A-DU: the claim's own two frontier documents assign opposite nodes.")
    adu = [(k, A[k].get("site"), A[k].get("support")) for k in A
           if "A-DU" in A[k]["transliteratedWords"]]
    print(f"      A-DU attestations in the corpus: {len(adu)}")
    for k, s, sup in sorted(adu):
        ws = A[k]["transliteratedWords"]
        i = ws.index("A-DU")
        nxt = ws[i+1:i+4]
        print(f"        {k:9s} {s:14s} {sup:10s} followed by {nxt}")
    print("      obligation-circuit note (2026-09-07): A-DU = RENDERED / PAID /")
    print("        FULFILLED, the positive complement of KI-RO, with DA-DU-MA-TA")
    print("        occupying the upstream ASSESSED node.")
    print("      scribe-9 dossier (2026-09-08) and HANDOVER: A-DU = ASSESSED /")
    print("        ACTIVATED OBLIGATION / ON-BOOK LIABILITY, i.e. the upstream node.")
    print("      Those are the two different arrows of the same state machine. The")
    print("      architecture diagram is not identified by the evidence offered for it.")


def p5_most_generous_coverage(A, tablets):
    """Score coverage the way most favourable to the claim, so the figure cannot be
    dismissed as an unfair denominator."""
    print("\n" + "=" * 78)
    print("P5  COVERAGE, SCORED THE WAY MOST FAVOURABLE TO THE CLAIM")
    print("=" * 78)
    named = set()
    for p in sorted(glob.glob(os.path.join(CLAIM_DIR, "*.md"))
                    + glob.glob(os.path.join(CLAIM_DIR, "*.csv"))):
        txt = open(p, encoding="utf-8").read()
        for m in re.finditer(r'\bHT\s?(\d+)', txt):
            named.add("HT" + m.group(1))
    namedht = sorted(n for n in named if n in tablets)
    print(f"  denominator = HT tablets only (not the whole corpus): {len(tablets)}")
    print(f"  HT tablets the claim names anywhere                 : {len(namedht)} "
          f"= {100.0*len(namedht)/len(tablets):.1f}%")
    s9 = sorted(t for t, d in tablets.items() if "HT Scribe 9" in d["scribe"])
    print(f"  HT tablets in the dossier proper                    : {len(s9)} "
          f"= {100.0*len(s9)/len(tablets):.1f}%")
    tok_all = sum(1 for t in tablets for w in tablets[t]["words"] if is_word(w))
    tok_s9 = sum(1 for t in s9 for w in tablets[t]["words"] if is_word(w))
    tok_nm = sum(1 for t in namedht for w in tablets[t]["words"] if is_word(w))
    print(f"  HT-tablet sign-group tokens: all {tok_all}; on named tablets {tok_nm} "
          f"({100.0*tok_nm/tok_all:.1f}%); on Scribe 9 {tok_s9} "
          f"({100.0*tok_s9/tok_all:.1f}%)")
    print("\n  On every denominator, nothing in the claim assigns a phonetic value, a")
    print("  morpheme, a word class or a language to any of these sign-groups. The")
    print("  pre-registered criterion asks for a LINGUISTIC decipherment accounting for")
    print("  a substantial portion of the corpus; the claim's own HANDOVER forbids the")
    print("  phrase 'Linear A deciphered' and labels itself not a phonetic decipherment")
    print("  and not a language-family solve.")


def p6_totals(A):
    """Independent re-derivation of the totals the dossier's architecture quotes, so the
    verdict does not borrow the 2026-09-25 session's numbers.  Sectioning rule, fixed
    before looking at outcomes: a block is every integer numeral since the previous
    KU-RO / PO-TO-KU-RO on the same face; erasures [[...]] are excluded; fractions are
    excluded and the block is then marked as fraction-bearing."""
    print("\n" + "=" * 78)
    print("P6  DO THE DOSSIER'S CONTROL TOTALS CLOSE? (independent re-derivation)")
    print("=" * 78)
    FRAC = re.compile(r'[¹²³⁴⁵⁶⁷⁸⁹'
                      r'₀-₉⁄]')
    ok = bad = 0
    for f in ["HT85a", "HT85b", "HT87", "HT88", "HT94a", "HT94b", "HT112a", "HT112b",
              "HT117a", "HT117b", "HT119", "HT122a", "HT122b", "HT128a", "HT128b",
              "HT132", "HT135a", "HT135b", "HT2", "HT28a", "HT28b"]:
        if f not in A:
            print(f"  {f:8s} absent from the corpus")
            continue
        ws = A[f]["transliteratedWords"]
        acc, frac = [], False
        for i, w in enumerate(ws):
            if w.startswith("[["):
                continue
            if w in ("KU-RO", "PO-TO-KU-RO"):
                nxt = ws[i + 1] if i + 1 < len(ws) else ""
                stated = int(nxt) if re.fullmatch(r'\d+', nxt or "") else None
                if stated is not None:
                    s = sum(acc)
                    flag = "closes" if s == stated else f"OFF by {s-stated:+d}"
                    if s == stated:
                        ok += 1
                    else:
                        bad += 1
                    print(f"  {f:8s} {w:11s} {len(acc):2d} preceding integers sum "
                          f"{s:6d}   stated {stated:6d}   {flag}"
                          f"{'   [fraction-bearing block]' if frac else ''}")
                acc, frac = [], False
            elif re.fullmatch(r'\d+', w):
                acc.append(int(w))
            elif FRAC.search(w) and not is_word(w):
                frac = True
    print(f"\n  blocks closing exactly: {ok}; blocks off: {bad}")
    print("  HT122 stated hierarchy 31 + KU-DA 1 + 65 = PO-TO-KU-RO 97 is arithmetic over")
    print("  STATED totals only; none of HT122's three stated totals is the sum of the")
    print("  entries it stands over.")
    print("  Agrees with dbourdeau/cyphersolver, which checked 35 KU-RO/PO-TO-KU-RO with")
    print("  exact fractions over five windows and found 10 balance, naming HT94a 1,")
    print("  HT119 1 and the HT122 grand total among the failures.")


def main():
    A = load_corpus()
    faces = ht_tablet_faces(A)
    tablets = merge_sides(A, faces)
    s9 = p1_coverage(A, tablets)
    p2_label_permutation(tablets, s9)
    p3_prior_art_ablation(tablets, s9)
    p4_ceiling(A, tablets)
    p5_most_generous_coverage(A, tablets)
    p6_totals(A)


if __name__ == "__main__":
    main()
