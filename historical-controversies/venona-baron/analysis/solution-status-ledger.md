# Solution-status ledger — is BARON already identified?

*Opened 2026-09-07. Read `access-ledger.md` first: no claim below is `[PRIMARY]`.*

`board/PRACTICES.md` requires a solution-status audit before a target is worked, because
this board has already been burned once: the frontier-model pass proposed DAN as an
unresolved London covername on the strength of a cable footnote reading "unidentified",
and the Vassiliev concordance had identified DAN as Stanley Graze all along. **BARON is a
near miss on the same failure mode**, and the audit should have been run before it was
ranked number one for Dominic.

## The finding

An identification of BARON is in print, and in the standard reference index.

| Claim | Status | Source |
|---|---|---|
| Nigel West, *VENONA: The Greatest Secret of the Cold War* (1999), pp. 67–69, identifies BARON as **Karel Sedláček** | `[SEARCH]` | West 1999, cited by page in indexed discussion |
| John Earl Haynes's cover-name concordance carries `"Baron": Sedlacek, Karel (U.K. line, [West Venona])` | `[SEARCH]` | johnearlhaynes.org/page66.html |
| The bracketed `[West Venona]` marks the attribution as **West's**, not an archival identification | `[INFERRED]` | Haynes's convention: bracketed tags name the source of an identification |
| A secondary account renders it hedged — BARON was "probably" Sedláček | `[SEARCH]` | indexed secondary discussion |
| An unnamed MI5 officer said in 1997 that **no serious attempt had been made to identify BARON** | `[SEARCH]` | quoted in indexed secondary discussion; original not located |
| NSA/VENONA annotation describes BARON as an unidentified agent who "apparently reported information obtained from U.K. decryption of German Enigma messages" | `[HUB]` + `[SEARCH]` | NSA *The Venona Story*; Hub frontier-pass manifest |

## Why the last two rows do not contradict each other

VENONA translator footnotes were **written once and rarely revised**. Indexed discussion of
the corpus notes explicitly that one translation may footnote a covername as unidentified
while another footnotes the same covername with an identification, because analysts seldom
went back to hand-correct an earlier footnote when a later identification landed. `[SEARCH]`

Generalised, this is the rule the board should have been using and was not:

> **A VENONA footnote reading "unidentified" records the state of knowledge at the moment
> that particular translation was typed. It is evidence about the annotator, not about the
> historiography. It is never a solution-status check.**

Posted to `board/log/2026-09-07-venona-baron-opened.md` for the orchestrator, because it
generalises past this problem to every remaining covername target on the Dominic list.

## Why the problem nevertheless survives

The Sedláček identification is not safe, and it fails a constraint that can be stated
without reading a single cable.

**The geography problem.** Karel Sedláček was a Czechoslovak military-intelligence officer
**resident in Switzerland**, not Britain, across the whole relevant period. Uneasy in Zurich
by spring 1939 because the city was full of German agents, he moved to **Lucerne**, where
Roessler lived; from **September 1939** he reported by wireless to the Czechs in London, his
material coming from Hausamann and ultimately from Roessler. SIS later gave him a false
British passport as "Charles Simpson"; he also used the alias Selzinger, and Alexander Foote
misidentified him under that alias as "Lucy" in *Handbook for Spies*. `[SEARCH]`

That produces a specific tension with the Haynes entry, which files BARON under the
**U.K. line**. A source physically in Lucerne, whose product is *German* operational
intelligence, is an awkward fit for a London-residency source reporting on **British**
cryptanalytic activity. Two ways out, both testable:

- **Relay.** BARON's reports reached the GRU through the Czech station in London, and the
  residency covernamed the ultimate originator rather than the person who handed the paper
  over. Then the GRU's *access* is to Czechoslovak military intelligence in London, and the
  person who matters for the Enigma provenance is not Sedláček.
- **Misattribution.** West assigned an unusually multi-service figure to an unusually
  Czech-flavoured covername on the strength of fit rather than traffic. The annotator's
  "possible connection with Military Intelligence" note would then be a coincidence that
  made the fit look better than it is — Czechoslovak military intelligence is also
  "Military Intelligence", and so is MI14.

**The direction problem.** Sedláček's established product flowed *from* central Europe *to*
London. A report about British decryption of German traffic flows the other way. Nothing in
the established biography supplies him with knowledge of British Ultra provenance.
`[INFERRED]`

**One real point in West's favour, stated fairly.** Sedláček is documented as dealing
simultaneously with the Swiss, the Czechs, the Soviets and the British — a man with a
Soviet channel already in place, and one whose service is literally "Military Intelligence".
Whatever else is true, he is not an arbitrary candidate.

## Verdict

**BARON is not solved, and it is not virgin either.** The correct scoping is *adjudicate a
standing named hypothesis*, and the first two moves are (1) read West pp. 67–69 to find out
what the identification rests on, and (2) read the two released BARON documents. If West's
identification turns out to rest on traffic-internal evidence — a Swiss dateline, a Czech
referent, a linking covername — the problem may close quickly, and reporting that is a
perfectly good outcome. If it rests on plausibility, the problem is wide open and the
candidate frame in `provenance-knowledge-constraint.md` applies.

**Do not demote this target and do not treat it as solved.** Record it as *contested; one
named hypothesis standing, untested.*
