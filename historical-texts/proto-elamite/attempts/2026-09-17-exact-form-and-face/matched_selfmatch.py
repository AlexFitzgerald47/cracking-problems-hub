#!/usr/bin/env python3
"""Sample-size-matched version of the cross-face self-match test.

The unmatched comparison in `face_and_form.py` is open to one objection: a sign's
self-distance splits its lines across two faces, so each profile is estimated from
fewer lines than the full-face profiles used for the between-sign distances. Noise
inflates the self-distance, which happens to work against the conclusion -- but the
comparison should not depend on that.

Here every distance is computed from two disjoint samples of exactly k lines, where k
is chosen per sign (or per sign pair) as the largest size both groups can supply. Three
quantities at identical k:

  NOISE  same sign, same face, two disjoint random halves  -- pure estimation noise
  FACE   same sign, obverse sample vs reverse sample       -- the class effect
  SIGN   two different signs, both on the obverse          -- the effect being measured

If FACE - NOISE is comparable to or larger than SIGN - NOISE, the class gap rivals the
signal and rankings that cross it are measuring the class (the Junius result). If it is
clearly smaller, the folder's associations may be read across faces.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

from face_and_form import eligible, load_lines, total_variation

REPEATS = 400
MIN_K = 10


def profile_from(lines, vocabulary):
    return [sum(n in ln.n_signs for ln in lines) / len(lines) for n in vocabulary]


def main():
    corpus = Path(Path(__file__).with_name("corpus_path.txt").read_text().strip())
    lines, _ = load_lines(corpus)
    el = eligible(lines)

    counts = Counter()
    for ln in el:
        counts.update(ln.n_signs)
    vocabulary = [n for n, _ in counts.most_common(15)]

    by_sign_face = defaultdict(list)
    for ln in el:
        if ln.surface not in ("obverse", "reverse"):
            continue
        for s in ln.m_signs:
            by_sign_face[(s, ln.surface)].append(ln)

    by_sign_face = dict(by_sign_face)
    signs = sorted(
        {
            s
            for (s, _f) in by_sign_face
            if len(by_sign_face.get((s, "obverse"), [])) >= 2 * MIN_K
            and len(by_sign_face.get((s, "reverse"), [])) >= MIN_K
        }
    )

    rng = random.Random(20260917)
    noise, face = {}, {}
    for s in signs:
        obv, rev = by_sign_face[(s, "obverse")], by_sign_face[(s, "reverse")]
        k = min(len(obv) // 2, len(rev))
        if k < MIN_K:
            continue
        nd, fd = [], []
        for _ in range(REPEATS):
            shuffled = list(obv)
            rng.shuffle(shuffled)
            nd.append(
                total_variation(
                    profile_from(shuffled[:k], vocabulary),
                    profile_from(shuffled[k : 2 * k], vocabulary),
                )
            )
            rev_s = list(rev)
            rng.shuffle(rev_s)
            fd.append(
                total_variation(
                    profile_from(shuffled[:k], vocabulary),
                    profile_from(rev_s[:k], vocabulary),
                )
            )
        noise[s] = {"k": k, "mean": statistics.mean(nd)}
        face[s] = {"k": k, "mean": statistics.mean(fd)}

    usable = sorted(noise)
    # SIGN distances at the k of each sign pair, obverse only, disjoint samples.
    sign_pairs = {}
    for i, s1 in enumerate(usable):
        for s2 in usable[i + 1 :]:
            o1, o2 = by_sign_face[(s1, "obverse")], by_sign_face[(s2, "obverse")]
            # Different signs can share a line; sample disjointly to stay honest.
            k = min(noise[s1]["k"], noise[s2]["k"])
            ds = []
            for _ in range(REPEATS):
                a, b = list(o1), list(o2)
                rng.shuffle(a)
                rng.shuffle(b)
                ds.append(
                    total_variation(profile_from(a[:k], vocabulary), profile_from(b[:k], vocabulary))
                )
            sign_pairs[f"{s1}|{s2}"] = {"k": k, "mean": statistics.mean(ds)}

    noise_mean = statistics.mean(v["mean"] for v in noise.values())
    face_mean = statistics.mean(v["mean"] for v in face.values())
    sign_mean = statistics.mean(v["mean"] for v in sign_pairs.values())

    out = {
        "vocabulary": vocabulary,
        "repeats": REPEATS,
        "signs_used": usable,
        "per_sign_noise": noise,
        "per_sign_face": face,
        "sign_pairs": sign_pairs,
        "summary": {
            "noise_mean": noise_mean,
            "face_mean": face_mean,
            "sign_mean": sign_mean,
            "face_effect_above_noise": face_mean - noise_mean,
            "sign_effect_above_noise": sign_mean - noise_mean,
            "ratio_face_to_sign": (face_mean - noise_mean) / (sign_mean - noise_mean),
        },
    }
    Path("results").mkdir(exist_ok=True)
    Path("results/matched_selfmatch.json").write_text(json.dumps(out, indent=2))

    print(f"signs used ({len(usable)}): {usable}")
    print(f"{'sign':8} {'k':>4} {'noise':>8} {'face':>8} {'face-noise':>11}")
    for s in usable:
        print(f"{s:8} {noise[s]['k']:4} {noise[s]['mean']:8.4f} {face[s]['mean']:8.4f} "
              f"{face[s]['mean']-noise[s]['mean']:11.4f}")
    print()
    print(f"NOISE (same sign, same face, disjoint halves) : {noise_mean:.4f}")
    print(f"FACE  (same sign, obverse vs reverse)         : {face_mean:.4f}"
          f"   above noise {face_mean-noise_mean:+.4f}")
    print(f"SIGN  (different signs, same face)            : {sign_mean:.4f}"
          f"   above noise {sign_mean-noise_mean:+.4f}")
    print(f"ratio  face-effect / sign-effect              : {out['summary']['ratio_face_to_sign']:.3f}")


if __name__ == "__main__":
    main()
