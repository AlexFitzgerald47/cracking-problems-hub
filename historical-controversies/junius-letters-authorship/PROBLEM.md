# The Letters of Junius: Re-testing the Attribution to Philip Francis

## Statement
The *Letters of Junius* (1769–72), a series of anonymous polemics against the government
of George III, remain the most famous unresolved authorship problem in English political
writing. Sir Philip Francis is the leading candidate, supported by Alvar Ellegård's 1962
stylometric study — one of the foundational works of quantitative authorship attribution.
Re-test that attribution with modern methods, and, equally important, test whether the
candidate set was ever properly constructed.

## Why it belongs on the board
This problem has an unusual property: **the evidence everyone relies on is now sixty
years old and was produced with methods that have since been substantially superseded.**
Ellegård's work was pioneering and his conclusion has largely been accepted, but it
predates modern authorship attribution entirely — no Burrows's Delta, no character
n-grams, no cross-validation, no principled significance testing, no imposters method.
Nobody appears to have systematically redone it.

That makes this a rare thing: a famous open question where the tractable path forward is
obvious, the corpus is fully available, and the required work is simply nobody's priority.
It is also a live methodological test. If modern methods reproduce Ellegård's result, that
is a meaningful validation of early stylometry. If they do not, a widely repeated
attribution needs revisiting.

The candidate-set question is the sharper one. Attribution methods are closed-set by
construction: they identify the best match *among candidates supplied*. If the true author
was never a candidate — and the eighteenth-century candidate list was assembled on
historical hunches, not systematically — every study since has been answering the wrong
question. Verification methods that can return "none of the above" did not exist when
Ellegård wrote and are the obvious application here.

## Known constraints / previous major attempts
- Junius's identity was concealed successfully in his own lifetime and has never been
  independently confirmed by external evidence. The attribution rests entirely on internal
  and circumstantial grounds.
- The case for Francis was made by John Taylor (1816) and elaborated by H. R. Francis
  (*Junius Revealed*, 1894), then given quantitative support by Alvar Ellegård,
  *A Statistical Method for Determining Authorship: The Junius Letters 1769–1772* (1962).
- Francis is now "generally, but not universally" accepted. Sceptical publications have
  continued; post-1980s scholarship has largely sidelined the alternatives, though
  arguably by attrition rather than by decisive test.
- Dozens of candidates have been proposed over two centuries, including Burke, Barré, and
  many others. Most were argued from biographical coincidence.
- The letters were published by Henry Sampson Woodfall; private correspondence between
  Junius and Woodfall survives and is part of the evidential base.

## Success criteria
1. Reproduction of Ellegård's analysis on his own terms, to establish a baseline and to
   check that his result is what it is remembered to be.
2. Independent re-test with modern methods — Burrows's Delta, character n-gram models,
   and at least one verification (open-set) method capable of rejecting all candidates —
   with proper cross-validation and reported confidence.
3. An explicit treatment of the closed-set problem: does the evidence support *Francis*,
   or merely *Francis over the others considered*? These are different claims and the
   distinction is the heart of the matter.
4. Controls that must not be skipped: genre and register differ sharply between polemical
   letters and Francis's official prose, and topic can masquerade as style. Any result
   that ignores this is worthless.

## Key sources & starting points
- The *Letters of Junius* — multiple public-domain editions; Project Gutenberg and the
  Internet Archive both carry them. **The primary corpus is fully available.**
- Comparison corpus for Francis: his published writings and official correspondence,
  substantially available through the Internet Archive and eighteenth-century collections.
  *Verify coverage and cleanliness before starting — this is the gating constraint, and
  ECCO-derived OCR quality varies badly.*
- Alvar Ellegård (1962), as above; also his *Who was Junius?* (1962).
- Wikipedia, "Identity of Junius" — usable as an index to the candidate literature only.

## Notes
The named comparison corpus an agent actually needs is Francis's non-Junius prose in
clean, machine-readable form, plus comparable-genre samples from at least a dozen rival
candidates. Assembling that is the real work; the statistics are routine once it exists.
OCR quality will be the limiting factor and must be reported honestly, since character
n-gram methods are sensitive to it.

Difficulty: moderate. Tractability with text/compute alone: **very good** — arguably the
most immediately actionable problem in this batch.

Time-waster warning: resist the pull of the biographical detective story. Two centuries
of that have produced no resolution. The contribution here is methodological rigour, and
a negative result — "the evidence does not identify an author" — is a perfectly good
outcome and should be reported as confidently as a positive one.
