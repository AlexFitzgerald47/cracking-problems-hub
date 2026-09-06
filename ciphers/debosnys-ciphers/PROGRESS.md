# Progress Log – The Debosnys Ciphers

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-05 – GPT-5.6 Sol / cross-page signature + shifted-phonetic breakthrough

### What was attempted
- Continued from the Folger-composition handover rather than restarting: froze a Debosnys-specific atomic inventory and machine-readable component constraints.
- Revisited Sektu's six-glyph `signature` line as a crib, but stopped guessing external real names and instead searched the *other Debosnys pages* for a plaintext signature by the same hand.
- Inspected the primary Commons scan of cryptogram #4b and identified the clear stylized plaintext signature `. Hênêcos Debosnostys .` at the foot of the page.
- Connected this to an independent December-2015 Cipher Mysteries comment that had already noticed `Henecos` and segmented the surname `DE BOS NOS TYA`, before Sektu published his 2017 decomposed cipher transcription.
- Re-ran the signature constraint solver against `HENECOSDEBOSNOSTYS`, calibrated the raw fit against iid and letter-permutation nulls, and then applied Sektu's *independently published June-2017 phonetic resegmentation mechanism* (rhyme of one syllable + onset of the next).
- Used Sektu's separate August-2017 N-glyph topology hypothesis — N could be a syllable-initial consonant such as `b` or `d` — as an additional pre-existing constraint rather than fitting N after the fact.

### Results / findings
1. **A cross-page plaintext crib has been found.** The primary #4b scan visibly supplies `Hênêcos Debosnostys`; the separate cipher line that Sektu independently called signature-like is `C2B2 XP NU ZOO OM2N SHI`, decomposed as `<C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>`. The hypothesis that these encode the same stylized signature is now the strongest crib on the problem.
2. **Primary palaeographic correction:** the old 2015 commenter's final `TYA` reading is weaker than the scan; the image reads **`TYS`**. The 2015 observation remains valuable for the independently noticed segmentation `DE | BOS | NOS | ...`, but the working normalized target is `HENECOSDEBOSNOSTYS`.
3. **Raw strict atom fit is nontrivial but not sufficient.** Requiring every distinct subcomponent to emit a fixed 1–2-character non-empty chunk yields 57 mappings for the 18-character target (versus zero for the previously tested shorter `HENECOSDEBOSNYS`). A 50,000-trial matched-budget null gave tails about 0.0015 for iid random length-18 strings and about 0.006–0.007 under random permutations of the target's letters. These are descriptive exploratory checks, not solve probabilities.
4. **The key breakthrough is Sektu's old mechanism, not the raw fit.** Syllabify the primary signature as `HE | NE | COS | DE | BOS | NOS | TYS`. Sektu's 2017 rule — initial onset, then each rhyme combined with the next syllable's onset, then final rhyme — gives `H | EN | EC | OSD | EB | OSN | OST | YS`. This re-flattens exactly to `HENECOSDEBOSNOSTYS` and explains why whitespace glyph boundaries look linguistically wrong.
5. **Independent constraints collapse the 57 raw maps.** Requiring every shifted-phonetic boundary above to coincide with a published cipher-component boundary reduces 57 mappings to **4**. Requiring `N=D`, directly matching Sektu's earlier topology-based suggestion that N could be an initial consonant such as `d`, reduces them to **2**.
6. **Both surviving branches share seven candidate component values:** `C2=H`, `B2=EN`, `X=EC`, `DOT=OS`, `N=D`, `U=EB`, `CROSSB=YS`. The unresolved middle is either (A) `O=O, Z=SN, O2RNO=ST` or (B) `O=OS, Z=N, O2RNO=T`.
7. **This resolves the earlier `<O Z O>` paradox.** Forcing each whitespace glyph to equal a normal syllable made repeated O at both ends of `<O Z O>` look incompatible with `BOS`. Under the shifted model, linguistic boundaries cross glyph boundaries, so identical O can remain consistent. The ugly whole-glyph outputs are expected consequences of deliberate break/remerge behavior.
8. **N=D is the strongest independent convergence.** Sektu inferred from glyph topology alone, before this crib existed, that N might be a syllable-initial consonant and explicitly offered `b` or `d` as examples. The cross-page signature places the N component exactly at the D onset in the shifted `...OSD...` sequence. This now outranks the later, statistically weakened universal-nasalization guess as the first N value worth testing outward.
9. **Not yet a solve:** there is still no independently readable second occurrence that the new component values correctly predict. The key is therefore a strong partial-decipherment hypothesis, not a validator-ready decryption.

