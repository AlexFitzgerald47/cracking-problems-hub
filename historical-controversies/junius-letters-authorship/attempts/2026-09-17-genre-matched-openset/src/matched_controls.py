#!/usr/bin/env python3
"""The matched-control experiment: everything held constant except the author.

Every cross-corpus attribution in this study compares texts that differ in edition,
printer, transcription pipeline, decade, register and subject at the same time as
they differ in author. The 1772/1812 Junius collections are the one place where that
is not true. They print, inside the same covers, in the same genre, on the same
subjects, in the same months, from the same press and through the same scanner:

    Junius            -- the target
    Philo Junius      -- Junius's own acknowledged second signature (POSITIVE control)
    Sir William Draper-- an opponent answering him (NEGATIVE control)
    John Horne        -- another opponent answering him (NEGATIVE control)

So this is the honest power test. Three questions, in order:

  Q1  Can the method separate Junius from Draper at all, with everything else
      controlled? If not, nothing else in this study means anything.
  Q2  With Philo Junius held out entirely, does the method put him with Junius
      rather than with the opponent? That is the positive control.
  Q3  Do Junius's own letters, transcribed independently from a DIFFERENT edition,
      still attribute to Junius? That isolates the edition/OCR source effect, which
      is the confound every cross-corpus comparison in this problem silently carries.

Chunks are 1,000 words here rather than 2,000 because the controls are short; the
cost is noisier Delta, which is the honest trade and is reported, not hidden.
"""
import json, os, sys
from collections import defaultdict, Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C
from funcwords import FUNCTION_WORDS

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
CHUNK = 1000
N_FEATURES = 100


def collect(name, tag):
    by = defaultdict(list)
    for d in C.load_jsonl(name):
        by[d["author"]].append(d["text"])
    out = []
    for a, texts in by.items():
        for i, ch in enumerate(C.chunk(" ".join(texts), CHUNK)):
            out.append(dict(author=a, source=tag, chunk=i, text=ch))
    return out


def vectorise(docs):
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
    return (X - mu) / sd, feats


def cent(Z, idx):
    return np.mean(Z[idx], 0)


def dl(z, c):
    return float(np.abs(z - c).mean())


def main():
    os.makedirs(RES, exist_ok=True)
    a1813 = collect("junius_1813_ocr.jsonl", "1813")
    a1772 = collect("junius_1772_wikisource.jsonl", "1772")
    docs = a1813 + a1772
    Z, feats = vectorise(docs)
    print(f"{len(docs)} documents of {CHUNK} words, {len(feats)} features")
    cnt = Counter((d["author"], d["source"]) for d in docs)
    for k in sorted(cnt):
        print(f"   {k[0]:18s} {k[1]}  {cnt[k]:3d} docs")
    print()

    def idxs(author, source=None):
        return [i for i, d in enumerate(docs)
                if d["author"] == author and (source is None or d["source"] == source)]

    J = idxs("Junius", "1813")
    D = idxs("William_Draper", "1813")
    P = idxs("Philo_Junius", "1813")
    J72 = idxs("Junius", "1772")
    D72 = idxs("William_Draper", "1772")
    H72 = idxs("John_Horne_Tooke", "1772")
    P72 = idxs("Philo_Junius", "1772")

    out = {}

    # ---- Q1 ------------------------------------------------------------
    print("Q1  Junius vs Draper, same edition, leave-one-document-out")
    ok = tot = 0
    for grp, lab in ((J, "Junius"), (D, "William_Draper")):
        for i in grp:
            cj = cent(Z, [x for x in J if x != i])
            cd = cent(Z, [x for x in D if x != i])
            pred = "Junius" if dl(Z[i], cj) < dl(Z[i], cd) else "William_Draper"
            ok += pred == lab
            tot += 1
    print(f"    accuracy {ok}/{tot} = {ok/tot:.3f}   (chance 0.500)")
    out["q1_accuracy"] = ok / tot

    # ---- Q2 ------------------------------------------------------------
    cj, cd = cent(Z, J), cent(Z, D)
    for name, grp in (("Philo Junius (1813)", P), ("Philo Junius (1772)", P72),
                      ("John Horne (1772)", H72), ("Draper (1772)", D72)):
        if not grp:
            continue
        toJ = sum(dl(Z[i], cj) < dl(Z[i], cd) for i in grp)
        mj = np.mean([dl(Z[i], cj) for i in grp])
        md = np.mean([dl(Z[i], cd) for i in grp])
        verdict = "-> Junius" if mj < md else "-> Draper"
        print(f"Q2  {name:22s} {toJ:2d}/{len(grp):2d} docs nearer Junius; "
              f"mean Delta  Junius {mj:.3f}  Draper {md:.3f}  {verdict}")
        out[f"q2_{name}"] = dict(to_junius=toJ, n=len(grp),
                                 mean_junius=round(mj, 4), mean_draper=round(md, 4))

    # ---- Q3 ------------------------------------------------------------
    print("\nQ3  edition/OCR source effect: Junius's own letters from the OTHER edition")
    if J72:
        toJ = sum(dl(Z[i], cj) < dl(Z[i], cd) for i in J72)
        mj = np.mean([dl(Z[i], cj) for i in J72])
        md = np.mean([dl(Z[i], cd) for i in J72])
        print(f"    Junius 1772 Wikisource vs 1813-OCR centroids: "
              f"{toJ}/{len(J72)} nearer Junius; Junius {mj:.3f} Draper {md:.3f}")
        out["q3"] = dict(to_junius=toJ, n=len(J72),
                         mean_junius=round(float(mj), 4), mean_draper=round(float(md), 4))
        # how big is the same-author cross-edition gap next to the author gap?
        within = np.mean([dl(Z[i], cj) for i in J])
        print(f"    same author, same edition   mean Delta to Junius centroid {within:.3f}")
        print(f"    same author, other edition  mean Delta to Junius centroid {mj:.3f}")
        print(f"    other author, same edition  mean Delta to Junius centroid "
              f"{np.mean([dl(Z[i], cj) for i in D]):.3f}")
        out["q3_gaps"] = dict(same_author_same_edition=round(float(within), 4),
                              same_author_other_edition=round(float(mj), 4),
                              other_author_same_edition=round(
                                  float(np.mean([dl(Z[i], cj) for i in D])), 4))

    json.dump(out, open(os.path.join(RES, "matched_controls.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
