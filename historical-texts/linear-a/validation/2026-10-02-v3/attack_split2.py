#!/usr/bin/env python3
"""
ATTACK 3d/3e — the label permutation done to the orchestrator's specification,
plus the two corrections the first pass missed.

  3d  SCRIBE-LABEL PERMUTATION.  Hold every tablet in place; permute only the
      scribe labels, preserving each scribe's tablet count exactly.  Report
        (i)  the null for the 10-tablet group  -> is Scribe 9's set special?
        (ii) the null for the MAXIMUM over all scribe groups with >=3 tablets
             -> Scribe 9 was SELECTED as 'the dossier' out of ~12 candidate
                scribes, so (ii) is the honest p.
  3e  FINDSPOT-matched null, now SIZE-matched as well (the first pass's 3c was
      confounded by the fact that Scribe-9's tablets are unusually long).
"""
import random, collections
from corpus import load_a, ht_tablet_faces, is_word, base
from attack_split import tablet_wordsets, cohesion, norm_pval, ADMIN

SEED = 20261002
N = 20000


def main():
    A = load_a()
    for strict, lab in ((False, "ALL sign-group types"),
                        (True, "STRICT: multi-sign names, admin operators removed")):
        by, meta = tablet_wordsets(A, strict)
        allt = sorted(by)
        sz = {t: len(by[t]) for t in allt}
        rng = random.Random(SEED)
        s9 = sorted(t for t in allt if "HT Scribe 9" in meta[t]["scribe"])
        obs, _ = cohesion(s9, by)
        print(f"\n{'='*78}\nATTACK 3d/3e [{lab}]\n{'='*78}")
        print(f"  observed Scribe-9 cohesion = {obs} over {len(s9)} tablets "
              f"({sum(sz[t] for t in s9)} type-slots; pool average "
              f"{sum(sz.values())/len(allt):.1f} per tablet, Scribe-9 average "
              f"{sum(sz[t] for t in s9)/len(s9):.1f})")

        # group-size profile of the real scribe attribution
        groups = collections.defaultdict(list)
        for t in allt:
            for s in meta[t]["scribe"]:
                groups[s].append(t)
        sizes = {s: len(v) for s, v in groups.items() if len(v) >= 3}
        print(f"  HT scribes with >=3 tablets: {len(sizes)} -> "
              f"{sorted(sizes.items(), key=lambda x: -x[1])}")
        labelled = sorted({t for s, v in groups.items() for t in v})
        print(f"  tablets carrying ANY scribe attribution: {len(labelled)} of {len(allt)}")

        # ---- 3d label permutation over the attributed tablets only
        order = list(labelled)
        tenc, maxc = [], []
        szlist = sorted(sizes.values(), reverse=True)
        for _ in range(N):
            rng.shuffle(order)
            i = 0; cs = []
            for s, n in sorted(sizes.items(), key=lambda x: -x[1]):
                grp = order[i:i + n]; i += n
                c = cohesion(grp, by)[0]
                cs.append((s, n, c))
                if n == len(s9):
                    tenc.append(c)
            maxc.append(max(c for _, _, c in cs))
        tenc.sort(); maxc.sort()
        print(f"\n  3d(i)  null for a permuted {len(s9)}-tablet scribe group, n={len(tenc)}:")
        print(f"         mean {sum(tenc)/len(tenc):.2f}  95% "
              f"[{tenc[int(.025*len(tenc))]}, {tenc[int(.975*len(tenc))]}]  "
              f"p = {norm_pval(obs, tenc):.4f}")
        print(f"  3d(ii) null for the MAX cohesion over all >=3-tablet groups "
              f"(selection-corrected), n={len(maxc)}:")
        print(f"         mean {sum(maxc)/len(maxc):.2f}  95% "
              f"[{maxc[int(.025*len(maxc))]}, {maxc[int(.975*len(maxc))]}]  "
              f"p = {norm_pval(obs, maxc):.4f}")

        # ---- 3e findspot AND size matched
        fs9 = set().union(*[meta[t]["findspot"] for t in s9])
        poolfs = [t for t in allt if meta[t]["findspot"] & fs9]
        tgt = sum(sz[t] for t in s9)
        d, tr = [], 0
        while len(d) < N and tr < 6000000:
            tr += 1
            p = rng.sample(poolfs, len(s9))
            if abs(sum(sz[t] for t in p) - tgt) <= 0.10 * tgt:
                d.append(cohesion(p, by)[0])
        d.sort()
        print(f"\n  3e  findspot-matched AND size-matched null "
              f"({len(poolfs)} tablets from the same three deposits, "
              f"+/-10% of {tgt} type-slots), n={len(d)}:")
        if d:
            print(f"      mean {sum(d)/len(d):.2f}  95% [{d[int(.025*len(d))]}, "
                  f"{d[int(.975*len(d))]}]  p = {norm_pval(obs, d):.4f}")
        # and the selection correction applied to the size-matched null:
        #   how often does SOME 10-tablet size-matched set reach 13?
        print("\n  summary of the four nulls for the same observed statistic:")
        print("      unmatched random 10 tablets                 -> p small (09-25: 0.0045)")
        print("      size-matched random 10 tablets              -> see ATTACK 3 3a")
        print(f"      scribe-label permutation, same group size   -> "
              f"p = {norm_pval(obs, tenc):.4f}")
        print(f"      same, corrected for choosing the best scribe -> "
              f"p = {norm_pval(obs, maxc):.4f}")
        if d:
            print(f"      findspot + size matched                     -> "
                  f"p = {norm_pval(obs, d):.4f}")


if __name__ == "__main__":
    main()
