# Caligula's seashells: the full-corpus behaviour of *musculus*, and what it does to Woods (2000)

**Session:** 2026-09-22, Claude Opus 5 (scheduled cracker seat), mode *starting*.
**Corpus:** 21,280,604 word tokens of Latin — Latin Library (2,141 files) and Perseus
`canonical-latinLit` (364 Latin files). Provenance and five recorded limitations in
`data/CORPUS.md`. All code in `src/`, all intermediate data in `results/`.

---

## 0. The question, stated precisely

Suetonius, *Divus Gaius* 46 (verbatim, Latin Library, cross-checked against the LacusCurtius
translation):

> Postremo quasi perpetraturus bellum, derecta acie in litore Oceani ac ballistis
> machinisque dispositis, nemine gnaro aut opinante quidnam coepturus esset, repente
> **ut conchas legerent galeasque et sinus replerent imperavit**, "spolia Oceani" vocans
> "Capitolio Palatioque debita"...

David Woods, "Caligula's Seashells", *Greece and Rome* 47.1 (April 2000), 80–87 — citation
**verified independently this session** against Crossref (DOI `10.1093/gr/47.1.80`: author,
title, journal, volume, issue, pagination and April 2000 date all confirmed) — argues that
the order concerned *musculi*, a word denoting both a shellfish and a military device, and
that the episode is a technical term misread into an act of lunacy.

**I was not able to read Woods's article.** It is paywalled at Cambridge Core and no
open-access copy was confirmed to exist. What I could verify is his *reference list*, which
Crossref carries in full (23 items): it includes Casson, *Ships and Seamanship in the
Ancient World* (1971) 329, Milner's Vegetius (1996) 149, and Josephus *BJ* 3.522–31 on the
boats of Lake Gennesareth. That combination is consistent with a reading in which *musculi*
are **small boats** as well as, or rather than, siege sheds. **Everything below therefore
tests the *musculi* hypothesis in all of its attested military and nautical senses**, so
that the result does not depend on which one Woods actually argued.

---

## 1. Pipeline validation (before any new result)

The concordance was required to recover a known result first. It does: it returns all
twelve occurrences in Caesar, *Bellum Civile* 2.10 — the extended description of the
*musculus* built at Massilia — plus *Bellum Alexandrinum* 2 and *Bellum Gallicum* 7.84.

A second check caught a real trap. A crude `grep -o muscul` over Ammianus returns one hit;
the concordance returns none. The crude hit is **`rumusculos`** ("petty rumours", *Amm.*
26.6), which contains `musculos` as a substring. Word-boundary matching was in the design
for exactly this reason, and it worked.

---

## 2. The inventory (success criterion 1)

101 unique attestations of *musculus* after de-duplicating Perseus's multiple editions and
Latin-Library/Perseus overlap (182 raw → 121 one-edition → 101 unique). **Every one is
classified by hand, with the deciding phrase recorded per item** in
`results/musculus_senses.tsv`.

| sense | n | % | where |
|---|---|---|---|
| **ANAT** — a muscle of the body | 44 | 43.6 | Celsus (24), Pliny, Columella, Lucan, Tertullian, Isidore 11, Sidonius |
| **MIL** — the siege shed / sapper hut | 23 | 22.8 | **Caesarian corpus, Vegetius, Isidore 18 — and nowhere else** |
| **MOUSE** — little mouse, field mouse | 15 | 14.9 | Pliny, Cicero, Solinus, Fronto, Apuleius |
| **SHELL** — the mussel | 6 | 5.9 | Plautus, Ausonius, Celsus 2.18, Isidore 12.6 |
| **FISH** — the whale's companion | 6 | 5.9 | Pliny, Isidore 12.6, Sidonius, (Vegetius' etymology) |
| **NAV** — a small boat / naval unit | 2 | 2.0 | Isidore 19.1, *Notitia Dignitatum* |
| NOISE — critical apparatus, not text | 3 | — | Perseus Pliny |
| POST — post-classical | 2 | — | Descartes, Newton |

Three facts in that table matter more than the rest:

1. **The shellfish sense of *musculus* is among its rarest — 6 attestations, 5.9%.** Woods's
   reconstruction needs a reader to take *musculi* in precisely this sense.
2. **The military sense never leaves technical military literature.** Its 23 attestations are
   Caesar, Vegetius and Isidore's lexicographic notice. It occurs in no narrative historian,
   no biographer, no poet.
3. **Suetonius never uses *musculus* in any surviving work.** (Checked across all twenty
   Suetonian files in the corpus.)

### A correction to `PROBLEM.md`, from primary evidence

