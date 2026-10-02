#!/usr/bin/env python3
"""Tests for the block-aware split.

The load-bearing tests are the two that pin this file's reimplemented blocked exact test
against the already-audited 2026-09-04 and 2026-09-17 implementations. If those fail,
nothing else in this directory means anything.

Needs the pinned corpus; path from corpus_path.txt or $PE_CORPUS.
"""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[0] / "2026-09-17-exact-form-and-face"))
sys.path.insert(0, str(HERE.parents[1] / "analysis"))

import block_aware_split as bas
from structure_associations import Line, blocked_randomization_p, split_name
from power_floor import floors as prev_floors
from face_and_form import eligible, load_lines


def corpus_dir() -> Path | None:
    env = os.environ.get("PE_CORPUS")
    if env:
        return Path(env)
    txt = HERE / "corpus_path.txt"
    if txt.exists():
        return Path(txt.read_text().strip())
    return None


def mk(tablet, surface, m, n, ordinal=1, damaged=False):
    return Line(
        tablet=tablet, surface=surface, label=str(ordinal), ordinal_on_surface=ordinal,
        text="", m_signs=frozenset(m), n_signs=frozenset(n), damaged=damaged,
    )


class TestFloorArithmetic(unittest.TestCase):
    def test_floor_is_product_of_block_max_probabilities(self):
        """p_floor must equal the product of P(max overlap) over informative blocks."""
        lines = [
            mk("T1", "obverse", ["M1"], ["N1"]), mk("T1", "obverse", ["M1"], [], 2),
            mk("T1", "obverse", [], ["N1"], 3), mk("T1", "obverse", [], [], 4),
            mk("T2", "reverse", ["M1"], ["N1"]), mk("T2", "reverse", [], ["N1"], 2),
            mk("T2", "reverse", [], [], 3),
        ]
        res = bas.blocked_p_and_floor(lines, "M1", "N1", "enriched")
        info = bas.informative_blocks(bas.block_marginals(lines, "M1", "N1"))
        self.assertEqual(len(info), 2)
        self.assertAlmostEqual(res["p_floor"], bas.floor_from_blocks(info), places=12)

    def test_non_informative_block_cannot_change_the_p_value(self):
        """A block with hi == lo shifts observed and support equally; p is unchanged."""
        base = [
            mk("T1", "obverse", ["M1"], ["N1"]), mk("T1", "obverse", ["M1"], [], 2),
            mk("T1", "obverse", [], ["N1"], 3), mk("T1", "obverse", [], [], 4),
        ]
        forced = base + [mk("T9", "obverse", ["M1"], ["N1"]), mk("T9", "obverse", ["M1"], ["N1"], 2)]
        a = bas.blocked_p_and_floor(base, "M1", "N1", "enriched")
        b = bas.blocked_p_and_floor(forced, "M1", "N1", "enriched")
        self.assertAlmostEqual(a["p"], b["p"], places=12)
        self.assertEqual(a["informative_blocks"], b["informative_blocks"])
        self.assertEqual(b["observed_overlap"], a["observed_overlap"] + 2)

    def test_split_rule_reads_only_marginals(self):
        """Moving the overlap around while holding every block marginal fixed must not
        change the carrier set, the informative blocks, or the floor."""
        lines = [
            mk("T1", "obverse", ["M1"], ["N1"]), mk("T1", "obverse", ["M1"], [], 2),
            mk("T1", "obverse", [], ["N1"], 3), mk("T1", "obverse", [], [], 4),
        ]
        swapped = [
            mk("T1", "obverse", ["M1"], []), mk("T1", "obverse", ["M1"], ["N1"], 2),
            mk("T1", "obverse", [], ["N1"], 3), mk("T1", "obverse", [], [], 4),
        ]
        self.assertEqual(
            bas.informative_blocks(bas.block_marginals(lines, "M1", "N1")),
            bas.informative_blocks(bas.block_marginals(swapped, "M1", "N1")),
        )
        self.assertEqual(
            bas.carrier_tablets(lines, "M1", "N1"), bas.carrier_tablets(swapped, "M1", "N1")
        )


class TestAgreementWithAuditedCode(unittest.TestCase):
    """Pin this file's blocked test against the two implementations already on record."""

    @classmethod
    def setUpClass(cls):
        d = corpus_dir()
        if d is None or not d.exists():
            raise unittest.SkipTest("pinned corpus not available; set PE_CORPUS")
        lines, _ = load_lines(d)
        cls.el = eligible(lines)
        cls.val = [ln for ln in cls.el if split_name(ln.tablet) == "validation"]

    def test_tablet_blocked_matches_2026_09_04_implementation(self):
        for m, n, d in bas.CONFIRMED:
            mine = bas.blocked_p_and_floor(
                self.val, m, n, d, block_key=lambda ln: ln.tablet
            )["p"]
            theirs = blocked_randomization_p(
                self.val, m, lambda ln, t=n: t in ln.n_signs, d
            )
            self.assertAlmostEqual(mine, theirs, delta=1e-12 + 1e-9 * theirs,
                                   msg=f"{m}-{n}")

    def test_face_blocked_matches_2026_09_17_implementation(self):
        for m, n, d in bas.CONFIRMED:
            mine = bas.blocked_p_and_floor(self.val, m, n, d)
            theirs = prev_floors(self.val, m, n, d, lambda ln: (ln.tablet, ln.surface))
            self.assertAlmostEqual(mine["p"], theirs["p"], delta=1e-12 + 1e-9 * theirs["p"],
                                   msg=f"{m}-{n} p")
            self.assertAlmostEqual(mine["p_floor"], theirs["p_floor"],
                                   delta=1e-12 + 1e-9 * theirs["p_floor"], msg=f"{m}-{n} floor")
            self.assertEqual(mine["informative_blocks"], theirs["informative_blocks"])

    def test_published_m288_n45_floor_is_0_12(self):
        r = bas.blocked_p_and_floor(self.val, "M288", "N45", "enriched")
        self.assertEqual(r["informative_blocks"], 4)
        self.assertAlmostEqual(r["p_floor"], 0.12, places=10)

    def test_arms_partition_the_carriers_disjointly(self):
        _, carriers, a = bas.arm_split(self.el, "A")
        _, _, b = bas.arm_split(self.el, "B")
        self.assertEqual(sorted(a + b), carriers)
        self.assertEqual(set(a) & set(b), set())
        self.assertEqual(len(carriers), 15)

    def test_each_arm_is_powered_and_floor_matches_marginal_product(self):
        for arm in ("A", "B"):
            val_tablets, _, _ = bas.arm_split(self.el, arm)
            val = [ln for ln in self.el if ln.tablet in val_tablets]
            r = bas.blocked_p_and_floor(val, "M288", "N45", "enriched")
            info = bas.informative_blocks(bas.block_marginals(val, "M288", "N45"))
            self.assertAlmostEqual(r["p_floor"], bas.floor_from_blocks(info), places=12)
            self.assertLessEqual(r["p_floor"], 0.05, msg=f"arm {arm} must be powered")

    def test_enumeration_reproduces_the_full_corpus_p_at_the_all_carriers_mask(self):
        e = bas.enumerate_splits(self.el)
        full_mask = (1 << len(e["carrier_tablets"])) - 1
        row = next(r for r in e["all"] if r["mask"] == full_mask)
        whole = bas.blocked_p_and_floor(self.el, "M288", "N45", "enriched")
        self.assertAlmostEqual(row["p"], whole["p"], delta=1e-12 + 1e-9 * whole["p"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
