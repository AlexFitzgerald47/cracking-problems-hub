# Progress

## 2026-09-05 — GPT-5.6 Sol — starting session

### 1. Primary evidence frozen

The National Library of Ireland catalogue record `vtls000655021` independently fixes the object and wording:

- date: **25 October 1923**;
- creator/context: IRA, Office of the Director of Intelligence;
- collection: Ernie O'Malley Papers;
- call number: **MS 10,973/15/24**;
- extent: one page;
- catalogue transcription: `Can any of 100's methods be used now that no VORFYDCGT?`
- broader memo topics: deputies in case of arrests, records for a commemorative book, and contact with prisoners.

Source: https://catalogue.nli.ie/Record/vtls000655021

No public scan of this exact one-page item has yet been located. Therefore the catalogue transcription is frozen as the working input, but the original glyphs, punctuation and whether `100` is definitely three digits remain an image-verification debt.

### 2. Solution-status check

Exact-string web searches for `VORFYDCGT` and the full surrounding sentence currently lead back to the NLI catalogue rather than to a published decipherment. Searches of indexed descriptions of Mahon & Gillogly's *Decoding the IRA* likewise produced no hit for this token.

This is **not proof of unsolved status**. The original book and archival finding aids still need a direct full-text/index audit. The problem remains provisionally open.

### 3. Same-office 1923 context: code words and prisoner communications are real

Three NLI catalogue records materially constrain the setting:

1. **25 June 1923, MS 50,300/6** — Michael Carolan, Acting Director of Intelligence, "confirms continued use of the existing code word" while corresponding with officers commanding prisons and camps.
   Source: https://catalogue.nli.ie/Record/vtls000742577
2. **19 July 1923, MS 50,300/15** — Carolan asks prisoners/camps to open new communication lines and requests a **coded list of safe addresses for letters**.
   Source: https://catalogue.nli.ie/Record/vtls000742759
3. **23–25 October 1923, MS 10,973/15/23** — the folder immediately preceding the target item contains Dublin intelligence and a note that the author will bring **Sean Lemass to Mountjoy Prison** because Lemass knows the prison better than "McDowell".
   Source: https://catalogue.nli.ie/Collection/vtls000655004/HierarchyTree?recordID=vtls000655004

This does not decode `VORFYDCGT`, but it changes the prior: a codeword, enciphered operational term, safe-address/contact mechanism, or prison-access/communications referent is now better motivated than treating the token as an isolated classical-cipher puzzle.

### 4. Known 1923 IRA short-cipher control reproduced

A published Gillogly example from 1923 contains short ciphertexts used to conceal transposition-key words. Secondary cryptology sources reproduce the set beginning `SDRDPX ...` and describe a six-letter Vigenere-family key reused from the start of each short item. The documented worked pair is:

`SDRDPX --GVZKLG--> MISTER`

A minimal reproducer is committed at `analysis/test_known_1923_key.py`. It uses ordinary A=0 Vigenere subtraction and asserts that the known pair recovers exactly before touching the disputed token.

Control result:

```
SDRDPX --GVZKLG--> MISTER
```

Target under the identical key/reset convention:

```
VORFYDCGT --GVZKLG--> PTSVNXWLU
```

`PTSVNXWLU` is not a plausible plaintext or obvious operational term. Therefore **reuse of the documented `GVZKLG` key with the same reset convention is rejected**.

This is a narrow negative result. It does **not** reject Vigenere-family encryption in general; a changed key, different alignment, encoded codeword, or another system remains possible.

Source for the short-key corpus and method description (secondary; original Mahon/Gillogly book remains the preferred verification target): https://studylib.net/doc/6596101/exercises

### 5. Structural constraints from the nine letters

`VORFYDCGT` contains nine distinct letters.

Consequences:

- internal repetition gives essentially no leverage for monoalphabetic substitution;
- any pure transposition must preserve the multiset `CDFGORTVY` exactly;
- a nine-character item is far below the point where unconstrained language scoring can certify a solution;
- therefore brute-force production of readable-looking candidates would be evidentially weak and was deliberately not treated as a crack.

### 6. Current hypothesis ranking

This is provisional and evidence-weighted, not a solution claim.

1. **Codeword or enciphered codeword tied to prisoner communication/access** — strengthened by same-office 1923 records and the target memo's own contact-with-prisoners topic.
2. **Short Vigenere-family item with a key other than `GVZKLG`** — historically demonstrated in IRA material in the same year; known-key reuse specifically failed.
3. **A key word for a longer transposition system** — also historically demonstrated; `VORFYDCGT` could itself be an encrypted key rather than ordinary prose.
4. **Other classical cipher / substitution** — technically possible but severely underdetermined at nine unique letters.
5. **Pure transposition of ordinary nine-letter plaintext** — possible in principle, but strongly constrained by the unusual exact letter multiset and currently unsupported.

