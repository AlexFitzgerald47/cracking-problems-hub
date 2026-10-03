#!/usr/bin/env python3
"""Unit tests for the 2026-10-01 block-aware machinery."""
import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from blocks import blocked_exact, is_informative, odds_ratio


class L:
    def __init__(self, tablet, surface, m, n):
        self.tablet, self.surface = tablet, surface
        self.m_signs, self.n_signs = frozenset(m), frozenset(n)


def key(ln):
    return (ln.tablet, ln.surface)


class TestInformative(unittest.TestCase):
    def test_saturated_block_is_not_informative(self):
        # every line carries the sign: the overlap is forced to equal t
        self.assertFalse(is_informative(total=4, s=4, t=1))

    def test_target_saturated_block_is_not_informative(self):
        self.assertFalse(is_informative(total=4, s=2, t=4))

    def test_absent_sign_is_not_informative(self):
        self.assertFalse(is_informative(total=4, s=0, t=2))

    def test_ordinary_block_is_informative(self):
        self.assertTrue(is_informative(total=4, s=2, t=1))

    def test_informative_depends_only_on_marginals(self):
        # same marginals, opposite overlaps -> same verdict
        self.assertEqual(is_informative(3, 1, 1), is_informative(3, 1, 1))


class TestBlockedExact(unittest.TestCase):
    def two_line_block(self, overlap):
        """One block: 2 lines, 1 carries M, 1 carries N. p must be 1/2 or 1."""
        if overlap:
            return [L("T", "obverse", ["M1"], ["N1"]), L("T", "obverse", [], [])]
        return [L("T", "obverse", ["M1"], []), L("T", "obverse", [], ["N1"])]

    def test_single_block_exact_half(self):
        r = blocked_exact(self.two_line_block(True), "M1", "N1", "enriched", key)
        self.assertAlmostEqual(r["p"], 0.5)
        self.assertAlmostEqual(r["p_floor"], 0.5)
        self.assertEqual(r["informative_blocks"], 1)

    def test_single_block_miss(self):
        r = blocked_exact(self.two_line_block(False), "M1", "N1", "enriched", key)
        self.assertAlmostEqual(r["p"], 1.0)

    def test_five_blocks_all_hit_is_two_to_the_minus_five(self):
        lines = []
        for i in range(5):
            lines += [L(f"T{i}", "obverse", ["M1"], ["N1"]), L(f"T{i}", "obverse", [], [])]
        r = blocked_exact(lines, "M1", "N1", "enriched", key)
        self.assertAlmostEqual(r["p"], 0.5 ** 5)
        self.assertAlmostEqual(r["p_floor"], 0.5 ** 5)

    def test_forced_blocks_do_not_change_p(self):
        """A saturated block shifts observed and the null by the same constant."""
        base = [L("T0", "obverse", ["M1"], ["N1"]), L("T0", "obverse", [], [])]
        forced = [L("T9", "obverse", ["M1"], ["N1"]), L("T9", "obverse", ["M1"], [])]
        a = blocked_exact(base, "M1", "N1", "enriched", key)
        b = blocked_exact(base + forced, "M1", "N1", "enriched", key)
        self.assertAlmostEqual(a["p"], b["p"])
        self.assertEqual(b["informative_blocks"], 1)
        self.assertEqual(b["blocks"], 2)

    def test_floor_bounds_p(self):
        lines = [L("T0", "obverse", ["M1"], []), L("T0", "obverse", [], ["N1"]),
                 L("T1", "obverse", ["M1"], ["N1"]), L("T1", "obverse", [], [])]
        r = blocked_exact(lines, "M1", "N1", "enriched", key)
        self.assertLessEqual(r["p_floor"], r["p"])

    def test_depleted_direction(self):
        lines = [L("T0", "obverse", ["M1"], []), L("T0", "obverse", [], ["N1"])]
        r = blocked_exact(lines, "M1", "N1", "depleted", key)
        self.assertAlmostEqual(r["p"], 0.5)


class TestOddsRatio(unittest.TestCase):
    def test_zero_cell_is_finite(self):
        self.assertTrue(0 < odds_ratio(0, 10, 10, 100) < float("inf"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
