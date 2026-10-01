#!/usr/bin/env python3
"""Tests for the block-aware split. The load-bearing one is
`test_tablet_key_reproduces_published_validation_p_values`: it requires the
re-parameterised exact test to return the eight published 2026-09-04 validation
p-values when handed the tablet block key. Every face-blocked number in
RESULTS.md comes from the same function with a different key, so if that test
passes the comparison is like-for-like at the level of the test statistic.
"""
from __future__ import annotations

import math
import random
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "analysis"))
sys.path.insert(0, str(_HERE.parents[1] / "attempts" / "2026-09-17-exact-form-and-face"))
sys.path.insert(0, str(_HERE))

from structure_associations import Line, split_name  # noqa: E402
from face_and_form import CONFIRMED, eligible, load_lines  # noqa: E402
from block_split import (  # noqa: E402
    FACE_KEY, TABLET_KEY, block_freedom, blocked_test, build_split,
    informative_tablets, screen, validate,
)
from nulls import permute_target_within  # noqa: E402

CORPUS = Path((_HERE / "corpus_path.txt").read_text().strip())
_CACHE: dict = {}


def el():
    if "el" not in _CACHE:
        lines, _ = load_lines(CORPUS)
        _CACHE["el"] = eligible(lines)
    return _CACHE["el"]


def mk(tablet, surface, m, n, ordinal=1):
    return Line(tablet=tablet, surface=surface, label=str(ordinal),
                ordinal_on_surface=ordinal, text="", m_signs=frozenset(m),
                n_signs=frozenset(n), damaged=False)


# published 2026-09-04 validation p-values, read programmatically from
# analysis/results/associations.csv -- not transcribed by hand. The first
# version of this file carried hand-entered constants and this test failed,
# which is what it is for.
PUBLISHED_P = {
    ("M297", "N39B"): 4.385332409747139e-06,
    ("M297", "N24"): 0.00030402662116529476,
    ("M297", "N01"): 0.00029696729663097155,
    ("M263", "N30C"): 0.0012307554600787746,
    ("M263", "N01"): 0.001749703554343871,
    ("M243", "N39B"): 0.002467279309384563,
    ("M106", "N24"): 0.005059860725189959,
    ("M288", "N45"): 0.00711538461538455,
}


class TestMarginals(unittest.TestCase):
    def test_freedom_bounds_are_marginal_functions(self):
        lines = [mk("T1", "obverse", ["M288"], ["N45"]),
                 mk("T1", "obverse", ["M001"], ["N01"], 2)]
        fr = block_freedom(lines, "M288", "N45")[("T1", "obverse")]
        self.assertEqual((fr["total"], fr["s"], fr["t"]), (2, 1, 1))
        self.assertEqual((fr["lo"], fr["hi"]), (0, 1))  # the fair coin

    def test_forced_overlap_block_is_not_informative(self):
        # two lines, both carry M288, both carry N45 -> overlap forced at 2
        lines = [mk("T1", "obverse", ["M288"], ["N45"]),
                 mk("T1", "obverse", ["M288"], ["N45"], 2)]
        fr = block_freedom(lines, "M288", "N45")[("T1", "obverse")]
        self.assertEqual((fr["lo"], fr["hi"]), (2, 2))
        self.assertFalse(fr["hi"] > fr["lo"])

    def test_absent_sign_block_is_not_informative(self):
        lines = [mk("T1", "obverse", ["M001"], ["N01"]),
                 mk("T1", "obverse", ["M002"], ["N45"], 2)]
        fr = block_freedom(lines, "M288", "N45")[("T1", "obverse")]
        self.assertEqual((fr["lo"], fr["hi"]), (0, 0))

    def test_faces_are_separate_blocks(self):
        lines = [mk("T1", "obverse", ["M288"], ["N45"]),
                 mk("T1", "reverse", ["M288"], ["N45"])]
        self.assertEqual(len(block_freedom(lines, "M288", "N45", FACE_KEY)), 2)
        self.assertEqual(len(block_freedom(lines, "M288", "N45", TABLET_KEY)), 1)


class TestExactTest(unittest.TestCase):
    def test_fair_coin_block_gives_one_half(self):
        lines = [mk("T1", "obverse", ["M288"], ["N45"]),
                 mk("T1", "obverse", ["M001"], ["N01"], 2)]
        r = blocked_test(lines, "M288", "N45", "enriched", FACE_KEY)
        self.assertAlmostEqual(r["p"], 0.5, places=12)
        self.assertAlmostEqual(r["p_floor"], 0.5, places=12)
        self.assertEqual(r["informative_blocks"], 1)

    def test_k_independent_fair_coins_give_two_to_the_minus_k(self):
        lines = []
        for i in range(6):
            lines += [mk(f"T{i}", "obverse", ["M288"], ["N45"]),
                      mk(f"T{i}", "obverse", ["M001"], ["N01"], 2)]
        r = blocked_test(lines, "M288", "N45", "enriched", FACE_KEY)
        self.assertAlmostEqual(r["p"], 0.5 ** 6, places=12)
        self.assertEqual(r["observed_overlap"], 6)
        self.assertEqual(r["freedom"], 6)

    def test_forced_overlap_is_reported_and_p_is_one(self):
        lines = [mk("T1", "obverse", ["M288"], ["N45"]),
                 mk("T1", "obverse", ["M288"], ["N45"], 2)]
        r = blocked_test(lines, "M288", "N45", "enriched", FACE_KEY)
        self.assertEqual(r["forced_overlap"], 2)
        self.assertEqual(r["freedom"], 0)
        self.assertAlmostEqual(r["p"], 1.0, places=12)

    def test_tablet_key_reproduces_published_validation_p_values(self):
        """LOAD-BEARING. Same function, published block key, published numbers."""
        val = [ln for ln in el() if split_name(ln.tablet) == "validation"]
        for (m, n, d) in CONFIRMED:
            got = blocked_test(val, m, n, d, TABLET_KEY)["p"]
            want = PUBLISHED_P[(m, n)]
            self.assertAlmostEqual(
                got, want, delta=1e-12,
                msg=f"{m}-{n}: got {got!r} want {want!r}")

    def test_face_key_is_stricter_or_equal_on_the_real_corpus(self):
        val = [ln for ln in el() if split_name(ln.tablet) == "validation"]
        for (m, n, d) in CONFIRMED:
            t = blocked_test(val, m, n, d, TABLET_KEY)
            f = blocked_test(val, m, n, d, FACE_KEY)
            self.assertGreaterEqual(f["blocks"], t["blocks"])
            self.assertGreaterEqual(f["forced_overlap"], t["forced_overlap"])


