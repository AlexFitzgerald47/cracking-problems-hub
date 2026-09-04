# Ireland's Population Before the Census: The Hearth Tax Multiplier Problem

## Statement
Ireland had no census before 1821. For the period c.1660–1821 the principal population
proxy is the hearth money returns, converted into population estimates by an assumed
household multiplier and an assumed evasion/under-registration rate. Both assumptions are
contested, neither is directly evidenced, and the resulting national population series —
which underpins essentially every quantitative statement about pre-Famine Ireland,
including the demographic baseline against which Famine mortality is measured — has not
been systematically rebuilt in over forty years.

The originals were held in the Public Record Office of Ireland and destroyed in 1922.
What survives is a patchwork of pre-1922 transcripts of very uneven county coverage.

## Corpus status — read this first
**Must be produced.** The surviving hearth money material is scattered across PRONI, local
historical societies, antiquarian journal appendices, genealogy-sector transcriptions, and
the Virtual Record Treasury. No consolidated, machine-readable, research-structured
dataset appears to exist. Building the inventory *is* the first deliverable and is worth
doing whether or not any new population estimate follows.

## Why it belongs on the board
This is the load-bearing number under a whole literature. It is also a textbook instance of
the pattern the Hub cares most about: a 1982 paper did the work properly, everyone has
cited it since, and nobody has redone it with the material that digitisation has since made
reachable. The estimate is not wrong because it was done badly — it was done well, once,
with what was then available. It is open because nobody has revisited it.

Specialist-recognisable, general-audience invisible, and quantitative. It also pairs
naturally with `famine-parish-register-mortality/` in this batch: that problem needs a
pre-Famine denominator, and this problem is that denominator.

## Known constraints / previous major attempts
- **D. Dickson, C. Ó Gráda and S. Daultrey, "Hearth Tax, Household Size and Irish
  Population Change 1672–1821," *Proceedings of the Royal Irish Academy* 82C (1982),
  pp. 125–160, 162–181.** *Verified:* author, title, venue, volume, year and pagination all
  confirmed; JSTOR stable 25506086; also in the UCD research repository. This is the
  standard reference and the thing to be re-tested.
- **K. H. Connell's earlier population work** is the tradition Dickson et al. were
  correcting. *Existence and role verified at summary level only.*
- **L. M. Cullen, "Population Trends in Seventeenth-Century Ireland"** — earlier framing.
  *Existence verified via a TCD repository listing; contents not checked.*
- A structural constraint worth knowing before starting: the establishment lists recording
  the officers on the hearth-tax payroll do not survive, so conclusions about collection
  practice — and therefore about evasion rates — are necessarily indirect. *Reported by the
  researching agent from a search snippet; treat as strong lead, re-check before relying.*
- Genealogy-sector inventories of which counties' rolls survive in transcript are useful
  for corpus-mapping but are not scholarly finding aids. Treat all county-survival claims
  from that sector as provisional until checked against an archival catalogue.

## Success criteria
1. A consolidated, cited inventory of exactly which parishes and baronies have surviving
   hearth-tax data in any form, with repository and provenance for each. This is the
   primary artefact and stands alone.
2. A re-derived provincial and (if defensible) national population series for c.1660–1821
   that states its multiplier and evasion assumptions explicitly, propagates their
   uncertainty, and shows the resulting range against Dickson–Ó Gráda–Daultrey (1982).
3. A sensitivity analysis: how much of the accepted series is driven by the multiplier
   choice rather than by the data? If the answer is "most of it", that is the finding.

## Key sources & starting points
- Dickson, Ó Gráda and Daultrey (1982), as above — verified.
- PRONI and the Virtual Record Treasury of Ireland for surviving transcripts. *Specific
  holdings not verified this run — establishing them is part of the work.*
- *History Ireland*, "A taxing enquiry: how many people were there in pre-census Ireland?"
  — a popular-register overview surfaced during verification; usable as an orientation
  pointer only, not as evidence.

## Notes
Difficulty: high. Tractability with text/compute alone: **moderate** — the bottleneck is
bibliographic and archival locating rather than computation or object access, which is
exactly the profile the brief favours.

**Time-waster warning.** County coverage is severely uneven — full or near-full rolls for a
handful of counties, thin fragments or nothing elsewhere. An agent who aggregates whatever
survives into a national figure will produce an estimate silently dominated by the
best-preserved counties, and the survival pattern is not random with respect to region,
settlement type, or landlord. Build the coverage map first and let it constrain what
claims are permissible. If the honest answer is "provincial estimates only, and not for
Connacht", say so.

Second trap: treating the multiplier as a parameter to be tuned until the output matches a
known later census. That is curve-fitting, not estimation, and it will reproduce the
existing series by construction.
