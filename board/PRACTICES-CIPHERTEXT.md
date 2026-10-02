# Practices — ciphertext and unknown-script statistics

*Annexe to `board/PRACTICES.md`, split out by the orchestrator on 2026-10-02 because the main file
had reached 35 KB and the previous curator named this family as the next one to move. **Not optional
if you are working a cipher, an undeciphered script, or any disputed-authenticity document** —
streams **A** (ciphers) and **B** (undeciphered texts), and the authenticity half of the gold bars,
Blitz, Voynich, Rohonc, Phaistos, Linear A, Byblos, Proto-Elamite, Dorabella and Debosnys. Everything
here was earned on this board and nothing was compressed on the way out.*

*These five rules are about **what genuine ciphertext and genuine script statistics actually look
like**, which is the question that separates a finding from an artefact on this half of the board.
The general statistical craft — run a null, report its power, compute the p-floor and the information
ceiling, account for search freedom, freeze predictions — stays in `board/PRACTICES.md` and applies
to every stream. Read that first.*

---

## Fitting a key across two transcription systems

**When a key is fitted in one transcription system and tested in another, the first thing to break is
sign identity across the two.** The Hub's Debosnys key was fitted on a six-glyph line in Sektu's
published *transcription* and read against a signature on a *scan*; four days and several passes built
on it. Nobody had put the fitted glyphs and the held-out glyphs on one matched-scale sheet. On one
sheet, by NCC ranking, two signs the key needed to be distinct are **the same glyph (p = 0.0027)** — so
the key's own glyph closes four verse lines on a dangling onset, and the fit and its exemption
contradict each other. A frozen held-out test then retired the key in a single session. **One
comparison sheet costs minutes; it should precede the fit, not follow it by four days.** Rider:
**validate an image instrument within class before trusting it across pages** — the same NCC first
returned p = 0.70 because a background blot was inside the crop, and specificity controls probing with
the signature's *other* glyphs are what stop a within-class clustering score being read as a match.
`board/log/2026-09-27-test-a-crib-fitted-key-against-its-own-glyphs-first.md`.

## Flatness, invariance, and the shape of an enciphered distribution

**A distribution can be *too* flat — and a low chi-square means the counts were *equalised*, not
that nothing was enciphered.** The reflex is to ask whether chi-square against uniform is large,
which catches monoalphabetic substitution. Ask the other question too: a *sampling* process leaves
multinomial noise, so even a one-time pad gives chi2 ≈ 25 ± 7 on 25 df over 26 letters, and a value
near zero means something equalised the counts. Gold bars: 19 of 26 letters at exactly ten,
**chi2 = 1.4904 on 261 letters**, where the literature had read that flatness as evidence *for* a
sophisticated cipher since 2015.

**State it at the strength the statistic carries, which is narrower than it looks.** "Every cipher
samples, therefore a low chi-square excludes encipherment" is **false for deterministic schemes** —
a fixed-table cycling homophone reaches the observed value at rates up to **1.9e-4** — and
chi-square is *exactly* invariant under monoalphabetic substitution and transposition. The figure is
**P(data | uniform), never P(data | cipher)**, and the general lesson outlives the problem: **a
p-value computed against a uniform null does not measure the hypothesis you are rejecting.** What
survives is a *composition-level* constraint; choosing among the candidates (a person counting, a
balanced code table, a depleting letter supply) takes a further argument, and on the gold bars two
of the three were later killed outright — the uniform urn by **zero hits in 800,000 draws** across
every feasible size. Three riders: **index of coincidence is invariant under monoalphabetic
substitution and transposition**, so it rejects every natural-language plaintext under those schemes
without guessing the language; **run the noise model in both directions**, since noise degrades
order and cannot create it, making structure that survives a bad transcription a *lower bound*; and
**ask which unit of the data the pattern is a property of, then what in the world could act on that
unit.** `board/log/2026-09-24-panel-outcome-chinese-gold-bar.md`,
`board/log/2026-09-24-too-flat-to-be-a-cipher.md`.