### 7. What failed / what remains unknown

- The known May-1923 key `GVZKLG` does not decrypt the token under the documented reset convention.
- Exact-string searches did not identify an existing published solution, but absence has not been proven.
- `100` remains unidentified. This is now the single highest-value contextual unknown.
- No image of MS 10,973/15/24 has been inspected; catalogue transcription could conceal a reading issue.
- No candidate plaintext has enough external support to deserve promotion.

### 8. Next decisive experiments

1. **Identify `100`.** Search adjacent Director-of-Intelligence correspondence for numeric aliases and references to "methods". A named person/office could collapse the semantic search space.
2. **Get the page image.** Verify `VORFYDCGT`, `100`, punctuation, spacing and any annotations directly on MS 10,973/15/24.
3. **Build a 1923 short-cipher ledger.** Collect every embedded short ciphertext / encrypted transposition key from the Mahon-Gillogly corpus with date, key, reset convention and plaintext where known. Test whether keys rotate by date, correspondent or network.
4. **Mine the NLI 1923 prisoner-dispatch corpus for repeated codewords.** In particular trace the "existing code word" of 25 June and coded safe-address material of 19 July.
5. **Exploit the adjacent Mountjoy material.** Test whether the missing semantic slot in `now that no ____` corresponds to a person, prison-access mechanism, address/channel, document, or liaison that disappears between the July and October traffic.

### 9. Six-letter-key architecture screened independently of the actual key

The May 1923 example is more useful than a single known key: it demonstrates a **six-letter repeating Vigenere key reset at the start of each short item**. Under that architecture, even if the October key changed completely, positions 1/7, 2/8 and 3/9 of a nine-letter ciphertext impose exact equality constraints on the required keystream.

`analysis/filter_period6_words.py` derives the key stream required for every alphabetic nine-letter CMUdict entry and retains only words compatible with an arbitrary repeated period-6 key.

Corpus screened: **13,124** nine-letter entries.

Only four survive:

```
bilzerian    key=UGGGUM
embattled    key=RCQFFK
embezzled    key=RCQBZE
embroiled    key=RCQOKV
```

None is a natural ordinary-noun completion of `now that no ____`. Therefore, **if** the target is one ordinary nine-letter English word and **if** the same six-letter reset architecture was used, the hypothesis is strongly disfavoured by this screening corpus.

This is not a universal elimination: CMUdict is not all English; codewords, names, abbreviations and non-English material remain outside the test. But it materially reduces the appeal of the most obvious same-architecture/direct-English reading.

### 10. New archival target surfaced

The O'Malley collection description explicitly contains an **Inspection report for Mountjoy Prison, 1 October 1923**, only 24 days before the target memo. Because the target memo concerns prisoner contact and the adjacent 23–25 October intelligence folder discusses bringing Sean Lemass into Mountjoy, this six-page report is now a high-value contextual document to obtain or inspect. It may reveal the physical/contact "methods" being discussed even if it contains no cipher itself.

Collection/folder anchor: https://catalogue.nli.ie/Record/vtls000536116

No solve claim is made. The session has now falsified both (a) reuse of the known May key and (b), within a 13,124-word screening corpus, the broader hypothesis that an arbitrary six-letter reset key directly encrypts a normal nine-letter English word fitting the sentence.

## 2026-09-05 — continuation and correction

### 11. Correction: the `SDRDPX` Vigenere material is not established as 1923

Sections 4, 6, 7, 8 and 9 above incorrectly described the `SDRDPX ...` short-key list and `GVZKLG` control as a **1923 / May-1923** system. That chronology is withdrawn.

What is actually supported by the sources seen this session is narrower:

- Mahon/Gillogly and later cryptology exercises establish that this is **IRA material from the 1920s** and that Vigenere-family encryption was used to conceal short transposition-key words.
- The UCD Moss Twomey finding aid and secondary cryptology discussion warn that some later IRA documents were deliberately back-dated, including 1926–27 material carrying apparent 1923–24 dates.
- No primary or securely dated source seen so far ties the `SDRDPX ...` list or key `GVZKLG` specifically to May 1923.

Therefore the reproducer remains a valid **later-IRA-system comparison only**. Its failure on `VORFYDCGT`, and the period-6 dictionary screen, do **not** currently constrain the actual October 1923 cipher family strongly. The earlier same-year inference should not be propagated.

The superficially suggestive phase-offset output `KILKZTRAN` obtained when the later `GVZKLG` key is started at offset four is likewise downgraded to an ungrounded coincidence unless independent evidence connects that key/system to this traffic.

