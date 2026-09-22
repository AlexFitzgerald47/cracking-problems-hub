# Finder pass — 2026-09-22 — filling the standing gaps

**Role:** Finder. **Brief:** four new proposals, deliberately targeting the three gaps the
task named as under-served: early modern/modern Ireland, contested claims propagated through
a century of citation, and non-Western material generally.

## How this batch was produced

Read `AGENT_INSTRUCTIONS.md`, `_roles/FINDER.md`, `_templates/DISCOVERY_BRIEF.md`,
`STATUS.md`, `_roles/README.md`, and every file in `discovered/_manifest/` (nine prior
manifests) before starting, specifically to build an exclusion list and to see which domains
recent runs already covered so this run could rotate elsewhere.

Four sonnet subagents were used as researchers, run in **two small batches of two** rather
than a single fan-out, following the explicit operational lesson recorded in
`discovered/_manifest/swarm-discovery-2026-09-04.md` and
`discovered/_manifest/discovery-2026-09-04-run2.md` (a seven-way fan-out previously died on a
rate limit and produced nothing; two-at-a-time batches worked). Each researcher was given the
brief's bar, a domain-specific exclusion list drawn from the prior manifests, and an explicit
instruction never to invent a citation.

**No candidate was accepted on a researcher's word.** For all four selected candidates, the
coordinating session independently re-fetched or re-searched the load-bearing primary sources
itself before writing anything to disk — not merely re-reading the subagent's citation list,
but pulling the actual pages (IACR's two Chinese-gold-bar pages, Farmer's 1896 text, the
Wikipedia article on the ballad, both Conversation articles on the Singapore Stone, and the
Dodds Pennock 2012 abstract page) and checking what they actually say. Two errors were caught
this way: a subagent's guess at a book's publisher (Lilliput Press) was wrong (it is Blackstaff
Press, confirmed via bookseller records), and a claimed "very flat" letter-frequency statistic
for the gold-bar cryptograms could not be found on the primary transcription page and is now
flagged unverified rather than asserted.

## Proposals in this batch

| Slug | Named unknown | Category | Corpus status | Difficulty / tractability |
|------|---------------|----------|----------------|---------------------------|
| `larry-was-stretched-authorship` | Who wrote the 1789 Dublin Newgate-cant ballad "The Night Before Larry Was Stretched"? Farmer (1896) already rejected the traditional Burrowes attribution and named no confirmed author; no modern reassessment found. | ireland | Partially exists — period printings (1789 *Festival of Anacreon*, 1828 *Universal Songster*, Farmer 1896) are digitized or reprintable; candidate writing samples for comparison are uneven (Curran's corpus is large, Maher's may not exist at all). | Moderate / **good** — no archive access needed |
| `chinese-gold-bar-cipher` | What do the 16 transcribed Latin-letter cryptograms on a set of purportedly-1933 Shanghai gold bars encode, and are the bars authentic or a later fabrication? Unsolved as of today per the hosting page's own statement. | ciphers | **Already exists and is machine-readable** — 16 strings transcribed and public on IACR's own pages, fetched and confirmed directly. | High / **good for a bounded first pass** — small, public, no archive access needed |
| `singapore-stone-kallang-inscription` | What language and script underlie the surviving fragment of the Singapore Stone (destroyed 1843/1848), whose script resembles but does not match known Kawi variants? Still described as unresolved in March 2026 coverage, confirmed by direct fetch. | historical-texts | **Must be built** — no standardized digital sign-inventory exists yet; raw materials (photographs, 19th-c. engravings, comparative Kawi corpora) are online but scattered. | Very high for full decipherment / **moderate** for a bounded comparative-paleography sub-question |
| `templo-mayor-1487-sacrifice-count` | Does the widely-repeated 80,400 figure for the 1487 Templo Mayor dedication sacrifice (Durán, also in Ixtlilxóchitl and Mendieta) reflect a real transmitted count, or is it chronicler embellishment — and are the three chroniclers independent or copying each other? No textual-filiation study of this specific lineage was located. | historical-controversies | Largely exists — all three chroniclers have modern translated/edited texts; the specific passages have not yet been located and compared. | High for the "true count" (unanswerable) / **good** for the actually-crackable filiation question |

