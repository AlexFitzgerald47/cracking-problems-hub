# The *conchae et umbilici* result

**Session:** 2026-09-07 · Cracker (starting mode) · Claude Opus 5, Claude Code remote
**Reproduce:** `analysis/data/survey.py`, raw output in `analysis/data/survey_output.txt`

---

## BLUF

The Hub inherited this problem framed as a two-way fight: literal seashells (madness or
theatre) versus a garbled technical term (Woods). **The corpus says both camps have been
reading the wrong word.**

`conchas ... legere` is not a description of an arbitrary act. Together with its partner
noun *umbilici* it is, in surviving Latin, effectively **a single idiom with a single
referent**: Scipio Aemilianus and Laelius gathering shells on the shore at Caieta and
Laurentum — the canonical Roman exemplum of the greatest commanders of the Republic at
leisure, glossed by Cicero as *repuerascere*, "becoming boys again."

Across 46.7 million characters of classical Latin including the complete *Natural History*,
`umbilicus` in the sense "shore shell" occurs **three times**:

| # | Passage | Subject |
|---|---|---|
| 1 | Cicero, *De Oratore* 2.22 | Scipio & Laelius |
| 2 | Valerius Maximus 8.8.1 | Scipio & Laelius |
| 3 | **Aurelius Victor, *De Caesaribus* 3.11** | **Caligula** |

Aurelius Victor reports Caligula's order as `conchas umbilicosque ... legi iussit`. That is
not a general Latin way of saying "shells". It is *the phrase*, and its only other owners in
the surviving language are Scipio and Laelius.

**The consequence:** the Channel episode does not need Woods's emendation, and it is not
evidence of derangement. It is a legible cultural act — an emperor putting an army into
battle order on the Ocean shore and making it perform, on command, the private *otium* of
Scipio and Laelius, then claiming the product as *spolia* owed to the Capitol. The scandal
is not that shells are worthless. It is that shell-gathering is what Roman generals did
**when they had stopped being generals.**

Whether the allusion is Caligula's own or the reporting tradition's is **not settled by this
session** and is the single most important open question left. See §6.

---

## 1. What was actually run

Two independent corpora, both cloned from GitHub (the only reachable host this session —
see §7 on egress):

| Corpus | Texts | Chars |
|---|---:|---:|
| `cltk/latin_text_latin_library` | 2,141 | 95.9M |
| `cltk/latin_text_tesserae` (incl. complete Pliny *NH*) | 748 | 46.7M |

Three lemmas surveyed with every window read by hand, not just counted: `concha` (incl.
`conchula`), `umbilicus`, `musculus`.

The primary text was verified against the corpus rather than quoted from memory —
Suet. *Cal.* 46: `repente ut conchas legerent galeasque et sinus replerent imperavit,
"spolia Oceani" vocans "Capitolio Palatioque debita"`.

---

## 2. The rarity result (the load-bearing finding)

Heuristic flag counts, then manual sense adjudication of every flagged window:

| Corpus | `umbilic*` total | flagged marine context | **actually = "shell"** |
|---|---:|---:|---:|
| Latin Library | 105 | 14 | **4** |
| Tesserae | 79 | 10 | **3** |

The three in Tesserae are Cicero, Valerius Maximus, Aurelius Victor. The Latin Library's
fourth is Lhomond's *De Viris Illustribus* (1775), a schoolbook paraphrase of the same
Scipio–Laelius anecdote — derivative, not an independent attestation.

Every other instance of the word in both corpora is the navel, the boss of a shield or
scroll, the centre of a territory, or a medical/anatomical usage.

**The complete *Natural History* — the largest surviving repository of Latin marine-species
vocabulary — contains zero instances of `umbilicus` meaning a shell.** Pliny catalogues
*conchae*, *cochleae*, *pectines*, *echini*, *pelorides*, *balani*, *murices*, *ostrea*. He
never once needs *umbilicus*. That is what makes the Cicero → Valerius Maximus → Victor
chain a citation rather than a coincidence: the word is not available in the general
marine-vocabulary pool.

### The three passages

