# Validation — Ennis ogham amber bead, `STINGING` (validator 3, refuter)

claim: The Ennis ogham amber bead (I-CLA-003 / CIIC 53) inscription, read as the six-sign payload `DMVAVA`, decodes under a uniform three-position backward cyclic displacement in the traditional learned 20-sign ogham order `B L V S N | H D T C Q | M G NG Z R | A O U E I` to the English plaintext `S T I NG I NG` = **STINGING**, apt for an object documented since 1856 as a sore-eye amulet.

problem: `ireland/ennis-ogham-amber-bead/`

criteria applied: `PROBLEM.md` has no section headed "Success criteria". Its pre-registered standard is the **Crack target**, quoted verbatim:

> Establish what the inscription says or encodes while explaining the anomalous marks, direction and circular/closure geometry rather than merely fitting an inherited transcription.

I read this as conjunctive, as both co-validators did and as the sentence's own grammar requires: the participial clause "*explaining* the anomalous marks, direction and circular/closure geometry" modifies "Establish", and the final clause "*rather than* merely fitting an inherited transcription" excludes a reading that satisfies the first clause alone. Four demands: (1) say what it says or encodes; (2) explain the anomalous marks; (3) explain the direction; (4) explain the circular/closure geometry — and none of the four by fitting an inherited string.

validator role: 3 (refuter)

---

reproduced: **partially.** The decipherment and the uniqueness claim reproduce exactly and survive a much larger budget than the one they were tested against. The headline null figure does not reproduce and is quoted three different ways in the repo. The physical input does not reproduce from the source at all.

**Code, run from scratch on a clean machine (Python 3.11.15):**

- `code/decode_stinging.py` — runs, asserts pass, prints `S T I NG I NG` → `STINGING`. It is a table lookup, not a search.
- `code/branch_model.py` — runs, emits the 4 fork serialisations and the structural lower bound of 8. It implements the **superseded fork model**; no committed code implements the 2026-09-08 cycle model.
- `code/caesar_affine_null.py` — `ModuleNotFoundError: cmudict` on a clean machine. After `pip install cmudict textblob` (resolved to `cmudict 1.1.3`, `textblob 0.20.1`) it completes and confirms every qualitative claim: across the 20 cyclic shifts of `dmfafa` the only English hit is `stinging` at +17 ≡ −3, in both lexicons; `DMLOVA`, `ATATML`, `ATODML` are silent; across all 160 invertible affine maps mod 20 the only hit is `(a,b) = (1,17)`, i.e. the Caesar shift itself.
- **The null's numbers do not reproduce and the repo contradicts itself three ways.** `PROGRESS.md` l.71–74: 13,108 forms / 13,005 orbits / **0.4064%** ("about 1 in 246"). `analysis/stinging-candidate-2026-09-07.md` l.38–40: 13,932 / 13,893 / **0.4342%**. `SOLUTION.md` l.58 promotes the lower of the two, **0.406%**. The committed script on my machine gives a fourth: **13,486 / 13,450 / 0.42031%** (CMUdict 1.1.3, 117,493 alphabetic headwords). TextBlob reproduces to the digit (2,875 / 2,874 / 0.089813%). This is `cmudict` package drift, not an arithmetic error, and both co-validators independently obtained my figure.

**Sources, fetched and read first-hand, not via the dossier:**

- Live OG(H)AM EpiDoc `lguariento/og-h-am` `XML/I-CLA/I-CLA-003.xml` — raw fetch, HTTP 200, 10,888 bytes. Read in full, and decomposed to code points (below).
- Hayden & Stifter 2025, *Ogam, cryptography and healing charms in the nineteenth century* — PDF retrieved from Maynooth MURAL (HTTP 200, 3,750,712 bytes), extracted, **45 pages / 102,223 characters read**, not just the abstract. This is the single most consequential thing I did that the panel had not done, and it goes against the claim (finding 4).
- Irish lexicon: Kevin Scannell's GaelSpell hunspell dictionary (`wooorm/dictionaries` `ga`, 120,423 entries → 118,292 headwords), accent-stripped.
- **UNVERIFIED:** `ogham.glasgow.ac.uk` (both cited posts) — HTTP 202 redirecting to `/.well-known/sgcaptcha/`, a site-wide SiteGround captcha; no TLS verification was disabled and no workaround attempted. GitHub API commit history for the EpiDoc file — HTTP 403, repository not enabled for this session, so I **cannot** confirm whether the transliteration ever read otherwise. Macalister CIIC 53 at document level. British Museum object record. Graves 1856.

