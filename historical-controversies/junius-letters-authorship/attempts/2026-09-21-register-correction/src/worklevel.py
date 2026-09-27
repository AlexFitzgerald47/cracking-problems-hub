#!/usr/bin/env python3
"""STEP 5 — the two tests that decide whether STEP 4 is a result or an artefact.

TEST 1  REPLICATION UNIT. `junius_apply.py` reports Francis's Two Speeches recovered
4 of 10 chunks, one-sided binomial p = 0.009. That p is not usable and the reason is
in PRACTICES: those ten chunks are ten slices of ONE work by ONE author printed in
ONE volume. The replication unit is the work, not the chunk. This file re-runs the
whole cross-register evaluation with the WORK as the unit -- each formal-register
work is attributed by majority vote of its chunks, and the score is works correct out
of works testable.

TEST 2  IS FRANCIS'S RANK MOVEMENT DISTINGUISHABLE FROM RESHUFFLING? Under the
correction Francis moves from #10 to #5 in the Junius ranking. So does everyone else
move: Burke goes #1 to #10. If the correction permutes the whole ranking, a candidate
moving five places is not evidence about that candidate. This file measures the
rank movement of all eleven candidates and places Francis's inside it.
"""
import sys, os
from collections import defaultdict, Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from correction import detrend, register_centre, registers_of
from junius_apply import build, POLITICAL_WORKS


def work_level(docs, Ztr, Zq, train_genres, test_genres):
    """Attribute each WORK in the test register by majority vote of its chunks."""
    train = common.index(docs, train_genres)
    cents = {a: Ztr[v].mean(0) for a, v in train.items()}
    works = defaultdict(list)
    for d in docs:
        if d["genre"] in test_genres and d["author"] in train \
                and d["author"] not in common.NOT_CANDIDATES:
            works[(d["author"], d["source"])].append(d["_i"])
    rows = []
    for (auth, src), idx in sorted(works.items()):
        votes = Counter()
        ranks = []
        for i in idx:
            ds = {a: float(np.abs(Zq[i] - cents[a]).mean()) for a in cents}
            order = sorted(ds, key=ds.get)
            votes[order[0]] += 1
            ranks.append(order.index(auth) + 1)
        win = votes.most_common(1)[0][0]
        rows.append(dict(author=auth, source=src, n_chunks=len(idx), winner=win,
                         correct=win == auth, median_rank=float(np.median(ranks))))
    return rows


def show(tag, rows, n_cand):
    ok = sum(r["correct"] for r in rows)
    print(f"\n  {tag}")
    print(f"    {ok}/{len(rows)} works correct  (chance {len(rows)/n_cand:.1f}/{len(rows)})"
          f"   median of median-ranks {np.median([r['median_rank'] for r in rows]):.1f}"
          f" of {n_cand}")
    for r in rows:
        m = "OK " if r["correct"] else "   "
        print(f"    {m} {r['author']:18s} {r['source'][:34]:34s} n={r['n_chunks']:3d} "
              f"-> {r['winner']:18s} rank {r['median_rank']:.0f}")
    return ok, len(rows)


def main():
    docs, Z, feats = common.load()
    out = {}

    print("=" * 78)
    print("TEST 1  WORK-LEVEL EVALUATION (replication unit = work, not chunk)")
    print("        formal-register works scored against private-letter centroids")
    n_cand = len(common.index(docs, common.LETTERS))
    for tag, dt, ct in (("uncorrected", False, False),
                        ("centre only", False, True),
                        ("detrend + centre", True, True)):
        Ztr, Zq = build(docs, Z, POLITICAL_WORKS, do_detrend=dt, do_centre=ct)
        if not ct:
            Ztr = Zq = detrend(Z, docs,
                               [d["_i"] for d in docs if d["genre"] in common.LETTERS]) \
                if dt else Z
        else:
            # for the general work-level test, centre questioned works on the OTHER
            # works of their own register (the plain recipe), not on the political
            # subset -- the political subset exists only because Junius's own
            # register has no independent works.
            Zt = detrend(Z, docs, [d["_i"] for d in docs if d["genre"] in common.LETTERS]) \
                if dt else Z
            regs = registers_of(docs)
            Ztr = Zq = register_centre(Zt, docs, regs, work_level=True)
        rows = work_level(docs, Ztr, Zq, common.LETTERS, common.FORMAL)
        ok, n = show(tag, rows, n_cand)
        out[tag] = dict(correct=ok, n=n, rows=rows)

    print("\n" + "=" * 78)
    print("        and the reverse direction: private-letter works vs formal centroids")
    n_cand2 = len(common.index(docs, common.FORMAL))
    for tag, dt, ct in (("uncorrected", False, False), ("detrend + centre", True, True)):
        Zt = detrend(Z, docs, [d["_i"] for d in docs if d["genre"] in common.FORMAL]) \
            if dt else Z
        Ztr = Zq = register_centre(Zt, docs, registers_of(docs), True) if ct else Zt
        rows = work_level(docs, Ztr, Zq, common.FORMAL, common.LETTERS)
        ok, n = show(tag + " (reverse)", rows, n_cand2)
        out[tag + "_reverse"] = dict(correct=ok, n=n, rows=rows)

    print("\n" + "=" * 78)
    print("TEST 2  IS FRANCIS'S RANK MOVEMENT SPECIAL?")
    ranks = {}
    for tag, dt, ct in (("uncorrected", False, False), ("corrected", True, True)):
        Ztr, Zq = build(docs, Z, POLITICAL_WORKS, do_detrend=dt, do_centre=ct)
        train = common.index(docs, common.LETTERS)
        cents = {a: Ztr[v].mean(0) for a, v in train.items()}
        for src in ("junius_1772_wikisource", "junius_1813_ocr"):
            jt = [d["_i"] for d in docs if d["author"] == "Junius" and d["source"] == src]
            cen = Zq[jt].mean(0)
            order = sorted(cents, key=lambda a: float(np.abs(cen - cents[a]).mean()))
            ranks[(tag, src)] = {a: k + 1 for k, a in enumerate(order)}
    for src in ("junius_1772_wikisource", "junius_1813_ocr"):
        u, c = ranks[("uncorrected", src)], ranks[("corrected", src)]
        moves = {a: c[a] - u[a] for a in u}
        mean_abs = np.mean([abs(v) for v in moves.values()])
        print(f"\n    {src}   mean |rank change| across 11 candidates = {mean_abs:.1f}")
        for a, v in sorted(moves.items(), key=lambda kv: kv[1]):
            m = "   <-- CANDIDATE" if a == "Philip_Francis" else ""
            print(f"      {a:20s} #{u[a]:2d} -> #{c[a]:2d}  ({v:+d}){m}")
        fm = abs(moves["Philip_Francis"])
        bigger = sum(1 for v in moves.values() if abs(v) >= fm)
        print(f"      Francis moved {fm} places; {bigger} of 11 candidates moved at "
              f"least as far.")
        out[f"rank_move_{src}"] = dict(mean_abs=float(mean_abs), moves=moves,
                                       francis_move=int(moves["Philip_Francis"]),
                                       n_at_least_as_far=int(bigger))
    common.dump("worklevel.json", out)


if __name__ == "__main__":
    main()
