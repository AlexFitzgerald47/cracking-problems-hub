# The *musculus* inventory, and what it does to the readings of Suet. *Calig.* 46

**Session:** 2026-09-22, Claude Opus 5 (Claude Code, remote). Mode: starting.
**Predictions frozen before any count:** `analysis/2026-09-22-frozen-predictions.md` (committed first).
**Code:** `code/`. **Data:** `data/musculus_inventory.csv` (120 classified tokens).

---

## 0. The correction that has to come first

**`PROBLEM.md` misdescribes Woods's thesis, and the error is load-bearing.**

`PROBLEM.md` says Woods (2000) argued that the order concerned *musculi* in the sense of
"small siege-shelters or sapper huts". Woods's own footnote apparatus says otherwise. I
retrieved the footnotes myself from the Cambridge Core article page, where the full
footnote text is embedded in the page's client-side JSON even though the body is paywalled
(`code/` does not automate this; the file is `woods_cup.html`, fetched 2026-09-22):

- **fn15:** "Balsdon (n. 12), 92 presents this as second possible interpretation of the
  seashell incident, and manages to avoid committing himself to either interpretation."
  The *musculi*-huts reading is **Balsdon's (1934)**, which Woods reports, not his own.
- **fn16–20**, in order: `OLD s.v. musculus, 1148` → `OLD s.v. concha, 386` →
  `ThLL s.v. concha, col. 29` (on *concha* of the apse of a basilica; Greek κόγχη of the
  hollow of the ear and a seal-case) → **`OED (2nd ed.) s.v. cockle, 417`** → "On the wide
  variety of terms used to denote various types of small craft, see Casson, L., *Ships and
  Seamanship in the Ancient World*."
- **fn21:** Woods's own methodological precedent — Libanius *misinterpreting* the technical
  term *vexillarius*.
- **fn27:** Josephus *BJ* 7.147, Vespasian and Titus parading captured **ships** in their
  AD 71 triumph.

That sequence is a **boat** argument. The English word *cockle* (shellfish → *cockle-shell*,
a small boat) supplies the analogy; Casson supplies the small-craft terminology; Josephus
supplies the parallel for ships as triumphal *spolia*. Woods's thesis is that the "spoils of
Ocean" were small craft, not that they were sappers' huts.

I could not read the body of the article (hard paywall; no open copy found), so I state this
as **a reconstruction from Woods's own apparatus, not from his conclusion**. But the
reconstruction is strong enough that the problem's success criteria have to be re-aimed: a
survey of the *military-shelter* sense alone tests Balsdon, not Woods.

Both readings are tested below.

## 1. Corpus

| source | texts | word tokens |
|---|---|---|
| The Latin Library (crawled 2026-09-22) | 2,212 files | ~12.2M |
| Perseus `canonical-latinLit` (git clone) | 364 Latin XML works | ~7.1M |