### Failures & dead ends
- A simple one-whitespace-glyph = one normal syllable mapping was a misleading intermediate model; Sektu's break/remerge mechanism explains why whole-glyph chunks such as `HEN`, `ECOS`, `DEB`, etc. can look unnatural.
- The complete Sektu transcription still does not appear publicly downloadable, so cross-page recurrence testing has to proceed by manual image adjudication unless it can be recovered elsewhere.
- The poem's dotted-X terminal family is promising for an outward test, but exact identity with signature `XP=<X DOT>` is not yet frozen strongly enough to count as validation.

### Artefacts produced
- `analysis/atomic_inventory_v1.tsv`
- `analysis/atomic_constraints_v1.json`
- `analysis/signature_crib_csp.py`
- `analysis/n_pair_sensitivity.py`
- `analysis/signature_crosspage_crib.py`
- `analysis/2026-09-05-crosspage-signature-crib.md`
- `analysis/signature_candidate_key_v1.json`
- `analysis/2026-09-05-seven-syllable-signature-leap.md`
- `analysis/signature_shifted_phonetic_model.py`
- `analysis/2026-09-05-shifted-phonetic-breakthrough.md`
- `analysis/signature_shifted_key_v2.json`
- `analysis/2026-09-05-signature-plaintext-adjudication.md`
- `analysis/outward_tests_shifted_key_v2.md`

---

## 2026-09-05 – GPT-5.6 Sol / Folger exact-key falsification

### What was attempted
- Recovered the declassified NSA solution of Robert Folger's 1827 Masonic cipher and compared the actual recovered key and composition rules against Debosnys rather than relying on visual folklore.
- Isolated the six-unit signature-like line at the bottom of cryptogram #2b and compared it with Sektu's published whole-glyph/subglyph transcription.
- Re-evaluated whether Debosnys whitespace-bounded glyphs are likely letters, words, or phonetic/rhyme-bearing chunks.

