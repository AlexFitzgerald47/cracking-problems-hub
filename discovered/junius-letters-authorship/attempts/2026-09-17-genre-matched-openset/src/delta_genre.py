#!/usr/bin/env python3
"""Delta again, with the register confound removed, plus the matched in-volume controls.

delta.py pools each author's documents into one centroid. That is unfair in a specific
direction: authors whose published formal prose happens to be digitised (Burke,
Johnson, Hume) get centroids pulled toward the formal register, and Junius's public
letters are formal register. Part of their apparent closeness to Junius is therefore
the genre of their surviving corpus, not their hand.

Here every class is an (author, register) cell, so like is compared with like and a
candidate can be read off against same-register rivals.

The second half runs the controls that the 1772 Woodfall volume supplies for free, and
they are the most informative thing in this file:

  POSITIVE CONTROL -- Philo Junius. Junius's own acknowledged second signature. If the
  method cannot put Philo Junius nearer to Junius than to fifteen other writers, it has
  no power to detect authorship at these sample sizes and nothing else here means
  anything.

  NEGATIVE CONTROLS -- Sir William Draper and John Horne. Named opponents, printed in
  the same volume, same genre, same topic, same year, same press. They are the only
  samples in the whole study where everything except the author is held constant.
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
CORP = os.path.join(HERE, "..", "data", "corpus")

JUNIUS_SIDE = ("Junius", "Philo_Junius", "William_Draper", "Modestus",
               "John_Horne_Tooke", "Anti_Sejanus")


def small_samples():
    """Junius-volume authors too small to chunk at 2,000 words are pooled whole and
    kept as single documents; their word counts are reported so the reader can weigh
    them. Delta on a 1,700-word sample is noisy and is not treated as equivalent."""
    out = []
    for name, tag in (("junius_1772_wikisource.jsonl", "junius_1772_wikisource"),
                      ("junius_1813_ocr.jsonl", "junius_1813_ocr")):
        p = os.path.join(CORP, name)
        if not os.path.exists(p):
            continue
        by = defaultdict(list)
        for d in C.load_jsonl(name):
            by[d["author"]].append(d["text"])
        for a, texts in by.items():
            if a == "Junius":
                continue
            joined = " ".join(texts)
            w = joined.split()
            chs = C.chunk(joined, CHUNK)
            if chs:
                for i, ch in enumerate(chs):
                    out.append(dict(author=a, genre="public_letter", source=tag,
                                    chunk=i, text=ch, n_words=CHUNK))
            elif len(w) >= 900:
                out.append(dict(author=a, genre="public_letter", source=tag,
                                chunk=0, text=joined, n_words=len(w)))
    return out


def build():
    docs = list(C.load_jsonl("panel_chunks.jsonl")) + junius_chunks() + small_samples()
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
    return docs, feats, (X - mu) / sd


def main():
    docs, feats, Z = build()
    cls = [f"{d['author']}|{d['genre']}" for d in docs]
    known = [i for i, d in enumerate(docs) if d["author"] not in JUNIUS_SIDE]
    kcls = sorted({cls[i] for i in known})
    print(f"{len(docs)} documents; {len(feats)} features; "
          f"{len(kcls)} known (author, register) classes\n")

    def cents(exclude=None, drop=None):
        g = defaultdict(list)
        for i in known:
            if i == exclude or cls[i] == drop:
                continue
            g[cls[i]].append(Z[i])
        return {k: np.mean(v, 0) for k, v in g.items()}

    def rank(z, c):
        return sorted(((float(np.abs(z - v).mean()), k) for k, v in c.items()))

    # power
    ok = sum(rank(Z[i], cents(exclude=i))[0][1] == cls[i] for i in known)
    print(f"POWER: leave-one-out accuracy over (author, register) classes "
          f"{ok}/{len(known)} = {ok/len(known):.3f}  (chance {1/len(kcls):.3f})\n")

    # absent-class null
    null = []
    for k in kcls:
        idx = [i for i in known if cls[i] == k]
        c = cents(drop=k)
        null += [rank(Z[i], c)[0][0] for i in idx]
    null = np.array(null)
    print(f"ABSENT-CLASS NULL: nearest-Delta median {np.median(null):.3f}, "
          f"5th {np.percentile(null,5):.3f}, 95th {np.percentile(null,95):.3f}\n")

    full = cents()

    def report(author, label):
        idx = [i for i, d in enumerate(docs) if d["author"] == author]
        if not idx:
            return None
        agg = defaultdict(list)
        near = []
        for i in idx:
            r = rank(Z[i], full)
            near.append(r[0][0])
            for dd, k in r:
                agg[k].append(dd)
        order = sorted(((float(np.mean(v)), k) for k, v in agg.items()))
        nwords = sum(d.get("n_words", CHUNK) for j, d in enumerate(docs) if j in idx)
        print(f"--- {label}: {len(idx)} docs, {nwords} words")
        for r_, (dd, k) in enumerate(order[:6], 1):
            print(f"      {r_}. {k:38s} {dd:.3f}")
        fr = [r_ for r_, (dd, k) in enumerate(order, 1) if k.startswith("Philip_Francis")]
        for r_ in fr:
            print(f"      ... Philip_Francis cells at rank "
                  f"{', '.join(str(x) for x in fr)} of {len(order)}")
            break
        nn = float(np.median(near))
        print(f"      median nearest Delta {nn:.3f} -> {(null <= nn).mean()*100:.0f}th "
              f"percentile of the absent-class null")
        return order

    print("THE TARGET AND ITS MATCHED CONTROLS "
          "(all from the same 1772/1813 Junius volumes)\n")
    report("Junius", "JUNIUS (target)")
    print()
    report("Philo_Junius", "PHILO JUNIUS (positive control: Junius's own second signature)")
    print()
    report("William_Draper", "WILLIAM DRAPER (negative control: opponent, same volume)")
    print()
    report("John_Horne_Tooke", "JOHN HORNE (negative control: opponent, same volume)")

    # Does the positive control actually attach to Junius?
    print("\n\nPOSITIVE-CONTROL TEST -- is Philo Junius nearer to Junius than to anyone else?")
    jidx = [i for i, d in enumerate(docs) if d["author"] == "Junius"]
    jc = np.mean(Z[jidx], 0)
    c2 = dict(full)
    c2["Junius|public_letter"] = jc
    for a in ("Philo_Junius", "William_Draper", "John_Horne_Tooke"):
        idx = [i for i, d in enumerate(docs) if d["author"] == a]
        if not idx:
            continue
        agg = defaultdict(list)
        for i in idx:
            for dd, k in rank(Z[i], c2):
                agg[k].append(dd)
        order = sorted(((float(np.mean(v)), k) for k, v in agg.items()))
        jr = [r_ for r_, (dd, k) in enumerate(order, 1) if k == "Junius|public_letter"][0]
        print(f"   {a:20s} -> Junius ranks {jr} of {len(order)}   "
              f"(nearest: {order[0][1]}, {order[0][0]:.3f})")

    json.dump(dict(loo_accuracy=ok / len(known), n_classes=len(kcls),
                   absent_null_median=float(np.median(null))),
              open(os.path.join(RES, "delta_genre.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