> **Cic. *De Or.* 2.22** — *Saepe ex socero meo audivi, cum is diceret socerum suum Laelium
> semper fere cum Scipione solitum rusticari eosque incredibiliter **repuerascere** esse
> solitos ... **conchas eos et umbilicos** ad Caietam et ad Laurentum **legere** consuesse et
> ad omnem animi remissionem **ludumque** descendere.*

> **Val. Max. 8.8.1** (book heading *De otio*) — *constat namque eos Caietae et Laurenti
> uagos litoribus **conchulas et umbilicos lectitasse**, idque se P. Crassus ex socero suo
> Scaeuola ... audisse saepe numero praedicauit.*

> **Aur. Vict. *Caes.* 3.11** — *Neque secus contractis ad unum legionibus spe in Germaniam
> transgrediendi **conchas umbilicosque** in ora maris Oceani **legi iussit**.*

Valerius Maximus matters for chronology: he wrote **under Tiberius**. The Scipio–Laelius
shell anecdote was a live, catalogued exemplum of aristocratic leisure in the reign
immediately before Caligula's, filed under *De otio*. The allusion was available to be made
and available to be heard in AD 40.

---

## 3. Woods's reading: falsified at the lexical level

Two independent search passes this session indicate Woods (2000) argued `conchae` denotes
**small boats**, not the *musculi* thesis the Hub's `PROBLEM.md` attributes to him. That
attribution discrepancy is unresolved (§7) — but **both** candidate theses fail here:

**Against `concha` = boat.** In 143 Tesserae instances across 71 texts, and 147 in the
Latin Library, `concha` **never** denotes a vessel. The nine ship-vocabulary windows are
Triton's conch-horn (Vergil *Aen.* 10.209, Silius 14.373, Lucan), shells on a sea-monster's
hide, the remora, pearl-diving, and one instructive near-miss:

> **Plin. *NH* 9.51** — *concham esse acatii modo **carinatam**, inflexa **puppe**, **prora**
> rostrata* — a shellfish (the nautilus) described *as if* built like a boat.

Pliny has to spell the comparison out — keel, stern, beak — precisely because the noun does
not carry the sense on its own. That passage is the strongest available evidence *against*
Woods, not for him.

**Against `concha` ← `musculus`.** Plautus, *Rud.* 297–99 lists a shore-gatherer's catch:
*echinos, lopadas, ostreas, balanos captamus, **conchas**, marinam urticam, **musculos**,
plagusias striatas*. The two words are **distinct items in the same list**. A source
confusion therefore needs two steps (hut → mussel → generic shell), not one.

The `musculus` base rate the previous handover asked for, counted both ways as instructed
(Latin Library, n=53, manual classification): anatomical muscle ~17; "little mouse" ~9;
shellfish ~6; sea-creature/whale-pilot ~3; **military siege-shed ~19** (Caesar *BC* 2.10–14
alone accounts for 12); boat ~2 (Isid. *Etym.* 19.1.14 *musculus, curtum navigium*; *Not.
Dign.* *musculorum Scythicorum*).

So the military-technical sense runs at roughly **40%** — Woods is not making an absurd
claim about the word. The survey does not kill *musculus*; it kills the need for it. You do
not emend an idiom that is already attested doing exactly this work.

---

## 4. `concha` is not a worthless-object word

Both camps assume the shells are beach litter. The corpus disagrees.

- **39%** of Tesserae `concha` windows (56/143) sit in pearl / purple / gem / luxury
  vocabulary. Pliny's own chapter sequence: *concharum genera. quanta luxuriae materia mari
  sit. de margaritis.* `Concha` is the header category under which pearls are filed.
- **Suetonius' own idiolect.** The `conch-` root appears **three times in the whole *Twelve
  Caesars***:
  1. *Cal.* 18 — Caligula distributes *fascias purpurae ac **conchylii*** to the people at a
     public banquet (murex-dye largesse, 28 chapters before our passage);
  2. *Cal.* 46 — the disputed order;
  3. *Nero* 31 — the Domus Aurea, *cuncta auro lita, distincta gemmis **unionum**que
     **conchis*** — pearl-shell revetment on an imperial palace.

  Not one worthless shell in the author who wrote the sentence. Both flanking instances are
  high-value commodity senses — and one of them is a Palatine building material, which is
  where *Cal.* 46 says the *spolia* were owed.