Coverage is reported, not asserted. **PHI Latin (`latin.packhum.org`) is Cloudflare-blocked
(403) from this environment** and was not used; that is the one corpus that would settle
"complete for classical Latin", and its absence is a real limit on the word "full" in
success criterion 1. The *Corpus Glossariorum Latinorum*, where a *musculus*/*concha* gloss
equivalence would most likely show up, is also not machine-readable here.

**Pipeline check before any claim** (P-recall predictions): the pipeline recovers Caesar
*BC* 2.10–11 (the extended technical description of the *musculus*) in full, *BG* 7.84,
Vegetius 4.16, and every locus Lewis & Short cites under *musculus* except those in texts
the corpus does not contain. A first crawl silently lost Cicero, Caesar and Ammianus because
the site's main index uses extensionless directory links (`/caesar`, `/cicero`) that my link
filter dropped; this was caught **by the Caesar recall check failing**, which is exactly what
that check is for. Fixed in `code/complete_ll2.py`.

## 2. The inventory (success criterion 1)

120 tokens, one edition per work, post-classical revivals (Newton, Descartes, the Latin
*Alice*) excluded. Every token is in `data/musculus_inventory.csv` with its context; every
token whose keyword-rule label I overrode on reading the passage carries the reason in a
`note` column.

| sense | tokens | % | distinct passages |
|---|---:|---:|---:|
| anatomical muscle | 62 | 51.7 | 62 |
| military shed / mantlet | 21 | 17.5 | 21 |
| shellfish (mussel) | 10 | 8.3 | 9 |
| mouse | 9 | 7.5 | 9 |
| whale-companion fish | 7 | 5.8 | 6 |
| fly (*muscula* < *musca*) | 5 | 4.2 | 5 |
| **small boat** | **3** | **2.5** | **3** |
| water-mouse | 3 | 2.5 | 3 |

### The military sense, by passage
Caes. *BG* 7.84.1 (`crates, longurios, musculos, falces` — plural, portable, carried out for
a sortie); Caes. *BC* 2.10.1–2.11.4 (one 60-ft machine, described at length); Caes. *BC*
3.80.5 (`scalas musculosque … fieri … iussit`, Gomphi); [Caes.] *B.Alex.*
(`testudinibus ac musculis aptantur`); Veg. *Mil.* 2.25; Veg. *Mil.* 4.16 (`De musculis`);
Isid. *Etym.* 18.11.4.

### The shellfish sense, by passage
Plaut. *Rud.* 297–8; Cels. *Med.* 2.29 and 3.6; Auson. *Epist.* (praef., and
`Iunctus limicolis musculus ostreis`); Isid. *Etym.* 12.6.6 and 12.6.53; Bede *HE* 1.1
(`musculae, quibus inclusam saepe margaritam`).

### The boat sense, by passage — all three
Isid. *Etym.* 19.1.14 (`cuius contrarius musculus, curtum navigium`); *Not. Dign. Occ.*
(`Praefectus militum musculariorum, Massiliae Graecorum`); *Not. Dign. Or.* 39
(`… secundae Herculiae musculorum Scythicorum et classis`).

## 3. Results against the frozen predictions

**P1 — sense rank and intervals. PARTIALLY FAILED, and I am recording the miss.**
Predicted rank muscle > military > shellfish > mouse. Actual: muscle > military > **mouse
(11, counting the water-mice) ≈ shellfish (10)**. Military 21 falls in the predicted 10–40.
Shellfish 10 is just outside the predicted 1–8, and appears in 5 distinct authors against a
predicted ≤ 4. Two of three sub-predictions missed narrowly. The miss is in the direction
that *helps* the mollusc reading.

**P2 — the crux. CONFIRMED.** With the identical one-edition-per-work rule:
*concha* (excluding *conchylium*) **271**; *conchylium* 137; *ostrea* 164;
*mitulus/mytilus* 89; ***musculus* in the shellfish sense 10**. *Musculus* is ~27× rarer
than *concha* as a word for a shellfish, and rarer than *mitulus*. It is a marginal word for
"mussel" — but see §4, because "marginal" is not "unavailable".

**P3 — FAILED, and the failure favours the huts reading.** I predicted under 35% of military
tokens would be plural and that plurals would cluster in late authors. By passage,
**5 of the 7 military passages are plural**, including two in Caesar himself (*BG* 7.84,
*BC* 3.80). The singular concentration is an artefact of one extended description of one
machine at *BC* 2.10. Plural *musculi* is the normal way to refer to these things, and at
*BG* 7.84 they are portable objects brought out alongside hurdles, poles and hooks. An order
about plural *musculi* is perfectly idiomatic Latin. Balsdon's premise survives this test
better than I expected it to.

**P4 — CONFIRMED.** No attestation of *legere* or *colligere* governing a military
*musculus*. The verbs are *facere / instituere / fieri / proferre / aptare / admovere /
devolvere*: these things are **built, brought and pushed**, not gathered.

**P5 — CONFIRMED, then sharpened against myself.** Siege-technical nouns per 10,000 words:
Caesar 36.94, Tacitus 10.74, Livy 8.44, Sallust 7.06, **Suetonius 2.26 (LL) / 2.74
(Perseus)**, Nepos 1.42. Suetonius runs at ~7% of Caesar's rate, comfortably below the
predicted one-fifth. **But reading the tokens weakens my own result and strengthens Woods's
premise:** 8 of Suetonius's ~13 hits are *tormenta* in the ordinary sense "torture", and his
single clearest piece of artillery vocabulary in the whole *De vita Caesarum* is
`ballistis machinisque dispositis` — **inside *Calig.* 46 itself**. Suetonius has almost no
siege register, and the one place he reaches for it is this sentence.

**P6 — the null model. CONFIRMED (13/17 = 76%).** Taking the device list from Vegetius
*Mil.* 4.13–22 plus the standard artillery and naval set, and requiring ≥3 corpus tokens in
the everyday sense: *aries, falx, testudo, vinea, pluteus, musculus, onager, scorpio, corvus,
cuniculus, lupus, ciconia, grus* are all homonyms of an animal or ordinary object;
*agger, turris, ballista, catapulta* are not. **Roman siege vocabulary is zoomorphic as a
system.** Therefore "this military word is also an animal word" has a likelihood ratio near 1
and carries almost no evidential weight on its own. Pointing at the ambiguity of *musculus*
is not an argument; it is the base rate.

**P7 — CONFIRMED, and this is the strongest single result.** `conchas legere` is not odd
Latin needing repair. **Cic. *De Or.* 2.22:** Scipio and Laelius `conchas eos et umbilicos
ad Caietam et ad Laurentum legere consuesse` — shell-gathering on the shore as the
recreation of great Romans. The collocation is idiomatic and carries an established literary
frame.

**P8 — CONFIRMED.** *musculus* and *concha* stand in the same shellfish list twice:
**Plaut. *Rud.* 297–8** `echinos, lopadas, ostreas, balanos captamus, conchas, / marinam
urticam, musculos, plagusias striatas` and **Cels. *Med.* 2.29** `ostrea, pelorides, echini,
musculi, et omnes fere conchulae`. In both they are **distinct members of one list**, i.e.
co-hyponyms, not synonyms. A paraphrast could slide *musculi* → *conchae*, but the slide is
species-to-genus, a generalisation, not a translation.

## 4. Three things the corpus decides

### 4.1 The mollusc sense was live in AD 40; the boat sense was not
This is the chronological test, and it is the board's own rule — *check the historical stage,
not the modern headword* (`board/PRACTICES.md`, the `ALUʀ`/*alr* case).

| sense of *musculus* | earliest attestation in this corpus | date |
|---|---|---|
| shellfish | Plaut. *Rud.* 297–8; **Cels. *Med.* 2.29, 3.6** | c. 200 BC; **Tiberian** |
| military shed | Caes. *BG* 7.84, *BC* 2.10 | 50s BC |
| whale-companion fish | Plin. *NH* 9.186, 11.165 | AD 77 |
| **small boat** | ***Not. Dign.*; Isid. *Etym.* 19.1.14** | **c. AD 400; 7th c.** |

Celsus wrote under Tiberius. The shellfish sense of *musculus* is attested **in Caligula's
own generation**. Caesar's siege sense is attested a century before. The **boat sense is not
attested until roughly AD 400 — some 360 years after the event.**

**The null model for that silence.** An argument from non-attestation is worthless if Latin
small-craft vocabulary is generally undocumented. It is not. Of 17 small-craft terms drawn
from Isidore's own ship catalogue (*Etym.* 19.1) plus the standard set, **13 are attested in
pre-AD 100 authors**: *scapha* (Plautus, Caesar, Livy), *lembus* (Livy, Plautus), *celox*
(Plautus, Livy), *linter* (Caesar, Livy, Ovid), *cumba* (Ovid, Propertius), *myoparo*
(Cicero, 13 tokens), *paro* (Cicero), *phaselus* (Catullus, Cicero, Livy), *actuaria*
(Caesar, Cicero), *navicula* (Cicero, Caesar), *liburna*, *triremis*, *ratis*. The four that
are **not** early are *dromo*, *barca*, *ancyromachus* and *musculus* — and *dromo* and
*barca* are independently known to be **late-antique ship types**, late in attestation
because the ships themselves are late. *Musculus*-the-boat patterns with the late ship
types, not with the classical vocabulary. (Two contamination traps caught and removed: the
28 "dromo" hits in Terence are a slave named Dromo; the early "barca" hits are Hamilcar
Barca.)

**And *concha* is never a boat in Latin at all.** Of 271 *concha* tokens, 32 have any
nautical word within ±150 characters and **not one is a vessel**: they are shells on a shore,
Triton's conch-trumpet, and Pliny's nautilus — `concham esse acatii modo carinatam, inflexa
puppe, prora rostrata` (*NH* 9.94), a shell **compared to** a boat. That is the exact
resemblance the English *cockle-shell* lexicalised. Latin noticed it and left it a simile.
Woods's analogy is supplied by fn19, *OED s.v. cockle* — by English, not by Latin.

### 4.2 The received text needs no repair
Woods's argument, and Balsdon's, both need the transmitted sentence to be strange enough to
want emending. It is not.

- `conchas legere` is **Cicero's** phrase for shore-gathering (*De Or.* 2.22).
- Gathering the Ocean's shells is what Romans said about **this coastline in this century**:
  **Tac. *Agr.* 12** `gignit et Oceanus margarita … quidam artem abesse **legentibus**
  arbitrantur; nam in rubro mari viva ac spirantia saxis avelli, in Britannia, prout expulsa
  sint, **colligi**`. Ocean + shells + *legere*/*colligere*, of Britain, within a generation.