---

verdict: **PARTIAL**

I was assigned to break this claim. I did not break its cryptographic core — I made it harder and it held. I did break, or further break, three links in the chain around it, and I resolved the falsifier the panel left open. The result is the same verdict as my two colleagues, reached by a different route, and I want the *reasons* for the convergence on record rather than the convergence itself, because three similar models agreeing is worth very little (`_roles/VALIDATOR.md`, "Why three").

---

reasoning:

## 0. What I did

Ran all three scripts. Then reimplemented the alphabet, the shift, the direction transform and the null independently in ~150 lines, importing nothing from `code/`, and computed **exact** family reachability by forward closure over the whole 20⁶ = 64,000,000 sequence space rather than by orbit counting or by the independence approximation `1−(1−p)ⁿ`. Then attacked.

## 1. The `VAVA repeated` falsifier — RESOLVED, and it does not fire

Validator 1 raised this as "the cleanest available kill" and neither co-validator resolved it. I resolve it against the live record, and it resolves **in the claim's favour**.

The apparatus prose is genuinely ambiguous in isolation: "one branch goes to the right at an angle (roughly 45º) and appears to have the ogham letters VA repeated". But the editors also published a formal ogham edition, and an EpiDoc `<div type="edition">` is the text; the apparatus glosses it. I decomposed that edition to code points:

```
?ᚇᚋᚃᚐ?ᚃᚐ
0  U+003F  QUESTION MARK
1  U+1687  OGHAM LETTER DAIR      D
2  U+168B  OGHAM LETTER MUIN      M
3  U+1683  OGHAM LETTER FEARN     V/F
4  U+1690  OGHAM LETTER AILM      A
5  U+003F  QUESTION MARK
6  U+1683  OGHAM LETTER FEARN     V/F
7  U+1690  OGHAM LETTER AILM      A
```

Eight slots, six ogham letters, **exactly one FEARN+AILM pair after the second `?`**. Nora White's edition encodes `VA` once on the branch. "The ogham letters VA repeated" therefore means "the letters VA, repeated [from `DMVA`]", not "VA twice on the branch". Had she meant the latter the edition would read `?ᚇᚋᚃᚐ?ᚃᚐᚃᚐ`. It does not.

So the eight-sign payload `DMVAVAVA` is **not** a live reading of the source, and the claim's choice between the two senses of that sentence was correct, if undefended. For completeness I ran it anyway: `DMVAVAVA` over all 12 cycle readings × 20 Caesar shifts and × 160 affine maps, against CMUdict, TextBlob and Irish — **0 hits in all six combinations**. Had the phrase gone the other way the decipherment would be dead. It does not go the other way.

**This is the one component of my attack that the claim wins outright, and I record it as such.** The panel's cleanest available kill has been discharged.

*Caveat I cannot remove:* I could not retrieve the file's commit history (GitHub API 403), so I am asserting that the *current* edition is unambiguous, not that it has always read this way.

## 2. The cryptographic core survives a budget twelve times larger, and I could not break it

This is the claim's real strength and I state it without hedging.

Exact reachability, computed by forward closure of each lexicon under the inverse maps and then under the reading group, over all 64,000,000 six-sign sequences:

| budget | English (CMU) | Irish (GaelSpell) | EN ∪ GA |
|---|---:|---:|---:|
| A. frozen path + Caesar (20) | 0.420% | 0.251% | **0.642%** (1 in 156) |
| B. both directions + Caesar (40) | 0.838% | 0.500% | **1.279%** (1 in 78) |
| C. cycle, 12 readings + Caesar (240) | 4.815% | 2.885% | **7.212%** (1 in 13.9) |
| D. frozen path + affine (160) | 3.236% | 1.934% | — |
| E. cycle, 12 readings + affine (1,920) | 31.498% | 19.669% | — |

The "12 readings" are the full dihedral orbit of the cycle: 6 rotations × 2 directions, with direction implemented properly as reversal **plus** the aicme side-swap B↔H, L↔D, V/F↔T, S↔C, N↔Q with M-aicme and vowels invariant — not naive string reversal. I verified my transform reproduces the claimants' `ATATML` and `ATODML` exactly, and Hayden & Stifter independently corroborate the side-swap model: they record 19th-century scribal confusions of precisely this form (S "four strokes below" written as C "four strokes above"; I "five strokes through" written as N "five strokes below"; DH written as F).

