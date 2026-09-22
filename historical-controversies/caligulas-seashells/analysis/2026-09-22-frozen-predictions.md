# Frozen predictions — 2026-09-22, before any corpus count was run

Written and committed **before** the corpus was searched. The crawl of the Latin Library
was still downloading when this file was written; Perseus was cloned but ungrepped. No
`musculus` token count of any kind had been produced at the time of this commit.

Honesty note on what "prospective" means here. I am a language model: I carry prior
knowledge of Latin literature, so "I have not run the count" is not the same as "I have no
expectation". Every prediction below is therefore labelled with the source of its prior:

- **P-corpus** — a genuine quantitative unknown. I do not know the number and my prior is a
  wide interval. Failure is informative.
- **P-recall** — I expect a specific passage to exist because I have read Latin literature.
  Recovering it is a **pipeline check**, not a discovery; failing to recover it means my
  corpus is broken, not that the fact is false.

## The chain being tested

Woods (2000) requires, as I understand the argument prior to reading it in full:

- **L1 (ambiguity).** `musculus` is genuinely ambiguous in Latin between a shellfish and a
  military shelter, such that a reader could take the military word for the mollusc.
- **L2 (substitution).** Someone in the transmission then rendered that mollusc sense with a
  *different* word, `concha`, which is what stands in Suetonius.
- **L3 (fit).** The rest of Suet. *Calig.* 46 (`galeas et sinus replere`, `spolia Oceani`)
  is compatible with the resulting text having grown out of such a misunderstanding.

L1 and L2 are corpus-testable. L3 is not, and I will not pretend otherwise.

## Predictions

**1. Sense distribution of `musculus` (P-corpus).** Over the whole searched corpus I predict
the rank order: anatomical *muscle* > military *shelter* > shellfish > *little mouse*.
Interval predictions: military-sense tokens **10–40**; shellfish-sense tokens **1–8**;
shellfish tokens confined to **≤ 4 distinct authors**.
*Failure condition:* shellfish tokens > 15, or more shellfish tokens than military tokens.

**2. The crux (P-corpus): `musculus` is a marginal word for "mussel".** Latin's ordinary
words for shellfish are `concha`, `conchylium`, `mitulus/mytilus`, `peloris`, `ostrea`. I
predict `musculus` in the shellfish sense is **at least an order of magnitude rarer** than
`concha` in the same corpus, and rarer than or comparable to `mitulus/mytilus`.
*Why it matters:* L1 needs the mollusc sense to be available to a reader at all. If the
mollusc sense is a lexicographer's curiosity rather than live usage, L1 is weak — and the
weakness is quantitative, not rhetorical.
*Failure condition:* shellfish-sense `musculus` within a factor of 3 of `concha`'s frequency.

**3. Number in the military sense (P-corpus).** The military `musculus` is one large built
structure per operation. I predict **fewer than 35%** of military-sense tokens are plural,
and that the plural ones cluster in late/derivative authors (Vegetius, Isidore, glossators)
rather than in the narrative sources. Woods's reconstruction needs a plural order.
*Failure condition:* plural share ≥ 50% including in Caesar-era narrative.

**4. Governing verbs in the military sense (P-corpus).** I predict the verbs governing a
military `musculus` are overwhelmingly verbs of *building and moving*
(`ago`, `facio`, `struo`, `aedifico`, `promoveo`, `subicio`, `applico`) and that **`legere`
never governs it** — `legere` is the verb Suetonius actually uses.
*Failure condition:* any attestation of `legere`/`colligere` + military `musculus`.

**5. Suetonius's own technical register (P-corpus).** If Suetonius is the kind of writer who
mishandles siege vocabulary, he should use little of it. I predict his rate of siege-technical
nouns (`vinea, testudo, pluteus, aries, agger, musculus, crates, cuniculus, ballista,
scorpio, tormentum, onager`) per 10,000 words is **below one-fifth** of Caesar's rate.
*Failure condition:* Suetonius within half of Caesar's rate.
*Note:* this cuts both ways by design. A low rate makes Woods's misunderstanding easier; it
does not make it actual.

**6. The base rate that decides how much L1 is worth (P-corpus) — the null model.** Roman
siege and naval engineering names its devices after animals and household objects as a
*system*: `testudo`, `aries`, `corvus`, `scorpio`, `onager`, `cuniculus`, `vinea`, `lupus`,
`ciconia`, `grus`, `asinus`, `apri`(?), `musculus`. I predict that of a pre-specified list of
Roman siege/naval device names, **at least 60%** are homonyms of an animal or ordinary object.
*Why it matters:* if ambiguity is the norm, then "this military word is ambiguous" has a
likelihood ratio near 1 and carries almost no evidential weight for Woods. The whole
argument would then rest on L2 alone.
*Failure condition:* under 40% homonymous, in which case `musculus` is genuinely unusual and
L1 does carry weight.

**7. `conchas legere` as idiom (P-corpus).** If gathering shells on a shore is an ordinary
Latin thing to say, Suetonius's clause is unremarkable Latin and needs no emendation to be
intelligible. I predict `concha` is attested as the object of `lego`/`colligo` or in a
shore-gathering context **at least once** outside Suetonius.
*Failure condition:* no such attestation anywhere in the corpus, which would make the phrase
odd and give Woods a positive argument I had not credited.

**8. L2's one positive test (P-corpus).** If `musculus`(shellfish) and `concha` occur in the
*same passage* as members of one shellfish list, a paraphrast could substitute one for the
other and L2 is supported. I predict **at least one** such co-occurrence.
*Failure condition:* none — which would leave L2 with no attested basis.

## Pipeline checks (P-recall — these test my corpus, not the hypothesis)

- Caesar, *Bellum Civile* 2.10 contains an extended technical description of a `musculus`.
  If my corpus does not return it, my corpus is broken.
- Vegetius, *Epitoma rei militaris* book 4 discusses the `musculus` among siege works.
- Every locus that Lewis & Short cites under `musculus` should be recoverable, or its absence
  explained by a coverage gap I can name. Coverage will be reported as a fraction, not asserted.

## What I will not claim

I cannot test L3, and no corpus count can establish what a first-century source document
said. The most this session can deliver is a quantified statement about how much work each
link in the chain can bear. If the answer is "the passage underdetermines this", that is the
finding and it will be reported as such.
