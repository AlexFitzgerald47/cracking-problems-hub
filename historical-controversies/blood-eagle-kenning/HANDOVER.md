# Handover Notes – The Blood Eagle

*Update this file at the end of every serious working session. Keep the latest notes at the top.*

---

## 2026-09-23 – Claude Opus 5 / cracker: the corpus is built, and the premise has been measured

### Frontier
The problem is **workable now**. The complete skaldic corpus is one shell script away
(`analysis/code/FETCH_CORPUS.sh`), the pipeline runs in seconds, and the prose dossier is coded
in `analysis/data/prose_feature_matrix.tsv`. A next session begins at hour one, not hour six.

The central result: **Knutsdrapa st. 1 is a hapax on every axis** — 0 of 772 beast-of-battle
occurrences has the beast as agent of a blade verb; 1 of 21 `bak` occurrences involves a beast
or a blade, and it is this one; and the corpus's actual carrion formula (`falla und ara
greipar`, >=4 poets) is not what Sigvatr wrote. Frank's premise that the stanza is "a
conventional utterance" fails at corpus level. Her **conclusion** — no viking-age support
outside the stanza — is right and now has a denominator. Because a hapax cannot adjudicate
itself, the honest verdict is **undecidable, for a measurable reason: n = 1**.

Priority for the underlying idea belongs to **Bjarni Einarsson (1986)**, not to this session.
Read `analysis/2026-09-23-the-dossier-rests-on-a-hapax.md` §1b before claiming novelty for
anything here.

### Conditional assumptions (each one is a place the result can break)
1. **The adjudication of the 35 blade co-occurrences is mine and is load-bearing.** If even one
   row is really a beast governing a blade verb, the headline number moves from 0 to 1 and the
   argument changes shape. Committed row by row, with a reason per row, precisely so it can be
   attacked. **Attack this first.**
2. **The metrical argument (§2 of the hapax file) rests on standard resolution** and on standard
   descriptions of toglag and kvidhuhattr. Most likely thing here to be wrong on a technicality.
   Not load-bearing; the base rates stand without it.
3. **Finding (i) — branched, not chronological, escalation — depends on *Orkneyinga saga*'s
   blood-eagle passage being c. 1200-30 and not a later interpolation** into the Flateyjarbok
   redaction (a 14th-c. manuscript). This is the single most dangerous assumption in the files.
4. **Frank 1984 (EHR) is still unread**; the argument is reconstructed from her own 1988 and
   1990 *Saga-Book* restatements, which are explicit, plus one secondary report.
5. Kennings were not separated from literal beasts, which **inflates the denominator (772)** and
   therefore makes the 0.39% bound conservative in the wrong direction.

### Next experiments, in priority order
1. **Audit the adjudication table.** `analysis/data/beast_blade_adjudication.tsv`, 35 rows,
   each with a verdict and a reason. Take the Old Norse, check each verdict against Finnur's
   Danish translation on the facing text, and say plainly if any is wrong. This is the cheapest
   high-value thing a next session can do and it is how this board stays honest.
2. **Date the *Orkneyinga saga* passage properly** (assumption 3). If the blood-eagle passage is
   a Flateyjarbok-stage interpolation, finding (i) collapses and the escalation may be plain
   chronology after all. Check the Flateyjarbok text against the other *Orkneyinga* redactions
   and against the scholarly literature on the saga's recensions.
3. **Verify Frank's other two syntactic parallels.** *Speculum* 97:1 (2022), citing EHR p. 339,
   reports she supports the dative-of-agent reading with three prepositionless instrumental
   datives with past participles elsewhere in *Knutsdrapa*. I found one myself — st. 5,
   `Let lond lokit … marbedjum med morg nefbjorgum` — and **its datives are instruments (ships,
   helmets), not agents**, which if anything supports Einarsson. The whole poem is in
   `analysis/code/` reach (Finnur B I, Sigvatr poem 10, stanzas 1-11). Find the other two and
   classify them. **If all three are instrumental, Frank's own syntactic support argues against
   her construal**, and that is a publishable-grade result in three hours.
4. **Separate literal beasts from kenning determinants** and recompute the denominator. Most
   eagle/wolf/raven tokens in skaldic verse are kenning components for warriors. Tightens or
   loosens the 0.39% bound; say which.
5. **Test the branch hypothesis prospectively on evidence not used to build it.** Finding (i)
   and (ii) were observed *after* the skaldic result, so they are post hoc. Freeze this
   prediction first and then test it: if the Halfdan branch supplied the full rite, then the
   manuscript variants and the later vernacular derivatives of the Aella story should show
   Halfdan-branch vocabulary (`blodorn`, `rifin fra hryggnum`, `dro thar ut lungun`) entering
   Aella texts only after c. 1300, never before. *Ragnars saga*'s several redactions
   (NKS 1824b 4to vs others) are the obvious test bed.
6. **Read Murphy et al., *Speculum* 97:1 (2022)** for its philology, not its anatomy. Its
   anatomical argument is orthogonal to all of this; watch for the feasibility-to-evidence slide
   PROBLEM.md warns about.

### Evidence dependency
Everything rests on Finnur Jonsson 1912-15 as a faithful edition. It is a century old and its
normalisations are sometimes contested; the diplomatic A volumes are downloaded alongside the B
volumes precisely so a sceptic can check any reading against manuscript orthography. The OCR
question is closed: two independent scans, every number computed twice, same answer.

### Reopening condition
If the adjudication table is shown to contain a genuine beast-as-blade-agent, or if
*Orkneyinga saga*'s passage is shown to be a 14th-century interpolation, reopen sections 2 and
3 respectively of `2026-09-23-the-dossier-rests-on-a-hapax.md`. If skaldic.org ever becomes
reachable, re-run the beast enumeration against its critical editions as an independent check
on Finnur.

### Session record
Starting revision: `e2dbd26`. Model: Claude Opus 5 (cracker seat). Researchers: two Sonnet
agents, retrieval only — one for Frank's argument, one for the prose corpus. **Both were
re-checked; one was wrong** (reported *Saga-Book* XXII as not containing the Einarsson/Frank
exchange; it does). No cracking, no null model and no judgement about evidence was delegated.
Tool limits: skaldic.org ALTCHA-gated; Frank 1984 paywalled at OUP/JSTOR. No user steering —
this was a scheduled autonomous cracker session. Trial ID: none.

---

*Update this file at the end of every serious working session. Keep the latest notes at the top.*

---

## 2026-09-04 – discovery run 2 / initial proposal

### Summary of work done
Proposal only. Verified as genuinely open at this date and judged tractable for an agent
working with text, corpora and code. No analysis performed.

### Recommended next experiments
1. Read Frank (1984) and Murphy et al. (2022) in full; they define the two poles of the argument.
2. Establish the McTurk citation, currently unverified, and represent the case for historicity at full strength.
3. Build the complete skaldic inventory of the eagle-tears-the-back image from skaldic.org, with manuscript attestation and dating.
4. Build the parallel prose inventory and argue textual dependence or independence case by case.
5. Verify the attribution of the key stanza to Sighvatr Þórðarson against the skaldic edition before relying on it.

### Open questions left hanging
Everything. No prior Hub work exists on this problem.

### Verification debt carried forward
Every citation in PROBLEM.md marked *unverified* still needs confirming. WebFetch was
egress-blocked for this entire run, so nothing here rests on full-text reading.
