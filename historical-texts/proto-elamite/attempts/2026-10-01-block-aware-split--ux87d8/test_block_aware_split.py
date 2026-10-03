#!/usr/bin/env python3
"""Tests for the block-aware split.

The load-bearing test is `test_reproduces_published_face_blocked_p_values`: the
block_report in this module must return the 2026-09-17 face-blocked p-values on the
bucket-0 holdout, and `test_reproduces_published_power_floors` must return its floors.
Both run against the audited face_and_form implementation, so every new number in this
attempt is like-for-like with the published set by construction.
"""

from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from block_aware_split import (  # noqa: E402
    BLOCK_KEYS,
    RICHNESS_CAP,
    block_report,
    blocks_of,
    donor_tablets,
    key_face,
    key_face_richness,
    other_n_count,
    permute_within_blocks,
    screen,
)
from face_and_form import CONFIRMED, blocked_randomization_p, eligible, load_lines  # noqa: E402
from structure_associations import Line, split_name  # noqa: E402

_FACE = Path(__file__).resolve().parent.parent / "2026-09-17-exact-form-and-face"

# From attempts/2026-09-17-exact-form-and-face/RESULTS.md section 1 and
# results/power_floor.json: face-blocked p-values on the bucket-0 holdout.
PUBLISHED_FACE_BLOCKED_P = {
    "M297-N39B": 0.0015, "M297-N24": 0.0281, "M297-N01": 0.0084,
    "M263-N30C": 0.0190, "M263-N01": 0.0003, "M243-N39B": 0.0031,
    "M106-N24": 0.0117, "M288-N45": 0.4700,
}
PUBLISHED_FACE_BLOCKED_FLOOR = {
    "M297-N39B": 0.0000, "M297-N24": 0.0002, "M297-N01": 0.0000,
    "M263-N30C": 0.0190, "M263-N01": 0.0000, "M243-N39B": 0.0000,
    "M106-N24": 0.0004, "M288-N45": 0.1200,
}


def line(tablet, surface, m_signs, n_signs, ordinal=1):
    return Line(
        tablet=tablet, surface=surface, label=str(ordinal), ordinal_on_surface=ordinal,
        text="", m_signs=frozenset(m_signs), n_signs=frozenset(n_signs), damaged=False,
    )


class BlockArithmetic(unittest.TestCase):
    def test_informative_requires_non_degenerate_support(self):
        # A face whose every line carries both signs has no freedom to vary.
        saturated = [line("P1", "obverse", ["M288"], ["N45"], i) for i in (1, 2)]
        (total, s, t, lo, hi, a), = blocks_of(saturated, "M288", "N45", key_face)
        self.assertEqual((total, s, t, lo, hi, a), (2, 2, 2, 2, 2, 2))
        self.assertEqual(hi, lo)
        self.assertEqual(donor_tablets(saturated, "M288", "N45", key_face), set())

    def test_informative_block_makes_a_donor(self):
        mixed = [
            line("P1", "obverse", ["M288"], ["N45"], 1),
            line("P1", "obverse", ["M999"], ["N01"], 2),
        ]
        (total, s, t, lo, hi, a), = blocks_of(mixed, "M288", "N45", key_face)
        self.assertEqual((s, t, lo, hi), (1, 1, 0, 1))
        self.assertEqual(donor_tablets(mixed, "M288", "N45", key_face), {"P1"})

    def test_floor_equals_p_when_overlap_is_maximal(self):
        mixed = [
            line("P1", "obverse", ["M288"], ["N45"], 1),
            line("P1", "obverse", ["M999"], ["N01"], 2),
        ]
        report = block_report(mixed, "M288", "N45", key_face, "enriched")
        self.assertEqual(report["observed_overlap"], report["max_possible_overlap"])
        self.assertAlmostEqual(report["p"], report["p_floor"])
        self.assertAlmostEqual(report["p"], 0.5)

    def test_faces_are_separate_blocks(self):
        two = [
            line("P1", "obverse", ["M288"], ["N45"], 1),
            line("P1", "reverse", ["M288"], ["N45"], 1),
        ]
        self.assertEqual(len(blocks_of(two, "M288", "N45", key_face)), 2)


class RichnessStratification(unittest.TestCase):
    def test_target_excluded_from_its_own_count(self):
        # Without exclusion these two lines would land in different strata purely
        # because one carries the target, which is the circularity to avoid.
        with_target = line("P1", "obverse", ["M288"], ["N45", "N01"])
        without = line("P1", "obverse", ["M288"], ["N01"])
        self.assertEqual(other_n_count(with_target, "N45"), 1)
        self.assertEqual(other_n_count(without, "N45"), 1)
        self.assertEqual(
            key_face_richness(with_target, "N45"), key_face_richness(without, "N45")
        )

    def test_count_is_capped(self):
        rich = line("P1", "obverse", ["M288"], ["N45"] + [f"N{i:02d}" for i in range(10)])
        self.assertEqual(other_n_count(rich, "N45"), RICHNESS_CAP)


