#!/usr/bin/env python3
"""Burrows's Delta on function words, with a leave-one-author-out open-set null.

Three things are measured, in this order, because the third is meaningless without
the first two:

  1. POWER. Leave-one-document-out attribution across the panel of known authors.
     If the method cannot recover authors whose identity is not in doubt, its verdict
     on Junius is worthless. Accuracy is reported overall and split by genre, because
     a method that is really sorting registers will show it here.

  2. THE OPEN-SET NULL. For each known author in turn, that author is REMOVED from
     the candidate set and their documents are attributed anyway. The resulting
     distances are what a genuinely absent author looks like. Junius may well be an
     absent author -- the true writer of the letters need not be anyone whose prose
     survives in a digitised volume -- and this is the only way to tell that case
     from a real match.

  3. THE CANDIDATE. Junius's documents are scored against every author, Francis
     included, and the competitors are counted.

Delta is length-sensitive, so every document is exactly 2,000 words. It is also
sensitive to how many features are used, so the feature count is fixed in advance and
the same for every author -- a candidate searched at one budget against rivals
searched at another measures the budget, which is a documented failure mode on this
board.
"""
import json, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C
from funcwords import FUNCTION_WORDS

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
CORP = os.path.join(HERE, "..", "data", "corpus")
CHUNK = 2000
N_FEATURES = 120


def junius_chunks():
    """Junius's own public letters, re-chunked to the panel's 2,000-word unit."""
    out = []
    for name, tag in (("junius_1813_ocr.jsonl", "junius_1813_ocr"),
                      ("junius_1772_wikisource.jsonl", "junius_1772_wikisource")):
        p = os.path.join(CORP, name)
        if not os.path.exists(p):
            continue
        byauth = defaultdict(list)
        for d in C.load_jsonl(name):
            byauth[d["author"]].append(d["text"])
        for a, texts in byauth.items():
            joined = " ".join(texts)
            for i, ch in enumerate(C.chunk(joined, CHUNK)):
                out.append(dict(author=a, genre="public_letter", source=tag,
                                chunk=i, text=ch))
    return out


def build():
    docs = list(C.load_jsonl("panel_chunks.jsonl")) + junius_chunks()
    # feature set: the most frequent FUNCTION words in the pooled corpus
    tot = Counter()
    per = []
    for d in docs:
        c = Counter(t for t in C.tokens(d["text"]) if t in set(FUNCTION_WORDS))
        per.append(c)
        tot.update(c)
    feats = [w for w, _ in tot.most_common(N_FEATURES)]
    n = len(feats)
    X = np.zeros((len(docs), n))
    for i, c in enumerate(per):
        s = sum(c.values()) or 1
        for j, w in enumerate(feats):
            X[i, j] = c[w] / s
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1e-12
    Z = (X - mu) / sd
    return docs, feats, Z


def centroids(Z, labels, exclude_idx=None, drop_author=None):
    d = defaultdict(list)
    for i, a in enumerate(labels):
        if exclude_idx is not None and i == exclude_idx:
            continue
        if drop_author is not None and a == drop_author:
            continue
        d[a].append(Z[i])
    return {a: np.mean(v, axis=0) for a, v in d.items() if v}


def rank(z, cents):
    return sorted(((np.abs(z - c).mean(), a) for a, c in cents.items()))