Now the hits. Under tier C — 240 combinations per core, 480 across both cores, the honest post-audit budget:

- `DMVAVA`: **one** English hit, `stinging`, at rotation 0, forward direction, shift −3. The other 11 readings are silent at all 20 shifts.
- `DMLOVA`: zero.
- Irish, both cores: **zero at every tier**, Caesar and affine.

Under tier E (1,920 combinations) `DMVAVA` picks up exactly one competitor in CMUdict — `vivier`, from reading `FAFADM` under `a=9, b=4` — a French surname in a pronunciation dictionary, at a non-shift affine map, in a family the claimants explicitly declined to privilege. TextBlob still yields only `stinging`.

I went looking for the classic failure — a plausible reading fitted to a corpus small enough to fit anything — and it is not there. Expand the search twelvefold and the answer does not change. That is a genuinely narrow, specific, reproducible hit and I will not have it written down as luck.

## 3. But the deletion that produces the payload is a *length-selection* effect, and the panel has been over-crediting the null results at length 7 and 8

Both co-validators tested the editors' actual strings and reported zero hits: V2 ran `DMVA?VA` over 20 fillings; V1 ran `?DMVA?VA` over 400 fillings × 2 directions × 20 shifts = 16,000 combinations. I reproduce both — `DMVA?VA` over 20 fillings × 12 cycle readings × 20 shifts = 4,800 combinations, 0 hits; `?DMVA?VA` over 16,000 combinations, 0 hits — and I now think **both results carry far less weight than either of us implied**, in a direction that hurts the claim.

English word density in ogham-sign space collapses with length:

| payload length | CMUdict sequences | density of 20ⁿ | cycle-budget hit-rate upper bound |
|---:|---:|---:|---:|
| 6 | 13,486 | 2.11 × 10⁻⁴ | 5.06% |
| 7 | 14,136 | 1.10 × 10⁻⁵ | 0.31% |
| 8 | 11,304 | 4.42 × 10⁻⁷ | 0.014% |

Zero hits at length 8 is *exactly what the null predicts* — the expected yield over V1's 16,000 combinations is about 0.007 words. Finding nothing there is not evidence that the two `?` are non-phonetic; it is evidence that eight-sign English words are rare. The inference has been running the wrong way round.

The corollary is the sharp one. Length 6 has **478 times** the false-positive density of length 8. The decision to delete two signs from `?DMVA?VA` is not a neutral tidying of unreadable marks — it relocated the search to the single length at which a spurious English word is most likely to appear, and it is the only length at which one does. `SOLUTION.md` presents the six-sign payload as a conservative restriction to "the six ordinary-looking signs". Statistically it is the opposite of conservative. Nothing in the dossier charges for it, and the 0.406% figure is computed *conditional on* the deletion having already been made.

## 4. The claim's own genre source refutes its "operation class is attested" argument

`SOLUTION.md` §5 separates **operation class** ("independently attested") from **nonce key** ("inferred"), and cites Hayden & Stifter 2025 as the modern authority. No one on this panel had read the paper — V2 verified the abstract, V1 verified the citation. I read all 45 pages. Three findings, all against the claim:

**(a) The attested nineteenth-century ogham ciphers are named, specific, and structurally unlike a positional rotation.** Hayden & Stifter enumerate them: *ogam craobh*; *ogam coll*, in which vowels are written as one to five `c`s (from the *Lebor Ogaim* variant *coll ar guta*, "C for a vowel"); and *ogam consaine*, a consonant-skeleton cipher with fixed substitutions — in the worked example, Í is represented by NG and the diphthong EA by doubled MM. These are vowel-suppression and consonant-skeleton devices inherited from the tract tradition. **Not one of them is a uniform displacement of the twenty phonetic values.** The attested class is not "alphabet re-indexing"; it is a small closed set of named graphical/orthographic ciphers, and `−3` is not in it. Combined with V2's finding that the NLI G 163 "Topsy Turvey Cryptography / Ogham Chinn air iomal" is on its name a way of *writing the strokes* rather than permuting values, the "operation class attested, key inferred" separation is overstated by a level: what is attested is that the tradition manipulated ogham systematically, not that it ever performed this kind of operation.