class Permutation(unittest.TestCase):
    def test_preserves_every_block_marginal(self):
        corpus = [
            line("P1", "obverse", ["M288"], ["N45", "N01"], 1),
            line("P1", "obverse", ["M288"], ["N01"], 2),
            line("P1", "obverse", ["M999"], ["N45"], 3),
            line("P1", "reverse", ["M288"], ["N45"], 1),
            line("P2", "obverse", ["M288"], ["N01"], 1),
            line("P2", "obverse", ["M999"], ["N45"], 2),
        ]
        before = sorted(blocks_of(corpus, "M288", "N45", key_face))
        rng = random.Random(7)
        for _ in range(40):
            after = blocks_of(permute_within_blocks(corpus, "N45", key_face, rng),
                              "M288", "N45", key_face)
            self.assertEqual(
                sorted((t, s, tt, lo, hi) for t, s, tt, lo, hi, _ in after),
                [(t, s, tt, lo, hi) for t, s, tt, lo, hi, _ in before],
            )

    def test_donor_set_invariant_under_the_null(self):
        corpus = [
            line("P1", "obverse", ["M288"], ["N45"], 1),
            line("P1", "obverse", ["M999"], ["N01"], 2),
            line("P2", "obverse", ["M288"], ["N45"], 1),
        ]
        truth = donor_tablets(corpus, "M288", "N45", key_face)
        rng = random.Random(3)
        for _ in range(60):
            permuted = permute_within_blocks(corpus, "N45", key_face, rng)
            self.assertEqual(donor_tablets(permuted, "M288", "N45", key_face), truth)

    def test_permutation_actually_moves_the_target(self):
        corpus = [
            line("P1", "obverse", ["M288"], ["N45"], 1),
            line("P1", "obverse", ["M999"], ["N01"], 2),
        ]
        rng = random.Random(1)
        seen = set()
        for _ in range(60):
            permuted = permute_within_blocks(corpus, "N45", key_face, rng)
            seen.add(tuple("N45" in ln.n_signs for ln in permuted))
        self.assertEqual(len(seen), 2)

    def test_permutation_leaves_other_n_signs_alone(self):
        corpus = [
            line("P1", "obverse", ["M288"], ["N45", "N01"], 1),
            line("P1", "obverse", ["M999"], ["N01"], 2),
        ]
        rng = random.Random(5)
        for _ in range(20):
            permuted = permute_within_blocks(corpus, "N45", key_face, rng)
            self.assertEqual([("N01" in ln.n_signs) for ln in permuted], [True, True])


class AgainstPublishedNumbers(unittest.TestCase):
    """These are the tests that make this attempt comparable to the published set."""

    @classmethod
    def setUpClass(cls):
        path = _FACE / "corpus_path.txt"
        if not path.exists():
            raise unittest.SkipTest("corpus_path.txt absent")
        raw, _ = load_lines(Path(path.read_text().strip()))
        cls.validation = [
            ln for ln in eligible(raw) if split_name(ln.tablet) == "validation"
        ]

    def test_reproduces_published_face_blocked_p_values(self):
        for m_sign, target, direction in CONFIRMED:
            got = block_report(self.validation, m_sign, target, key_face, direction)["p"]
            self.assertAlmostEqual(
                got, PUBLISHED_FACE_BLOCKED_P[f"{m_sign}-{target}"], places=4,
                msg=f"{m_sign}-{target}",
            )

    def test_reproduces_published_power_floors(self):
        for m_sign, target, direction in CONFIRMED:
            got = block_report(self.validation, m_sign, target, key_face, direction)
            self.assertAlmostEqual(
                got["p_floor"], PUBLISHED_FACE_BLOCKED_FLOOR[f"{m_sign}-{target}"],
                places=4, msg=f"{m_sign}-{target}",
            )

    def test_agrees_with_the_audited_implementation(self):
        for m_sign, target, direction in CONFIRMED:
            mine = block_report(self.validation, m_sign, target, key_face, direction)["p"]
            theirs = blocked_randomization_p(
                self.validation, m_sign, target, direction,
                lambda ln: (ln.tablet, ln.surface),
            )
            self.assertAlmostEqual(mine, theirs, places=12, msg=f"{m_sign}-{target}")

    def test_m288_n45_has_four_informative_blocks_on_bucket_zero(self):
        report = block_report(self.validation, "M288", "N45", key_face, "enriched")
        self.assertEqual(report["informative_blocks"], 4)
        self.assertFalse(report["has_power_at_05"])

    def test_screen_recovers_the_pair_on_the_published_training_set(self):
        raw, _ = load_lines(Path((_FACE / "corpus_path.txt").read_text().strip()))
        train = [ln for ln in eligible(raw) if split_name(ln.tablet) == "train"]
        self.assertIn("M288-N45", screen(train)["selected"])


if __name__ == "__main__":
    unittest.main()
