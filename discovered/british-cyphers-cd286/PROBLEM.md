# British RIC and military cyphers — Tadhg Kennedy Group 2 (CD 286 / legacy CD 280)

## The unknown

Can the British RIC and military code/cypher telegrams preserved in Tadhg Kennedy's Bureau of Military History Contemporary Documents **Group 2, “Cyphers and Codes — British”** be identified and decrypted, especially the series which the Bureau of Military History and National Library were unable to decode in the 1950s?

This is a concrete historical cryptanalysis problem, not a general study of codebreaking in the War of Independence.

## Archive-reference warning

The current Military Archives appendix identifies the Kennedy collection as **CD 286**. Kerry Library's 2020 guide identifies matching Kennedy Group 2 material as **CD 280**. Public OCR derivatives can introduce further number errors. Until the archive clarifies the discrepancy, retrieve by **Tadhg Kennedy + Group 2 title + both CD 286/CD 280**, not by catalogue number alone.

## Why this is genuinely open

The official BMH Contemporary Documents register describes Kennedy Group 2 as British cyphers/codes from **June–September 1920**. It lists:

- item 1: 16 RIC/military telegrams plus a purported RIC key dated 31 May 1921, intended for June 1921;
- item 2: 10 similar messages;
- item 3: further manuscript/typed messages, **some with decoded versions**.

The register explicitly notes that attempts to decode the marked series by the **Bureau of Military History and the National Library failed**, and that the key filed with item 1 did not appear to belong to those message series.

A fresh public-source search on 2026-09-05 did not locate a later published solution. That is not proof that no private/unindexed solution exists, so solution status remains an explicit audit task.

## Corpus / evidence readiness

**Mixed.** The metadata and surrounding historical evidence are remotely accessible, but the decisive Kennedy Group 2 Contemporary Documents are not currently confirmed downloadable.

- Digitised Collins Papers and BMH witness statements are remotely accessible and contain substantial parallel evidence about the relevant RIC/military cipher systems.
- A photographed Mullingar RIC ciphertext is publicly reproduced from the Collins Papers, providing a real ciphertext specimen, although the newspaper image is too damaged to freeze every glyph safely.
- Group 2 item 3 reportedly contains decoded versions beside some messages, ideal for blind pipeline validation once scans are obtained.

**Current hard blocker:** obtain the actual Kennedy Group 2 telegram images/transcriptions. Until then, work should recover systems, keys, cribs and parallel traffic so the target is ready when the ciphertext arrives.

## Cipher families already reconstructed / identified

### 1. Early RIC paired-alphabet keyword cipher

Liam Archer, BMH WS 819, gives an operationally complete description. Despite calling it a “transposition”, it is a paired-alphabet substitution:

1. Deduplicate a keyword, normally 10–11 letters and no more than 13.
2. Append the earliest unused alphabet letters until the top row contains 13 characters.
3. Put the remaining 13 letters below.
4. Substitute each letter with the one directly opposite it; the mapping is self-inverse.

Archer's example resolves to:

```text
SWITZERLANDBC
FGHJKMOPQUVXY
```

so `F ↔ S`, etc. New monthly keywords were transmitted in the old cipher. `ric_cipher.py` implements this system and `test_ric_cipher.py` reproduces the historical row construction.

### 2. Later RIC systems

Archer records a later two-key version and then a homophonic figure cipher with multiple two-digit values per plaintext letter. Full key tables have not yet been recovered in this session.

### 3. British military Playfair

James Hynes (BMH WS 867) says he could decode police cyphers but **never decoded the military cypher because he never obtained a key**; Harry Conroy intended to teach him the **Playfair system used by the military** but did not reach that stage. Other BMH testimony also distinguishes military Playfair from RIC substitution and Auxiliary figure traffic.

This makes Kennedy's surviving military subset an especially strong orphan-cipher seam.

### 4. Separate two-word system

Eamon Broy describes a system using one daily word and one weekly word plus separate operating instructions. Collins and Broy could not use the correct words until the instructions were obtained. Treat this as a distinct family, not as the early RIC paired alphabet.

## Historically attested crib

