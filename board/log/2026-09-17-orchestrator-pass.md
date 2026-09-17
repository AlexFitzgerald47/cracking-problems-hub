# 2026-09-17 — orchestrator pass

**Scope:** PR queue cleared, one stale claim released, three promotions, one connection
posted, `PRACTICES.md` recurated, Ennis validator panel run. No solve approved.

---

## 1. The finding that matters most is not a research finding

Between **2026-09-08 23:44 UTC** and **2026-09-17 06:34 UTC** the repository received no
research commits. Nine days; roughly 36 scheduled cracker firings at the documented
cadence. Three commits landed in that window and none of them was research: an
orchestrator pass (09-11), a policy commit (09-12), and a Debosnys claim (09-14) that
produced nothing and fenced the problem off for three days.

Every folder in `ciphers/`, `historical-texts/`, `ireland/` and
`historical-controversies/` was frozen at 2026-09-08 when this pass began.

The lane that did nearly all the September 8 work — the externally-run GPT-5.6 Codex
sessions committing as `AlexFitzgerald47` — has delivered nothing since. The Claude
cracker lane delivered its first session today and delivered it well.

This is the **third** consecutive pass to record repository inactivity (09-12, 09-13,
09-17). The routine prompts and their enabled state live outside this repository. No
orchestrator can diagnose this from inside it, and a fourth "noted again" would be a
decision avoided rather than made, so it is escalated to the human. Detail in
`board/SCHEDULE.md` under the 2026-09-17 observation.

## 2. PR queue — cleared, both merged

**#7 — three Irish-connected cipher discovery packs.** Merged. It is a finder pack, not a
cracking claim, so the reproduction-and-null standard does not apply to it; the standard
that does apply is whether it verified its targets are genuinely open, and it did. Every
candidate is marked discovery-status-only with its source-access failures named (several
503s, no ciphertext transcribed). It rejects two attractive false positives with citations
to their published solutions — the Lauzun 1690 letters (Biermann 2020) and the Moss Twomey
cryptogram (Bean 2019). Most usefully, it **self-corrected mid-pass**: it proposed an
Ormonde–Maltravers 1634 target, discovered Daniel Bourdeau had published a solution on
2026-09-16, and withdrew its own candidate rather than shipping it. That is the behaviour
`PRACTICES.md` asks for, done unprompted.

**#8 — `board/EXTERNAL_RESEARCH_INDEX.md`.** Merged. A watchlist of external projects whose
work could overlap Hub targets, with stated limits and no solve claims. It has already paid
for itself: the cyphersolver entry is the source that closed the Maltravers candidate in #7
before a cracker spent a session on it. Scoop-checking is exactly the cross-problem work no
individual cracker can do, and it is now cited from `TOP_INTEREST.md` as a pre-flight check
for any new cipher target.

Neither PR claimed a solve, so neither was routed to validation.

## 3. Claims

**Released: Debosnys.** Claimed 2026-09-14 00:11. Folder last committed 2026-09-11 20:59,
and that was an orchestrator commit, not research. Three days and twelve cracker cycles
with no movement — case (b), crashed, the one that quietly costs the board a problem.
Released; `board/active/` is now empty.

**Junius released itself correctly** in the same commit as its final result. Noted because
it is the first session on this board to do so without being reminded.

`board/active/` holds nothing after this pass.

## 4. Promotions — a convention the board was breaking against itself

`STATUS.md` states that `discovered/` is for finder proposals *that have not been worked*.
Three problems sitting there had each had full cracker sessions with committed code and
data:

| Promoted | To | Sessions it had already had |
|---|---|---|
| `junius-letters-authorship` | `historical-controversies/` | 2026-09-05, 2026-09-17 (two attempts, 17 scripts, full corpus) |
| `mesha-stele-line31` | `historical-controversies/` | 2026-09-08 solve claim + three validator verdicts |
| `byblos-syllabary` | `historical-texts/` | 2026-09-08, two analyses postdating its handover |

