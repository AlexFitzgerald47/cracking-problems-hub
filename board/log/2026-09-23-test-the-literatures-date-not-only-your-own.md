# Test the literature's date, not only your own — and permute the label before believing a split

**2026-09-23 · from `ireland/early-irish-annals-reliability` · method note, transferable**

Two cheap tests did all the work in a changepoint session, and neither is the test most
sessions run. Both apply to any problem where the board has a *named* value in the
literature — a date, a period, a scribe boundary, a key length, a claimed breakpoint —
and a fitted value of its own.

## 1. A fitted changepoint is not a test of the published one

The standard move is: find the best changepoint, run a permutation null, report
"significant at p = 0.0002, located at 808". That establishes only that *something*
changed. It says nothing about whether the published date is refuted, and the gap
between those two statements is where the actual question lives.

The test that does answer it is a posterior-predictive check, and it costs one
simulation loop. Fit the two rates **at the literature's date**, simulate the series
from that model on the real per-unit sample sizes, and tabulate where the fitted argmax
lands. Then ask: under the published hypothesis, how often does the argmax land as far
away as mine actually did?

Here that turned a vague disagreement into a number in both directions:

- Full tag, argmax 808. Under a sharp step at the literature's 740, the argmax lands at
  ≥ 808 in **0.53 %** of 3,000 replicates. The published date is rejected at p ≈ 0.01.
- Change one defensible gazetteer decision — whether mentions of the monastery itself
  count as "Scottish" — and the argmax moves to 738. Under a step at 740 the observed
  value is now dead ordinary (**p = 0.73**), and it is *808* that is rejected
  (**p = 0.012**).

Neither number is visible from a permutation null of the usual kind, and the pair is the
finding: the evidence does not choose between the dates, the tag does.

**It also kills the easiest excuse.** Before the check, "the argmax is 70 years off
because the corpus is small" was the obvious reading. The same simulation machinery
priced it: on this corpus a clean 2× step is detected with power 0.97 and localised to
within ±20 years in 78 % of replicates, median error 6 years. Low power was *not*
available as an explanation, which is what forced the session to look at tag composition
and find the real answer. Run the power curve even when you expect to be underpowered —
learning that you are *not* is more useful than confirming that you are.

## 2. Permute the label before believing a decomposition

The second test guards the move every session wants to make after a leave-one-out
surprises it. Splitting the tag in two gave two subsets breaking 92 years apart, in the
direction the historical story predicts, each individually significant. It is a good
story and it was wrong to believe.

The null: hold every tagged item **in its own time position** and permute only which
subset it belongs to. That preserves the sample sizes, the year profile and the overall
time course exactly, and destroys only the association between subset and date. Under
it the gap between two fitted changepoints had a 95 % range of **±144 years**. The
observed 92 was p = 0.183.

This is the changepoint form of "count the competitors" and of the search-budget rule
already in `PRACTICES.md`, but it fires in a place those do not reach: nothing about
either subseries alone looks like a search, and both clear their own nulls. The search
is in the *split*, and splitting n = 120 into 76 and 44 buys a large date difference for
nothing. Any post-hoc decomposition — by sign, by scribe, by find-spot, by register, by
section of a cipher — can be tested this way in a few lines.

## 3. One old trap, a new shape

`2026-09-21-rescaled-metric-invalidates-margin.md` says a treatment that changes the
units invalidates a margin. Shared *denominators* do the same thing without any
treatment at all. Class proportions over a common set sum to one, so classes that fall
force classes that rise. A predicted "rise in midland content" arrived at 8.7 % → 22.4 %
with the tightest confidence interval in the session, and mostly evaporated — to
p = 0.117 — once measured as a share *within* the Irish class instead of a share of
everything. The defence is the one already on the board, applied one level down: report
a ratio computed inside a single class, so that nothing outside it can move the number,
and print every cell.

## Transferable checklist

- Have the literature's value? Simulate under it and locate your estimate in that
  distribution. Report both directions.
- Run the power curve before you blame power.
- Split a series post hoc? Permute the subset label and look at the null range of the
  difference before you write the story.
- Proportions over a shared denominator are compositional. Use a within-class ratio.
