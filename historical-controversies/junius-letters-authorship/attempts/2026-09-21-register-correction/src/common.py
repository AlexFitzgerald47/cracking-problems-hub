#!/usr/bin/env python3
"""Shared loading/feature layer for the 2026-09-21 register-correction session.

Everything here is deliberately IDENTICAL to the 2026-09-17 session's
`prediction_test.py` feature construction, so that any difference in results is
attributable to the correction under test and not to a changed pipeline. The
2026-09-17 numbers reproduce byte-identically under this loader (see RESULTS.md
section "Reproduction").

The one thing added is a per-source year, needed for the detrending arm. The panel
manifest records a `period` RANGE per source ("1758-1814"), not a date per document,
so the year variable available here is SOURCE-LEVEL. That is a material weakness of
the detrending arm on this corpus and is treated as such throughout.
"""
import json, os, sys
from collections import Counter, defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PRIOR_SRC = os.path.abspath(os.path.join(HERE, "..", "..",
                                         "2026-09-17-genre-matched-openset", "src"))
sys.path.insert(0, PRIOR_SRC)
import corpus as C                      # noqa: E402
from funcwords import FUNCTION_WORDS    # noqa: E402
from delta import junius_chunks         # noqa: E402

RES = os.path.join(HERE, "..", "results")
N_FEATURES = 120

FORMAL = ("published_prose", "political_prose")
LETTERS = ("private_letter",)
NOT_CANDIDATES = ("Junius", "Philo_Junius", "William_Draper", "John_Horne")


def period_mid(period):
    """Midpoint year of a source's period range. Source-level, not document-level."""
    parts = str(period).split("-")
    try:
        a = int(parts[0])
        b = int(parts[1]) if len(parts) > 1 else a
    except ValueError:
        return None
    return (a + b) / 2.0


def load():
    """Return (docs, Z, feats). Z is the global z-scored function-word profile matrix."""
    docs = list(C.load_jsonl("panel_chunks.jsonl")) + junius_chunks()
    fw = set(FUNCTION_WORDS)
    tot, per = Counter(), []
    for d in docs:
        c = Counter(t for t in C.tokens(d["text"]) if t in fw)
        per.append(c)
        tot.update(c)
    feats = [w for w, _ in tot.most_common(N_FEATURES)]
    X = np.zeros((len(docs), len(feats)))
    for i, c in enumerate(per):
        s = sum(c.values()) or 1
        for j, w in enumerate(feats):
            X[i, j] = c[w] / s
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1e-12
    Z = (X - mu) / sd
    # The Junius/Draper/Horne chunks carry no `period` (they are built by the prior
    # session's junius_chunks()). The 1772 Woodfall collection covers 21 Jan 1769 to
    # 21 Jan 1772, so 1770.5 is the correct midpoint on the same convention used for
    # every other source.
    for i, d in enumerate(docs):
        d["_i"] = i
        d["year"] = period_mid(d["period"]) if "period" in d else 1770.5
    return docs, Z, feats


def index(docs, genres, exclude_authors=NOT_CANDIDATES, min_docs=8):
    """Author -> row indices, for docs in `genres`, keeping authors with >= min_docs."""
    by = defaultdict(list)
    for d in docs:
        if d["genre"] in genres and d["author"] not in exclude_authors:
            by[d["author"]].append(d["_i"])
    return {a: v for a, v in by.items() if len(v) >= min_docs}


def dump(name, obj):
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, name), "w") as f:
        json.dump(obj, f, indent=1, default=float)
