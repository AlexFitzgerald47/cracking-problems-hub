# Frozen predictions — 2026-09-23, before the Annals of the Four Masters were fetched

Everything in `RESULTS.md` up to this point is **exploratory**: it was derived on
AU / AT / CS / AI, and the Patrician entries were read before the comparison
class was built. The predictions below are recorded *before* the holdout witness
was fetched or parsed, and are tested in `results/afm_*.json`.

Holdout: the **Annals of the Four Masters** (CELT `T100005A`ff.), compiled at
Donegal 1632–36. It is an independent editorial act, three centuries later than
anything in the developed corpus, drawing on the Annals of Clonmacnoise, the
Book of Lecan and other witnesses the four texts above do not descend from.

## P1 — the marker stratum replicates
AFM's alternative-source markers will be concentrated before c.700: the rate in
430–699 will be at least **3×** the rate in 700–1099.
*Fails if* the ratio is below 3.
*Vacuous if* AFM carries fewer than 8 markers in total — the Four Masters may
have harmonised variants away, which is a real possibility and is not a pass.

## P2 — the comparison class does not reach the Patrician gap  **(the strong test)**
Building AFM's comparison class by the same procedure (multiply-dated events,
430–760, hand-audited), **no non-Patrician cluster will have a consecutive gap
of 31 years or more**.
*Fails if* any does. This is the prediction the headline claim actually rests
on: the claim is that a 31-year step is outside what these compilers do, and a
witness they did not contribute to is entitled to refute it.

## P3 — the Patrician bimodality replicates
AFM will record a Patrician obit at two or more years whose largest consecutive
gap is **≥ 25 years**.
*Held weakly:* it is background knowledge that AFM dates Sen-Phátraic to 457 and
Patrick to 493, so a pass here is worth much less than a pass on P2, and is
recorded as a consistency check rather than a test.

## P4 — each sub-tradition is ordinary
In AFM, each Patrician sub-tradition taken alone will span **≤ 8 years** (the
90th percentile of the developed comparison class). The claim is bimodality,
not dispersion; a smear would refute it.
*Fails if* either sub-tradition spans more than 8 years.

## P5 — the changepoint lands in the same place
A single changepoint fitted to AFM's marker rate alone will fall in **560–760**.
(The four-witness fit was 663, year-level bootstrap 596–666.)
*Fails if* it falls outside, or if AFM has too few markers to fit.

## Not predicted
Nothing is predicted about *which* Patrick AFM assigns to which year, about the
identity question, or about Palladius. This analysis measures the shape of the
annalistic disagreement; it does not count people.