class TestSplit(unittest.TestCase):
    def test_split_is_disjoint_and_hits_the_block_target(self):
        val_tablets, diag = build_split(el(), "M288", "N45", 10)
        train = {ln.tablet for ln in el() if ln.tablet not in val_tablets}
        self.assertEqual(train & val_tablets, set())
        self.assertGreaterEqual(diag["informative_blocks_in_validation"], 10)
        self.assertEqual(
            diag["informative_blocks_in_validation"]
            + diag["informative_blocks_in_train"],
            diag["informative_blocks_total"])

    def test_split_is_deterministic(self):
        a, _ = build_split(el(), "M288", "N45", 10)
        b, _ = build_split(el(), "M288", "N45", 10)
        self.assertEqual(a, b)

    def test_validation_floor_beats_the_published_holdout(self):
        val_tablets, _ = build_split(el(), "M288", "N45", 10)
        new = blocked_test([ln for ln in el() if ln.tablet in val_tablets],
                           "M288", "N45", "enriched", FACE_KEY)
        old = blocked_test([ln for ln in el() if split_name(ln.tablet) == "validation"],
                           "M288", "N45", "enriched", FACE_KEY)
        self.assertLess(new["p_floor"], 0.05)
        self.assertGreater(old["p_floor"], 0.05)

    def test_split_depends_only_on_marginals(self):
        """The null preserves block marginals, so it must leave the split alone."""
        rng = random.Random(7)
        base, _ = build_split(el(), "M288", "N45", 10)
        for _ in range(3):
            perm = permute_target_within(el(), "N45", FACE_KEY, rng)
            self.assertEqual(build_split(perm, "M288", "N45", 10)[0], base)


class TestPermutation(unittest.TestCase):
    def test_permutation_preserves_block_marginals(self):
        rng = random.Random(11)
        before = block_freedom(el(), "M288", "N45", FACE_KEY)
        perm = permute_target_within(el(), "N45", FACE_KEY, rng)
        after = block_freedom(perm, "M288", "N45", FACE_KEY)
        self.assertEqual(before.keys(), after.keys())
        for k in before:
            self.assertEqual(before[k], after[k])

    def test_permutation_actually_moves_something(self):
        rng = random.Random(13)
        perm = permute_target_within(el(), "N45", FACE_KEY, rng)
        a = sum("M288" in l.m_signs and "N45" in l.n_signs for l in el())
        b = sum("M288" in l.m_signs and "N45" in l.n_signs for l in perm)
        self.assertNotEqual(a, b)

    def test_permutation_leaves_other_signs_untouched(self):
        rng = random.Random(17)
        perm = permute_target_within(el(), "N45", FACE_KEY, rng)
        for sign in ("N01", "N39B", "N24"):
            self.assertEqual(sum(sign in l.n_signs for l in el()),
                             sum(sign in l.n_signs for l in perm))


class TestScreenAndValidate(unittest.TestCase):
    def test_screen_reproduces_the_published_candidate_count(self):
        train = [ln for ln in el() if split_name(ln.tablet) == "train"]
        selected, raw = screen(train)
        self.assertEqual(len(selected), 54)
        pairs = {(r["m_sign"], r["n_sign"]) for r in selected}
        for m, n, _ in CONFIRMED:
            self.assertIn((m, n), pairs)

    def test_published_eight_confirm_under_the_published_tablet_key(self):
        train = [ln for ln in el() if split_name(ln.tablet) == "train"]
        val = [ln for ln in el() if split_name(ln.tablet) == "validation"]
        selected, _ = screen(train)
        rows = validate(val, selected, TABLET_KEY)
        confirmed = {(r["m_sign"], r["n_sign"]) for r in rows if r["confirmed"]}
        self.assertEqual(confirmed, {(m, n) for m, n, _ in CONFIRMED})


class TestCoinFaces(unittest.TestCase):
    def test_eight_fair_coin_faces_for_the_pair_under_test(self):
        from coinflip_and_base import coinflip_audit
        a = coinflip_audit(el(), "M288", "N45")
        self.assertEqual(a["coin_blocks"], 8)
        self.assertEqual(a["coin_heads"], 8)
        self.assertAlmostEqual(a["coin_binomial_p"], 1 / 256, places=12)
        self.assertEqual(a["forced_overlap"], 38)
        self.assertEqual(a["observed_overlap"], 56)

    def test_binomial_tail_matches_math_comb(self):
        from coinflip_and_base import coinflip_audit
        a = coinflip_audit(el(), "M263", "N01")
        n, h = a["coin_blocks"], a["coin_heads"]
        want = sum(math.comb(n, k) for k in range(h, n + 1)) / 2 ** n
        self.assertAlmostEqual(a["coin_binomial_p"], want, places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
