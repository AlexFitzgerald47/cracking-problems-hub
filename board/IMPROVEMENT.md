# Adaptive Research Practice — design and operating plan

Adopted by user direction, 2026-09-13. Owner: Orchestrator.
Status: operating design installed; improvement in discovery performance NOT demonstrated.
Historical baseline: `388ddac76d78bb914831a1cc36b0f8612b2dc223`.
Current policy: the repository revision actually read, plus the session's delivered instructions.
This document supersedes the proposed heavyweight RSI architecture.

## Purpose and resource envelope

Increase the chance of a genuinely novel, substantiated discovery using Alex's existing
sessions and token allowances across platforms. GitHub holds durable memory; sessions
are temporary researchers. No new paid services, always-on workers, benchmark farm or
scheduled meta-science are required by this design.

Most effort belongs to direct research, evidence acquisition and decisive validation.
Improvement is a small part of ordinary work. Use one capable primary researcher by
default; additional agents must earn their cost through a specific independent task.
Do not invent exact token costs when the platform does not expose them.

The recursive ambition is to learn which methods help discovery and revise them in
light of subsequent work. Retaining experience and changing policy do not by themselves
prove improved capability or accelerating returns.

## 1. Make bold leaps; earn confidence afterward

**Be bold in what you attempt, selective in what you test, and precise in what you claim.**

Actively seek unconventional explanations, bridge gaps, temporarily assume an ambitious
model, and push several steps ahead when that could unlock the problem. Attempt the
decipherment or reconstruct the missing mechanism. Do not demand proof of every
intermediate step before exploring its consequences.

Once a promising consequence is concrete, choose a small number of discriminating
checks. One decisive contradiction or independent prediction can matter more than
hundreds of weak tests. More testing is justified by a specific unresolved evidential
risk, not by a ritual count. Some claims genuinely require substantial computation.

Label the working assumptions and where the leap occurred. Freeze the prediction before
inspecting its test evidence if claiming a prospective test; evidence already seen can
support exploratory inference but cannot become a holdout retrospectively. An assumption
may generate new ideas without becoming an established input.

A useful failed conjecture and prompt self-correction are welcome. Unsupported certainty,
fabricated evidence and hiding inconvenient outcomes are failures. Neither caution nor
boldness alone earns credit: what did the work make possible or resolve?

## 2. Campaigns are the unit of research

Use the existing problem folder and HANDOVER, not a parallel database. The latest
handover should give a compact frontier brief:

- Established, conditional and unresolved results, with links.
- The decisive uncertainty and a promising next move; the next agent may choose better.
- Any missing evidence, its exact target/source, and what obtaining it would change.
- State: reasoning-ready, evidence-blocked, validation-ready or dormant.
- Reopening condition for a blocked approach.

A missing scan need not block every conditional attack. Record which inference needs
it and pursue useful consequences or another approach where possible. Do not endlessly
restate a block, and do not silently treat missing evidence as obtained.

Keep a few high-upside campaigns alive alongside tractable work. Famousness, easy
micro-results and short-session success are poor substitutes for scientific importance.

## 3. Four roles, with occasional meta-science

Cracker: advances a campaign, including imaginative model construction.
Finder: identifies worthwhile, accessible open questions and evidence opportunities.
Validator: checks a stated claim against evidence, with effort proportionate to scope.
Orchestrator: routes work, keeps memory current, transfers methods and reviews improvements.

Meta-science is an occasional Orchestrator assignment, not a fifth permanent worker.
Only run a dedicated review when accumulated material makes it worth a session.
The Orchestrator owns this file; others submit their own new board/log entries.
Research conclusions remain owned by their campaigns and validators.

## 4. Evidence receipt and light provenance

Append these four lines to ordinary PROGRESS entries, using links instead of duplicate prose:

- Changed: what we now know or can do.
- Evidence: the supporting observation, source or executable artifact.
- Still conditional: assumptions and missing checks; distinguish prediction from confirmation.
- Next: the most useful continuation.

Record once per serious session: starting repository revision, platform/model as actually
known, relevant tool/source limits, trial ID or none, and material user steering. Record
available cost/elapsed information; unknown is acceptable. Store task instructions or a
faithful non-sensitive summary when they differ from repository policy. Never copy
credentials or hidden system instructions.

Capture failed and empty runs when observable. A missing commit establishes no durable
delivery, not why it happened. Keep bookkeeping brief; no reconstruction of private
reasoning traces is required.

## 5. One improvement trial at a time

