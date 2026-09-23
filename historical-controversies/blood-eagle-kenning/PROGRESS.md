# Progress Log – The Blood Eagle

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-23 – Claude Opus 5 / cracker, *starting* mode: skaldic base rates, prose transmission map

### What was attempted
First substantive session on this problem. Built the complete skaldic corpus from primary
editions and measured the base rate behind the premise the whole sceptical case rests on:
that Sigvatr's *Knutsdrapa* st. 1 uses a **conventional** beasts-of-battle image. Then built
the prose dossier from primary text and coded it feature by feature.

Predictions were frozen before any counting: `analysis/2026-09-23-PREREGISTERED.md`.
Full write-ups: `analysis/2026-09-23-skaldic-base-rates.md` (measurements) and
`analysis/2026-09-23-the-dossier-rests-on-a-hapax.md` (what they mean, and the literature).
Code in `analysis/code/`, data in `analysis/data/`, corpus rebuild script included.

### Results / findings
**Corpus.** Finnur Jonsson, *Den norsk-islandske skjaldedigtning* A I-II + B I-II (1912-15),
all four volumes, from **two independent archive.org OCR scans used as replicates**. Every
number was computed twice. The scans differ by ~7% on raw counts and agree on every result.

1. **No beast of battle is ever the agent of a blade verb.** 772 (scan A) / 719 (scan B)
   beast-of-battle lexemes in Old Norse verse; 35 blade-verb co-occurrences across both scans,
   **adjudicated one at a time** (proximity is not construction). Zero have the beast as agent.
   The apparent hits are warrior kennings (`ara braedis` = "eagle-feeder"), swords and ships as
   subject, the **personal name Hrafn**, stanza-boundary artefacts, and the noun `sker`
   "skerry". Committed row by row with a verdict and a reason:
   `analysis/data/beast_blade_adjudication.tsv`. Feeding/colouring verbs run at 14.6-19.5%.
   Rule-of-three 95% upper bound on beast-as-blade-agent: **0.39%**.
2. **`bak` is not a beasts-of-battle word.** Complete enumeration: 21 / 20 occurrences in ON
   verse, ~76% the idiom (`a bak` = behind/on horseback; `ganga a bak ordum` = renege). It
   co-occurs with a beast **exactly once** and with a blade verb **exactly once** — both times
   in Knutsdrapa 1. Killing wounds in skaldic verse go to `herdar`, `haus`, `leggr`, `fjor`.
