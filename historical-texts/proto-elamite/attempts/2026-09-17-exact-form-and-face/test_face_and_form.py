#!/usr/bin/env python3
"""Tests for the 2026-09-17 face/exact-form audit.

The load-bearing test is `test_tablet_block_reproduces_published_p_values`: the new
parameterised randomization must return the 2026-09-04 numbers to the last digit when
given the tablet block key. If it does not, every face-blocked number in this attempt
is uninterpretable.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from face_and_form import (
    CONFIRMED,
    blocked_randomization_p,
    contingency,
    eligible,
    exact_forms,
    load_lines,
    profile,
    total_variation,
)

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))
from structure_associations import split_name  # noqa: E402

CORPUS = Path(__file__).with_name("corpus_path.txt")


def corpus_dir() -> Path:
    return Path(CORPUS.read_text(encoding="utf-8").strip())


class ExactFormTests(unittest.TestCase):
    def test_value_annotated_form(self):
        self.assertEqual(exact_forms("ri2<M297<M297~B , 2(N39B)", "M297"), {"M297~B"})

    def test_plain_form(self):
        self.assertEqual(exact_forms("ri2<M297<M297 , 2(N39B)", "M297"), {"M297"})

    def test_orientation_retained(self):
        self.assertEqual(exact_forms("ri2<M297<M297@b ,", "M297"), {"M297@b"})

    def test_compound_members_are_separate_forms(self):
        self.assertEqual(exact_forms("M297+M296 ,", "M297"), {"M297"})
        self.assertEqual(exact_forms("M297~B+M388 ,", "M297"), {"M297~B"})

    def test_numeral_field_is_not_scanned(self):
        # An M-sign after the comma is not an entry-field occurrence.
        self.assertEqual(exact_forms("M263 , 1(N01) M297", "M297"), set())

    def test_other_family_ignored(self):
        self.assertEqual(exact_forms("ri2<M297<M297~B ,", "M296"), set())


class DistanceTests(unittest.TestCase):
    def test_identical_profiles_are_zero(self):
        self.assertEqual(total_variation([0.1, 0.2], [0.1, 0.2]), 0.0)

    def test_disjoint_profiles_are_one(self):
        self.assertEqual(total_variation([1.0, 0.0], [0.0, 1.0]), 1.0)

    def test_mean_absolute_difference(self):
        self.assertAlmostEqual(total_variation([1.0, 0.0], [0.0, 0.0]), 0.5)


class CorpusTests(unittest.TestCase):
    """End-to-end checks against the pinned corpus."""

    @classmethod
    def setUpClass(cls):
        if not CORPUS.exists():
            raise unittest.SkipTest("corpus_path.txt not present")
        lines, _ = load_lines(corpus_dir())
        cls.eligible = eligible(lines)
        cls.validation = [ln for ln in cls.eligible if split_name(ln.tablet) == "validation"]

    def test_validation_line_count_matches_published_run(self):
        # analysis/results/associations.json records 1050 validation M+N lines.
        self.assertEqual(len(self.validation), 1050)

    def test_tablet_block_reproduces_published_p_values(self):
        published = {
            ("M297", "N39B"): 4.385332409747139e-06,
            ("M297", "N24"): 0.00030402662116529476,
            ("M297", "N01"): 0.00029696729663097155,
            ("M263", "N30C"): 0.0012307554600787746,
            ("M263", "N01"): 0.001749703554343871,
            ("M243", "N39B"): 0.002467279309384563,
            ("M106", "N24"): 0.005059860725189959,
            ("M288", "N45"): 0.00711538461538455,
        }
        for m_sign, n_sign, direction in CONFIRMED:
            with self.subTest(pair=(m_sign, n_sign)):
                p = blocked_randomization_p(
                    self.validation, m_sign, n_sign, direction, lambda ln: ln.tablet
                )
                self.assertAlmostEqual(p, published[(m_sign, n_sign)], delta=1e-12)

    def test_published_contingency_cells_reproduce(self):
        published = {
            ("M297", "N39B"): (32, 23, 96, 899),
            ("M263", "N30C"): (0, 46, 68, 936),
            ("M288", "N45"): (15, 103, 8, 924),
        }
        for pair, cells in published.items():
            with self.subTest(pair=pair):
                self.assertEqual(contingency(self.validation, *pair), cells)

    def test_face_blocking_is_strictly_finer(self):
        tablets = {ln.tablet for ln in self.validation}
        faces = {(ln.tablet, ln.surface) for ln in self.validation}
        self.assertGreater(len(faces), len(tablets))

    def test_profile_length_matches_vocabulary(self):
        vocab = ["N01", "N14", "N39B"]
        p = profile(self.eligible, "M297", vocab)
        self.assertEqual(len(p), 3)
        self.assertTrue(all(0.0 <= v <= 1.0 for v in p))


if __name__ == "__main__":
    unittest.main(verbosity=2)
