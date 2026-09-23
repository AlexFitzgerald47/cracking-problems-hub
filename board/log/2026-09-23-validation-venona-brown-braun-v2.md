# Validation — VENONA BROWN/BRAUN — validator 2

claim: that the 1940 London GRU covername **BROWN / BRAUN** was "most likely" **Frederick William Meredith**, and (linked) that **POULTRY-DEALER** was "most likely" **Wilfrid Foulston Vernon**, with the Henry Hughes information channel explained by Smiths Aircraft Instruments' 1935 controlling interest in Henry Hughes & Son. Claimed in `board/log/2026-09-06-venona-meredith-brown-provisional-crack.md` and `board/log/2026-09-06-venona-meredith-solve-attempt.md`; argued in `historical-controversies/venona-brown-braun/analysis/frederick-meredith-brown-candidate.md` and `analysis/wilfrid-vernon-poultry-dealer.md`.

problem: `venona-brown-braun`

criteria applied: quoted verbatim from `historical-controversies/venona-brown-braun/PROBLEM.md`, "Success criteria":

> ### Full crack
> A real individual is identified who independently satisfies the primary-cable constraints, with documentary evidence tying that person to BROWN's Soviet/Communist network and explaining the Henry Hughes information channel.
>
> ### Strong partial crack
> Reduce the search to a small candidate set and demonstrate which role model (Henry Hughes insider vs intermediary/handler) best explains all three cables, with at least one new archival/documentary link.
>
> ### Falsifiable candidate standard
> A candidate should be tested against:
> - alive/present in Britain in summer 1940;
> - plausible London/Essex geography;
> - access to or a direct contact inside Henry Hughes's echo-sounder work;
> - Communist/Soviet trust-network evidence consistent with No. 876;
> - ability to participate in clandestine W/T logistics / use of a flat;
> - chronology consistent with all three messages;
> - no contradiction from occupation, military service, known residence or security files.

validator role: 2 (assigned angle: **the candidate field** — was the search exhaustive or did it stop at the first plausible name; and **covername semantics** — is there any positive reason BROWN maps to Meredith)

reproduced: **partially** — the three cables and their surrounding traffic reproduce cleanly from the raw source, and I independently recovered two corrections to the text the project has been working from. The *identification* does not reproduce: rebuilt from the cables alone, the constraint ledger does not select Meredith, and it ranks him below candidates the project had already generated and then set aside.

---

## What I actually did

I worked from the raw cables before reading any candidate dossier's conclusions, and I did not read validator 1's verdict until after I had formed my own reading and finished my own extraction.

1. Downloaded the Wilson Center aggregate (`Venona-London-GRU.pdf`, 564 KB). No `pdftotext` exists here and `pypdf` will not import (the `cryptography` Rust bindings panic), so I wrote a zlib + `Tj`/`TJ` content-stream extractor and pulled the whole corpus to text (26,804 lines).
2. Read **No. 798** (22 Jul 1940, 3/PPDT/T30), **No. 876** (13 Aug 1940, 3/PPDT/T45) and **No. 976** (4 Sep 1940, 3/PPDT/T50) in full with footnotes, plus the whole POULTRY-DEALER corpus — **882** (14 Aug), **1112** (4 Oct), **1141** (9 Oct).
3. `media.defense.gov` returns **403** through the agent proxy. I pulled the NSA scan of No. 976 from the Wayback Machine, found only a badly degraded OCR layer, extracted the embedded `DCTDecode` JPEG by hand and read the **image** of the original typescript, then cropped and 5× upscaled the critical footnote line to settle a word.
4. Reconstructed the **residency outgoing-number series** across the corpus by regex, to test PROBLEM.md's own "No. 256" trap note.
5. Built a **covername register inventory** from every footnote gloss in the corpus (45 distinct covernames), to test whether BROWN/BRAUN carries any identifying information.
6. Re-checked the load-bearing secondary facts myself: Grace's Guide on Henry Hughes & Son; Wikipedia on Meredith, Weiss and Vernon; the Dulwich Society Vernon article (via Wayback, the live site would not serve); the Filton raid of 25 Sep 1940.
7. Read `harry-fraser-candidate.md`, `fraser-residence-kill-test.md`, `george-barnard-candidate.md`, `poultry-dealer-candidate-comparison.md`, `constraint-ledger.md` and `HANDOVER.md` **as a record of how the candidate field was generated and closed**, which is my assigned angle.

