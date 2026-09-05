#!/usr/bin/env python3
"""Reproduce the raw lexical audit used in the 2026-09-05 Junius attempt.

This is deliberately a *source audit*, not an attribution classifier. It downloads the
public-domain Internet Archive OCR, normalizes whitespace/hyphenated line breaks, counts
predeclared Ellegard-style alternatives, and prints contexts so a human can determine
whether a hit is authorial prose or embedded quotation.

Do not treat raw counts as authorial frequencies until the quoted/reply/editorial segments
have been removed.
"""

from __future__ import annotations

import re
import urllib.request
from collections import Counter

SOURCES = {
    "junius_1786": "https://archive.org/stream/lettersofjuniusc00juniiala/lettersofjuniusc00juniiala_djvu.txt",
    "francis_1784": "https://archive.org/stream/twospeechesinhou00franiala/twospeechesinhou00franiala_djvu.txt",
    "francis_1816": "https://archive.org/stream/lettermissivefro00fran/lettermissivefro00fran_djvu.txt",
}

FEATURE_SETS = {
    "among": ("among", "amongst"),
    "farther": ("farther", "further"),
    "until": ("until", "till"),
    "completeness": ("completely", "entirely", "totally", "wholly"),
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "cracking-problems-hub/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def normalize(text: str) -> str:
    # Repair only line-break hyphenation and whitespace. Do NOT silently modernize long-s
    # OCR (f/s), spelling, or punctuation; those operations can alter stylometric features.
    text = re.sub(r"([A-Za-z])-\s*\n\s*([A-Za-z])", r"\1\2", text)
    return re.sub(r"\s+", " ", text).strip()


def token_counts(text: str, words: tuple[str, ...]) -> Counter:
    lower = text.lower()
    return Counter({w: len(re.findall(rf"(?<![a-z]){re.escape(w)}(?![a-z])", lower)) for w in words})


def contexts(text: str, word: str, radius: int = 90, limit: int = 8) -> list[str]:
    lower = text.lower()
    out = []
    for m in re.finditer(rf"(?<![a-z]){re.escape(word.lower())}(?![a-z])", lower):
        start = max(0, m.start() - radius)
        end = min(len(text), m.end() + radius)
        out.append(text[start:end])
        if len(out) >= limit:
            break
    return out


def main() -> None:
    for source_id, url in SOURCES.items():
        text = normalize(fetch(url))
        print(f"\n## {source_id}\nchars={len(text):,}")
        for label, words in FEATURE_SETS.items():
            counts = token_counts(text, words)
            print(label, dict(counts))
        print("\nContexts for contamination-sensitive alternatives:")
        for word in ("amongst", "farther", "further", "until", "till"):
            hits = contexts(text, word)
            if hits:
                print(f"\n[{word}] raw_hits_shown={len(hits)}")
                for hit in hits:
                    print(" -", hit)


if __name__ == "__main__":
    main()
