#!/usr/bin/env python3
"""Correct label-permutation nulls for the cross-register attribution numbers.

Two corrections to the first pass of shift_or_loss.py, both recorded rather than hidden:

1. Permuting whole author BLOCKS (author a's document set gets author b's name) leaves the
   set of centroids numerically identical and only renames them. Concentration of the
   prediction sink is therefore invariant under it, so that reference measured nothing.
   The null must reassign individual DOCUMENTS among the authors, preserving class sizes.

2. The 2026-09-17 session compared cross-register accuracy 0.108 against 1/n_candidates =
   0.125 and read it as "at or below chance". The classes here are strongly unbalanced --
   Burke has 174 formal chunks, Price 13 -- and that session's own limits section says
   baselines should be label-permutation, not 1/n. Under the correct null, 1/n is not the
   reference. This file computes the reference the headline needs.
"""
import json, os, sys, random
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K
from shift_or_loss import train_index, attribute

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
NPERM = 300


def shuffled_train(train, rng):
    """Reassign documents among authors, preserving each author's document count."""
    allidx = [i for v in train.values() for i in v]
    rng.shuffle(allidx)
    out, k = {}, 0
    for a in sorted(train, key=lambda a: -len(train[a])):
        n = len(train[a])
        out[a] = allidx[k:k + n]
        k += n
    return out


def main():
    rng = random.Random(7)
    docs, counts, ranked = K.load_docs()
    Z = K.build_Z(counts, ranked[:K.N_FEATURES])
    trainF = train_index(docs, K.FORMAL)
    trainL = train_index(docs, K.LETTERS)
    testL = [i for i, d in enumerate(docs)
             if d["genre"] in K.LETTERS and d["author"] in trainF
             and d["author"] not in ("Junius", "Philo_Junius")]
    testLL = [i for i, d in enumerate(docs)
              if d["genre"] in K.LETTERS and d["author"] in trainL
              and d["author"] not in ("Junius", "Philo_Junius")]

    out = {}
    print("test-set composition (letters of the 8 formal-register candidates):")
    for a, k in Counter(docs[i]["author"] for i in testL).most_common():
        print(f"   {a:<18} {k:>4}   ({k/len(testL):.3f})")
    print(f"   majority-class baseline = {max(Counter(docs[i]['author'] for i in testL).values())/len(testL):.3f}")
    out["test_composition"] = dict(Counter(docs[i]["author"] for i in testL))

    for name, train, test in (("cross_letters_to_formal", trainF, testL),
                              ("same_register_letters", trainL, testLL)):
        acc, _ = attribute(Z, docs, train, test)
        nulls = []
        for _ in range(NPERM):
            t2 = shuffled_train(train, rng)
            a2, _ = attribute(Z, docs, t2, test)
            nulls.append(a2)
        p = float(np.mean([n >= acc for n in nulls]))
        print(f"\n{name}: accuracy {acc:.3f}")
        print(f"   1/n_candidates            {1/len(train):.3f}")
        print(f"   document-permutation null median {np.median(nulls):.3f}, "
              f"p95 {np.percentile(nulls,95):.3f}, p = {p:.4f}")
        out[name] = dict(accuracy=acc, n_candidates=len(train), one_over_n=1/len(train),
                         null_median=float(np.median(nulls)),
                         null_p95=float(np.percentile(nulls, 95)), p=p,
                         n_test=len(test))

    # sink concentration under the correct null
    fr = []
    for _ in range(100):
        t2 = shuffled_train(trainF, rng)
        _, pr = attribute(Z, docs, t2, testL)
        fr.append(Counter(pr).most_common(1)[0][1] / len(pr))
    print(f"\nsink concentration under document-permutation null: "
          f"top receiver {np.mean(fr):.3f} +- {np.std(fr):.3f}  (observed 0.341)")
    out["null_sink_concentration"] = dict(mean=float(np.mean(fr)), sd=float(np.std(fr)))

    json.dump(out, open(os.path.join(RES, "nulls.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