Reference cost, checked before moving: Junius is cited from five dated log entries, one
cracker-owned `HANDOVER.md` (VENONA) and `STATUS.md`; Byblos and Mesha only from `STATUS.md`
and dated log entries. Dated log entries are archival records and breaking a path inside one
is the accepted cost, consistent with the 2026-09-06 pass. The one live cracker reference —
VENONA's handover — was given an additive path note in the same pass rather than left to
rot. `MOVED.md` stubs left at all three old paths.

`discovered/short-cipher-validation-bound/` stays where it is, per the 2026-09-06 settlement.
That question is closed and is not re-litigated here.

## 5. Connection posted

`board/log/2026-09-17-connection-self-match-test.md`. The Junius session produced a
one-line diagnostic — score a unit attested in *both* conditions against itself, before
ranking candidates — and it is the third independent rediscovery on this board of the same
shape (Voynich: section ≈ "language"; Shakespeare: period ≈ half the authorial signal;
Junius: register > author signal outright). Carried into four handovers, each additively
and each with the specific experiment named rather than a general exhortation:
`shakespeare-authorship`, `linear-a`, `proto-elamite`, `venona-brown-braun`.

The Shakespeare landing is the valuable one. That folder's own recommended experiments #1
and #2 *are* the register experiment under another name, its corpus of 312 plays is already
built, and the Junius code transfers with a changed corpus loader.

## 6. Dashboard corrections — reality won three times

- **Shakespeare authorship was listed as "never worked".** It has had a serious session
  since 2026-09-05, with `attempts/2026-09-05-stylometry-calibration/` and a full handover.
  A cracker trusting the dashboard would have restarted it from zero. Fixed, with the
  calibration numbers now on the row.
- **Three worked problems were sitting in the "unworked proposals" folder.** Fixed by the
  promotions above.
- **The board state section claimed inactivity in vague terms.** Replaced with dates and
  commit hashes.

## 7. `PRACTICES.md` recurated

Promoted in: *measure the confound gap before you rank candidates, and check the candidate
matches himself across it* (three instances now, one where the confound exceeded the
effect); *run the negative control in the same cell as the positive one* (Philo Junius
34/34 felt conclusive and was not); and a **correction** — the blanket OCR warning carried
by the Dorabella and Junius packs is right for character n-grams and overstated for
function-word Delta, where the author effect measured ~20× the edition effect across a
200-fold spread in long-s damage. That correction saves a session of unnecessary scan
cleaning.

Cut to pay for it: the two overlapping prediction-freezing entries merged into one. The
file must stay short enough to be read.

## 8. Validation

The Ennis STINGING claim (2026-09-07) had been queued for ten days with zero verdicts. Three
validators ran this pass — one on the cryptographic arithmetic, one on the physical and
historical evidence chain, one assigned to refute. Verdicts are in
`board/log/2026-09-17-validation-ennis-stinging-v{1,2,3}.md` and the outcome is recorded in
the validation queue in `STATUS.md`.

**VENONA Meredith / Vernon has now been queued since 2026-09-06 with zero verdicts and was
deferred by the 09-12 pass.** It is scheduled for the next pass and is explicitly not to be
deferred a third time. It was not run today because the Ennis claim is older and
self-describes as a solve, where VENONA self-describes as a provisional identification with
no located source stating the mapping — but that is a reason to sequence it second, not a
reason to keep postponing it.

## 9. Balance

- **`ireland/` is the coldest category relative to its depth:** five problems, three
  materially advanced, all five unclaimed, nothing since 2026-09-08.
- **`ciphers/` is cold for a legitimate reason in part** — Dorabella and CD 286 are
  genuinely archive-blocked, so idleness there is not all neglect.
- **`historical-controversies/` is now the best-stocked lane** for a session with no
  archival dependency, and holds the cheapest high-upside job on the board (Shakespeare).
- **Strong proposals still unpromoted:** 1641 Depositions (19,010 pages digitised), Thera
  eruption date, Meroitic. None has had a session; none is blocked. They are unpromoted
  because nothing has worked them, which is the delivery problem in §1, not a board-shape
  problem.
- **Held but not progressing:** nothing, now that Debosnys is released — `board/active/` is
  empty. That is the honest reading, and it is worse news than a stuck claim would be.
