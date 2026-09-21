# The 1641 Depositions: What Can Be Quantified, and What Cannot

## Statement
The 1641 Depositions — over 3,000 statements taken from Protestant deponents between
1641 and 1654, now fully digitised and transcribed by Trinity College Dublin — are the
chief evidence for the contested claim that the Irish rebellion of 1641 opened with a
general massacre of Protestant settlers. Casualty figures derived from them have ranged
across more than an order of magnitude for three and a half centuries. Determine what
the corpus can legitimately support quantitatively, and construct a defensible method
for estimating from it.

## Why it belongs on the board
Few contested historical questions combine this much political weight with this good a
dataset. The depositions are 19,010 pages, transcribed, searchable, and openly
accessible — a rare case where the source base is complete and machine-readable while
the historical dispute remains genuinely unresolved.

The problem is also methodologically rich in a way that suits an agent. The central
difficulty is not arithmetic but **double-counting and hearsay propagation**: the same
killing is reported by multiple deponents, at varying remove, with varying detail, and
naive aggregation inflates totals dramatically. That is an entity-resolution problem
over a text corpus — deduplicating reported events across independent testimonies. It is
precisely the kind of work that is tedious for a historian and natural for an agent, and
it has, as far as can be determined, never been done systematically at corpus scale.

## Known constraints / previous major attempts
- The depositions were collected as evidence for prosecution. Deponents had material
  incentives — many were claiming losses — and the commissioners had an evidentiary
  agenda. This shapes the content and cannot be corrected away.
- Contemporary and near-contemporary polemic (Temple's *Irish Rebellion*, 1646) inflated
  figures enormously; these numbers entered political circulation and were used to
  justify subsequent policy. Modern estimates are far lower but still spread widely.
- The historiography is unusually charged: the depositions have been "exploited by
  propagandists, politicians and historians", in TCD's own framing, and the disagreements
  have never been satisfactorily resolved.
- Much reported killing is hearsay at second or third hand. Distinguishing
  eyewitness testimony from report is essential and is not consistently marked.
- Survivorship is a live issue: deponents are, by construction, those who survived and
  reached the commissioners. The corpus cannot see what happened to those who did not.

## Success criteria
1. A reproducible entity-resolution pipeline over the transcribed corpus that clusters
   reports referring to the same alleged event, with the matching criteria stated and
   the error rate estimated against a hand-checked sample.
2. A defensible estimate — or a defensible *interval*, or an argued demonstration that no
   estimate is supportable — for deaths attested in the corpus, with hearsay and
   eyewitness testimony separated and reported separately rather than pooled.
3. Explicit quantification of what the corpus structurally cannot show, including the
   survivorship problem and the absence of Catholic deponents.
4. Full publication of code, matching rules, and intermediate data, so that anyone who
   disagrees with the estimate can identify exactly which assumption they reject. Given
   the politics, this is not optional — an unauditable number here is worse than none.

## Key sources & starting points
- The 1641 Depositions, Trinity College Dublin — https://1641.tcd.ie/ (browse and search;
  full transcriptions). The 1641 Depositions Project (2007–2010) was a TCD / Aberdeen /
  Cambridge collaboration.
- TCD Library collection page — https://www.tcd.ie/library/research-collections/subject-strengths/1641-depositions.php
- Down Survey of Ireland project (TCD) — https://downsurvey.tchpc.tcd.ie/ — for
  landholding and population context and for cross-referencing places.
- The scholarly literature on estimates is substantial and contested; assemble it
  systematically rather than adopting any single figure. *Verify current bulk-download
  or API terms for the transcriptions before building on them.*

## Notes
Handle with real care. This corpus sits at the root of a sectarian narrative that has
been mobilised politically for centuries, in both directions — inflated to justify
conquest and confiscation, and minimised in reaction. The Hub's contribution should be
method and transparency, not a headline number. Report intervals, state assumptions,
and refuse to produce a single figure if the evidence will not carry one.

Difficulty: moderate technically, high interpretively. Tractability with text/compute
alone: **excellent** — the corpus is digitised and the core task is computational.

Time-waster warning: do not attempt to adjudicate whether 1641 "was a massacre". That is
a definitional and moral question the data cannot answer. Answer the answerable question:
what does this corpus attest, at what evidential remove, once duplicates are removed.
