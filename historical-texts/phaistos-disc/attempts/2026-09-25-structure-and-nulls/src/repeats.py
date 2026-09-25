#!/usr/bin/env python3
"""Sign-level repetition, independent of the word segmentation.

H1 above depends on the group boundaries.  This does not: it works on the raw
241-sign stream per side and asks how long the longest repeated substring is,
against nulls that preserve progressively more of the Disc's own structure.

Nulls (each preserves more than the last, so the test gets progressively harder):
  M1  shuffle all signs within a side (preserves sign frequencies only)
  M2  shuffle the ORDER OF GROUPS within a side (preserves every group intact;
      asks whether the repeats are more than the group inventory already implies)
  M3  Markov-1: resample the stream from the observed bigram transition matrix
"""
import csv, os, json, random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(20260925)
B = 20000

rows = list(csv.DictReader(open(os.path.join(HERE, "data", "phaistos_words.csv"))))
groups = {"A": [], "B": []}
for r in rows:
    groups[r["side"]].append([int(x) for x in r["signs"].split("-")])

def longest_repeat(seq):
    """length of the longest substring occurring at least twice (non-identical start)"""
    n = len(seq)
    best = 0
    seen = {}
    for L in range(1, n):
        seen = defaultdict(int)
        for i in range(n - L + 1):
            seen[tuple(seq[i:i + L])] += 1
        if max(seen.values()) >= 2:
            best = L
        else:
            break
    return best

def total_repeated_mass(seq, L):
    """how many positions lie inside some substring of length >= L that repeats"""
    n = len(seq); cov = set()
    occ = defaultdict(list)
    for i in range(n - L + 1):
        occ[tuple(seq[i:i + L])].append(i)
    for k, v in occ.items():
        if len(v) >= 2:
            for i in v:
                cov.update(range(i, i + L))
    return len(cov)

out = ["Phaistos Disc: sign-level repetition, segmentation-independent", ""]
res = {}
for side in ("A", "B"):
    stream = [s for g in groups[side] for s in g]
    obs = longest_repeat(stream)
    mass = total_repeated_mass(stream, 4)
    out.append("side %s: %d sign positions, longest repeated substring = %d signs; "
               "positions inside a repeated >=4-sign block = %d" % (side, len(stream), obs, mass))
    res[side] = {"n": len(stream), "obs_longest": obs, "mass4": mass}

    # M1 within-side sign shuffle
    pool = list(stream)
    cnt = 0
    for _ in range(B):
        random.shuffle(pool)
        if longest_repeat(pool) >= obs: cnt += 1
    p1 = (cnt + 1) / (B + 1)

    # M2 shuffle group order (every group kept intact)
    gs = list(groups[side]); cnt = 0
    for _ in range(B):
        random.shuffle(gs)
        if longest_repeat([s for g in gs for s in g]) >= obs: cnt += 1
    p2 = (cnt + 1) / (B + 1)

    # M3 Markov-1 resample
    trans = defaultdict(list)
    for i in range(len(stream) - 1):
        trans[stream[i]].append(stream[i + 1])
    starts = [stream[0]]
    cnt = 0
    for _ in range(B):
        cur = random.choice(stream); seq = [cur]
        for _ in range(len(stream) - 1):
            nxt = trans.get(cur)
            cur = random.choice(nxt) if nxt else random.choice(stream)
            seq.append(cur)
        if longest_repeat(seq) >= obs: cnt += 1
    p3 = (cnt + 1) / (B + 1)

    out.append("   M1 sign shuffle          P(longest >= %d) = %.5f" % (obs, p1))
    out.append("   M2 group-order shuffle   P(longest >= %d) = %.5f   <- groups kept intact" % (obs, p2))
    out.append("   M3 Markov-1 resample     P(longest >= %d) = %.5f" % (obs, p3))
    out.append("   (p-floor of this run: %.2e)" % (1 / (B + 1)))
    res[side].update({"p_M1": p1, "p_M2": p2, "p_M3": p3})
    out.append("")

out.append("Note on M2: shuffling group order cannot destroy a repeat that lies INSIDE one")
out.append("group, so where the longest repeat spans a group boundary M2 is the informative")
out.append("null and where it does not, M2 is expected to be uninformative by construction.")
out.append("")
# which repeats cross boundaries?
for side in ("A", "B"):
    stream = [s for g in groups[side] for s in g]
    L = res[side]["obs_longest"]
    occ = defaultdict(list)
    for i in range(len(stream) - L + 1):
        occ[tuple(stream[i:i + L])].append(i)
    bounds = set(); acc = 0
    for g in groups[side]:
        acc += len(g); bounds.add(acc)
    for k, v in occ.items():
        if len(v) >= 2:
            crosses = any(b > i and b < i + L for i in v for b in bounds)
            out.append("side %s longest repeat %s at positions %s; crosses a group boundary: %s"
                       % (side, "-".join("%02d" % x for x in k), v, crosses))

txt = "\n".join(out)
print(txt)
open(os.path.join(HERE, "results", "repeats.txt"), "w").write(txt + "\n")
json.dump(res, open(os.path.join(HERE, "results", "repeats.json"), "w"), indent=1)
