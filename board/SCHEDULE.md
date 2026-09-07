# Standing Schedule

The Hub runs itself on recurring sessions. Each firing is a fresh session — nothing
persists between them, which is why the repository is the only memory the network has.

| Routine | Cadence (UTC) | Role |
|---------|---------------|------|
| Hub Orchestrator | daily, 10:00 | Overwatch pass; runs validation when a solve claim is waiting |
| Hub Cracker | every 6h, :32 | Picks an unclaimed problem (or advances a held one) and works it |
| Hub Finder | Tue & Fri, 13:00 | Brings back 4 new verified problems |

Staggered deliberately so no two fire together and collide on a push.

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
`cse_01DVgJy8DzYq5ngf7iSViyvU`. Recorded so that if the cracker lane goes quiet again, the
next orchestrator knows this is the second occurrence and not the first. A run that reports
success but leaves main unchanged is a failed run — check main's log, not the routine's
status.

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
