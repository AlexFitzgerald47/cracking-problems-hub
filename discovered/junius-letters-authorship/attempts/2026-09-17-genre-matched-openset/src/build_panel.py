#!/usr/bin/env python3
"""Assemble the analysis panel: every author reduced to equal-length word chunks by
one shared pipeline.

Genre is recorded per volume and is not a cosmetic label. Junius's public letters are
polemical newspaper prose; Philip Francis's best-attested acknowledged prose is
private family correspondence. Comparing them directly measures genre at least as
much as authorship, so the panel carries both a public-prose stratum and a
private-letter stratum, and every reported result says which stratum it came from.

Every volume here was downloaded and its byte size checked in this session; the
manifest written alongside records identifier, byte size and measured long-s OCR
damage rate, so a later session can tell which corpora are actually comparable.
"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "data", "raw")
OUT = os.path.join(HERE, "..", "data", "corpus")

CHUNK = 2000

# author, genre, period-of-composition, archive.org identifier
VOLUMES = [
    # --- private / familiar letters -------------------------------------------
    ("Philip_Francis",      "private_letter", "1758-1814", "francisletters01franuoft"),
    ("Philip_Francis",      "private_letter", "1774-1818", "francisletters02franuoft"),
    ("Lord_Chesterfield",   "private_letter", "1737-1768", "letterstohisson01chesiala"),
    ("Horace_Walpole",      "private_letter", "1741-1785", "lettersofhoracew03walp"),
    ("Thomas_Gray",         "private_letter", "1734-1771", "lettersofthomasg00gray"),
    ("James_Boswell",       "private_letter", "1758-1795", "lettersofjamesbo00boswuoft"),
    ("Laurence_Sterne",     "private_letter", "1739-1768", "letterslaterevm00stergoog"),
    ("Edward_Gibbon",       "private_letter", "1753-1794", "privatelettersof02gibb"),
    ("David_Hume",          "private_letter", "1751-1776", "lettersdavidhum00humegoog"),
    ("Samuel_Johnson",      "private_letter", "1731-1784", "letterssamueljo00johngoog"),
    ("William_Cowper",      "private_letter", "1765-1800", "letterswilliamc00cowpgoog"),
    ("Edmund_Burke",        "private_letter", "1744-1797", "correspondencer01burkgoog"),
    # --- polemical / political prose ------------------------------------------
    ("John_Wilkes",         "political_prose", "1762-1769", "bim_eighteenth-century_english-liberty-being-a_wilkes-john_1769_1"),
    ("Richard_Price",       "political_prose", "1776",      "observationsonna00pric"),
    ("Thomas_Pownall",      "political_prose", "1774",      "administrationb01wargoog"),
    ("Hugh_Boyd",           "political_prose", "1770-1794", "miscellaneouswor01boydiala"),
    ("Philip_Francis",      "political_prose", "1784",      "twospeechesinhou00franiala"),
    # --- published formal prose by authors whose PRIVATE letters are also in the
    #     panel. These are the genre controls: same author, two registers, so the
    #     genre shift in each variable can be measured instead of assumed. Gutenberg
    #     e-texts, hand-proofread, so they also act as a clean-text reference class.
    ("Edmund_Burke",        "published_prose", "1770",      "gutenberg_2173"),
    ("Edmund_Burke",        "published_prose", "1756-1790", "gutenberg_15043"),
    ("Edmund_Burke",        "published_prose", "1756-1790", "gutenberg_15198"),
    ("Samuel_Johnson",      "published_prose", "1750-1760", "gutenberg_43656"),
    ("Samuel_Johnson",      "published_prose", "1750-1760", "gutenberg_11397"),
    ("David_Hume",          "published_prose", "1741-1777", "gutenberg_36120"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    docs, manifest = [], []
    for author, genre, period, ident in VOLUMES:
        path = os.path.join(RAW, ident + ".txt")
        if not os.path.exists(path):
            print(f"MISSING {ident}", file=sys.stderr)
            continue
        raw = open(path, errors="replace").read()
        cleaned = C.clean_volume(raw)
        rate = C.long_s_rate(cleaned)
        chunks = C.chunk(cleaned, CHUNK)
        for i, ch in enumerate(chunks):
            docs.append(dict(author=author, genre=genre, period=period,
                             source=ident, chunk=i, n_words=CHUNK, text=ch))
        manifest.append(dict(author=author, genre=genre, period=period, identifier=ident,
                             raw_bytes=os.path.getsize(path),
                             cleaned_words=len(cleaned.split()),
                             n_chunks=len(chunks), long_s_rate=round(rate, 5)))
        print(f"{author:20s} {genre:16s} {ident[:46]:46s} {len(chunks):4d} chunks  long-s {rate:.5f}")

    with open(os.path.join(OUT, "panel_chunks.jsonl"), "w") as f:
        for d in docs:
            f.write(json.dumps(d) + "\n")
    with open(os.path.join(OUT, "panel_manifest.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        wr.writeheader()
        wr.writerows(manifest)
    print(f"\n{len(docs)} chunks of {CHUNK} words from {len(manifest)} volumes")


if __name__ == "__main__":
    main()
