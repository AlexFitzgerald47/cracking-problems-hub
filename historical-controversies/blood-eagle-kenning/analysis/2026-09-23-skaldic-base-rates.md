# The eagle never cuts: base rates for the beasts-of-battle topos, and what they do to the blood-eagle argument

Session: 2026-09-23, Claude Opus 5, cracker, *starting* mode.
Predictions frozen before any counting: `analysis/2026-09-23-PREREGISTERED.md`.
Code: `analysis/code/`. Adjudication table: `analysis/data/beast_blade_adjudication.tsv`.
Rebuild the corpus with `analysis/code/FETCH_CORPUS.sh`.

---

## 0. What this session did, in one paragraph

Roberta Frank's 1984 sceptical case rests on one load-bearing adjective: that Sigvatr
Þórðarson's *Knútsdrápa* st. 1 uses a **conventional** skaldic image — the beasts-of-battle
eagle tearing at a corpse — which later saga-writers mistook for a surgical rite. Nobody
appears to have checked "conventional" against the corpus. This session built the complete
skaldic corpus from Finnur Jónsson's edition, enumerated every place where a beast of battle
stands near a blade verb, every occurrence of the noun `bak`, and the conventional formula
for leaving a body as carrion, and measured the base rates. The result is that
**Knútsdrápa 1 is a triple hapax**, and that the skaldic corpus has a perfectly good formula
for what Frank says Sigvatr meant — which Sigvatr did not use. Separately, and pointing the
other way, the session found that the *second* blood-eagle victim has a surviving verse
witness by his own killer, and that witness **does** use the conventional formula, with no
rite. Frank's mechanism is demonstrably real; the stanza she built it on is the worst
available example of it.

---

## 1. Corpus and pipeline

