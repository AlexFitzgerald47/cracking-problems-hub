# The Junius attribution cannot be tested against Philip Francis with the surviving digitised evidence

**Session:** 2026-09-17, Hub Cracker routine, Claude Opus 5.
**Mode:** advancing. Takes the experiment the 2026-09-05 session specified and could
not run, because that session had no HTTP egress and this one does.

---

## Headline

The attribution of the *Letters of Junius* to Sir Philip Francis rests on comparing
Junius's anonymous political polemic with Francis's acknowledged private
correspondence. **That comparison is between two registers, and on this corpus the
register gap is larger than the gap between different authors.** Measured here:

| quantity | median Delta | n |
|---|---:|---:|
| same author, different register | **0.587** | 4 |
| different author, same register | **0.470** | 69 |

86% of different-author same-register pairs are closer together than the median
same-author cross-register pair. A cross-register comparison therefore cannot tell
"different author" from "same author writing something else", and no ranking of
Junius candidates built on one is evidence in either direction.

This is not a claim that the pipeline is weak. With register held constant the same
pipeline is accurate:

| test | result |
|---|---|
| Junius vs Draper, same volume, leave-one-out | **97/100 = 0.970** (chance 0.500) |
| Philo Junius (Junius's own second signature) placed with Junius | **23/23 documents** |
| Draper's independently transcribed 1772 text placed with Draper | **3/3 documents** |
| 11-author same-register leave-one-out | **0.884** (chance 0.091) |
| the same 11 authors, cross-register | **0.105** (chance 0.125) |

The method works. The evidence does not support the comparison the attribution needs.

**The sharpest single number:** Philip Francis's private letters and Philip Francis's
1784 parliamentary speeches sit **0.671** apart — further apart than Junius sits from
sixteen of the nineteen author/register cells in the panel, Francis's own two cells
included. On this measure Philip Francis does not match Philip Francis.

---

## What was done

### Corpus

All primary text was fetched and byte-checked in this session; see `data/SOURCES.md`
for the full manifest with sizes and measured OCR damage rates.

* **Junius, reference text.** The proofread Wikisource transcription of Woodfall's
  1772 first edition, one file per letter. The Wikisource page header says
  `author = Junius` on every numbered letter and this is **wrong** — Letter II is
  signed WILLIAM DRAPER and Letters LI and LIII are signed JOHN HORNE. Authorship is
  taken from the signature at the foot of each letter, never from the edition's
  framing.
* **Junius, second digitisation.** The 1813 Philadelphia reprint of Woodfall's 1812
  collection (2 vols, archive.org OCR), segmented the same way. Having the same
  letters from two editions and two transcription pipelines is what makes the
  edition/OCR effect measurable rather than assumable.
* **Philip Francis.** *The Francis Letters* (Beata Francis & Eliza Keary, 1901),
  both volumes, segmented per letter by the edition's "X TO Y." headers with
  "THE SAME TO THE SAME" resolved: **173 letters, 78,881 words, 1758–1814.** Plus
  his acknowledged *Two Speeches* (1784) for the public register.
  A Philip Francis author listing includes *A Complete Collection of Junius's
  Letters*; scraping an author bibliography would put the target inside the
  candidate's training data. The 2026-09-05 session flagged this trap and it is
  respected here.
* **Rival panel.** 14 further period writers — Burke, Johnson, Hume, Chesterfield,
  Walpole, Gray, Boswell, Sterne, Gibbon, Cowper, Wilkes, Price, Pownall, Boyd —
  in private letters, political prose and published formal prose. Hugh Boyd, John
  Wilkes and John Horne Tooke were themselves Junius candidates.
* Every author, **the candidate included**, is reduced to fixed-length chunks by one
  shared pipeline. Hand-cleaning Francis while machine-chunking the rivals would let
  Francis win on pipeline quality.

### Controls that made the result possible

The 1772/1812 Junius collections print, inside the same covers, in the same genre, on
the same subjects, in the same months, from the same press, and through the same
scanner: **Junius, Philo Junius (his own acknowledged second signature), Sir William
Draper and John Horne**. That is the only place in this problem where everything
except the author is held constant, and it supplies both a positive and a negative
control for free. It appears not to have been used this way before.

---

## Results

### 1. The famous `among`/`amongst` discriminator has almost no power

Junius prefers `among` over `amongst`. So does Philip Francis. So, it turns out, does
almost everyone:

**11 of 13 testable panel authors share Junius's preference** — Hume, Burke, Gibbon,
Boyd, Wilkes, Chesterfield, Price, Johnson, Gray, Cowper and Francis. The two that do
not (Walpole 0.47, Boswell 0.48) are mixed users, not `amongst` writers. The shared
preference is the period norm and carries essentially no information about identity.

**Audit correction to the 2026-09-05 Hub session.** That session reported that Burke's
1770 *Thoughts on the Cause of the Present Discontents* "uses `amongst` repeatedly in
clearly authorial prose", and concluded the feature "discriminates at least one serious
contemporary rival" and "is not merely generic eighteenth-century political usage."
The observation is true; the inference is not. Counted in full, in that very pamphlet
(Gutenberg 2173, 47,035 words): **`among` 23, `amongst` 10 — Burke prefers `among`,
0.70.** Across his correspondence the figure is 0.90. Presence/absence was the wrong
statistic. The prior session itself noted, in its point 6, that "some historical
features are gradients, not binaries"; that caution needed to be applied to its own
headline, and was not. Corrected forward, not deleted — the corpus trap that session
identified is real and load-bearing, and its four other findings stand.

Of the ten synonym variables tested, three survive a genre control with real
discriminating power (`farther/further`, `till/until`, `on/upon`), and on all three
Junius and Francis **disagree**. That is suggestive but it is not reported as a
finding, because §3 shows the register gap can produce exactly that pattern.

### 2. The edition/OCR gap is small; this is a positive methodological result

I expected transcription differences to swamp everything. They do not:

| comparison | mean Delta to the Junius-1813 centroid |
|---|---:|
| same author, same edition | 0.765 |
| same author, **other** edition (1772 proofread vs 1813 OCR) | 0.777 |
| **different** author, same edition (Draper) | 0.828 |

The author effect (0.063) is about five times the edition effect (0.012), and
Junius's 1772 text attributes to Junius 34/34 against 1813-OCR centroids. Function-word
Delta tolerates this level of OCR and edition variation. Cross-corpus comparison in
this problem is legitimate **on that axis**. The long-s damage rate in `data/SOURCES.md`
splits the corpus two-hundred-fold between eighteenth-century printings and later
reprints, and it still does not break the method.

### 3. The register gap does break it

Three panel authors survive in two registers (Burke, Johnson, Hume), and Francis makes
a fourth:

| author | registers | Delta |
|---|---|---:|
| Edmund Burke | private letters vs published prose | 0.382 |
| David Hume | private letters vs published prose | 0.561 |
| Samuel Johnson | private letters vs published prose | 0.613 |
| **Philip Francis** | private letters vs 1784 speeches | **0.671** |

Median 0.587, against a different-author same-register median of 0.470.

**Frozen prediction and test.** Before running it I predicted that if register
dominates author, cross-register attribution would collapse to chance while
same-register attribution stayed high, and set the failure condition that anything
near the same-register figure would refute the session's conclusion. Result:

* same-register, 11 candidates: **0.884** (chance 0.091)
* cross-register, private letters against formal-prose centroids, 8 candidates:
  **0.105** (chance 0.125) — *at or below chance*
* cross-register, the other direction, 11 candidates: 0.345

Prediction upheld. The most telling single confusion: **Philip Francis's private
letters are attributed to Edmund Burke 48 times** when the candidate set offers only
formal prose — even though Francis's own formal prose is among the candidates.

### 4. Where Francis actually lands, and why it should not be read as a result

For completeness, with both digitisations of Junius agreeing almost exactly:

* Author-pooled centroids, 15 candidates: **Francis ranks 8th** (1772 text) and
  **8th** (1813 text). Burke, Hume and Boyd are nearer.
* Junius's median nearest-author Delta sits at the **39th–50th percentile of the
  absent-author null** — the distribution produced by removing each known author from
  the candidate set and scoring their documents anyway. Junius looks like an author
  who is not in the panel. Given that the true writer need not survive in any
  digitised volume, that is the expected reading.

**These rankings are reported and should not be believed**, in either direction. They
are cross-register comparisons, and §3 establishes that cross-register comparisons on
this corpus run at chance. A ranking that puts Francis 8th is no more evidence against
him than a ranking that put him 1st would have been evidence for him.

---

## What this means for the problem

The problem statement asked whether modern methods reproduce Ellegård (1962), and
whether the evidence supports *Francis* or merely *Francis over the others considered*.
The answer found here is prior to both: **with the digitised evidence as it currently
stands, neither question can be answered**, because the only substantial body of
Francis's acknowledged prose is in the wrong register, and the register gap exceeds the
authorial signal.

I have **not** read Ellegård's 1962 monograph in this session and make no claim about
what he did. His method — synonym-choice variables — is not refuted here; §1 shows one
celebrated instance of it has no discriminating power on a proper competitor panel, and
§3 shows that any cross-register application of it inherits the register problem. Both
are reasons to re-examine, not grounds to declare the 1962 result wrong.

This is a negative result about evidence availability, not about Francis. He may well
be Junius. Nothing here counts against him, and the historical and circumstantial case
is untouched.

## What evidence would change it

Ranked by how much of the branch tree it would remove:

1. **≥20,000 words of Philip Francis's acknowledged prose in the public polemical
   register, 1769–1775.** This is the binding constraint and everything else is
   secondary. The *Two Speeches* (1784) are 19,119 words but twelve years late and
   parliamentary rather than journalistic, and they are the most OCR-damaged text in
   the corpus (long-s rate 0.021). Candidate sources: Francis's War Office
   correspondence; his signed contributions to the press; the Parkes & Merivale
   *Memoirs* (1867), downloaded here but not yet segmented.
2. **A second two-register author pair from the 1769–1772 window specifically.** The
   register calibration rests on n = 4. It is consistent and it is corroborated by the
   document-level prediction test, but four pairs is four pairs.
3. **Any anonymous 1769–1772 newspaper polemic of known authorship.** Same register,
   same venue, same years, known author — that would let the register confound be
   estimated inside the target genre instead of extrapolated into it.

---

## Reproducing

```
python3 src/fetch_wikisource_text.py    # resumable; Wikimedia rate-limits hard
python3 src/build_junius_wikisource.py
python3 src/build_junius_ocr_corpus.py
python3 src/build_francis_corpus.py
python3 src/build_panel.py
python3 src/synonym_test.py             # §1
python3 src/genre_effect.py             # feeds the variable filter
python3 src/matched_controls.py         # §2, and the power test
python3 src/register_calibration.py     # §3
python3 src/prediction_test.py          # §3 frozen prediction
python3 src/delta.py ; python3 src/delta_genre.py   # §4
```

Requires `numpy`. Results land in `results/*.json`.

## Limits, stated plainly

* The Wikisource fetch was rate-limited and was still running when this was written;
  the clean 1772 corpus covers a subset of the 69 letters. Every conclusion was
  checked against the complete 1813 OCR corpus and the two agree. `fetch_wikisource_text.py`
  resumes from disk.
* Register calibration n = 4. Corroborated by the independent document-level test but
  thin.
* Rival samples are machine-chunked from whole volumes with an apparatus filter, not
  hand-segmented. The filter is conservative but imperfect; residual editorial prose
  would push rivals *away* from Junius, which biases in Francis's favour, not against.
* Francis's letters in the exact Junius window (1768–1773) total only 10,131 words, so
  the Francis private-letter profile pools 1758–1814 and carries a chronology caveat.
* `delta_genre.py`'s positive/negative control section is confounded — Junius is the
  only public-letter class in that candidate set, so "nearest is Junius" partly means
  "nearest same register". It is kept for the record; `matched_controls.py` is the
  unconfounded version and is what §2 reports.
