#!/usr/bin/env python3
"""
2026-09-25 refutation session, Linear A "labor-liability / obligation-circuit" dossier.

Independent reproduction from raw, GORILA-derived corpus data:
  witness A : mwenge/lineara.xyz  LinearAInscriptions.js  (Godart-Olivier GORILA via
              G. Douros's tabulation; carries numerals, scribe and findspot metadata)
  witness B : SigLA (Salgarella & Castellan), https://sigla.phis.me/  per-document
              "word view" pages (sign-groups only, no numerals)

Nothing here reads the claimant's analysis/*.csv or analysis/*.md files.

Usage:
    python3 refute_scribe9.py fetch     # download both witnesses into ./data
    python3 refute_scribe9.py run       # run the checks
"""
import json, os, re, html, sys, random, urllib.request, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
A_URL = "https://raw.githubusercontent.com/mwenge/lineara.xyz/master/LinearAInscriptions.js"
SIGLA = "https://sigla.phis.me/document/{}/index-word.html"
SIGLA_DOCS = ["HT 85a","HT 85b","HT 87","HT 88","HT 94a","HT 94b",
              "HT 117a","HT 117b","HT 119","HT 122a","HT 122b"]

NUM = re.compile(r'^[\d¹²³⁴⁵⁶⁷⁸⁹⁰⁄₀₁₂₃₄₅₆₇₈₉/≈\s\.\-]+$')
DIVIDER = "\U00010101"      # Aegean word separator dot, rendered 𐄁


# ---------------------------------------------------------------- witnesses
def fetch():
    os.makedirs(DATA, exist_ok=True)
    def get(u, p):
        req = urllib.request.Request(u, headers={"User-Agent": "cracking-problems-hub/validator"})
        with urllib.request.urlopen(req, timeout=120) as r:
            open(p, "wb").write(r.read())
        print("ok", p)
    get(A_URL, os.path.join(DATA, "LinearAInscriptions.js"))
    for d in SIGLA_DOCS:
        get(SIGLA.format(urllib.parse.quote(d)),
            os.path.join(DATA, "sigla_" + d.replace(" ", "_") + ".html"))


def load_a():
    s = open(os.path.join(DATA, "LinearAInscriptions.js"), encoding="utf-8").read()
    start = s.index("new Map(") + len("new Map(")
    end = s.index("]);", start) + 1
    body = s[start:end]
    body = re.sub(r',(\s*[\]\}])', r'\1', body)                       # trailing commas
    body = re.sub(r'\\u\{([0-9a-fA-F]+)\}', lambda m: chr(int(m.group(1), 16)), body)
    return dict(json.loads(body))


