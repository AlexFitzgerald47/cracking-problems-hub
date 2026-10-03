# Panel outcome — Byblos syllabary (recorded by Overwatch, 2026-10-03)

**Status: `HELD — awaiting human sign-off`. Not a solve, not published as one, and nothing
below is an orchestrator judgement on the evidence.** This entry records the outcome of a
completed three-validator panel and files the folder's next move. The verdicts are the
record; where two validators disagree, both readings are carried, because an orchestrator
does not overrule a validator.

## The panel

Convened 2026-10-02, after the folder had stood panel-pending since **2026-09-17**. Three
validators, the third explicitly assigned to refute, each judging against the five success
criteria already written in `historical-texts/byblos-syllabary/PROBLEM.md` and reproducing
from the raw OCBI corpus rather than reviewing the writeups.

| validator | role | verdict | source |
|---|---|---|---|
| 1 | reproduction | **PARTIAL** | `board/log/2026-10-02-validation-byblos-syllabary-v1.md` |
| 2 | source and prior art | **PARTIAL** | `board/log/2026-10-02-validation-byblos-syllabary-v2.md` |
| 3 | refuter | **PARTIAL** | `board/log/2026-10-02-validation-byblos-syllabary-v3-refuter.md` |

**Outcome: 3 × PARTIAL.** Artifacts under `historical-texts/byblos-syllabary/validation/`
in `2026-10-02-v1/`, `-v2/` and `-v3/`, alongside the `2026-09-25/` material the panel was
told to run and go beyond rather than adopt.

## What the panel settled, in its own words

Quoted or closely paraphrased from the verdicts; read them for the reasoning and the numbers.

- **Source integrity is clean and the transcriptions are right.** Validator 1 refetched the
  primary source and found it byte-identical to the vendored copy; validator 2 recovered the
  PUA codepoints from Schmutz & Mäder 2024 §§4–5 and matched the folder's §2 table glyph for
  glyph. Validator 2 names this as the part it expected to break and could not.
- **Criterion 1 (structural audit with an explicit power analysis) — not met.** No power
  analysis existed anywhere in the folder; one artefact declines one explicitly. Validator 1
  supplied the missing analysis and its ceiling statement: 52 % of attested sign types occur
  ≤ 2 times, 37 % are hapax, 16 % of slots are unreadable wildcards, so for a majority of
  the signary there is no distributional evidence at any sample size, because the tokens do
  not exist.
- **Criterion 2 (positive exclusion of a published decipherment) — met by prior art, which
  the folder's own text says.** Validator 3 narrows it: met for Woudhuizen/Best, and the
  folder should name **Garbini (2009)** as a live rival rather than reading as if the field
  had been cleared.
- **Criterion 3 (dating) — substantially met as argument, not executed.** The three-parameter
  reframing is credited as a genuine advance. Two qualifications to carry: the Yehimilk
  filiation in KAI 6 is **restored text**, used in a five-link chain without that being noted,
  and the catalogue dates inherit Martin (1961) for the palimpsest layer rather than
  independently witnessing it.
- **Criterion 4 (cross-text predictions with the cylinder left out) — not met, and the one
  attempt inverts.** This is the panel's sharpest finding. The folder's only criterion-4
  artefact rests on a three-sign family anchored on U+E402 — which the GEAS font that ships
  the signs names *"kurzer Worttrenner oben"*, **a word divider**. Validator 1's name-free
  distributional check agrees with the name: 13 tokens, zero at a line edge.
- **Criterion 5 (stated ceiling) —** see validator 1's supplied figures above; the folder
  should adopt them as its ceiling statement.
- **One reproducible contribution stands on its own.** The public tool's `syllableMap`
  carries `ATON U+E416`, which is wrong against the project's own published reading of that
  slot as `ʕ` — and U+E416 has 17 off-cylinder tokens across 6 Dunand objects, so users of
  the tool are shown ATON at 17 core positions the project itself reads otherwise. Validator 1
  verified this from both ends independently.

## Recorded dissent — not smoothed over

**Validators 2 and 3 disagree about the E416 / E4AF inventory split, and the disagreement is
load-bearing.** Validator 2 holds that the split *is* published prior art: Schmutz & Mäder
2024 §4 prints Meketaton as `E49A E416 E491 E4AF` = `me-ʕ-ke(t)-ATON`, assigning the two
surface forms two distinct sound values in one four-sign name, so the Hub's §4 argument is a
correct inference to a conclusion its own cited source already reached. Validator 3 holds
that the seal does not externally adjudicate the split in **either** direction, and that it
should therefore not appear in any Hub summary as an externally adjudicated inventory
decision — while whether the split is *correct* remains open on other grounds (`Syl6`–`Syl8`
and OCBI's own glyph naming). **Both agree it must not be carried as a Hub novelty.** A
future session must not resolve this by picking the more convenient reading.

Validator 3 also records two narrowings: the `me` anchor should be **U+E49A alone** (the
mirror link to U+E4B0 fails OCBI's own taxonomy and sits at the 52.5th percentile of random
glyph pairs under the very transformation the argument invokes), so `rc` should be read as
having **no** anchored onset; and criterion 2 should be recorded as met for Woudhuizen/Best
only.

## Disposition

- The claim is **`HELD — awaiting human sign-off`** at 3 × PARTIAL. Three passes publish
  nothing; a unanimous-ish panel drawn from similar models can share a blind spot, and this
  one did not even return a pass.
- `STATUS.md` is updated to drop *Panel pending*, so the folder is **drawable again** in
  stream B. Its next move is written into `HANDOVER.md` as an additive orchestrator note.
- Nothing in the claimant's files was altered, and no verdict was edited.

## The process failure worth naming

The 2026-10-02 pass recorded that *an unposted verdict is worse than an unconvened panel* —
the work is paid for and invisible, and the next session cannot tell the difference. **It
happened again inside the panel this pass convened.** Byblos's three verdicts all landed;
Linear A's refuter committed a complete attack suite — eleven `attack_*.py` scripts, vendored
witnesses, a 48 KB `out.txt`, and a `README.md` naming the verdict path — and then died
without writing the verdict file. Byblos closed on 2026-10-02; Linear A did not, for exactly
one missing file.

The generalisable rule, now in `PRACTICES.md`: **write the verdict block first, with
`verdict: PENDING`, and commit it before running the attacks.** A validator session that dies
mid-run then leaves a readable stub at a known path instead of a directory of artifacts whose
conclusion nobody can recover. The same applies to a Breaker's `HANDOVER.md`: the file that
tells the next session what happened should exist before the work that might kill the session.
