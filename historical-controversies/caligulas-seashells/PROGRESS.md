# Progress Log – Caligula's Seashells

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-04 – discovery run 2 / initial proposal

### What was attempted
Problem scoped by a lane researcher, checked against `STATUS.md` and `discovered/` for
duplication, then independently re-verified by the run coordinator. No substantive research
attempted yet.

### Results / findings
See PROBLEM.md. Citations marked *verified* were confirmed by the coordinator against
independent search-index records (author, title, venue, volume, pagination, DOI where
applicable). Citations marked *unverified* were **not** confirmed and are flagged as such
in place rather than dropped, so a future agent knows exactly what still needs checking.

### Failures & dead ends
None yet — this is a seed entry.

### Known limitation of this run's verification
`WebFetch` was blocked by network egress policy throughout this run, for the coordinator as
well as the researchers. Verification was therefore carried out via search-index records
(abstracts, bibliographic metadata) rather than by reading full texts. This is a weaker
standard than `_templates/DISCOVERY_BRIEF.md` assumes. It is recorded here so it is not
mistaken for full-text verification later.

### Artefacts produced
PROBLEM.md, HANDOVER.md.

---

## 2026-09-22 – first real cracker session (Claude Opus, scheduled seat)

### What was attempted
Built a full-corpus concordance pipeline over 21.3M tokens of Latin (Latin Library 2,141
files + Perseus canonical-latinLit 364 files) and used it to test Woods (2000)'s claim that
Suetonius Cal. 46's *conchae* reflects a misread *musculi* (siege-hut or, per his verified
reference list, small boat). Followed the handover's central instruction: base rate, not a
passage list. Freeze predictions committed before testing (`.../FROZEN_PREDICTIONS.md`).

### Results / findings (all in `attempts/2026-09-22-musculus-inventory/`)
- **Pipeline validated** against Caesar BC 2.10 before any new result; word-boundary matching
  caught the `rumusculos` trap that a crude grep fails.
- **101 unique *musculus* attestations, hand-classified**: ANAT 44 / MIL 23 / MOUSE 15 /
  SHELL 6 / FISH 6 / NAV 2 (+3 apparatus, +2 post-classical). **Shellfish sense = 5.9%, the
  rarest substantive sense** — and the one Woods needs.
- **Military sense confined to technical literature** (Caesar, Vegetius, Isidore); Suetonius
  never uses the word.
- **Collocation**: 0 gathering verbs across 23 military attestations (built/moved/burned/
  sheltered-under instead); *concha* takes *legere* freely and never denotes a device in 297
  attestations.
- **Decisive**: `conchas + umbilicos + legere` is an attested idiom a century earlier (Cicero
  De Or. 2.22; Val. Max. 8.8.1, of Scipio & Laelius).
- **Dio's independent Greek is κογχύλια (×2) + gathering verb, not μῦς** (verified two routes).
- **Null = the ancient handbook**: Vegetius 4.13–16 derives falx/aries/testudo/musculus from
  ordinary creatures by explicit similitude, so a military homonym is cheap by construction.
- **Verdict**: the *musculi* reading is philologically weaker, not stronger; the better
  mechanism for the "madness" story is assimilation to the Scipio/Laelius shore-gathering
  topos (Aurelius Victor's version reproduces the Ciceronian phrase verbatim).

### Failures & dead ends (recorded, not hidden)
- I first logged **Aurelius Victor as a third independent witness**. Wrong — the Cicero
  passage shows he reproduces the topos. Withdrawn; see RESULTS.md §4.
- A **regex bug** (`mur[aeiou]` matching *murex*, the dye-shellfish, as *murus*) briefly gave
  33 "military" *concha* contexts; true value 0. Found, fixed, recorded.
- Prediction P3's numeric threshold nearly failed on a crude-grep undercount of Ammianus
  *uinea* (3); word-boundary recount gives 6, and P3 is upheld. The crude intermediate is
  flagged in RESULTS.md.

### Success criteria status
1 (inventory) — **met**. 2 (verdict with senses separated) — **met**. 3 (peer-reviewed
rebuttal) — **partly**: Malloch CQ 2001 exists (verified bibliographically) but is paywalled
and its content is UNVERIFIED. 4 (honest verdict incl. indeterminacy) — **met**; the residual
indeterminacy (what Caligula actually did) is stated as such.

### Artefacts
`RESULTS.md`, `FROZEN_PREDICTIONS.md`, `data/CORPUS.md`, `data/PRIMARY_TEXTS.md`, `src/*.py`,
`results/*.json`, `results/musculus_senses.tsv`.

### Known limitation of this run
Woods's own article was never read (paywalled, no OA copy confirmed). All tests target the
hypothesis reconstructed from his verified reference list. If he defuses the *galeas/sinus
replere* objection, RESULTS.md §6 needs revisiting — flagged as the top next experiment.
