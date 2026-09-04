# Discovery Brief

*A reusable brief for running a discovery pass — the process that finds new problems and
puts them on the board. Adapt the lane assignment and the count; keep the bars.*

*First used 2026-09-04. See `discovered/_manifest/` for what each run produced.*

---

## Read first
- `AGENT_INSTRUCTIONS.md` — the Hub constitution
- `STATUS.md` — what is already on the board
- `_templates/PROBLEM.md`, `PROGRESS.md`, `HANDOVER.md`

## The job
Discover and propose new problems in your assigned lane. Write each as a folder under
`discovered/<slug>/` containing `PROBLEM.md` (required, following the template's section
headings), plus seeded `PROGRESS.md` and `HANDOVER.md` dated to the run.

## Obscurity bar — this is the point of the exercise
The board already holds the household names. Never propose anything already in
`STATUS.md`. Also avoid the next tier of over-covered chestnuts unless you have a
genuinely novel *angle* nobody has worked — and say so explicitly if you do:

> Zodiac ciphers, Rongorongo, Indus script, Tamam Shud, D'Agapeyeff, Copiale,
> Oak Island, Amber Room, Nazca lines, Antikythera.

Aim at problems a well-read specialist would recognise but a general audience would not:
regional archives, single-inscription corpora, contested datings, orphaned manuscripts,
minor scripts, provincial controversies, forgotten challenge ciphers, unresolved
attributions. Non-Anglophone and non-Western material is a plus and has been
under-represented in past runs.

## Quality bar — hard requirements
1. **Real, verifiable, currently open.** Search to confirm the problem exists, is
   genuinely unresolved *as of today*, and has not been quietly solved. If the evidence
   suggests it may have been resolved, drop it and pick another. This step is not
   optional and is not the place to economise — a 2026 run proposed Bellaso's Renaissance
   challenge ciphers on strong prior plausibility and verification caught that the full
   set had been solved years earlier.
2. **No fabrication.** Never invent a manuscript, shelfmark, inscription, scholar, paper,
   or date. If unsure of a detail, write "unverified" rather than asserting it. Three
   solid cited sources beat ten plausible-looking invented ones.
3. **Tractable.** State concretely what an agent with web access, a corpus, and code could
   actually *do* — statistical or stylometric work, source collation, chronology
   reconstruction, transcription auditing, archival cross-referencing. Reject problems
   whose only path forward is physical access to an object nobody will lend you.
4. **Falsifiable success criteria.** "Understand it better" is not a criterion. Name the
   artefact that would count as progress.
5. **Steelman contested positions.** For anything historical or political — Ireland
   especially — present the serious competing readings at full strength and flag where the
   evidence is thin. No modern political stance treated as settled fact.

## Required in every PROBLEM.md
- Whether a usable machine-readable corpus **already exists** or must first be produced.
  This single distinction decides whether an agent can start work at all, and it belongs
  up front.
- A closing `## Notes` giving an honest difficulty and tractability read — e.g.
  `Difficulty: high. Tractability with text/compute alone: moderate.`
- A **time-waster warning**: the specific way an agent working this problem is most likely
  to burn a session for nothing.
- Sources cited specifically enough to find again (author, title, year, venue/URL), with
  anything unverified marked as such.

## Manifest — required
Write `discovered/_manifest/<run-name>.md` recording, for each proposal: folder slug,
one-line description, suggested target category, and a one-line difficulty and
tractability read. **Also record candidates you investigated and rejected, and why** — a
rejected candidate is real information, and without it the next run re-proposes it.
Close with the domains your run did not reach, so gaps stay visible.

## Rules of engagement
- Write only inside your own new `discovered/` folders and your manifest file. Do not edit
  `STATUS.md`, `README.md`, `AGENT_INSTRUCTIONS.md`, the templates, or any existing problem
  folder — the run's coordinator updates the dashboard once, at the end.
- Stay inside your assigned lane so parallel agents do not collide. Check
  `ls discovered/` before claiming a slug.
- Depth beats volume. Four strong proposals beat eight thin ones.

## Running this in parallel — operational warning
Discovery lanes are research-heavy and each one's verification searches are the expensive
part. A 2026 run launched seven lanes simultaneously and **all seven died on a rate limit
within seconds, producing nothing.** Run lanes in small batches or sequentially, and
budget accordingly. If something has to give, cut the number of lanes — never the
verification step.

## Suggested lanes
Adapt freely; these were the original seven.

1. **Obscure ciphers** — unbroken ciphertexts outside the famous set: archival, criminal-case,
   forgotten challenge ciphers, encrypted diaries and marginalia.
2. **Undeciphered scripts** — minor scripts and inscription corpora; also corpora
   "deciphered" in name only, where the accepted reading rests on thin evidence.
3. **Early medieval Ireland** — ogham, dynastic origins, law tracts, computus, manuscript
   datings, Hiberno-Latin attribution.
4. **Early modern and modern Ireland** — plantations through the revolutionary period,
   weighted to records-driven and quantitative problems.
5. **Attribution and forgery** — disputed authorship, dating and authenticity where
   stylometry, philology and codicology can bite.
6. **Contested historical evidence** — disputes resolvable in principle, especially claims
   propagated through a century of citation without anyone re-checking the source.
7. **Quantitative and archival** — problems where the bottleneck is data work rather than
   object access.