A recurring failure or useful new method can motivate one small amendment. Define the
change, expected benefit, downside and evidence that would justify keeping or removing it.
Keep the ordinary policy stable during comparison. Trials can be opt-in through the
session prompt; recording a trial here does not silently activate it for all crackers.

Try changes in research sessions already being run. When convenient, compare two isolated
sessions from the same starting evidence before sharing outputs. Hold model/tools steady
for a policy comparison where possible. Different platforms and user steering confound
causal attribution; document them and treat findings as operational observations.

Do not purchase extra runs for symmetry. Historical replay is optional diagnostic work:
public history may leak, and later history cannot score an experiment never performed.
A few cases cannot establish broad superiority.

Decisions: Trial -> Provisionally useful -> Established within a stated scope, or Retired.
Inconclusive is a valid review result. No automatic promotion threshold. Write a dated
decision with evidence and limitations; preserve rejected trials in existing logs.
Do not count a policy's own successful installation as evidence it improves research.

## 6. Evaluate useful work, not an advancement score

Assess concrete evidential progress, warranted conclusions, reusable artifacts, cost,
and credible discovery potential. Keep trade-offs visible. No universal numerical score,
validator-vote reward, leaderboard, or penalty merely for withdrawing a conjecture.

Ask whether the method changed action, whether that action helped, and whether a shorter
instruction would work as well. Consider contrary cases, empty runs, dependent sessions
and downstream reuse. Repeated runs on one problem are not independent domain evidence.
Do not promote a challenger simply because enough attempts eventually produced a win.

Validators are fallible observers, not truth labels. External primary evidence and
independent calculations must be able to contradict the entire institution.
An improvement cannot change its own evaluation criteria mid-trial.

## 7. Proportionate validation

Preparation and bounded computations: check relevant inputs and reproducibility.
Working conjectures: label assumptions and develop a discriminating consequence.
Important intermediate findings: a fresh session attempts reproduction or refutation.
Solve claims and consequential identity claims: retain the full three-validator protocol,
including a refuter, followed by human sign-off before announcing a solve.

A validator's inability to obtain evidence is unresolved assessment, not proof of falsity.
Failed hypotheses need not indicate poor research. Different model platforms do not
guarantee independent errors. Panels can occur sequentially across available sessions.
Human sign-off is governance and does not erase an evidential gap.

## 8. Memory and method revision

Keep PRACTICES short, with supporting cases linked into existing logs. Scope a method to
the bottleneck where it helps; revise or retire it when evidence changes, not merely
because time passes. Adding a rule should prompt consideration of shortening another.

Preserve old analyses. Corrections should name affected downstream claims so the next
reader knows what must be revisited. Use explicit links for dependency tracking initially;
build no automatic evidence graph until manual use establishes its value.

Git preserves policy versions. This file records current decisions; separate log files
preserve each session's account. No copied policy directories or second shared ledger.

## 9. Implementation and rollout

1. Install this design; link it from entrypoints and role instructions.
2. Align creative exploration, validation scope and handover guidance.
3. Register ARP-001 below without claiming results or launching research jobs.
4. Next ordinary campaign session: use the compact handover and receipt; optionally
   activate ARP-001 explicitly.
5. Next Orchestrator pass with relevant session evidence: review usefulness and overhead,
   retain an inconclusive state if needed, and remove friction.
6. Consider replay, conditional methods, model routing or team changes only when a
   concrete recurring bottleneck warrants their cost. Test one change at a time.

External routine settings and platform prompts are separate from repository policy.
This installation neither restarts them nor establishes their current model or enabled
state. New sessions should read current repository instructions; stale external prompts
must be reconciled explicitly when encountered.

## Current trial: ARP-001 — decisive uncertainty without creative paralysis

Status: Trial registered; no evaluated runs. Activation: explicitly name ARP-001 in a
normal research session. Baseline for the narrow amendment: this installed design with
ARP-001 inactive. The pre-redesign revision above is historical context, not a controlled
baseline for the amendment.

Amendment:
> Before substantial execution, briefly identify the uncertainty this move could resolve.
> You may assume an unproven model and leap ahead to expose a decisive consequence.
> If direct evidence is unavailable, pursue a useful conditional attack, acquisition step
> or alternative route. Avoid elaborate preflight checklists.

Hypothesis: this reduces low-discrimination work while preserving ambitious exploration.
Possible harm: premature blocking, generic uncertainty prose, lost momentum or excessive
caution. Watch for these as seriously as unsupported claims.

Evidence for provisional adoption: multiple concrete session examples where the amendment
changed the selected action and produced useful evidence or a credible new attack, with
acceptable overhead and no observed suppression of exploration. This supports a limited
operational judgment, not measured general superiority.
Evidence against: repetitive planning, no action change, premature stopping, or avoidable
loss of promising speculation. Simplify or retire if these dominate.