3. **The corpus HAS a carrion formula, and Sigvatr did not use it.** The victim *falls, lies or
   sinks under the eagle's talons*, and the bird treads: `fell Ottarr und ara greipar … a Vendli
   sparn` (Ynglingatal 19), `und arnar hrammu`, `und gulri klo gras arnar`, and Torf-Einarr
   lv. 4. >=5 instances, >=4 poets. Frank herself names this formula's frequency as her reason
   for calling the image conventional — while reading a stanza that does not use it.
4. **Torf-Einarr is the control, and it favours Frank.** The one man the tradition credits with
   a blood eagle who is also a surviving poet describes that very killing with the conventional
   carrion formula and no rite: `hverr ilthorna arnar undir hlytr at standa`. *Orkneyinga saga*
   quotes that verse and produces `rista blodorn a baki honum … draga thar ut lungun … gaf hann
   Odni til sigurs ser`. In the Halfdan branch Frank's mechanism is documented input and
   documented output, not a hypothesis.
5. **The prose escalation is branched, not chronological.** Coded from primary text
   (`analysis/data/prose_feature_matrix.tsv`): *Orkneyinga saga* (c.1200-30) is contemporary
   with Saxo (c.1200) and already has the complete rite — compound `blodorn`, ribs, lungs,
   Odinn — while Saxo has only an eagle-shaped wound and *Ragnars saga* only a marked-and-
   reddened outline. Two branches with different content from the earliest date. They **merge at
   *Ragnarssona thattr* c.1300, which is also the only text that quotes Sigvatr** — the skaldic
   citation enters the dossier at the END of the chain, as corroboration, not at its head.
   Also: the prose verb is `rista`/`marka`, never Sigvatr's `skera`, which the prose reserves
   for the ribs.
6. **The convergence.** The prose dossier's invariant core across Latin and Norse, historical
   and legendary victims, both branches, is the bare pair *eagle + back*. That pair occurs
   **once** in the whole skaldic corpus. The invariant of the prose is the hapax of the verse.

**Verdict.** Frank's *conclusion* — "deprived of its skaldic stanza, the rite of the blood-eagle
has no viking-age support" — is right and now has a denominator. Her *argument* for it, that the
stanza is "a conventional utterance," is wrong: it is a hapax on the verb, on the body part, and
on the formula. And because it is a hapax, **it cannot adjudicate itself**. The question is
undecidable from the skaldic evidence for a measurable reason: n = 1. On the relative merits of
the two construals the corpus does decide, and it decides against the received sceptical reading
— Frank needs the eagle to be the agent of a blade verb (0/772); Einarsson needs `skera` to carve
a figure on a surface, which is attested (`rikula ristin rit`, `baugvang skorinn`, `fagrt of
skornir drekar`).

### Corrections to the record
- **PROBLEM.md's verification debt on the stanza's attribution is cleared.** Sigvatr Thordarson,
  *Knutsdrapa* st. 1, confirmed against the primary edition in both the diplomatic (A I:
  `1. Ok ellv bak / at let hin er sat / ivaR ara / iorvik skorib.`, under the poet heading
  OCR'd `SKJVATR`, poem numbered `10. Knutsdrapa (o. 1038)`) and the normalised text (B I).
- **Priority belongs to Bjarni Einarsson (1986)**, not to this session. He asserted that `skera`
  of carrion beasts is "inconceivable" in the old poetic language and that `skera` and `bak` are
  "both unsuitable," with four citations (*Saga-Book* XXII:1, 79-82, at 80). This session
  measured what he asserted. Said plainly at the top of both analysis files.
- **A delegated researcher reported that the *Saga-Book* XXII PDF did not contain the
  Einarsson/Frank exchange. It does** — both notes, in full, at
  `https://vsnr.org/wp-content/uploads/2021/11/Saga-Book-XXII.pdf`. I fetched and read it
  myself. A second researcher's Old Norse quotations were all checked against the sources and
  were accurate. Board rule confirmed again: re-check everything a researcher hands back.

### Failures & dead ends
- **skaldic.org is unusable** — behind an ALTCHA proof-of-work bot gate, and the Wayback mirror
  too. Finnur Jonsson on archive.org is the working substitute and is better for this purpose
  anyway (it is the complete corpus in one searchable text, with a Danish translation of every
  stanza as a second channel).
- **First-pass proximity counting was wrong and would have published a false negative result.**
  Raw co-occurrence said 18-21 beast/blade hits, i.e. "P1 refuted." Every one dissolved under
  adjudication. Proximity is not construction; a `±70`-character window crosses stanza
  boundaries (3 of 35 rows did).
- **Two lexical traps cost time and would silently corrupt any future run:** most corpus tokens
  of `hryggr` are the **adjective** "sad," not the noun "spine" (12 of ~20 here); and `hrafn` is
  a common **man's name**, which produced 5 of the 35 false blade co-occurrences.
- The `bak` result is **underpowered on its own** — n = 21 can only exclude rates above ~15%
  (0.85^20 = 0.039). It is corroborative. The n = 772 result is the load-bearing one.
- Frank 1984 (EHR) itself could not be obtained; paywalled at OUP/JSTOR with no open deposit.
  Worked around via her own 1988 and 1990 *Saga-Book* restatements, which are explicit enough
  that the risk is low but not zero. Recorded as standing debt.

### Artefacts produced
`analysis/2026-09-23-PREREGISTERED.md`, `analysis/2026-09-23-skaldic-base-rates.md`,
`analysis/2026-09-23-the-dossier-rests-on-a-hapax.md`,
`analysis/data/beast_blade_adjudication.tsv` (35 rows, verdict + reason each),
`analysis/data/prose_feature_matrix.tsv` (8 texts x 11 features),
`analysis/code/` (9 scripts + `FETCH_CORPUS.sh`, rebuilds everything from scratch).

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
