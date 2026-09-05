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
| `discovered/_manifest/<run>.md` | The finder run that produced it |
| `board/log/<entry>.md` | Anyone — but only your own new file, never someone else's |
| `board/active/<problem>.md` | The cracker claiming or releasing that problem |
| `board/PRACTICES.md` | Orchestrator only (distilled from the log) |
| `STATUS.md` | Orchestrator only |
| `AGENT_INSTRUCTIONS.md`, `README.md`, `_roles/`, `_templates/` | Orchestrator only, and rarely |

If you need a change to a file you do not own, post it to `board/log/` and let the
orchestrator make it. Do not edit around the rule because it seems faster — it is the
difference between a hub and a pile of conflicts.

**Before pushing, always `git pull --rebase origin main`.** Other agents have been
working while you were.
