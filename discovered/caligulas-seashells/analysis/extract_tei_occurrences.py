#!/usr/bin/env python3
"""Extract citable lemma occurrences from a pinned Perseus TEI corpus.

The extractor deliberately does not lemmatize.  Each search pattern is an explicit
set of surface endings, which makes false positives and omissions auditable.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


PINNED_CORPUS_COMMIT = "2481af34dea79eab4e595f06719d292c6660b716"
TEI_NAMESPACE = "http://www.tei-c.org/ns/1.0"
XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
PASSAGE_TAGS = {"ab", "item", "l", "p", "s"}

# The target pattern covers the noun's ordinary first/second-declension forms and
# the common -que/-ve enclitics.  It intentionally excludes muscular/is adjectives.
LEMMA_PATTERNS = {
    "musculus": re.compile(
        r"(?<![A-Za-z])muscul(?:us|i|o|um|orum|is|os|a|ae|am|arum|as)"
        r"(?:que|ve|ue)?(?![A-Za-z])",
        re.IGNORECASE,
    ),
    "aries": re.compile(
        r"(?<![A-Za-z])ariet(?:is|i|em|e|es|um|ibus)(?:que|ve|ue)?(?![A-Za-z])"
        r"|(?<![A-Za-z])aries(?:que|ve|ue)?(?![A-Za-z])",
        re.IGNORECASE,
    ),
    "scorpio": re.compile(
        r"(?<![A-Za-z])scorpi(?:o|onis|oni|onem|one|ones|onum|onibus)"
        r"(?:que|ve|ue)?(?![A-Za-z])",
        re.IGNORECASE,
    ),
    "testudo": re.compile(
        r"(?<![A-Za-z])testudin(?:is|i|em|e|es|um|ibus)(?:que|ve|ue)?(?![A-Za-z])"
        r"|(?<![A-Za-z])testudo(?:que|ve|ue)?(?![A-Za-z])",
        re.IGNORECASE,
    ),
    "vinea": re.compile(
        r"(?<![A-Za-z])vine(?:a|ae|am|arum|as|is)(?:que|ve|ue)?(?![A-Za-z])",
        re.IGNORECASE,
    ),
}


@dataclass(frozen=True)
class Occurrence:
    lemma: str
    work_id: str
    source_file: str
    source_sha256: str
    author: str
    title: str
    citation: str
    surface_forms: str
    token_count: int
    context: str


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def normalized_text(element: ET.Element) -> str:
    return " ".join("".join(element.itertext()).split())


def first_text(root: ET.Element, xpath: str) -> str:
    element = root.find(xpath, {"tei": TEI_NAMESPACE})
    return normalized_text(element) if element is not None else ""


def is_latin_edition(path: Path) -> bool:
    name = path.name.lower()
    return name.endswith(".xml") and (
        ".perseus-lat" in name or ".opp-lat" in name
    )


def passage_elements(body: ET.Element) -> list[ET.Element]:
    candidates = [
        element for element in body.iter() if local_name(element.tag) in PASSAGE_TAGS
    ]
    candidate_ids = {id(element) for element in candidates}
    leaves: list[ET.Element] = []
    for element in candidates:
        if any(
            id(descendant) in candidate_ids
            for descendant in element.iter()
            if descendant is not element
        ):
            continue
        leaves.append(element)
    return leaves


def citation_for(element: ET.Element, parent_map: dict[ET.Element, ET.Element]) -> str:
    ancestors: list[ET.Element] = []
    current = element
    while current in parent_map:
        current = parent_map[current]
        ancestors.append(current)
    ancestors.reverse()

    parts: list[str] = []
    for ancestor in ancestors:
        if local_name(ancestor.tag) != "div":
            continue
        number = ancestor.get("n")
        if not number:
            continue
        label = ancestor.get("subtype") or ancestor.get("type") or "part"
        parts.append(f"{label}={number}")

    own_number = element.get("n")
    if own_number:
        parts.append(f"{local_name(element.tag)}={own_number}")
    xml_id = element.get(f"{{{XML_NAMESPACE}}}id")
    if xml_id and not parts:
        parts.append(f"xml:id={xml_id}")
    return "/".join(parts) or "uncited"


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_tei(path: Path) -> ET.ElementTree:
    """Parse repository TEI, tolerating its legacy HTML named entities.

    A small number of canonical-latinLit files contain entities such as
    ``&dagger;`` without declaring them in an XML DTD.  They are valid source
    data but rejected by the stdlib parser.  Resolve only named HTML entities
    and remove XML-forbidden control characters; leave structural markup alone.
    """

    source = path.read_text(encoding="utf-8-sig", errors="replace")

    def replace_entity(match: re.Match[str]) -> str:
        entity = match.group(0)
        decoded = html.unescape(entity)
        return decoded if decoded != entity else entity

    source = re.sub(r"&[A-Za-z][A-Za-z0-9]+;", replace_entity, source)
    source = "".join(
        character
        for character in source
        if character in "\t\n\r" or ord(character) >= 0x20
    )
    return ET.ElementTree(ET.fromstring(source))


def extract_file(path: Path, corpus_root: Path, lemmas: Iterable[str]) -> list[Occurrence]:
    try:
        tree = parse_tei(path)
    except ET.ParseError as error:
        print(f"warning: cannot parse {path}: {error}", file=sys.stderr)
        return []

    root = tree.getroot()
    body = root.find(".//tei:body", {"tei": TEI_NAMESPACE})
    if body is None:
        return []

    author = first_text(root, ".//tei:teiHeader//tei:titleStmt/tei:author")
    title = first_text(root, ".//tei:teiHeader//tei:titleStmt/tei:title")
    relative_path = path.relative_to(corpus_root).as_posix()
    work_id = "/".join(path.relative_to(corpus_root / "data").parts[:2])
    sha256 = file_digest(path)
    parent_map = {child: parent for parent in root.iter() for child in parent}

    occurrences: list[Occurrence] = []
    for element in passage_elements(body):
        context = normalized_text(element)
        if not context:
            continue
        for lemma in lemmas:
            matches = list(LEMMA_PATTERNS[lemma].finditer(context))
            if not matches:
                continue
            occurrences.append(
                Occurrence(
                    lemma=lemma,
                    work_id=work_id,
                    source_file=relative_path,
                    source_sha256=sha256,
                    author=author,
                    title=title,
                    citation=citation_for(element, parent_map),
                    surface_forms="|".join(match.group(0) for match in matches),
                    token_count=len(matches),
                    context=context,
                )
            )
    return occurrences


def corpus_commit(corpus_root: Path) -> str:
    head = corpus_root / ".git" / "HEAD"
    if not head.exists():
        return "unknown"
    import subprocess

    result = subprocess.run(
        ["git", "-C", str(corpus_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def write_csv(path: Path, rows: list[Occurrence]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(asdict(rows[0]).keys()) if rows else list(Occurrence.__annotations__)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus_root", type=Path)
    parser.add_argument("--lemma", action="append", choices=sorted(LEMMA_PATTERNS))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path)
    arguments = parser.parse_args()

    corpus_root = arguments.corpus_root.resolve()
    data_root = corpus_root / "data"
    if not data_root.is_dir():
        parser.error(f"not a canonical-latinLit checkout: {corpus_root}")

    observed_commit = corpus_commit(corpus_root)
    if observed_commit != PINNED_CORPUS_COMMIT:
        parser.error(
            f"expected corpus commit {PINNED_CORPUS_COMMIT}, got {observed_commit}"
        )

    lemmas = arguments.lemma or ["musculus"]
    source_files = sorted(path for path in data_root.rglob("*.xml") if is_latin_edition(path))
    rows: list[Occurrence] = []
    for path in source_files:
        rows.extend(extract_file(path, corpus_root, lemmas))
    rows.sort(key=lambda row: (row.lemma, row.work_id, row.source_file, row.citation))
    write_csv(arguments.output, rows)

    metadata = {
        "corpus_repository": "https://github.com/PerseusDL/canonical-latinLit",
        "corpus_commit": observed_commit,
        "latin_edition_files_scanned": len(source_files),
        "lemmas": lemmas,
        "passage_rows": len(rows),
        "token_matches": sum(row.token_count for row in rows),
        "matching_source_files": len({row.source_file for row in rows}),
    }
    if arguments.metadata:
        arguments.metadata.parent.mkdir(parents=True, exist_ok=True)
        arguments.metadata.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(metadata, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
