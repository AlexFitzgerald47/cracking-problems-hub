#!/usr/bin/env python3
"""Split a live CDLI bulk ATF export into per-tablet files, SFU layout.

Route (verified 2026-10-01, HTTP 200, text/x-c-atf):
  https://cdli.earth/search?period=Proto-Elamite&format=atf&aspect=inscriptions&limit=3000

The pinned SFU corpus is `pe-sign-value-data` at commit 538949cc (August 2022),
1,467 files named `P######.values.atf`. The live CDLI export is raw ATF without
the SFU `value<family<exactform` annotations. The 2026-09-04 parser reads
`M[0-9]{3}` and parenthesised N-signs, neither of which depends on the
annotation, so the same parser applies -- but that has to be CHECKED on the
overlapping tablets, not assumed, which `cdli_replicate.py` does first.

Output files are named `P######.values.atf` purely so the existing loader's glob
finds them. They contain raw CDLI ATF, not SFU value data.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

HEADER_RE = re.compile(r"^&(P[0-9]{6})\b")


def split_export(export: Path, out_dir: Path) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    current: list[str] = []
    name: str | None = None
    written: list[str] = []

    def flush():
        if name and current:
            (out_dir / f"{name}.values.atf").write_text(
                "".join(current), encoding="utf-8"
            )
            written.append(name)

    for raw in export.read_text(encoding="utf-8").splitlines(keepends=True):
        m = HEADER_RE.match(raw)
        if m:
            flush()
            name = m.group(1)
            current = [raw]
        elif name:
            current.append(raw)
    flush()
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export", type=Path)
    ap.add_argument("out_dir", type=Path)
    args = ap.parse_args()
    written = split_export(args.export, args.out_dir)
    print(f"wrote {len(written)} tablets to {args.out_dir}")
    print(f"first {written[:3]}  last {written[-3:]}")
    dupes = len(written) - len(set(written))
    print(f"duplicate P-numbers in export: {dupes}")


if __name__ == "__main__":
    main()