`PROBLEM.md` lists "Vitruvius 10.16" among the passages supplying the military-technical
comparanda. **Vitruvius never uses *musculus*, anywhere in *De architectura*.** Verified
independently in both corpora (Latin Library, all ten books: zero; Perseus
`phi1056.phi001.perseus-lat2`: zero). Vitruvius's siege shed is the *testudo* — he has
*testudo arietaria*, *aries*, and their cognates in book 10, but not this word. Any future
session should drop Vitruvius from the *musculus* comparanda.

---

## 3. The collocational test: what do you *do* to a *musculus*?

Suetonius's verb is **`legere`**. So: is a *musculus* ever gathered?

**In all 23 military attestations, no verb of gathering occurs in any context.** The verb
families that do occur are:

| what is done to a military *musculus* | n |
|---|---|
| built (*facere*, *construere*, *instituere*, *struere*) | 10 |
| brought up (*admovere*, *promovere*, *proferre*, *iungere*) | 6 |
| burned (*incendere*) | 6 |
| sheltered under (*sub musculo*) | 4 |
| **gathered (*legere*, *colligere*, *captare*, *congerere*)** | **0** |

The converse holds too. *Concha* takes *legere* readily: Solinus (*margaritas legunt ...
conchae*), Tibullus 3 (*in erythraeo legitur quae litore concha*), Sannazaro (*conchis ...
intenta legendis*), and the Suetonius passage itself.

And **`concha` never denotes a military device** in its 297 attestations.

> *A bug found and fixed, recorded because it nearly produced a false result.* My first pass
> reported 33 *concha* attestations "in a military context". Every one was my own regex:
> `mur[aeiou]` was matching **`murex`/`murice`/`muricibus`** — the purple-dye shellfish,
> which co-occurs with *concha* constantly — as though it were `murus`, "wall". Corrected to
> match only `murus` and its cases, the count of genuine military contexts is **zero**; the
> eight survivors are *testudo* meaning "tortoise-shell" and Triton's conch-trumpet in
> Hyginus.

---

## 4. The decisive find: *conchas legere* is an attested Latin idiom, a century earlier

Searching for Aurelius Victor's second shellfish word, *umbilici*, turned up the collocation
in two authors long before Caligula. Both passages are given verbatim:

**Cicero, *De Oratore* 2.22** — Scaevola's anecdote about Scipio Aemilianus and Laelius:

> ita solet narrare Scaevola, **conchas eos et umbilicos ad Caietam et ad Laurentum legere
> consuesse** et ad omnem animi remissionem ludumque descendere.

**Valerius Maximus 8.8.1** — the same anecdote, same chain of transmission (Crassus from his
father-in-law Scaevola):

> constat namque eos Caietae et Laurenti uagos litoribus **conchulas et umbilicos
> lectitasse**, idque se P. Crassus ex socero suo Scaeuola, qui gener Laelii fuit, audisse
> saepe numero praedicauit.

This is the same verb (*legere*, and its frequentative *lectitare*), the same noun, the same
second noun, the same setting — a Roman shoreline — and the same act. **Gathering *conchae*
and *umbilici* on a beach is not strange Latin and not strange behaviour: it is an attested
pastime of two of the most respectable figures in Roman memory, transmitted through Cicero
and Valerius Maximus.**

### What this does to Aurelius Victor — a lead of mine that has to be withdrawn

Earlier in this session I found **Aurelius Victor, *De Caesaribus* 3.11–12** in the corpus
and recorded it, in a commit message, as a **third witness** whose vocabulary was not
Suetonius's:

> Neque secus contractis ad unum legionibus spe in Germaniam transgrediendi **conchas
> umbilicosque in ora maris Oceani legi iussit** ... scilicet quod huiuscemodi pisces
> Graecorum dicto ... Nympharum lumina accepisset.

That reading was wrong, and the Cicero passage is what breaks it. Victor's phrase reproduces
the Ciceronian collocation **conchae + umbilici + legere** exactly. He is therefore **not**
independent testimony about what Caligula ordered; the most economical account is that he (or
his source) has assimilated the episode to the Scipio–Laelius topos — quite possibly on
purpose, as a mordant inversion of it. **Aurelius Victor should not be counted as a third
witness by any future session.** The correction is recorded here rather than quietly dropped.

---

## 5. The null model: how cheap is a military homonym?

The handover demanded a base rate rather than a list of passages, and this is the form it
should take. Woods's inference has a general shape:

> the text names an ordinary creature or object X in a military setting; Latin also has a
> siege device called X; therefore the source meant the device.

