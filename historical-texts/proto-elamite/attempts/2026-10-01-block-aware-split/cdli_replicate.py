#!/usr/bin/env python3
"""Replication of the eight published constraints on 130 genuinely new tablets.

The pinned SFU corpus (1,467 tablets, August 2022) is a strict subset of the live
CDLI Proto-Elamite export (1,597 tablets, fetched 2026-10-01). The 130 tablets
in the difference were in no part of the 2026-09-04 screen or holdout, so they
are the independent falsification test the folder has been asking for since
2026-09-04.

Predictions R1-R5 are frozen in REPLICATION_PREDICTIONS.md, committed first.

Reported for each pair: the contingency table and corrected odds ratio on the new
tablets, the direction verdict (the published prediction), and the face-blocked
exact test WITH its p-value floor, because on 130 tablets the floor is the number
that decides whether a p-value means anything.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "analysis"))
sys.path.insert(0, str(_HERE.parents[1] / "attempts" / "2026-09-17-exact-form-and-face"))

from structure_associations import corpus_digest, odds_ratio, parse_tablet  # noqa: E402
from face_and_form import CONFIRMED, eligible  # noqa: E402
from block_split import blocked_test, contingency, FACE_KEY  # noqa: E402


def load(corpus: Path, names):
    lines = []
    for name in sorted(names):
        lines.extend(parse_tablet(corpus / f"{name}.values.atf"))
    return lines


def coin_faces(lines, m_sign, n_sign):
    blocks = defaultdict(list)
    for ln in lines:
        blocks[(ln.tablet, ln.surface)].append(ln)
    faces = []
    for bk, bl in sorted(blocks.items()):
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(n_sign in ln.n_signs for ln in bl)
        if (len(bl), s, t) != (2, 1, 1):
            continue
        m_line = next(ln for ln in bl if m_sign in ln.m_signs)
        faces.append({"tablet": bk[0], "face": bk[1],
                      "heads": n_sign in m_line.n_signs})
    return faces


def binom_tail(heads, n):
    if n == 0:
        return 1.0
    return sum(math.comb(n, k) for k in range(heads, n + 1)) / 2 ** n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pin_corpus", type=Path)
    ap.add_argument("cdli_corpus", type=Path)
    args = ap.parse_args()

    pin = {p.name.split(".")[0] for p in args.pin_corpus.glob("*.values.atf")}
    live = {p.name.split(".")[0] for p in args.cdli_corpus.glob("*.values.atf")}
    new = sorted(live - pin)
    print(f"pinned {len(pin)}  live {len(live)}  NEW {len(new)}")

    new_lines = load(args.cdli_corpus, new)
    new_el = eligible(new_lines)
    all_lines = load(args.cdli_corpus, sorted(live))
    all_el = eligible(all_lines)
    pub = Counter()
    for name in new:
        head = (args.cdli_corpus / f"{name}.values.atf").read_text(
            encoding="utf-8").splitlines()[0]
        pub[head.split("=", 1)[1].strip().rsplit(",", 1)[0].strip()
            if "=" in head else "?"] += 1
    print(f"new tablets: {len(new_lines)} numbered lines, {len(new_el)} eligible")
    print(f"new tablets by publication group: {dict(pub.most_common(8))}")
    print(f"pooled corpus: {len(all_el)} eligible lines, "
          f"{len({l.tablet for l in all_el})} tablets with eligible lines")

    print("\n" + "=" * 78)
    print("R1/R2/R3 -- the eight published pairs on the 130 NEW tablets alone")
    print("=" * 78)
    print(f"{'pair':12} {'published':10} {'a':>4} {'b':>4} {'c':>4} {'d':>5} "
          f"{'OR':>7} {'dir':>5} {'p':>8} {'floor':>8} {'infB':>5} pwr")
    rows = {}
    for m, n, d in CONFIRMED:
        a, b, c, dd = contingency(new_el, m, n)
        orr = odds_ratio(a, b, c, dd)
        agrees = (orr > 1) if d == "enriched" else (orr < 1)
        r = blocked_test(new_el, m, n, d, FACE_KEY)
        rows[f"{m}-{n}"] = {
            "published_direction": d, "cells": [a, b, c, dd], "odds_ratio": orr,
            "direction_agrees": agrees, "sign_lines": a + b, "target_lines": a + c,
            **r,
        }
        print(f"{m+'-'+n:12} {d:10} {a:>4} {b:>4} {c:>4} {dd:>5} {orr:>7.2f} "
              f"{'OK' if agrees else 'FAIL':>5} {r['p']:8.4f} {r['p_floor']:8.4f} "
              f"{r['informative_blocks']:5} {'Y' if r['has_power_at_05'] else 'n'}")

    load_bearing = ["M297-N39B", "M263-N01", "M263-N30C"]
    print(f"\nR1 load-bearing direction: " + ", ".join(
        f"{p} {'OK' if rows[p]['direction_agrees'] else 'FAIL'}" for p in load_bearing))
    powered = [p for p, r in rows.items() if r["has_power_at_05"]]
    print(f"R2 pairs with power at 0.05 on the new tablets: {len(powered)}/8 {powered}")
    t = rows["M288-N45"]
    print(f"R3 M288-N45 on new tablets: {t['informative_blocks']} informative blocks, "
          f"floor {t['p_floor']:.4f}, "
          f"{'UNTESTABLE' if not t['has_power_at_05'] else 'testable'}")

    print("\n" + "=" * 78)
    print("R4 -- M288-N45 fair-coin faces, pin vs pooled")
    print("=" * 78)
    pin_lines = load(args.cdli_corpus, sorted(pin))
    pin_coins = coin_faces(eligible(pin_lines), "M288", "N45")
    all_coins = coin_faces(all_el, "M288", "N45")
    new_coins = [c for c in all_coins if c["tablet"] in set(new)]
    for label, cs in (("pinned 1,467 (CDLI serialisation)", pin_coins),
                      ("new 130 only", new_coins),
                      ("pooled 1,597", all_coins)):
        h = sum(c["heads"] for c in cs)
        print(f"  {label:34} {h:2}/{len(cs):<2} heads   "
              f"binomial p = {binom_tail(h, len(cs)):.5f}")
    for c in new_coins:
        print(f"    new coin face: {c['tablet']} {c['face']} heads={c['heads']}")

    print("\n" + "=" * 78)
    print("Pooled-corpus face-blocked test for all eight pairs (1,597 tablets)")
    print("=" * 78)
    print(f"{'pair':12} {'OR':>7} {'p':>9} {'floor':>8} {'obs/frc/max':>13} {'infB':>5}")
    pooled = {}
    for m, n, d in CONFIRMED:
        a, b, c, dd = contingency(all_el, m, n)
        r = blocked_test(all_el, m, n, d, FACE_KEY)
        pooled[f"{m}-{n}"] = {"cells": [a, b, c, dd],
                              "odds_ratio": odds_ratio(a, b, c, dd), **r}
        counts = f"{r['observed_overlap']}/{r['forced_overlap']}/{r['max_possible_overlap']}"
        print(f"{m+'-'+n:12} {odds_ratio(a,b,c,dd):>7.2f} {r['p']:9.5f} "
              f"{r['p_floor']:8.4f} {counts:>13} {r['informative_blocks']:5}")

    out = {
        "fetched": "2026-10-01T18:43:20Z",
        "route": ("https://cdli.earth/search?period=Proto-Elamite&format=atf"
                  "&aspect=inscriptions&limit=3000"),
        "pinned_tablets": len(pin), "live_tablets": len(live), "new_tablets": len(new),
        "new_tablet_ids": new,
        "new_publication_groups": dict(pub),
        "new_numbered_lines": len(new_lines), "new_eligible_lines": len(new_el),
        "pooled_eligible_lines": len(all_el),
        "live_corpus_sha256": corpus_digest(
            sorted(args.cdli_corpus.glob("*.values.atf"))),
        "new_tablets_rows": rows,
        "r1_load_bearing_direction": {p: rows[p]["direction_agrees"]
                                      for p in load_bearing},
        "r2_powered_on_new": powered,
        "coin_faces": {
            "pinned": {"n": len(pin_coins), "heads": sum(c["heads"] for c in pin_coins),
                       "binomial_p": binom_tail(sum(c["heads"] for c in pin_coins),
                                                len(pin_coins))},
            "new_only": {"n": len(new_coins),
                         "heads": sum(c["heads"] for c in new_coins),
                         "detail": new_coins},
            "pooled": {"n": len(all_coins), "heads": sum(c["heads"] for c in all_coins),
                       "binomial_p": binom_tail(sum(c["heads"] for c in all_coins),
                                                len(all_coins))},
        },
        "pooled_face_blocked": pooled,
    }
    (_HERE / "results").mkdir(exist_ok=True)
    (_HERE / "results" / "cdli_replicate.json").write_text(
        json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