---

## Part 1 — two corrections to the working text (independently recovered)

I found these before reading validator 1. V1 reports both. **Convergence here is not independent confirmation in the strong sense** — we used the same two sources and, it appears, a similar hand-rolled extraction route, which is exactly the correlated-error risk `VALIDATOR.md` warns about. I record them because the first is unambiguous from the page image and both change the constraint ledger.

**(a) "illicit ink" is "illicit LINK".** Footnote [iv] to No. 976 in the Wilson Center transcription reads "sent on BROWN's illicit **ink**". The NSA typescript, magnified, reads without ambiguity:

> "It is possible that it should have been sent on BROWN's illicit **link** (see LONDON's No. 798 of 22nd July 1940)."

The cross-reference settles it independently of the glyphs: No. 798 contains no secret writing. It contains a flat and a W/T set for BRAUN. "Ink" makes the cross-reference meaningless; "link" makes it exact. **The VENONA annotators read No. 798 as giving BROWN a clandestine radio link of his own**, and thought the 4 Sep report anomalous precisely because it went by Embassy cipher instead of over that link.

This *raises* the W/T bar rather than lowering it. `analysis/stanley-role-separation.md` is correct that the *operating* role is STANLEY's, but the set and the flat are attached to BROWN in all three references — "a flat at once **for BRAUN** with a MUSIC" (798 §3), "a MUSIC **from BROWN**" (876 §1), "**BROWN's** illicit link" (976 fn iv).

**(b) No. 876 more naturally says BROWN *leaked* the set than *supplied* it.** Raw text:

> "POULTRY-DEALER [KURNIK] has reported that the Area Secretary of the CORPORATION [KORPORATsIYa] knows about the presence of a MUSIC [MUZEKA] from BROWN. POULTRY-DEALER considers BROWN to be [B% devoted to our cause] but talkative."

PROBLEM.md §2 and `constraint-ledger.md` C4 render this as a set "obtained from/through BROWN". The reading that makes "but talkative" and the remedy cohere is that the Area Secretary heard of the set **from** BROWN. Either way the operative constraint is the same and it is demanding: **BROWN was in ordinary conversational range of a local CPGB Area Secretary.** That is a branch-level party man, not a compartmented technical source.

**(c) Footnotes [ii] and [iii] to No. 976 are blank in the NSA original too.** Nothing was lost in transcription; there is no NSA gloss on the Henry Hughes works or the instrument to recover. Confirmed from the page image.

---

## Part 2 — the constraint ledger rebuilt from the cables

| # | From the raw text | What it demands of BROWN |
|---|---|---|
| B1 | 798 §3: "We shall find a flat at once for BRAUN with a MUSIC. STENLI has already learnt how to use the code and will come to work on the days [B% indicated by you]." | BROWN is the **host of the transmitter site**. STANLEY travels to it. |
| B2 | 798 §5: "STENLI receives material from us via BRAUN." | BROWN is a **downward** conduit — Soviet material to STANLEY. In this cable he is not a collector at all. |
| B3 | 798 §5: "will be put in touch with MINISTR or with our man depending on your instructions" | As of 22 Jul 1940 BROWN was **not yet** in direct contact with a Soviet officer. |
| B4 | 876 §1: Area Secretary / "talkative" | Branch-level CPGB embedding, socially loose. |
| B5 | 876 §1A: "BROWN will move to his old flat" | Two flats, three moves, six-week London footprint. |
| B6 | 976: "received direct from the production line [PROIZVODSTVO] at the HENRY HUGHES works in LONDON" | A channel reaching the **shop floor** at Hainault / Forest Gate / Ilford. |
| B7 | 976 fn iv: BROWN's own illicit link | BROWN holds a clandestine W/T link. |

Two structural observations that follow from my own extraction:

