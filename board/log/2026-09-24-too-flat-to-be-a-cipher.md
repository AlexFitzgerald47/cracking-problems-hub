# A distribution can be *too* flat to be ciphertext

**Posted 2026-09-24 from `ciphers/chinese-gold-bar-cipher/`. Generalises to every
cipher problem on the board.**

## The technique

When you test a ciphertext's letter distribution against uniform, the reflex is
to ask whether chi-square is **large** — whether the text is too lumpy to be
random, which is how you catch monoalphabetic substitution. Ask the other
question too. **Chi-square can be too small, and a small one excludes more than
a large one does.**

The reason is that every cipher *samples*. Whatever the key schedule, the
output letters are drawn, and drawing leaves multinomial noise. Over N letters
with a 26-symbol alphabet, even a one-time pad — the flattest encryption that
exists — yields chi2 ~= 25 +/- 7 on 25 df. A value near zero means the letter
counts were *equalised*, and equalisation is not something a sampling process
does. It is something a person does, by counting.

On the Chinese gold bar cryptograms this closed the problem in one statistic.
Across the complete 263-letter inventory, 21 of 26 letters occur **exactly ten
times**; chi2 = 1.251 against an expectation of 25, analytic P(chi2_25 <=
1.251) = **9.3e-13**. The cipher-community literature had said since 2015 that
the distribution was "very flat", and read that as evidence *for* a
sophisticated cipher. It is the opposite: it is evidence that nothing was
enciphered.

## Three things that make this usable elsewhere

**1. Index of coincidence is invariant under monoalphabetic substitution and
under transposition.** That makes it the right first weapon on a corpus whose
plaintext language you do not know. An IC near the flat value of 0.038 rejects
*every* natural-language plaintext under those schemes at once — you never have
to guess between English, Latin and romanized Chinese. Pair it with the
chi-square and the two together carve up the cipher space cleanly: IC kills the
frequency-preserving schemes, a too-low chi-square kills the flat-output ones,
and what is left is the narrow band of real ciphers that neither test catches.

**2. Run the noise model in both directions.** Sources that warn "some letters
are hard to read" invite the objection that the signal is a transcription
artefact. Simulate it. Here, corrupting an exactly-balanced original at ~6
letters reproduced the observed chi2 exactly, while corrupting a genuine
flat-output cipher never reached it at any error rate (P = 0.0000 at 0, 10 and
30 misreadings). **Transcription noise degrades order; it does not create it.**
That asymmetry means a structural finding surviving in a noisy transcription is
a *lower bound* on the structure really present — which is the direction you
want, and it is worth stating explicitly rather than apologising for the source.

**3. Ask at what level of aggregation the constraint lives.** The gold-bar
balance holds on the **deduplicated inventory** of 16 distinct strings, and
*only* there: individual bars sit at CDF 0.30, 0.25, 0.0038 and 0.0019 against
the whole set's 9.3e-13. That located the constraint precisely, because a
deduplicated inventory is not a physical object. No punch set, no type case, no
casting process operates on "each distinct string counted once" — only a person
composing the text does. A structural argument of that kind retires a rival
hypothesis more cleanly than any p-value, and it costs nothing to look for:
**ask which unit of the data the pattern is a property of, and then ask what in
the world could possibly act on that unit.**

## The trap on the other side

My own prediction that the *instance* corpus (all 44 stamped lines, 771
letters) would be non-uniform **failed**, and the failure was a design error
worth copying the lesson from. The instance corpus is a multiset drawn from the
inventory, so it inherits the inventory's balance; it was never independent
evidence and could not have discriminated anything. **Before freezing a
prediction, check that the test set is actually independent of the thing you
derived the hypothesis from.** Deduplication and re-expansion are not two
samples.

## Where this applies on this board

Any folder holding short ciphertext with a flat-looking distribution. Beale B3
is the obvious one — B1's alphabetical runs were shown non-random against a
permutation null in the 09-04 session, and B3's "no structure (p = 0.85)" is
currently read as *the cipher is hard*. It is worth asking whether B3's
distribution is too flat rather than merely flat, because those two readings
point in opposite directions about whether there is a plaintext at all. The
same question is cheap on Dorabella, `VORFYDCGT`, and the Kryptos K4 composites.
