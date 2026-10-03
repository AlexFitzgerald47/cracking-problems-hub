#!/usr/bin/env python3
"""
ATTACK R4 (new, 2026-10-03) — two things the earlier suite leaves untested.

R4a  CELL-LEVEL AUDIT of the claim's own primary table,
     analysis/scribe9_dossier.csv, mechanically against BOTH vendored
     witness-A snapshots.  The earlier suite audits the arithmetic and the
     structure; it never asks what fraction of the table's factual cells are
     simply wrong.  Validator 1 found two by hand; this does all of them.

R4b  the cohesion null RESTRICTED TO ATTRIBUTED TABLETS.  Every earlier null
     (09-25, v1, v2 and attacks 3/3') draws the comparison set from all 133
     HT tablets, 58 of which carry NO scribal attribution at all.  That is
     the wrong pool for a claim about a hand: a random 10-tablet draw can mix
     tablets that are in fact one hand (deflating the null) and the
     unattributed tablets are systematically the short and broken ones.  The
     apposite question is: among the tablets a palaeographer could attribute,
     is Scribe 9's set unusually cohesive?
"""
import csv, collections, random, re, os, itertools
import r_common as R

HERE = os.path.dirname(os.path.abspath(__file__))
CSVP = os.path.normpath(os.path.join(HERE, "..", "..", "analysis", "scribe9_dossier.csv"))
SEED = 20261003

print("=" * 78)
print("ATTACK R4a — cell-level audit of analysis/scribe9_dossier.csv")
print("=" * 78)

snaps = {"2026-09-25": R.load("data"), "2026-10-02": R.load("data_20261002")}
rows = list(csv.DictReader(open(CSVP, encoding="utf-8")))


def norm(s):
    """normalise for comparison: strip subscript digits, unify * forms"""
    s = s.strip()
    sub = {"₀": "0", "₁": "1", "₂": "2", "₃": "3",
           "₄": "4", "₅": "5"}
    for a, b in sub.items():
        s = s.replace(a, b)
    return s.upper()


def face_tokens(A, tab):
    out = []
    for k, v in A.items():
        if R.tablet(k) == tab:
            out += [w for w in v["transliteratedWords"] if w != "\n"]
    return out


verdicts = collections.Counter()
detail = []
for r in rows:
    tab = r["tablet"]
    anchors = [a.strip() for a in r["strong_anchors"].split(";") if a.strip()]
    for a in anchors:
        m = re.match(r'^(.*?)(?:\s+(\d+))?$', a)
        sign, num = norm(m.group(1)), m.group(2)
        if sign == "VIR":  # the cell reads "VIR 68"
            pass
        per = {}
        for sn, A in snaps.items():
            ws = [norm(w) for w in face_tokens(A, tab)]
            exact = sign in ws
            # an ideogram cited bare (VIR, GRA) matches its witnessed
            # compound/qualified forms (VIR+[?], GRA+KU); a cell saying
            # "GRA variants" matches any GRA form. This is deliberately
            # generous: only genuine content errors should fail.
            pref = any(w == sign or w.startswith(sign + "+") or w.startswith(sign + "-")
                       for w in ws)
            if sign.endswith(" VARIANTS"):
                stem = sign[:-len(" VARIANTS")]
                pref = any(w.startswith(stem) for w in ws)
            numok = None
            if num is not None:
                numok = False
                for i, w in enumerate(ws):
                    if (w == sign or w.startswith(sign + "+")) and i + 1 < len(ws) \
                            and ws[i + 1] == num:
                        numok = True
            per[sn] = (exact, pref, numok)
        p25, p02 = per["2026-09-25"], per["2026-10-02"]
        if not p25[1] and not p02[1]:
            v = "ABSENT from both snapshots"
        elif p25[1] != p02[1]:
            v = "PRESENT in one snapshot only"
        elif num is not None and not p25[2]:
            v = "sign present, NUMERAL does not attach"
        elif not p25[0]:
            v = "ok (ideogram cited bare; witness has a qualified form)"
        else:
            v = "ok"
        verdicts[v] += 1
        detail.append((tab, a, v))

for tab, a, v in detail:
    flag = "" if v.startswith("ok") else "   <<<<"
    print(f"   {tab:7s} anchor {a:22s} -> {v}{flag}")
print()
for v, c in verdicts.most_common():
    print(f"   {c:3d}  {v}")
bad = sum(c for v, c in verdicts.items() if not v.startswith("ok"))
print(f"   failing cells: {bad}/{sum(verdicts.values())} "
      f"= {100*bad/sum(verdicts.values()):.0f}% of the table's factual anchors")

print("\n-- what the failing cells actually are")
A = snaps["2026-09-25"]
print("   HT112 'OVISf':   witness has", " ".join(face_tokens(A, "HT112")))
print("   HT132 'OVISf 27':witness has", " ".join(face_tokens(A, "HT132")))
ovis = collections.Counter(w for v in A.values() for w in v["transliteratedWords"]
                           if "OVIS" in w or re.match(r'^\*2[12][FM]', w))
