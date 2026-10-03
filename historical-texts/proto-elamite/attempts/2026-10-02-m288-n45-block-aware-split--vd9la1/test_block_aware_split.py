#!/usr/bin/env python3
"""Tests for the 2026-10-02 block-aware split.

The load-bearing test is `test_reproduces_2026_09_17_face_blocked_values`: the same
`floor_and_p` used for every number in RESULTS.md must return the eight face-blocked
p-values and floors recorded by the 2026-09-17 session when handed that session's
bucket-0 holdout. If it does, the new figures are like-for-like with the old by
construction rather than by assertion.

The validity tests are `test_informativeness_depends_only_on_marginals` and
`test_split_is_invariant_to_observed_overlap`: the split rule's whole defence is that it
reads block marginals and never the observed overlap. Those two hold the marginals fixed,
move the overlap around, and require the chosen validation set not to budge.

Run:  python3 -m unittest -v test_block_aware_split.py
"""
from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

from common import Line, block_stats, face_key, load_eligible
from block_aware_split import (contingency, floor_and_p, informative_tablets,
                               rescreen, split_for_pair)
from structure_associations import split_name

# The reference is READ from the 2026-09-17 session's committed result file rather
# than retyped, so the comparison is against its full stored precision and no
# transcription step can soften it.
_PF = (Path(__file__).resolve().parents[1]
       / "2026-09-17-exact-form-and-face" / "results" / "power_floor.json")
REFERENCE_2026_09_17 = {}
if _PF.exists():
    import json as _json
    for _pair, _v in _json.loads(_PF.read_text()).items():
        _m, _n = _pair.split("-", 1)
        _f = _v["face_blocked"]
        REFERENCE_2026_09_17[(_m, _n, _v["direction"])] = (
            _f["p"], _f["p_floor"], _f["informative_blocks"])


def mk(tablet, surface, m, n, i=0):
    return Line(tablet=tablet, surface=surface, label=str(i), ordinal_on_surface=i,
                text="", m_signs=frozenset(m), n_signs=frozenset(n), damaged=False)


class TestSyntheticBlockLogic(unittest.TestCase):
    def test_single_line_face_is_never_informative(self):
        """27 of the 36 forced co-occurrence blocks are single-line faces."""
        lines = [mk("P1", "reverse", ["M288"], ["N45"])]
        rows = block_stats(lines, "M288", "N45")
        self.assertEqual(len(rows), 1)
        self.assertFalse(rows[0]["informative"])
        self.assertEqual(rows[0]["lo"], rows[0]["hi"])

    def test_forced_blocks_contribute_a_constant_not_a_p_value(self):
        """A forced block shifts observed and max equally, so p is unchanged."""
        free = [mk("P1", "obverse", ["M288"], [], 1),
                mk("P1", "obverse", [], ["N45"], 2)]
        p_free = floor_and_p(free, "M288", "N45", "enriched")
        plus_forced = free + [mk("P2", "reverse", ["M288"], ["N45"], 1)]
        p_both = floor_and_p(plus_forced, "M288", "N45", "enriched")
        self.assertAlmostEqual(p_free["p"], p_both["p"], places=12)
        self.assertEqual(p_both["observed_overlap"], p_free["observed_overlap"] + 1)
        self.assertEqual(p_both["max_possible_overlap"],
                         p_free["max_possible_overlap"] + 1)

    def test_informativeness_depends_only_on_marginals(self):
        """Same marginals, opposite overlap -> same informativeness."""
        hit = [mk("P1", "obverse", ["M288"], ["N45"], 1),
               mk("P1", "obverse", [], [], 2)]
        miss = [mk("P1", "obverse", ["M288"], [], 1),
                mk("P1", "obverse", [], ["N45"], 2)]
        for lines in (hit, miss):
            rows = block_stats(lines, "M288", "N45")
            self.assertEqual([r["informative"] for r in rows], [True])
        self.assertEqual(floor_and_p(hit, "M288", "N45", "enriched")["observed_overlap"], 1)
        self.assertEqual(floor_and_p(miss, "M288", "N45", "enriched")["observed_overlap"], 0)

    def test_split_puts_no_tablet_on_both_sides(self):
        lines = [mk("P1", "obverse", ["M288"], ["N45"], 1),
                 mk("P1", "obverse", [], [], 2),
                 mk("P1", "reverse", ["M288"], ["N45"], 1),
                 mk("P2", "obverse", ["M288"], [], 1)]
        train, val, val_tabs = split_for_pair(lines, "M288", "N45")
        self.assertEqual({ln.tablet for ln in train} & {ln.tablet for ln in val}, set())
        self.assertEqual(val_tabs, {"P1"})
        # the forced P1 reverse block travels with its tablet
        self.assertEqual(len(val), 3)


