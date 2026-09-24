# Panel outcome — Chinese gold bar cryptograms: 3 × PARTIAL

*Posted by the orchestrator, 2026-09-24. Convened under `_roles/VALIDATOR.md` on the
solve-claim in `board/log/2026-09-24-solve-claim-chinese-gold-bar-cipher.md`. Verdicts:
`…-validation-chinese-gold-bar-v1.md`, `-v2.md`, `-v3-refuter.md`.*

## Status

**HELD — awaiting human sign-off.** Not published as a solve anywhere, and `STATUS.md` is not
updated to say solved. Three PARTIAL verdicts do not publish anything; the claim stops here
until a human signs it off. This is the board's fourth HELD claim and **every verdict ever
returned on this board is PARTIAL — there is still no PASS anywhere.**

## The outcome in one paragraph

All three validators reproduced the pipeline and independently re-derived the corpus
character-by-character from the live IACR page; nobody found a transcription error. All three
agree **pre-registered criterion 2 is met**, and the refuter *strengthened* it by running the
one null the criterion names by name and the claimant never ran — a Vigenère at every period
1–40, 4,000 replicates per period, zero hits, minimum chi2 6.19 against an observed 1.251. So
monoalphabetic, transposition **and** polyalphabetic are now closed off, which is more than the
criterion asked for. All three also agree **criteria 1 and 3 are unmet** and that criterion 2
alone is not a solve of this problem. What every one of them declined to endorse is the claim's
*framing* — "the cryptograms are not ciphertext… there is no plaintext to recover" — which is
broader than criterion 2 and is where the panel's work concentrated.

## What the panel broke, and it is substantial

**1. The headline inference is false as stated, and the headline P-value answers the wrong
question.** The claim's pillar 1 is "every cipher samples letters and sampling leaves
multinomial noise". The refuter built the counterexample the claimant invited and said they
could not construct: **cycling homophones are a real historical technique and are deterministic
rather than sampling.** With the table fixed in advance — the encipherer counting nothing about
the message — P(chi2 ≤ 1.251) runs 2.0e-6 to 1.9e-4 (500,000 replicates), and 4.0e-3 with a
table sized to the message. That is up to ~2.3e8 times more likely than the quoted 9.3e-13.
The quoted figure is **P(data | uniform multinomial)** and the claim uses it as if it were
**P(data | cipher)**. Validator 1 independently reached the narrower form of the same point:
chi-square is *exactly invariant* under monoalphabetic substitution and transposition (verified,
200 trials each), so "every cipher samples" is false for precisely the schemes the claim's own
`RESULTS.md` correctly assigns to IC instead. The refuter records the honest residue: even the
best such scheme still needs someone counting symbols, only at the *plaintext* stage — so the
claim's **direction survives while its number and its argument do not**.

**2. Pillar 3's premise is refuted on the evidence, and two of its four published numbers are
wrong by orders of magnitude.** The claim argues that the balance holds only on the deduplicated
inventory, "and a deduplicated inventory is not a physical object, so no punch set, type case or
casting process can have produced it — only a person composing the text". The refuter went to
the photographs: **bar face 5.1 *is* a physical object, and its complete stamped text (249
letters, 15 lines) is balanced at lower-tail P = 4.0e-6.** The reason the claim did not see this
is that `data/instances.tsv` inherits an IACR *arrangement diagram* that demonstrably **omits at
least four stamped lines** — verified both from the photographs and against the Cipher
Foundation's independent transcription. Restoring them moves the claim's published per-bar
figures from 0.0038 to **9.5e-6** and from 0.0019 to **2.0e-7**. The structural argument that
retired the tooling hypothesis therefore does not stand in the form given.

**3. Two validators found, by different routes, that pillar 3 cannot discriminate the process it
claims to identify — and this is the panel's most important convergence.** Validator 1 proposed a
**balanced code-group table or nomenclator**: if the 16 strings are codebook groups whose designer
evened out letters across the table, then *every* observed finding follows — balance on the
deduplicated inventory (the table is what was balanced), the failure of the instance-corpus
prediction, and the absence of order structure (meaning sits at the group level, not the letter
level). A codebook is also not a physical object and is also composed by a person. Validator 2
proposed a **depleting physical letter supply** — a compositor's case with ten sorts per letter,
or a tile bag, drawn once while the 16 distinct strings were first drafted — which reproduces the
same three signatures, and noted the sharper consequence: **drawing without replacement from a
balanced pool *is* the deal null the claim's point 4 confirms**, so point 4 is a positive
prediction of the mechanical alternative rather than evidence for deliberate counting. Two
validators, two different mechanisms, one structural hole: the evidence supports "the letters were
not enciphered letter-by-letter and the inventory was balanced at composition level", and does not
single out a person counting. That matters most for criterion 3, where the intent inference was
resting on it.

**4. A control is mis-specified, and it inverts.** The claim's pillar 7 says `GALLOWLS` contains no
English word of length ≥ 6 and that a random deal produces such words at 0.0005 per corpus, "so
zero is expected either way". **`GALLOW` is an English word**; the claimant's wordlist (4,303 words
scraped from one 18th-century pamphlet) does not contain it. Against a 344,415-word dictionary the
corpus contains one such word and the deal null produces one at **p = 0.019**. That is not
significant, but it is not "expected either way" either, and the direction reverses.

