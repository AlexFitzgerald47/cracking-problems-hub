"""E2 -- pipeline validation: how well does Delta identify KNOWN Latin authors
at the sample sizes the Historia Augusta actually offers?

Half the HA's vitae are under 3,000 words. A null result on the six sigla means
nothing unless we know what Delta can do at that length on authors whose
identity is not in doubt. This produces that number.

Two designs are reported, because they give very different answers:

  chunk-LOO  nearest neighbour may be another chunk of the SAME work. This is
             the design that flatters itself: it measures work-recognition as
             much as author-recognition, and it is reported only to show how
             large that inflation is.
  work-LOO   every chunk of the held-out work is removed from the candidate
             pool, so the model must recognise the author from their OTHER
             works. This is the design that corresponds to the HA question.

Both are still period-confounded: the authors are spread over four centuries,
and part of what Delta separates is date, not hand. The genre- and
period-matched sub-test at the end (Suetonius vs Nepos, both collections of
short lives) is the closest available analogue to the HA problem.
"""

import numpy as np

import stylo

RNG = np.random.default_rng(20260906)
N_MFW = 200
SIZES = [1000, 1500, 2000, 3000, 5000]
N_PERM = 400


def build(segs, size, authors=None):
    """Chunk every work, keeping author and work labels."""
    chunks, auth, work = [], [], []
    for s in segs:
        if s["corpus"] not in ("CTRL", "SUET", "NEPOS"):
            continue
        a = {"SUET": "Suetonius", "NEPOS": "Nepos"}.get(s["corpus"], s["author"])
        if authors and a not in authors:
            continue
        for b in stylo.chunk(s, size):
            chunks.append(dict(tokens=b, n_tokens=len(b)))
            auth.append(a)
            work.append(s["seg_id"])
    return chunks, np.array(auth), np.array(work)


def loo(chunks, auth, work, words, hold_work):
    """Nearest-neighbour Delta accuracy; optionally exclude the same work."""
    if len(chunks) < 4:
        return None
    z = stylo.zscore(stylo.matrix(chunks, words))
    d = stylo.delta_matrix(z)
    np.fill_diagonal(d, np.inf)
    if hold_work:
        d = d.copy()
        for i in range(len(chunks)):
            d[i, work == work[i]] = np.inf
    # A chunk is only scorable if some candidate of its own author survives.
    ok = np.array([np.isfinite(d[i][auth == auth[i]]).any()
                   for i in range(len(chunks))])
    if ok.sum() < 4:
        return None
    nn = np.argmin(d[ok], axis=1)
    pred = auth[nn]
    acc = float((pred == auth[ok]).mean())

    null = np.empty(N_PERM)
    for i in range(N_PERM):
        p = RNG.permutation(auth)
        null[i] = (p[nn] == p[ok]).mean()
    return acc, float(null.mean()), int(ok.sum()), len(set(auth))


def main():
    segs = stylo.load()
    words = stylo.mfw_list(stylo.by_corpus(segs, "CTRL"), N_MFW)

    multi = ["Caesar", "Sallust", "Tacitus", "Nepos", "Suetonius"]

    print("E2  nearest-neighbour Delta attribution of known Latin authors")
    print("    features: %d MFW culled from the control pool" % N_MFW)
    print()
    print("    %-7s | %-28s | %-28s" %
          ("chunk", "chunk-LOO (same work allowed)", "work-LOO (same work held out)"))
    print("    %-7s | %6s %9s %9s | %6s %9s %9s" %
          ("tokens", "n", "acc", "null", "n", "acc", "null"))
    for size in SIZES:
        c, a, w = build(segs, size, multi)
        r1 = loo(c, a, w, words, hold_work=False)
        r2 = loo(c, a, w, words, hold_work=True)
        if not r1 or not r2:
            continue
        print("    %-7d | %6d %9.3f %9.3f | %6d %9.3f %9.3f"
              % (size, r1[2], r1[0], r1[1], r2[2], r2[0], r2[1]))
    print("    authors (each with >=2 separate works): %s" % ", ".join(multi))

    print()
    print("    genre- and period-matched pair, work-LOO:")
    print("    %-7s %6s %9s %9s" % ("tokens", "n", "acc", "null"))
    for size in SIZES:
        c, a, w = build(segs, size, ["Suetonius", "Nepos"])
        r = loo(c, a, w, words, hold_work=True)
        if r:
            print("    %-7d %6d %9.3f %9.3f" % (size, r[2], r[0], r[1]))
    print("    (Suetonius vs Nepos: both collections of short lives, but two")
    print("     centuries apart, so this is still an upper bound on what Delta")
    print("     could do between two contemporaries inside one collection.)")

    ha = stylo.by_corpus(segs, "HA")
    lens = np.array([s["n_tokens"] for s in ha])
    print()
    print("    HA vita lengths: median %d, quartiles %d/%d, range %d-%d"
          % (np.median(lens), np.percentile(lens, 25), np.percentile(lens, 75),
             lens.min(), lens.max()))
    print("    vitae under 3,000 tokens: %d of %d" % ((lens < 3000).sum(), len(lens)))


if __name__ == "__main__":
    main()