### 12. `100` identified: Frank Thornton

The highest-value contextual unknown in section 7 has been resolved.

The Irish Military Archives' official Collins Papers page captions a surviving item as:

`Communications between agent '100', F [Frank Thornton] and L [Liam Tobin], 13 July 1921.`

A UCD historian independently explains the Collins intelligence-agent numbering system and states explicitly that **Frank Thornton was Agent 100**.

This changes the target sentence materially:

`Can any of [Frank Thornton's] methods be used now that no VORFYDCGT?`

Important caution: Thornton supported the Treaty and served in the Free State Army during the Civil War. The 1923 anti-Treaty Director of Intelligence is therefore most plausibly invoking **Thornton's earlier Collins-era intelligence methods / institutional tradecraft**, unless evidence appears that the numeric alias `100` was reassigned after the split.

Source anchors:
- https://www.militaryarchives.ie/en/collections/online-collections/michael-collins-papers
- UCD / Irish Independent historical article on the Collins Papers agent-number system (session web research; exact publication metadata to pin in a later source audit).

### 13. What Thornton's documented methods were

Thornton's own Bureau of Military History evidence and supporting accounts make one method especially relevant: **identify, cultivate and handle insiders inside government/police institutions**.

Contemporary/reminiscence evidence describes Thornton and the GHQ Intelligence staff recruiting or turning policemen and other institutional insiders, and instructing intelligence personnel to develop sources inside enemy departments. Paired-source / cross-checking practices also appear in descriptions of his network.

This sharply raises the probability that `100's methods` means **insider recruitment / handling**, not a cryptographic algorithm.

A prison-specific precedent exists: Mountjoy warder **Patrick J. Berry** covertly assisted IRA prisoners and was later arrested on suspicion of supplying arms to them; other friendly warders are documented as carrying notes or facilitating prisoners. Thus the phrase can naturally describe using Thornton-style agent recruitment to restore a lost prisoner-contact channel.

### 14. 1923 prison-communications context strengthens the insider/channel reading

The June–July Carolan dispatches already show a sustained effort to rebuild secret communication with imprisoned anti-Treaty personnel. The collection-level description adds a physical concealment technique: thin dispatch flimsies could be rolled into **cigarettes with most tobacco removed** for smuggling.

Immediately before the target memo, Mountjoy's communications environment changed abruptly:

- the mass hunger strike began in mid-October 1923;
- escape tunnels were discovered around 17–20 October;
- prisoners were transferred between Mountjoy and Kilmainham;
- an official finding aid records three prisoners escaping from an ambulance between Mountjoy and Kilmainham on 20 October;
- the adjacent 23–25 October O'Malley folder discusses bringing **Sean Lemass to Mountjoy because he knows the prison better than 'McDowell'**.

The timing makes `now that no VORFYDCGT` especially likely to refer to a lost **person, route, access mechanism, address, or communications channel** rather than a general abstract noun.

### 15. Correct cipher-generation targets now identified

Two same-era archival items are much more valuable than importing the later Twomey/Gillogly system:

1. **20 Nov 1922:** an O'Malley-file `Copy letter to be coded, sent from Chief of Staff [Liam Lynch] to G.O.C. Cork`. If its encoded counterpart or associated instructions survive nearby, it could expose the actual Civil-War-era coding procedure.
2. **14 Apr 1923, NLI MS 10,973/15/16:** Free State Intelligence recorded a `translation of a cypher message about the cessation of hostilities and the ending of the Civil War`, explicitly mentioning `Notes captured on Austin Stack`. This is direct evidence that a contemporary anti-Treaty cipher was being translated by April 1923 and is now the highest-value known-plaintext/system lead.

The attack is switching to these contemporaneous items.

### 16. Revised live hypotheses

1. **Enciphered name/codeword for a lost prisoner-contact person or channel** — strongest overall because Thornton's `methods` are insider-recruitment methods and the memo is about prisoner contact.
2. **Operational codeword whose referent was lost during the Mountjoy/Kilmainham disruption of 17–21 October** — strong contextual fit.
3. **Contemporary 1922–23 anti-Treaty cipher applied to an ordinary term** — live, but the actual system must first be recovered from the Austin Stack translation / `to be coded` material.
4. **Cigarette / physical concealment route** — specifically motivated by the secret-dispatch corpus, but grammar and exact referent remain weak.
5. **Later 1920s Vigenere/transposition-key architecture** — downgraded; no secure chronological bridge to October 1923.

No plaintext is yet certified. The largest real advance is contextual: `100` is now Frank Thornton, and his documented method strongly predicts the semantic class of the missing token.