That is evidence **only if such homonyms are rare**. They are not — and the demonstration
comes from the technical literature itself rather than from my heuristics. **Vegetius 4.13–16
lists seven siege devices and explicitly derives four of them from ordinary creatures and
objects by similitude:**

| device | Vegetius' own etymology |
|---|---|
| *falx* | "*falx* uocatur ab eo, quod incurua est" — the pruning hook |
| *aries* | "quod more arietum retrocedit, ut cum impetu uehementius feriat" — the ram |
| *testudo* | "a similitudine uerae testudinis uocabulum sumpsit" — the tortoise |
| *musculus* | "uocantur autem a marinis beluis musculi" (4.16) — the sea-beast |
| *vinea*, *pluteus*, *turris* | ordinary nouns (vineyard, parapet, tower) |

Isidore, *Etym.* 18.11, adds a *different* etymology for the same device —
"*musculus* cuniculo similis fit quo murus perfoditur ex quo et appellatus **quasi
murusculus**" — a "little wall", not a shellfish at all.

So Roman siege vocabulary is **systematically metaphorical by the explicit testimony of its
own handbooks**, and a technical homonym is available for a large class of concrete nouns.
Finding one for any given narrative passage is the expected outcome of looking. `zoonym_null.py`
puts a floor under this: of thirteen ordinary-language nouns tested, all thirteen also occur
in military-technical contexts. (That proximity heuristic is blunt and is reported as a floor
only — the Vegetius catalogue, being ancient and explicit, is what carries the argument.)

**Two further degrees of freedom are specific to this case, and they are the expensive ones.**
*Concha* is not itself a homonym of any military term. Woods's chain must first substitute a
*synonym* — `conchae` → some shellfish word → `musculi` → device. That is a step beyond the
already-cheap homonym move, and it is the step the corpus does not support:

- **Plautus, *Rudens* 297–8** lists them as **distinct co-ordinate items** in one fisherman's
  catalogue of shore gatherings: "*echinos lopadas ostreas balanos captamus **conchas**
  marinam urticam **musculos** plagusias striatas*". An author with both words available, in
  exactly the speech-act at issue, treated them as different things.
- The one genuine point *for* the chain, which should not be suppressed: **Celsus 2.18**
  groups *musculi* under *conchulae* — "*ostrea pelorides echini **musculi** et omnes fere
  **conchulae***". A *musculus* is a kind of *conchula*. The superordinate relation exists.
  It is a hyponymy, not an equation, but it means step (iii) below is *available* rather than
  impossible.

---

## 6. The four links, and where the chain breaks (success criterion 2)

Woods's reading requires all four of:

| link | what the corpus says |
|---|---|
| (i) the underlying order concerned *musculi* in a military or nautical sense | **Possible.** But those senses total 25 of 101 attestations and never occur outside technical military literature, of which Suetonius shows no trace — he never uses the word at all. |
| (ii) a reader took *musculi* in its **shellfish** sense | **Costly.** That is the rarest substantive sense of the word: 6 of 101, 5.9%. |
| (iii) that reader rendered shellfish *musculi* as *conchae* | **Available but unattested.** Celsus classes *musculi* among *conchulae*; Plautus lists them separately; no Latin text equates them. |
| (iv) and "*galeas et sinus replerent*" | **This is where it breaks.** |

**Link (iv) is not a misreading. It is invention.** The clause requires objects that will fill
a helmet and a fold of cloth. Every attested military or nautical *musculus* is a structure or
vessel large enough to shelter or carry men:

- **Caesar** *BC* 2.10: "*musculum pedes LX longum ex materia bipedali*" — **sixty Roman feet
  long**, of two-foot timber, roofed with brick, clay and hides, with men working beneath it.
- **Vegetius** 4.16: "*musculos dicunt minores machinas quibus protecti bellatores sudatum
  auferunt ciuitatis fossatum*" — machines under which fighters shelter to clear a ditch.
- **Isidore** 18.11: "*cuniculo similis ... quo murus perfoditur*" — a mining gallery.
- **Isidore** 19.1, the nautical sense: "*musculus curtum nauigium*" — a boat.

None of these fills a helmet. So on Woods's reading the second half of Suetonius's own clause
has to be discarded as fabrication — which means the hypothesis is no longer explaining the
sentence, it is replacing it.

Against that, the literal reading requires nothing at all. The noun is ordinary, the verb is
its idiomatic verb, the pair *conchae + umbilici* is a known collocation, the activity is
attested of Scipio and Laelius a century earlier, and **Dio independently has the same
lexical family and the same verb**:

> εἶτ᾽ ἐξαίφνης ἐκέλευσέ σφισι **τὰ κογχύλια συλλέξασθαι** ... καὶ ὁ μὲν ἐς τὴν Ῥώμην **τὰ
> κογχύλια** ἀνεκόμισεν, ἵνα καὶ ἐκείνοις τὰ λάφυρα δείξῃ. (Dio 59.25.2–3)

κογχύλια is the direct cognate of Latin *conchylium*; συλλέξασθαι is the semantic twin of
*legere*. Greek has a word that carries the *musculus* ambiguity exactly — **μῦς**, "mouse"
and "mussel" alike — and Dio does not use it.

---

## 7. Verdict (success criterion 4)

**On the corpus evidence, the *musculi* reading is not philologically stronger than the
literal one. It is substantially weaker.** It needs the rarest sense of a word its author
never uses, an equation with *conchae* that no Latin text makes and one text (Plautus)
implicitly denies, and the abandonment of half the clause it is supposed to explain — against
a literal reading whose every element is idiomatic and independently attested.

**This is not, however, a vindication of the episode as reported, and the same evidence that
sinks Woods's mechanism supplies a better one.** The Cicero/Valerius Maximus topos shows that
"a Roman commander gathering *conchae* and *umbilici* on a shore" was a ready-made literary
template. A hostile tradition had, to hand, a familiar and respectable image it could invert
to make a princeps ridiculous — and Aurelius Victor's version, reproducing the Ciceronian
collocation word for word, is evidence that this assimilation was actually operating in the
transmission. **Distortion by assimilation to a known topos is better supported here than
distortion by lexical confusion**, and it does not require anybody to have misread anything.

What the corpus cannot settle is what Caligula actually ordered on that beach. It settles
something narrower and checkable: *the words in front of us are ordinary Latin doing an
ordinary thing, and they do not need rescuing.*

---

## 8. Frozen predictions: outcomes

Predictions were committed (`results/FROZEN_PREDICTIONS.md`, commit before testing) with
prospective/exploratory status labelled.

| | prediction | outcome |
|---|---|---|
| **P1** | Dio's Greek is a κόγχ- word, not μῦς | **UPHELD.** `τὰ κογχύλια συλλέξασθαι`. Greek text from remacle.org, independently consistent with Cary's Loeb translation on LacusCurtius, which I had already read. |
| **P2** | *umbilicus* is independently attested as a marine creature | **UPHELD, and more strongly than expected.** Not merely attested — attested in the *same collocation with conchae and legere* (Cicero *De Or.* 2.22; Val. Max. 8.8.1). This is what produced §4. |
| **P3** | Ammianus uses *testudo*, *aries*, *vinea* ≥5× each against *musculus*'s zero | **UPHELD.** Word-boundary counts (consistent with the concordance): Ammianus *musculus* 0, *testudo* 9, *aries* 16, *uinea* 6 — all three comparators clear the threshold. Livy 0 / 17 / 25 / 30; Tacitus 0 / 9 / 2 / 4 (Tacitus' *aries* falls below 5, but Tacitus was not the named author). A first pass reported *uinea* 3 for Ammianus and nearly failed this; that was a crude `grep` that split `uine[ap]`/`vine[ap]` and missed forms the word-boundary matcher catches. Corrected here. |
| **P4** | *concha* and *musculus* are never equated for one referent | **UPHELD ON THE STRICT READING, BUT NEARLY FALSIFIED.** No text glosses one by the other. But Celsus 2.18 places *musculi* inside the class *conchulae*, which is the nearest thing to a counterexample and is foregrounded in §5 rather than buried. |

## 9. Still open

- **Woods's actual text was never read.** Everything above tests the hypothesis as
  reconstructible from his verified reference list. If he anticipates the helmet objection,
  §6 needs revisiting.
- **A peer-reviewed response exists and was not read.** S. J. V. Malloch, "Gaius on the
  Channel Coast", *Classical Quarterly* 51.2 (Dec. 2001), 551–556 — **bibliographically
  verified by me via Crossref** (DOI `10.1093/cq/51.2.551`: author, title, journal, volume,
  issue, pagination, date). **Its content is UNVERIFIED**; it is paywalled and no summary
  used here rests on reading it. Success criterion 3 is therefore **partly** met: a
  peer-reviewed rebuttal *exists*, and its argument is not yet fairly represented.
- **The Suetonius/Dio source relationship** is constrained but not settled. Both use the
  *conch-* family; Dio has narrative detail Suetonius lacks (the trireme, the trumpeters, the
  shells carried to Rome). That is consistent with a common source rather than dependence,
  but the corpus cannot decide it.