class TestAgainstRealCorpus(unittest.TestCase):
    """These need the pinned corpus; skipped if corpus_path.txt is absent."""

    @classmethod
    def setUpClass(cls):
        try:
            cls.lines = load_eligible(["x"])
        except Exception as exc:  # pragma: no cover
            raise unittest.SkipTest(f"pinned corpus unavailable: {exc}")

    def test_eligible_line_count_matches_published_audit(self):
        self.assertEqual(len(self.lines), 4869)

    def test_reproduces_2026_09_17_face_blocked_values(self):
        """Load-bearing: identical function, that session's bucket-0 holdout."""
        self.assertEqual(len(REFERENCE_2026_09_17), 8,
                         "2026-09-17 power_floor.json not found or incomplete")
        val = [ln for ln in self.lines if split_name(ln.tablet) == "validation"]
        for (m, n, d), (p_ref, floor_ref, inf_ref) in REFERENCE_2026_09_17.items():
            with self.subTest(pair=f"{m}-{n}"):
                got = floor_and_p(val, m, n, d)
                self.assertAlmostEqual(got["p"], p_ref, delta=abs(p_ref) * 1e-12)
                self.assertAlmostEqual(got["p_floor"], floor_ref,
                                       delta=abs(floor_ref) * 1e-12)
                self.assertEqual(got["informative_blocks"], inf_ref)
                self.assertEqual(got["blocks"], 290)

    def test_m288_n45_has_sixteen_informative_blocks_corpus_wide(self):
        rows = block_stats(self.lines, "M288", "N45")
        self.assertEqual(sum(r["informative"] for r in rows), 16)
        self.assertEqual(len(rows), 1426)

    def test_split_is_invariant_to_observed_overlap(self):
        """Permute N45 WITHIN each (tablet, face) block, preserving all marginals.

        The validation tablet set must be identical every time: it is a function of
        marginals, and this permutation changes only the overlap. This is the empirical
        form of the ancillarity argument the design rests on.
        """
        baseline = informative_tablets(self.lines, "M288", "N45")
        by_block: dict[object, list[int]] = {}
        for i, ln in enumerate(self.lines):
            by_block.setdefault(face_key(ln), []).append(i)
        rng = random.Random(7)
        for _ in range(25):
            flags = ["N45" in ln.n_signs for ln in self.lines]
            for idx in by_block.values():
                if len(idx) > 1:
                    vals = [flags[i] for i in idx]
                    rng.shuffle(vals)
                    for i, v in zip(idx, vals):
                        flags[i] = v
            shuffled = [
                Line(tablet=ln.tablet, surface=ln.surface, label=ln.label,
                     ordinal_on_surface=ln.ordinal_on_surface, text=ln.text,
                     m_signs=ln.m_signs,
                     n_signs=frozenset(({"N45"} if flags[i] else set())
                                       | (ln.n_signs - {"N45"})),
                     damaged=ln.damaged)
                for i, ln in enumerate(self.lines)
            ]
            self.assertEqual(informative_tablets(shuffled, "M288", "N45"), baseline)

    def test_rescreen_uses_training_only_and_selects_m288_n45(self):
        train, val, _ = split_for_pair(self.lines, "M288", "N45")
        self.assertEqual(len(train) + len(val), len(self.lines))
        screen, n_cands, n_sel = rescreen(train, "M288", "N45")
        self.assertIsNotNone(screen)
        self.assertTrue(screen["selected"])
        self.assertLessEqual(screen["q"], 0.01)
        self.assertGreaterEqual(screen["odds_ratio"], 3.0)
        # the screen must not see a single validation line
        val_tabs = {ln.tablet for ln in val}
        self.assertFalse(any(ln.tablet in val_tabs for ln in train))

    def test_depleted_direction_floor_is_the_minimum_attainable(self):
        _, val, _ = split_for_pair(self.lines, "M263", "N30C")
        got = floor_and_p(val, "M263", "N30C", "depleted")
        self.assertEqual(got["observed_overlap"], got["min_possible_overlap"])
        self.assertAlmostEqual(got["p"], got["p_floor"], places=12)


if __name__ == "__main__":
    unittest.main()
