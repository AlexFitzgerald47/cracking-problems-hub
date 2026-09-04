# Famine Mortality at Parish Resolution: The Unindexed NLI Parish Registers

## Statement
Great Famine mortality is known at county, baronial and district-electoral-division
resolution, but not reliably at parish level — the resolution at which the enormous local
variation in the catastrophe actually happened. The National Library of Ireland holds a
free, fully digitised image corpus of Catholic parish registers that in principle spans
the Famine decade for over a thousand parishes, and it has never been transcribed or
indexed. The open problem is what parish-resolution demographic estimates that corpus can
actually support once turned into data — and, equally, what it cannot.

## Corpus status — read this first
**Images exist; data must be produced.** *Verified:* the NLI released its digitised Roman
Catholic parish register microfilm collection free at `registers.nli.ie` on 8 July 2015 —
approximately **373,000 images**, from about **3,500 registers** covering **1,086 parishes**,
dating **1740–1880**, containing **baptisms and marriages**. The NLI has explicitly **not**
transcribed or indexed the collection: it is browsable by parish only and cannot be searched
by name. Partial third-party indexes exist (Irish Genealogy for Kerry, Dublin city and parts
of Cork, free; Roots Ireland for most parishes, subscription).

This is the whole shape of the problem: a large, open, free image corpus with zero
structured data behind it.

## Why it belongs on the board
The corpus is genuinely open, genuinely large, and genuinely unexploited for quantitative
history — a rare combination. The task is concrete data engineering with a well-posed
demographic question at the end of it, and the answer would refine a number that matters.

*Verified as still open:* the state of the field is that "precise mortality figures at local
level remain elusive", with the regional picture resting on Cousens, Mokyr, Ó Gráda and
more recently Willie Smyth; successive work has pushed from county-level (n=32) to
parish-level 1841 census data (n=2,437) and to district electoral divisions (n>3,000) and
baronies (n>300). The disaggregation effort is live and incomplete.

## Known constraints / previous major attempts
- **P. Boyle and C. Ó Gráda, "Fertility Trends, Excess Mortality, and the Great Irish
  Famine," *Demography* (1986).** *Verified as existing* (Springer/JSTOR listings). The key
  methodological precedent: excess mortality inferred **indirectly from fertility
  (baptism) shortfalls**, not from counting burials. Understand why before starting.
- **S. H. Cousens, "Regional death rates in Ireland during the great famine, from 1846 to
  1851," *Population Studies* 14:1 (1960).** *Verified as existing.*
- **Joel Mokyr's** county-level excess-mortality estimates — the standard against which any
  new figure must be benchmarked. Mokyr's calculation attributes roughly 40 per cent of
  total excess deaths (~437,000) to Connacht. *Figure reported from a search summary;
  re-check against Mokyr directly before citing.*
- **M. Blum, C. L. Colvin and E. McLaughlin, "Scarring and Selection in the Great Irish
  Famine," *Economic History Review* 79:1 (Feb 2026), pp. 189–220,** DOI 10.1111/ehr.70013.
  *Verified:* author list, venue, volume, issue, pagination and DOI all confirmed. **Note
  the correction:** this was proposed to the run as single-authored by Blum; it is not. It
  is anthropometric (stature, scarring versus selection, ~14,500 individuals) and so
  demonstrates that Famine demography is actively worked in 2026 — it is *not* itself
  evidence about parish-level mortality, and should not be cited as though it were.
- Guinnane and Ó Gráda on workhouse mortality — complementary institutional data.
  *Existence reported, not independently verified this run.*

## Success criteria
1. A transcription pipeline over a defined, deliberately stratified sample of parishes
   spanning counties of differing Famine severity, with a reported and honest OCR/HTR
   accuracy rate against a hand-checked gold-standard subset. The accuracy figure is part
   of the deliverable, not an implementation detail.
2. Parish-level baptism series across c.1835–1855, with the fertility trend break
   quantified per parish.
3. Parish-resolution excess-mortality estimates derived by the Boyle–Ó Gráda indirect
   method, with confidence intervals, benchmarked against existing county-level figures.
4. An explicit register-survival map: which parishes have continuous coverage through
   1845–51 and which do not. Survival is certainly not random with respect to Famine
   severity, and quantifying that bias may be the most durable contribution here.

## Key sources & starting points
- `registers.nli.ie` — the corpus. Free, no account required. Figures above verified.
- Boyle and Ó Gráda (1986); Cousens (1960); Mokyr — as above.
- The 1841 and 1851 censuses for denominators; the 1851 census's own mortality tables are
  themselves a contested source and should be treated as evidence to be audited, not ground
  truth.

## Notes
Difficulty: high. Tractability with text/compute alone: **mixed, and honestly assessed as
lower than it first appears** — the images are open and the demographic method is
established, but handwritten-text recognition on nineteenth-century Latin-abbreviated
parish hands at scale is a hard problem in its own right.

**Time-waster warning — the sharpest in this batch, and the reason this folder exists.**
Catholic parish registers of this period record **baptisms and marriages**. They very often
do **not** record burials at all; many parishes kept no burial register before the later
nineteenth century, and the NLI collection is described as baptisms and marriages
(*verified*). This is precisely why Boyle and Ó Gráda inferred mortality indirectly from
fertility shortfalls instead of counting deaths. An agent who sets out to measure Famine
mortality by counting burials in this corpus will spend a session transcribing before
discovering the deaths are not in there. **The indirect fertility-shortfall method is not
one option among several; it is the only method this source base supports.** Design for it
from the first hour.

Second trap: transcribing whatever parishes are easiest to read. Legibility correlates with
parish wealth and clerical practice, which correlate with Famine impact. Stratify the
sample deliberately or the result is biased in the direction of the thing being measured.