**Held-out confirmation.** Having derived this from the base rate alone, the prediction was
that Suetonius elsewhere links crossing the Ocean to shell-borne treasure. He does, in the
first Life of the same work:

> **Suet. *Iul.* 47** — ***Britanniam petisse spe margaritarum**, quarum amplitudinem
> conferentem interdum sua manu exegisse pondus.*

Caesar crossed the Ocean *in the hope of pearls*, and weighed them in his own hand.
Suetonius made that the canonical motive for a British expedition before he ever wrote
*Cal.* 46. Caesar came back from the Ocean with pearls; Caligula came back with the shells.

This does **not** mean the order was "collect pearls" — that popular reading is not
supported here and is not being advanced. It means the word `concha` carries an
economic charge that makes `spolia Oceani ... Capitolio Palatioque debita` intelligible as a
claim rather than as a symptom.

---

## 5. The compositional frame

`Cal.` 45–47 is a designed triad about **counterfeit triumphal material**, and the shells
are its middle term:

| ch. | act | counterfeit |
|---|---|---|
| 45 | Germans planted across the Rhine and "captured"; felled trees dressed *in modum tropaeorum*; crowns named *exploratoriae*, figured with sun, moon and stars | trophies |
| 46 | *conchas legerent* → *spolia Oceani* | spoils |
| 47 | tallest Gauls picked out (*legit ac seposuit ad pompam*), hair dyed red, made to learn German and take barbarian names | captives |

Chapter 47 reuses the verb: Caligula *legit* the Gauls as his men *legerent* the shells. The
episode is not a loose madness anecdote dropped into the Life. It is the second of three
staged substitutions, and the only one anybody has felt the need to emend.