**(b) The Minchin Manuscript charms are in plain ogham, not cipher.** This is a category error at the heart of the dossier's synthesis. In Hayden & Stifter the ciphers (*coll*, *consaine*) appear in signatures, colophons and set texts — the Pater Noster and Ave Maria in RIA MS 23 K 34. The Minchin notebook is "written entirely in ogam" with no superimposed substitution: the cryptic element *is* the script. `SOLUTION.md` fuses two distinct nineteenth-century practices into a single genre, "cryptic healing ogham", and no attested object belongs to it. The three "independently attested components" are real individually; their conjunction is the claim's own construction.

**(c) The genre comparator predicts against an English bare symptom word — specifically.** The Minchin eye-charms are the closest comparanda in existence, and Hayden & Stifter describe them: two prayers for *drochshúil* ("weak eyesight" or "the evil eye"), invoking St Brigid. The manuscript's 59 charms are organised under Irish headings of the form `ᚐᚏ …` (*ar x*, "for [or against] x"), followed by a prayer body. So the one corpus cited as genre support predicts an **Irish** ailment-name, under an **`ar` heading**, attached to a **prayer**. `STINGING` is an English participle, with no heading and no prayer, and is not the Irish for anything. `analysis/stinging-candidate-2026-09-07.md` §5 concedes half of this ("charm comparators are usually fuller formulae"); the full version is worse than the concession.

Against this, the EpiDoc's own language field reads `<textLang mainLang="ga-Ogam" cert="medium">Probably Irish written in ogham script</textLang>`, and my Irish search returned **zero hits for `DMVAVA` across all 240 Caesar and 1,920 affine cycle combinations**. The only language in which this object speaks is the one every external witness makes least likely, and it is silent in the language the editors assign it.

## 5. The reading has zero tolerance to exactly the error the editors record on this object

The EpiDoc `<handNote>` states, of this bead specifically: "Ogham strokes from the B- and H- *aicmi* sometimes stop at the stem-line but other times cross it slightly." That is a recorded, object-level warning that the side of the stemline — the thing that distinguishes B-aicme from H-aicme, and a stopping stroke from a crossing M-aicme stroke — is not cleanly determinable here. Hayden & Stifter document the same confusion class as a live scribal phenomenon in nineteenth-century ogham.

I tested how much of that the decipherment can absorb.

- All 114 single-sign substitutions of `DMVAVA`, frozen path + Caesar: **1 of 114** retains an English hit — `DNVAVA` → `SLINGING`.
- The 12 substitutions corresponding to the confusions the sources actually document (aicme side-swap per sign; ±1 stroke within an aicme): **0 of 12** retain any hit.

So the reading is knife-edge. Every one of the six signs must be exactly right, and the specific misreadings the editors flag on this object each destroy it. A decipherment can legitimately be fragile — most are — but a fragile decipherment resting on signs whose editors have formally recorded a stroke-side ambiguity cannot be treated as established, and the ~0.42% null figure assumes the sign identities are certain when the source says they are not.

Note also that `SOLUTION.md` §1 describes the branch as carrying "further ordinary-looking `VA` signs" and omits the editors' qualification, which `analysis/evidence-ledger.md` does carry: "the final A is quite short and looks like an X at the end of the stemline". Sign 6 of 6 — one of the two `A`s that supply the `I-NG I-NG` morphology the claim rests on — is flagged as doubtful in the source and as secure in the solution document.

## 6. The cycle model is itself an inference presented as an observation, and it costs the claim either way

`analysis/evidence-ledger.md` lists under **OBSERVED from the modern specialist record**: "A cut stemline runs around the object and is best modelled geometrically as a **loop/cycle**". The live record does not say this. It says "split stem-line" in the `<handNote>`, "a split in the stemline (possibly to avoid running into the perforation)" in the apparatus, and gives a linear reading instruction: "the inscription may be read upwards on the cut stem-line with the perforation to the right". The encircling geometry traces to Macalister 1945, whom I could not read at document level (**UNVERIFIED**; V2 reached it only as a search-engine extract).

This is a fork with no good branch:

- If the **fork** model is right, the two arcs are alternatives, selecting one is coherent — and `PROBLEM.md`'s clause (4) "circular/closure geometry" is being answered with a model the claim itself has disavowed.
- If the **cycle** model is right, the arcs are parts of one continuous path, every traversal passes through both, discarding the left-branch mark is unlicensed (V2's finding 2, which I confirm), and the honest null is tier C: **7.2%, one in fourteen**.

The dossier holds the fork-model *conclusion* inside the cycle-model *frame*, and prices the result at the fork-model rate.

## 7. Against each clause of the Crack target

| clause | met? | why |
|---|---|---|
| "Establish what the inscription says or encodes" | **conditionally** | A specific, reproducible, unusually narrow candidate — conditional on a traversal the editors state is undetermined ("It is unclear where to start reading the inscription") and on a payload not present in any edition. |
| "explaining the anomalous marks" | **no** | The `<` exclusion is properly sourced (not a known ogham character, does not meet the stemline). The second exclusion is not: the left branch's "oblique stroke to the right" is an ordinary ogham stroke form, and it is excluded because including it yields no word (0 hits over 4,800 and 16,000 combinations). Exclusion is not explanation, and §3 above shows the exclusion is also the step that maximises the false-positive rate. |
| "direction" | **no** | The source says direction and start point are undetermined. The claim selects the direction that yields a word; it is inferred *from* the plaintext, not *for* it. |
| "circular/closure geometry" | **no** | Unresolved by the claimants' own 2026-09-08 audit, and §6 shows the geometry rests on a single unexamined 1945 witness. |
| "rather than merely fitting an inherited transcription" | **no** | `DMVAVA` is the inherited `?DMVA?VA` with two signs deleted. This clause was written to forbid this move, and the deletion is not cosmetic — it is load-bearing and statistically self-serving. |

## 8. The defensible null figure

For the record, since this is quoted four different ways across the repo and the orchestrator will need one number:

- **Do not quote 0.406% or "1 in 246."** It does not reproduce, it is the most favourable of three committed values, and it is the frozen-path, English-only, deletion-conditional rate.
- The reproducible frozen-path rates, on `cmudict 1.1.3` / `textblob 0.20.1`: **0.4203%** (CMUdict) and **0.0898%** (TextBlob, which reproduces exactly and is the figure to prefer if a single frozen-path number is wanted).
- **The defensible headline figure, under the physical model the repo itself adopted on 2026-09-08 and the languages the source record actually admits, is 7.2% — about 1 in 14.** That is my exact enumeration over all 64,000,000 six-sign sequences for the 12-reading cycle budget under the Caesar family with an English ∪ Irish lexicon. It is *not* a union bound and *not* the `1−(1−p)ⁿ` approximation; both co-validators' figures (V1's 2.6–5.2% union bound, V2's 4.9% at n=12) are consistent with it and mine supersedes them.
- That 7.2% still charges nothing for the deletion (§3), nothing for the `DMLO` transcription alternative, and nothing for the affine family the claimants also searched. Charged for the affine family it is 31.5% English alone.

One in fourteen is not nothing. It is also not a decipherment.

## 9. What survives my attack

Stated plainly, because a refuter who only lists damage is not being fair:

1. **The arithmetic is exact and reproduces**, from scratch, without the repo's code. `D`=6, `M`=10, `V`/Fearn=2, `A`=15; −3 mod 20 → 3, 7, 19, 12 = `S`, `T`, `I`, `NG`.
2. **The uniqueness claim holds under a twelvefold larger budget.** 480 cycle-model combinations across both cores, three lexicons: one English word. I tried to find a competitor and there is essentially none.
3. **The `VAVA repeated` falsifier is discharged** against the editors' own ogham edition (§1). The panel's cleanest kill does not fire.
4. **The direction transform is implemented correctly** — the side-swap, not string reversal — and is independently corroborated by Hayden & Stifter's scribal-error evidence. `ATATML` / `ATODML` are right.
5. **The `<` exclusion is properly sourced.**
6. **The demolition of `ATUCMLU` as ground truth and of the Glenfahan / `MTBCML` parallel** is sound and survives.
7. **`VA VA → I-NG I-NG`** is real, though V1 is right that it is forced by bijectivity and carries no independent weight once the payload is fixed.
8. **The dossier's own adversarial file reached the correct verdict** — "PARTIAL / high-value candidate. Do not post a solve claim yet" — before the board log overstated it, and the 2026-09-08 audit walked the physical claim back unprompted. The current `SOLUTION.md`, `HANDOVER.md` and `PROBLEM.md` do not oversell. `board/log/2026-09-07-ennis-stinging-solve.md`, read alone, does.

## 10. Why this is PARTIAL and not FAIL

I looked for a contradiction and did not find one. Everything I found is an unsupported assertion or an unassessable gap, which `_roles/VALIDATOR.md` requires me to distinguish from contradiction. The single available contradiction — `VAVA` on the branch — I resolved in the claim's favour. The work is not wrong; it is unproven, and it is unproven in a way that no further lexical search can fix.

PARTIAL, and per `_roles/VALIDATOR.md` this claim is **HELD — awaiting human sign-off**, and remains held whatever the other two verdicts say.

---

dissent: **None from the verdict.** All three validators independently return PARTIAL. I read v1 and v2 only after running the code and forming my own attack, as instructed, and I record that the convergence is not an echo: V1 came at it through the criteria and the statistics, V2 through the physical and historical evidence chain, and I through an attempt to kill it. We arrive at the same place by three different roads, which is worth more than the agreement itself. Where we overlap I confirm: I reproduce V1's and V2's CMUdict figure (13,486 / 13,450 / 0.4203%), V2's zero-hit result for `DMVA?VA`, V1's zero-hit result for 16,000 `?DMVA?VA` combinations, and both of their readings of the Crack target as conjunctive.

Four points of my own to record, two of which move numbers my colleagues committed:

1. **V1's stated falsifier is discharged, not open.** V1 left, as item 1 for whoever picked this up, the question whether "the ogham letters VA repeated" means the branch carries `VAVA`. It does not: the editors' own ogham edition `?ᚇᚋᚃᚐ?ᚃᚐ` contains exactly one FEARN+AILM pair after the second `?` (§1). `DMVAVAVA` is not a live reading. The board should stop carrying this as an open kill.
2. **I dissent from the evidential weight both co-validators placed on the length-7 and length-8 null results.** Zero English hits over V1's 16,000 `?DMVA?VA` combinations is the *expected* outcome under the null (expected yield ≈ 0.007 words), because eight-sign English words are 478× rarer in sign space than six-sign ones. Neither verdict says so, and V1 presents it as showing "there is no assignment of the two anomalous marks under which this cipher produces an English word" — true, but nearly uninformative. The real finding in that vicinity is the reverse one: deleting to length 6 selects the length of maximal false-positive density (§3).
3. **The honest null number is 7.2%, not 0.65% and not 4.9%.** V1's English ∪ Irish figure (0.6526%) is the *frozen-path* union and does not carry the cycle budget; V2's 4.9% carries the cycle budget but is English-only and uses the independence approximation. The exact English ∪ Irish cycle-budget rate over all 64,000,000 sequences is **7.212%, one in 13.9** (§8). If one number goes on the board, that is the one.
4. **New evidence against the historical bridge, from the claim's own source.** Neither co-validator read Hayden & Stifter beyond the abstract. The paper's enumeration of attested nineteenth-century ogham ciphers — *ogam craobh*, *ogam coll* ("C for a vowel"), *ogam consaine* (Í→NG, EA→MM) — contains no positional rotation of the twenty values; the Minchin charms are in plain ogham with no superimposed cipher, so "cryptic healing ogham" is the dossier's construction rather than an attested genre; and the Minchin eye-charms are Irish *drochshúil* prayers to St Brigid under `ar x` headings, which is a comparator predicting specifically against a bare English participle (§4). `SOLUTION.md` §5's "operation class independently attested / nonce key inferred" split should be downgraded: the attested class does not contain this operation.

If a human reviewer is inclined to sign this off as a solve on the strength of the statistics, the two questions I would want answered first are §3 (why is a deletion that moves the search to the length of maximal false-positive density treated as conservative?) and §5 (how can a reading survive as established when 0 of the 12 sign-confusions the editors record on this very object leave it standing?). Neither is answerable by more searching. The decisive test remains the one the dossier already identifies: the photogrammetry and RTI captured on 2023-12-05, read blind to `STINGING`.

And the thing I would not want lost in the doubts: expanded twelvefold, across three lexicons and 480 combinations, this inscription still produces exactly one English word, and it is the word for what the object was kept to cure. I could not make that go away.