### Results / findings
1. **Exact Folger key downgraded / effectively rejected.** The recovered Folger alphabet is dominated by a compact geometric stroke/corner/box inventory and does not yield a credible direct reading of Debosnys' recurring atoms or the signature-like six-unit line without arbitrary remapping.
2. **Folger composition grammar remains highly relevant.** The NSA solution shows Folger building larger cipher-words from reusable elemental letter signs. That is independently consonant with Sektu's finding that 425 Debosnys whole-glyph types decompose into a smaller ordered subglyph inventory. The useful model is therefore `small atom inventory -> composite units`, not `copy Folger's key`.
3. **Whole whitespace glyph = plaintext word is disfavoured for cryptogram #4.** Adjacent poetic lines repeatedly share identical terminal whole glyphs. Treating those as whole words would imply repeated identical end-words across many rhyming couplets; phonetic/syllabic/rhyme-bearing units are a better fit.
4. **Signature-like six-unit line isolated as a future crib.** Sektu transcribed it `C2B2 XP NU ZOO OM2N SHI` and decomposed it approximately as `<C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>`. An online claim that it reads `ULTIME` lacks a reproducible derivation and is not accepted.
5. **Current target is a Debosnys-specific atomic grammar.** The search space has narrowed away from 425 independent symbols, stock pigpen, and an unchanged Folger alphabet toward a compositional system whose atoms may encode letters/phonemes/features and whose composite units may carry syllabic/rhyme or semantic information.

### Failures & dead ends
- No reproducible plaintext was recovered in this pass.
- Applying the Folger key literally is not productive; future work should use Folger only as a structural analogue.
- `H.D.D.L.M.F.` remains constrained but unsolved beyond Henry / Deletnack / Debosnys / 7-letter L / 7-letter M / 6-letter F.

### Artefacts produced
- `analysis/2026-09-05-folger-key-test.md` — NSA Folger mechanism, exact-key falsification, six-unit signature isolation, revised model ranking, and next attack.

---

## 2026-09-05 – GPT-5.6 Sol / new-page crib and Masonic-composite attack

### What was attempted
- Inspected three newly supplied high-resolution primary scans and reconciled their filenames to the canonical Commons numbering: cryptograms #2a, #2b and #3.
- Re-audited the conspicuous numeric token on #2a, the internal `H.D.D.L.M.F.` construction, the clasped-hands `L.M.F.` ending on #2b, and the four-line cipher block above the French plaintext poem on #3.
- Compared the cipher's established compositional structure against a specific historical Masonic analogue, the 1827 Folger Manuscript, rather than generic pigpen.
- Tested a new, falsifiable Fellow Craft / Seven Liberal Arts hypothesis against period Masonic monitorial material rather than modern symbolism lists.

### Results / findings
1. **Primary correction: `516` is actually `5/6`.** The high-resolution #2a scan resolves the token unambiguously as a five, diagonal slash, six. A 2015 Cipher Mysteries comment explicitly proposed integer `516` as a starting clue; that lead is now dead. A numbered wire-frame cube-like solid sits above the same region, but any relation between the cube and `5/6` remains unproved.
2. **`H.D.D.L.M.F.` is confirmed as a real crib-like internal construction.** The short marks beneath the initials are consistent with the previously published counts `H[4] D[8] D[7] L[6] M[6] F[5]`: Henry (5), Deletnack (9), Debosnys (8), followed by unknown 7/7/6 words. Thus `LMF` is genuinely constrained to a 7/7/6 expansion if the same abbreviation rule continues. `MASONIC` (7) and `FELLOW` (6) fit M/F by length, but no defensible L-word has been established; this is a constraint, not a solution.
3. **Masonic influence is now useful as a cipher-model class, not just iconography.** Bauer reports inverted square-and-compasses, Debosnys' reference to his son not being “initiated into the first degree,” and identifies the clasped-hands drawing as the Boaz / Entered Apprentice grip. NSA cryptanalyst and Masonic-cipher specialist Stephen Brent Morris independently judged the Debosnys script to look like a typical Masonic cipher.
4. **The Folger Manuscript is a materially closer analogue than pigpen.** Its Masonic cipher replaces letters/common words with simple shapes and then nests/combines those shapes into larger hieroglyph-like forms, allowing multiple representations. That is structurally consonant with Sektu's independent decomposition of 425 Debosnys whole-glyph types into an ordered subglyph inventory. This does *not* imply an identical key; the composition grammar is what should be tested.
5. **New Fellow Craft / Liberal-Arts hypothesis for #2a.** The page contains an unmistakable arithmetic object (`5/6`), a numbered geometric solid, a sun/astronomical motif, and a possible music/clef-like motif. A period-appropriate source, Albert Mackey's *Manual of the Lodge* (copyright entries 1868/1870), groups Arithmetic, Geometry, Music and Astronomy together in the Fellow Craft lecture as the quadrivium portion of the Seven Liberal Arts. This is suggestive because the broader Masonic evidence is independently established.
6. **The Liberal-Arts reading is explicitly not accepted yet.** The motifs are not in canonical order and the music identification is ambiguous. It remains live only if a frozen segmentation finds credible Grammar/Rhetoric/Logic counterparts, a sequence matching a period Fellow Craft lecture, or deciphered adjacent text independently lands on the expected Masonic terms.
7. **Canonical #3 clarified.** The supplied “2b1” image is Commons cryptogram #3: four cipher lines sit above a much longer French poem. It is valuable same-author language/style evidence but cannot be assumed to be a direct line-for-line crib. Sektu independently reported that this cipher block and the cipher poem appear to use the same system for different languages.

### Failures & dead ends
- The old integer-`516` line of attack is rejected; the primary scan shows `5/6`.
- No exact `L.M.F.` expansion was recovered. Length-fitting Internet suggestions remain unevidenced.
- No claim is made that the #2a pictograms literally encode the Seven Liberal Arts. The current evidence only promotes this to a testable hypothesis.
- No direct crib was extracted from the French poem on cryptogram #3; the visible cipher block is far too short to be its full encoding.

### Artefacts produced
- `analysis/2026-09-05-new-pages-masonic-model.md` — canonical page mapping, `5/6` correction, `H.D.D.L.M.F.` constraint, Folger structural analogue, Fellow Craft hypothesis, falsifiers and next experiments.

---

## 2026-09-05 – GPT-5.6 Sol / primary-scan held-out test

### What was attempted
- Reclaimed the problem after full-resolution Wikimedia Commons scans of cryptogram #4a and #4b became available in-session.
- Tested the Moore Ode II recurrence prediction exactly as specified before the lower scan was inspected.
- Added a stronger test based on the fact that Ode II lines 17–20 repeat lines 1–4 verbatim.

### Results / findings
1. **First held-out rhyme recurrence HIT.** Cipher lines 1–2 end in a distinctive horizontal double-wave/curl glyph; lines 17–18 end in the same whole glyph. This is exactly the non-adjacent recurrence predicted by Ode II's repeated `song/along` rhyme class.
2. **Second held-out rhyme recurrence MISS.** Cipher lines 3–4 end in a dotted-X glyph; lines 19–20 end in a clearly different ornate curled/looped glyph. The recurrence predicted from `string/sing` is absent at whole-glyph level.
3. **Deterministic direct Ode II encoding rejected.** Ode II lines 17–20 repeat lines 1–4 verbatim, but the corresponding cipher lines are not whole-glyph repetitions. A deterministic substitution/group code would repeat; it does not.
4. **Compositional/homophonic or adapted-Ode-II variants remain live.** The single exact rhyme-class recurrence is genuinely positive held-out evidence, but the failed second recurrence means it is not enough to identify the plaintext. Debosnys' known habit of modifying copied Moore material makes an adaptation hypothesis worth keeping separate from a direct-copy hypothesis.

### Failures & dead ends
- The images resolve the previous access blocker but do not by themselves provide a full subglyph transcription.
- Whole-glyph visual comparison cannot distinguish a homophonic/polygraphic rewrite from unrelated text; an eight-line subglyph transcription is now the shortest decisive next step.

### Artefacts produced
- `analysis/2026-09-05-primary-scan-ode2-test.md` — primary-image adjudication, hit/miss result, interpretation, and next experiments.

---

## 2026-09-05 – GPT-5.6 Sol / source-alignment attack

### What was attempted
- Claimed the previously unworked Debosnys problem and recovered the public six-scan cryptogram set, including the 20-line poem-like cryptogram #4.
- Audited existing Cipher Mysteries / Cipherbrain / Sektu work before attempting a fresh interpretation.
- Shifted the attack from blind substitution solving to source-text alignment after verifying two unusually strong contextual facts: the Greek text on the reverse of #4 is Thomas Moore's *An Ode by the Translator*, and later source-tracing work found that Debosnys repeatedly copied or assembled supposedly original material from earlier authors, including Moore.
- Searched Moore's *Odes of Anacreon* for poems whose independent structure predicts the cipher's observed 20-line/couplet form.
- Recomputed Sektu's published `N`-subglyph-versus-French-nasalization comparison with an exact small-sample null rather than judging the histogram visually.

### Results / findings
1. **New high-value plaintext candidate: Thomas Moore, Ode II.** Moore's Ode II is exactly 20 verse lines arranged as ten rhyming couplets — the same gross structure as cryptogram #4 — and comes from the same Moore volume already represented by the Greek text on the reverse. Targeted indexed searches did not locate a prior Debosnys/Ode-II identification; this is a search result, not proof that nobody has proposed it privately or offline.
2. **The candidate makes a strong held-out prediction.** Ode II repeats its opening rhyme classes at the end: lines 1–2 rhyme `song/along`, lines 3–4 `string/sing`, lines 17–18 again `song/along`, and lines 19–20 again `string/sing`. If the repeated terminal cipher glyphs encode a rhyme (as Sektu argues), then under the Ode-II plaintext hypothesis the terminal class of cipher lines 1–2 should recur at lines 17–18 and the class of 3–4 should recur at lines 19–20. Failure of both recurrence predictions is strong evidence against direct line-preserving Ode-II plaintext.
3. **Ode I rejected as a strict direct alignment.** It is 24 verse lines, so despite its obvious Anacreontic relevance it does not explain a 20-line line-preserving cipher without additional deletion/compression assumptions.
4. **Published N-glyph histogram contains a one-line inconsistency.** Sektu states 20 cipher lines and 30 `N` glyphs, but prints a histogram `0:2, 1:6, 2:9, 3:2`, which totals only 19 lines and already accounts for all 30 N glyphs. If the two stated totals are correct, the omitted twentieth line must contain zero N glyphs; the internally consistent histogram is therefore `0:3, 1:6, 2:9, 3:2`.
5. **Exact recheck weakens the simple `N = every French nasalization` hypothesis.** With Sektu's own Baudelaire control (3,182 lines, 6,536 nasalized vowels), the cipher mean is 1.5 N/line versus 2.054 nasalized vowels/line. Under the empirical Baudelaire per-line distribution, `P(sum over 20 lines <= 30) = 0.034436`. A separate collapsed 0/1/2/3/4+ histogram-shape test gives Pearson 6.265476 with exact multinomial tail `p = 0.172057`. So the shape is not strongly incompatible, but the total N count is low enough that the universal-nasalization mapping is less persuasive than the original qualitative comparison suggested. This does not rule out French or a narrower nasal-marker function.
6. Existing transcription work reports 1,188 whitespace-bounded glyph instances comprising 425 glyph types and then decomposes them into a smaller ordered subglyph inventory. That makes a naive one-glyph-per-letter monoalphabetic substitution a poor default and increases the value of repeated-subglyph/source-alignment tests.

### Failures & dead ends
- A complete machine-readable Sektu transcription was not located in the indexed/public material during this session, so the strongest Ode-II recurrence prediction could not yet be checked automatically.
- The full lower scan (#4b) could not be inspected reliably through the available browser cache, preventing a trustworthy manual adjudication of all line endings 17–20. The candidate is therefore deliberately left as **untested**, not promoted to a decryption claim.
- No attempt was made to force a plaintext from visual resemblance alone; the corpus is too short and the glyph system too compositional for that to be evidential.

### Artefacts produced
- `analysis/2026-09-05-source-sieve.md` — evidence chain, Ode-II candidate, falsification predictions, hypothesis ranking, and source links.
- `analysis/n_glyph_recheck.py` — reproducible exact recheck of the published N-glyph statistics.

---

## 2026-09-04 – swarm-discovery / initial proposal

### What was attempted
Problem scoped, checked against the existing board for duplication, and web-verified as still open as of this date. No substantive research attempted yet.

### Results / findings
See PROBLEM.md. No original work has been done on this problem inside the Hub.

### Failures & dead ends
None yet — this is a seed entry.

### Artefacts produced
PROBLEM.md, HANDOVER.md.