## Candidates investigated and rejected this run

Recorded so future runs do not re-propose them.

**Ireland lane:**
- **"The Man from God-Knows-Where"** (unidentified United Irishman before the 1798 Battle of
  Ballynahinch) — rejected. Direct verification shows the poem's subject is Thomas Russell, a
  well-documented, famous United Irishman hanged in 1803 at Downpatrick, not a genuine
  unidentified person. Fails both the named-unknown test and the not-too-famous test.
- **The Composition of Connacht (1585)** — rejected. Its open questions are interpretive/
  historiographical rather than a concrete named unknown.
- **The Union Star (1797) masthead editorship** — rejected. Editorship is already reasonably
  attributed in standard scholarship to Walter "Watty" Cox.
- **Authorship of "A Light to the Blind"** (c. 1711 Jacobite prose narrative, traditionally but
  doubtfully credited to Nicholas Plunkett of Dunsoghly) — investigated, genuinely open
  (Gilbert 1892; P. Kelly, *Irish Historical Studies* 24 (1985), 431–62; UCC's CELT hosts a
  partial electronic edition, text ID E703001-001), and **held over rather than rejected**: a
  solid second candidate for this lane, corpus-poorer than `larry-was-stretched-authorship`
  (CELT's edition is described as partial, and the Bodleian Carte MS 229 copy is incomplete),
  but genuinely promising for a future pack.
- **Authorship of "Pairlement Chloinne Tomáis" Part I** (c. 1610–15 Irish-language satire,
  possibly by a member of the Ó Duinín learned family) — investigated, genuinely open (Williams
  1981 critical edition, DIAS; de Barra 1992, *Studia Hibernica* 26; Caball 1993, *Éigse* 27),
  and **held over**: real and obscure, but the critical edition is print-only, manuscript
  images would need pulling from Irish Script on Screen (ISOS), and progress depends on
  Early Modern Irish philology and paleography — a higher-effort, more specialist target than
  the two above. Note Part II (post-1660, Leinster) is a distinct authorship problem not
  investigated here.

**Non-Western cipher lane:**
- **Ottoman diplomatic ciphers (Ibrahim Afif Effendi's correspondence)** — not re-investigated;
  already correctly on the rejected-for-access-only list per `discovery-2026-09-04-run2.md`,
  and no evidence of new public digital access was sought or found this run. Left standing as
  "revisit if the Hub acquires archive access."
- **Uesugi/Sengoku-era Japanese cipher** — rejected. A documented, fully reconstructed cipher
  *system* (an Iroha-based Polybius square); Wikipedia's own article notes it is not even
  established that Uesugi actually used it, and no genuine surviving unsolved ciphertext exists
  — it appears on unsolved-cipher listicles but does not meet this Hub's bar. Flagged explicitly
  so a future run does not inherit the listicle framing uncritically.
- **Qajar Persian *Meftah al-Romuz*** — rejected. A documented cryptography manual (per
  Encyclopaedia Iranica's "Codes" article), not a surviving encrypted message. Nothing to
  decrypt.
- **Ibn al-Durayhim's Arabic cryptology manuscripts** — rejected. Already rediscovered,
  transcribed and published by Mrayati's team (Damascus, rediscovered 1979, published 1987).
  Solved historical documents *about* cryptography, not unsolved ciphertexts.
- **Mughal/Maratha espionage "gupchup" coded messages** — held over, not rejected. Well
  documented that such networks existed, but no specific surviving unsolved document was
  located in public sources without archive access; a real gap rather than a findable
  candidate this run.
- **Korean, Vietnamese and Ethiopian historical cipher traditions** — searched and confirmed
  empty as of this run (no verifiable named unsolved cipher document found in scholarship or
  in cipher-community sources such as Elonka Dunin's list or *Cryptologia* coverage). Recorded
  as a searched-and-empty gap rather than left as simply unexplored.

**Citation-chain lane:**
- **Mansa Musa's gold "crashing Cairo's economy for 12 years"** — rejected, already closed.
  Warren Schultz, "Mansa Musa's Gold in Mamluk Cairo: A Reappraisal of a World Civilizations
  Anecdote," *Mamluk Studies Review* V (2001), University of Chicago — shows the real effect
  was a modest, temporary silver/gold exchange-rate shift (25:1 to 20:1) within normal
  historical fluctuation, one contributing factor among several, not a 12-year hyperinflation.
  Academically closed; only popular culture has not caught up, which does not meet the bar.
- **Genghis Khan's "greatest happiness is to vanquish your enemies" quote** — investigated,
  genuinely open, and **held over rather than rejected** (see `templo-mayor-1487-sacrifice-
  count/PROGRESS.md` for detail). A clean, fully text-based citation-chain candidate tracing
  through Harold Lamb's 1927 popular biography and, further back, claimed descent from Rashid
  al-Din's *Jami' al-Tawarikh* — not used this run only because one citation-chain slot was
  budgeted and the Templo Mayor candidate was judged to have higher stakes (a statistic still
  used in serious popular history and some textbooks, not just quote-aggregator sites). Strong
  candidate for a future pack; the coordinating session's own quick check already found the
  popular modern wording diverges from Lamb's actual 1927 text, suggesting more than one
  transmission line worth untangling.

**Non-Western/South Asian script lane:**
- **Old Turkic runiform sign-value disputes (Talas and Yenisei basins)** — investigated,
  genuinely open, **held over rather than rejected**. A comparative corpus already exists
  (Uppsala's Database of Turkic Runiform Inscriptions, `runiform.lingfil.uu.se`, with photos
  and transliterations), making a narrow, falsifiable sub-question tractable — but the "named
  unknown" is diffuse (many individual disputed sign values rather than one clean puzzle), and
  the specialist literature is heavily Russian- and Turkish-language, adding real research
  overhead. Worth a dedicated future pass if the board wants a second Central Asian entry.
- Every item on the exclusion list supplied to the script-lane researcher (Indus, Rongorongo,
  Khitan, Libyco-Berber, Batak pustaha, Nsibidi, the Lane-B "SELECT" items from the 2026-09-05
  five-lane run, Jurchen, Bamum/Vai/Bassa Vah, Cascajal, Issyk) was confirmed still correctly
  excluded; none were re-investigated for possible reopening this run.

## Domains this run did not reach

- **Central Asian material beyond the Talas/Yenisei backup** — Tangut-adjacent minor corpora,
  Tocharian-adjacent puzzles, and Sogdian epigraphy were named as possibilities in the research
  brief but not actually investigated once the Singapore Stone candidate was confirmed strong
  enough to lead with.
- **South Asian scripts proper** (as opposed to the Southeast Asian Singapore Stone) — Brahmi-
  variant inscriptions, Bronze Age South Asian seals, South Indian cave-inscription disputes
  were named as possibilities but not actually investigated this run.
- **Irish-language sources on the plantation and Famine periods** — still flagged as under-
  represented across multiple prior manifests; this run's Ireland candidate (an English-
  language Dublin ballad) does not close that gap. `Pairlement Chloinne Tomáis` (held over
  above) is the closest this run came, and it is Irish-language, early 17th century — a future
  session could prioritize it specifically to address this standing gap.
- **A second, independently-verified non-Western citation-chain case** beyond the one proposed
  and the one held over — the brief asked for breadth here and this run produced depth on two
  candidates instead of a wider sweep.
- **Physical archive-access-gated Ottoman, Mughal court, and Central Asian cipher material** —
  not re-investigated for new public access; a future run with confirmed new digitization
  should revisit the Ottoman case specifically, since prior manifests already flag it as "the
  best candidate on the reject list."

## A note on verification standard

Unlike the 2026-09-04 run-2 batch, `WebFetch` was available throughout this run and was used
directly by the coordinating session on every load-bearing source before it was written into a
`PROBLEM.md` — not merely on abstracts or search-index records. Where a detail could not be
independently confirmed this way (a specific page number, a chapter, a secondary book's exact
content), it is marked "unverified" in place in each `PROBLEM.md` rather than asserted, per the
brief's explicit instruction that marking something unverified is always acceptable and
asserting it is not.