- **Suetonius himself** supplies the motive, in the same work: *Iul.* 47,
  `Britanniam petisse spe margaritarum, quarum amplitudinem conferentem interdum sua manu
  exegisse pondus` — Caesar went to Britain hoping for pearls and weighed them in his own
  hand. Cf. Plin. *NH* 9.116, Caesar's breastplate of British pearls dedicated to **Venus
  Genetrix**, and — in the very next sentence — **Lollia Paulina, `quae fuit Gai principis
  matrona`**, Caligula's own wife, in a pearl passage.
- The base rate: **16.1%** of *concha* tokens have a pearl-word (*margarita, unio, bacca,
  gemma*) within ±150 characters. Pearl-bearing shell is a standard specialised sense.

None of this proves the shells were gathered for pearls — Flory (*Historia* 1988) and Hind
(*Britannia* 2003) are already on that ground, and I could not read either. What it shows is
narrower and sufficient: **there is no lexical pressure to emend.** The clause is ordinary
Latin, in the ordinary idiom, about the one coastline whose shells Romans actually talked
about. An emendation has to earn its place against a text that reads perfectly well, and
neither the huts nor the boats reading has yet paid that price.

### 4.3 The later tradition moves *deeper* into molluscs, with a word Woods cannot source
**Aurelius Victor, *Caes.* 3.11–12** (verified in the text, not in a summary):
`conchas umbilicosque in ora maris Oceani legi iussit … spolia a se non ex hominibus, sed
caelestium capi dictitaret, scilicet quod huiuscemodi pisces Graecorum dicto … Nympharum
lumina accepisset.`

