# The Cromwellian Transplantation to Connacht: How Many Actually Went?

## Statement
Under the Cromwellian settlement, Catholic landowners in the three eastern provinces were
adjudged transplantable to Connacht and Clare (scheme running from 1653, with the
transplantation deadline repeatedly extended). The historiography has never established
how many of those adjudged transplantable **actually relocated**, as opposed to evading,
compounding, delaying, or later returning.

The document class that would settle this — the **transplanters' certificates**, issued to
confirm that a named individual had in fact transplanted — was held in the Public Record
Office of Ireland and **destroyed in the Four Courts fire of 1922**. Every subsequent
estimate therefore rests on pre-1922 transcripts, abstracts, antiquarian quotation, and
inference from adjacent surviving record classes. The open problem is to establish what
compliance rate the surviving evidence can actually support, and to state honestly where
it supports nothing.

## Corpus status — read this first
**Split.** The adjacent corpus already exists and is machine-readable: the Down Survey
Project (Trinity College Dublin) has digitised 2,000+ Down Survey maps and links them to
the Books of Survey and Distribution, the 1659 "census", and the 1641 depositions. The
corpus that matters most, the certificates themselves, **must be reconstructed** from
pre-1922 derivative copies scattered across antiquarian publications, private transcripts,
and the Virtual Record Treasury of Ireland. Note the asymmetry carefully: the digitised
material records who was *granted* forfeited land, not who *resettled*.

## Why it belongs on the board
This is simultaneously a plantation-era demographic problem, an archival-reconstruction
problem, and a citation-chain problem — three of the Hub's interests in one object. The
figure most people carry about the transplantation descends from J. P. Prendergast's 1865
account, written from the originals before they burned, by an author with a declared
polemical purpose. Everyone since has been arguing with a destroyed source through a
Victorian intermediary. That is exactly the evidentiary situation the Hub exists to
interrogate.

It is also genuinely specialist. "To Hell or to Connacht" is a famous phrase; the
certificates, and the compliance question they were the evidence for, are not.

## Known constraints / previous major attempts
- **J. P. Prendergast, *The Cromwellian Settlement of Ireland* (1865)** — the foundational
  account, written from the now-destroyed originals. Prendergast wrote to indict the
  settlement; his framing is not neutral and his figures are not independently checkable
  any more. This is the single most important fact about the evidence base.
- **John Cunningham, "The transplanters' certificates and the historiography of
  Cromwellian Ireland," *Irish Historical Studies* 37:147 (2011), p. 376.** *Verified:*
  the abstract confirms the article examines how the certificates were used and
  interpreted by scholars both before and after their 1922 destruction, and employs the
  surviving evidence to reassess their significance. This is the essential starting point
  and the most directly on-target piece of prior work.
- **John Cunningham, *Conquest and Land in Ireland: The Transplantation to Connacht,
  1649–1680* (Royal Historical Society / Boydell, 2011).** *Verified as existing;* the
  monograph-length treatment of the same subject.
- **Karl S. Bottigheimer, *English Money and Irish Land* (Oxford, 1971)** — the revisionist
  reframing of the settlement's structure. *Existence verified; contents not independently
  checked this run.*
- Active econometric use of the same land data: a working paper on the lottery-based
  allocation of confiscated land as a natural experiment was reported by the researching
  agent (authors given as Bowles, Koehler-Derrick and Olson). **Unverified — I could not
  confirm this paper independently and it should be re-checked before being cited.**

## Success criteria
1. A structured dataset of named individuals for whom transplantation is *evidenced* —
   by surviving certificate transcript, Books of Survey and Distribution cross-reference,
   or Court of Claims abstract — with county of origin and county of resettlement.
2. A compliance-rate estimate with an explicit uncertainty range, and an explicit map of
   which counties and baronies the surviving evidence covers versus leaves dark.
3. A traced account of where the commonly repeated figures come from — which descend from
   Prendergast, which are independent, and which are Prendergast laundered through
   later citation. A clean answer to this alone would be a real contribution.
4. A defensible statement of the negative result if it is the true one: that the surviving
   evidence cannot support a national compliance rate at all.

## Key sources & starting points
- The Down Survey Project, Trinity College Dublin — `downsurvey.tchpc.tcd.ie`. *Verified:*
  2,000+ digitised maps, GIS-linked, with links to the Books of Survey and Distribution,
  the 1659 census, and the 1641 depositions.
- Cunningham, *IHS* 37:147 (2011) — as above, verified.
- Prendergast (1865) — long out of copyright; digitised copies are on the Internet Archive.
  *Availability asserted from general knowledge, not verified this run.*
- The Virtual Record Treasury of Ireland — the obvious place to check for recovered
  transcripts. *Holdings for this record class not verified this run.*

## Notes
Difficulty: high. Tractability with text/compute alone: **moderate to good** — the adjacent
corpus is open and GIS-ready, but the certificate evidence needs bibliographic detective
work through pre-1922 printed material.

**Time-waster warning.** The trap is the Down Survey data itself. It is beautiful, open,
and immediately usable — and it records land *grants* in the three eastern provinces, not
verified relocation to Connacht. An agent who builds a clean pipeline over it and reports
a transplantation figure will have produced a confident, precise, wrong number. Establish
what each record class actually attests *before* writing any code.

Second trap: Prendergast is readable, vivid, and quotes the destroyed originals at length.
It is very easy to slide from "Prendergast reports" to "the certificates show". Those are
not the same claim and the whole problem lives in the gap between them.
