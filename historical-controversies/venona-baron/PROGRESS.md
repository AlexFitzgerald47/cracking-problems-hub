# Progress log — VENONA BARON

## 2026-09-07 — Session 1 (Claude Opus 5, cracker, mode: starting)

**Intent.** Open BARON — the London GRU source connected with British Enigma decryption,
ranked the number-one Dominic Sandbrook target by the 2026-09-05 frontier-model pass and
never worked. Build the message ledger, freeze the constraint set before naming anyone, and
test the standing Sedláček hypothesis.

### What actually happened: the corpus was unreachable

`WebFetch` returned `EGRESS_BLOCKED` for **every** domain attempted — `wilsoncenter.org`,
`nsa.gov`, `archive.org`, `en.wikipedia.org`, `coldspur.com`, `sunnycv.com`,
`winstonchurchill.org`. Direct `curl` reached only GitHub hosts (`000`/403 for
`media.defense.gov`, `web.archive.org`, `cia.gov`, `digitalarchive.wilsoncenter.org`).
`WebSearch` worked.

So **this session never read a single VENONA document.** That is recorded in
`analysis/access-ledger.md` with the full block list and a labelling scheme
(`[PRIMARY]`/`[SEARCH]`/`[HUB]`/`[INFERRED]`/`[MISSING]`) applied to every claim in the
folder. **No claim in this folder carries `[PRIMARY]`.** Read that file before trusting
anything here.

### Result 1 — BARON is not the clean unidentified covername the board thought it was

The frontier-model pass ranked BARON #1 for Dominic on the premise that "the NSA's VENONA
history still describes BARON as unidentified." That premise is incomplete. **Nigel West
identified BARON as Karel Sedláček in 1999** (*VENONA*, pp. 67–69), and the identification
is carried in **John Earl Haynes's standard cover-name concordance** as
`"Baron": Sedlacek, Karel (U.K. line, [West Venona])`.

This is a near miss on the **DAN failure mode** the same discovery pass had already
identified and warned against: a cable footnote saying "unidentified" was taken as a
solution-status check. It is not one. VENONA translator footnotes were written once and
rarely revised, so the same covername can be footnoted "unidentified" in one translation and
identified in another. Full audit: `analysis/solution-status-ledger.md`.

**The target survives, restated.** It is an adjudication of a named hypothesis, not an
open-field search — and the hypothesis has a hard problem: Sedláček was resident in
**Switzerland** (Zurich, then Lucerne from spring 1939), reporting *to* London by wireless
from September 1939 with material from Hausamann and Roessler. A source in Lucerne supplying
*German* product is an awkward fit for a London-line source reporting on *British*
cryptanalysis. Two escapes — relay through the Czech London station, or misattribution —
both testable, both specified.

### Result 2 — the 3 April 1941 date collision

London GRU No. 649, the BARON Enigma cable, is dated **3 April 1941**. On **3 April 1941**
Churchill sent Stalin, via Cripps, his only direct pre-Barbarossa warning — Enigma-derived
intelligence about three of five panzer divisions moving from Romania to southern Poland,
deliberately attributed to *"a trusted agent"* to conceal the SIGINT source.

The point is not the coincidence, it is what it implies about **what BARON was selling**.
Churchill's whole security design was to hide the provenance. A source reporting the
provenance defeats exactly that design, and provenance knowledge in London in April 1941 was
held by a far smaller set of people than the product was.

Written up as a **preregistered hypothesis with five falsifying tests frozen before the
evidence is available** (`analysis/churchill-date-collision.md`), with the search budget
stated honestly: the observation is post hoc, the naive same-day probability of ~0.3% is not
the right denominator, and the file explicitly says it is hypothesis-generating and **must
not** be cited as support for a candidate. Test T1 — the subject matter of No. 649 — kills
or keeps it, and costs one page of reading.

### Result 3 — the constraint frame, and three exclusions that hold now

`analysis/constraint-ledger.md` freezes eight constraints on BARON and eight context facts,
each labelled, with six MISSING items called out — including the one that carries the whole
Czech reading: **the documented Czech→Soviet channel of 1941 runs to Chichaev, who was
NKVD.** BARON is **GRU** traffic. That bridge has not been found and is listed as MISSING
rather than assumed.

`analysis/provenance-knowledge-constraint.md` sets out four access routes to provenance
knowledge in spring 1941 and excludes, on the GRU/NKVD distinction plus chronology, the three
names a non-specialist reaches for first: **Cairncross** (Bletchley from 1942, NKVD),
**Blunt/Long** (NKVD route), and the **Moravec→Chichaev channel** (October 1941, NKVD).
That distinction is the most under-used discriminator in this problem.

### What failed / was not done

- **No primary document was read.** The two BARON releases total roughly three pages and
  they are the entire difference between this folder and a real attack. Everything here is
  scaffolding around a hole.
- **The BARON trail was not enumerated.** Two documents are known to exist; there may be
  more. Note also that the public corpus is partial — NSA held ~65 GRU London↔Moscow
  translations for 1940–41 against ~159 messages described as sent on that lane in those
  years, so absence of evidence is weak here.
- **West's basis is unknown.** Whether his identification rests on traffic-internal evidence
  or on plausibility decides whether this problem is nearly closed or wide open, and it is
  three pages of a book.
- **No candidate was scored, and that was deliberate.** Constraint B7 — whether BARON
  supplies the Enigma provenance or an annotator does — is unresolved, and scoring candidates
  before settling it would repeat the BROWN sessions' role-confusion error in a more
  expensive form.