Two observations, both new as far as I can tell:

1. **Victor's phrase is Cicero's.** `conchas umbilicosque … legi` against *De Or.* 2.22
   `conchas … et umbilicos … legere`. The **same pairing of the same two mollusc words with
   the same verb**. The fourth-century tradition is elaborating the episode *through the
   Ciceronian shell-gathering topos* — assimilating Caligula on the beach to Scipio and
   Laelius at Caieta, and inverting it.
2. **Victor adds *umbilici*, which cannot come from *musculi*.** Whatever produced
   *conchae*, a second and different mollusc word entered the tradition. On the misreading
   hypothesis this has to be pure invention; on the literal hypothesis it is a natural
   Ciceronian expansion. Victor also glosses the objects as `pisces` with a Greek nickname,
   `Nympharum lumina` — he is reaching for more marine biology, not less.

**Cassius Dio 59.25.3** (Greek text read directly): `ἐκέλευσέ σφισι τὰ κογχύλια
συλλέξασθαι` … `καὶ ὁ μὲν ἐς τὴν Ῥώμην τὰ κογχύλια ἀνεκόμισεν`. Dio's word is
**κογχύλια**, the specific Greek term for shellfish, with **συλλέγω** — the exact
counterpart of *legere*. κογχύλιον is not a boat either.