**The "No. 256" series is a single residency officer sequence, and BROWN sits inside it.** I reconstructed the run: 205 BARCh, 207 DICK, 211 DICK, 212 BARCh, 213 BARCh, 218 DICK, 219 BARCh, 220 DICK, **221 BARCh (=No. 876)**, 224 DICK, 225 BARCh (=No. 882), 226 DICK, 227 BARCh, 228 BARCh, 230 DICK, 231 BARCh … 252 DICK, 254 DICK, 255 BARCh, **256 BROWN**, 259 BARCh. PROBLEM.md's trap note is confirmed — 256 is a local outgoing number, not an agent number. But the stronger fact is the one the trap note does not draw: **every other holder of a number in that series is an Embassy officer** (BARCh ≈ Kremer, DICK, later BRION). The NSA annotators flag this themselves as "the only known occurrence in LONDON GRU messages of an agent outside the Embassy signing a message passed in the Embassy cipher by Embassy facilities" — i.e. they treat the identity of the No. 976 *signer* with the No. 798/876 *subject* as anomalous. That identity is an inference from name-identity, not an established fact, and **the claim treats C7–C9 as unproblematically BROWN-the-agent's own report.** A reading in which the No. 976 signature belongs to the residency side was never enumerated.

**POULTRY-DEALER's reporting range is national, not local.** 1141 §2 has POULTRY reporting Eastern Command HQ (Hounslow), **70–80 small river-type vessels landed at Hull**, and the **Bristol Aircraft Factory** raid. I checked the last against the record: Filton, 25 Sep 1940 — ~57 He111s, 168 bombs, 132 killed (91 of them company workers), a shelter taking a direct hit. POULTRY reports "about 80" aircraft, "about 200" bombs, "123 people", and "slightly damaging two workshops". That is **inflated, second-hand grapevine reporting**, of a raid 120 miles from Hounslow, filed alongside a Hull item. POULTRY is a rumour-collector with a national catchment, in the same class as THERAPEUTIST (aerodrome gossip) and BUSINESSMAN (parachutists at Newbury) in the same cable. This matters below.

---

## Part 3 — my assigned angle (i): was the candidate field exhausted?

**No. It was closed by instruction, and the record of the closure is in the project's own files.**

This is not an inference about the claimant's state of mind. It is documented:

1. **Fraser was never killed.** `fraser-residence-kill-test.md` (2026-09-05) ends: *"Test status: BLOCKED / UNRESOLVED — not passed."* The next day the Meredith dossier's comparison table demotes Fraser to "downgraded #2/3" on the entries "No direct proof" and "None found". **No new evidence about Fraser was acquired between the two documents.** He was downgraded on *absence of evidence*, on the same day Meredith was promoted on an *inference from corporate ownership*. That asymmetry is the whole pivot.

2. **Barnard's own dossier prescribed a research program that was abandoned the next day.** Its closing verdict: *"The key new research object is therefore no longer one man. It is the **1940 Plessey Communist/industrial network**, especially shop stewards and the local Party area structure, intersected with Henry Hughes personnel."* That is the correct object given B4 and B6. It was never pursued.

3. **The solve-attempt handoff closes the field explicitly.** `2026-09-06-venona-meredith-solve-attempt.md`: *"Do **not** restart from Fraser or generate more generic Communist candidates. The task is now to prove or kill Meredith/Vernon."* A candidate field closed by fiat one day after the leading candidate appeared is the textbook form of stopping at the first plausible name.

4. **The two ledger queries aimed at the population the cable actually names were never executed.** `constraint-ledger.md` Q2 ("Who physically worked on the relevant horizontal/ASDIC production line in summer 1940?") and Q3 ("Who was the Communist Party Area Secretary in the Henry Hughes/Hainault/Ilford locality in Aug 1940?"). These target B6 and B4 — the two most discriminating constraints — and both populations are **small and enumerable**: a single works' wartime shop floor, and one named party official. They remain open.

**What a competing candidate set actually looks like**, scored on the ledger above rather than on narrative strength:

| | B4 CPGB branch embedding | B6 Hainault/Ilford shop-floor reach | B7 / B1 W/T + flat | Soviet-network evidence | Geography |
|---|---|---|---|---|---|
| **Meredith** | No — fellow-traveller, not a branch man known to local officers | **No** — Cricklewood NW2, aviation division, parent company only | No evidence of any kind | **Yes**, but 1936–39, Weiss *illegal* net, Paris controllers, **aeronautical** subjects | St Albans → Bishop's Cleeve; no Essex/east-London connection |
| **Fraser** | Yes — CPGB from 1926, Ilford/Goodmayes branch milieu | Same locality; Plessey Ilford; married an Ilford CPGB activist Oct 1940 | Electronics/evening-class training; later radar at Cossor | Springhall and Beurton edges; no proof | **Ilford** |
| **Barnard** | Yes — CPGB from 1933, workplace political role | **Plessey Ilford from Mar 1940**, "roving mathematician", "special types of radio sets" | Direct radio-production access | None found | **Ilford** |
| *Never enumerated:* Henry Hughes Hainault shop floor / AEU / CPGB | — | **by definition, exactly** | — | — | **Hainault** |
| *Never enumerated:* the Ilford/Essex Area Secretary's own contact circle | **by definition, exactly** | — | — | — | **Ilford** |
| *Never enumerated:* a residency-side reading of the No. 256 signature | — | — | — | — | — |

On the cables' own constraints, **Meredith ranks below two candidates the project had already generated**, and below two populations it identified but never enumerated. He leads on exactly one row — documented Soviet work — and that row is attested for the **wrong period** (1936–39), the **wrong network** (Weiss/"Harry II", an illegal line run from Paris, versus the 1940 legal residency under BARCh/Kremer), and the **wrong subject matter** (Queen Bee, bomb sights, aircraft stabilisation — his own speciality; BROWN's product is naval acoustics). If Meredith were BROWN, sitting inside Smiths' aviation division, the expected output is aviation-instrument intelligence. There is none in the BROWN traffic.

I will state the cost plainly, because it is the reason Meredith cannot stand: **the Smiths → Henry Hughes bridge is anti-selective.** The relation it establishes is "employed somewhere in the S. Smith & Sons group". Every one of the Hughes employees actually on the Hainault production line — the people No. 976's own words point at — satisfies that same corporate relation *and* satisfies B6 directly, which Meredith does not. A bridge that admits thousands and ranks its own nominee below the population it is competing against is not a narrowing.

There is also a tradecraft objection the claim never meets. B1 asks the GRU to install the London residency's clandestine transmitter **in a flat rented for BROWN**, and B4 then has BROWN gossiping about it to a party official. No service would site a transmitter with a high-value, uncompromised, nationally known senior aeronautical designer — the "Meredith effect" man, Chief Designer at Smiths — and no such man is plausibly the one who blabs to an Area Secretary. B1 and B4 describe a low-profile, locally embedded, technically handy party member. They describe Fraser's and Barnard's *class* of person. They do not describe Meredith.

### On POULTRY-DEALER = Vernon, I go further than the claim and further than validator 1

The candidate field for POULTRY-DEALER was generated from a **single feature**: "Osterley instructors" (`poultry-dealer-candidate-comparison.md` considers Vernon, Slater, Levy, Wintringham — all four Osterley men, and nobody else). That generator is unsound, for two reasons I established from the raw text:

- **The Wintringham datum is not discriminating.** No. 882 §6 has POULTRY reporting that someone *"has proposed to TOM WINTRINGHAM … that he should help them to organize a Republican group with a view to a rising against FRANCO"*, and adds that Wintringham "was expelled from the CORPORATION after his arrival from the south" and now works at a Home Guard school. That is CPGB and Spanish-exile political gossip, not Osterley-insider knowledge. Wintringham's expulsion and his school were common currency in Communist and Spanish-veteran circles, and the school was nationally famous through *Picture Post*. Any well-connected London party member could file that paragraph.
- **The Hounslow-geography argument does not survive POULTRY's own reporting range.** The same source files Hull and Bristol/Filton items at second hand and with inflated figures. He is not reporting his neighbourhood; he is reporting circulating rumour. And Vernon's own documented 1940 addresses point away: the Dulwich Society account (from his MI5 file) places him at **Crouch End** in January 1940 and in **Kensington/Pembroke Square** in March 1940 — north and west-central London, not Hounslow. The Vernon dossier grades "Hounslow geography — very strong"; on the evidence it is a workplace adjacency, not a residence, and it is doing no discriminating work.