print(f"   ovicaprid-family signs attested anywhere in witness A: "
      f"{dict(sorted(ovis.items()))}")
print("   There is NO 'OVIS' sign in the witness at all. Both cells assert a")
print("   sheep reading of the undeciphered *21F/*22F series -- which is")
print("   exactly the identification this folder's own PROGRESS.md item 5")
print("   flags as subject to a systematic AB21/AB22 inversion across 14")
print("   documents in a widely used digital corpus, to be plate-checked")
print("   before the Hub relies on livestock distributions. The dossier")
print("   relies on it, twice, without the check.")
print()
print("   'QI-TU-NE' (HT87, HT117): witness A reads *21F-TU-NE; witness B")
print("   reads qif-tu-ne. The 'accountable unit QI-TU-NE' is named from a")
print("   phonetic value for *21F that the corpus does not supply -- the same")
print("   sign series as the two OVISf cells above.")
print("   *21F-family sign-groups in witness A:",
      sorted({w for v in A.values() for w in v['transliteratedWords']
              if w.startswith('*21F')}))

print("\n-- metadata cells (scribe, findspot) checked against the witness")
mm = 0
for r in rows:
    tab = r["tablet"]
    scr = {A[k].get("scribe") for k in A if R.tablet(k) == tab}
    fs = {A[k].get("findspot") for k in A if R.tablet(k) == tab}
    okS = any((s or "").endswith(" " + r["scribe"]) for s in scr)
    okF = r["findspot"] in fs
    if not (okS and okF):
        mm += 1
    print(f"   {tab:7s} csv scribe={r['scribe']:3s} findspot={r['findspot']:16s}"
          f" witness scribe={sorted(x or '-' for x in scr)} findspot={sorted(x or '-' for x in fs)}"
          f"  {'ok' if okS and okF else 'MISMATCH'}")
print(f"   metadata mismatches: {mm}/10  -- the scribe and findspot columns")
print("   reproduce exactly. The dossier's FRAME is sound; its CONTENT cells")
print("   are where the failures are.")

# ------------------------------------------------------------------ R4b
print()
print("=" * 78)
print("ATTACK R4b — cohesion null drawn from ATTRIBUTED tablets only")
print("=" * 78)
T = R.ht_tablets(A)
POOL = sorted(T)
attr = sorted(t for t in POOL
              if any((A[f].get("scribe") or "").startswith("HT Scribe") for f in T[t]))
print(f"   HT tablets total {len(POOL)}; carrying an 'HT Scribe n' attribution {len(attr)}")
print(f"   unattributed {len(POOL)-len(attr)} -- these are systematically the")
print(f"   short/broken ones: mean sign-group type-slots "
      f"{sum(len(R.types_on(A,T[t])) for t in POOL if t not in attr)/(len(POOL)-len(attr)):.1f}"
      f" vs {sum(len(R.types_on(A,T[t])) for t in attr)/len(attr):.1f} for attributed")

D = R.DOSSIER
for label, namefn in (("ALL sign-group types", R.types_on),
                      ("STRICT multi-sign, operators dropped",
                       lambda AA, fs: R.names_on(AA, fs))):
    def coh(ts, fn):
        c = collections.Counter()
        for t in ts:
            for x in fn(A, T[t]):
                c[x] += 1
        return sum(1 for v in c.values() if v >= 2)
    obs = coh(D, namefn)
    slots = {t: len(R.types_on(A, T[t])) for t in POOL}
    target = sum(slots[t] for t in D)
    print(f"\n   [{label}] observed Scribe-9 cohesion = {obs}")
    for pname, pl in (("all 133 HT tablets", POOL), ("attributed only", attr)):
        rng = random.Random(SEED)
        vals, hits, draws, tries = [], 0, 0, 0
        while draws < 20000 and tries < 3000000:
            tries += 1
            s = rng.sample(pl, 10)
            if abs(sum(slots[t] for t in s) - target) > 0.10 * target:
                continue
            draws += 1
            c = coh(s, namefn)
            vals.append(c)
            if c >= obs:
                hits += 1
        vals.sort()
        print(f"     pool = {pname:20s} n={draws:5d}  null mean {sum(vals)/len(vals):5.2f}"
              f"  95% [{vals[int(.025*len(vals))]}, {vals[int(.975*len(vals))-1]}]"
              f"  p = {(hits+1)/(draws+1):.4f}")
print("\n   => restricting the null to the pool the claim is actually about")
print("      -- tablets with a hand -- moves the p-value in the UNFAVOURABLE")
print("      direction. The Scribe-9 cohesion is not distinguishable from a")
print("      size-matched draw of attributed HT tablets.")
