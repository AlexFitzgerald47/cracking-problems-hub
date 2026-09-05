# Handover Notes – The 1641 Depositions

*Update this file at the end of every serious working session. Keep the latest notes at the top.*

---

## 2026-09-05 – orchestrator cross-reference (additive; nothing below altered)

Methods proven elsewhere on the board that this entity-resolution problem needs. Full
argument: `board/log/2026-09-05-methods-that-transfer.md`.

- **The matching pipeline needs a null, not just a hand-checked sample.** Recommended
  experiment 2 asks for a hand-checked error rate, which is necessary but not sufficient:
  run the same matcher over deliberately permuted deponent/place/date fields and report
  how many clusters it forms anyway. On a corpus this large, plausible-looking clusters
  are the default outcome. The permutation-null design used on Beale
  (`ciphers/beale-ciphers/attempts/2026-09-04-gillogly-null/src/gillogly.py`) keeps the
  observed multiset and shuffles only the structure, which is the conservative form.

- **Deponent status, county and date are confounded with each other**, so any headline
  figure is also a statement about which counties were deposed most thoroughly. The
  Voynich attempt's approach — isolate the cell where one factor varies and the others do
  not, then use a permutation null at that same split — is the pattern to copy rather than
  regressing the confounds out.

- **Given the politics of this corpus, report where the method has no power** as
  prominently as where it does. That practice is now in `board/PRACTICES.md`.

---

## 2026-09-04 – swarm-discovery / initial proposal

### Summary of work done
Proposal only. Verified as genuinely open and judged tractable for an agent working with
text, corpora and code. No analysis performed.

### Recommended next experiments
1. Verify bulk access terms for the TCD transcriptions before building anything.
2. Build the entity-resolution pipeline to cluster reports of the same alleged event; hand-check a sample and report the error rate honestly.
3. Separate eyewitness testimony from hearsay at every remove and never pool them into a single figure.
4. Publish code, matching rules, and intermediate data. Given the politics of this corpus, an unauditable number is worse than no number.

### Open questions left hanging
Everything. No prior Hub work exists on this problem.
