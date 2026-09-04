#!/usr/bin/env python3
"""Find held-out Proto-Elamite structural associations in the SFU/CDLI ATF corpus.

The analysis deliberately stops short of assigning meanings. It asks two narrower,
falsifiable questions:

1. Which M-sign families are disproportionately present on the first obverse line?
2. Which M-sign families are disproportionately associated with particular N-sign
   families on intact lines?

Candidates are selected on an 80% tablet split and tested once on the remaining 20%.
No tablet contributes lines to both splits.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


LINE_RE = re.compile(r"^\s*([0-9]+[A-Za-z']*)\.\s*(.*)$")
M_SIGN_RE = re.compile(r"M[0-9]{3}")
N_SIGN_RE = re.compile(r"\((N[0-9]+[A-Za-z]?(?:~[A-Za-z]+)?(?:@[A-Za-z]+)?)\)")
DAMAGE_RE = re.compile(r"\.\.\.|(?<![A-Za-z0-9])x(?![A-Za-z0-9])")
FACE_TAGS = {"obverse", "reverse", "top", "bottom", "left", "right", "edge"}


@dataclass(frozen=True)
class Line:
    tablet: str
    surface: str
    label: str
    ordinal_on_surface: int
    text: str
    m_signs: frozenset[str]
    n_signs: frozenset[str]
    damaged: bool


@dataclass(frozen=True)
class Association:
    analysis: str
    m_sign: str
    target: str
    train_a: int
    train_b: int
    train_c: int
    train_d: int
    train_odds_ratio: float
    train_p: float
    train_q: float
    validation_a: int
    validation_b: int
    validation_c: int
    validation_d: int
    validation_odds_ratio: float
    validation_p: float
    validation_q: float


def normalize_n_sign(raw: str) -> str:
    """Normalize zero-padding only; preserve letter and orientation variants."""
    match = re.fullmatch(
        r"N([0-9]+)([A-Za-z]?)(~[A-Za-z]+)?(@[A-Za-z]+)?", raw
    )
    if not match:
        return raw
    number, variant, modifier, orientation = match.groups()
    return (
        f"N{int(number):02d}{variant.upper()}"
        f"{(modifier or '').lower()}{(orientation or '').lower()}"
    )


def corpus_digest(files: Sequence[Path]) -> str:
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def parse_tablet(path: Path) -> list[Line]:
    tablet = path.name.split(".", 1)[0]
    surface = "unspecified"
    surface_ordinals: dict[str, int] = {}
    records: list[Line] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith("&"):
            tablet_match = re.match(r"&([A-Z][0-9]+)", raw_line)
            if tablet_match:
                tablet = tablet_match.group(1)
            continue
        if raw_line.startswith("@"):
            tag = raw_line[1:].strip().split()[0].lower()
            # @column and @seal subdivide a physical face; they must not erase
            # whether a line is on the obverse or reverse.
            if tag in FACE_TAGS:
                surface = tag
                surface_ordinals.setdefault(surface, 0)
            continue
        match = LINE_RE.match(raw_line)
        if not match:
            continue

        label, text = match.groups()
        surface_ordinals[surface] = surface_ordinals.get(surface, 0) + 1
        m_signs = frozenset(M_SIGN_RE.findall(text))
        # Parenthesized N-signs also occur inside compound M-sign expressions.
        # Only the field after the ATF entry-boundary comma is an accounting
        # numeral sequence. Numeral-only lines have no comma and remain eligible.
        numeric_field = text.split(",", 1)[1] if "," in text else text
        n_signs = frozenset(
            normalize_n_sign(value) for value in N_SIGN_RE.findall(numeric_field)
        )
        records.append(
            Line(
                tablet=tablet,
                surface=surface,
                label=label,
                ordinal_on_surface=surface_ordinals[surface],
                text=text,
                m_signs=m_signs,
                n_signs=n_signs,
                damaged=bool(DAMAGE_RE.search(text)),
            )
        )
    return records


def split_name(tablet: str) -> str:
    bucket = int(hashlib.sha256(tablet.encode("ascii")).hexdigest()[:8], 16) % 5
    return "validation" if bucket == 0 else "train"


def log_choose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def hypergeom_probability(a: int, row_one: int, col_one: int, total: int) -> float:
    return math.exp(
        log_choose(col_one, a)
        + log_choose(total - col_one, row_one - a)
        - log_choose(total, row_one)
    )


def fisher_exact_two_sided(a: int, b: int, c: int, d: int) -> float:
    """Two-sided Fisher exact p-value using the probability-ordering definition."""
    row_one = a + b
    col_one = a + c
    total = a + b + c + d
    observed = hypergeom_probability(a, row_one, col_one, total)
    lower = max(0, row_one - (total - col_one))
    upper = min(row_one, col_one)
    p_value = 0.0
    for candidate in range(lower, upper + 1):
        probability = hypergeom_probability(candidate, row_one, col_one, total)
        if probability <= observed * (1.0 + 1e-12):
            p_value += probability
    return min(1.0, p_value)


def odds_ratio(a: int, b: int, c: int, d: int) -> float:
    """Haldane-Anscombe corrected odds ratio, finite even with a zero cell."""
    return ((a + 0.5) * (d + 0.5)) / ((b + 0.5) * (c + 0.5))


def bh_adjust(p_values: Sequence[float]) -> list[float]:
    count = len(p_values)
    adjusted = [1.0] * count
    running_min = 1.0
    for rank, index in reversed(
        list(enumerate(sorted(range(count), key=p_values.__getitem__), start=1))
    ):
        running_min = min(running_min, p_values[index] * count / rank)
        adjusted[index] = min(1.0, running_min)
    return adjusted


def contingency(
    lines: Sequence[Line], m_sign: str, predicate
) -> tuple[int, int, int, int]:
    a = b = c = d = 0
    for line in lines:
        has_sign = m_sign in line.m_signs
        has_target = predicate(line)
        if has_sign and has_target:
            a += 1
        elif has_sign:
            b += 1
        elif has_target:
            c += 1
        else:
            d += 1
    return a, b, c, d


def blocked_randomization_p(
    lines: Sequence[Line], m_sign: str, predicate, direction: str
) -> float:
    """Exact one-sided test that shuffles the target only within each tablet.

    For each tablet, the overlap between sign-bearing lines and target lines follows
    a hypergeometric distribution under the null. Convolution gives the exact null
    distribution for the total overlap without treating same-tablet lines as
    independent.
    """
    by_tablet: dict[str, list[Line]] = {}
    for line in lines:
        by_tablet.setdefault(line.tablet, []).append(line)

    distribution = [1.0]
    observed_total = 0
    for tablet_lines in by_tablet.values():
        total = len(tablet_lines)
        sign_count = sum(m_sign in line.m_signs for line in tablet_lines)
        target_count = sum(bool(predicate(line)) for line in tablet_lines)
        observed_total += sum(
            m_sign in line.m_signs and bool(predicate(line)) for line in tablet_lines
        )
        lower = max(0, sign_count - (total - target_count))
        upper = min(sign_count, target_count)
        local = [0.0] * (upper + 1)
        for overlap in range(lower, upper + 1):
            local[overlap] = hypergeom_probability(
                overlap, sign_count, target_count, total
            )

        combined = [0.0] * (len(distribution) + len(local) - 1)
        for current_overlap, current_probability in enumerate(distribution):
            for local_overlap, local_probability in enumerate(local):
                combined[current_overlap + local_overlap] += (
                    current_probability * local_probability
                )
        distribution = combined

    if direction == "enriched":
        return min(1.0, sum(distribution[observed_total:]))
    if direction == "depleted":
        return min(1.0, sum(distribution[: observed_total + 1]))
    raise ValueError(f"unknown direction: {direction}")


def discover_and_validate(
    analysis: str,
    train_lines: Sequence[Line],
    validation_lines: Sequence[Line],
    targets: Iterable[tuple[str, object]],
    minimum_train_sign_lines: int,
    minimum_validation_sign_lines: int,
) -> list[Association]:
    train_signs = sorted({sign for line in train_lines for sign in line.m_signs})
    raw_candidates: list[dict[str, object]] = []

    for target_name, predicate in targets:
        for sign in train_signs:
            a, b, c, d = contingency(train_lines, sign, predicate)
            if a + b < minimum_train_sign_lines or a + c < 20:
                continue
            p_value = fisher_exact_two_sided(a, b, c, d)
            raw_candidates.append(
                {
                    "m_sign": sign,
                    "target": target_name,
                    "train_cells": (a, b, c, d),
                    "train_odds_ratio": odds_ratio(a, b, c, d),
                    "train_p": p_value,
                }
            )

    train_q_values = bh_adjust([float(item["train_p"]) for item in raw_candidates])
    selected: list[dict[str, object]] = []
    for item, q_value in zip(raw_candidates, train_q_values):
        item["train_q"] = q_value
        train_or = float(item["train_odds_ratio"])
        if q_value <= 0.01 and (train_or >= 3.0 or train_or <= 1.0 / 3.0):
            selected.append(item)

    validation_p_values: list[float] = []
    validation_rows: list[tuple[int, int, int, int]] = []
    target_lookup = dict(targets)
    for item in selected:
        cells = contingency(
            validation_lines,
            str(item["m_sign"]),
            target_lookup[str(item["target"])],
        )
        validation_rows.append(cells)
        direction = "enriched" if float(item["train_odds_ratio"]) > 1 else "depleted"
        validation_p_values.append(
            blocked_randomization_p(
                validation_lines,
                str(item["m_sign"]),
                target_lookup[str(item["target"])],
                direction,
            )
        )

    validation_q_values = bh_adjust(validation_p_values)
    confirmed: list[Association] = []
    for item, cells, p_value, q_value in zip(
        selected, validation_rows, validation_p_values, validation_q_values
    ):
        validation_or = odds_ratio(*cells)
        train_or = float(item["train_odds_ratio"])
        same_direction = (train_or > 1 and validation_or > 1) or (
            train_or < 1 and validation_or < 1
        )
        validation_sign_lines = cells[0] + cells[1]
        if (
            validation_sign_lines >= minimum_validation_sign_lines
            and same_direction
            and q_value <= 0.05
            and (validation_or >= 1.5 or validation_or <= 1.0 / 1.5)
        ):
            train_cells = item["train_cells"]
            assert isinstance(train_cells, tuple)
            confirmed.append(
                Association(
                    analysis=analysis,
                    m_sign=str(item["m_sign"]),
                    target=str(item["target"]),
                    train_a=train_cells[0],
                    train_b=train_cells[1],
                    train_c=train_cells[2],
                    train_d=train_cells[3],
                    train_odds_ratio=train_or,
                    train_p=float(item["train_p"]),
                    train_q=float(item["train_q"]),
                    validation_a=cells[0],
                    validation_b=cells[1],
                    validation_c=cells[2],
                    validation_d=cells[3],
                    validation_odds_ratio=validation_or,
                    validation_p=p_value,
                    validation_q=q_value,
                )
            )

    return sorted(
        confirmed,
        key=lambda row: (row.analysis, row.validation_q, -abs(math.log(row.validation_odds_ratio))),
    )


def analyze(corpus_dir: Path) -> dict[str, object]:
    files = sorted(corpus_dir.glob("*.values.atf"))
    if not files:
        raise ValueError(f"no *.values.atf files found in {corpus_dir}")
    parsed_files = [(path, parse_tablet(path)) for path in files]
    empty_files = [path.name for path, path_lines in parsed_files if not path_lines]
    lines = [line for _, path_lines in parsed_files for line in path_lines]
    tablets = sorted({line.tablet for line in lines})
    train_tablets = {tablet for tablet in tablets if split_name(tablet) == "train"}
    validation_tablets = set(tablets) - train_tablets

    intact_m_lines = [line for line in lines if line.m_signs and not line.damaged]
    header_lines = [
        line
        for line in intact_m_lines
        if line.surface == "obverse" and line.ordinal_on_surface >= 1
    ]
    mixed_lines = [
        line for line in intact_m_lines if line.n_signs
    ]

    train_headers = [line for line in header_lines if line.tablet in train_tablets]
    validation_headers = [line for line in header_lines if line.tablet in validation_tablets]
    header_target = [("first_obverse_line", lambda line: line.ordinal_on_surface == 1)]
    header_results = discover_and_validate(
        "header_position",
        train_headers,
        validation_headers,
        header_target,
        minimum_train_sign_lines=15,
        minimum_validation_sign_lines=5,
    )

    train_mixed = [line for line in mixed_lines if line.tablet in train_tablets]
    validation_mixed = [line for line in mixed_lines if line.tablet in validation_tablets]
    n_signs = sorted({sign for line in train_mixed for sign in line.n_signs})
    numeral_targets = [
        (n_sign, lambda line, target=n_sign: target in line.n_signs) for n_sign in n_signs
    ]
    numeral_results = discover_and_validate(
        "numeral_association",
        train_mixed,
        validation_mixed,
        numeral_targets,
        minimum_train_sign_lines=20,
        minimum_validation_sign_lines=5,
    )

    return {
        "schema_version": 1,
        "method": {
            "split": "sha256(tablet_id) modulo 5; bucket 0 validation, others train",
            "unit": "line presence/absence; tablets never cross splits",
            "sign_normalization": "M-signs reduced to three-digit family; N-sign zero-padding normalized, variants retained",
            "damage_filter": "lines containing ... or standalone x excluded",
            "selection": "training BH q <= 0.01 and corrected OR >= 3 or <= 1/3",
            "confirmation": "within-tablet exact randomization, validation BH q <= 0.05, same direction, corrected OR >= 1.5 or <= 2/3",
            "interpretive_limit": "association and positional specialization only; no lexical meaning assigned",
        },
        "corpus": {
            "file_count": len(files),
            "files_without_numbered_lines": empty_files,
            "sha256": corpus_digest(files),
            "tablet_count": len(tablets),
            "line_count": len(lines),
            "intact_m_line_count": len(intact_m_lines),
            "intact_m_n_line_count": len(mixed_lines),
            "train_tablet_count": len(train_tablets),
            "validation_tablet_count": len(validation_tablets),
            "train_m_n_line_count": len(train_mixed),
            "validation_m_n_line_count": len(validation_mixed),
        },
        "associations": [asdict(row) for row in header_results + numeral_results],
    }


def write_csv(path: Path, associations: Sequence[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not associations:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(associations[0]))
        writer.writeheader()
        writer.writerows(associations)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus_dir", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--csv", type=Path, required=True)
    args = parser.parse_args()

    result = analyze(args.corpus_dir)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    write_csv(args.csv, result["associations"])
    print(json.dumps(result["corpus"], indent=2))
    print(f"confirmed associations: {len(result['associations'])}")


if __name__ == "__main__":
    main()
