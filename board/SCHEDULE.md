# Standing Schedule

The Hub runs itself on recurring sessions. Each firing is a fresh session — nothing
persists between them, which is why the repository is the only memory the network has.

| Routine | Cadence (UTC) | Role |
|---------|---------------|------|
| Hub Orchestrator | daily, 10:00 | Overwatch pass; runs validation when a solve claim is waiting |
| Hub Cracker | every 6h, :32 | Picks an unclaimed problem (or advances a held one) and works it |
| Hub Finder | Tue & Fri, 13:00 | Brings back 4 new verified problems |

Staggered deliberately so no two fire together and collide on a push.

## Models

| Routine | Model | Why |
|---------|-------|-----|
| Hub Cracker | `claude-opus-5` (pinned 2026-09-07) | Cracker seats are frontier-model seats. See `_roles/CRACKER.md` |
| Hub Orchestrator | `claude-opus-5` (pinned 2026-09-07) | It spawns the three validators, and refuting a named-person identification from raw evidence is the highest-stakes reasoning the board does |
| Hub Finder | environment default | Not pinned. It already delegates to Sonnet researchers and verifies their work itself; raise it if a verification miss ever gets through |

Researchers and fan-out subagents stay cheap deliberately — Sonnet is the right tool for
searching, retrieval and corpus gathering. The split is strict: delegate the looking,
never the judging.

Before these were pinned, every routine ran on the environment default, which served
Sonnet 5. The Debosnys, Moynagh Lough, Hunt Museum and VENONA work in this repository was
done by GPT-5.6 Codex sessions the human runs separately; those are not configured from
here, and the standard in `_roles/CRACKER.md` is what reaches them.

## Changes to the routine prompts

The routine prompts live outside this repository, so a future agent cannot read them.
Record changes here or they are lost.

**2026-09-07 — the three-day claim rule was removed from the cracker and orchestrator
prompts.** Both previously said a claim was live until it was ~3 days old. Sessions here
last minutes to a couple of hours, so that rule let a *crashed* session fence off a problem
for three days — which is exactly what happened to Caligula's Seashells on 2026-09-05, and
crackers were correctly obeying an instruction that made it worse. Both prompts now judge a
claim by `git log -1 -- <problem folder>`: dead after two cracker cycles (12h), crashed if
the folder never moved at all, live only if committed to within the last cycle. This
matches the rule in `_roles/ORCHESTRATOR.md`. The cracker prompt also now says explicitly
that `HANDOVER.md` is not covered by analysis files, and that a session ending without a
commit has produced nothing.

## Known operational failures

**2026-09-06 18:32 UTC — a cracker firing produced nothing.** The routine reported SUCCEEDED
after twelve minutes and ~154k tokens, and pushed no commit. `board/active/` was empty at
the time, so nothing blocked it from claiming work. Cause unknown; the session record is
`cse_01DVgJy8DzYq5ngf7iSViyvU`. A run that reports success but leaves main unchanged is a
failed run — check main's log, not the routine's status.

*Not repeated:* the next firing at 2026-09-07 00:32, under the revised prompt, worked
VENONA and pushed the Meredith provisional identification. One isolated no-op, not a broken
lane. If it happens again, that is the second occurrence and worth chasing.

## What this means if you are an agent reading this

You are one firing of one of these. You are not supervised in real time and nobody will
catch your mistake before it lands. Two consequences:

**Write down what you learned.** The next session inherits nothing but the repository. An
insight you did not commit is an insight the network never had.

**Do not overstate.** An unattended agent's confident error propagates into every session
that reads it afterwards. "Unverified", "this failed", and "I could not reproduce this"
are the most valuable things you can write, because they are the ones nobody else will
correct for you.

## For the human

The orchestrator reports after each pass and sends a notification when something needs a
decision. Validated solve claims are **held** and never published without sign-off —
see `_roles/VALIDATOR.md` for why three passes are not enough on their own.

To pause everything, disable the routines from the claude.ai Routines view. Disabling
costs nothing and loses nothing; the board simply stops advancing until you re-enable it.


## 2026-09-12 repository observation

At this pass, the latest research commit was 2026-09-09 03:44 UTC (`2a29cf1`). The documented cadence therefore is not evidence of current delivery. External Claude routines were not inspected or changed; their enabled state and failure cause remain unknown. This manually requested orchestrator pass does not restart or duplicate those routines.

## 2026-09-13 operating-design installation

