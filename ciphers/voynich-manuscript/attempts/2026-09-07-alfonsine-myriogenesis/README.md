# Frontier attack: Alfonsine myriogenesis as the missing zodiac crib

**Date:** 2026-09-07  
**Status:** active lead; not a solve claim  
**Target:** recover an external ordered crib for the Voynich zodiac labels, which would turn the recent verbose/homophonic mechanism work into plaintext constraints.

## Why this is the solve route

Recent 2026 work by Vitaly Averyanov argues that the Voynich zodiac labels are approximately two-letter sigla in closed, sign-specific lists of ~30 entries and publishes a falsification pipeline for external degree-name lists. Its negative program tested seven source classes: Astrolabium-planum/Pietro-d'Abano degree images, cisiojanus, sanctorals, Liber Hermetis planetary monomoiriai, Firmicus paranatellonta, Alfonsine star catalogues, and herbal/pharmacopoeial lists. It reports no surviving external crib.

A separate August-2026 unit-scale paper by Rozanova & Temerev independently strengthens the premise that visible Voynich glyphs/tokens/spaces should not be assumed to be plaintext letters/words/boundaries, making a variable/verbose external crib attack more plausible than another monoalphabetic solve.

The best path to an actual reading is therefore not to hill-climb the whole manuscript again. It is to find a period, ordered, 30-per-sign source whose entries can anchor the zodiac sigla and thereby constrain the lost code tables.

## Candidate missed by the published negative ledger

**Alfonso X's Libro de Astromagia / Alfonsine myriogenesis (moirogenesis), ultimately drawing on Arabic degree/paranatellonta traditions.**

This is materially different from the tested 1488 *Astrolabium planum* degree-image catalogue.

The crucial structural description in Peter J. Forshaw's study of Alfonsine magical manuscripts is:

- the *Libro de Astromagia* has a **central image of the zodiac sign**;
- it has **two rings**;
- the **outer ring represents each degree**;
- the **inner ring contains a brief description of the fate/nature of the person born in that degree**.

Forshaw gives a concrete Taurus example: degree 1 is represented by a man leading a bull and its native is unhappy/unlucky; degree 2 is a woman with a tambourine and its native loves entertainment/music.

The Biblioteca Virtual Miguel de Cervantes survey of Alfonso's astromagical works likewise describes the *monomoiriai/myriogenesis* as a separate influence/fate for **every degree of every sign**, and identifies the *Libro de Astromagia* as preserving individualized degree figures. It notes that the detailed Alfonsine system may derive from an Arabic work attributed to Tankalusha/Teucer.

This matters because the Voynich zodiac has the same unusual macro-architecture: central zodiac sign plus rings totalling about thirty human figures/labels per sign. The correspondence was noticed informally in Voynich discussion as early as 2002, including an attempted Leo/Regulus alignment, but I find **no test of the ordered Alfonsine native/fate text in the Hub and it is not one of Averyanov's seven reported crib classes**.

## The leap

The prior crib search assumes the short Voynich labels abbreviate a list of *names*. I propose a broader and more historically motivated possibility:

> **Each Voynich nymph label is a code/siglum for the degree's `native` or diagnostic fate/quality in an Alfonsine-style myriogenesis, not necessarily a proper name.**

That changes the candidate extraction rule. For each degree, extract the first or most distinctive content word in the *native/fate clause* (or, separately, the figure description), normalize to its first two plaintext letters, and feed those ordered 360 sigla into the existing external-crib pipeline.

This is not post-hoc word fishing if the extraction rules are frozen before seeing Voynich correspondences.

## Preregistered candidate variants

Run these as separate candidates and count all against the same multiplicity budget:

1. **NATIVE-FIRST-NOUN:** first content noun in the degree's native/fate description.
2. **NATIVE-FIRST-ADJ:** first adjective/property applied to the native.
3. **NATIVE-DISTINCTIVE:** deterministic TF-IDF-like most distinctive lemmatized content word within each 30-degree sign, ties resolved by earliest occurrence.
4. **FIGURE-FIRST-NOUN:** first content noun in the degree-image description.
5. **FIGURE-DISTINCTIVE:** deterministic most distinctive content word in the image description.

Do not invent a sixth rule after looking at results.

## Hard predictions

A genuine relationship must satisfy all of these:

1. **Profile before alignment.** The chosen 30-item lists must naturally land near the observed Voynich ring regime (~20-25 distinct effective two-letter types per 30), rather than being forced there.
2. **Order matters.** Under one global orientation/offset model, same-siglum degree pairs must predict Voynich label-pair part sharing better than within-sign permutations.
3. **Cross-sign replication.** Fit/choose orientation on a strict subset of signs and predict held-out signs. No sign-specific shifts.
4. **Source-layer stability.** If Latin/Old Spanish/Arabic witnesses of the same myriogenesis survive, the signal should be supported by concepts already present in the earliest layer, not late wording.
5. **Iconographic side prediction.** Degrees whose source figure is female/male, crowned, clothed/nude, or carries a salient object should show above-null agreement with independently coded Voynich nymph attributes if those attributes are part of the same degree tradition. This must be scored blind to labels.
6. **Known Leo test.** The old 2002 observation predicts the degree corresponding to Regulus / `little king` should land on the crowned Voynich Leo nymph under the same orientation used globally. Treat this only as a held-out iconographic check, not as an alignment seed.

## Falsifiers

Kill the candidate if:

- profile diversity fails before any positional test;
- significance disappears under held-out signs;
- each sign needs its own rotation/reversal;
- the best extraction rule was selected after examining Voynich fit without paying the full search budget;
- any apparent signal is supported only by a late witness or vocabulary absent from the medieval source layer.

## Sources checked this session

- V. Averyanov (2026), *Thirty Names per Sign* / Voynich Studies: reported zodiac-label structure and seven-class negative ledger.
- V. Averyanov (2026), *A Workshop Cipher*: reported Naibbe-class verbose/homophonic mechanism; explicitly no recovered key.
- L. Rozanova & A. Temerev (2026), arXiv:2608.17096: glyph/token/space unit assumptions rejected under matched controls; recurrent multi-symbol units and graded boundaries.
- P. J. Forshaw, *From Occult Ekphrasis to Magical Art* / discussion of Alfonso X's astromagical manuscripts: central sign + two-ring myriogenesis, degree images plus native/fate descriptions.
- Biblioteca Virtual Miguel de Cervantes, *Imágenes mágicas. La obra astromágica de Alfonso X...*: monomoiriai/myriogenesis background and individualized degree figures; possible Tankalusha/Teucer source lineage.
- Voynich mailing-list archive, Sept. 2002: prior informal comparison of *Libro de Astromagia* degree figures to Voynich zodiac, including Leo/Regulus/crowned-nymph observation. This establishes that the iconographic resemblance itself is not new; **the new attack here is the explicit use of the ordered native/fate clauses as a frozen external siglum crib against the 2026 cipher/label pipeline.**

## Blocker / next action

The binding input is a machine-readable transcription of the 360 Alfonsine myriogenesis degree entries, ideally Alfonso D'Agostino's 1992 edition of *Astromagia* or a primary manuscript transcription. Once obtained, the five frozen extraction rules above can be run through the published label pipeline. Do not substitute modern summaries for the 360 ordered entries.

## Assessment

This is a higher-value solve attempt than another unconstrained whole-text optimizer because it attacks the exact missing object identified by the strongest 2026 mechanism work: an **external ordered crib**. It also has an independently motivated iconographic architecture unusually close to the Voynich zodiac and predates the manuscript by more than a century. It is not yet evidence of plaintext and must not be described as a decipherment until the positional and held-out tests pass.