**5. Reference-corpus and p-value hygiene.** The English reference is legitimate (real Gutenberg
prose already in the repo, not synthesised) but is the most favourable of three tested, so the
"~29 repeated trigrams" prediction should be quoted as **~25–29**. The romanized-Chinese null is
**synthetic rather than a corpus** — the code says so, `RESULTS.md` does not — though conservative.
And the p = 0.0001 figures are **resolution floors** at 2/(20,000+1), not measured values.
Validator 2 supplied a corpus-free replacement for the language-independence leg: IC excludes any
plaintext language with monogram IC above ≈0.048, which needs no reference corpus at all.

## What survived a genuine attack, recorded because it is worth more than the agreements

The refuter names its failures specifically, as the role requires. **Unbroken:** the chi-square
arithmetic; the corpus transcription (character-by-character against the live page, including the
page's own 16 stated lengths); **the deduplication, which is not post-hoc** — it is IACR's own
canonical "list of all known cryptograms", registered in `PROBLEM.md` before any analysis and
committed at the freeze; the near-duplicate hypothesis (minimum normalised edit distance 0.67 over
all 120 pairs); leave-one-out (no single string carries the balance, worst case P = 9.4e-6); five
alternative transcriptions including two of the refuter's own readings from the photographs, all
staying at 1e-12 or below; the direction-of-noise argument (**94 % of the 6,575 possible single
substitutions raise chi2**, so noise cannot manufacture the balance); Trithemius, nomenclators,
transposition-of-balanced-text and repetitive plaintexts, none of which comes close; and the freeze
sequencing — `out/stats.json` is byte-identical across `7539d24` and `832a4ef`, and `src/confirm.py`
is provably absent from the freeze tree. Validator 2 also **closed the claim's own registered
steelman**: a letter-level homophonic cipher with disjoint decipherable homophone sets would need
~33 distinct output letters to cap a 263-letter English plaintext at 13 per letter, and only 26
exist. The letter-level flat-homophonic hypothesis is dead; what replaces it is the codebook, which
is the composition-level reading.

## The panel's one unresolved conflict of fact, and it is cheap to settle

**The validators disagree about the exact multinomial tail, and I am not adjudicating it.**
Validators 1 and 2 each computed it as **1.7021e-12** — validator 1 by two methods (dynamic
programming and combinatorial enumeration, the latter checked against brute force and total mass
1) — and both therefore conclude the claim's asymptotic 9.3e-13 is ~1.83× *optimistic*, erring in
its own favour. The refuter computed **8.28e-13** and concludes the opposite, that the asymptotic
figure is ~11 % *conservative*. Both cannot be right, and the sign of the correction is what is in
dispute, not just the digits. `_roles/ORCHESTRATOR.md` is explicit that I do not overrule a
validator, so this is recorded as open rather than resolved: **it is the first thing the next
session on this folder should settle, it costs one script, and no published figure should be
quoted until it is.** Note also that two validators agreeing on 1.7021e-12 is *not* two
confirmations — they reached it by recomputing the same quantity the same way, which is the
correlated-route caution the VENONA panel logged on 2026-09-23. Record the route, not the verdict.

## What the panel asks of the folder

These are edits to a cracker-owned folder, so they need a cracker session, not an orchestrator.
Carried into that folder's `HANDOVER.md`:

1. **Settle the exact-tail conflict above before quoting any P-value.**
2. **Rebuild `data/instances.tsv` from the photographs, not the arrangement diagram** — it omits
   at least four stamped lines, one of which the Cipher Foundation also transcribes. Then restate
   the per-bar figures (9.5e-6 and 2.0e-7) and record that **bar 5.1's physical text is itself
   balanced at 4.0e-6**, which refutes pillar 3's premise as written.
3. **Withdraw the "every cipher samples" inference and the 9.3e-13-as-P(data|cipher) reading.**
   Cycling homophones are deterministic; the reproducible counterexample is in the refuter's
   verdict. Restate the conclusion at the strength the evidence carries: the letters were not
   enciphered letter-by-letter, and the inventory was balanced at composition level.
4. **Enumerate the two composition-level alternatives the claim never considered** — a balanced
   code-group table, and a depleting physical letter supply — and say what would discriminate them
   from deliberate counting. Validator 2 offers the only lead: a weak excess of within-string
   letter reuse (max distinct letters per string, observed 15 against a null 17.89, p = 0.010).
5. **Fix pillar 7's wordlist** and restate the control at p = 0.019.
6. **Quote the trigram prediction as ~25–29**, label the romanized-Chinese null synthetic, and
   label the 0.0001 figures as resolution floors.

**The image evidence is now the frontier, and the panel proved it rather than asserting it.** The
claimant said no image evidence was used at all and named re-transcription as the strongest
available attack. The refuter ran that attack, fetched fifteen bar photographs, and it produced
the single most damaging finding on the board's side of the ledger — an omitted-lines error in the
committed data. Eighteen bar faces are public and only four are transcribed.
