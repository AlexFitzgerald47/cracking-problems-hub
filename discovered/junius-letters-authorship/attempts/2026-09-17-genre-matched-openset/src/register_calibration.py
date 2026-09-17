#!/usr/bin/env python3
"""The last confound: register.

matched_controls.py showed the method separates Junius from Draper at 97% and puts
Philo Junius with Junius 22/22, with everything except the author held constant. It
also showed the edition/OCR effect is small (0.018 Delta) next to the author effect
(0.060). So the pipeline works, and the digitisation gap is not what defeats it.

What is NOT held constant between Junius and Philip Francis is register. Junius is
polemical newspaper prose; Francis's attested prose is private family correspondence.
This script measures the size of that gap directly, using the three authors who
appear in the panel in two registers (Burke, Johnson, Hume):

    A = same author, different register      <- the gap Junius/Francis must survive
    B = different author, same register      <- the signal we are trying to detect

If A >= B, then a Junius-to-Francis Delta cannot distinguish "different author" from
"same author writing in a different register", and no ranking of candidates built on
cross-register comparison is evidence. That would be a power failure, and it would
apply to every published stylometric treatment of this problem that compares Junius's
polemic with Francis's correspondence -- including, on the face of it, Ellegard's.
"""
import json, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C
from funcwords import FUNCTION_WORDS
from delta import junius_chunks, CHUNK, N_FEATURES

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")


def main():
    docs = list(C.load_jsonl("panel_chunks.jsonl")) + junius_chunks()
    fw = set(FUNCTION_WORDS)
    tot, per = Counter(), []
    for d in docs:
        c = Counter(t for t in C.tokens(d["text"]) if t in fw)
        per.append(c)
        tot.update(c)
    feats = [w for w, _ in tot.most_common(N_FEATURES)]
    X = np.zeros((len(docs), len(feats)))
    for i, c in enumerate(per):
        s = sum(c.values()) or 1
        for j, w in enumerate(feats):
            X[i, j] = c[w] / s
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1e-12
    Z = (X - mu) / sd

    cells = defaultdict(list)
    for i, d in enumerate(docs):
        cells[(d["author"], d["genre"])].append(i)
    cents = {k: np.mean(Z[v], 0) for k, v in cells.items() if len(v) >= 8}

    def dl(a, b):
        return float(np.abs(a - b).mean())

    A, B = [], []
    print("A  SAME AUTHOR, DIFFERENT REGISTER")
    for (a1, g1), c1 in sorted(cents.items()):
        for (a2, g2), c2 in sorted(cents.items()):
            if a1 == a2 and g1 < g2:
                d = dl(c1, c2)
                A.append(d)
                print(f"   {a1:18s} {g1:16s} vs {g2:16s} {d:.3f}")
    print("\nB  DIFFERENT AUTHOR, SAME REGISTER")
    bylist = defaultdict(list)
    for (a, g), c in cents.items():
        bylist[g].append((a, c))
    for g, lst in sorted(bylist.items()):
        lst.sort()
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                B.append(dl(lst[i][1], lst[j][1]))
    for g, lst in sorted(bylist.items()):
        vals = []
        lst2 = sorted(lst)
        for i in range(len(lst2)):
            for j in range(i + 1, len(lst2)):
                vals.append(dl(lst2[i][1], lst2[j][1]))
        if vals:
            print(f"   {g:18s} n={len(vals):3d} pairs   "
                  f"median {np.median(vals):.3f}  min {min(vals):.3f}  max {max(vals):.3f}")

    A, B = np.array(A), np.array(B)
    print(f"\nA  same author, different register : n={len(A)}, median {np.median(A):.3f}, "
          f"range {A.min():.3f}-{A.max():.3f}")
    print(f"B  different author, same register : n={len(B)}, median {np.median(B):.3f}, "
          f"range {B.min():.3f}-{B.max():.3f}")
    overlap = (B <= np.median(A)).mean()
    print(f"\n{overlap*100:.0f}% of different-author same-register pairs are CLOSER than the")
    print(f"median same-author cross-register pair.")
    verdict = ("UNDERPOWERED: a cross-register comparison cannot separate author from register"
               if np.median(A) >= np.median(B) else
               "usable, but the register gap must be subtracted before any ranking is read")
    print(f"\nVERDICT: {verdict}")

    # where does Junius-to-Francis sit?
    jk = [k for k in cents if k[0] == "Junius"]
    fk = [k for k in cents if k[0] == "Philip_Francis"]
    print("\nJUNIUS -> FRANCIS, against those two distributions")
    for j in jk:
        for f in fk:
            d = dl(cents[j], cents[f])
            print(f"   {j} vs {f}: {d:.3f}   "
                  f"(percentile of A: {(A <= d).mean()*100:.0f}, of B: {(B <= d).mean()*100:.0f})")
    print("\nJUNIUS -> every same-register-as-Francis rival, for context")
    rows = []
    for (a, g), c in cents.items():
        if a in ("Junius", "Philo_Junius"):
            continue
        for j in jk:
            rows.append((dl(cents[j], c), a, g))
    rows.sort()
    for d, a, g in rows:
        mark = "  <-- CANDIDATE" if a == "Philip_Francis" else ""
        print(f"   {d:.3f}  {a:20s} {g}{mark}")

    json.dump(dict(same_author_cross_register=dict(n=len(A), median=float(np.median(A)),
                                                   min=float(A.min()), max=float(A.max())),
                   diff_author_same_register=dict(n=len(B), median=float(np.median(B)),
                                                  min=float(B.min()), max=float(B.max())),
                   verdict=verdict),
              open(os.path.join(RES, "register_calibration.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