BMH WS 1468 says RIC railway-warning messages were stereotyped, commonly beginning:

`BY TRAIN TO YOU NOW ...`

The first three cipher characters were dead/nulls. Aligning the next 15 characters to that formula supplied enough substitution information to continue breaking the message. This provides a historically grounded crib attack for appropriate RIC traffic.

## Known-plaintext / key opportunities

- Kennedy Group 2 item 1 contains a purported RIC key dated 31 May 1921.
- Group 2 item 3 contains messages **with decoded versions**, which must be held out as controls.
- Seán Kavanagh (BMH WS 524) describes obtaining both cipher telegrams and matching decoded messages, and later monthly keys, showing that plaintext/ciphertext pairs circulated in the intelligence network.
- Archer describes successful decryption of an Inspector-General-to-Cork message and says he copied all police cipher traffic passing through his office during parts of November 1920.
- The Collins Papers include searchable/downloadable codebreaking correspondence and known keywords such as `STAMBOUL`, `REPUBLIC`, and later Mullingar keywords reported as `HONDURAS`, `PERSIAN GULF`, `CUMBERLAND`.

## First falsifiable experiments

1. **System reconstruction control.** Validate `ric_cipher.py` on a securely paired historical RIC ciphertext/plaintext, not just Archer's key rows.
2. **Crib reproduction.** Reproduce the `BY TRAIN TO YOU NOW` attack on a suitable RIC railway message and verify that the recovered mapping predicts letters outside the crib.
3. **Playfair discrimination.** On candidate military traffic, test whether formatting/digraph structure is consistent with Playfair rather than RIC substitution.
4. **Kennedy known-plaintext recovery.** When Group 2 item 3 is obtained, hide supplied decodes and reproduce them from ciphertext/key/context.
5. **Historically failed-series attack.** Only after controls pass, apply the recovered system(s) to the messages marked historically undecoded.

## Success criteria

A strong result is any one of:

- independently reproduce a supplied historical decode;
- identify the exact cipher family/key schedule used by one Kennedy series;
- recover a previously unrecorded plaintext from a telegram the archive marks undecoded;
- prove that the purported key cannot belong to a given series and identify the correct system;
- establish a rigorous access/information bound showing why a particular series cannot yet be solved.

## Time-waster warning

Do **not** assume every photographed British cipher is unsolved. The IRA historically recovered many RIC keys, and plaintext/key material often survives in different files. Build the solution-status ledger first. Do not apply the RIC paired-alphabet decoder to military Playfair or numerical traffic, and do not treat hand-guessed transcription of a damaged image as ground truth.

## Sources

- Military Archives, *Appendix to Contemporary Documents Register*, Tadhg Kennedy Group 2, current CD 286 reference: https://www.militaryarchives.ie/uploads/documents/Appendix_to_Contemporary_Documents_opt_05.pdf
- Kerry Library, *Historical Sources on the history of County Kerry during the period 1919–1923* (2020), matching Kennedy material under CD 280.
- Liam Archer, BMH WS 819: https://bmh.militaryarchives.ie/reels/bmh/BMH.WS0819.pdf
- James Hynes, BMH WS 867: https://bmh.militaryarchives.ie/reels/bmh/BMH.WS0867.pdf
- Seán Kavanagh, BMH WS 524: https://bmh.militaryarchives.ie/reels/bmh/BMH.WS0524.pdf
- BMH WS 1468, testimony describing RIC substitution, military Playfair, Auxiliary figure code, dead-prefix practice, and the `BY TRAIN TO YOU NOW` crib.
- Military Archives, *Collins Papers 1917–1922*: https://www.militaryarchives.ie/en/online-collections/the-collins-papers-1917-1922
- Paul Hughes, “Mullingar was centre stage in Michael Collins’ intelligence war”, *Westmeath Examiner*, 3 July 2020: https://www.westmeathexaminer.ie/2020/07/03/mullingar-was-centre-stage-in-michael-collins-intelligence-war/

## Notes

Difficulty: **high**, with unusually high historical payoff if the raw Kennedy telegrams are obtained.  
Tractability with text/compute alone: **moderate now; high with Group 2 scans.**