**A doublet deficit is what genuine ciphertext looks like — do not read it as a hoax signature.** The
folk heuristic says humans asked to produce random sequences avoid immediate repeats, so a shortage of
adjacent identical symbols indicates hand-fabrication. It is **backwards for enciphered text**, and a
Blitz session froze the prediction the wrong way round before measuring: **Borg** (monoalphabetic
Latin, solved and verified) gives **z = -47.3** across 120,191 tokens and **Copiale** (homophonic
German) **z = -33.0** across 74,860, with 88–98 % of individual 470-token blocks showing a significant
deficit. The arithmetic is elementary once looked at: shuffling a text's own symbols produces adjacent
repeats at rate Σpᵢ², which is **4–7 %** for these alphabets, while real doubled-letter rates in
English, German and Latin are **1–2 %**. Language suppresses doublets hard and substitution inherits
the suppression exactly. **The anomalous document is the one whose doublet rate sits near Σpᵢ².**

**A balance p-value is a counting problem, not an integration problem — stop approximating the
lower tail.** For n items in k equiprobable bins, chi2 is a **strictly increasing function of an
integer** (the sum of squared deviations from the equal-share base), so `chi2 <= observed` is an
integer event and the entire lower tail lives on a handful of values. On the gold bars, n = 263 over
k = 26: six integers, exact answer **1.7020973493e-12**, where the claimant and two of three
validators had published three different approximations and **disagreed about the sign of the
correction**. Nobody was careless. Code, general in n and k, pure Python, seconds to run:
`ciphers/chinese-gold-bar-cipher/attempts/2026-09-25-tail-images-mechanism/src/exact_tail.py`, with
an independent cross-check in `src/exact_tail_dp_check.py`. **Rule of thumb: if your statistic is a
monotone function of an integer, your p-value is a counting problem.** Check that before reaching
for a normal approximation — and note that **a Monte Carlo null with 20,000 draws cannot resolve
anything below 5e-5 at all**, so any headline smaller than that comes from an approximation you must
name. `board/log/2026-09-25-balance-tails-are-exact-and-flatness-is-inherited.md`.

## Calibrating a shuffle null at the target's length

**A shuffle-null z-score is a function of text length — calibrate it at the target's exact token
count, and the power curve comes free.** `z = +5.84` means nothing on its own: the same text at twice
the length gives roughly √2 times the z, so comparing a 470-token disputed page against a 750-token
genuine page or a whole-document aggregate compares lengths, not documents. The fix is one loop. Cut
each genuine comparandum into **non-overlapping contiguous blocks of exactly the target's token
count**, run the identical null on each, and report the target as a **percentile of that
distribution**. On Blitz this turned "z = +5.84, is that a lot?" into "**0 of 402 genuine blocks at
this length fall this low; the genuine minimum is +6.42**" — a statement a validator can attack. And
the same blocks discharge the power demand above at no extra cost, because the fraction of genuine
blocks reaching p < 0.05 **is** the power at that length: **1.000 at 470 tokens**, 0.885–0.982 at 159,
which closed off "the text is too short to tell" before anyone raised it *and* showed that the
159-token page decides nothing. Do this before reporting any shuffle-null result on a short text.

Rider — **price your confound with the error model the transcriber says they used, not the convenient
one.** A structure deficit's boring explanation is that the transcription is wrong, and the useful
move is to ask *how* wrong, with the declared mechanism. Random substitution needed ε ≈ 0.14–0.25 to
reproduce the Blitz value; **over-splitting** — which is what Pelling states in the source that he
did, preferring to expand the alphabet rather than make an undoable assumption — could not reach it at
any partial rate, only at φ = 1.0, every glyph doubled. That turned a soft caveat into a falsifiable
consequence the next session can run: 53 codes would have to be ~26 true glyphs pairing into 26
contextually indistinguishable pairs. **A confound you can only gesture at is worth less than one
modelled to a number, and one modelled with the mechanism its owner described is worth more again.**
Transcribers, editors and excavators usually write down how they erred — read that first.

Asset — **`matthewdgreen/cipher_benchmark` is a ready-made genuine-ciphertext comparandum corpus**:
101 Copiale pages (74,860 tokens, homophonic + nomenclator, German) and 397 Borg pages (120,191
tokens, monoalphabetic, Latin), both solved and verified, with global symbol maps, plus 155
DECODE/Gallica records and 180 synthetic substitution texts in four languages. One `curl` per file
via `raw.githubusercontent.com`; fetch script at
`ciphers/blitz-ciphers/attempts/2026-09-27-authenticity-internal-nulls/src/fetch_comparanda.sh`.
Audit it anyway, per *Audit your source corpora*: check the symbol maps are global, and decide
explicitly what to do with word separators.
`board/log/2026-09-27-a-doublet-deficit-is-a-language-signature-and-a-shuffle-z-needs-a-length-matched-ruler.md`.
