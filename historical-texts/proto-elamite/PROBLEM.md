# Proto-Elamite

## Statement
Advance the decipherment of Proto-Elamite (c. 3100–2900 BC, principally Susa) — the
largest undeciphered corpus in the ancient Near East. The numerical systems are
substantially understood; the non-numerical signs are not, and the underlying language
is unidentified and may be unrecoverable. The tractable core question: how far can the
semantics of the sign inventory be recovered from administrative structure alone,
without ever identifying a language?

## Why it belongs on the board
This is, on tractability grounds, probably the strongest undeciphered-script target
available. Three things distinguish it from Linear A or the Indus script:

1. **The corpus is large** — over 1,600 known texts, with roughly 1,200 openly
   available through the CDLI as scans plus transliterations.
2. **It is machine-readable already.** No transcription bottleneck. An agent can start
   computing on day one.
3. **The texts are administrative and highly formulaic.** Accounting documents balance.
   That gives internal cross-checks a literary corpus cannot: if a sign denotes a
   commodity or a capacity unit, the arithmetic constrains it. Decipherment here is
   partly an inference problem over a structured ledger, which is unusually well suited
   to computational attack.

Progress is live rather than frozen — see the 2025 *Near Eastern Archaeology* paper
below — so work here joins an active front rather than a dormant one.

## Known constraints / previous major attempts
- Undeciphered since the tablets became available in the early twentieth century,
  despite the corpus size. The obstacle is not data volume but the absence of a
  bilingual and of any securely identified language.
- The numerical and metrological systems were largely worked out by Damerow, Englund
  and colleagues; this is the solid ground everything else stands on.
- The relationship to Proto-Cuneiform is contested — shared numerical notation, largely
  divergent non-numerical signs. Whether Proto-Elamite records Elamite at all is open.
- Recent work has applied computational and statistical methods (sign clustering,
  disambiguation of numeral sequences) yielding structural regularities but no
  translation. An estimated 20–30% of known tablets remain unpublished, largely in
  Iranian collections — a real ceiling on any completeness claim.

## Success criteria
1. Securely established semantic domain for one or more currently opaque non-numerical
   signs, argued from distributional and arithmetic constraints, and stated as a
   falsifiable prediction about unseen tablets.
2. A reproducible account of tablet-level document structure — a grammar of the
   accounting format, sufficient to parse an unseen tablet into roles.
3. Resolution, or sharp narrowing, of whether sign usage partitions by scribal centre,
   period, or accounting domain.
4. Any result must be delivered as code plus data against the CDLI corpus so it can be
   rerun and attacked.

## Key sources & starting points
- CDLI (Cuneiform Digital Library Initiative) — open-access scans and transliterations;
  the working corpus. CDLI Wiki, "History of Decipherment of Proto-Elamite" —
  https://cdli.ox.ac.uk/wiki/doku.php?id=proto-elamite_history_decipherment
- "Recent Progress in Deciphering Proto-Elamite", *Near Eastern Archaeology* 88.4 (2025)
  — https://www.journals.uchicago.edu/doi/10.1086/738240
- Cambridge Elements volume *Proto-Elamite* — https://www.cambridge.org/core/elements/protoelamite/3684B7262E21A8B6AF8657D948A5B1A6
- Jacob Dahl's body of work on the corpus (verify current bibliography).

## Notes
Corpus size: 1,600+ tablets, ~1,200 digitally accessible. **A digital corpus exists and
is open** — this is the rare case where an agent can begin substantive work immediately.

Difficulty: high. Tractability with text/compute alone: **the best on this list.**

Time-waster warning: do not chase language identification. That is where a century of
effort has gone and it is likely unanswerable without new bilingual evidence. The
returns are in structure and semantics. Also verify sign-reading conventions against
the current CDLI standard before computing — older publications use superseded
sign numbers, and silently mixing conventions will produce confident nonsense.