**Corpus.** Finnur Jónsson, *Den norsk-islandske skjaldedigtning*, Kommissionen for det
Arnamagnæanske Legat, København/Kristiania 1912–15. Volumes A I–II (`tekst efter
håndskrifterne`, diplomatic) and B I–II (`rettet tekst`, normalised, each stanza followed by
Finnur's Danish prose translation). This is the complete skaldic corpus. All four volumes are
public-domain full text on archive.org.

**OCR replicates.** The OCR is bad — Old Norse diacritics (`þ ð ǫ æ ø á í ó`) are mangled
constantly. Rather than trust one scan, this session downloaded **two independent scans of the
same four volumes** (University of Ottawa, identifiers `…finn`; University of North Carolina,
`…finnu`) and ran the whole pipeline on each. Every number below is reported for both. The
scans are genuine replicates, not a formality: they disagree about which characters are
present, and the fact that they agree about the *result* is the evidence that the result is
not an OCR artefact.

**Pipeline.** `code/foldlib.py` folds OCR noise (þ-ligatures, `5`→`ð`, `9`→`ǫ`, accent
stripping) into a flat ASCII skeleton. `code/extract.py`, `inventory.py`, `construals.py`,
`final_numbers.py` and `formula.py` do the enumeration. Old Norse verse lines are separated
from Finnur's Danish translation by a function-word test (`is_da`); this is crude and its
failures are visible in the committed contexts, which is why the contexts are committed.

**Pipeline validation — recovering what is already known.** Before anything contested, the
pipeline was required to find the target stanza in the primary edition. It does, in both the
diplomatic and the normalised text, and it recovers the poem's attribution independently:

- A I (diplomatic, manuscript orthography):
  `1. Ok ellv bak / at let hin er sat / ivaR ara / iorvik skorib.`
  The section heading two lines away reads `10. Knutsdråpa (o. 1038)`, under the poet heading
  OCR'd `SKJVATR` (= SIGVATR). **This clears one item of the verification debt PROBLEM.md
  carried:** the attribution of the stanza to Sigvatr Þórðarson, flagged there as reported but
  unverified, is confirmed against the primary edition.
- B I (normalised): `Ok Ellu bak, / at, lét, hinn's sat, / Ívarr, ara, / Jórvík, skorit.`
- Finnur's own prose word-order: `Ok Ívarr, hinn 's sat at Jórvík, lét bak Ellu skorit ara.`
- Finnur's Danish translation: `Og Ivar, han som residerede i York, ristede ørn på Ellas ryg.`
  ("…carved an eagle on Ælla's back.") The Ottawa scan garbles `ørn` to `om`; the UNC scan
  renders it `orn`. **Finnur read the stanza as the rite.** Recorded here as a datum about the
  editor, not as evidence about the poet.

---

## 2. Result 1 — no beast of battle is ever the agent of a blade verb

Every occurrence of an eagle/raven/wolf lexeme in Old Norse verse was located, and its ±70
characters (roughly one clause, in practice often a whole helmingr) searched for a blade verb
(`skera, skar, skorit, sker, rísta, reist, ristinn, hǫggva, hjó, kljúfa, klauf, sníða`).

| | scan A (Ottawa) | scan B (UNC) |
|---|---|---|
| beast-of-battle lexemes in ON verse | 772 | 719 |
| …within ±70 chars of a **blade** verb | 18 | 16 |
| …within ±70 chars of a **feeding/colouring** verb | 113 | 140 |

The 35 blade co-occurrences across both scans were then adjudicated one by one — not counted.
Proximity is not construction, and this distinction is where the whole result lives. The full
table with a verdict and a reason for every row is `data/beast_blade_adjudication.tsv`.

| verdict | n | what it means |
|---|---|---|
| `NOT-AGENT:separate` | 13 | blade verb's subject is a warrior or a sword in a different clause |
| `NOT-AGENT:kenning` | 7 | the beast word is a determinant in a warrior/ship kenning (`ara brœðis` = "eagle-feeder" = warrior; `hrafn gælir` = "raven-gladdener" = warrior) |
| `NOT-AGENT:name` | 5 | **Hrafn is a man's name**, not a bird — `vissak Hrafn hǫggva mik` |
| `WINDOW-ARTEFACT` | 3 | the blade verb belongs to the neighbouring stanza; a stanza number intervenes |
| `FALSE-POSITIVE` | 2 | `sker` is the noun "skerry"; `Úlfsfót`/`Sóta` are place-names |
| `TARGET` | 5 | the disputed passage itself, in both scans and both text and translation |

**Adjudicated count of beast-as-agent-of-a-blade-verb in the skaldic corpus, excluding the
disputed passage: zero.** In both scans independently.

What the beasts do instead is completely regular. The clearest specimen the search turned up
is a whole stanza of it:

> `Ǫrn drekkr sylg, ylgr fær undǫrn af hræum, opt rýðr ulfr kjǫpt, ari getr þar verð`
> — the eagle drinks a draught, the she-wolf gets her morning meal from the corpses, often the
> wolf reddens its jaws, the eagle gets its food there.

Four clauses, four verbs, all feeding or colouring. The division of labour across the corpus is
strict: **the warrior and the sword are the agents of blade verbs; the beast is the agent of
feeding verbs and the patient of feeding and colouring verbs.** `vargfœðir rauð granar mǫrgum
vargi` ("the wolf-feeder reddened the jaws for many a wolf") is the pattern — and note that in
that very line the blade verb `skar` is present, with `eggjandi` (the inciter) as its subject,
two words away from a dative wolf. That is exactly the configuration that a proximity count
would have scored as a hit, and it is not one.

**Statistical statement.** 0/772, so by the rule of three the 95 % upper bound on the rate of
beast-as-blade-agent in skaldic verse is 3/772 = **0.39 %**. The feeding/colouring rate is
113/772 = 14.6 % (scan A) to 19.5 % (scan B). The two constructions differ by a factor of at
least 37. This test is **well powered**: with n = 772 the corpus can exclude the construction
being anything but very rare.

---

## 3. Result 2 — `bak` is not a beasts-of-battle word at all

Complete enumeration of `bak / baki / baks` in Old Norse verse:

| | scan A | scan B |
|---|---|---|
| total occurrences | 21 | 20 |
| idiomatic (`á bak` = behind/on horseback; `ganga á bak orðum` = renege) | 16 (76 %) | 15 (75 %) |
| co-occurring with any beast-of-battle lexeme | **1** | **1** |
| co-occurring with a blade verb | **1** | **1** |

The single co-occurrence, in each scan, is Knútsdrápa 1.

Where skaldic verse puts killing wounds is a different set of words: `herðar` (a spear driven
between the shoulders — `fleinn vas fœrðr meðal herða Friðreks`; a sword between skull and
shoulders), `haus` (skull), `leggr` (leg), `fjǫr` (life), `hryggr` in the sense of a crushed
spine. Note also a lexical trap that any future session will hit: **most corpus tokens of
`hryggr` are the adjective "sad", not the noun "spine"** — 12 of the ~20 occurrences here.

So `bak` is neither a conventional wound site nor a conventional target of beast action.
Knútsdrápa 1 is the only place in the corpus where a back, an eagle and a cutting verb occur
together — a hapax on each axis and on their combination.

**Power caveat, stated plainly.** This test is *weakly* powered on the `bak` side. With only
21 occurrences, a rate of 10 % for an "eagle-scores-the-back" image would still give
P(0 further instances) = 0.9²⁰ = 0.12 — not excludable. The test excludes rates above roughly
15 % (0.85²⁰ = 0.039). The strong claim in §2 rests on n = 772; the `bak` claim in §3 rests on
n = 21 and should be treated as corroborative, not decisive.

---

## 4. Result 3 — the corpus *does* have a formula for "left as carrion", and Sigvatr did not use it

This is the positive complement of the zero, and it is what makes the zero interpretable.
Searching for a bird of prey in construction with talons/claws/feet under a preposition of
position returns a recurrent formula, in which **the victim is the subject of a verb of
falling or lying, and the bird sits in a prepositional phrase**:

1. **Þjóðólfr ór Hvini, *Ynglingatal* st. 19** (c. 900, the oldest skaldic poem):
   `Fell Óttarr / und ara greipar / dugandligr / fyr Dana vǫpnum; / þann hergamr / hrægum
   fœti, / víts borinn, / á Vendli sparn.`
   — "Óttarr the valiant fell **under the eagle's talons** before the Danes' weapons; the
   war-vulture, born of malice, **trod** him with bloody foot on Vendil."
   The bird's verb is `sparn` (spyrna, to tread), not a blade verb.
2. **Torf-Einarr Rǫgnvaldsson, lausavísa 4** (c. 900) — see §5.
3. `fjándr grams hnigu … und arnar hrammu` — "the king's foes **sank under the eagle's
   claws**".
4. `gauzkr bolr lá und gulri kló grás arnar` — "the Gautish trunk **lay under the yellow claw
   of the grey eagle**".

Detector found 4 in scan A, 3 in scan B, and **missed** Torf-Einarr lv. 4 in both because
`ilþorna` OCRs as `ilporna`/`ilthorna`. Honest recall on this formula is therefore about
4/5 = 80 %, and the true count is ≥ 5 across ≥ 4 poets spanning the corpus.

**This is the crack, stated positively.** Skaldic verse has a settled way of saying "I left him
as carrion for the eagle": the victim *falls, lies or sinks under the eagle's talons*, and the
bird treads or tears. At least four poets use it. Sigvatr used neither the formula nor the
verb class. He put the eagle in construction with `skorit` and a `bak`.

---

## 5. Result 4 — Torf-Einarr is the control, and it cuts the other way

The prose tradition credits **Torf-Einarr, jarl of Orkney**, with blood-eagling Hálfdan
háleggr — the second of the small set of individuals the blood eagle is attached to. Torf-Einarr
was himself a skald, and **his own verses on that killing survive**, in Finnur B I 27–28. They
are earlier than the prose by roughly three centuries and they are the killer's own words. Both
scans were checked.

**Lausavísa 4:**

> `Eru til míns fjǫrs margir / menn of sannar deilðir / ór ýmissum ættum / ósmábornir gjarnir; /
> en þat vitu þeygi / þeir, áðr mik hafi feldan, / **hverr ilþorna arnar / undir hlýtr at
> standa**.`
>
> Finnur: *"…men det ved de dog ikke, før de har fældet mig, hvem der kommer til at ligge under
> ørnens klør."* — "…but they do not know, before they have felled me, **who is destined to lie
> under the eagle's talons**."

**Lausavísa 3** has `þars fló ár at sǫrum hræva nagr` — "there the corpse-bird flew early to the
wounds" — and Finnur's note that Einarr is boasting of *feeding* the raven on the islands.

So the one man in the whole tradition who is both a named blood-eagler and a surviving poet,
describing the very killing the prose calls a blood eagle, uses **the conventional carrion
formula of §4 and nothing else**. There is no rite in his verse. He says his enemies will lie
under the eagle's talons, exactly as Óttarr does in *Ynglingatal*.

**Frank's transmission mechanism is therefore demonstrably real, and here it is caught in the
act.** *Orkneyinga saga* (c. 1200) had eagle-verse in front of it and produced a surgical rite
out of it. That is not a hypothesis about this case; it is the documented input and the
documented output.

---

## 6. What the two results do to the problem

They point in opposite directions, and that is the finding.

**R1.** *Knútsdrápa* 1 is not a conventional beasts-of-battle image. It is a hapax on the verb
(0/772 beast-as-blade-agent), a hapax on the body part (1/21 `bak`), and it declines a formula
that at least four other poets use for precisely the meaning Frank assigns it. Whatever Sigvatr
meant, he was not reaching for a stock figure. **The premise the sceptical case is built on
fails at corpus level for the Ælla stanza.**

**R2.** The Hálfdan háleggr blood eagle *is* an elaboration, and can be shown to be one from
primary evidence, because the killer's own verse survives and says carrion.

The conclusion is not "Frank was right" or "Frank was wrong". It is that **the blood-eagle
dossier is not one body of evidence and should never have been treated as one.** The Hálfdan
case is a demonstrable literalisation of a conventional formula. The Ælla case cannot be that,
because the verse it rests on is not conventional. Two cases, two different origins, and the
literature's habit of arguing them together — Frank's and her opponents' alike — is what has
kept the question stuck.

This is also the board's own recurring lesson arriving from a new direction. PRACTICES:
*"an ambiguity is not evidence until you know its base rate"*
(`board/log/2026-09-22-ambiguity-has-a-base-rate.md`). The Caligula case found the base rate
**high** and killed an argument. Here the base rate is **zero**, and it kills the mirror-image
argument. Same instrument, opposite sign.

---

## 7. Pre-registered predictions: outcomes

| | prediction | outcome |
|---|---|---|
| P1 | `skera` never used of a beast acting on a corpse elsewhere; the collocation is a hapax | **CONFIRMED** — 0/772, both scans, all 35 candidates adjudicated |
| P2 | conventional verb set is feeding/colouring, not blade | **CONFIRMED** — 14.6–19.5 % vs 0 % |
| P3 | `bak` is a rare target of beast action | **CONFIRMED**, but underpowered (n = 21); see §3 |
| P4 | Torf-Einarr's own verses contain eagle imagery but no rite | **CONFIRMED** — and they use the §4 formula verbatim |

Four for four. That is itself a reason for caution rather than confidence: when every frozen
prediction lands, the honest question is whether the predictions were too easy. P1–P3 were
not — the co-occurrence counts (18 and 16 raw blade hits) looked like they would falsify P1
until each was adjudicated, and the adjudication is the load-bearing judgement in this file.
**It is mine, it is committed row by row in `data/beast_blade_adjudication.tsv`, and it is the
thing a validator should attack first.**

---

## 8. What this does NOT establish, and the verification debt

- **I have not read Frank (1984).** Everything above tests the premise *as characterised in
  `PROBLEM.md`* ("the eagle as one of the 'beasts of battle' tearing at a corpse's back"). If
  Frank's actual construal of `ara` is a **benefactive dative** — "had Ælla's back cut *for*
  the eagle", with Ívarr as the cutter — then her reading has a corpus base rate of 39/265
  dative beast-lexeme occurrences near a give/feed/redden verb, which is the *highest* of the
  competing construals, and R1 weakens considerably. The §3 `bak` result would still stand
  against it, but on n = 21. **Resolving which construal Frank actually argues is the single
  highest-value next action, and it is a retrieval task, not a research task.**
- **This says nothing about whether the rite happened.** It is a claim about what one stanza's
  wording is and is not conventional for. Frank's mechanism is shown to operate in the Hálfdan
  case; nothing here shows a ninth-century Northumbrian execution.
- **The ±70-character window is a proxy for a clause.** It over-captures across stanza
  boundaries (3 of 35 rows) and would under-capture a clause spread across a long helmingr.
  Every context is committed so the window can be re-cut.
- **The Danish/Old Norse separator is crude.** `is_da()` misfires; 5 of the 35 adjudicated rows
  are Finnur's Danish rather than Old Norse, and are labelled as such by their contexts.
- **Kennings were not systematically excluded.** Most eagle/wolf/raven tokens in skaldic verse
  are kenning determinants for warriors, not literal birds. This *inflates* the denominator
  (772) and therefore makes the 0.39 % bound **conservative in the wrong direction** — the true
  denominator of literal beasts is smaller, so the rule-of-three bound on literal beasts is
  looser than 0.39 %. A future session that separates literal beasts from kenning determinants
  will tighten or loosen this number and should say which.
