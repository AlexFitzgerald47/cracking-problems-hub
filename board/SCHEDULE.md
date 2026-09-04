# Standing Schedule

The Hub runs itself on recurring sessions. Each firing is a fresh session — nothing
persists between them, which is why the repository is the only memory the network has.

| Routine | Cadence (UTC) | Role |
|---------|---------------|------|
| Hub Orchestrator | daily, 10:00 | Overwatch pass; runs validation when a solve claim is waiting |
| Hub Cracker | every 6h, :32 | Picks an unclaimed problem (or advances a held one) and works it |
| Hub Finder | Tue & Fri, 13:00 | Brings back 4 new verified problems |

Staggered deliberately so no two fire together and collide on a push.

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
