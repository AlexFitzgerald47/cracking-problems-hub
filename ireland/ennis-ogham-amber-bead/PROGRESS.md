# Progress — Ennis ogham amber bead

## 2026-09-06 — GPT-5.6 Sol — first cracker pass

### Goal

Freeze the inscription from the best remotely available object evidence, enumerate the real structural branches before language-fitting, and test the two inherited “magical formula” readings against that frozen evidence.

### Evidence inspected

- Hub instructions, cracker role and practices; live claim board checked before work.
- OG(H)AM January 2024 report based on direct British Museum examination in December 2023, including the multi-angle photographs.
- 1856 first published description / woodcut source (interpretation explicitly not attempted there).
- Macalister, CIIC vol. 1 (1945), no. 53.
- Arntz, *Das Ogom*, for the older `MTBCML` / Glenfahan comparison and Marstrander proposal.
- Westropp 1911 via Clare Libraries, specifically to audit the claimed Glenfahan parallel.
- OG(H)AM data-v1 `og_readings.csv` and `og_words.csv` as corpus controls.

Full URLs and source cautions are in `SOURCES.md`.

### Result 1 — the object is not securely a seven-character linear string

The 2023 direct examination reports:

- a detached `<`-like shape that does not meet the stemline and is not a known ogham character;
- a relatively clear middle `DMVA`, with `DMLO` retained as an alternative;
- a **split stemline** close to the perforation;
- a right branch apparently containing `VA`;
- a left branch ending in a separate oblique stroke.

That topology matters. A serialized text such as `?DMVA?VA` hides a choice about how a reader traverses a physical fork. The conservative upward-orientation graph already has four path serialisations (`?DMVAVA`, `?DMVA?`, `?DMLOVA`, `?DMLO?`). Allowing the opposite reading direction gives a lower bound of **8 structural cases** before assigning values to either anomalous mark. See `analysis/evidence-ledger.md` and `code/branch_model.py`.

### Result 2 — Macalister's `ATUCMLU` is falsified as a frozen transcription

Macalister's reading requires treating two anomalous V-shaped structures as the U-forfid. He explicitly said there was “little justification” for doing so. The modern object examination instead identifies the first as detached/non-standard and the later structure as part of a fork.

Therefore `ATUCMLU` remains a historical interpretive branch, but it is **not sufficiently secure to be the ciphertext/plaintext target**. Searching dictionaries or cryptic-ogham tables for meanings of `ATUCMLU` without first resolving the marks is downstream of an unstable input.

This is a negative result with high value: it removes the most common inherited string from privileged status.

### Result 3 — the old Ennis ↔ Glenfahan “same secret formula” argument does not reproduce on the modern transcription

Arntz reports:

- Glenfahan: `LMCBDV`;
- Ennis: `MTBCML`;
- reverse Ennis approximately resembles Glenfahan;
- Marstrander consequently proposed a common *rúnogam* in which vowels are supplied in alphabetic order, producing `LaMoCuBeDVi`.

Arntz himself calls the resulting interpretation unconvincing. More importantly, the December-2023 Ennis examination does not reproduce `MTBCML` or its reverse consonant skeleton. The apparent cross-object match is therefore contingent on an older Ennis reading rather than an independently stable property of the marks.

**Conclusion:** the Glenfahan analogy remains relevant to function/genre, especially given the bead's amuletic tradition, but it no longer supports a decipherment of the Ennis strokes.

### Result 4 — probable attribution/transmission error in Westropp's published comparison

The Clare Libraries transcription of Westropp 1911 says Ennis=`LMCBDV` and Fahan=`LMCBTM`. This conflicts with Arntz and with the later corpus tradition, in which Glenfahan is `LMCBDV`; the OG(H)AM data-v1 corpus likewise stores `LMCBDV` for the Glenfahan object while storing inherited `ATUCMLU` for Ennis.

The most economical explanation is that Westropp's account (or its modern transcription) has swapped the object assignments / derived comparison. Until the original printed plate and footnote are adjudicated, **do not count Westropp as independent support for Ennis=`LMCBDV`**.

### Corpus control

`og_readings.csv` was searched for the principal inherited strings:

- `ATUCMLU` exists as the inherited Ennis entry.
- `LMCBDV` exists for Glenfahan; a `LBMCBDV` variant also exists.
- no exact `DMVAVA` or `MTBCML` hit was found in the data-v1 search.

Because data-v1 predates the 2023 re-examination, absence of `DMVAVA` is expected and is **not** a linguistic argument.

The McManus-derived `og_words.csv` likewise gives no reason to privilege `ATUCMLU` as an ordinary formula or lexical item. This is only a sanity check: an amuletic/cryptic inscription need not be an ordinary dictionary word.

### What failed / was deliberately not done

- No dictionary-fit claim was accepted from any short serialization: the structural branch budget is too large and the input is not frozen.
- No simple reversal of the modern strings was treated as a legitimate opposite-direction transliteration. In ogham, stroke side/orientation can change character values; the opposite direction must be recomputed from geometry.
- Westropp's attractive comparator was initially treated as a possible independent witness, then **withdrawn** after cross-source checking showed the likely object-assignment conflict.

### Significant finding

The question has been materially reframed. The remote evidence does **not** currently support “decipher `ATUCMLU`.” It supports a branched-object problem with at least eight structural cases. Two historical magical/cryptic readings depend on mutually inconsistent linearisations, and the direct 2023 examination does not reproduce the old Glenfahan-like consonant skeleton.

The next decisive evidence is geometric: high-resolution photogrammetry/RTI or equivalent surface data around the fork and anomalous marks. That evidence can eliminate whole branches at once; additional word-searching cannot.
