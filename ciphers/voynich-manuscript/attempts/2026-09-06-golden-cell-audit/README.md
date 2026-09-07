# Attempt: audit the Voynich "golden cell" before testing axis parallelism

**Date:** 2026-09-06  
**Status:** complete; material correction to the 2026-09-04 interpretation  
**Crack mode:** advancing

## Why this audit came first

The previous session's highest-value next experiment was to compare the direction of the Currier A→B shift with section shifts such as Herbal→Biological. Before using that A→B axis, this session re-audited the claimed clean contrast on which it rested:

`A / Hand 3 / Stars  vs  B / Hand 3 / Stars`

The prior code labelled this **"LANGUAGE (hand and section held)"** and reported distance 12.76 versus a permutation-null mean 5.53 (`p < 0.0002`). That numerical calculation is reproducible from the existing result file. The interpretation is not.

## Material correction

### 1. `$I=S` is not a manuscript-section identifier

The IVTFF format defines:

- `$Q` = physical quire;
- `$I` = **illustration type**;
- `$L` = Currier language;
- `$H` = writing hand according to **Lisa Fagin Davis**;
- `$C` = Currier's hand classification.

For `$I`, value `S` means **"marginal stars only"**. It does not mean a single physical or textual "Stars section".

Primary format reference: René Zandbergen, *IVTFF – Intermediate Voynich Transliteration File Format*, v2.0/2.0.1, table of page variables: https://www.voynich.nu/software/ivtt/IVTFF_format.pdf

The inherited parser therefore grouped pages by a coarse illustration-type code and then described that grouping as "section held". Those are different variables.

### 2. The A side is f58r/v in Quire 8; the B side is later star/recipe material

The only two Currier-A pages assigned to LFD Hand 3 are **f58r and f58v**. They are the two sides of one folio in **Quire 8**, both text-only with a few marginal stars.

Source: René Zandbergen, Quire 8 page catalogue: https://www.voynich.nu/q08/index.html

The same catalogue records the other Hand-3 material in Quire 8 (f65r/v) as Currier language unclassified, not B. The Currier-B Hand-3 pages used by the inherited `$I=S` cell belong to later material, especially the **Quire 20 recipes section**, whose pages are text-only with marginal stars and are Currier B / LFD Hand 3.

Source: René Zandbergen, Quire 20 page catalogue: https://www.voynich.nu/q20/index.html

A separate modern statistical taxonomy already treats these as different text groups rather than one section:

- `R` = text on f58r/v (742 words);
- `S` and `T` = two sets of bifolios in the Quire 20 recipes section (5,270 and 5,536 words).

Source: René Zandbergen, *Currier language extension*: https://www.voynich.nu/extra/rz_lang.html

### 3. There is no same-Hand-3, same-quire A/B contrast behind the reported p-value

The earlier result file itself records only **two Language-A / Hand-3 pages** in the entire 227-page metadata table. Direct page audit identifies those as f58r/v in Quire 8. Quire 8 contains no Currier-B running text by Hand 3.

Therefore the claimed golden cell does **not** hold both scribe and physical section/quire constant. It holds LFD hand and the broad visual property "marginal stars" constant while comparing physically separated manuscript zones.

This means the 12.76 distance is real as a descriptive distance between those groups, but it cannot establish that Currier A/B survives physical-section/quire control.

## A second statistical problem: the A side is one physical folio

The previous pipeline concatenated words and split them into fixed 250-word blocks. `A/H3/$I=S` yielded three blocks (750 analysed words), but those blocks come from f58r/v — **the two sides of a single physical folio**.

Permuting those three blocks as though they were exchangeable independent replicates against 41 B blocks does not create independent manuscript evidence. At the folio level there is only one A observational unit in this supposed clean cell. The quoted block-level permutation p-value is therefore not a valid measure of replication across folios.

This does **not** imply that the A/B distinction is false. It means this particular experiment cannot prove that the distinction is independent of manuscript zone.

## What survives from the 2026-09-04 session

Several descriptive findings remain useful:

1. Currier A/B is strongly confounded with LFD hand in the manuscript as a whole.
2. Section/illustration regimes carry large textual differences.
3. The exact 250-word-block distances are reproducible for the ZL3b transliteration.
4. The observation that f58 differs strongly from Quire 20 is itself real; it was simply assigned too narrow a causal interpretation.

The headline **"Currier A/B survives holding scribe and section constant" should be withdrawn** pending a design that controls physical manuscript zone independently of language.

## Consequence for the planned axis-parallelism experiment

Do **not** compare an A→B axis defined by f58 (Quire 8) versus Quire 20 and call it a pure language axis. Any parallelism with Herbal→Biological could reflect combinations of language, quire, genre, layout, production phase, or local lexical regime.

The next defensible analysis should use one of these designs:

1. **Matched physical-neighbour design:** search for adjacent/bifolium-local A/B transitions within the same LFD hand. If none exist, report non-identifiability rather than manufacturing a control.
2. **Hierarchical page/folio model:** page or folio as the unit; language effect estimated alongside quire, illustration type and hand, with partial pooling and explicit rank/overlap diagnostics.
3. **Within-language section geometry first:** establish stable section axes entirely inside A and entirely inside B, then ask whether they generalise across manuscript zones without using the f58/Q20 contrast as a language ground truth.
4. **Transliteration sensitivity:** repeat any surviving result under Takahashi or another independent transliteration.

## Reproducibility

`src/audit_golden_cell.py` prints:

- every LFD Hand-3 page with Currier language, illustration type, quire and bifolio;
- all same-hand/same-quire cells that actually contain both A and B;
- the quire composition of the inherited `H3/$I=S` A and B cells.

It uses the same ZL3b parser as the 2026-09-04 attempt and therefore isolates the design error without changing the source data.

## Bottom line

**Significant negative/corrective result:** the board's strongest claimed clean Voynich A/B control is not clean. `$I=S` was treated as a section identifier when it is only an illustration-type flag, and the A side consists of one Quire-8 folio while the B side comes from later manuscript zones. The old p-value cannot support the claim that A/B is independent of section/quire.