Validator 1 calls the Osterley/Hounslow inference "a fair reading of the primary text". I think that is one notch too generous, and I record the difference. Vernon remains a *reasonable* POULTRY-DEALER candidate — his Jan 1940 Popov lunch and his real pre-war GRU history are genuine and I verified both — but he is the best of a four-man set generated from a non-discriminating feature, and the reporting fingerprint does not localise to him.

---

## Part 4 — my assigned angle (ii): covername semantics

**Direct answer: there is no positive reason whatever that BROWN/BRAUN maps to Meredith. The covername contributes exactly zero identifying information, and I can show this from the corpus rather than assert it.**

I inventoried all 45 glossed covernames in the London GRU traffic. They fall into two registers:

- **Descriptive nouns**, often transparent: SAUSAGE-DEALERS (Germans), CORPORATION (Communist Party), METRO (Soviet Embassy), MASTER (the Ambassador), FRIENDS (party members), MUSIC (W/T set), and the agent labels THERAPEUTIST, BUSINESSMAN, CARPENTER, WRITER, ADMINISTRATOR, MINISTER, NOBILITY, INTELLIGENTSIA, **POULTRY-DEALER**.
- **Bare personal names**: BARCh, BRION, DICK, JOHN, MARK, NIK, KLARK, MIM, MARY, MARTHA, ANDERS, STENLI, BAUER, **BRAUN**.

The decisive test is the second register's *resolved* cases, and the result is uniform:

| Covername | Identified as | Relation of covername to true name |
|---|---|---|
| BARCh | Simon Davidovich **Kremer** | none |
| ZhEROM (JEROME) | André **Labarthe** | none |
| BAUER | Lieut. **Hein**, Czech Army | none |
| MIM | *possibly* Mikhail Ivanovich **Mikhailov** | initial only, and hedged "possibly" |

**In this corpus, where a personal-name covername has been resolved, it bears no relation to the true name.** BRAUN therefore behaves as a null label. It cannot corroborate Meredith, Fraser, Barnard or anyone else; PROBLEM.md's own trap #2 already forbids arguing from the surname in the other direction. The entire mapping must be carried by constraint satisfaction — and Part 3 is where it fails.

Two further notes from the inventory. First, POULTRY-DEALER sits in the *descriptive* register alongside THERAPEUTIST, BUSINESSMAN and CARPENTER, which raises the possibility that these labels are occupation- or role-derived. I looked for a poultry, chicken or smallholding association for Vernon and **found none** in any source I could reach. So no positive hook exists on that side either. Second, the personal-name register is disproportionately the *Embassy/residency* register — BARCh, DICK, BRION, MIM, and MARK/NIK/KLARK who do the Embassy's photographic work in 798 §1. BRAUN sits in that register, and BROWN signs at No. 256 inside the officers' outgoing sequence. STENLI is a clear counter-example (a Canadian agent, £20 a month), so this is a tendency and not a rule — but it is a real pattern, it points at a hypothesis class the project never enumerated, and it is a further reason the covername gives no support to a British-industrial-source reading specifically.

---

## Part 5 — Meredith against the Falsifiable candidate standard

