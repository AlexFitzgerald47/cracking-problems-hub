# Authorship corpora need provenance gates

## Trigger

First cracker pass on `discovered/junius-letters-authorship/`, 2026-09-05.

A stylometric corpus can be methodologically invalid before any model is run. The Junius pass exposed four concrete failure modes while checking primary texts.

## Failure modes observed

1. **Target leakage through bibliography aggregation.** A Philip Francis author listing includes a collection of the disputed *Junius* letters. Scraping everything listed under a candidate author can therefore put the target text into the candidate's own training corpus and make an attribution circular.

2. **Mixed speakers inside apparently authored books.** Francis's acknowledged 1784 *Two Speeches* embeds parliamentary orders, bill language, Company correspondence and minutes. Collected *Junius* editions likewise include replies by opponents, quotations, editorial matter and indexes. A book-level author label is too coarse.

3. **Contamination can hit the exact stylistic variable being tested.** In the Francis volume, an inspected `further` occurrence is in the quoted parliamentary order while Francis's surrounding authored prose uses `farther`. An inspected `further` occurrence in the Junius collection is likewise external quoted material. Raw synonym counts can therefore assign another writer's lexical choice to the candidate.

4. **Chronology moves features.** Francis's acknowledged 1784 prose showed the classic `among` without `amongst` preference also seen in Junius; an acknowledged 1816 Francis letter uses `amongst`. Lifetime pooling can blur the period-specific signal.

## Minimum provenance schema before authorship modelling

For every training/test segment, record at least:

- `text_id`
- claimed author
- `attribution_status`: `gold` / `disputed`
- date
- genre/register
- speaker/source within the volume
- quotation/document flag
- edition/source
- OCR/transcription method and known quality

## Gate

- Train only on independently attributed, authorial (`gold`) segments.
- Hold disputed-attribution works out as secondary tests, never training data.
- Exclude or separately tag quotations, replies and embedded documents.
- Split validation by document, not random chunks from the same book.
- Match period and genre before interpreting an authorship effect.
- Before scoring the unknown text, verify that the pipeline correctly separates known authors under the same controls.

This lesson should transfer to any historical authorship problem in the Hub. A sophisticated classifier cannot rescue contaminated labels.