`board/IMPROVEMENT.md` and revised roles define the lightweight research design.
No external routine configuration was inspected, changed or restarted by this installation.
The cadence/model tables above remain historical configuration records, not confirmation
of live execution. Read current repository instructions in each session; record material
differences in delivered external prompts. ARP-001 requires explicit session activation.
No new recurring meta-science task is created.

## 2026-09-17 observation — the nine-day delivery gap, escalated

Measured this pass, not inferred: the last research commit before today was
**2026-09-08 23:44 UTC** (`Debosnys: add frozen XP outward test script`). The next was
**2026-09-17 06:34 UTC** (the Claude cracker claiming Junius). In the nine days between,
the repository received exactly three commits — an orchestrator pass (09-11), a policy
commit (09-12), and a Debosnys claim (09-14) that produced no research and left a stale
claim fencing the problem until this pass released it.

At the documented cracker cadence of every six hours that window should have contained
roughly 36 firings. Every category folder was frozen at 2026-09-08 throughout.

The split is clean and worth stating precisely: the sessions that commit as
`AlexFitzgerald47` (the externally-run GPT-5.6 Codex lane, which did nearly all the
September 8 work) have delivered nothing since 2026-09-08. The sessions that commit as
`Claude` delivered their first full cracker session on 2026-09-17, and it was good work.

**This is the third consecutive pass to record repository inactivity** (2026-09-12,
2026-09-13, 2026-09-17). The routine prompts and their enabled/failed state live outside
this repository, so no orchestrator can diagnose or fix this from inside it, and recording
it a fourth time would be a decision avoided rather than made. It is escalated to the human
as a decision. The two candidate explanations an orchestrator cannot distinguish from here
are (a) the external routines are disabled, erroring or rate-limited, and (b) they are
firing and producing nothing, as the 2026-09-06 18:32 failure above did. Checking the
claude.ai Routines view and the external scheduler's run history distinguishes them in a
minute; nothing in the repository can.

## 2026-09-21 observation — the gap is no longer confined to one lane

Measured this pass from `git log` on `main`, not inferred from routine status.

Since the 2026-09-17 orchestrator pass, research commits landed in exactly two windows:

| Window | What landed |
|---|---|
| 2026-09-17 18:33–18:47 | Proto-Elamite face-confound audit (Claude cracker) |
| 2026-09-21 06:33–07:01 | Shakespeare period-detrend / equal-N session (Claude cracker) |

Against the documented cadence, that leaves:

- **Cracker (every 6h, :32)** — twelve firings between 09-18 06:32 and 09-21 00:32 inclusive
  with no commit of any kind.
- **Orchestrator (daily, 10:00)** — no commit on 09-18, 09-19 or 09-20. Three passes.
  The 09-17 and 09-21 passes both landed. This is the **first time the orchestrator lane
  itself shows the gap**, and it is the reason this entry exists: the 09-17 escalation
  described a cracker-lane and Codex-lane problem, and that description is now too narrow.
- **Finder (Tue & Fri, 13:00)** — nothing landed from the Friday 09-18 firing; `discovered/`
  gained no pack between 09-17 and this pass.
- **GPT-5.6 Codex lane (`AlexFitzgerald47`)** — no research commit since **2026-09-08**,
  thirteen days. Last activity of any kind was merging two finder PRs on 09-17. The PR
  queue is empty at this pass, so it is not contributing by that route either.

One firing did produce a commit without producing work: **2026-09-18 00:33**, which wrote
`board/active/shakespeare-authorship.md` and nothing else. The 2026-09-21 cracker detected
it correctly by the folder rule, said so in its commit message, and retook the claim. The
2026-09-07 claim-rule change is doing its job; that failure cost the board three days of one
problem instead of fencing it off indefinitely.

**What an agent can and cannot conclude from this.** `main`'s log is the only evidence
available from inside the repository. It shows that firings are not landing commits. It
cannot distinguish between a routine that is disabled, a routine that fires and errors, a
routine that fires and produces a session that ends without committing, and a scheduler
that is not firing at all. The 2026-09-06 known operational failure above is the documented
precedent for the third of those, and it was a single isolated occurrence; what is happening
now is not isolated.

Because the silence now spans three different routines with three different prompts and two
different models, a prompt-level cause is the least likely explanation, and the repository
cannot investigate the others. This remains a **decision for the human**, unchanged in
substance from 2026-09-17 and not re-litigated here: check whether the routines are enabled
and what their run history shows.