1. **alive/present in Britain in summer 1940** — **PASS.**
2. **plausible London/Essex geography** — **FAIL on the Essex/east-London limb.** Cricklewood NW2 is London, but it is the wrong division of the wrong site; Henry Hughes was at Hainault, Forest Gate and Ilford (Grace's Guide, verified). Meredith's attested residences are Hertfordshire (1939) and Gloucestershire (by May 1941). His Jul–Sep 1940 residence is unknown to the project and to me.
3. **access to or a direct contact inside Henry Hughes's echo-sounder work** — **FAIL.** Common ownership, verified; access, absent. No person, site, project, committee or document. The claim's own F2 concedes it.
4. **Communist/Soviet trust-network evidence consistent with No. 876** — **FAIL as against No. 876 specifically.** His Soviet work is real but belongs to a different period, a different network and a different subject. No. 876 requires branch-level CPGB embedding; Meredith is attested as a fellow-traveller, not as a man local party officers chatted to.
5. **ability to participate in clandestine W/T logistics / use of a flat** — **NOT MET**, and on the corrected reading of footnote [iv] the bar is higher than the project assumed: BROWN holds an illicit link and hosts it across two flats and three moves in six weeks.
6. **chronology consistent with all three messages** — **NOT DEMONSTRATED.** Nothing places Meredith in contact with Soviet intelligence in 1940. §6 of the dossier ("reconnected old source") is an unevidenced bridge and says so.
7. **no contradiction from occupation, military service, known residence or security files** — **NOT DEMONSTRATED.** No contradiction found; but the files that would supply one (KV 2/2199–2202) are unopened, so this cannot be scored as a pass.

One pass, six not met.

---

verdict: **PARTIAL**

## reasoning

**Why not PASS.** The Full-crack bar needs "documentary evidence tying that person to BROWN's Soviet/Communist network and explaining the Henry Hughes information channel." Neither exists, and the claim says so itself. The Strong-partial bar has three components:

- *"demonstrate which role model … best explains all three cables"* — **met.** The STANLEY role separation is real and reproduces off 798 §3–6, 816, 847 and 876 §1B: the operating role is STANLEY's, so BROWN need not be a radio technician, and an intermediary reading beats H1. This is the session's genuine result and it should stand as progress. My one amendment: with "illicit **link**" restored, BROWN is still attached to the set and the flat throughout, so the W/T constraint should not have been down-weighted as far as `stanley-role-separation.md` takes it.
- *"reduce the search to a small candidate set"* — **not met, and this is where my angle bites hardest.** The field was not reduced; it was *closed*. Fraser's kill test returned BLOCKED and he was demoted anyway, with no new evidence, the following day. Barnard's own prescribed program — enumerate the Ilford industrial-Communist network and intersect it with Hughes personnel — was dropped. Q2 and Q3 of the project's own constraint ledger, which target the two small enumerable populations the cables actually name, were never run. And the handoff instructs the next session in writing not to generate further candidates. Meanwhile the replacement narrowing device, the Smiths corporate bridge, admits thousands and ranks Meredith below the Hughes shop-floor population the cable points at.
- *"with at least one new archival/documentary link"* — **not met.** Everything load-bearing is published secondary material: Grace's Guide, three Wikipedia articles, a local-history society article, patent abstracts. KV 2/2199–2202 and KV 2/992–996 are unopened. No archive was touched.

**Why not FAIL.** Meredith is *unevidenced*, not *refuted* — I found nothing that contradicts him outright, and the two cheap tests that could kill him (his Jul–Sep 1940 address; a settled family residence in the MI5 reconstruction) have not been run. The board log is honest about its own status, labels the work provisional, lists its proof debt, and states plainly that no source says "BROWN = Meredith". Three components are genuinely sound and I verified them from raw evidence rather than from the writeup: the STANLEY role separation; the Smiths/Hughes corporate facts as facts; and Vernon's real pre-war GRU history and January 1940 Soviet Embassy contact. Per `VALIDATOR.md`, an explicitly speculative hypothesis failing its test can be good research, and this is closer to that than to a bad claim.

**The failure mode worth recording for the board.** The Meredith case is built by *substitution*, not by elimination. Fraser and Barnard satisfied the cables' hard local constraints (Ilford geography, branch CPGB, radio-production competence) but lacked a Soviet-intelligence edge. Meredith had the Soviet edge but satisfies none of the local constraints. Rather than treating that as evidence that **the right candidate has both** — i.e. that the search should continue into the Hainault/Ilford population where both properties could coexist — the project swapped the constraint set for the one its new candidate met, and closed the field. The Smiths acquisition is a real fact that arrived looking like a bridge and functioned as a permission slip.

## dissent

I reach the same verdict as validator 1 and, on two textual points, the same findings. I want the panel record to show three things.

1. **Our agreement on the two text corrections is weaker evidence than it looks.** V1 and I used the same two sources and near-identical hand-rolled extraction routes, in the same environment, against the same 403. That is precisely the correlated-error channel `VALIDATOR.md` warns about. The "illicit **link**" reading I regard as settled, because it is legible in the magnified page image *and* because the cross-reference to No. 798 only coheres under it. The leak-reading of "a MUSIC from BROWN" I regard as the better English reading but genuinely uncertain without the Russian, and I would not want a future session to treat it as established.

2. **I dissent from validator 1, mildly, on POULTRY-DEALER.** V1 writes that "the Osterley/Hounslow inference … is a fair reading of the primary text". I do not think the Hounslow limb survives contact with POULTRY's own reporting range — Hull, and a Filton raid reported at second hand with every figure wrong — or with Vernon's documented 1940 addresses at Crouch End and Kensington. Vernon stays a reasonable candidate on his Soviet history and his July 1940 Osterley post; but the geography argument should be struck, and the candidate set should not have been generated from Osterley staff lists in the first place.

3. **If either other validator returns PASS**, my objection is Part 3: the candidate field was closed by written instruction one day after Meredith appeared, with Fraser's kill test explicitly unresolved and the two most discriminating enumerable populations never enumerated, while the bridge that replaced them ranks Meredith below the Henry Hughes staff whom the cable's own "direct from the production line" wording names. A named-person identification cannot be built on a corporate relation that its own nominee satisfies worse than the population he is competing with. **If either returns FAIL**, I dissent the other way: the STANLEY role separation is a real reproducible result on the Strong-partial bar's second component, and the two textual corrections should be carried into `PROBLEM.md` and `constraint-ledger.md` by whoever holds the pen — the project has been working from a transcription error and a paraphrase that softened the hardest constraint.

**Cheapest next tests, from my angle** (offered as specification, not wish-list): (a) run ledger **Q3** — name the CPGB Area Secretary for the Ilford/Hainault area in Aug 1940 from CPGB/MI5 records; that is *one person*, and his contact circle is the smallest set that satisfies B4. (b) Run ledger **Q2** — build the 1939 Register occupational list for the Hughes Hainault/Forest Gate works; that population is small, enumerable, and is the only one that satisfies B6 directly. (c) Re-open Fraser and Barnard at the same budget Meredith received, since neither was refuted. (d) Enter Meredith into `analysis/network-intersection-1940.md`, which still has no row for him.

status: **HELD — awaiting human sign-off.**

---

## Verification ledger

| Source / item | Status |
|---|---|
| Wilson Center aggregate PDF (`Venona-London-GRU.pdf`, 564 KB), downloaded and text-extracted in full | **VERIFIED** |
| London No. 798, 22 Jul 1940 (3/PPDT/T30), read in full with all 14 footnotes | **VERIFIED** |
| London No. 876, 13 Aug 1940 (3/PPDT/T45), read in full with all 10 footnotes | **VERIFIED** |
| London No. 976, 4 Sep 1940 (3/PPDT/T50), read in full with footnotes | **VERIFIED** |
| POULTRY-DEALER corpus: Nos. 882 (14 Aug), 1112 (4 Oct), 1141 (9 Oct) | **VERIFIED** |
| Residency outgoing-number series reconstructed (205→259; 255 BARCh / 256 BROWN / 259 BARCh) | **VERIFIED** — PROBLEM.md's "No. 256" trap note confirmed; BROWN sits inside the officers' sequence |
| Covername register inventory, 45 glossed covernames across the corpus | **VERIFIED** |
| Resolved personal-name covernames: BARCh=Kremer, ZhEROM=Labarthe, BAUER=Lieut. Hein, MIM=possibly Mikhailov | **VERIFIED** — none bears any relation to the true name |
| NSA scan of No. 976, direct from `media.defense.gov` | **BLOCKED** — HTTP 403 through the agent proxy |
| NSA scan of No. 976 via Wayback; `DCTDecode` JPEG extracted and read as an image; footnote line cropped and 5× upscaled | **VERIFIED** — reads "illicit **link**"; footnotes [ii] and [iii] blank in the original |
| Smiths controlling interest in Henry Hughes & Son, 1935 | **VERIFIED** — Grace's Guide: "1935: Controlling interest in the company was acquired by Smiths" |
| Henry Hughes works at Forest Gate, Ilford; new works at Hainault (1919); office 59 Fenchurch St | **VERIFIED** — Grace's Guide |
| Meredith left RAE April 1938; Smiths Aircraft Instrument, Cricklewood, head of Physics and Instruments, title Chief Designer | **VERIFIED** — Wikipedia, *Frederick William Meredith* |
| Meredith's Soviet work dated **1936–1939** via Weiss/"Harry II"; subjects Queen Bee, bomb sights, stabilisation; MI5 opened 30 Jan 1948 from the Robinson papers; Skardon interview 6 Jan 1949 | **VERIFIED** — Wikipedia, *Frederick William Meredith* and *Ernest David Weiss* |
| Weiss network ran early 1930s–1941; Weiss interned Oct 1940, released Dec 1940 | **VERIFIED** — Wikipedia, *Ernest David Weiss* |
| Meredith ↔ Henry Hughes / Sproule / marine acoustics / Hainault, any date, any form | **NOT FOUND** |
| Meredith's residence Jul–Sep 1940 | **NOT FOUND** — unestablished by the claim and by me |
| Meredith 1940 address via GB patent front page (GB591758A and related Meredith/Cooke/S. Smith filings) | **BLOCKED** — Espacenet 403, Google Patents 503 through the proxy, to both WebFetch and curl. This remains the cheapest untried kill test |
| Vernon at Osterley Park from July 1940 alongside Wintringham; explosives instructor | **VERIFIED** — Wikipedia, *Wilfrid Vernon*; Dulwich Society (via Wayback), quoting Purcell |
| Vernon: MI5 recorded Jan 1940 lunch in Kensington with Ivan Popov, 2nd secretary, Soviet Embassy; postal warrant; living at **Crouch End** | **VERIFIED** — Dulwich Society (via Wayback) |
| Vernon dismissed from RAE 1937; admitted a **pre-war** Soviet ring to Skardon, Feb 1952 | **VERIFIED** — Wikipedia, *Wilfrid Vernon* |
| Weiss/Vernon/Meredith collaboration dated "**1936 and 1937**" | **VERIFIED** — Dulwich Society (via Wayback). Note: that article names him "Frederick **Stephen** Meredith", not William — the secondary chain is loose |
| "Vernon said Meredith recruited him" | **PARTIALLY VERIFIED** — the collaboration is attested; the *recruitment* direction I could not confirm in any source I reached |
| Vernon ↔ poultry / chickens / smallholding (covername semantic hook) | **NOT FOUND** — searched; no association located |
| Dulwich Society article, live site | **BLOCKED** — HTTP 202 with an empty body; recovered via Wayback. Single popular secondary source for the whole Vernon-1940 evidence base |
| Filton / Bristol Aeroplane Co. raid, 25 Sep 1940: ~57 He111s, 168 bombs, 132 killed (91 workers), shelter hit | **VERIFIED** — IWM and Battle of Britain timeline; compare POULTRY's "80 aircraft / 200 bombs / 123 killed / two workshops slightly damaged" |
| A published identification of BROWN/BRAUN or POULTRY-DEALER anywhere in the literature | **NOT FOUND** — searched; NSA/Wilson Center annotations still read "Unidentified covername" |
| TNA KV 2/2199–2202 (Meredith), KV 2/992–996 (Vernon) | **UNVERIFIED** — not consulted by the claim or by me |
| TNA HS 9/1401 (Sproule, SOE personnel series) | **UNVERIFIED** — not consulted |
| 1939 Register, "Old Brew House, St Albans" | **UNVERIFIED** — subscription source; not checked; not relied on above |
