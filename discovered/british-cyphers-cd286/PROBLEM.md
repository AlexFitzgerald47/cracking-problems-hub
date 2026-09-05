# British RIC and military cyphers in BMH CD 286

## The unknown

Can the British RIC and military code/cypher telegrams preserved in Bureau of Military History Contemporary Documents **CD 286, Group 2** be identified and decrypted, especially the series which the Bureau of Military History and National Library were unable to decode in the 1950s?

This is a concrete historical cryptanalysis problem, not a general study of codebreaking in the War of Independence.

## Why this is genuinely open

The official BMH Contemporary Documents register describes CD 286, donated by Kerry IRA intelligence officer **Tadhg Kennedy**, as containing British RIC and military code/cypher telegrams from June–September 1920/21. For Group 2 items 2–3 the register explicitly records that attempts to decode them by the **Bureau of Military History and the National Library failed**, and that the purported RIC key filed with item 1 did not appear to belong to those message series.

A fresh public-source search on 2026-09-05 did not locate a later published solution. That is not proof that no private/unindexed solution exists, so solution status remains an explicit audit task.

## Corpus / evidence readiness

**Mixed.** The metadata and surrounding historical evidence are remotely accessible, but the decisive CD 286 Contemporary Documents are not currently confirmed downloadable.

- Military Archives says the vast majority of the BMH Contemporary Documents series remains reading-room-only, although a major recent digitisation project captured tens of thousands of images and more material is intended for online release.
- Digitised Collins Papers and BMH witness statements are available remotely and contain substantial parallel evidence about the relevant RIC/military cipher systems.
- A photographed Mullingar RIC ciphertext is publicly reproduced by the Westmeath Examiner from the Collins Papers, providing at least one real ciphertext specimen for pipeline reconstruction.

**Current hard blocker:** obtain the actual CD 286 Group 2 telegram images/transcriptions. Until then, work should focus on recovering the systems, keys, cribs and parallel traffic so the target is ready the moment the ciphertext is obtained.

## Immediate breakthrough discovered during setup

Two historically distinct systems need to be separated:

1. **RIC/police cyphers.** James Hynes (BMH WS 867), a Mullingar Post Office clerk working for IRA intelligence, says he was given police keywords `STAMBOUL`, then discovered `REPUBLIC`, and later became able to determine new keywords himself. Contemporary/secondary reporting from the Collins Papers records later keywords including `HONDURAS`, `PERSIAN GULF` and `CUMBERLAND`.
2. **British military cyphers.** Hynes explicitly says he **never decoded military cypher messages because he never got a key**. Harry Conroy intended to teach him the **Playfair system used by the military**, but they never reached that point.

This makes surviving military Playfair traffic a particularly strong orphan-cipher seam.

Separately, BMH CD 286 is stronger than the generic Collins-mining target because the archive itself records failed historical decryption attempts.

## Known-plaintext / key opportunities

- CD 286 Group 2 item 1 contains 16 RIC/military telegrams plus a purported RIC key dated 31 May 1921.
- Group 2 item 3 contains similar messages, **some with decoded versions**. These can function as known-plaintext controls once images are obtained.
- Seán Kavanagh (BMH WS 524) describes acquiring both cipher telegrams and the same messages decoded, allowing construction of the current RIC figure-cipher key; later monthly keys were obtained from an insider. This proves that plaintext/ciphertext pairs existed in the intelligence network and may survive elsewhere.
- The Collins Papers include 1921 codebreaking correspondence and are searchable/downloadable online.

## First falsifiable experiments

1. **System reconstruction control.** Reconstruct the documented Mullingar police cipher from the known keywords and verify it against at least one known cipher/plaintext pair before applying it to unidentified traffic.
2. **Playfair discrimination.** On any candidate military ciphertext, test whether length, digraph behaviour and repeated-pair structure are consistent with period British Playfair rather than the RIC alphabetical system.
3. **CD 286 known-plaintext recovery.** When Group 2 item 3 is obtained, reproduce its supplied decodes from the message text without using the plaintext during derivation. Failure means the model/system is wrong.
4. **Unsolved-series attack.** Only after controls pass, apply the recovered system to Group 2 items 2–3 passages marked historically undecoded.

## Success criteria

A strong result is any one of:

- independently reproduce a supplied historical decode;
- identify the exact cipher family/key schedule used by one CD 286 series;
- recover a previously unrecorded plaintext from a telegram the archive marks undecoded;
- prove that a purported key cannot belong to a given series and identify the correct system;
- establish a rigorous access/information bound showing why a particular series cannot yet be solved.

## Time-waster warning

Do **not** assume every photographed British cipher is unsolved. The IRA historically recovered many RIC keys, and plaintext/key material often survives in different files. Build a solution-status ledger first. Also do not brute-force short ciphertexts before identifying whether they are police substitution/code traffic, figure cipher, or military Playfair.

## Sources

- Military Archives, *Appendix to Contemporary Documents Register*, CD 286, Tadhg Kennedy, Group 2: https://www.militaryarchives.ie/uploads/documents/Appendix_to_Contemporary_Documents_opt_05.pdf
- Military Archives, *Bureau of Military History 1913–1921*, description and digitisation status of Contemporary Documents: https://www.militaryarchives.ie/en/online-collections/bureau-of-military-history-1913-1921
- Military Archives, *Collins Papers 1917–1922*: https://www.militaryarchives.ie/en/online-collections/the-collins-papers-1917-1922
- James Hynes, BMH WS 867: https://bmh.militaryarchives.ie/reels/bmh/BMH.WS0867.pdf
- Seán Kavanagh, BMH WS 524: https://bmh.militaryarchives.ie/reels/bmh/BMH.WS0524.pdf
- Paul Hughes, “Mullingar was centre stage in Michael Collins’ intelligence war”, *Westmeath Examiner*, 3 July 2020: https://www.westmeathexaminer.ie/2020/07/03/mullingar-was-centre-stage-in-michael-collins-intelligence-war/
- Eneclann, BMH Contemporary Documents digitisation project: https://www.eneclann.ie/case_studies/bmhcd-military-archives/

## Notes

Difficulty: **high**, but potentially unusually high payoff.  
Tractability with text/compute alone: **moderate now; high if CD 286 images are obtained.**
