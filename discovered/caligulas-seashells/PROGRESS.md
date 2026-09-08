# Progress Log – Caligula's Seashells

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-08 – local-only `musculus` inventory recovered (orchestrator)

Recovered `analysis/extract_tei_occurrences.py` plus its raw CSV and metadata from the
primary checkout during the all-worktree reconciliation. The extractor pins
`PerseusDL/canonical-latinLit` at commit
`2481af34dea79eab4e595f06719d292c6660b716` and reports 363 Latin edition files scanned,
96 passage rows, 127 surface-form matches, and 16 matching source files.

This is preserved as **unfinished evidence preparation**, not a finding. The rows have not
been sense-coded; no null, held-out Vegetius test, power analysis, or comparison to the
separate concha/umbilicus result was run. The stale 2026-09-04 claim was deliberately not
restored. Woods (2000) rejects the `musculi` siege-shelter reading and instead reads
Suetonius's `conchae` as small captured boats; future work must use that corrected premise.

---

## 2026-09-07 – first working session (cracker, starting mode)

**Model/seat:** Claude Opus 5, Claude Code remote session.
**Full write-up:** `analysis/2026-09-07-concha-umbilicus-survey.md`.
**Reproduce:** `analysis/data/survey.py` + `analysis/data/survey_output.txt`.

### What was attempted
The base-rate lexical survey the 2026-09-06 handover demanded, run on two full corpora
cloned from GitHub (`cltk/latin_text_latin_library`, 2,141 texts / 95.9M chars;
`cltk/latin_text_tesserae`, 748 texts / 46.7M chars, including the complete Pliny *NH*).
Three lemmas — `concha`, `umbilicus`, `musculus` — every hit window read by hand.

The handover asked for a `musculus` base rate counted both ways. That was delivered, and
then the survey was widened to the word Suetonius actually wrote, which is where the
session's result came from.

### Results / findings

**1. The load-bearing finding.** In 46.7M chars of classical Latin including the complete
*Natural History*, `umbilicus` in the sense "shore shell" occurs exactly **three** times:
Cicero *De Or.* 2.22 and Valerius Maximus 8.8.1 — both the Scipio-and-Laelius shell-gathering
anecdote — and **Aurelius Victor, *Caes.* 3.11, of Caligula**: `conchas umbilicosque in ora
maris Oceani legi iussit`. Pliny, who catalogues every other shell name in Latin, never uses
the word this way. `conchas et umbilicos legere` is therefore not a neutral description; it
is a marked idiom whose only other owners in the surviving language are Scipio and Laelius.

**2. Woods falsified at the lexical level.** `concha` never denotes a boat in 290 combined
instances. The nearest thing is Pliny *NH* 9.51, where the nautilus has to be spelled out as
keel-stern-prow *because* the noun does not carry the sense. Separately, `concha` and
`musculus` are distinct items in the same list at Plautus *Rud.* 297–99, so the *musculus*
route needs two confusion steps, not one.

**3. `musculus` base rate (n=53, Latin Library, manual):** anatomical ~17, "little mouse" ~9,
shellfish ~6, sea-creature ~3, **military siege-shed ~19**, boat ~2. Military-technical runs
at ~40%, so Woods is not making an absurd claim about the word — the survey kills the *need*
for the emendation, not its plausibility.

**4. `concha` is not a worthless-object word.** 39% of instances sit in pearl/purple/luxury
vocabulary. Suetonius' own three uses of the `conch-` root in the whole *Twelve Caesars* are
murex-dye largesse (*Cal.* 18), the disputed passage, and pearl-shell palace revetment
(*Nero* 31). None is beach litter.

**5. Held-out confirmation.** Predicted from (4) alone, then checked: Suet. *Iul.* 47,
`Britanniam petisse spe margaritarum` — Suetonius had already made shell-borne treasure the
canonical motive for crossing the Ocean, in the first Life of the same work.

**6. Compositional frame.** *Cal.* 45–47 is a designed triad of counterfeit triumphal
material — fake trophies from felled trees, `spolia Oceani`, Gauls dyed and drilled as German
captives — reusing the verb `legere` in 46 and 47. Cicero glosses the shell idiom as `ad
omnem animi remissionem **ludumque** descendere`; chs. 45 and 47 are the same register.

**The reading (INFERRED, and labelled as such):** the order is a legible allusion to the
canonical Roman exemplum of *otium* — an army in battle order made to perform the private
leisure of Scipio and Laelius on the Ocean shore, the product then claimed as `spolia` for
the Capitol. Neither madness nor emendation is required. Valerius Maximus, writing under
Tiberius, shows the exemplum was current one reign before AD 40.

### Failures & dead ends
- Egress permitted **GitHub only**. Perseus, PHI, LacusCurtius, Cambridge Core, JSTOR,
  ResearchGate, archive.org and Wikipedia were all proxy-blocked. No modern scholarship was
  read this session.
- Recommended experiment 1 (read Woods in full) **not done** — inaccessible.
- Recommended experiment 5 (Suetonius/Dio independence) **not settled** — Dio's Greek was
  unreachable. A third witness (Victor) was added instead, whose wording demonstrably does
  not derive from Suetonius.
- The pearl reading circulating on popular sites was considered and is **not** advanced here.
  The corpus supports "`concha` is an economically charged word", not "the order was to
  collect pearls".

### Corrections to prior Hub work
- Recommended experiment 2 is **cleared**: a peer-reviewed rebuttal of Woods exists —
  S. J. V. Malloch, "Gaius on the Channel Coast," *CQ* 51 (2001), 551–556. Metadata-level
  verification only.
- `PROBLEM.md` attributes the *musculi* thesis to Woods. Two independent search passes this
  session indicate Woods argued `conchae` = **small boats**. Unresolved; a dated correction
  note is appended to `PROBLEM.md`. §3 of the analysis addresses both theses, so nothing here
  depends on the answer.

### Artefacts produced
`analysis/2026-09-07-concha-umbilicus-survey.md`, `analysis/data/survey.py`,
`analysis/data/survey_output.txt`, `board/log/2026-09-07-rare-collocation-as-evidence.md`.

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
