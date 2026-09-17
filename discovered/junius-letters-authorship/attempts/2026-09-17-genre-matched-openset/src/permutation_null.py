#!/usr/bin/env python3
"""Label-permutation null and majority-class baseline for the attribution accuracies.

"Chance = 1/n_classes" assumes balanced classes, and these are not balanced: Burke has
245 documents and Richard Price 13. Two honest baselines are needed before an accuracy
can be called high:

  * the MAJORITY-CLASS baseline -- always guess the biggest author;
  * a LABEL-PERMUTATION null -- shuffle the author labels and rerun the whole
    leave-one-out procedure, which preserves the class-size distribution and the
    feature geometry while destroying the author/text association.

The same-register figure is the one the session's conclusion leans on, so it is the
one that has to survive this.
"""
import json, os, random, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C
from funcwords import FUNCTION_WORDS
from delta import junius_chunks, N_FEATURES

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
N_PERM = 200
SEED = 20260917


def vec(docs):
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
    return (X - mu) / sd


def loo_accuracy(Z, labels):
    """Leave-one-out nearest-centroid. Centroids are updated in closed form rather
    than recomputed, which is what makes 200 permutations affordable."""
    labs = np.array(labels)
    uniq = sorted(set(labels))
    sums = {a: Z[labs == a].sum(0) for a in uniq}
    counts = {a: int((labs == a).sum()) for a in uniq}
    ok = 0
    for i in range(len(labs)):
        best, bl = None, None
        for a in uniq:
            n = counts[a] - (1 if labs[i] == a else 0)
            if n == 0:
                continue
            c = (sums[a] - (Z[i] if labs[i] == a else 0)) / n
            d = float(np.abs(Z[i] - c).mean())
            if best is None or d < best:
                best, bl = d, a
        ok += bl == labs[i]
    return ok / len(labs)


def main():
    docs = list(C.load_jsonl("panel_chunks.jsonl")) + junius_chunks()
    Z = vec(docs)
    out = {}
    rnd = random.Random(SEED)

    for name, keep in (("same-register (private letters, 11 authors)",
                        lambda d: d["genre"] == "private_letter"),
                       ("all registers pooled by author",
                        lambda d: True)):
        idx = [i for i, d in enumerate(docs)
               if keep(d) and d["author"] not in ("Junius", "Philo_Junius")]
        labels = [docs[i]["author"] for i in idx]
        Zi = Z[idx]
        acc = loo_accuracy(Zi, labels)
        cnt = Counter(labels)
        maj = max(cnt.values()) / len(labels)
        perms = []
        for _ in range(N_PERM):
            sh = labels[:]
            rnd.shuffle(sh)
            perms.append(loo_accuracy(Zi, sh))
        perms = np.array(perms)
        p = float((perms >= acc).mean())
        print(f"\n{name}")
        print(f"   documents {len(labels)}, classes {len(cnt)}")
        print(f"   observed leave-one-out accuracy   {acc:.3f}")
        print(f"   majority-class baseline           {maj:.3f}")
        print(f"   1/n_classes                       {1/len(cnt):.3f}")
        print(f"   label-permutation null ({N_PERM} runs)  "
              f"median {np.median(perms):.3f}, 95th {np.percentile(perms,95):.3f}")
        print(f"   permutation p-value               {'< ' + str(1/N_PERM) if p == 0 else p}")
        out[name] = dict(accuracy=acc, majority=maj, n_classes=len(cnt),
                         perm_median=float(np.median(perms)),
                         perm_p95=float(np.percentile(perms, 95)), p_value=p)

    json.dump(out, open(os.path.join(RES, "permutation_null.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