So all three surviving witnesses are in the mollusc frame, and the two later ones each add
*further* mollusc detail. Woods's fn28 is candid that the source relationship is unknown;
that cuts both ways, but it means the tradition offers no point at which the mollusc reading
is thin.

## 5. Verdict

**On success criterion 2 — is the *musculi* reading philologically stronger than the literal
one?** No, and the two versions fail differently.

- **Woods's boat reading (*musculus*/*concha* = small craft) fails a chronological test.**
  The boat sense of *musculus* is unattested for ~360 years after AD 40, in a corpus that
  documents thirteen other small-craft names in the classical period; *concha* never means a
  boat in Latin at all; and the analogy that makes the reading attractive is English
  (*cockle-shell*), imported through *OED*. This is the board's own `ALUʀ`/*alr* failure
  mode: a resemblance defeated by the historical stage of the word.
- **Balsdon's huts reading (*musculi* = sappers' sheds) is lexically possible and survived
  my tests better than I predicted.** Both senses were live in AD 40; plural *musculi* is
  normal, and at *BG* 7.84 they are portable; *musculi* and *conchae* do sit in one
  shellfish list, so the substitution has a basis. What it lacks is a *motive*: the
  transmitted sentence is idiomatic Latin (P4, P7), so nothing in the text asks to be
  repaired — and *legere* is not what one does to a *musculus* (P4).
- **Both readings are additionally discounted by the null model (P6).** Ambiguity between a
  device-name and an animal is the norm in Roman siege vocabulary (76%), so the observation
  that *musculus* is ambiguous is worth almost nothing on its own.

**On success criterion 4 — the honest answer is that the passage underdetermines the
event, but not the philology.** No corpus count can establish what a lost first-century
dispatch said, and Suetonius's near-empty siege register (P5) is a genuine point in favour of
his being out of his depth in exactly this sentence. But the *philological* question the
problem asked — whether the Latin supports emending *conchae* — has an answer: **it does
not.** The text is idiomatic, the idiom is attested for this coast in this century, and the
later tradition elaborates it with a second mollusc word from the same Ciceronian model.

**What would change this.** Not more corpus work on *musculus* — that line is now exhausted
to the limit of the accessible corpora. See `HANDOVER.md`.

## 6. Verification status of everything above

- **Verified by me in the primary text, in this corpus:** every Latin quotation and every
  count in §2–§4, including Caes. *BG* 7.84, *BC* 2.10 and 3.80, [Caes.] *B.Alex.*, Veg.
  *Mil.* 2.25 and 4.16, Isid. *Etym.* 12.6.6, 12.6.53, 18.11.4, 19.1.14, Plaut. *Rud.*
  297–8, Cels. *Med.* 2.29, Auson. *Epist.*, Bede *HE* 1.1, *Not. Dign.* Occ. and Or.,
  Cic. *De Or.* 2.22, Tac. *Agr.* 12, Plin. *NH* 9.94, 9.116, 9.186, 11.165, Suet. *Iul.* 47
  and *Calig.* 46, Aur. Vict. *Caes.* 3.11–12.
- **Verified by me directly from the publisher's page:** Woods 2000 bibliographic record and
  the text of footnotes 2–28. Dio 59.25.2–3 Greek read directly from Perseus.
- **NOT verified — do not treat as read:** the body of Woods 2000; Malloch, "Gaius on the
  Channel Coast", *CQ* 51.2 (2001), 551–6 (exists, cites Woods — the only CrossRef-registered
  citation of it — content unread); Hind, *Britannia* 34 (2003), 272–4 (exists, cites Woods
  in its reference list — content unread); Wardle's commentary; Balsdon 1934; Flory 1988;
  Barrett; Hurley; Lindsay. All were surfaced by a Sonnet researcher and I re-checked only
  their *existence and citation relationship*, not their arguments.
- **Corpus limits:** PHI Latin 403-blocked; *CGL* not machine-readable; the Latin Library
  crawl has 259 paths that 404 on the site's own stale index links.
