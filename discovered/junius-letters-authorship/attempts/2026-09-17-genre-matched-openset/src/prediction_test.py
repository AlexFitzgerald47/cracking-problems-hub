#!/usr/bin/env python3
"""A frozen prediction from the register calibration, and its test.

THE PREDICTION (written before running this file; the calibration it follows from used
centroid-to-centroid distances, whereas the test below uses document-level
leave-one-out accuracy, which is a different statistic on the same corpus):

    If register dominates author -- median same-author cross-register Delta 0.587
    against median different-author same-register Delta 0.470 -- then attributing a
    document to an author whose only surviving sample is in a DIFFERENT register
    should fail at close to chance, even though same-register attribution runs at
    0.848 on the same documents, the same features and the same method.

    Failure condition: if cross-register attribution accuracy comes out anywhere near
    the same-register figure, the register confound is not what limits this problem
    and the conclusion of this session is wrong.

THE TEST. Three authors appear in two registers: Burke, Johnson, Hume. For each, take
their private letters and attribute them against candidate centroids built ONLY from
published/political prose -- so the correct answer is present, but only in the wrong
register. Then the reverse direction. Chance is 1/(number of candidates).
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

PREDICTION = ("cross-register attribution accuracy will be at or near chance, and far "
              "below the 0.848 same-register figure")


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

    FORMAL = ("published_prose", "political_prose")
    LETTERS = ("private_letter",)

    def run(test_genres, train_genres, name):
        train = defaultdict(list)
        for i, d in enumerate(docs):
            if d["genre"] in train_genres and d["author"] not in ("Junius", "Philo_Junius"):
                train[d["author"]].append(i)
        cents = {a: np.mean(Z[v], 0) for a, v in train.items() if len(v) >= 8}
        cand = sorted(cents)
        test = [i for i, d in enumerate(docs)
                if d["genre"] in test_genres and d["author"] in cents
                and d["author"] not in ("Junius", "Philo_Junius")]
        if not test:
            print(f"{name}: no testable documents")
            return None
        ok = 0
        conf = Counter()
        for i in test:
            pred = min(cents, key=lambda a: float(np.abs(Z[i] - cents[a]).mean()))
            ok += pred == docs[i]["author"]
            if pred != docs[i]["author"]:
                conf[(docs[i]["author"], pred)] += 1
        acc = ok / len(test)
        print(f"{name}")
        print(f"   candidates: {len(cand)} ({', '.join(cand)})")
        print(f"   accuracy {ok}/{len(test)} = {acc:.3f}   chance {1/len(cand):.3f}")
        for (t, p), c in conf.most_common(4):
            print(f"     {t} -> {p}: {c}")
        return dict(accuracy=acc, n=len(test), chance=1 / len(cand), candidates=cand)

    print("PREDICTION:", PREDICTION, "\n")
    a = run(LETTERS, FORMAL, "CROSS-REGISTER  private letters scored against formal-prose centroids")
    print()
    b = run(FORMAL, LETTERS, "CROSS-REGISTER  formal prose scored against private-letter centroids")
    print()
    c = run(LETTERS, LETTERS, "SAME-REGISTER control  private letters vs private-letter centroids")
    print()

    out = dict(prediction=PREDICTION, cross_letters_vs_formal=a,
               cross_formal_vs_letters=b, same_register_control=c)
    if a and c:
        upheld = a["accuracy"] < 0.5 * c["accuracy"]
        print(f"PREDICTION {'UPHELD' if upheld else 'FAILED'}: cross-register "
              f"{a['accuracy']:.3f} vs same-register {c['accuracy']:.3f}")
        out["upheld"] = bool(upheld)
    json.dump(out, open(os.path.join(RES, "prediction_test.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