def main():
    os.makedirs(RES, exist_ok=True)
    docs, feats, Z = build()
    labels = [d["author"] for d in docs]
    genres = [d["genre"] for d in docs]
    known = [i for i, d in enumerate(docs)
             if d["author"] not in ("Junius", "Philo_Junius", "William_Draper",
                                    "Modestus", "John_Horne_Tooke")]
    print(f"{len(docs)} documents of {CHUNK} words; {len(feats)} function-word features")
    print(f"{len(set(labels[i] for i in known))} known-author classes, "
          f"{len(known)} known-author documents\n")

    # ---- 1. POWER --------------------------------------------------------
    ok = 0
    per_genre = defaultdict(lambda: [0, 0])
    conf = Counter()
    for i in known:
        cents = centroids(Z[known], [labels[k] for k in known],
                          exclude_idx=known.index(i))
        pred = rank(Z[i], cents)[0][1]
        hit = pred == labels[i]
        ok += hit
        g = genres[i]
        per_genre[g][0] += hit
        per_genre[g][1] += 1
        if not hit:
            conf[(labels[i], pred)] += 1
    print("1. POWER -- leave-one-document-out attribution over known authors")
    print(f"   overall accuracy {ok}/{len(known)} = {ok/len(known):.3f}")
    for g, (h, t) in sorted(per_genre.items()):
        print(f"     {g:18s} {h:4d}/{t:4d} = {h/t:.3f}")
    print("   most common confusions:")
    for (t, p), c in conf.most_common(6):
        print(f"     {t} -> {p}: {c}")

    # ---- 2. OPEN-SET NULL ------------------------------------------------
    print("\n2. OPEN-SET NULL -- each author removed from the candidate set, then scored")
    print(f"   {'absent author':22s} {'docs':>5s} {'median nearest-wrong Delta':>27s}")
    null_d = []
    for a in sorted(set(labels[i] for i in known)):
        idx = [i for i in known if labels[i] == a]
        cents = centroids(Z[known], [labels[k] for k in known], drop_author=a)
        ds = [rank(Z[i], cents)[0][0] for i in idx]
        null_d += ds
        print(f"   {a:22s} {len(idx):5d} {np.median(ds):27.3f}")
    null_d = np.array(null_d)
    print(f"\n   absent-author nearest-Delta distribution: "
          f"median {np.median(null_d):.3f}, 5th pct {np.percentile(null_d,5):.3f}, "
          f"95th {np.percentile(null_d,95):.3f}")

    # for contrast: present-author nearest Delta
    pres = []
    for i in known:
        cents = centroids(Z[known], [labels[k] for k in known], exclude_idx=known.index(i))
        pres.append(rank(Z[i], cents)[0][0])
    pres = np.array(pres)
    print(f"   present-author nearest-Delta distribution: "
          f"median {np.median(pres):.3f}, 95th {np.percentile(pres,95):.3f}")

    # ---- 3. THE CANDIDATE ------------------------------------------------
    cents = centroids(Z[known], [labels[k] for k in known])
    for src in sorted({d["source"] for d in docs if d["author"] == "Junius"}):
        jidx = [i for i, d in enumerate(docs)
                if d["author"] == "Junius" and d["source"] == src]
        if not jidx:
            continue
        print(f"\n3. JUNIUS ({src}, {len(jidx)} documents) scored against every known author")
        agg = defaultdict(list)
        nearest = []
        for i in jidx:
            r = rank(Z[i], cents)
            nearest.append(r[0][0])
            for d_, a in r:
                agg[a].append(d_)
        order = sorted(((np.mean(v), a) for a, v in agg.items()))
        print(f"   {'rank':>4s}  {'author':22s} {'mean Delta':>10s}")
        for k, (d_, a) in enumerate(order, 1):
            mark = "   <-- CANDIDATE" if a == "Philip_Francis" else ""
            print(f"   {k:4d}  {a:22s} {d_:10.3f}{mark}")
        fr = [k for k, (d_, a) in enumerate(order, 1) if a == "Philip_Francis"]
        nn = np.median(nearest)
        pct = (null_d <= nn).mean()
        print(f"\n   Francis rank: {fr[0]} of {len(order)}")
        print(f"   Junius median nearest-author Delta = {nn:.3f}")
        print(f"   -> that is at the {pct*100:.0f}th percentile of the ABSENT-author null")
        print(f"      (present-author median {np.median(pres):.3f}, "
              f"absent-author median {np.median(null_d):.3f})")

    json.dump(dict(n_features=len(feats), features=feats,
                   loo_accuracy=ok / len(known),
                   per_genre={g: v for g, v in per_genre.items()},
                   absent_null=dict(median=float(np.median(null_d)),
                                    p5=float(np.percentile(null_d, 5)),
                                    p95=float(np.percentile(null_d, 95))),
                   present=dict(median=float(np.median(pres)),
                                p95=float(np.percentile(pres, 95)))),
              open(os.path.join(RES, "delta.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
