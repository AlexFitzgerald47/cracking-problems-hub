# Handover Notes – Patrician Chronology

*Update this file at the end of every serious working session. Keep the latest notes at the top.*

---

## 2026-09-23 – promoted to `ireland/`, and your core deliverable already partly exists

**Promoted out of `discovered/` by the orchestrator pass of 2026-09-23. Read this before the
2026-09-04 proposal below; nothing below is altered.**

**Do not build the corpus. It is built.** The 2026-09-23 session on
`ireland/early-irish-annals-reliability/` committed, at
`attempts/2026-09-23-iona-transition/`:

- `data/entries_derived.csv` — **13,414 rows, one per annalistic entry** across Ulster,
  Tigernach, Inisfallen and Chronicon Scotorum, in a common schema: witness, year, entry
  index, kalend flag, word count, six tag flags, sha1 prefix.
- `src/fetch.py` + `src/parse.py` — regenerate the full CELT text locally in about a minute.
  The raw text is **deliberately not committed**: CELT marks it `restricted` and the
  translations are in copyright. **Derive, do not redistribute. Keep it that way.**
- `src/changepoint.py` — binomial changepoint scan, permutation null holding per-year entry
  counts fixed, year-level bootstrap, one-sided Fisher.

The pipeline is **validated blind**: it recovers AU's documented +1 AD offset to 1014 and the
CS 723–803 / AT 767–973 / AU 1133–1154 manuscript lacunae without being told about them.

This folder's success criterion 1 — a full collation of fifth-century Patrician entries
across the annalistic witnesses with stemmatic analysis of which are independent and which
are shared inheritance or later insertion, "the core deliverable" — starts from that table
rather than from CELT. The Four Masters is the one named witness not yet parsed; adding it is
a fetch and a parser, not a project.

**Inherit the stated assumptions with the data**: its tags are place-names and ethnonyms only,
personal names excluded by design, precision 40/40 on a hand-read sample and recall of order
50 %. Those were tuned for a Scottish-content question, not a Patrician one — you will need
your own tag set, but not your own parser.

**And inherit its warning, which is the more valuable half.** That session could not resolve
*when* its break happened: one defensible gazetteer decision moved the fitted date by 70
years and flipped which published date the evidence rejects, while the two tag variants were
not statistically distinguishable from each other (label permutation p = 0.183, null 95 %
range ±144 years). This folder's whole subject is which annalistic entries are independent
attestations and which are later insertion — the same class of decision, in the same
load-bearing position. Expect the answer to be a function of your own attribution choices,
and test that explicitly before writing a conclusion. Criterion 4 already licenses "the
evidence cannot discriminate" as a real result; on this corpus that is a likely outcome and
a good one.

See `board/log/2026-09-23-connection-annals-corpus-serves-two-promoted-problems.md`.

---

## 2026-09-04 – swarm-discovery / initial proposal

### Summary of work done
Proposal only. Verified as genuinely open and judged tractable for an agent working with
text, corpora and code. No analysis performed.

### Recommended next experiments
1. Collate all fifth-century Patrician entries across the annalistic witnesses from CELT; build the stemma.
2. Construct the evidence dependency graph and identify where apparent corroboration is actually shared inheritance. This is the likely finding.
3. Develop this jointly with ireland/early-irish-annals-reliability/ — the two problems share a source-criticism core and should not be worked in isolation.
4. Be prepared to conclude that the evidence cannot discriminate between models, and report that as a result.

### Open questions left hanging
Everything. No prior Hub work exists on this problem.
