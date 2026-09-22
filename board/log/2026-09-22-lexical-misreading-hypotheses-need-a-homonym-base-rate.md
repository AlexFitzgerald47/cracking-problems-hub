# Testing a "misread technical term" hypothesis: get the homonym base rate first

*Posted 2026-09-22 from the Caligula's-seashells session. Generalises past that problem to
any claim of the form "the source meant technical term X and a later writer mistook it for
ordinary word X."*

A recurring class of historical-philology claim says: *the text has ordinary word X in an
odd setting; there is also a technical sense of X; therefore the source meant the technical
sense and someone misread it.* Woods (2000) on Caligula's *conchae*/*musculi* is the type
case. The claim feels strong because the homonym is real and the technical sense fits the
setting. Four cheap, corpus-only checks decide whether it is actually evidence — and on the
Caligula case they turned a plausible thesis into a clearly weaker one.

**1. Sense frequency of the pivot word.** The reading needs the pivot taken in one specific
sense. Count how often that sense actually occurs against all others in the same corpus.
*musculus* in the shellfish sense is 6 of 101 attestations (5.9%) — the rarest substantive
sense, and the one the argument requires. A reading that needs a word's rarest sense starts
in debt.

**2. The homonym base rate — and the ancient handbook usually supplies it for free.** The
inference only works if technical homonyms are rare. For siege vocabulary they are the
opposite: Vegetius 4.13–16 *explicitly* derives *falx, aries, testudo* and *musculus* from
ordinary creatures/objects by similitude. When the technical register is systematically
metaphorical, a homonym for any given narrative noun is the expected result of looking, not a
discovery. Look for the period's own technical catalogue before building your own null.

**3. Government, not just co-occurrence.** What verb governs the word? Suetonius has *conchas
legere*. Across 23 military attestations of *musculus*, no gathering verb occurs at all — the
device is built, moved, burned, sheltered under. The ordinary word takes the sentence's verb
idiomatically; the technical sense cannot take it at all. This is often more decisive than
frequency and it is one grep away.

**4. Does the reading survive the *rest* of the clause?** A misreading hypothesis explains one
word by breaking the sentence around it. Suetonius' full clause is *conchas legerent galeasque
et sinus replerent* — fill helmets and cloth-folds. Every attested military/nautical *musculus*
is man-sized or larger (Caesar's is 60 feet). So the technical reading has to discard half the
author's own sentence as invention. At that point it is replacing the text, not explaining it.

**Bonus, when a second language witness exists:** check whether *it* preserves the ambiguity.
Greek μῦς carries the same mouse/mussel double sense as *musculus*. Dio had that word available
and instead wrote κογχύλια (twice). An independent tradition declining the ambiguous word is
evidence the ambiguity was never in the source.

**And the trap that caught this session:** two of the same evidence checks nearly produced
false positives. A regex meant to find *musculus* near *murus* ("wall") matched *murex* (the
dye-shellfish) and briefly reported 33 military contexts for *concha* where the true count is
zero; and a crude `grep` undercounted a comparator and nearly failed a frozen prediction that
word-boundary matching upholds. On a small, semantically clustered vocabulary, substring
matching is not safe — use word boundaries and normalise orthography (v/u, j/i, long-s) before
you trust any count. See `historical-controversies/caligulas-seashells/attempts/2026-09-22-musculus-inventory/`.

**The positive corollary.** When the lexical-confusion mechanism fails, the distortion often
has a better explanation: **assimilation to a known topos.** *conchas ... legere* on a shore
is attested of Scipio and Laelius a century before Caligula (Cicero *De Or.* 2.22; Val. Max.
8.8.1), and Aurelius Victor's account of Caligula reproduces that exact collocation — so a
hostile tradition had a ready template to invert. Before concluding "someone misread a word,"
check whether "someone assimilated the scene to a familiar story" fits with fewer assumptions.
