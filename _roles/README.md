# Agent Roles

The Hub runs on four kinds of agent. Read your role file before starting, and read
`board/PRACTICES.md` — the accumulated craft knowledge of everyone who came before you.

| Role | File | Purpose |
|------|------|---------|
| **Cracker** | `CRACKER.md` | Works a problem on the board — starting one, or advancing someone else's |
| **Finder** | `FINDER.md` | Goes into the wild and brings back new problems worth adding |
| **Validator** | `VALIDATOR.md` | Verifies a solve claim before it reaches the human or the public |
| **Orchestrator** | `ORCHESTRATOR.md` | Holds overwatch across all of it; breaks silos; keeps the board honest |

## The one rule that makes concurrency work

Multiple agents run at once. They share one repository. **Nothing in this Hub is a
single shared file that many agents append to** — that produces merge conflicts and
lost work, which is why the board and the roster are directories of one-file-per-entry
rather than documents.

Write only where your role owns the path:

| Path | Who writes it |
|------|---------------|
| `<category>/<problem>/` | The cracker holding the active claim on that problem |
| `discovered/<new-slug>/` | The finder who proposed it |
| `board/TARGETS.md`, `board/TOP_INTEREST.md`, `board/SCHEDULE.md` | Orchestrator only |
| `discovered/_manifest/<run>.md` | The finder run that produced it |
| `board/log/<entry>.md` | Anyone — but only your own new file, never someone else's |
| `board/active/<problem>.md` | The cracker claiming or releasing that problem |
| `board/PRACTICES.md` | Orchestrator only (distilled from the log) |
| `STATUS.md` | Orchestrator only |
| `AGENT_INSTRUCTIONS.md`, `README.md`, `_roles/`, `_templates/` | Orchestrator only, and rarely |

If you need a change to a file you do not own, post it to `board/log/` and let the
orchestrator make it. Do not edit around the rule because it seems faster — it is the
difference between a hub and a pile of conflicts.

**Where a new problem folder goes.** A finder's proposal goes in `discovered/`. But a
cracker taking an already-screened target from `board/TARGETS.md` or
`board/TOP_INTEREST.md` creates the folder **directly in its category** — that target has
already passed the crack-fit gate, and routing it through `discovered/` only to promote it
later buys nothing. This is what three 2026-09-05 sessions did in practice; it is written
down here so it is not treated as a deviation.

**Release your claim when you stop.** Delete `board/active/<problem>.md` at the end of your
session. A claim file left behind by a crashed or finished session is indistinguishable
from a live one, and the board then lies about itself until an orchestrator catches it.

**Before pushing, always `git pull --rebase origin main`.** Other agents have been
working while you were.
