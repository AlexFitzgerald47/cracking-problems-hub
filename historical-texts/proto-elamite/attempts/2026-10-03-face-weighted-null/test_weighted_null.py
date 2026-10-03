#!/usr/bin/env python3
"""Tests for the face-weighted null.

The load-bearing test is `test_w_one_reproduces_published_test`: with w = 1 the
weighted distribution must equal the 2026-09-04 within-tablet hypergeometric test to
1e-12 on all eight published pairs. Every weighted number reported by this attempt
comes from the same function with w != 1, so that identity is what makes the
comparison like-for-like.

Run:  python3 -m unittest -v test_weighted_null
(requires corpus_path.txt, as in the 2026-09-17 attempt)
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
_ANALYSIS = Path(__file__).resolve().parents[2] / "analysis"
sys.path.insert(0, str(_ANALYSIS))

from structure_associations import Line, blocked_randomization_p  # noqa: E402
from weighted_null import (  # noqa: E402
    face_weight,
    is_reverse,
    load_eligible,
    tablet_overlap_distribution,
    weighted_randomization_p,
)

CONFIRMED = [
    ("M297", "N39B", "enriched"),
    ("M297", "N24", "enriched"),
    ("M297", "N01", "depleted"),
    ("M263", "N30C", "depleted"),
    ("M263", "N01", "enriched"),
    ("M243", "N39B", "enriched"),
    ("M106", "N24", "enriched"),
    ("M288", "N45", "enriched"),
]

_CORPUS_FILE = Path(__file__).with_name("corpus_path.txt")


def _mk(tablet, surface, m, n):
    return Line(
        tablet=tablet,
        surface=surface,
        label="1",
        ordinal_on_surface=1,
        text="",
        m_signs=frozenset(m),
        n_signs=frozenset(n),
        damaged=False,
    )


class TestUnitLevel(unittest.TestCase):
    def test_distribution_sums_to_one(self):
        block = [
            _mk("P1", "obverse", ["M288"], ["N45"]),
            _mk("P1", "obverse", ["M288"], ["N01"]),
            _mk("P1", "reverse", ["M999"], ["N45"]),
            _mk("P1", "reverse", ["M999"], ["N01"]),
        ]
        for w in (0.25, 1.0, 3.0, 50.0):
            dist = tablet_overlap_distribution(block, "M288", "N45", w)
            self.assertAlmostEqual(sum(dist), 1.0, places=12)

    def test_w_one_is_hypergeometric(self):
        # 4 lines, 2 carry the sign, 2 carry the target: overlap ~ Hypergeom(4,2,2)
        block = [
            _mk("P1", "obverse", ["M288"], ["N45"]),
            _mk("P1", "obverse", ["M288"], ["N01"]),
            _mk("P1", "obverse", [], ["N45"]),
            _mk("P1", "obverse", [], ["N01"]),
        ]
        dist = tablet_overlap_distribution(block, "M288", "N45", 1.0)
        self.assertAlmostEqual(dist[0], 1 / 6, places=12)
        self.assertAlmostEqual(dist[1], 4 / 6, places=12)
        self.assertAlmostEqual(dist[2], 1 / 6, places=12)

    def test_large_w_forces_target_onto_reverse(self):
        # Sign is obverse-only; as w grows the target is driven to the reverse, so the
        # overlap must collapse to zero.
        block = [
            _mk("P1", "obverse", ["M288"], ["N45"]),
            _mk("P1", "obverse", ["M288"], ["N01"]),
            _mk("P1", "reverse", [], ["N01"]),
            _mk("P1", "reverse", [], ["N01"]),
        ]
        w = 10_000.0
        dist = tablet_overlap_distribution(block, "M288", "N45", w)
        # One target to place among 2 obverse sign-lines and 2 reverse non-sign lines:
        # P(overlap = 0) = 2w / (2w + 2), which tends to 1 but is never equal to it.
        self.assertAlmostEqual(dist[0], 2 * w / (2 * w + 2), places=12)
        self.assertGreater(dist[0], 0.9998)

    def test_single_line_block_is_degenerate(self):
        block = [_mk("P1", "obverse", ["M288"], ["N45"])]
        self.assertEqual(tablet_overlap_distribution(block, "M288", "N45", 7.0), [0.0, 1.0])

    def test_face_weight_recovers_a_planted_skew(self):
        lines = []
        for i in range(100):
            lines.append(_mk(f"T{i}", "reverse", ["M999"], ["N45"] if i < 50 else ["N01"]))
        for i in range(100):
            lines.append(_mk(f"U{i}", "obverse", ["M999"], ["N45"] if i < 10 else ["N01"]))
        info = face_weight(lines, "M288", "N45")
        self.assertAlmostEqual(info["reverse_rate"], 0.50, places=6)
        self.assertAlmostEqual(info["obverse_rate"], 0.10, places=6)
        self.assertGreater(info["w"], 8.0)
        self.assertLess(info["w"], 10.0)

    def test_face_weight_ignores_lines_with_the_sign_under_test(self):
        lines = [
            _mk("T1", "reverse", ["M288"], ["N45"]),
            _mk("T2", "reverse", [], ["N01"]),
            _mk("T3", "obverse", [], ["N01"]),
        ]
        info = face_weight(lines, "M288", "N45")
        self.assertEqual(info["reverse_target"], 0)
        self.assertEqual(info["reverse_other"], 1)

    def test_is_reverse(self):
        self.assertTrue(is_reverse(_mk("T", "reverse", [], [])))
        self.assertFalse(is_reverse(_mk("T", "obverse", [], [])))
        self.assertFalse(is_reverse(_mk("T", "unspecified", [], [])))


@unittest.skipUnless(_CORPUS_FILE.exists(), "corpus_path.txt not present")
class TestAgainstPublishedNumbers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lines = load_eligible(Path(_CORPUS_FILE.read_text().strip()))

    def test_corpus_matches_published_audit(self):
        self.assertEqual(len(self.lines), 4869)

    def test_w_one_reproduces_published_test(self):
        """w = 1 must equal structure_associations.blocked_randomization_p exactly."""
        for m_sign, n_sign, direction in CONFIRMED:
            with self.subTest(pair=f"{m_sign}-{n_sign}"):
                expected = blocked_randomization_p(
                    self.lines,
                    m_sign,
                    lambda ln, t=n_sign: t in ln.n_signs,
                    direction,
                )
                got = weighted_randomization_p(
                    self.lines, m_sign, n_sign, direction, w=1.0
                )["p"]
                self.assertAlmostEqual(got, expected, delta=1e-12)

    def test_p_is_monotone_in_w_for_the_target_pair(self):
        previous = 0.0
        for w in (1.0, 2.0, 4.0, 8.0, 16.0):
            p = weighted_randomization_p(self.lines, "M288", "N45", "enriched", w)["p"]
            self.assertGreaterEqual(p + 1e-15, previous)
            previous = p


if __name__ == "__main__":
    unittest.main()
