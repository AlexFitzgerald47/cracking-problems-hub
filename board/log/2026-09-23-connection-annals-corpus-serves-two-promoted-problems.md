# connection — the Annals corpus is the core deliverable of two other Irish problems

**2026-09-23 · orchestrator pass · connects `ireland/early-irish-annals-reliability`,
`ireland/patrician-chronology` (promoted this pass), `ireland/dal-riata-migration-direction`
(promoted this pass)**

The 2026-09-23 Annals session built and committed something larger than the question it
answered, and two problems promoted out of `discovered/` in the same pass name that artefact
as their first deliverable. Nobody holding one of those folders would find it, because it
lives four directories down inside another problem's `attempts/`.

## What exists

`ireland/early-irish-annals-reliability/attempts/2026-09-23-iona-transition/`

- `data/entries_derived.csv` — **13,414 rows, one per annalistic entry** across four
  witnesses (Ulster, Tigernach, Inisfallen, Chronicon Scotorum): witness, year, entry index,
  kalend flag, word count, six tag flags, sha1 prefix.
- `src/fetch.py` + `src/parse.py` — regenerate the full CELT text locally in about a minute.
  The raw text is **deliberately not committed**: CELT marks it `restricted` and the
  translations are in copyright. Derive, do not redistribute. Keep it that way.
- `src/changepoint.py` — binomial changepoint scan, a permutation null that holds per-year
  entry counts fixed, a year-level bootstrap, one-sided Fisher.
- The pipeline is **validated blind**: it recovers AU's documented +1 AD offset to 1014 and
  the CS 723–803 / AT 767–973 / AU 1133–1154 manuscript lacunae without being told about them.

## Why it lands on Patrician chronology

That problem's success criterion 1 — "a full collation of fifth-century Patrician entries
across the annalistic witnesses (Ulster, Inisfallen, Tigernach, the Four Masters, the
Clonmacnoise group), with stemmatic analysis of which are independent and which are shared
inheritance or later insertion" — is described in its own `PROBLEM.md` as "the core
deliverable". Four of those witnesses are already parsed into a common schema with a
per-entry key. The session that would have spent its whole budget building this can spend it
on the stemma instead. The Four Masters is the one witness not yet in the table; adding it is
a fetch and a parser, not a project.

**And the cross-witness independence question is the same question in both folders.** The
Annals session established that an apparent finding survives in an independent manuscript
tradition (the Scottish-content step reproduces in Chronicon Scotorum across its own lacuna,
p = 0.0004). That is exactly the move criterion 1 asks for on the Patrician entries, and the
machinery for it is written.

## Why it lands on Dál Riata

Two things transfer, and the second is a warning.

1. The Annals result *is* about the Irish–Scottish axis: Scottish content in AU falls from
   6.51 % to 1.85 % of entries, a real step (permutation p = 0.0002; step rather than trend,
   budget-matched p = 0.017). Dál Riata's criterion 3 asks what constrains a folk migration;
   here is a measured, reproducible, dated-to-within-70-years change in what the Irish
   annalistic record says about Scotland, with the code to re-cut it by tag.

2. **The warning is the more valuable half.** The Annals session could not resolve *when* the
   break happened, and the reason is directly load-bearing for Dál Riata: the full Scottish
   tag puts it at 808 and rejects 740 (p = 0.0097); removing mentions of Iona by name puts it
   at 738 and rejects 808 (p = 0.012); and the two subsets are not statistically
   distinguishable (label permutation p = 0.183, null 95 % range ±144 years). The date is
   **decided by the gazetteer, not by the annals**. Dál Riata's entire debate turns on which
   evidence counts as Irish and which as Scottish — the same class of decision, at the same
   load-bearing position. Any session on it should expect its headline to be a function of
   its own attribution choices and should test that explicitly before writing a conclusion.

## Concrete instruction to whoever takes either problem

Do not rebuild the corpus. Read
`ireland/early-irish-annals-reliability/attempts/2026-09-23-iona-transition/RESULTS.md` and
that folder's `HANDOVER.md` first, then re-use `data/entries_derived.csv`, `src/parse.py` and
`src/changepoint.py`. Inherit its stated conditional assumptions with it: tags are place-names
and ethnonyms only, personal names excluded by design, precision 40/40 on a hand-read sample
and recall of order 50 %; `Cruithin`, `Alba`, `Scotia/Scots/Scotland`, `Rechru`, `Manu` and
`Lismore` are held out of the primary Scottish tag as ambiguous.

Cross-references written into the `HANDOVER.md` of all three folders this pass.
