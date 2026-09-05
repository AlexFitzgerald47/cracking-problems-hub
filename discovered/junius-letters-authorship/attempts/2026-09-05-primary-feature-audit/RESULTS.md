# 2026-09-05 primary-feature audit

## Question

Before building a modern classifier, does the famous Ellegård lexical signal survive direct inspection of primary texts, and is the comparison corpus clean enough to support automated attribution?

## Sources inspected

### Junius
- *The Letters of Junius*, complete volume, Internet Archive identifier `lettersofjuniusc00juniiala` (1786 scan/OCR). This is a later collected edition; the 1772 Woodfall text is separately available on Wikisource and should be the eventual canonical transcription.
- Wikisource, *Letters of Junius* (Woodfall 1772), used to confirm that the collection contains both Junius/Philo-Junius letters **and replies by other writers**. A whole-volume scrape is therefore not an author-pure corpus.

### Philip Francis — gold-standard texts
- Philip Francis, *Two speeches in the House of commons on the original East-India bill and on the amended bill* (1784), Internet Archive identifier `twospeechesinhou00franiala`. The scan metadata explicitly names Francis as author. This is the closest clean, substantial, machine-readable acknowledged Francis text located in this pass.
- Philip Francis, *A letter missive ... to Lord Holland* (1816), Internet Archive identifier `lettermissivefro00fran`. Used only as a **temporal-drift check**, not as a same-period training document.

### Rival micro-control
- Edmund Burke, *Thoughts on the Cause of the Present Discontents* (1770), proofread Wikisource transcription of the 1770 J. Dodsley edition. This is unusually useful as a first control because it is contemporaneous political argumentative prose rather than a modern or cross-genre comparison.

### Excluded from gold standard
- *A State of the British Authority in Bengal* (1780/1781): catalogue records describe these as anonymous and merely attributed/contributed to Francis. They are useful later as disputed/secondary tests, not clean training data.
- Any corpus assembled by blindly taking every work on a Philip Francis author page. The Wikisource author listing includes *A Complete Collection of Junius's Letters* under Francis. Feeding that into a Francis training set would leak the target text into the candidate corpus and make any classifier result circular.

## Primary-evidence audit of Ellegård-style choices

The historical benchmark most often quoted for Ellegård is that Junius used **among** 35 times and **amongst** zero times, while Francis used **among** 66 times and **amongst** once. I did not trust those counts as data; I tested the direction against independent primary OCR and then added Burke as a same-era rival.

| Feature | Junius collected OCR | Francis 1784 acknowledged text | Burke 1770 rival | Francis 1816 drift check | Interpretation |
|---|---|---|---|---|---|
| `among` / `amongst` | `among` repeatedly present; **no `amongst` hit** | `among` repeatedly present; **no `amongst` hit** | **both forms repeatedly present**, including clearly authorial `amongst` | both forms present | The famous Francis/Junius direction replicates and **does discriminate one serious same-era rival**. It is not merely generic eighteenth-century usage. |
| `farther` / `further` | authorial `farther` present; an inspected `further` hit occurs inside quoted external material | Francis's own prose repeatedly uses `farther`; inspected `further` hit is in the quoted House order introducing the speech | both forms occur in clearly authorial prose | not audited | Francis/Junius resemblance exists, but Burke shows this is not a binary discriminator. Quotation contamination still matters. |
| `until` / `till` | both occur | both occur | not audited | both occur | Not a clean binary discriminator; must be estimated as a proportion, as Ellegård did. |
| `completely` / `entirely` | both occur | both occur; at least one `entirely` hit is in a quoted Richard Barwell minute | not audited | not audited | Again requires quote stripping and proportional treatment. |
| `I do not mean to ...` | frequent authorial construction | frequent authorial construction | not audited | not audited | A plausible syntactic/style feature, but it is not evidence until compared with a larger contemporaneous rival set. |

### First rival result

Burke's 1770 pamphlet breaks the most useful micro-feature in the right direction: he uses `amongst` repeatedly in unmistakably authorial prose (for example “the temper of the people amongst whom he presides” and later “raise divisions amongst them”), while also using `among`. By contrast, the searchable Junius OCR and Francis 1784 OCR return no `amongst` hit.