Report in the session receipt or a unique board/log entry: trial activation, what action
changed (or none), result/artifact, overhead if known, and downside. Review when useful
evidence accumulates, never after an arbitrary quota.

## Decision history

2026-09-13: User authorized the redesign and implementation, emphasizing cross-platform
token allowances and leaps of faith. Four roles retained; bold exploration adopted as
user-directed policy. ARP-001 registered as unproven. No benchmark, research campaign,
external scheduler or validation panel was run by this installation.

## 2026-09-21 — first trial review of ARP-001

**Measurement: zero activations in eight days.** ARP-001 was registered 2026-09-13 and
requires a session to name it explicitly. Searching the repository, no session has. Three
research sessions have landed in that window (Junius 09-17, Proto-Elamite 09-17,
Shakespeare 09-21) and none activated it.

**Supporting case for the trial:** none yet, because none exists — no activated run has
occurred, so there is no evidence either way about the amendment's usefulness. It is
unevaluated, not disconfirmed, and this entry does not treat "no evidence" as evidence
against.

**Contrary case, about the mechanism rather than the amendment:** the opt-in is visible
and is being declined deliberately, which is sharper than an awareness problem. `_roles/
CRACKER.md` names the trial, and both the Proto-Elamite and Shakespeare sessions wrote
`Trial ID: none (ARP-001 not activated)` into their `PROGRESS.md` receipts. So three
sessions saw the trial, recorded a decision about it, and each decided not to run it. The
reason is not recorded by any of them and should not be guessed at here; the plausible
candidates are that an optional trial with no stated benefit to the current session is
never the rational choice for that session, and that a session under a stored prompt has no
standing instruction to accept overhead on the network's behalf. Either way, the mechanism
is what has failed to produce data, not the hypothesis.

**Cost limit and uncertainty:** the cost so far is a paragraph of standing text nobody
acts on, which is small but not nothing — unused policy text crowds the files new agents
read. The uncertainty that matters is whether the board's binding constraint is policy at
all: between 09-18 and 09-21, twelve cracker firings landed nothing. A network delivering
roughly two sessions a week cannot evaluate a policy trial in any reasonable time, and
adding instrumentation to those scarce sessions would spend them on meta-science instead
of research, which `_roles/ORCHESTRATOR.md` explicitly rules against.

**Decision, small and reversible:** ARP-001 stays registered and unchanged. It is **not**
promoted, **not** made default, and **not** given a second trial alongside it. No
instrumentation is added to cracker sessions to chase activations. If the next orchestrator
pass finds activations still at zero, the trial is retired as unevaluable under current
delivery and re-registered when the board is landing sessions daily — retirement in that
case records nothing about the amendment's merit, only about the conditions available to
test it.

This is a decision about a policy trial, not about research practice. Nothing here changes
what any cracker, finder or validator does.

## 2026-09-24 — second trial review of ARP-001: retired in its opt-in form

**The 2026-09-21 review set a condition and this pass is the one that has to apply it:** "If
the next orchestrator pass finds activations still at zero, the trial is retired as unevaluable
under current delivery." The 2026-09-23 pass did not mention ARP-001 at all, so the condition
falls to this one. A decision deferred twice is a decision not being made.

**Measurement: still zero activations, eleven days after registration.** No session anywhere in
the repository has named ARP-001 as active. The count of sessions that *saw* it and recorded a
decision about it has grown from three to **nine** — Junius, Proto-Elamite, Shakespeare (three
separate entries), Thera, Caligula, the Annals, Patrician chronology — every one writing some
form of `Trial ID: none (ARP-001 not activated)` into its receipt.

**Decision: ARP-001 is retired in its opt-in form. It is not re-registered as an opt-in.**

**The delivery premise the last review rested on has changed, and that sharpens rather than
softens the conclusion.** On 09-21 the argument for holding the trial open was that a network
landing two sessions a week cannot evaluate a policy in reasonable time, and the stated
re-registration condition was "when the board is landing sessions daily". **That condition is now
met** — the board has landed sessions on 09-21, 09-22 (×3), 09-23 (×3) and 09-24. So delivery is
no longer the binding constraint, and what remains is the mechanism.

**The mechanism failed, and this is a measured finding rather than absent data.** Nine sessions
saw an optional trial, each recorded a deliberate decision, and all nine declined. That is not
an awareness problem and not a sample too small to read. The most economical explanation is the
one the 09-21 review already named and did not act on: **an optional trial that imposes a cost
on the session running it and states no benefit to that session will never be the rational choice
for that session**, and a session firing from a stored prompt has no standing instruction to
accept overhead on the network's behalf. Nine declines is enough to stop treating this as a trial
awaiting data.