def load_b():
    out = {}
    for d in SIGLA_DOCS:
        p = os.path.join(DATA, "sigla_" + d.replace(" ", "_") + ".html")
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        txt = html.unescape(re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', s)))
        seqs = re.findall(r'Sequence #\d+(.*?)\(\d+ signs?\)', txt)
        out[d] = [re.sub(r'\s+', '', x) for x in seqs]
    return out


# ---------------------------------------------------------------- helpers
def is_num(t):
    return bool(t) and bool(NUM.match(t)) and any(c.isdigit() or c in "¹²³⁴⁵⁶⁷⁸⁹⁰⁄" for c in t)

def to_val(t):
    t = t.strip()
    if re.fullmatch(r'\d+', t):
        return float(t)
    return None

def is_word(t):
    """A syllabic sign-group: not a numeral, divider, newline, ruling or ideogram."""
    if t in ("\n", DIVIDER, "—", "", " "):
        return False
    if is_num(t):
        return False
    if re.match(r'^(GRA|VIN|OLE|OLIV|CYP|FIC|VIR|MUL|BOS|OVIS|CAP|SUS|AROM|TELA|'
                r'HORD|double|mina)', t):
        return False
    if t.startswith("*") or t.startswith("\U0001076b"):
        return False
    return True

def ht_tablets(A):
    return {k: v for k, v in A.items()
            if v.get("site") == "Haghia Triada" and v.get("support") == "Tablet"
            and any(is_word(w) for w in v["transliteratedWords"])}

def base(name):
    m = re.match(r'^(HT\d+)', name)
    return m.group(1) if m else name


# ---------------------------------------------------------------- checks
def check_scribe9(A):
    print("\n### C0  Scribe-9 set and findspots, straight from the corpus metadata")
    s9 = sorted(k for k, v in A.items() if v.get("scribe") == "HT Scribe 9")
    print("  HT Scribe 9 faces :", s9)
    print("  distinct tablets  :", sorted(set(base(k) for k in s9)))
    for k in s9:
        pass
    fs = collections.Counter(A[k].get("findspot") for k in s9)
    print("  findspots         :", dict(fs))
    for t in ["HT88", "HT95", "HT86", "HT1", "HT15", "HT34", "HT30", "HT37"]:
        sc = {A[k].get("scribe") for k in A if base(k) == t}
        print(f"  scribe of {t:6s}   : {sc}")
    return s9


def kuro_blocks(ws):
    """Split a face at each KU-RO / PO-TO-KU-RO and return
    (entries_in_the_block, stated_total).  An entry is any numeral seen since the
    previous total marker."""
    acc, out = [], []
    for i, w in enumerate(ws):
        if w in ("KU-RO", "PO-TO-KU-RO"):
            nxt = ws[i+1] if i+1 < len(ws) else None
            out.append((list(acc), to_val(nxt) if nxt else None, w))
            acc = []
        elif to_val(w) is not None:
            acc.append(to_val(w))
    return out


def check_arithmetic(A):
    print("\n### C1  arithmetic audit of every total the dossier quotes")
    print("     (a block is everything since the previous total marker on that face)")
    for t in ["HT85a", "HT88", "HT94a", "HT94b", "HT117a", "HT119", "HT122a", "HT122b",
              "HT2", "HT97"]:
        if t not in A:
            print(f"  {t}: absent"); continue
        ws = A[t]["transliteratedWords"]
        for ents, tot, mark in kuro_blocks(ws):
            if tot is None:
                continue
            ssum = sum(ents)
            flag = "OK" if abs(ssum - tot) < 1e-9 else f"MISMATCH ({ssum-tot:+g})"
            print(f"  {t:7s} {mark:11s} sum of {len(ents):2d} preceding numerals "
                  f"= {ssum:7g}   stated = {tot:g}   {flag}")
    print("  HT122 stated-subtotal hierarchy: 31 + KU-DA 1 + 65 =", 31 + 1 + 65,
          "= PO-TO-KU-RO 97   OK (this is arithmetic over stated totals only)")


def check_ht85(A, B):
    print("\n### C2  HT85: is '66 = 11 gangs of six' anything more than 66 % 11 == 0 ?")
    a = A["HT85a"]["transliteratedWords"]; b = A["HT85b"]["transliteratedWords"]
    ents_a = [to_val(w) for w in a if to_val(w) is not None and w != "66"]
    print("  HT85a contributor amounts (witness A):", ents_a, "sum", sum(x for x in ents_a))
    print("  -> none of 5, 3, 4 is a multiple of 6; the 66 does not partition into sixes")
    nb_a = sum(1 for w in b if is_word(w)) - 1     # minus the KI-KI-RA-JA header
    print("  HT85b entries, witness A (Douros/GORILA):", nb_a)
    if "HT 85b" in B:
        print("  HT85b entries, witness B (SigLA)         :", len(B["HT 85b"]) - 1,
              "  sequences:", B["HT 85b"])
    print("  every HT85b entry in witness A carries the numeral 1, not 6:",
          [w for w in b if to_val(w) is not None][:12])


def check_ht119(A):
    print("\n### C3  HT119: is '*327 34 : VIR 68 = 1:2' a statement or a coincidence?")
    ws = A["HT119"]["transliteratedWords"]
    print("  ", " ".join(ws).replace(" \n ", " | "))
    vals = [to_val(w) for w in ws if to_val(w) is not None]
    body, total = vals[:-1], vals[-1]
    print("  list items:", body, " sum =", sum(body), " stated KU-RO =", total)
    pairs = [(x, y) for i, x in enumerate(body) for y in body[i+1:]
             if x and y and (abs(y - 2*x) < 1e-9 or abs(x - 2*y) < 1e-9)]
    print("  exact 2:1 pairs anywhere in this 9-item list:", pairs)


def block_headers(A):
    """Every word standing immediately before a run of '<word> <numeral>' entries that
    is closed by KU-RO -- i.e. every competitor for the slot KI-RO is said to occupy."""
    found = []
    for k, v in ht_tablets(A).items():
        ws = [w for w in v["transliteratedWords"] if w not in ("\n", "\u2014")]
        for i, w in enumerate(ws):
            if w != "KU-RO":
                continue
            j = i - 1; n = 0
            while j - 1 >= 0 and is_word(ws[j-1]) and to_val(ws[j]) is not None:
                n += 1; j -= 2
            if n < 2:
                continue
            # walk back over dividers to the heading word
            b = j
            while b >= 0 and ws[b] == DIVIDER:
                b -= 1
            head = ws[b] if b >= 0 and is_word(ws[b]) else "(no heading)"
            found.append((head, k, n))
    return found


def check_competitors(A):
    print("\n### C4  competitor count: which words head a KU-RO-closed list of "
          "'<name> <numeral>' entries?")
    found = block_headers(A)
    words = collections.Counter(h for h, k, n in found)
    for h, k, n in sorted(found, key=lambda x: (-x[2], x[0])):
        print(f"    heading {h:14s} on {k:8s} over {n} entries")
    print("  distinct headings in that slot:", len(words), dict(words))
    print("  -> KI-RO heads", words.get("KI-RO", 0), "of", len(found), "such blocks")


def check_next_token(A):
    print("\n### C5  background rate: does 'numeral after X vs divider after X' single "
          "KI-RO out?")
    prof = collections.defaultdict(lambda: [0, 0, 0])   # numeral, divider, other
    for k, v in ht_tablets(A).items():
        ws = [w for w in v["transliteratedWords"] if w != "\n"]
        for i, w in enumerate(ws):
            if not is_word(w):
                continue
            nxt = ws[i+1] if i+1 < len(ws) else None
            if nxt is None:                 prof[w][2] += 1
            elif to_val(nxt) is not None:   prof[w][0] += 1
            elif nxt == DIVIDER:            prof[w][1] += 1
            else:                           prof[w][2] += 1
    both = [(w, c) for w, c in prof.items() if c[0] >= 1 and c[1] >= 1]
    print("  HT word types with >=4 occurrences:",
          sum(1 for w, c in prof.items() if sum(c) >= 4))
    print("  ... of those, how many show BOTH a numeral-following and a divider-following "
          "occurrence (i.e. would score a perfect 'two-construction grammar' by the same "
          "rule):", sum(1 for w, c in prof.items() if sum(c) >= 4 and c[0] and c[1]))
    for w in ["KI-RO", "KU-RO", "A-DU", "KA-PA", "SA-RA₂", "MA-KA-RI-TE", "U-MI-NA-SI"]:
        if w in prof:
            print(f"    {w:12s} numeral-next {prof[w][0]:3d}  divider-next {prof[w][1]:3d}"
                  f"  other {prof[w][2]:3d}")
    print("  full list of types showing both patterns (n>=4):",
          sorted(w for w, c in prof.items() if sum(c) >= 4 and c[0] and c[1]))


def wordsets(A):
    by_t = {}
    for k, v in ht_tablets(A).items():
        by_t.setdefault(base(k), set()).update(
            w for w in A[k]["transliteratedWords"] if is_word(w))
    return by_t


ADMIN = {"KU-RO", "PO-TO-KU-RO", "KI-RO", "KU-DA", "A-DU", "KA-PA", "SA-RA\u2082"}


def wordsets_strict(A):
    """Only multi-sign sign-groups, excluding the universal administrative operators.
    This is the set a claim about 'repeated personnel/unit names' actually rests on."""
    by_t = {}
    for k, v in ht_tablets(A).items():
        by_t.setdefault(base(k), set()).update(
            w for w in A[k]["transliteratedWords"]
            if is_word(w) and "-" in w and w not in ADMIN)
    return by_t


def cohesion_sets(tabs, by_t):
    """number of word types attested on >=2 distinct tablets of the set"""
    c = collections.Counter()
    for t in tabs:
        for w in by_t[t]:
            c[w] += 1
    return sum(1 for w, n in c.items() if n >= 2), sorted(w for w, n in c.items() if n >= 2)


def check_permutation(A, seed=20260925, N=20000):
    print("\n### C6  LABEL PERMUTATION on the post-hoc split (board attack (a))")
    by_t = wordsets(A)
    all_t = sorted(by_t)
    s9 = sorted(set(base(k) for k, v in A.items() if v.get("scribe") == "HT Scribe 9"
                    and base(k) in by_t))
    obs, shared = cohesion_sets(s9, by_t)
    print(f"  Scribe-9 tablets in play: {s9}")
    print(f"  OBSERVED cohesion (word types on >=2 of the {len(s9)} tablets) = {obs}")
    print(f"           shared types = {shared}")
    size = {}
    for k, v in ht_tablets(A).items():
        size[base(k)] = size.get(base(k), 0) + sum(1 for w in v['transliteratedWords'] if is_word(w))
    s9size = sum(size[t] for t in s9)
    print(f"  Scribe-9 word tokens = {s9size}; HT tablet pool = {len(all_t)} tablets, "
          f"{sum(size.values())} word tokens")

    rng = random.Random(seed)
    draws = []
    for _ in range(N):
        draws.append(cohesion_sets(rng.sample(all_t, len(s9)), by_t)[0])
    p1 = (sum(1 for d in draws if d >= obs) + 1) / (N + 1)
    draws.sort()
    print(f"  null (i)  {len(s9)} random HT tablets      : mean {sum(draws)/N:.2f}  "
          f"95% [{draws[int(.025*N)]}, {draws[int(.975*N)]}]  p = {p1:.4f}")

    draws2 = []; tries = 0
    while len(draws2) < 5000 and tries < 2000000:
        tries += 1
        pick = rng.sample(all_t, len(s9))
        if abs(sum(size[t] for t in pick) - s9size) <= 0.10 * s9size:
            draws2.append(cohesion_sets(pick, by_t)[0])
    if draws2:
        draws2.sort(); n2 = len(draws2)
        p2 = (sum(1 for d in draws2 if d >= obs) + 1) / (n2 + 1)
        print(f"  null (ii) size-matched (+/-10%), n={n2} of {tries} tries: "
              f"mean {sum(draws2)/n2:.2f}  95% [{draws2[int(.025*n2)]}, "
              f"{draws2[int(.975*n2)]}]  p = {p2:.4f}")
    else:
        print("  null (ii) size-matched: no draws")

    # --- same two nulls on the strict statistic (multi-sign names only)
    st = wordsets_strict(A)
    all_s = sorted(st)
    obs_s, shared_s = cohesion_sets([t for t in s9 if t in st], st)
    print(f"  STRICT statistic (multi-sign names only, admin operators dropped): "
          f"observed {obs_s}  {shared_s}")
    sz = {t: len(st[t]) for t in all_s}
    tgt = sum(sz[t] for t in s9 if t in st)
    d3 = [cohesion_sets(rng.sample(all_s, len(s9)), st)[0] for _ in range(N)]
    pS = (sum(1 for d in d3 if d >= obs_s) + 1) / (N + 1)
    d3.sort()
    print(f"    null  {len(s9)} random HT tablets : mean {sum(d3)/N:.2f} "
          f"95% [{d3[int(.025*N)]}, {d3[int(.975*N)]}]  p = {pS:.4f}")
    d4 = []; tr = 0
    while len(d4) < 5000 and tr < 2000000:
        tr += 1
        pick = rng.sample(all_s, len(s9))
        if abs(sum(sz[t] for t in pick) - tgt) <= 0.10 * max(tgt, 1):
            d4.append(cohesion_sets(pick, st)[0])
    if d4:
        d4.sort(); n4 = len(d4)
        pS2 = (sum(1 for d in d4 if d >= obs_s) + 1) / (n4 + 1)
        print(f"    null  size-matched (+/-10%), n={n4}: mean {sum(d4)/n4:.2f} "
              f"95% [{d4[int(.025*n4)]}, {d4[int(.975*n4)]}]  p = {pS2:.4f}")

    exc = ["HT94", "HT117"]; ordn = ["HT85", "HT87", "HT122"]
    def cross(e, o):
        we = set().union(*[by_t[t] for t in e]); wo = set().union(*[by_t[t] for t in o])
        return len(we & wo), sorted(we & wo)
    obs3, sh3 = cross(exc, ordn)
    pool = exc + ordn
    ds = []
    for _ in range(5000):
        p = pool[:]; rng.shuffle(p)
        ds.append(cross(p[:2], p[2:])[0])
    p3 = (sum(1 for d in ds if d >= obs3) + 1) / 5001
    print(f"  null (iii) permute exception/ordinary label inside Scribe 9: "
          f"observed {obs3} shared types {sh3}, null mean {sum(ds)/len(ds):.2f}, p = {p3:.4f}")


def check_abbrev(A):
    print("\n### C7  the abbreviation trap")
    toks = collections.Counter()
    for k, v in A.items():
        if v.get("site") != "Haghia Triada":
            continue
        for w in v["transliteratedWords"]:
            if w in ("\n", DIVIDER, "—"):
                continue
            toks[w] += 1
    words = {w: c for w, c in toks.items() if is_word(w)}
    one = {w: c for w, c in words.items() if "-" not in w and len(w) <= 3}
    print(f"  HT word tokens {sum(words.values())}, of which one-syllabogram "
          f"{sum(one.values())} = {100*sum(one.values())/sum(words.values()):.1f}%")
    print("  top one-sign tokens:", collections.Counter(one).most_common(12))
    # where do they sit?
    onsupport = collections.Counter()
    for k, v in A.items():
        if v.get("site") != "Haghia Triada":
            continue
        for w in v["transliteratedWords"]:
            if is_word(w) and "-" not in w and len(w) <= 3:
                onsupport[v.get("support")] += 1
    print("  one-sign word tokens by support:", dict(onsupport))
    print("  one-sign 'entities' inside the dossier's own personnel lists:")
    for t in ["HT85b", "HT122a", "HT94a", "HT94b"]:
        got = [w for w in A[t]["transliteratedWords"] if is_word(w) and "-" not in w and len(w) <= 3]
        print(f"    {t}: {got}")


def check_divisibility(A):
    print("\n### C8  base rate of the HT85 move: does a KU-RO total on one face divide "
          "evenly by the entry count on the other face?")
    by_t = collections.defaultdict(dict)
    for k, v in ht_tablets(A).items():
        m = re.match(r'^(HT\d+)([ab])$', k)
        if m:
            by_t[m.group(1)][m.group(2)] = v
    hits = tot = 0; ex = []
    for t, faces in sorted(by_t.items()):
        if set(faces) != {"a", "b"}:
            continue
        for src, dst in (("a", "b"), ("b", "a")):
            ws = faces[src]["transliteratedWords"]
            kur = [to_val(ws[i+1]) for i, w in enumerate(ws)
                   if w == "KU-RO" and i+1 < len(ws) and to_val(ws[i+1])]
            n = sum(1 for w in faces[dst]["transliteratedWords"] if is_word(w)) - 1
            for K in kur:
                if not K or n < 2:
                    continue
                tot += 1
                if K % n == 0 and K // n >= 2:
                    hits += 1; ex.append((t, src, K, n, int(K // n)))
    print(f"  {hits}/{tot} face pairs give an exact integer 'gang size' >= 2")
    for e in ex:
        print("    ", e)


def check_witness_divergence(A, B):
    print("\n### C9  two independent editions of the same tablets (PRACTICES: scan twice)")
    for doc in SIGLA_DOCS:
        key = doc.replace(" ", "")
        if key not in A or doc not in B:
            continue
        a = [w for w in A[key]["transliteratedWords"] if is_word(w)]
        b = [x for x in B[doc]]
        norm = lambda s: re.sub(r'[\[\]\?]', '', s.lower().replace("₂", "2").replace("₃", "3")
                                 .replace("*56", "pa3").replace("A", "*"))
        an = [norm(x) for x in a]; bn = [norm(x) for x in b]
        onlyA = [x for x in an if x not in bn]
        onlyB = [x for x in bn if x not in an]
        print(f"  {doc:9s} A={len(a):2d} words  B={len(b):2d} words   "
              f"only-A {onlyA}  only-B {onlyB}")


def main():
    A = load_a(); B = load_b()
    print(f"witness A: {len(A)} documents;  witness B: {len(B)} documents")
    check_scribe9(A)
    check_arithmetic(A)
    check_ht85(A, B)
    check_ht119(A)
    check_competitors(A)
    check_next_token(A)
    check_permutation(A)
    check_abbrev(A)
    check_divisibility(A)
    check_witness_divergence(A, B)


if __name__ == "__main__":
    import urllib.parse
    if len(sys.argv) > 1 and sys.argv[1] == "fetch":
        fetch()
    else:
        main()
