import tempfile
import unittest
from pathlib import Path

from structure_associations import (
    Line,
    bh_adjust,
    blocked_randomization_p,
    fisher_exact_two_sided,
    normalize_n_sign,
    parse_tablet,
    split_name,
)


class StructureAssociationTests(unittest.TestCase):
    def test_parse_tablet_preserves_surface_order_and_filters_reading_aliases(self):
        fixture = """&P123456 = fixture
@tablet
@obverse
@column 1
1. li<M319<M319~A M157 ,
2. M346 , 2(N1@b)
3. M036+1(N30D) , 5(N01)
@reverse
1. M346 ... , 1(N14)
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "P123456.values.atf"
            path.write_text(fixture, encoding="utf-8")
            lines = parse_tablet(path)

        self.assertEqual(4, len(lines))
        self.assertEqual("obverse", lines[0].surface)
        self.assertEqual(1, lines[0].ordinal_on_surface)
        self.assertEqual(frozenset({"M319", "M157"}), lines[0].m_signs)
        self.assertEqual(frozenset({"N01@b"}), lines[1].n_signs)
        self.assertEqual(frozenset({"N01"}), lines[2].n_signs)
        self.assertTrue(lines[3].damaged)

    def test_fisher_exact_matches_known_example(self):
        self.assertAlmostEqual(0.002759456, fisher_exact_two_sided(1, 9, 11, 3), places=8)

    def test_bh_adjust_is_monotonic_in_rank_order(self):
        adjusted = bh_adjust([0.01, 0.04, 0.03, 0.002])
        self.assertEqual([0.02, 0.04, 0.04, 0.008], [round(value, 3) for value in adjusted])

    def test_split_is_deterministic(self):
        self.assertEqual(split_name("P008001"), split_name("P008001"))
        self.assertIn(split_name("P008001"), {"train", "validation"})

    def test_normalize_n_sign_only_changes_padding_and_case(self):
        self.assertEqual("N01@b", normalize_n_sign("N1@b"))
        self.assertEqual("N39B", normalize_n_sign("N39B"))
        self.assertEqual("N39~b", normalize_n_sign("N39~b"))

    def test_blocked_randomization_respects_tablets(self):
        lines = []
        for tablet in ("P1", "P2"):
            lines.extend(
                [
                    Line(tablet, "obverse", "1", 1, "", frozenset({"M001"}), frozenset({"N01"}), False),
                    Line(tablet, "obverse", "2", 2, "", frozenset({"M002"}), frozenset({"N02"}), False),
                ]
            )
        p_value = blocked_randomization_p(
            lines, "M001", lambda line: "N01" in line.n_signs, "enriched"
        )
        self.assertAlmostEqual(0.25, p_value)


if __name__ == "__main__":
    unittest.main()
