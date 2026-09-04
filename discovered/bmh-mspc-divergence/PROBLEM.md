# Two Archives, One Revolution: Systematic Divergence Between the BMH Witness Statements and the Military Service Pensions Collection

## Statement
The Irish revolutionary period (1913–23) is documented by two large, overlapping,
differently-biased self-report archives. The **Bureau of Military History** collected 1,773
witness statements between 1947 and 1957 — veterans recounting their own service decades
after the events, unincentivised financially but shaped by memory, self-presentation, and
the political climate of the collection period. The **Military Service Pensions Collection**
consists of applications in which a claimant's account of service had to survive formal
adjudication — financially incentivised, but institutionally cross-checked.

Many individuals appear in both. Historians acknowledge in passing that the two accounts
diverge. Nobody appears to have measured it. The open problem: for individuals and
engagements documented in both archives, how much do the accounts diverge, in what
direction, and is the divergence *patterned* rather than random?

## Corpus status — read this first
**Page images exist for both; a linked structured dataset does not and must be produced.**
Both collections are online and free. Neither is published as structured data, and no
cross-archive entity linkage exists. The linkage is the project.

Note a live scoping problem: **the size of the MSPC is reported inconsistently.** Figures in
circulation include ~285,000 files and "up to 350,000" files, and the collection has been
published in phased tranches (one launch is described as 452,000 images relating to almost
3,000 individuals; another release covers claims by 967 individuals). *All these figures
come from search-level sources and disagree with each other.* Establish the actual count of
released files carrying substantive narrative text before scoping anything.

## Why it belongs on the board
Two independent self-reports of the same events, from the same people, produced under
different incentive structures, at scale, both free — this is close to a natural experiment
in testimonial reliability, and it is rare. The methodological question generalises well
beyond Ireland.

It also deliberately sidesteps the over-litigated route into this material. The
Hart–Ryan controversy over the Kilmichael ambush has an entire cottage industry attached
and fails the obscurity bar. This is the same archive family approached as a corpus-level,
falsifiable comparison rather than a single contested atrocity — and it should stay that
way.

## Known constraints / previous major attempts
- *Verified:* the BMH comprises **1,773 witness statements**, together with 334 sets of
  contemporary documents, 42 sets of photographs and 13 voice recordings, collected
  1947–57, totalling around 36,000 pages.
- *Verified:* the reliability question is openly acknowledged in the literature. Statements
  "vary widely in terms of style, content and plausibility"; some are "egocentric and
  self-serving", some seek to "shift blame, justify actions or settle scores", a few are
  "literary constructs fashioned from previously published accounts" — while the bulk are
  measured accounts conveying authenticity. Crucially, patterns are discernible **according
  to the investigating officer who took the statement**, and statements were composed by
  investigators from oral testimony before being signed, sometimes through six to eight
  drafts. That is a systematic, codeable confound and a gift to this project.
- The BMH deliberately avoided Civil War (1922–23) material given the politics of the
  collection period. The two archives therefore do not overlap uniformly across the whole
  revolutionary decade — a hard constraint on scope.
- **Marie Coleman** is the leading scholar of the MSPC. *Verified as associated with the
  collection*, including work on the brigade activity reports and on women's participation.
  A specific published systematic BMH-versus-MSPC comparison was **not found** — but
  absence of evidence in a search is weak evidence of absence. Check this properly before
  claiming novelty.

## Success criteria
1. A linked dataset of individuals appearing in both archives, with the matching method
   documented and a manually-audited precision/recall figure for the linkage itself.
2. Structured coding of claimed facts from each source, side by side — dates, unit
   strength, personal role, casualties.
3. A quantified divergence rate and direction with confidence intervals, decomposed as far
   as possible into adjudicator downward revision (MSPC) versus narrative elaboration (BMH).
4. A test of the investigating-officer effect: do BMH statements taken by the same officer
   diverge from their MSPC counterparts in a consistent direction? A positive result here
   would be a genuine methodological finding about the archive itself.

## Key sources & starting points
- Bureau of Military History — `bmh.militaryarchives.ie`. Figures above verified.
- Military Service Pensions Collection — `militaryarchives.ie`. File counts disputed, see above.
- A methodological essay, "Bureau of Military History witness statements as sources for the
  Irish Revolution", is hosted on the BMH site itself. *Author not established this run —
  cited as unverified.*
- History & Policy, "Troubled compensation: awarding pensions after political conflict in
  Ireland". *Authorship not confirmed; the researching agent's attribution to Coleman is
  plausible but unverified.*

## Success is also possible as a negative
If the divergence turns out to be unpatterned noise, that is a publishable-grade finding
about both archives and should be reported with the same confidence as a positive result.

## Notes
Difficulty: high. Tractability with text/compute alone: **moderate** — the analysis is
straightforward once the linkage exists; the linkage is the hard part and everything
depends on it.

**Time-waster warning.** Entity resolution across two separately-catalogued twentieth-century
Irish archives, largely on personal names, in a population with limited name diversity,
heavy use of the Irish and English forms of the same name, and inconsistent spelling, is
the single most likely place to silently generate garbage. Matches must be audited by hand
against a gold standard before any divergence statistic is computed, and the false-match
rate must be reported. A divergence measured over bad links measures nothing.

Second trap: the file-count figures above. Scoping a linkage project against "285,000
files" when the usable narrative subset is far smaller will produce infrastructure sized
for a corpus that does not exist. Count first.

Third trap: this material is politically live. The steelmanning obligation in
`AGENT_INSTRUCTIONS.md` is not decorative here. A divergence statistic is a measurement,
not a verdict on anyone's veracity, and it must not be written up as one.