Read with §2, the point sharpens: chs. 45 and 47 are play — *ludus*, dressing-up, war in a
wood. Cicero's gloss on *conchas et umbilicos legere* is `ad omnem animi remissionem
**ludumque** descendere`. Ch. 46 is the same register, and Suetonius' *repente ... nemine
gnaro aut opinante* frames it as the punchline of the sequence.

---

## 6. OBSERVED / INFERRED / MISSING

| Edge | Status | Note |
|---|---|---|
| Suet. *Cal.* 46 text as quoted | **OBSERVED** | verified in corpus, not from memory |
| `umbilicus` = shell occurs 3× in 46.7M chars, all three listed | **OBSERVED** | reproducible; zero in complete Pliny *NH* |
| Cicero, Val. Max. and Victor share the noun pair + `legere` | **OBSERVED** | exact citations in §2 |
| Val. Max. wrote under Tiberius; anecdote filed under *De otio* | **OBSERVED** | book 8.8 heading |
| `concha` never denotes a boat in 290 combined instances | **OBSERVED** | Woods's lexical base rate is zero |
| `concha` ≠ `musculus` (distinct items, Plaut. *Rud.* 297–99) | **OBSERVED** | |
| Suetonius' 3 uses of `conch-` are all commodity senses | **OBSERVED** | n=3; small, but it is the author's own usage |
| Suet. *Iul.* 47 makes pearls the motive for crossing the Ocean | **OBSERVED** | held out from derivation |
| The order alludes to the Scipio–Laelius exemplum | **INFERRED** | this is the leap; §2 is its evidence |
| The allusion was **Caligula's**, not the tradition's | **MISSING** | Suetonius has only `conchas`; the pair survives in Victor, c. AD 361 |
| Victor's source for `umbilicos` | **MISSING** | *Kaisergeschichte*? direct Ciceronian colour? decisive either way |
| Whether classicists have already noted this intertext | **MISSING** | see §7 — real verification debt |
| Dio 59.25 Greek wording (one noun or two?) | **MISSING** | the cheapest decisive next test — see falsifier F4 |

**The honest shape of the claim.** What is proved is that the phrase reported of Caligula is
a rare, marked, culturally loaded idiom rather than a neutral description, and that neither
existing camp has reckoned with that. What is *inferred* is the reading built on it. The
inference is strong but it rests on one bridge — Victor's `umbilicos` — and that bridge is
dated three centuries after the event.

---

## 7. Preregistered falsifiers

Written down **before** anyone acts on §2, so the model cannot absorb the results.

- **F1 — rarity.** Search PHI / *Library of Latin Texts* / the Thesaurus for `umbilicus` in a
  shell sense outside these three passages. Each independent attestation found weakens the
  citation argument proportionally. **More than three or four and the idiom claim fails.**
  Priority checks: Pliny *NH* 32's species catalogue (already checked here, clean), Festus,
  Nonius, Isidore *Etym.* 12, the *Cena Trimalchionis*, the medical writers.
- **F2 — priority.** If Wardle's commentary on Suetonius *Caligula*, Bird's commentary on
  Aurelius Victor, Malloch (CQ 2001) or Woods (G&R 2000) already notes the Cicero/Valerius
  Maximus ↔ Victor link, this is a **replication, not a discovery**, and must be relabelled
  as such in `PROGRESS.md` without argument. My searches surfaced no scholarly source
  asserting it, but I could not read any of those four items (§8).
- **F3 — direction of the allusion.** If Victor's `umbilicos` can be traced to a source
  independent of the Ciceronian tradition and current in AD 40, the allusion is Caligula's
  own act. If it is shown to be Victor's own literary colouring, the allusion belongs to the
  tradition and the historical claim shrinks to "this is how Rome chose to remember it" —
  still a result, a smaller one.
- **F4 — the Greek control.** Dio 59.25.3 is the independent witness. **If Dio preserves a
  two-noun pair** (κόγχοι + a second shell-word) the pair predates Victor and the case
  strengthens sharply. **If Dio has one noun only**, the pair is likelier to be late Latin
  literary colour and F3 resolves against Caligula. This is the single cheapest decisive
  experiment left and it needs nothing but access to Dio's Greek.
- **F5 — competitor count.** How many *other* rare Latin collocations in *Cal.* 45–47 have a
  single famous referent? If the Life is thick with them, the `conchae et umbilici` match is
  one of many and proves less. This session did not run that null and it should be run.

---

## 8. Verification debt carried forward — read before citing anything here

Network egress this session permitted **GitHub only**. Perseus, PHI, LacusCurtius,
Cambridge Core, JSTOR, ResearchGate, archive.org, unicode.org and Wikipedia were all blocked
at the proxy. Consequences:

- **Every Latin text quoted here was read in full from a cloned corpus.** Those are
  OBSERVED and safe.
- **No modern scholarship was read.** Woods (2000), Malloch (2001), Wardle's commentary and
  Bird's Victor are cited at metadata level only, from search-index records. Do not
  represent any of them as read.
- **Woods's actual thesis is unresolved.** `PROBLEM.md` attributes the *musculi* argument to
  him; two search passes this session indicate he argued `conchae` = small boats. Both are
  addressed in §3, so nothing here depends on the answer — but the Hub's framing must be
  corrected once someone reads the eight pages. See the appended note in `PROBLEM.md`.
- **A peer-reviewed rebuttal of Woods does exist**, clearing the previous handover's
  recommended experiment 2: **S. J. V. Malloch, "Gaius on the Channel Coast," *Classical
  Quarterly* 51 (2001), 551–556.** Metadata-level verification only; its argument is
  unknown to this session and must not be characterised.
- **Suetonius/Dio independence (recommended experiment 5) is NOT settled.** Dio's Greek was
  unreachable. What this session adds instead is a *third* witness, Aurelius Victor, whose
  wording is demonstrably not derived from Suetonius — Suetonius has no `umbilici`. That
  makes the Suetonius/Dio/Victor relationship more interesting, not less, and F4 is now the
  way into it.

## 9. Corpus caveat

Neither corpus is the complete surviving Latin. The Latin Library is broad but
uncritically edited and includes post-classical and early-modern material (Lhomond, More,
Erasmus, Newton, Descartes all surfaced in these scans and were excluded by hand where
relevant). Tesserae is cleaner and includes the complete *NH*, which is why the rarity
result is reported on it. **The counts are corpus-bounded, not absolute**, and F1 exists
precisely to test them against the full apparatus.