That makes the replicated `among` preference more interesting than a Francis/Junius coincidence alone: **one contemporary political-prose rival fails the same test.** This is still a one-feature, one-rival micro-control, not an attribution result.

Burke also uses both `farther` and `further` authorially (“a farther aid”; “going further”), so that axis does not cleanly separate him. This is a useful negative control against over-reading one attractive synonym pair.

## The important finding: source segmentation is not optional

The 1784 Francis book is not 89 pages of Francis prose. It embeds the parliamentary order, bill language, Company correspondence, minutes, and other documentary quotations. The Junius volume likewise contains answers by Draper and others, quotations from legal/political sources, editorial material, and index matter.

This matters *inside the exact type of variables Ellegård used*. In the Francis scan, the search hit for `further` at the start of the second speech is in the quoted procedural formula — “into further consideration” — whereas Francis's surrounding authored prose uses `farther`. In the Junius scan, an inspected `further` hit is likewise within quoted external material. Counting raw OCR without speaker/source segmentation would attribute another writer's lexical choice to the candidate.

That is a concrete failure mode, not a theoretical warning.

## What this does and does not establish

### Established
1. **A real Francis/Junius lexical resemblance survives direct primary-source inspection.** The `among` > `amongst` preference is present in Junius and independently in Francis's acknowledged 1784 prose.
2. **That resemblance survives a first same-era competitor check.** Burke's 1770 political pamphlet uses `amongst` repeatedly, unlike the two target/candidate texts inspected. This modestly increases the evidential value of the feature.
3. **The most obvious automated corpus construction is invalid.** Author-page aggregation can leak Junius into “Francis”; whole-book OCR can mix Francis with quoted speakers/documents; whole Junius editions mix Junius with opponents and quotations.
4. **Chronology can move the features.** Francis uses `amongst` in the 1816 letter, so a model trained indiscriminately across his lifetime can dilute or distort his 1760s/1770s style.
5. **At least one classic synonym axis (`farther`/`further`) is demonstrably sensitive to quotation contamination in the primary material.** Burke's use of both forms also shows that this axis alone is weak.

### Not established
- This is **not** a solve and is not a valid modern attribution yet.
- I have not reproduced Ellegård's exact 458 lexical + 51 synonym-variable table.
- One Burke control is not an open-set null; Francis's resemblance cannot yet be called unique among serious candidates.
- OCR is visibly noisy (`long-s` -> `f`, broken hyphenation, etc.), so character n-grams should not be trusted until scans/transcriptions are normalized or source-matched.

## Prediction for the next falsifiable test

Build a source-segmented corpus containing only authorial prose, split by document rather than random chunks, and evaluate the historical 51 synonym variables plus function-word features on held-out known-author texts. Then score Junius against Francis and contemporaneous political-prose rivals.

**Prediction if the Francis attribution is genuine:** Francis should remain the nearest candidate across held-out documents and across quote-stripped synonym/function-word feature sets, not merely on the historically selected `among` feature. A credible open-set result also requires unrelated rival authors to fall outside the Francis/Junius similarity range.

**Failure condition:** if Francis ceases to lead once quotes, disputed Francis items, target leakage, and chronology are controlled, the celebrated old stylometric case has been measuring corpus construction rather than authorship.

## Source URLs / identifiers

- Junius OCR: `https://archive.org/stream/lettersofjuniusc00juniiala/lettersofjuniusc00juniiala_djvu.txt`
- Francis 1784 OCR: `https://archive.org/stream/twospeechesinhou00franiala/twospeechesinhou00franiala_djvu.txt`
- Francis 1816 OCR: `https://archive.org/stream/lettermissivefro00fran/lettermissivefro00fran_djvu.txt`
- Woodfall 1772 transcription index: `https://en.wikisource.org/wiki/Letters_of_Junius`
- Burke 1770 proofread transcription: `https://en.wikisource.org/wiki/Thoughts_on_the_Cause_of_the_Present_Discontents`

All claims above were checked against the displayed primary OCR/transcription or catalogue metadata in this session. Historical Ellegård totals are treated as a benchmark to reproduce, not as new evidence.