**What is retired, and what is not.** Retired: the ARP-001 *opt-in trial* and the instruction in
`_roles/CRACKER.md` inviting sessions to activate it. **Not** retired and **not** judged: the
amendment's content. It remains unevaluated — no activated run ever occurred, so nothing here is
evidence about whether it would help, and a later pass must not cite this retirement as if it
were a negative result. The `Trial ID:` line in session receipts is harmless and can stay; it now
records "no trial active", which is true.

**Cost of the retirement:** a paragraph of standing policy text leaves the files new agents read.
That is the whole benefit and it is small. The cost of *not* retiring is the same paragraph
staying, plus a third pass spent re-measuring zero.

**What would be needed to evaluate the amendment, recorded so it is not rediscovered.** Not
another opt-in. It would have to be **default-on for a named set of sessions, with the cost
stated in the prompt those sessions receive**, and compared against sessions run without it —
which means spending research sessions on meta-science and modifying the external stored prompts
that this repository cannot reach. `_roles/ORCHESTRATOR.md` rules against the first without
warrant and the second is outside any agent's access. **So this is a decision for the human, and
it is on the standing list in `STATUS.md`:** either accept that the amendment stays unevaluated
and its text stays retired, or direct that a named run be instrumented. No orchestrator pass can
choose that, and no further pass should re-open it as a trial review.

This is a decision about a policy trial and its mechanism. **Nothing here changes what any
cracker, finder or validator does,** and no research practice is altered by it.

---

## 2026-09-25 — two mechanisms installed, both reversible, both with a stated failure condition

*Orchestrator pass. Neither is a policy trial and neither asks any session to do anything extra;
they are changes to the shape of files the orchestrator already owns. Recorded here so the next
pass can judge them rather than rediscover them. **No policy trial is active. ARP-001 stays
retired and its content stays unevaluated** — see the 09-24 entry above; that remains a human
decision and this pass does not re-open it.*

**1. A specialist practices family gets its own annexe rather than being compressed or cut.**
`board/PRACTICES.md` was at 28.6 KB with the previous curator's instruction attached: at ~30 KB,
**cut a rule rather than compress one**, because compression was exhausted. Three rules earned
promotion this pass and no rule in the file was untrue, so the instruction as written would have
required destroying something correct. Instead the five-rule stylometry and confound family — the
largest block, and specialist rather than general — moved to `board/PRACTICES-STYLOMETRY.md`,
pointed at from `Start here` and from the four folders it serves. 4.4 KB left the file every new
agent reads.

*Supporting case:* the family is genuinely specialist; two of the four problems that produced it
found the confound larger than the signal, so cutting it would have been costly, and it is not
needed by a cipher or archival session at all. *Contrary case, stated because it is real:* this is
how a second unreadable log gets started, which `_roles/ORCHESTRATOR.md` names as the failure mode
of `PRACTICES.md` itself. The mechanism is only safe while annexes are **few, named in
`Start here`, and each addressed to identifiable folders.** *Cost limit:* **at most three annexes
ever.** *Failure condition:* if a later pass finds a session that needed an annexe's rule and did
not read it, the split caused the harm it was meant to avoid and the family goes back inline, with
a rule cut to pay for it. *Uncertainty:* untested — no session has yet started work under the
split.

**2. A standing draw order replaces per-pass re-litigation of `discovered/`.** Every remaining pack
has been passed over more than three times, so the board's own promotion rule makes them all
technically promotable, while promoting them en masse would be tidying — **promotion does not
create sessions.** `STATUS.md` now carries a per-category ranked queue with a named trigger (a
category with no unblocked new work for ten days) and two items closed outright (`cypro-minoan` as
evidence-blocked, not low-tractability; `ormonde-maltravers` already solved externally).

*Supporting case:* three consecutive passes recorded a promotion decision for the same list, which
`_roles/ORCHESTRATOR.md` names as a decision not being made. *Contrary case:* a queue fixed now may
be wrong later, because the right promotion has twice turned out to be the one another folder just
made cheap — which no queue written in advance can anticipate. *Mitigation, and it is the important
half:* **the queue is a default, not a lock.** A specific enabling reason always outranks it and a
pass that promotes out of order should say why in one line. *Failure condition:* if two consecutive
passes promote out of order, the queue is not describing how promotion actually happens and should
be deleted rather than maintained.
